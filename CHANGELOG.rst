1.0.0 (In Development)
======================

1.0.0rc0 (2024-12-27)
---------------------

**Features:**

- **BREAKING CHANGE:** Only support latest pre-commit 4.0 (#101)

**Other:**

- **BREAKING CHANGE:** Update dev Python version to 3.11.1 (#89)
- Sync common project files (#86)
- Do not install all for tests (#87)
- Update Python dev version to 3.10.8 (#88)
- Monthly maintenance (Jan 2023) (#96)
- Bump dev Python version to 3.11.2 (#99)
- Update CI badge and versions table in README (#103)
- (**deps-dev**) bump pytest-cov from 4.1.0 to 5.0.0 in the dev-dependencies group (#102)
- Setup proper permissions for CI Package reusable workflow call (#106)
- Disable attestations on publishing to PyPI from reusable workflow (#109)

1.0.0b1 (2022-08-09)
--------------------

**Other:**

- Sync common project files (#76)

1.0.0b0 (2022-06-17)
--------------------

**Other:**

- [#27] **BREAKING CHANGE:** Update dev Python version to 3.10.5 (#63)
- Use latest pytest
- (**deps-dev**) bump pytest from 6.0.1 to 6.1.0 (#23)
- (**deps-dev**) bump coverage from 5.2.1 to 5.3 (#24)
- (**deps-dev**) bump pytest from 6.1.0 to 6.1.2 (#25)
- Update default branch name (#64)

1.0.0a3 (2020-08-27)
--------------------

**Features:**

- Support latest pre-commit 2.7.1

**Other:**

- Do not provide language version for pre-commit hooks (`#12 <https://github.com/playpauseandstop/pre-commit-run-hook-entry/issues/12>`_)
- Update github actions versions to use

1.0.0a2 (2020-07-06)
--------------------

**Features:**

- Mark this script dangerous to use cause of `pre-commit/pre-commit#1468
  <https://github.com/pre-commit/pre-commit/issues/1468#issuecomment-640699437>`_
- Implement ``pre-commit-which-hook-entry`` script for finding out full path
  of hook entry script

1.0.0a1 (2020-06-11)
--------------------

**Fixes**

- Ensure sublack integration for all project files

**Other**

- Create GitHub release on pushing git tag
- Cover all functionality with tests

1.0.0a0 (2020-06-08)
--------------------

**Features**

- Initial implementation

**Other**

- Provide more pre-commit hooks
