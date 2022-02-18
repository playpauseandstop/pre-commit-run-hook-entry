import pytest

from pre_commit_run_hook_entry.hooks import get_hook_args


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
def test_get_hook_args(args, expected):
    assert get_hook_args(args) == expected
