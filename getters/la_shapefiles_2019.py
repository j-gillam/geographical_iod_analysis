import altair as alt
import geopandas as gpd


def get_english_la_shapefiles_2019() -> alt.Data:
    """Pulling in the English Local Authority (LA) shape files for 2019; with the England regions 
    and LA codes/names. The Deciles are of the Average LSOA Score for each LA.
    Note: You have to use a public url to pull in the shapefiles, it is an issue with altair/streamlit.
    Otherwise it won't plot the map.

    Returns:
        alt.Data: Data for Altair to produce the choropleths in streamlit.
    """
    geojson_la = "https://raw.githubusercontent.com/j-gillam/geographical_iod_analysis/main/shapefiles/la_clean_shapefiles_2019.geojson"
    geodata_la = alt.Data(
        url=geojson_la, format=alt.DataFormat(property="features", type="json")
    )
    return geodata_la

def get_english_la_long_lat_shapefiles_2019() -> alt.Data:
    """Pulling in the English Local Authority (LA) shape files for 2019; with the England regions 
    and LA codes/names. The Deciles are of the Average LSOA Score for each LA.
    Note: You have to use a public url to pull in the shapefiles, it is an issue with altair/streamlit.
    Otherwise it won't plot the map.

    Returns:
        alt.Data: Data for Altair to produce the choropleths in streamlit.
    """
    geojson_la = "https://raw.githubusercontent.com/j-gillam/geographical_iod_analysis/main/shapefiles/la_clean_shapefiles_2019.geojson"
    return gpd.read_file(geojson_la)