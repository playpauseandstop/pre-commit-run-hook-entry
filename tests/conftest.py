import os
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

import pytest


ROOT_PATH = Path(__file__).absolute().parent.parent
SRC_PATH = ROOT_PATH / "src" / "pre_commit_run_hook_entry"


@pytest.fixture(scope="function")
def chdir():
    @contextmanager
    def factory(path: Path) -> Iterator[Path]:
        cwd = Path.cwd()
        try:
            yield os.chdir(path)
        finally:
            os.chdir(cwd)

    return factory


@pytest.fixture(scope="function")
def root_path() -> Path:
    return ROOT_PATH


@pytest.fixture(scope="function")
def src_path() -> Path:
    return SRC_PATH
