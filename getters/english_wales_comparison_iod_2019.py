import pandas as pd


def get_english_wales_lsoa_iod_2019() -> pd.DataFrame:
    """Pulling in the English and Welsh IoD data for 2019; with the England regions, LA codes/names
    and IoD deciles. This data has been made for comparability for Income and Employment domains ONLY. 
    The results may slightly differ from the English and Welsh IoD's. The deciles were calculated from the 
    Ranks. The lower the decile, the higher the deprivation.

    Returns:
        pd.DataFrame: Pandas dataframe.
    """
    url = "https://raw.githubusercontent.com/j-gillam/geographical_iod_analysis/main/data/england_wales_decile_comparison.csv"
    return pd.read_csv(url)