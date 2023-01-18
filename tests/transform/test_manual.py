from unittest import TestCase

import pandas as pd

from ckg_connector.dataset.synthetic_dataset import SyntheticDataset
from ckg_connector.transform.manual import convert_columns_with_manual_mapping
from path_helper import get_project_root_dir


class Test(TestCase):
    def test_convert_columns_with_manual_mapping(self):
        ckg_input = pd.DataFrame(data={"existing_col": [1, 0, 1]})
        dataset = SyntheticDataset(
            f"{get_project_root_dir()}/tests/test_data/test_dataset.xlsx"
        )
        transform_analytics = pd.DataFrame(
            data=None, columns=dataset.raw_dataset.columns
        )
        manual_mapping = pd.DataFrame(
            data={
                "source_column_name": ["Clinical parameter", "Lab value"],
                "target_column_name": [
                    "Clinical parameter (1)",
                    "Lab value (2)",
                ],
            }
        )
        ckg_input_with_manual = convert_columns_with_manual_mapping(
            ckg_input, dataset, transform_analytics, manual_mapping
        )
        expected = pd.DataFrame(
            data={
                "existing_col": [1, 0, 1],
                "Clinical parameter (1)": [120, 140, 160],
                "Lab value (2)": [0.1, 0.2, 0.3],
            }
        )
        self.assertTrue(ckg_input_with_manual.equals(expected))
