import pandas as pd

from ckg_connector.dataset.dataset import DatasetInterface
from path_helper import get_project_root_dir


def convert_columns_with_manual_mapping(
    ckg_input: pd.DataFrame,
    dataset: DatasetInterface,
    transform_analytics: pd.DataFrame,
    manual_mapping=pd.read_csv(
        get_project_root_dir() + "/data/mappings/manual.csv"
    ),
) -> pd.DataFrame:
    for row in manual_mapping.values.tolist():
        source_column_name = row[0]
        target_column_name = row[1]
        ckg_input[target_column_name] = dataset.raw_dataset[source_column_name]
        transform_analytics.loc[0, source_column_name] = "Done"
        transform_analytics.loc[
            1, source_column_name
        ] = "Manual defined mapping"

    return ckg_input
