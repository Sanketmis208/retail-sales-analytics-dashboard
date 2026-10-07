from __future__ import annotations

import sqlite3

import pandas as pd

from .config import DB_PATH, REPORTS_DIR, SQL_DIR


def load_query(name: str) -> str:
    query_text = (SQL_DIR / "business_queries.sql").read_text()
    sections = {}
    current_name = None
    current_lines = []
    for line in query_text.splitlines():
        if line.startswith("-- name:"):
            if current_name:
                sections[current_name] = "\n".join(current_lines).strip()
            current_name = line.split(":", 1)[1].strip()
            current_lines = []
        elif current_name:
            current_lines.append(line)
    if current_name:
        sections[current_name] = "\n".join(current_lines).strip()
    return sections[name]


def run_named_query(name: str) -> pd.DataFrame:
    with sqlite3.connect(DB_PATH) as connection:
        return pd.read_sql_query(load_query(name), connection)


def create_kpi_snapshot() -> pd.DataFrame:
    monthly = run_named_query("monthly_revenue")
    customer = run_named_query("customer_retention")
    inventory = run_named_query("inventory_risk")
    regional = run_named_query("regional_sales")

    snapshot = pd.DataFrame(
        [
            {
                "metric": "Total Revenue",
                "value": round(monthly["revenue"].sum(), 2),
            },
            {
                "metric": "Average Monthly Revenue",
                "value": round(monthly["revenue"].mean(), 2),
            },
            {
                "metric": "Retention Rate",
                "value": round(customer["retention_rate"].iloc[0], 4),
            },
            {
                "metric": "Products Below Reorder Point",
                "value": int(inventory["products_below_reorder"].iloc[0]),
            },
            {
                "metric": "Top Region",
                "value": regional.sort_values("revenue", ascending=False).iloc[0]["region"],
            },
        ]
    )
    return snapshot


def export_analytics_outputs() -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    outputs = {
        "monthly_revenue.csv": run_named_query("monthly_revenue"),
        "customer_retention.csv": run_named_query("customer_retention"),
        "regional_sales.csv": run_named_query("regional_sales"),
        "segment_performance.csv": run_named_query("segment_performance"),
        "inventory_risk.csv": run_named_query("inventory_risk"),
        "pricing_opportunities.csv": run_named_query("pricing_opportunities"),
        "kpi_snapshot.csv": create_kpi_snapshot(),
    }
    for filename, dataframe in outputs.items():
        dataframe.to_csv(REPORTS_DIR / filename, index=False)
