from unittest import TestCase

import pandas as pd

from ckg_connector.dataset.synthetic_dataset import SyntheticDataset
from path_helper import get_project_root_dir


class TestSyntheticDataset(TestCase):
    @classmethod
    def setUpClass(cls):
        project_root_dir = get_project_root_dir()
        cls.project_root_dir = project_root_dir
        cls.test_dataset = SyntheticDataset(
            f"{project_root_dir}/tests/test_data/test_dataset.xlsx"
        )

    def test_read_dataset_from_file(self):
        real_dataset: pd.DataFrame = self.test_dataset.read_dataset_from_file(
            f"{self.project_root_dir}/tests/test_data/test_dataset.xlsx"
        )
        expected_dataset = pd.read_excel(
            f"{self.project_root_dir}/tests/test_data/test_dataset.xlsx"
        )
        self.assertTrue(real_dataset.equals(expected_dataset))

    def test_get_icd_column_names_and_codes(self):
        real_icd_codes = self.test_dataset.get_icd_column_names_and_codes()
        expected_icd_codes = {
            "ICD_A00": "A00",
            "ICD_A42": "A42",
            "Cancer_C00": "C00",
            "Cancer_C01": "C01",
        }
        self.assertEquals(real_icd_codes, expected_icd_codes)

    def test_get_ops_column_names_and_codes(self):
        real_ops_codes = self.test_dataset.get_ops_column_names_and_codes()
        expected_ops_codes = {"OPS_1-100": "1-100", "OPS_1-200": "1-200"}
        self.assertEquals(real_ops_codes, expected_ops_codes)

    def test_get_binary_coded_subpart_codes_per_record(self):
        real_icd_binary_coded = (
            self.test_dataset.get_binary_coded_subpart_codes_per_record("icd")
        )
        expected_icd_binary_coded = pd.read_csv(
            f"{self.project_root_dir}/tests/dataset/"
            "expected_binary_coded_icd_codes.csv",
            index_col=0,
        )
        self.assertTrue(
            real_icd_binary_coded.equals(expected_icd_binary_coded)
        )

        real_ops_binary_coded = (
            self.test_dataset.get_binary_coded_subpart_codes_per_record("ops")
        )
        expected_ops_binary_coded = pd.read_csv(
            f"{self.project_root_dir}/tests/dataset/"
            "expected_binary_coded_ops_codes.csv",
            index_col=0,
        )
        self.assertTrue(
            real_ops_binary_coded.equals(expected_ops_binary_coded)
        )
