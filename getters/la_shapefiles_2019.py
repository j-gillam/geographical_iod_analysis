import altair as alt


def get_la_shapefiles_2019() -> alt.Data:

    geojson_la = "https://raw.githubusercontent.com/j-gillam/geographical_iod_analysis/main/shapefiles/la_clean_shapefiles_2019.geojson"
    geodata_la = alt.Data(
        url=geojson_la, format=alt.DataFormat(property="features", type="json")
    )
    return geodata_la
