from pathlib import Path
import pandas as pd
import os

current_dir = os.getcwd()


def get_la_iod_2019() -> pd.DataFrame:
    """Pulling in the Local Authority (LA) IoD data for 2019; with the England regions, LA codes/names
    and IoD deciles. The Deciles are of the Average LSOA Score for each LA. The lower the decile, the
    higher the deprivation.

    Returns:
        pd.DataFrame: Pandas dataframe.
    """
    return pd.read_csv(f"{current_dir}/inputs/data/la_clean_iod_2019.csv")
