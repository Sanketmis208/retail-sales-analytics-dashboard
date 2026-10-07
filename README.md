# Retail Sales Analytics Dashboard

An end-to-end retail analytics project built with Python, SQL, SQLite, Pandas, and Streamlit. It simulates a business-ready reporting workflow covering sales analysis, customer segmentation, retention trends, and inventory monitoring with Power BI-ready outputs.

## Project highlights

- Synthetic retail dataset with customers, products, transactions, and inventory snapshots
- Pandas-based data cleaning and feature engineering
- SQLite warehouse with reusable business SQL queries
- Streamlit dashboard for KPI monitoring and interactive business review
- Automated report exports for monthly revenue, retention, regional sales, and pricing opportunities
- Power BI handoff docs for the same modeled data

## Tech stack

- Python
- Pandas
- SQLite
- SQL
- Streamlit
- Altair
- Power BI compatible CSV and database outputs

## Project structure

```text
.
├── app.py
├── data/
│   ├── raw/
│   └── processed/
├── power_bi/
├── reports/
├── scripts/
├── sql/
├── src/retail_dashboard/
└── tests/
```

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 scripts/run_pipeline.py
streamlit run app.py
```

## Analytics workflow

1. `scripts/run_pipeline.py` generates synthetic retail data.
2. The pipeline cleans and enriches transactions using Pandas.
3. Curated datasets are loaded into `data/processed/retail_analytics.db`.
4. Reusable SQL in `sql/business_queries.sql` powers downstream reporting.
5. CSV outputs are exported into `reports/` for Power BI or scheduled reporting.

## Business questions answered

- How is monthly revenue trending over time?
- Which regions contribute the most revenue and margin?
- What share of orders come from retained customers?
- Which customer segments drive the strongest order value?
- Which categories show pricing pressure from repeated discounting?
- Which products are at reorder risk or overstocked?

## Key outputs

- `reports/monthly_revenue.csv`
- `reports/customer_retention.csv`
- `reports/regional_sales.csv`
- `reports/segment_performance.csv`
- `reports/pricing_opportunities.csv`
- `reports/kpi_snapshot.csv`
- `data/processed/retail_analytics.db`

## Testing

```bash
PYTHONPATH=. python3 -m unittest discover -s tests
```

## Portfolio framing

This project is designed to represent the work implied by the brief:

- end-to-end retail sales dashboarding
- customer segmentation and retention analysis
- inventory trend monitoring
- automated reporting workflows
- scalable reusable SQL reporting assets
