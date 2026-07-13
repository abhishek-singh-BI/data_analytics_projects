# Bolt Case Study

This project contains Python analyses for a marketplace operations case study. The scripts use demand and supply data from an Excel workbook to identify demand patterns, supply gaps, weekly performance, and short-term forecasts.

## Data source

All scripts expect this workbook to be available locally:

```text
/Users/abhisheksingh/Downloads/Marketplace Ops - Home Task.xlsx
```

The workbook must contain `Demand` and `Supply` sheets.

## Scripts

| Script | Purpose |
| --- | --- |
| `task_1_bolt.py` | Calculates potential orders and returns the five highest-demand time periods for each city. |
| `task_2.py` | Compares average potential demand with average supply by city and hour. |
| `task_2.1.py` | Compares potential demand and supply for each city, date, and hour. |
| `task_3.py` | Finds each city's week with the highest average shrinkage and estimates courier-hours cost and potential additional revenue. |
| `task_3.1.py` | SQL-based version of the weekly shrinkage analysis. |
| `task_4.py` | Builds and evaluates forecasting models for Warsaw's weekly completed orders and online hours. |

## Setup

Install the required packages:

```bash
pip install pandas pandasql openpyxl numpy scikit-learn statsmodels matplotlib
```

## Run an analysis

From the repository root, run a script with Python:

```bash
python bolt_case_study/task_1_bolt.py
```

Most scripts print their results and write an Excel output file to the Downloads folder. `task_4.py` also displays forecast charts.

## Notes

- File paths are currently hard-coded for the local machine. Update `excel_file` and `output_file` in a script if the workbook or desired output location changes.
- The included `bolt_pdf_output.pdf` is a PDF deliverable associated with the case study.
