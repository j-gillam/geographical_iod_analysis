import altair as alt


def get_english_lsoa_shapefiles_2011(region_name: str) -> alt.Data:
    """Pulling in the English Lower Super Output Area (LSOA) shape files for 2011; with the England regions,
    LSOA codes/names and LA codes/names.
    Note: You have to use a public url to pull in the shapefiles, it is an issue with altair/streamlit.
    Otherwise it won't plot the map.
    Args:
        region_name (str): The lower case region name.

    Returns:
        alt.Data: Data for Altair to produce the choropleths in streamlit.
    """
    geojson_lsoa = f"https://raw.githubusercontent.com/j-gillam/geographical_iod_analysis/main/shapefiles/lsoa_clean_shapefiles_2011_{region_name}_reduced.geojson"
    geodata_lsoa = alt.Data(
        url=geojson_lsoa, format=alt.DataFormat(property="features", type="json")
    )
    return geodata_lsoa

def get_welsh_lsoa_shapefiles_2011() -> alt.Data:
    """Pulling in the Welsh Lower Super Output Area (LSOA) shape files for 2011; with the LSOA codes/names. 
    Note: You have to use a public url to pull in the shapefiles, it is an issue with altair/streamlit.
    Otherwise it won't plot the map.
    Args:
        region_name (str): The lower case region name.

    Returns:
        alt.Data: Data for Altair to produce the choropleths in streamlit.
    """
    geojson_lsoa = f"https://raw.githubusercontent.com/j-gillam/geographical_iod_analysis/main/shapefiles/lsoa_clean_shapefiles_2011_wales.geojson"
    geodata_lsoa = alt.Data(
        url=geojson_lsoa, format=alt.DataFormat(property="features", type="json")
    )
    return geodata_lsoa
