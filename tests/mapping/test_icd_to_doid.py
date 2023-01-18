from unittest import TestCase

import networkx as nx

from ckg_connector.mapping.icd_to_doid import IcdToDoidMapper


class TestIcdToDoidMapper(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.icd_mapper = IcdToDoidMapper("A00")

    def test_get_doid_matches_for_icd_code(self):
        G = nx.Graph()
        G.add_node("DOID:100")
        G.add_node("DOID:200")
        G.add_node("DOID:300")
        xref_values = {
            "DOID:100": ["ICD10CM:A00"],
            "DOID:200": ["ICD10CM:A01", "ICD9CM:A02"],
            "DOID:300": ["ICD10CM:C00.1"],
        }
        nx.set_node_attributes(G, xref_values, "xref")

        real_matches_exact = self.icd_mapper.get_doid_matches_for_icd_code(
            "A00", G
        )
        expected_exact = {
            "exact_match": {"DOID:100": "ICD10CM:A00"},
            "related_matches": {},
        }
        self.assertEquals(real_matches_exact, expected_exact)

        real_matches_releated = self.icd_mapper.get_doid_matches_for_icd_code(
            "C00", G
        )
        expected_related = {
            "exact_match": {},
            "related_matches": {"DOID:300": "ICD10CM:C00.1"},
        }
        self.assertEquals(real_matches_releated, expected_related)

    def test_evaluate_matches(self):
        matches_exact = {
            "exact_match": {"DOID:100": "ICD10CM:A00"},
            "related_matches": {},
        }
        matches_exact_with_related = {
            "exact_match": {"DOID:100": "ICD10CM:A00"},
            "related_matches": {
                "DOID:100": "ICD10CM:A00",
                "DOID:200": "ICD10CM:A00",
            },
        }
        matches_multiple_exact = {
            "exact_match": {
                "DOID:100": "ICD10CM:A00",
                "DOID:200": "ICD10CM:A00",
            },
            "related_matches": {},
        }
        matches_one_related = {
            "exact_match": {},
            "related_matches": {"DOID:300": "ICD10CM:C00.1"},
        }
        matches_multiple_related = {
            "exact_match": {},
            "related_matches": {
                "DOID:300": "ICD10CM:C00.1",
                "DOID:400": "ICD10CM:C00.2",
            },
        }
        no_match = {"exact_match": {}, "related_matches": {}}
        matches = [
            matches_exact,
            matches_exact_with_related,
            matches_multiple_exact,
            matches_one_related,
            matches_multiple_related,
            no_match,
        ]

        expected_matching_status = [
            "Exact",
            "Exact",
            "Multiple exact matches",
            "No exact match: only one related",
            "No exact match: Multiple possibilities",
            "No match",
        ]
        expected_corresponding_doid_codes = [
            "DOID:100",
            "DOID:100",
            "DOID:100|DOID:200",
            "DOID:300",
            "DOID:300|DOID:400",
            "",
        ]

        for i, match in enumerate(matches):
            (
                matching_status,
                corresponding_doid_codes,
            ) = self.icd_mapper.evaluate_matches(match)
            self.assertEquals(matching_status, expected_matching_status[i])
            self.assertEquals(
                corresponding_doid_codes, expected_corresponding_doid_codes[i]
            )
