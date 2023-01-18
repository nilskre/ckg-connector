import argparse
import os

from ckg_connector.dataset.synthetic_dataset import SyntheticDataset
from ckg_connector.mapping.icd_to_doid import IcdToDoidMapper
from ckg_connector.mapping.mapper import create_mappings
from ckg_connector.setup.populate_data_folder import populate_data_folder
from ckg_connector.transform.transformer import convert_dataset_to_ckg_input
from path_helper import get_project_root_dir


def main():
    parser = argparse.ArgumentParser(
        description="Convert datasets to CKG input files."
    )
    parser.add_argument(
        "--datadir",
        type=dir_path,
        default=f"{get_project_root_dir()}/data",
        help="absolute path to data directory (default: ckg-connector/data)",
    )
    args = parser.parse_args()

    data_dir = args.datadir

    run(data_dir)


def run(data_dir):
    print("Start setup")
    populate_data_folder(data_dir)
    print("Finished setup")
    print("Start loading dataset")
    synthetic_dataset = SyntheticDataset(
        f"{data_dir}/input/synthetic_data_Interaction_Project.xlsx"
    )
    number_of_columns = synthetic_dataset.raw_dataset.shape[1]
    print("Finished loading dataset")
    print("Start building mappings")
    icd_column_names_and_codes = (
        synthetic_dataset.get_icd_column_names_and_codes()
    )
    icd_to_doid_mapper = IcdToDoidMapper(
        list(icd_column_names_and_codes.values())
    )
    create_mappings([icd_to_doid_mapper])
    print("Finished building mappings")
    print("Start transforming")
    output_clinical_data, transform_analytics = convert_dataset_to_ckg_input(
        synthetic_dataset
    )
    print("Finished transforming")
    print("Transform stats")
    print(f"- Total number of columns {number_of_columns}")
    print(transform_analytics.T.value_counts(dropna=False))
    print(transform_analytics.T.value_counts(dropna=False, normalize=True))
    print(transform_analytics.T.value_counts()[1])
    output_clinical_data.to_csv(f"{data_dir}/output/clinical_data.csv")
    transform_analytics.to_csv(
        f"{data_dir}/output/statistics/transform_analytics.csv"
    )


def dir_path(path):
    if os.path.isdir(path):
        return path
    else:
        raise argparse.ArgumentTypeError(
            f"readable_dir:{path} is not a valid path"
        )


if __name__ == "__main__":
    main()
