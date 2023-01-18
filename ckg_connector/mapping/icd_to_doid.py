import obonet
import pandas as pd

from ckg_connector.mapping.mapper import MapperInterface
from path_helper import get_project_root_dir


class IcdToDoidMapper(MapperInterface):
    def __init__(self, icd_codes_to_map):
        self.icd_codes_to_map = icd_codes_to_map

    def create_mapping(self):
        ontology_file = get_project_root_dir() + "/data/ontologies/DO/doid.obo"
        doid_graph = obonet.read_obo(ontology_file)
        corresponding_doid_codes = []
        matching_status = []

        for icd_code in self.icd_codes_to_map:
            matches = self.get_doid_matches_for_icd_code(icd_code, doid_graph)
            (
                one_icd_code_matching_status,
                one_icd_corresponding_doid,
            ) = self.evaluate_matches(matches)
            matching_status.append(one_icd_code_matching_status)
            corresponding_doid_codes.append(one_icd_corresponding_doid)

        d = {
            "icd_code": self.icd_codes_to_map,
            "doid_code": corresponding_doid_codes,
            "matching_status": matching_status,
        }
        match_icd_doid = pd.DataFrame(data=d)
        match_icd_doid.to_csv(
            f"{get_project_root_dir()}/data/mappings/icd_to_doid.csv"
        )
        ax = (
            match_icd_doid["matching_status"]
            .value_counts()
            .plot(kind="bar", title="Mapping statistics: ICD -> DOID")
        )
        ax.figure.savefig(
            f"{get_project_root_dir()}"
            + "/data/mappings/statistics/icd_to_doid_mapping_statistics.png",
            bbox_inches="tight",
        )

    def get_doid_matches_for_icd_code(self, icd_code, graph):
        candidates = {"exact_match": {}, "related_matches": {}}
        for node_id in graph.nodes:
            node_properties = graph.nodes[node_id]
            try:
                for reference in node_properties["xref"]:
                    if ("ICD" == reference[:3]) & (
                        ":" + icd_code == reference[-4:]
                    ):
                        # Multiple nodes could have an exact match
                        # -> add to list and check after comparison of all nodes
                        candidates["exact_match"][node_id] = reference
                    elif ("ICD" in reference) & (icd_code in reference):
                        candidates["related_matches"][node_id] = reference
            except KeyError:
                pass  # "DOID node has no xref attribute"
        return candidates

    def evaluate_matches(self, matches):
        matching_status = None
        corresponding_doid_codes = None

        if len(matches["exact_match"]) > 0:
            if len(matches["exact_match"]) == 1:
                matching_status = "Exact"
                corresponding_doid_codes = list(matches["exact_match"].keys())[
                    0
                ]
            elif len(matches["exact_match"]) > 1:
                # When there are multiple exact matches -> add all of them
                matching_status = "Multiple exact matches"
                corresponding_doid_codes = "|".join(
                    list(matches["exact_match"].keys())
                )
        elif (len(matches["exact_match"]) == 0) & (
            len(matches["related_matches"]) > 0
        ):
            if len(set(matches["related_matches"].keys())) <= 1:
                # No exact match: but only one node has related matches -> use this node
                matching_status = "No exact match: only one related"
                corresponding_doid_codes = list(
                    matches["related_matches"].keys()
                )[0]
            else:
                # When there are multiple matches -> add all of them
                matching_status = "No exact match: Multiple possibilities"
                corresponding_doid_codes = "|".join(
                    list(matches["related_matches"].keys())
                )
        elif (len(matches["exact_match"]) == 0) & (
            len(matches["related_matches"]) == 0
        ):
            matching_status = "No match"
            corresponding_doid_codes = ""

        return matching_status, corresponding_doid_codes
