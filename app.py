from __future__ import annotations

from pathlib import Path

import altair as alt
import pandas as pd
import streamlit as st

from src.retail_dashboard.analytics import create_kpi_snapshot, run_named_query
from src.retail_dashboard.config import DB_PATH


st.set_page_config(page_title="Retail Sales Analytics Dashboard", page_icon=":bar_chart:", layout="wide")


@st.cache_data
def load_dashboard_data() -> dict[str, pd.DataFrame]:
    return {
        "kpis": create_kpi_snapshot(),
        "monthly": run_named_query("monthly_revenue"),
        "retention": run_named_query("customer_retention"),
        "regional": run_named_query("regional_sales"),
        "segments": run_named_query("segment_performance"),
        "inventory": run_named_query("inventory_risk"),
        "pricing": run_named_query("pricing_opportunities"),
    }


def currency(value: float) -> str:
    return f"${value:,.0f}"


st.title("Retail Sales Analytics Dashboard")
st.caption("Python + SQL analytics workflow with a Power BI-ready reporting layer.")

if not Path(DB_PATH).exists():
    st.error("Warehouse not found. Run `python3 scripts/run_pipeline.py` first.")
    st.stop()

data = load_dashboard_data()
kpis = data["kpis"]

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Revenue", currency(kpis.loc[kpis["metric"] == "Total Revenue", "value"].iloc[0]))
col2.metric("Average Monthly Revenue", currency(kpis.loc[kpis["metric"] == "Average Monthly Revenue", "value"].iloc[0]))
col3.metric("Retention Rate", f"{kpis.loc[kpis['metric'] == 'Retention Rate', 'value'].iloc[0] * 100:.1f}%")
col4.metric("Products Below Reorder", int(kpis.loc[kpis["metric"] == "Products Below Reorder Point", "value"].iloc[0]))

st.subheader("Revenue Trend")
monthly = data["monthly"].copy()
monthly["month"] = pd.to_datetime(monthly["month"])
st.altair_chart(
    alt.Chart(monthly)
    .mark_line(point=True)
    .encode(
        x=alt.X("month:T", title="Month"),
        y=alt.Y("revenue:Q", title="Revenue"),
        tooltip=["month:T", "revenue:Q", "profit:Q"],
    )
    .properties(height=320),
    use_container_width=True,
)

left, right = st.columns([1.1, 0.9])

with left:
    st.subheader("Regional Sales Performance")
    regional = data["regional"]
    st.altair_chart(
        alt.Chart(regional)
        .mark_bar(cornerRadiusTopLeft=5, cornerRadiusTopRight=5)
        .encode(
            x=alt.X("region:N", sort="-y", title="Region"),
            y=alt.Y("revenue:Q", title="Revenue"),
            color=alt.Color("region:N", legend=None),
            tooltip=["region:N", "revenue:Q", "profit_margin:Q"],
        )
        .properties(height=320),
        use_container_width=True,
    )

with right:
    st.subheader("Customer Segment Mix")
    segments = data["segments"]
    st.altair_chart(
        alt.Chart(segments)
        .mark_arc(innerRadius=60)
        .encode(
            theta=alt.Theta("customers:Q"),
            color=alt.Color("segment:N"),
            tooltip=["segment:N", "customers:Q", "avg_order_value:Q"],
        )
        .properties(height=320),
        use_container_width=True,
    )

left, right = st.columns(2)

with left:
    st.subheader("Customer Retention")
    st.dataframe(data["retention"], use_container_width=True, hide_index=True)

with right:
    st.subheader("Inventory Risk")
    st.dataframe(data["inventory"], use_container_width=True, hide_index=True)

st.subheader("Pricing Optimization Signals")
st.dataframe(data["pricing"], use_container_width=True, hide_index=True)

st.info(
    "Power BI handoff: use the CSV files in `reports/` or connect directly to the SQLite warehouse in "
    "`data/processed/retail_analytics.db`."
)
