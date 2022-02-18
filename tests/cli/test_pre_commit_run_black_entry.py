import subprocess


def test_pre_commit_run_black_entry(src_path):
    result = subprocess.run(
        [
            "pre-commit-run-black-entry",
            "--check",
            str(src_path / "cli.py"),
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
