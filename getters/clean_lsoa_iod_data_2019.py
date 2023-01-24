import pandas as pd



def get_lsoa_iod_2019() -> pd.DataFrame:
    """Pulling in the Lower Super Output Area (LSOA) IoD data for 2019; with the England regions, LA codes/names,
    LSOA codes/names and IoD deciles. The lower the decile, the
    higher the deprivation.

    Returns:
        pd.DataFrame: Pandas dataframe.
    """
    url = "https://raw.githubusercontent.com/j-gillam/geographical_iod_analysis/main/inputs/data/lsoa_clean_iod_2019.csv"
    return pd.read_csv(url)
