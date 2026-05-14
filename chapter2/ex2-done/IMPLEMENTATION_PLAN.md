# NiceGUI Sales Dashboard — Implementation Plan

## 1) Data understanding (done)
- Profile `../sales_data.csv`.
- Save reusable summary in `data_summary.md`.

## 2) Modular structure
- `data_loader.py`: read and validate CSV, parse dates, derive month field.
- `analytics.py`: compute chart/table-ready aggregations.
- `ui_components.py`: render charts, KPI cards, and top-salespeople table.
- `main.py`: app entrypoint and wiring.

## 3) Dashboard scope
- Monthly revenue by category charts:
  - stacked bar chart
  - multi-series line chart
- Top 10 salespeople table by revenue.
- A few headline KPIs (total revenue, records, date range).

## 4) Validation
- Run static error check.
- Ensure app starts from `ex2-good/main.py`.
