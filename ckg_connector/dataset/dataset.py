import pandas as pd


class DatasetInterface:
    def __init__(self, dataset_file_path: str):
        self.dataset_file_path = dataset_file_path
        self.raw_dataset = self.read_dataset_from_file(dataset_file_path)

    def read_dataset_from_file(self, dataset_file_path: str) -> pd.DataFrame:
        """Read dataset from file to DataFrame."""
        pass

    def get_icd_column_names_and_codes(self) -> dict:
        """Returns a dict with all icd column names (keys) and codes (values)."""
        pass

    def get_ops_column_names_and_codes(self) -> dict:
        """Returns a dict with all ops column names (keys) and codes (values)."""
        pass

    def get_binary_coded_subpart_codes_per_record(
        self, subpart: str
    ) -> pd.DataFrame:
        """Returns a subset of the dataset containing the
        subpart columns (e.g. ICD or OPS)."""
        # returns a dataframe with the following structure:
        # patient_id, icd_x, icd_y, ...
        # binary coding yes 1 no 0
        pass
