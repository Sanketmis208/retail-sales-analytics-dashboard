from src.retail_dashboard.analytics import create_kpi_snapshot, export_analytics_outputs


def main() -> None:
    export_analytics_outputs()
    print(create_kpi_snapshot().to_string(index=False))


if __name__ == "__main__":
    main()
