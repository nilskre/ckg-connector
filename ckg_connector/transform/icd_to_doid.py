import pandas as pd

from ckg_connector.dataset.dataset import DatasetInterface
from ckg_connector.transform.utils import replace_ones_with_col_name
from path_helper import get_project_root_dir


def convert_icd_columns(
    ckg_input: pd.DataFrame,
    dataset: DatasetInterface,
    transform_analytics: pd.DataFrame,
    mapping_icd_doid=pd.read_csv(
        get_project_root_dir() + "/data/mappings/icd_to_doid.csv",
        keep_default_na=False,
    ),
) -> pd.DataFrame:

    patient_id_and_icd = dataset.get_binary_coded_subpart_codes_per_record(
        "icd"
    )
    patient_id_and_icd_filled = replace_ones_with_col_name(patient_id_and_icd)

    icd_diseases = []
    doid_diseases = []
    for icd_codes_one_patient in patient_id_and_icd_filled.values.tolist():
        icd_diseases_one_patient = []
        doid_diseases_one_patient = []
        for icd_code in icd_codes_one_patient:
            if icd_code != 0:
                icd_diseases_one_patient.append(icd_code)
                one_icd_code_mapping = mapping_icd_doid[
                    mapping_icd_doid["icd_code"] == icd_code
                ]
                doid_code = one_icd_code_mapping["doid_code"].values[0]
                if doid_code != "":
                    doid_diseases_one_patient.append(doid_code)

        icd_diseases.append(icd_diseases_one_patient)
        doid_diseases.append(doid_diseases_one_patient)

    doid_diseases_string = ["|".join(x) for x in doid_diseases]
    ckg_input["disease"] = doid_diseases_string

    icd_columns = dataset.get_icd_column_names_and_codes().keys()
    transform_analytics.loc[0, icd_columns] = "Done"
    transform_analytics.loc[1, icd_columns] = "Automatical ICD mapping"

    return ckg_input
