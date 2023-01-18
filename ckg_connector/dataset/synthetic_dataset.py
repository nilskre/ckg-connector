import pandas as pd

from ckg_connector.dataset.dataset import DatasetInterface


class SyntheticDataset(DatasetInterface):
    def __init__(self, dataset_file_path: str):
        super().__init__(dataset_file_path)

    def read_dataset_from_file(self, dataset_file_path: str) -> pd.DataFrame:
        raw_dataset: pd.DataFrame = pd.read_excel(dataset_file_path)
        return raw_dataset

    def get_icd_column_names_and_codes(self) -> dict:
        icd_column_names = [
            col
            for col in self.raw_dataset.columns
            if ("ICD" in col) or ("Cancer_" in col)
        ]
        icd_column_names_and_codes = {}
        for col in icd_column_names:
            icd_column_names_and_codes[col] = col.split("_", 1)[1]
        return icd_column_names_and_codes

    def get_ops_column_names_and_codes(self) -> dict:
        ops_column_names = [
            col for col in self.raw_dataset.columns if "OPS" in col
        ]
        ops_column_names_and_codes = {}
        for col in ops_column_names:
            ops_column_names_and_codes[col] = col.split("_", 1)[1]
        return ops_column_names_and_codes

    def get_binary_coded_subpart_codes_per_record(
        self, subpart: str
    ) -> pd.DataFrame:
        if subpart == "icd":
            column_names = list(self.get_icd_column_names_and_codes().keys())
            column_codes = list(self.get_icd_column_names_and_codes().values())
        elif subpart == "ops":
            column_names = list(self.get_ops_column_names_and_codes().keys())
            column_codes = list(self.get_ops_column_names_and_codes().values())
        subset = column_names.copy()
        subset.insert(0, "Patient ID")
        patient_id_and_icd: pd.DataFrame = self.raw_dataset[subset]
        patient_id_and_icd = patient_id_and_icd.set_index("Patient ID")
        patient_id_and_icd.columns = column_codes
        return patient_id_and_icd
