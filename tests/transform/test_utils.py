from unittest import TestCase

import pandas as pd

from ckg_connector.transform.utils import replace_ones_with_col_name


class Test(TestCase):
    def test_replace_ones_with_col_name(self):
        df = pd.DataFrame(data={"col1": [1, 0], "col2": [1, 1]})
        expected_df = pd.DataFrame(
            data={"col1": ["col1", 0], "col2": ["col2", "col2"]}
        )
        print(df)
        real_df = replace_ones_with_col_name(df)
        print(real_df)
        self.assertTrue(real_df.equals(expected_df))
