from typing import Tuple

import pandas as pd

from ckg_connector.dataset.dataset import DatasetInterface
from ckg_connector.transform.icd_to_doid import convert_icd_columns
from ckg_connector.transform.manual import convert_columns_with_manual_mapping
from ckg_connector.transform.ops_to_snomed import convert_ops_columns
from path_helper import get_project_root_dir


def convert_dataset_to_ckg_input(
    dataset: DatasetInterface,
) -> Tuple[pd.DataFrame, pd.DataFrame]:

    ckg_clinical_template: pd.DataFrame = read_ckg_clinical_template()

    transform_analytics = pd.DataFrame(
        data=None, columns=dataset.raw_dataset.columns
    )

    ckg_clinical_with_id = set_patient_id(
        ckg_clinical_template, dataset, transform_analytics
    )
    ckg_clinical_disease = convert_icd_columns(
        ckg_clinical_with_id,
        dataset,
        transform_analytics,
        pd.read_csv(
            get_project_root_dir() + "/data/mappings/icd_to_doid.csv",
            keep_default_na=False,
        ),
    )
    ckg_clinical_manual = convert_columns_with_manual_mapping(
        ckg_clinical_disease, dataset, transform_analytics
    )
    ckg_clinical_ops = convert_ops_columns(
        ckg_clinical_manual,
        dataset,
        transform_analytics,
        pd.read_csv(
            get_project_root_dir() + "/data/mappings/OPS_Snomed_map.csv",
            keep_default_na=False,
        ),
    )

    return ckg_clinical_ops, transform_analytics


def read_ckg_clinical_template():
    ckg_clinical_template: pd.DataFrame = pd.read_excel(
        get_project_root_dir() + "/data/templates/ClinicalData__Pxxxxxxx.xlsx"
    )
    return ckg_clinical_template


def set_patient_id(ckg_clinical_template, dataset, transform_analytics):
    ckg_clinical_template["subject external_id"] = dataset.raw_dataset[
        "Patient ID"
    ]
    transform_analytics.loc[0, "Patient ID"] = "Done"
    transform_analytics.loc[1, "Patient ID"] = "Manual defined mapping"
    return ckg_clinical_template
