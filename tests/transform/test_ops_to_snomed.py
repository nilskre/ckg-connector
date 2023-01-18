from unittest import TestCase

import pandas as pd

from ckg_connector.transform.ops_to_snomed import (
    get_mapping_to_snomedct_for_ops_code,
    get_snomed_values,
)


class Test(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mapping_ops_snomed = pd.DataFrame(
            data={
                "OPS Code": [
                    "1-100",
                    "1-200",
                    "1-200.1",
                    "1-300.0",
                    "1-300.1",
                ],
                "SNOMED CT C1": [
                    "1 |Snomed CT 11 (procedure)|",
                    "2 |Snomed CT 12 (procedure)|",
                    "3 |Snomed CT 13 (procedure)|",
                    "4 |Snomed CT 14 (procedure)|",
                    "5 |Snomed CT 15 (procedure)|",
                ],
                "SNOMED CT C2": [
                    "",
                    "",
                    "",
                    "4 |Snomed CT 24 (procedure)|",
                    "5 |Snomed CT 25 (procedure)|",
                ],
                "SNOMED CT C3": [
                    "",
                    "",
                    "",
                    "4 |Snomed CT 34 (procedure)|",
                    "5 |Snomed CT 35 (procedure)|",
                ],
                "SNOMED CT C4": [
                    "",
                    "",
                    "",
                    "",
                    "5 |Snomed CT 45 (procedure)|",
                ],
                "SNOMED CT C5": [
                    "",
                    "",
                    "",
                    "",
                    "5 |Snomed CT 55 (procedure)|",
                ],
                "SNOMED CT substance or device code ": ["", "", "", "", ""],
            }
        )

    def test_get_snomed_values_exact(self):
        ops_code = "1-100"
        expected_snomed_values = ["1 |Snomed CT 11 (procedure)|"]
        self.helper_get_snomed_values(
            ops_code, expected_snomed_values, "mapping exact"
        )

    def test_get_snomed_values_post_processed(self):
        ops_code = "1-300"
        expected_snomed_values = [
            "4 |Snomed CT 14 (procedure)|",
            "4 |Snomed CT 24 (procedure)|",
            "4 |Snomed CT 34 (procedure)|",
            "5 |Snomed CT 15 (procedure)|",
            "5 |Snomed CT 25 (procedure)|",
            "5 |Snomed CT 35 (procedure)|",
            "5 |Snomed CT 45 (procedure)|",
            "5 |Snomed CT 55 (procedure)|",
        ]
        self.helper_get_snomed_values(
            ops_code, expected_snomed_values, "mapping post processed"
        )

    def helper_get_snomed_values(
        self, ops_code, expected_snomed_values, expected_mapping
    ):
        one_ops_snomedct_mapping = self.mapping_ops_snomed[
            self.mapping_ops_snomed["OPS Code"].str.contains(ops_code)
        ]
        snomed_values, mapping_type = get_snomed_values(
            one_ops_snomedct_mapping
        )
        self.assertEquals(snomed_values, expected_snomed_values)
        self.assertEquals(mapping_type, expected_mapping)

    def test_get_mapping_to_snomedct_for_ops_value_exact_match(self):
        ops_code = "1-100"
        expected_mapping = pd.DataFrame(
            data={
                "OPS Code": ["1-100"],
                "SNOMED CT C1": ["1 |Snomed CT 11 (procedure)|"],
                "SNOMED CT C2": [""],
                "SNOMED CT C3": [""],
                "SNOMED CT C4": [""],
                "SNOMED CT C5": [""],
                "SNOMED CT substance or device code ": [""],
            }
        )
        self.helper_get_mapping_to_snomedct_for_ops_value(
            ops_code, expected_mapping
        )

    def test_get_mapping_to_snomedct_for_ops_value_only_related_matches(self):
        ops_code = "1-300"
        expected_mapping = pd.DataFrame(
            data={
                "OPS Code": ["1-300.0", "1-300.1"],
                "SNOMED CT C1": [
                    "4 |Snomed CT 14 (procedure)|",
                    "5 |Snomed CT 15 (procedure)|",
                ],
                "SNOMED CT C2": [
                    "4 |Snomed CT 24 (procedure)|",
                    "5 |Snomed CT 25 (procedure)|",
                ],
                "SNOMED CT C3": [
                    "4 |Snomed CT 34 (procedure)|",
                    "5 |Snomed CT 35 (procedure)|",
                ],
                "SNOMED CT C4": ["", "5 |Snomed CT 45 (procedure)|"],
                "SNOMED CT C5": ["", "5 |Snomed CT 55 (procedure)|"],
                "SNOMED CT substance or device code ": ["", ""],
            }
        )
        expected_mapping["index"] = [3, 4]
        expected_mapping = expected_mapping.set_index("index")
        self.helper_get_mapping_to_snomedct_for_ops_value(
            ops_code, expected_mapping
        )

    def helper_get_mapping_to_snomedct_for_ops_value(
        self, ops_code, expected_mapping
    ):
        real_mapping = get_mapping_to_snomedct_for_ops_code(
            ops_code, self.mapping_ops_snomed
        )
        self.assertTrue(real_mapping.equals(expected_mapping))
