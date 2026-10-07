from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

import numpy as np
import pandas as pd


REGIONS = ["North", "South", "East", "West", "Central"]
CITIES = {
    "North": ["Delhi", "Chandigarh", "Jaipur"],
    "South": ["Bengaluru", "Chennai", "Hyderabad"],
    "East": ["Kolkata", "Bhubaneswar", "Guwahati"],
    "West": ["Mumbai", "Pune", "Ahmedabad"],
    "Central": ["Indore", "Bhopal", "Nagpur"],
}
CATEGORIES = {
    "Electronics": ["Laptop", "Headphones", "Smartphone", "Smartwatch"],
    "Fashion": ["Jacket", "Sneakers", "Jeans", "Backpack"],
    "Home": ["Mixer", "Chair", "Lamp", "Storage Box"],
    "Beauty": ["Serum", "Moisturizer", "Perfume", "Sunscreen"],
    "Grocery": ["Coffee", "Cereal", "Pasta", "Snacks"],
}
SEGMENTS = ["High Value", "Loyal", "At Risk", "New"]
CHANNELS = ["Online", "In-Store", "Marketplace"]
PAYMENT_METHODS = ["Card", "UPI", "Wallet", "Net Banking", "Cash"]


@dataclass(frozen=True)
class RetailDataset:
    customers: pd.DataFrame
    products: pd.DataFrame
    inventory: pd.DataFrame
    transactions: pd.DataFrame


def build_retail_dataset(seed: int = 42) -> RetailDataset:
    rng = np.random.default_rng(seed)

    customers = _build_customers(rng)
    products = _build_products(rng)
    transactions = _build_transactions(rng, customers, products)
    inventory = _build_inventory(rng, products, transactions)
    return RetailDataset(
        customers=customers,
        products=products,
        inventory=inventory,
        transactions=transactions,
    )


def _build_customers(rng: np.random.Generator, total_customers: int = 1200) -> pd.DataFrame:
    customer_ids = np.arange(1, total_customers + 1)
    regions = rng.choice(REGIONS, size=total_customers, p=[0.23, 0.22, 0.18, 0.23, 0.14])
    age_group = rng.choice(
        ["18-25", "26-35", "36-45", "46-60", "60+"],
        size=total_customers,
        p=[0.19, 0.32, 0.24, 0.17, 0.08],
    )
    join_dates = pd.to_datetime(
        rng.integers(
            np.datetime64("2022-01-01").astype("datetime64[D]").astype(int),
            np.datetime64("2024-12-31").astype("datetime64[D]").astype(int),
            size=total_customers,
        ),
        unit="D",
    )
    segments = rng.choice(SEGMENTS, size=total_customers, p=[0.18, 0.31, 0.24, 0.27])
    channels = rng.choice(CHANNELS, size=total_customers, p=[0.45, 0.33, 0.22])

    customers = pd.DataFrame(
        {
            "customer_id": customer_ids,
            "customer_name": [f"Customer {i:04d}" for i in customer_ids],
            "region": regions,
            "city": [rng.choice(CITIES[region]) for region in regions],
            "age_group": age_group,
            "join_date": join_dates,
            "segment": segments,
            "preferred_channel": channels,
        }
    )
    return customers


def _build_products(rng: np.random.Generator) -> pd.DataFrame:
    records = []
    product_id = 1
    for category, names in CATEGORIES.items():
        for name in names:
            records.append(
                {
                    "product_id": product_id,
                    "product_name": name,
                    "category": category,
                    "unit_cost": round(rng.uniform(8, 550), 2),
                    "base_price": round(rng.uniform(15, 900), 2),
                    "supplier_lead_days": int(rng.integers(3, 16)),
                }
            )
            product_id += 1
    return pd.DataFrame.from_records(records)


def _build_transactions(
    rng: np.random.Generator,
    customers: pd.DataFrame,
    products: pd.DataFrame,
    total_transactions: int = 14000,
) -> pd.DataFrame:
    customer_choices = customers.sample(total_transactions, replace=True, random_state=11).reset_index(drop=True)
    product_choices = products.sample(total_transactions, replace=True, random_state=21).reset_index(drop=True)
    order_dates = pd.to_datetime(
        rng.integers(
            np.datetime64("2023-01-01").astype("datetime64[D]").astype(int),
            np.datetime64("2025-04-30").astype("datetime64[D]").astype(int),
            size=total_transactions,
        ),
        unit="D",
    )

    quantity = rng.integers(1, 7, size=total_transactions)
    discount = np.round(rng.choice([0, 0.05, 0.1, 0.15, 0.2], size=total_transactions, p=[0.4, 0.23, 0.19, 0.12, 0.06]), 2)
    seasonal_lift = np.where(pd.Series(order_dates).dt.month.isin([10, 11, 12]), 1.12, 1.0)
    base_price = product_choices["base_price"].to_numpy()
    gross_sales = quantity * base_price * seasonal_lift
    net_sales = gross_sales * (1 - discount)
    cogs = quantity * product_choices["unit_cost"].to_numpy()
    profit = net_sales - cogs
    shipment_days = rng.integers(1, 8, size=total_transactions)

    transactions = pd.DataFrame(
        {
            "order_id": np.arange(1, total_transactions + 1),
            "order_date": order_dates,
            "customer_id": customer_choices["customer_id"],
            "product_id": product_choices["product_id"],
            "region": customer_choices["region"],
            "sales_channel": rng.choice(CHANNELS, size=total_transactions, p=[0.49, 0.35, 0.16]),
            "payment_method": rng.choice(PAYMENT_METHODS, size=total_transactions),
            "quantity": quantity,
            "gross_sales": np.round(gross_sales, 2),
            "discount_pct": discount,
            "net_sales": np.round(net_sales, 2),
            "cost_of_goods": np.round(cogs, 2),
            "profit": np.round(profit, 2),
            "shipment_days": shipment_days,
            "order_status": rng.choice(["Delivered", "Delivered", "Delivered", "Returned", "Cancelled"], size=total_transactions),
        }
    )
    return transactions


def _build_inventory(
    rng: np.random.Generator,
    products: pd.DataFrame,
    transactions: pd.DataFrame,
) -> pd.DataFrame:
    product_demand = transactions.groupby("product_id")["quantity"].sum().rename("units_sold")
    inventory = products.merge(product_demand, on="product_id", how="left").fillna({"units_sold": 0})
    inventory["stock_on_hand"] = rng.integers(45, 400, size=len(inventory))
    inventory["reorder_point"] = rng.integers(35, 120, size=len(inventory))
    inventory["days_of_cover"] = np.round(inventory["stock_on_hand"] / (inventory["units_sold"].clip(lower=1) / 120), 1)
    inventory["inventory_status"] = np.where(
        inventory["stock_on_hand"] <= inventory["reorder_point"],
        "Reorder",
        np.where(inventory["days_of_cover"] > 75, "Overstock", "Healthy"),
    )
    inventory["snapshot_date"] = pd.Timestamp(datetime(2025, 5, 1))
    return inventory[
        [
            "product_id",
            "stock_on_hand",
            "reorder_point",
            "days_of_cover",
            "inventory_status",
            "snapshot_date",
        ]
    ]
