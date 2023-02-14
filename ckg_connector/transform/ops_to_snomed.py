import numpy as np
import pandas as pd

from ckg_connector.dataset.dataset import DatasetInterface
from path_helper import get_project_root_dir


def convert_ops_columns(
    ckg_clinical_template: pd.DataFrame,
    dataset: DatasetInterface,
    transform_analytics: pd.DataFrame,
    mapping_ops_snomed: pd.DataFrame,
) -> pd.DataFrame:
    patient_id_and_ops = dataset.get_binary_coded_subpart_codes_per_record(
        "ops"
    )
    mapping_status, ops_codes, map_ops_snomed = lookup_ops_codes_in_mapping(
        mapping_ops_snomed, patient_id_and_ops
    )
    all_mapped_columns = map_dataset(map_ops_snomed, patient_id_and_ops)
    ckg_input = pd.concat([ckg_clinical_template, all_mapped_columns], axis=1)
    generate_summary_statistics(mapping_status, ops_codes, transform_analytics)
    return ckg_input


def lookup_ops_codes_in_mapping(mapping_ops_snomed, patient_id_and_ops):
    ops_codes = []
    snomedct_codes = {}
    mapping_status = []
    for ops_code in patient_id_and_ops.columns:
        ops_codes.append(ops_code)
        one_ops_snomedct_mapping = get_mapping_to_snomedct_for_ops_code(
            ops_code, mapping_ops_snomed
        )

        if one_ops_snomedct_mapping.shape[0] == 0:
            snomedct_codes[ops_code] = "No mapping"
            mapping_status.append("No mapping")
        elif one_ops_snomedct_mapping.shape[0] > 0:
            snomedct_values, mapping_type = get_snomed_values(
                one_ops_snomedct_mapping
            )
            snomedct_codes[ops_code] = snomedct_values
            if one_ops_snomedct_mapping.shape[0] == 1:
                mapping_status.append(f"OPS code exact match; {mapping_type}")
            elif one_ops_snomedct_mapping.shape[0] > 1:
                mapping_status.append(
                    f"OPS code multiple related matches (add all); {mapping_type}"
                )
    return mapping_status, ops_codes, snomedct_codes


def get_mapping_to_snomedct_for_ops_code(ops_value, mapping_ops_snomed):
    one_ops_snomedct_mapping = mapping_ops_snomed[
        mapping_ops_snomed["OPS Code"].str.contains(ops_value)
    ]
    return one_ops_snomedct_mapping


def get_snomed_values(one_ops_snomedct_mapping):
    snomed_ct_code_cols = [
        "SNOMED CT C1",
        "SNOMED CT C2",
        "SNOMED CT C3",
        "SNOMED CT C4",
        "SNOMED CT C5",
        "SNOMED CT substance or device code ",
    ]

    snomedct_values = []

    for row in one_ops_snomedct_mapping[snomed_ct_code_cols].values:
        for snomedct_value in row:
            if snomedct_value != "":
                snomedct_values.append(snomedct_value)

    mapping_type = ""
    if len(snomedct_values) == 1:
        mapping_type = "mapping exact"
    elif len(snomedct_values) > 1:
        mapping_type = "mapping post processed"

    return snomedct_values, mapping_type


def map_dataset(map_ops_snomed, patient_id_and_ops):
    data = {}
    for col_name in patient_id_and_ops.columns:
        mapping = map_ops_snomed[col_name]
        if len(mapping) == 1:
            data[mapping[0]] = patient_id_and_ops[col_name]
        elif len(mapping) > 1:
            for snomedct_code in mapping:
                data[snomedct_code] = patient_id_and_ops[col_name]
    all_mapped_columns = pd.DataFrame(data=data)
    all_mapped_columns = all_mapped_columns.replace(0, "")
    return all_mapped_columns


def generate_summary_statistics(
    mapping_status, ops_codes, transform_analytics
):
    mapping_status = np.array(mapping_status)
    ops_codes = np.array(ops_codes)
    mask_mapped_cols = mapping_status != "No mapping"
    mapped_cols = [
        "OPS_" + ops_code for ops_code in ops_codes[mask_mapped_cols]
    ]
    not_mapped_cols = [
        "OPS_" + ops_code for ops_code in ops_codes[~mask_mapped_cols]
    ]
    transform_analytics.loc[0, mapped_cols] = "Done"
    transform_analytics.loc[1, mapped_cols] = "Automatical OPS mapping"
    transform_analytics.loc[0, not_mapped_cols] = "ToDo"
    transform_analytics.loc[1, not_mapped_cols] = "No mapping found"

    mapping_status = pd.DataFrame(data=mapping_status)
    ax = mapping_status.value_counts().plot(
        kind="bar", title="Mapping statistics: OPS -> Snomed CT"
    )
    ax.figure.savefig(
        f"{get_project_root_dir()}"
        + "/data/mappings/statistics/ops_to_snomedct_mapping_statistics.png",
        bbox_inches="tight",
    )
