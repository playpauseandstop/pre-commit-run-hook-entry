import subprocess


def test_pre_commit_which_hook_entry():
    result = subprocess.run(
        ["pre-commit-which-hook-entry", "black"], capture_output=True
    )
    assert result.returncode == 0
    assert result.stdout.endswith(b"/black\n")
    assert result.stderr == b""


def test_pre_commit_which_hook_entry_does_not_exist():
    result = subprocess.run(
        ["pre-commit-which-hook-entry", "eslint"], capture_output=True
    )
    assert result.returncode == 3
    assert result.stdout.startswith(b"An unexpected error has occurred: ")
    assert result.stderr == b""
