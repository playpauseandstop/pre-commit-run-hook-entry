import argparse
import sys
import tempfile
from contextlib import contextmanager
from pathlib import Path
from typing import cast, Iterator, NamedTuple, Optional, Tuple

from pre_commit.clientlib import load_config
from pre_commit.hook import Hook
from pre_commit.languages.all import languages
from pre_commit.repository import all_hooks, install_hook_envs
from pre_commit.store import Store

from pre_commit_run_hook_entry.annotations import Argv


ARG_BREAK = "--"
ARG_STDIN = "-"


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


def get_hook_args(argv: Argv) -> Tuple[str, Argv]:
    if ARG_BREAK not in argv:
        return (argv[0], argv[1:])

    idx = argv.index(ARG_BREAK)
    if idx == 1:
        return (argv[0], argv[2:])

    next_idx = idx + 2
    return (argv[idx + 1], [*argv[:idx], *argv[next_idx:]])


@contextmanager
def hook_context(argv: Argv) -> Iterator[HookContext]:
    hook, extra_args = get_hook_args(argv)

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


def patch_hook(
    hook: Hook, *, extra_args: Argv = None, entry: str = None
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


def run_hook(hook: Hook, use_color: bool) -> Tuple[int, bytes]:
    language = languages[hook.language]
    return cast(Tuple[int, bytes], language.run_hook(hook, [], use_color))
