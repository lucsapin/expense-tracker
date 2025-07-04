# Expense Tracker

A simple, modular tool for tracking personal and shared expenses, summarizing spending by category, and archiving monthly data.

## Features
- Add new expenses daily
- Monitor and summarize expenses monthly
- Archive and export monthly data
- Separate tracking for Personal and Shared accounts

## Folder Structure
- `add_new_expense.py` — Add a new expense entry
- `mounthly_expenses_monitor.py` — Summarize monthly expenses
- `end_of_mounth_archive.py` — Archive and reset monthly data
- `expenses_working.txt` — Working file for current month's expenses
- `archive/` — Archived monthly expense files
- `summary/` — Monthly summary files
- `export/` — Exported data (optional)

## Setup
1. **Clone the repository**
2. **Create a virtual environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. **Install dependencies:**
   ```bash
   pip install pandas
   ```

## Sample Workflow

### 1. Add Expenses Daily
- Run `add_new_expense.py` to log each new expense.
- Expenses are saved to `expenses_working.txt`.

### 2. Monitor Expenses Monthly
- At the end of the month, run `mounthly_expenses_monitor.py`.
- This script summarizes expenses by category and account, saving results to `summary/`.

### 3. Archive at Month End
- After monitoring, run `end_of_mounth_archive.py`.
- This script archives the month's expenses to `archive/` and resets the working file.

## Example Timeline
| Date         | Action                                 |
|--------------|----------------------------------------|
| Daily        | Run `add_new_expense.py` after spending|
| Last day/mo. | Run `mounthly_expenses_monitor.py`     |
| Last day/mo. | Run `end_of_mounth_archive.py`         |

## Notes
- Make sure to activate your virtual environment before running scripts.
- Adjust file paths in scripts if your data is stored elsewhere.

---
Feel free to customize and extend this project to fit your needs! 