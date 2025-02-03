[![pypi](https://img.shields.io/pypi/v/parent-lookup.svg?color=blue)](https://pypi.python.org/pypi/parent-lookup)
[![versions](https://img.shields.io/pypi/pyversions/parent-lookup.svg?color=blue)](https://pypi.python.org/pypi/parent-lookup)
[![license](https://img.shields.io/pypi/l/parent-lookup.svg)](https://github.com/ClaasRostock/parent-lookup/blob/main/LICENSE)
![ci](https://img.shields.io/github/actions/workflow/status/ClaasRostock/parent-lookup/.github%2Fworkflows%2Fnightly_build.yml?label=ci)
[![docs](https://img.shields.io/github/actions/workflow/status/ClaasRostock/parent-lookup/.github%2Fworkflows%2Fpush_to_release.yml?label=docs)][parent_lookup_docs]

# parent-lookup
parent-lookup is a utility Python package enabling a child object to dynamically lookup its parent at runtime. <br>
It comprises of a small set of decorators and methods allowing bidirectional parent-child relationships without hard-coded circular dependencies or circular imports.


## Installation

```sh
pip install parent-lookup
```

## Usage Example

API:

```py
from parent_lookup import TParent, is_child_lookup, lookup_registry

class Child:
    def __init__(self) -> None:
        pass

    @overload
    def find_parent(self, parent_type: type[TParent]) -> TParent | None:
        pass

    @overload
    def find_parent(self, parent_type: TParent) -> TParent | None:
        pass

    def find_parent(self, parent_type: type[TParent] | TParent) -> TParent | None:
        return lookup_registry.lookup_parent(self, parent_type)


class Parent:
    def __init__(self) -> None:
        self._childs: list[Child] = []

    def __new__(
        cls,
    ) -> Parent:
        instance = super().__new__(cls)
        lookup_registry.register_parent(instance)
        return instance

    def add_child(self, child: Child) -> None:
        self._childs.append(child)

    @property
    @is_child_lookup
    def childs(self) -> list[Child]:
        return self._childs

# Create two objects: A parent object and a child object
parent = Parent()
child = Child()
# Add child to parent
parent.add_child(child)
# Lookup parent from child
found_parent = child.find_parent(Parent)
assert found_parent is parent
```

_For more examples and usage, please refer to parent-lookup's [documentation][parent_lookup_docs]._


## Development Setup

### 1. Install uv
This project uses `uv` as package manager.
If you haven't already, install [uv](https://docs.astral.sh/uv), preferably using it's ["Standalone installer"](https://docs.astral.sh/uv/getting-started/installation/#__tabbed_1_2) method: <br>
..on Windows:
```sh
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```
..on MacOS and Linux:
```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
```
(see [docs.astral.sh/uv](https://docs.astral.sh/uv/getting-started/installation/) for all / alternative installation methods.)

Once installed, you can update `uv` to its latest version, anytime, by running:
```sh
uv self update
```

### 2. Install Python
This project requires Python 3.10 or later. <br>
If you don't already have a compatible version installed on your machine, the probably most comfortable way to install Python is through `uv`:
```sh
uv python install
```
This will install the latest stable version of Python into the uv Python directory, i.e. as a uv-managed version of Python.

Alternatively, and if you want a standalone version of Python on your machine, you can install Python either via `winget`:
```sh
winget install --id Python.Python
```
or you can download and install Python from the [python.org](https://www.python.org/downloads/) website.

### 3. Clone the repository
Clone the parent-lookup repository into your local development directory:
```sh
git clone https://github.com/ClaasRostock/parent-lookup path/to/your/dev/parent-lookup
```
Change into the project directory after cloning:
```sh
cd parent-lookup
```

### 4. Install dependencies
Run `uv sync` to create a virtual environment and install all project dependencies into it:
```sh
uv sync
```
> **Note**: Using `--no-dev` will omit installing development dependencies.

> **Note**: `uv` will create a new virtual environment called `.venv` in the project root directory when running
> `uv sync` the first time. Optionally, you can create your own virtual environment using e.g. `uv venv`, before running
> `uv sync`.

### 6. (Optional) Activate the virtual environment
When using `uv`, there is in almost all cases no longer a need to manually activate the virtual environment. <br>
`uv` will find the `.venv` virtual environment in the working directory or any parent directory, and activate it on the fly whenever you run a command via `uv` inside your project folder structure:
```sh
uv run <command>
```

However, you still _can_ manually activate the virtual environment if needed.
When developing in an IDE, for instance, this can in some cases be necessary depending on your IDE settings.
To manually activate the virtual environment, run one of the "known" legacy commands: <br>
..on Windows:
```sh
.venv\Scripts\activate.bat
```
..on Linux:
```sh
source .venv/bin/activate
```

### 7. Install pre-commit hooks
The `.pre-commit-config.yaml` file in the project root directory contains a configuration for pre-commit hooks.
To install the pre-commit hooks defined therein in your local git repository, run:
```sh
uv run pre-commit install
```

All pre-commit hooks configured in `.pre-commit-config.yaml` will now run each time you commit changes.

pre-commit can also manually be invoked, at anytime, using:
```sh
uv run pre-commit run --all-files
```

To skip the pre-commit validation on commits (e.g. when intentionally committing broken code), run:
```sh
uv run git commit -m <MSG> --no-verify
```

To update the hooks configured in `.pre-commit-config.yaml` to their newest versions, run:
```sh
uv run pre-commit autoupdate
```

### 8. Test that the installation works
To test that the installation works, run pytest in the project root folder:
```sh
uv run pytest
```

## Meta

Copyright (c) 2025 [Claas Rostock](https://github.com/ClaasRostock). All rights reserved.

Claas Rostock - [@LinkedIn](https://www.linkedin.com/in/claasrostock/?locale=en_US) - claas.rostock@dnv.com



Distributed under the MIT license. See [LICENSE](LICENSE.md) for more information.

[https://github.com/ClaasRostock/parent-lookup](https://github.com/ClaasRostock/parent-lookup)

## Contributing

1. Fork it (<https://github.com/ClaasRostock/parent-lookup/fork>)
2. Create an issue in your GitHub repo
3. Create your branch based on the issue number and type (`git checkout -b issue-name`)
4. Evaluate and stage the changes you want to commit (`git add -i`)
5. Commit your changes (`git commit -am 'place a descriptive commit message here'`)
6. Push to the branch (`git push origin issue-name`)
7. Create a new Pull Request in GitHub

For your contribution, please make sure you follow the [STYLEGUIDE](STYLEGUIDE.md) before creating the Pull Request.

<!-- Markdown link & img dfn's -->
[parent_lookup_docs]: https://ClaasRostock.github.io/parent-lookup/README.html
