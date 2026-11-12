# Namma Metro Ridership Analysis

This project organizes the source data, cleaned data, and analysis work for a Namma Metro ridership study.

## Project folders

- `namma metro/` — source data, cleaned and merged data, and ridership analysis. Its contents are described below.
- `namma metro power bi dashboard/` — Power BI dashboard and star schema files.
- `Star Schema/` — supporting star schema workbook, image, and Power BI file.
- `DAX measures/` — Power BI file and CSV report for DAX measures.









## (1) Namma Metro folder contents

The `namma metro/` folder is organized into three work areas:

### `vimal collected data/` — source workbooks

- `Station-wise Hourly Data - August 2025.xlsx` — August station-level hourly data. The workbook has one sheet with business date, station, and 24 hourly columns.
- `station-hourly.xlsx` — September 2025 station-wise entry and exit data, with separate `Sep-2025 Entry` and `Sep-2025 Exit` sheets. Each sheet contains a date, station, and hourly values.
- `Hourly Station-wise Entry and Exit Data - August 2025.xlsx` — August hourly station-to-station data. Its single sheet has business date, station, and station-code columns.

### `pithambar data cleaning and merging/` — prepared data

- `cleaned_merged_station_ridership.xlsx` — combined and cleaned workbook. It contains:
  - `Combined Hourly` — hourly station records, with source, measure, date, station, and hourly values.
  - `Station Lookup` — station code-to-name mapping.
  - `August OD Matrix` and `August OD Aggregates` — August origin-destination records and aggregated data.
  - `Data Quality` — row counts and cleaning notes for the source datasets.

### `nithin analysing data/` — analysis

- `Member3_Metro_Ridership_Analysis.xlsx` — analysis workbook. Its sheets include `Member 3 Overview`, `Analysis Ready Data`, `Daily Analysis`, `Station Analysis`, `Hourly Analysis`, `Data Quality Checks`, `Station Lookup`, and `Data Quality`. The analysis-ready sheet reshapes hourly columns into hour-and-ridership rows; other sheets summarize ridership by date, station, and hour and report validation checks.
- `1.txt` — a short project reference note with summary figures and a pointer to the analysis workbook. It also mentions `Member3_Analysis_and_Dashboard.md`, which is not currently present in this folder.

## Analysis snapshot

The reference note reports the following figures:

- **Total network ridership:** 55,505,708
- **Unpivoted records:** 152,040
- **Stations:** 84
- **Active dates:** 48, covering August 1 to September 30, 2025

The analysis workbook notes that the source hourly measure is unspecified and that metro line analysis was not included because the combined hourly data has no metro line field. Consult the workbooks for the underlying data and detailed calculations.







## (2) Star Schema

The Star Schema work organizes ridership data into a central fact table and related dimension tables so the data can be analyzed by attributes such as station, date, and hour.

### Team contributions

- **Pithambar — Relationships:** created the relationships between the fact table and dimension tables in the Power BI model.
- **Nithin — Dimension tables:** created the dimension tables used to organize descriptive data. The supporting workbook includes a `Dim_Station` table with station codes and names.
- **Vimal — `Dim_Hour`:** created the hour dimension table using DAX code.

### Files

- `Star Schema/data for star schema.xlsx` — model input workbook with a `Fact_Ridership` table (station code, date, hour, measure, and ridership count) and a `Dim_Station` lookup (station code and station name).
- `Star Schema/star schema image.png` — image illustrating the star schema.
- `Star Schema/star schema.pbix` — Power BI model file for the star schema.

The fact table contains the ridership observations; dimension tables provide descriptive context for filtering and grouping them. The Power BI file is the place to review the model relationships and DAX-created `Dim_Hour` table.







## (3) DAX measures

The `DAX measures/` folder contains two Power BI files, a detailed DAX guide, and a CSV report of the ten measure results:

- `dax implementing.pbix` — Power BI file for the DAX measure work.
- `star schema.pbix` — Power BI file for the star schema.
- `README.md` — team assignments, DAX formulas, explanations, and setup notes for all ten measures.
- `final report of all 10 measures.csv` — a one-row snapshot of the reported results.

The measures are grouped by analysis purpose:

- **Core ridership:** `Total Ridership` sums ridership; `Total Entries` and `Total Exits` filter that sum by the `Measure` category.
- **Average and peak hour:** `Average Ridership` calculates the average per fact-table row; `Peak Hour Ridership` finds the maximum hour total; `Peak Hour Share` compares that peak with total ridership.
- **Day type and month comparison:** `Weekday Ridership` and `Weekend Ridership` compare day types; `Previous Month Ridership` calculates the prior-month total; `MoM % Change` compares current ridership with the previous month.

The DAX guide assigns three measures to Nithin, three to Pithambar, and four to Vimal. It also documents a required `Day Type` calculated column for weekday/weekend analysis. The entry and exit measures depend on `Fact_Ridership[Measure]` containing the exact categories `Entry` and `Exit`. The month-over-month calculation depends on a suitable date table and date relationships. Format `Peak Hour Share` and `MoM % Change` as percentages in Power BI; the formulas return ratios and should not multiply by 100.

### Results snapshot

The CSV report contains these values:

| Measure | Reported value |
|---|---:|
| Total Ridership | 55,505,708 |
| Total Entries | 21,721,271 |
| Total Exits | 21,667,826 |
| Average Ridership | 365.073 |
| Peak Hour Ridership | 5,376,931 |
| Peak Hour Share | 0.0969 (about 9.69%) |
| Weekday Ridership | 42,530,867 |
| Weekend Ridership | 12,974,841 |
| Previous Month Ridership | 12,116,611 |
| MoM % Change | 3.581 (a ratio, about 358.10% when formatted as a percentage) |

These are the values in the saved report, not a guarantee of what every filter context or Power BI refresh will produce. See the DAX guide and Power BI files for formulas and model details.








## (4) Power BI dashboard

The `namma metro power bi dashboard/` folder contains the Power BI dashboard and its supporting star schema file:

- `dashboard.pbix` — the dashboard report, organized into three pages.
- `star schema.pbix` — the Power BI model containing the star schema used to support the report.

### Team contributions

- **Pithambar — Page 1:** created the first dashboard page.
- **Nithin — Page 2:** created the second dashboard page.
- **Vimal — Page 3:** created the third dashboard page.

Open `dashboard.pbix` in Power BI Desktop to explore the report pages and interact with its visuals and filters.