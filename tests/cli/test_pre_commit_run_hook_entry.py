import subprocess

import pytest


@pytest.mark.parametrize(
    "args, base_path, file_name",
    (
        (
            [
                "black",
                "--",
                "--check",
            ],
            "src_path",
            "cli.py",
        ),
        (["flake8", "--"], "src_path", "cli.py"),
        (["mypy", "--"], "src_path", "cli.py"),
        (["check-toml", "--"], "root_path", "pyproject.toml"),
        (["check-yaml", "--"], "root_path", ".pre-commit-config.yaml"),
    ),
)
def test_pre_commit_run_hook_entry(request, args, base_path, file_name):
    assert (
        subprocess.check_call(
            [
                "pre-commit-run-hook-entry",
                *args,
                str(request.getfixturevalue(base_path) / file_name),
            ]
        )
        == 0
    )


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
