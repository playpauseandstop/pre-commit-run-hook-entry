import argparse
import os
import sys
import tempfile
from contextlib import contextmanager
from pathlib import Path
from typing import cast, Iterator, NamedTuple, Optional, Sequence, Tuple

from pre_commit import git
from pre_commit.clientlib import load_config
from pre_commit.error_handler import error_handler
from pre_commit.hook import Hook
from pre_commit.languages.all import languages
from pre_commit.logging_handler import logging_handler
from pre_commit.main import (
    _add_color_option,
    _add_config_option,
    _add_run_options,
)
from pre_commit.repository import all_hooks, install_hook_envs
from pre_commit.store import Store


ARG_DIFF = "--diff"
ARG_STDIN = "-"
ARG_BREAK = "--"
HOOK_BLACK = "black"

Argv = Sequence[str]

__prog__ = "pre-commit-run-hook-entry"
__author__ = "Igor Davdenko"
__license__ = "BSD-3-Clause"
__version__ = "1.0.0a0"


class HookContext(NamedTuple):
    hook: str
    extra_args: Argv
    tmp_path: Optional[Path] = None


def find_hook(args: argparse.Namespace, store: Store) -> Hook:
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


def get_args(argv: Argv) -> Tuple[str, Argv]:
    """
    >>> get_args(["black"])
    ("black", [])
    >>> get_args(["mypy", "+"])
    ("mypy", ["+"])
    >>> get_args(["black", "--", "--diff", "--quiet", "file.py"])
    ("black", ["--diff", "--quiet", "file.py"])
    >>> get_args(["--diff", "--quiet", "file.py", "--", "black"])
    ("black", ["--diff", "--quiet", "file.py"])
    >>> get_args(["--format", "default", "--", "flake8", "-"])
    ("flake8", ["--format", "default", "-"])
    """
    if ARG_BREAK not in argv:
        return (argv[0], argv[1:])

    idx = argv.index(ARG_BREAK)
    if idx == 1:
        return (argv[0], argv[2:])

    next_idx = idx + 2
    return (argv[idx + 1], (*argv[:idx], *argv[next_idx:]))


def get_pre_commit_args(hook: str) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    _add_color_option(parser)
    _add_config_option(parser)
    _add_run_options(parser)
    return parser.parse_args([hook])


@contextmanager
def hook_context(argv: Argv) -> Iterator[HookContext]:
    hook, extra_args = get_args(argv)

    tmp_path: Optional[Path] = None
    if ARG_STDIN in extra_args:
        tmp_path = redirect_stdin_to_temp_file()
        extra_args = list(extra_args)
        extra_args[extra_args.index(ARG_STDIN)] = str(tmp_path)

    try:
        yield HookContext(hook, extra_args, tmp_path)
    finally:
        if tmp_path:
            tmp_path.unlink()


def main(argv: Argv = None) -> int:
    if argv is None:
        argv = sys.argv[1:]

    if not argv:
        return usage()

    with hook_context(argv) as ctx:
        hook, extra_args, tmp_path = ctx
        if hook.startswith("-"):
            return usage()

        pre_commit_args = get_pre_commit_args(hook)

        with error_handler(), logging_handler(pre_commit_args.color):
            git.check_for_cygwin_mismatch()

            store = Store()
            with store.exclusive_lock():
                store.mark_config_used(pre_commit_args.config)

            original_hook = find_hook(pre_commit_args, store)
            retcode, out = run_hook(
                patch_hook(original_hook, extra_args), pre_commit_args.color
            )

            if tmp_path and hook == HOOK_BLACK and ARG_DIFF not in extra_args:
                sys.stdout.buffer.write(tmp_path.read_bytes())

            sys.stdout.buffer.write(out)
            sys.stdout.buffer.flush()

            return retcode


def main_black(argv: Argv = None) -> int:
    args = [HOOK_BLACK, ARG_BREAK, "--quiet"]

    maybe_pyproject = Path(os.getcwd()) / "pyproject.toml"
    if maybe_pyproject.exists():
        args.extend(["--config", str(maybe_pyproject)])

    args.extend(argv or sys.argv[1:])
    return main(args)


def patch_hook(hook: Hook, extra_args: Argv) -> Hook:
    patched = Hook(*hook)
    patched.args.extend(extra_args)
    return patched


def redirect_stdin_to_temp_file() -> Path:
    tmp_file = tempfile.NamedTemporaryFile(
        prefix="pcrhe", mode="w+", delete=False
    )
    tmp_file.write(sys.stdin.read())
    return Path(tmp_file.name)


def run_hook(hook: Hook, use_color: bool) -> Tuple[int, bytes]:
    language = languages[hook.language]
    return cast(Tuple[int, bytes], language.run_hook(hook, [], use_color))


def usage() -> int:
    print(f"Usage: {__prog__} HOOK ...", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
