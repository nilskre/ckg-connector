from unittest import TestCase

import pandas as pd

from ckg_connector.dataset.synthetic_dataset import SyntheticDataset
from ckg_connector.transform.icd_to_doid import convert_icd_columns
from path_helper import get_project_root_dir


class Test(TestCase):
    def test_convert_icd_columns(self):
        ckg_input = pd.DataFrame(data={"existing_col": [1, 0, 1]})
        dataset = SyntheticDataset(
            f"{get_project_root_dir()}/tests/test_data/test_dataset.xlsx"
        )
        transform_analytics = pd.DataFrame(
            data=None, columns=dataset.raw_dataset.columns
        )
        icd_to_doid_mapping = pd.DataFrame(
            data={
                "icd_code": ["A00", "A42", "C00", "C01"],
                "doid_code": [
                    "DOID:100",
                    "DOID:200",
                    "DOID:300",
                    "DOID:400|DOID:500",
                ],
            }
        )

        real_icd_converted = convert_icd_columns(
            ckg_input, dataset, transform_analytics, icd_to_doid_mapping
        )
        expected = pd.DataFrame(
            data={
                "existing_col": [1, 0, 1],
                "disease": [
                    "DOID:100|DOID:300",
                    "DOID:200",
                    "DOID:100|DOID:200|DOID:300|DOID:400|DOID:500",
                ],
            }
        )
        self.assertTrue(real_icd_converted.equals(expected))
