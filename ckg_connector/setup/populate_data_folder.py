import os

import requests


def populate_data_folder(data_dir: str):
    ops_snomed_mapping_file_path = data_dir + "/mappings/OPS_Snomed_map.csv"
    doid_file_path = data_dir + "/ontologies/DO/doid.obo"

    if not file_exists(ops_snomed_mapping_file_path):
        download_file(
            "https://open.trinetx.com/wp-content/uploads/sites/2/2020/"
            "06/OPS-SNOMED_map_20191217.csv",
            ops_snomed_mapping_file_path,
        )
    if not file_exists(doid_file_path):
        if not file_exists(data_dir + "/ontologies/DO/"):
            os.mkdir(data_dir + "/ontologies/DO/")
        download_file(
            "http://purl.obolibrary.org/obo/doid.obo", doid_file_path
        )


def file_exists(file_path):
    return os.path.exists(file_path)


def download_file(source_file_location, target_file_location):
    request = requests.get(source_file_location, allow_redirects=True)
    open(target_file_location, "wb").write(request.content)
