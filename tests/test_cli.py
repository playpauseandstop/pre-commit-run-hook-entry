from random import choice
from string import ascii_letters, digits

from pre_commit_run_hook_entry.cli import find_file, get_pre_commit_args


def test_find_file(chdir, root_path):
    workflows_path = root_path / ".github" / "workflows"
    with chdir(workflows_path):
        assert find_file("ci.yml") == workflows_path / "ci.yml"
        assert find_file("pyproject.toml") == root_path / "pyproject.toml"


def test_find_file_does_not_exist():
    prefix = "".join(choice(ascii_letters) for _ in range(16))
    suffix = "".join(choice(digits) for _ in range(8))
    file_name = f"{prefix}_{suffix}"
    assert find_file(file_name) is None


def test_get_pre_commit_args_default():
    args = get_pre_commit_args("black")
    assert args.hook == "black"
    assert args.config == ".pre-commit-config.yaml"


def test_get_pre_commmit_args_with_config(root_path):
    config_yaml = root_path / ".pre-commit-config.yaml"
    args = get_pre_commit_args("black", config=config_yaml)
    assert args.config == str(config_yaml)
