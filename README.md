# myuni

A CLI tool for importing student grades from a CSV export into university Excel (XLSX) grade sheets. Built to handle the specific student ID format and Greek-language column headers used in Greek university grade management systems.

## Features

- Parses and validates student grades from CSV files
- Matches students by ID and writes grades into the correct column in an XLSX workbook
- Enforces grade cap of 10 (max passing grade)
- Optional filtering to only apply passing grades (≥5)
- Debug mode to identify unmatched student IDs

## Requirements

- Python ≥ 3.13
- [uv](https://docs.astral.sh/uv/) (recommended) or pip

## Installation

```bash
# Clone the repository
git clone https://github.com/ethan42/myuni.git
cd myuni

# Install dependencies with uv
uv sync
```

## Usage

```bash
uv run main.py <csv_file> <xlsx_file> [--only-passing] [--debug]
```

### Arguments

| Argument | Type | Description |
|---|---|---|
| `csv_file` | positional | Path to the CSV file containing student grades |
| `xlsx_file` | positional | Path to the XLSX workbook where grades will be written |
| `--only-passing` | flag | Only apply grades ≥ 5 (passing threshold) |
| `--debug` | flag | Print a warning for each student ID in the XLSX not found in the CSV |

### Examples

Apply all grades from a CSV to an XLSX:
```bash
uv run main.py grades.csv gradebook.xlsx
```

Apply only passing grades:
```bash
uv run main.py grades.csv gradebook.xlsx --only-passing
```

Debug unmatched students:
```bash
uv run main.py grades.csv gradebook.xlsx --debug
```

## Input Format

### CSV File

Each line must contain exactly one student ID and one integer grade, comma-separated:

```
111520230012,8
111520220047,5
111520240003,9
```

#### Student ID Format

Student IDs follow a fixed 13-digit format:

```
111520 YY 00 NNN
^^^^^^ ^^ ^^ ^^^
|      |  |  └── Student number (3 digits)
|      |  └───── Fixed segment "00"
|      └──────── Matriculation year (2 digits, e.g. 23 for 2023)
└─────────────── Fixed institutional prefix
```

All characters must be numeric. Lines that do not conform to this format will cause the script to exit with a `ValueError`.

### XLSX File

The workbook must have an active sheet with a header row (row 1 is skipped) followed by data rows starting at row 2. The sheet must contain at least two columns with the following Greek headers anywhere in that header row:

| Header | Meaning |
|---|---|
| `Αριθμός Μητρώου` | Student registration number (ID) |
| `Βαθμολογία` | Grade |

Grades are written into the `Βαθμολογία` column for each row whose `Αριθμός Μητρώου` value matches a student ID from the CSV.

> **Note:** Grades exceeding 10 are automatically capped at 10.

## License

MIT © 2026 University of Athens
