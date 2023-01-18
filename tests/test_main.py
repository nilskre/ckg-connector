from unittest import TestCase

import pandas as pd

from ckg_connector.main import run
from path_helper import get_project_root_dir


class Test(TestCase):
    def test_run(self):
        run(f"{get_project_root_dir()}/data")

        real_clinical_data = pd.read_csv(
            f"{get_project_root_dir()}/data/output/clinical_data.csv"
        )
        real_transform_analytics = pd.read_csv(
            f"{get_project_root_dir()}/data/output/statistics/transform_analytics.csv"
        )

        expected_clinical_data = pd.read_csv(
            f"{get_project_root_dir()}/tests/expected_clinical_data.csv"
        )
        expected_transform_analytics = pd.read_csv(
            f"{get_project_root_dir()}/tests/expected_transform_analytics.csv"
        )

        self.assertTrue(real_clinical_data.equals(expected_clinical_data))
        self.assertTrue(
            real_transform_analytics.equals(expected_transform_analytics)
        )
