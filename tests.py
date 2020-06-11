import os
import subprocess
from contextlib import contextmanager
from pathlib import Path
from random import choice
from string import ascii_letters, digits
from typing import Iterator

import pytest

from pre_commit_run_hook_entry import find_file, get_args, get_pre_commit_args


ROOT_PATH = (Path(__file__).parent).absolute()


@contextmanager
def chdir(path: Path) -> Iterator[Path]:
    cwd = Path.cwd()
    try:
        yield os.chdir(path)
    finally:
        os.chdir(cwd)


def test_find_file():
    workflows_path = ROOT_PATH / ".github" / "workflows"
    with chdir(workflows_path):
        assert find_file("ci.yml") == workflows_path / "ci.yml"
        assert find_file("pyproject.toml") == ROOT_PATH / "pyproject.toml"


def test_find_file_does_not_exist():
    prefix = "".join(choice(ascii_letters) for _ in range(16))
    suffix = "".join(choice(digits) for _ in range(8))
    file_name = f"{prefix}_{suffix}"
    assert find_file(file_name) is None


@pytest.mark.parametrize(
    "args, expected",
    (
        (["--help"], ("--help", [])),
        (["black"], ("black", [])),
        (["mypy", "file.py"], ("mypy", ["file.py"])),
        (
            ["black", "--", "--diff", "--quiet", "file.py"],
            ("black", ["--diff", "--quiet", "file.py"]),
        ),
        (
            ["--format", "default", "--", "flake8", "-"],
            ("flake8", ["--format", "default", "-"]),
        ),
    ),
)
def test_get_args(args, expected):
    assert get_args(args) == expected


def test_get_pre_commit_args_default():
    args = get_pre_commit_args("black")
    assert args.hook == "black"
    assert args.config == ".pre-commit-config.yaml"


def test_get_pre_commmit_args_with_config():
    config_yaml = ROOT_PATH / ".pre-commit-config.yaml"
    args = get_pre_commit_args("black", config=config_yaml)
    assert args.config == str(config_yaml)


def test_pre_commit_run_black_entry():
    result = subprocess.run(
        [
            "pre-commit-run-black-entry",
            "--check",
            "pre_commit_run_hook_entry.py",
        ],
        capture_output=True,
    )
    assert result.returncode == 0
    assert result.stdout == b""
    assert result.stderr == b""


def test_pre_commit_run_black_entry_stdin(tmp_path):
    sample = tmp_path / "file.py"
    sample.write_text('print("Hello, world")\n')

    with open(sample, "rb") as handler:
        result = subprocess.run(
            ["pre-commit-run-black-entry", "-"],
            stdin=handler,
            capture_output=True,
        )
        assert result.returncode == 0
        assert result.stdout == b'print("Hello, world")\n'
        assert result.stderr == b""


@pytest.mark.parametrize(
    "args",
    (
        ["black", "--", "--check", "pre_commit_run_hook_entry.py"],
        ["flake8", "--", "pre_commit_run_hook_entry.py"],
        ["mypy", "--", "pre_commit_run_hook_entry.py"],
        ["check-toml", "--", "pyproject.toml"],
        ["check-yaml", "--", ".pre-commit-config.yaml"],
        ["rstcheck", "--", "README.rst"],
    ),
)
def test_pre_commit_run_hook_entry(args):
    assert subprocess.check_call(["pre-commit-run-hook-entry", *args]) == 0


def test_pre_commit_run_hook_entry_error():
    with pytest.raises(subprocess.CalledProcessError):
        subprocess.check_call(
            ["pre-commit-run-hook-entry", "does-not-exist", "--", "README.rst"]
        )


def test_pre_commit_run_hook_entry_stdin(tmp_path):
    sample = tmp_path / "file.py"
    sample.write_text('print("Hello, world!")\n')

    with open(sample, "rb") as handler:
        assert (
            subprocess.check_call(
                [
                    "pre-commit-run-hook-entry",
                    "black",
                    "--",
                    "--check",
                    "--diff",
                    "-",
                ],
                stdin=handler,
            )
            == 0
        )


@pytest.mark.parametrize("args", ([], ["--help"]))
def test_pre_commit_run_hook_entry_usage(args):
    result = subprocess.run(
        ["pre-commit-run-hook-entry", *args], capture_output=True
    )
    assert result.returncode == 1
    assert result.stdout == b""
    assert result.stderr == b"Usage: pre-commit-run-hook-entry HOOK ...\n"
