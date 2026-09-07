# Python Calculator

A simple calculator application built with Python to practice project structure,
unit testing, virtual environments, code formatting, and linting.

## Features

- Addition
- Subtraction
- Multiplication
- Division
- Division-by-zero validation
- Automated tests with pytest
- Code quality checks with Ruff

## Project Structure

```text
python-calculator/
├── src/
│   └── calculator/
│       ├── __init__.py
│       └── operations.py
├── tests/
│   └── test_operations.py
├── pyproject.toml
├── README.md
└── .gitignore
```

## Requirements

- Python 3.11 or later

## Setup

Clone the repository:

```bash
git clone [https://github.com/YOUR_USERNAME/python-calculator.git](https://github.com/YOUR_USERNAME/python-calculator.git)
cd python-calculator
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Activate it on macOS/Linux:

```bash
source .venv/bin/activate
```

Install the development dependencies:

```bash
python -m pip install pytest ruff
```

## Run Tests

```bash
pytest
```

## Format and Lint the Code

```bash
ruff format .
ruff check .
```

## Learning Objectives

This project was created to practice:

- Python modules and packages
- Functions and exception handling
- Virtual environments
- Unit testing with pytest
- Code formatting and linting
- Git and GitHub workflow

## Future Improvements

- Add a command-line interface
- Add more comprehensive tests
- Add test coverage reporting
- Add GitHub Actions for continuous integration
- Add support for scientific calculator operations

## License

This project is licensed under the MIT License.
