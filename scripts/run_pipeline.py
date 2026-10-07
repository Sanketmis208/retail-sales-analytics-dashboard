from src.retail_dashboard.analytics import export_analytics_outputs
from src.retail_dashboard.pipeline import build_sqlite_warehouse, create_raw_assets, transform_raw_assets


def main() -> None:
    create_raw_assets()
    frames = transform_raw_assets()
    build_sqlite_warehouse(frames)
    export_analytics_outputs()
    print("Retail analytics pipeline completed.")


if __name__ == "__main__":
    main()
