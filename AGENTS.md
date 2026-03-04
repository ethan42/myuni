# AGENTS.md

Guidelines for AI agents (Claude, Codex, Copilot, etc.) working in this repository.

## Project Overview

`myuni` is a small, single-file Python CLI tool (`main.py`). It reads student grades from a CSV file and writes them into the correct cells of a university-issued XLSX gradebook downloaded from myuni. The code is intentionally minimal — keep it that way.

## Repository Structure

```
main.py          # Entire application logic and CLI entry point
pyproject.toml   # Project metadata and dependencies (managed with uv)
uv.lock          # Pinned dependency lockfile — do not edit manually
README.md        # User-facing documentation
AGENTS.md        # This file
LICENSE          # MIT License
```

## Development Environment

- **Python:** 3.13+
- **Package manager:** [uv](https://docs.astral.sh/uv/) — use `uv sync` to install dependencies, `uv run main.py` to execute
- **Single dependency:** `openpyxl` for Excel read/write

## Coding Conventions

- Follow [PEP 8](https://peps.python.org/pep-0008/) style
- All public functions must have docstrings describing parameters, return values, and exceptions raised
- Type hints are required on all function signatures
- Avoid adding new dependencies unless strictly necessary — this tool is intentionally lightweight

## Data Constraints (Do Not Change Without Review)

The following constraints encode real-world requirements of the Greek university system this tool targets. Any changes here must be verified against actual university data formats before merging:

- **Student ID prefix:** `111520` (fixed institutional code)
- **Student ID format:** 13 numeric digits — `111520YY00NNN`
- **Maximum grade:** 10 (hard cap enforced in `apply_grades_to_xlsx`)
- **Passing threshold:** 5 (used by `--only-passing` flag)
- **XLSX column headers:** `Αριθμός Μητρώου` (ID) and `Βαθμολογία` (grade) — these are Greek-language strings from the university's export format and must not be changed
- **XLSX row layout:** Row 1 is a meta/title row (skipped), row 2 is the column header row, data starts at row 3

## What Agents Should and Should Not Do

**Do:**
- Improve docstrings, inline comments, and type annotations
- Add tests (e.g., with `pytest`) for `read_grades_from_csv` and `apply_grades_to_xlsx`
- Improve error messages to be more user-friendly
- Refactor within `main.py` without changing observable behavior
- Update README.md when behavior changes

**Do not:**
- Change the student ID validation rules without explicit instruction
- Change the XLSX column header strings
- Add new CLI arguments without discussing the design first
- Introduce new dependencies without a clear rationale
- Modify `uv.lock` directly — run `uv add` or `uv sync` instead
- Rewrite the tool in a different language or framework

## Testing

There is currently no test suite. When adding tests:

- Use `pytest`
- Add `pytest` as a dev dependency: `uv add --dev pytest`
- Place tests in a `tests/` directory
- Use small fixture CSV and XLSX files (do not include real student data)

## Making Changes

1. Work on a feature branch off `main`
2. Keep commits focused and atomic
3. Update `README.md` if any user-visible behavior changes
4. Run `uv run main.py --help` to verify the CLI still works before opening a PR
