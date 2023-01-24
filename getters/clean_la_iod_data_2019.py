import pandas as pd


def get_la_iod_2019() -> pd.DataFrame:
    """Pulling in the Local Authority (LA) IoD data for 2019; with the England regions, LA codes/names
    and IoD deciles. The Deciles are of the Average LSOA Score for each LA. The lower the decile, the
    higher the deprivation.

    Returns:
        pd.DataFrame: Pandas dataframe.
    """
    url = "https://raw.githubusercontent.com/j-gillam/geographical_iod_analysis/main/inputs/data/la_clean_iod_2019.csv"
    return pd.read_csv(url)
