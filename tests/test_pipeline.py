from pathlib import Path
import unittest

import pandas as pd

from src.retail_dashboard.analytics import create_kpi_snapshot, run_named_query
from src.retail_dashboard.config import DB_PATH
from src.retail_dashboard.pipeline import build_sqlite_warehouse, create_raw_assets, transform_raw_assets


class PipelineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        create_raw_assets(seed=123)
        frames = transform_raw_assets()
        build_sqlite_warehouse(frames)

    def test_pipeline_outputs_exist(self) -> None:
        self.assertTrue(Path(DB_PATH).exists())
        monthly = run_named_query("monthly_revenue")
        self.assertFalse(monthly.empty)
        self.assertTrue({"month", "revenue", "profit"}.issubset(monthly.columns))

    def test_kpi_snapshot_shape(self) -> None:
        snapshot = create_kpi_snapshot()
        self.assertIsInstance(snapshot, pd.DataFrame)
        self.assertEqual(set(snapshot.columns), {"metric", "value"})
        self.assertEqual(len(snapshot), 5)


if __name__ == "__main__":
    unittest.main()
