import argparse
import dataclasses
import sys
import tempfile
from collections.abc import Callable, Iterator, Sequence
from contextlib import contextmanager
from pathlib import Path
from typing import cast, TypeAlias

from pre_commit import git
from pre_commit.all_languages import languages
from pre_commit.clientlib import load_config
from pre_commit.color import add_color_option
from pre_commit.error_handler import error_handler
from pre_commit.hook import Hook
from pre_commit.logging_handler import logging_handler
from pre_commit.main import _add_config_option, _add_run_options
from pre_commit.repository import all_hooks, install_hook_envs
from pre_commit.store import Store

from pre_commit_run_hook_entry import __prog__


# Constants
ARG_CONFIG = "--config"
ARG_DIFF = "--diff"
ARG_QUIET = "--quiet"
ARG_STDIN = "-"
ARG_BREAK = "--"
CHUNK_SIZE = 4096
HOOK_BLACK = "black"

# Type aliases
Argv: TypeAlias = Sequence[str]


# Dataclasses
@dataclasses.dataclass(frozen=True, kw_only=True)
class HookContext:
    hook: str
    extra_args: Argv
    tmp_path: Path | None = None


# Private functions
def find_file(file_name: str, /, *, path: Path | None = None) -> Path | None:
    if path is None:
        path = Path.cwd()
    maybe_file = path / file_name
    if maybe_file.exists():
        return maybe_file.absolute()
    if path.parent != path:
        return find_file(file_name, path=path.parent)
    return None


def find_hook(args: argparse.Namespace, store: Store, /) -> Hook:
    config = load_config(args.config)
    hooks = [
        hook
        for hook in all_hooks(config, store)
        if not args.hook or hook.id == args.hook or hook.alias == args.hook
        if args.hook_stage in hook.stages
    ]

    if not hooks:
        raise ValueError(
            f"No hook with id `{args.hook}` in stage `{args.hook_stage}`"
        )

    install_hook_envs(hooks, store)
    return hooks[0]


def get_args(argv: Argv, /) -> tuple[str, Argv]:
    if ARG_BREAK not in argv:
        return (argv[0], argv[1:])

    idx = argv.index(ARG_BREAK)
    if idx == 1:
        return (argv[0], argv[2:])

    next_idx = idx + 2
    return (argv[idx + 1], [*argv[:idx], *argv[next_idx:]])


def get_pre_commit_args(
    hook: str, /, *, config: Path | None = None
) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    add_color_option(parser)
    _add_config_option(parser)
    _add_run_options(parser)

    args = [hook]
    if config:
        args += ["--config", str(config)]

    return parser.parse_args(args)


@contextmanager
def hook_context(argv: Argv, /) -> Iterator[HookContext]:
    hook, extra_args = get_args(argv)

    tmp_path: Path | None = None
    if ARG_STDIN in extra_args:
        tmp_path = redirect_stdin_to_temp_file()
        extra_args = list(extra_args)
        extra_args[extra_args.index(ARG_STDIN)] = str(tmp_path)

    try:
        yield HookContext(hook=hook, extra_args=extra_args, tmp_path=tmp_path)
    finally:
        if tmp_path:
            tmp_path.unlink()


def patch_hook(
    hook: Hook,
    /,
    *,
    extra_args: Argv | None = None,
    entry: str | None = None,
) -> Hook:
    patched = hook._asdict()

    if extra_args:
        patched["args"].extend(extra_args)
    if entry:
        patched["entry"] = entry

    return Hook(**patched)


def redirect_stdin_to_temp_file() -> Path:
    tmp_file = tempfile.NamedTemporaryFile(
        prefix="pcrhe", mode="w+", delete=False
    )
    tmp_file.write(sys.stdin.read())
    return Path(tmp_file.name)


def run_hook(hook: Hook, /, *, color: bool) -> tuple[int, bytes]:
    language = languages[hook.language]
    with language.in_env(hook.prefix, hook.language_version):
        return cast(
            "tuple[int, bytes]",
            language.run_hook(
                hook.prefix,
                hook.entry,
                hook.args,
                [],
                is_local=hook.src == "local",
                require_serial=hook.require_serial,
                color=color,
            ),
        )


def usage() -> int:
    print(f"Usage: {__prog__} HOOK ...", file=sys.stderr)
    raise SystemExit(1)


# Main entrypoints
def main(
    argv: Argv | None = None,
    /,
    *,
    pre_commit_config_yaml: Path | None = None,
    hook_entry_func: Callable[[Hook], str] | None = None,
    tmp_path_func: Callable[[Path], None] | None = None,
) -> int:
    if argv is None:
        argv = sys.argv[1:]

    if not argv:
        return usage()

    with hook_context(argv) as ctx:
        hook_name, extra_args, tmp_path = dataclasses.astuple(ctx)
        if hook_name.startswith("-"):
            return usage()

        pre_commit_args = get_pre_commit_args(
            hook_name, config=pre_commit_config_yaml
        )

        with error_handler(), logging_handler(pre_commit_args.color):
            git.check_for_cygwin_mismatch()

            store = Store()
            with store.exclusive_lock():
                store.mark_config_used(pre_commit_args.config)

            hook = find_hook(pre_commit_args, store)
            retcode, out = run_hook(
                patch_hook(
                    hook,
                    extra_args=extra_args,
                    entry=hook_entry_func(hook) if hook_entry_func else None,
                ),
                color=pre_commit_args.color,
            )

            if tmp_path and tmp_path_func:
                tmp_path_func(tmp_path)

            sys.stdout.buffer.write(out)
            sys.stdout.buffer.flush()

            return retcode


def main_black(argv: Argv | None = None, /) -> int:
    """Special case for run black pre-commit hook for `sublack`_ needs.

    Unlike other Sublime Text 3 plugins, sublack calls ``black_command`` from
    file directory, not from project root. As well, as unlike black integration
    for VS Code sublack expects on whole formatted file by default, not on
    their diff.

    That results in necessity of,

    - Finding root ``.pre-commit-config.yaml`` file for pre-commit
    - Finding root ``pyproject.toml`` file for black config
    - Print content of tmp path into stdout

    .. _sublack: https://github.com/jgirardet/sublack
    """

    def print_tmp_path(tmp_path: Path) -> None:
        # TODO: Print file content by chunks
        sys.stdout.buffer.write(tmp_path.read_bytes())

    # Setup black arguments
    args = [HOOK_BLACK, ARG_BREAK, "--quiet"]

    pyproject_toml = find_file("pyproject.toml")
    if pyproject_toml:
        args += [ARG_CONFIG, str(pyproject_toml)]

    args += argv or sys.argv[1:]

    # Special case of calling ``pre-commit-run-hook-entry``
    pre_commit_config_yaml = find_file(".pre-commit-config.yaml")
    return main(
        args,
        pre_commit_config_yaml=pre_commit_config_yaml,
        tmp_path_func=print_tmp_path,
    )


def main_which(argv: Argv | None = None, /) -> int:
    """Find out hook entry full path.

    This is useful for cases, when ``pre-commit-run-hook-entry`` cannot be used
    as command for text editor formatting / linting tool, such as for
    `SublimeLinter-eslint
    <https://github.com/SublimeLinter/SublimeLinter-eslint>`_.

    In that case, you need to run,

    .. code-block:: bash

        pre-commit-which-hook-entry HOOK

    and then paste output into tool config.
    """

    def which_entry(hook: Hook) -> str:
        return f"which {hook.entry}"

    return main(argv, hook_entry_func=which_entry)
