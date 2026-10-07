from __future__ import annotations

import sqlite3

import pandas as pd

from .config import DATA_PROCESSED_DIR, DATA_RAW_DIR, DB_PATH, SQL_DIR
from .generator import build_retail_dataset


def create_raw_assets(seed: int = 42) -> None:
    DATA_RAW_DIR.mkdir(parents=True, exist_ok=True)
    dataset = build_retail_dataset(seed=seed)
    dataset.customers.to_csv(DATA_RAW_DIR / "customers.csv", index=False)
    dataset.products.to_csv(DATA_RAW_DIR / "products.csv", index=False)
    dataset.inventory.to_csv(DATA_RAW_DIR / "inventory.csv", index=False)
    dataset.transactions.to_csv(DATA_RAW_DIR / "transactions.csv", index=False)


def transform_raw_assets() -> dict[str, pd.DataFrame]:
    customers = pd.read_csv(DATA_RAW_DIR / "customers.csv", parse_dates=["join_date"])
    products = pd.read_csv(DATA_RAW_DIR / "products.csv")
    inventory = pd.read_csv(DATA_RAW_DIR / "inventory.csv", parse_dates=["snapshot_date"])
    transactions = pd.read_csv(DATA_RAW_DIR / "transactions.csv", parse_dates=["order_date"])

    transactions["month"] = transactions["order_date"].dt.to_period("M").dt.to_timestamp()
    transactions["is_returned"] = transactions["order_status"].eq("Returned").astype(int)
    transactions["is_cancelled"] = transactions["order_status"].eq("Cancelled").astype(int)
    transactions["retained_customer"] = (
        transactions.sort_values("order_date")
        .groupby("customer_id")
        .cumcount()
        .gt(0)
        .astype(int)
    )

    DATA_PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    customers.to_csv(DATA_PROCESSED_DIR / "dim_customers.csv", index=False)
    products.to_csv(DATA_PROCESSED_DIR / "dim_products.csv", index=False)
    inventory.to_csv(DATA_PROCESSED_DIR / "fact_inventory.csv", index=False)
    transactions.to_csv(DATA_PROCESSED_DIR / "fact_sales.csv", index=False)

    return {
        "customers": customers,
        "products": products,
        "inventory": inventory,
        "transactions": transactions,
    }


def build_sqlite_warehouse(dataframes: dict[str, pd.DataFrame]) -> None:
    schema_sql = (SQL_DIR / "schema.sql").read_text()
    with sqlite3.connect(DB_PATH) as connection:
        connection.executescript(schema_sql)
        dataframes["customers"].to_sql("dim_customers", connection, if_exists="replace", index=False)
        dataframes["products"].to_sql("dim_products", connection, if_exists="replace", index=False)
        dataframes["inventory"].to_sql("fact_inventory", connection, if_exists="replace", index=False)
        dataframes["transactions"].to_sql("fact_sales", connection, if_exists="replace", index=False)


def load_warehouse_tables() -> dict[str, pd.DataFrame]:
    with sqlite3.connect(DB_PATH) as connection:
        return {
            "customers": pd.read_sql_query("select * from dim_customers", connection, parse_dates=["join_date"]),
            "products": pd.read_sql_query("select * from dim_products", connection),
            "inventory": pd.read_sql_query("select * from fact_inventory", connection, parse_dates=["snapshot_date"]),
            "transactions": pd.read_sql_query("select * from fact_sales", connection, parse_dates=["order_date", "month"]),
        }
