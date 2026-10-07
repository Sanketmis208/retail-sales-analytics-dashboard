# Power BI Handoff

This repository uses SQLite and CSV outputs so the same curated model can be consumed in Power BI.

## Recommended connection options

1. Import `reports/*.csv` for a quick dashboard prototype.
2. Connect Power BI to `data/processed/retail_analytics.db` through an SQLite connector for a live modeled source.

## Suggested visuals

- KPI cards: total revenue, average monthly revenue, retention rate, products below reorder point
- Line chart: monthly revenue and profit trend
- Clustered bar chart: regional sales and profit margin
- Donut chart: customer segment mix
- Matrix: pricing opportunities by category
- Table: inventory risk summary

## Core measures

- `Total Revenue = SUM(fact_sales[net_sales])`
- `Total Profit = SUM(fact_sales[profit])`
- `Retention Rate = AVERAGE(fact_sales[retained_customer])`
- `Profit Margin % = DIVIDE([Total Profit], [Total Revenue])`

## Refresh workflow

Run `python3 scripts/run_pipeline.py` before refreshing Power BI so the CSV extracts and SQLite warehouse stay current.
