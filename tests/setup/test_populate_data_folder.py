import os
import shutil
from unittest import TestCase

from ckg_connector.setup.populate_data_folder import populate_data_folder
from path_helper import get_project_root_dir


class Test(TestCase):
    def test_populate_data_folder(self):
        data_dir = f"{get_project_root_dir()}/data"
        ops_snomed_mapping_file_path = (
            data_dir + "/mappings/OPS_Snomed_map.csv"
        )
        doid_file_path = data_dir + "/ontologies/DO/doid.obo"

        if os.path.exists(ops_snomed_mapping_file_path):
            os.remove(ops_snomed_mapping_file_path)
        if os.path.exists(doid_file_path):
            shutil.rmtree(data_dir + "/ontologies/DO")

        populate_data_folder(data_dir)

        self.assertTrue(os.path.exists(ops_snomed_mapping_file_path))
        self.assertTrue(os.path.exists(doid_file_path))
