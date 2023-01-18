import pandas as pd


def replace_ones_with_col_name(df: pd.DataFrame) -> pd.DataFrame:
    df_filled = df.replace(1, pd.Series(df.columns, df.columns))
    return df_filled
