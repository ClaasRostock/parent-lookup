# Changelog

All notable changes to the [parent-lookup] project will be documented in this file.<br>
The changelog format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

### Dependencies
* Updated to ruff>=0.14.3  (from ruff>=0.9.2)
* Updated to pyright>=1.1.407  (from pyright>=1.1.392)
* Updated to sourcery>=1.40  (from sourcery>=1.31)
* Updated to pytest>=8.4  (from pytest>=8.3)
* Updated to pytest-cov>=7.0  (from pytest-cov>=6.0)
* Updated to Sphinx>=8.2  (from Sphinx>=8.1)
* Updated to sphinx-argparse-cli>=1.20  (from sphinx-argparse-cli>=1.19)
* Updated to sphinx-autodoc-typehints>=3.5  (from sphinx-autodoc-typehints>=3.0)
* Updated to furo>=2025.9  (from furo>=2024.8)
* Updated to pre-commit>=4.3  (from pre-commit>=4.0)
* Updated to mypy>=1.18  (from mypy>=1.14)
* Updated to checkout@v5  (from checkout@v4)
* Updated to setup-python@v6  (from setup-python@v5)
* Updated to setup-uv@v7  (from setup-uv@v5)
* Updated to upload-artifact@v5  (from upload-artifact@v4)
* Updated to download-artifact@v5  (from download-artifact@v4)
* pyproject.toml: added required-environments to uv.tools (windows, linux, macos)
* pyproject.toml: updated required Python version to ">= 3.11, < 3.15"
* pyproject.toml: updated supported Python versions to 3.11, 3.12, 3.13, 3.14
* ruff.toml: updated target Python version to "py311"
* .sourcery.yaml: updated the lowest Python version the project supports to '3.11'
* pyproject.toml: removed deprecated pyright setting 'reportShadowedImports'
* pyproject.toml: removed leading carets and trailing slashes from 'exclude' paths
* pyproject.toml: removed trailing slashes from 'exclude' paths
* GitHub workflow _test.yml: updated Python versions in test matrix to 3.11, 3.12, 3.13, 3.14
* GitHub workflow _test_future.yml: updated Python version in test_future to 3.15.0-alpha - 3.15.0
* GitHub workflow _test_future.yml: updated name of test_future job to 'test315'
* GitHub workflow _test_future.yml: updated Python specifier in comment to 3.15
* GitHub workflow _test_future.yml: updated Python specifier in workflow name to py315
* .pre-commit-config.yaml: updated rev of pre-commit-hooks to v6.0.0
* .pre-commit-config.yaml: updated rev of ruff-pre-commit to v0.14.3
* .pre-commit-config.yaml: updated id of ruff to ruff-check
* Sphinx conf.py: removed ruff rule exception on file level
* VS Code settings: (Recommended extensions) Removed deprecated Intellicode extension and replaced it by Github Copilot Chat as recommended replacement.
* VS Code settings: Updated 'mypy-type-checker.reportingScope' to 'custom'.

### Changed
* Do not run code quality checks in nightly builds
* Included uv.lock file in version control


## [0.2.0] - 2025-02-03

* Initial release


## [0.1.1] - 2025-02-03

* Beta release


## [0.0.1] - 2025-02-03

* Beta release

### Added

* added this

### Changed

* changed that

### Dependencies

* updated to some_package_on_pypi>=0.1.0

### Fixed

* fixed issue #12345

### Deprecated

* following features will soon be removed and have been marked as deprecated:
    * function x in module z

### Removed

* following features have been removed:
    * function y in module z


<!-- Markdown link & img dfn's -->
[unreleased]: https://github.com/ClaasRostock/parent-lookup/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/ClaasRostock/parent-lookup/releases/tag/v0.1.1...v0.2.0
[0.1.1]: https://github.com/ClaasRostock/parent-lookup/releases/tag/v0.0.1...v0.1.1
[0.0.1]: https://github.com/ClaasRostock/parent-lookup/releases/tag/v0.0.1
[parent-lookup]: https://github.com/ClaasRostock/parent-lookup
