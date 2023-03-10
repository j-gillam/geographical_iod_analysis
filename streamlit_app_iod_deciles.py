import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import altair as alt
from utils.utils_fonts_colours import *
from utils.utils_iod_values import *
from PIL import Image
from getters.english_la_iod_data_2019 import get_english_la_iod_2019
from getters.english_lsoa_iod_data_2019 import get_english_lsoa_iod_2019
from getters.la_shapefiles_2019 import get_english_la_shapefiles_2019
from getters.english_wales_comparison_iod_2019 import get_english_wales_lsoa_iod_2019
from getters.lsoa_shapefiles_2011 import (
    get_english_lsoa_shapefiles_2011, get_welsh_lsoa_shapefiles_2011
)
from getters.welsh_lsoa_iod_data_2019 import get_welsh_lsoa_iod_2019
from utils.utils_preprocessing import preprocess_strings
import os


@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode("utf-8")


current_dir = os.getcwd()

# Creating the font/colours we use for the figures:
alt.themes.register("nestafont", nestafont)
alt.themes.enable("nestafont")

colours = NESTA_COLOURS
# Load the favicon and set the page config (so what appears in the tab on your web browser)
im = Image.open(f"{current_dir}/images/favicon.ico")
st.set_page_config(page_title="IoD Deciles across England", layout="wide", page_icon=im)

# Creates the Navigation bar on the side:
with st.sidebar:
    choose = option_menu(
        "IoD Geographical Analysis",
        ["About", "English LA Breakdown", 
        "English LA Comparison", "English LSOA Breakdown", 
        "Welsh LSOA Breakdown",
        "Comparing Welsh and English IoD"
        ],
        icons=["house", "geo-alt", 
        "kanban", "geo-alt",
        "geo-alt", "kanban"
        ],
        default_index=0,
        orientation="vertical",
        styles={
            "container": {
                "padding": "5!important",
                "background-color": NESTA_COLOURS[12],
            },
            "icon": {"color": NESTA_COLOURS[10], "font-size": "25px"},
            "nav-link": {
                "font-size": "16px",
                "text-align": "left",
                "margin": "0px",
                "--hover-color": "#eee",
            },
            "nav-link-selected": {"background-color": NESTA_COLOURS[0]},
        },
    )


# For the About page (which we have not password protected):
if choose == "About":

    # Creates a separate container for us to put the header in
    header = st.container()

    with header:

        # How to add images:
        nesta_logo = Image.open(f"{current_dir}/images/nesta_logo.png")
        st.image(nesta_logo, width=250)

        # How to create a title for the page:
        st.title("Geographical Analysis of the IoD Deciles Across England and Wales")

        st.markdown(
            "  **website:** https://www.nesta.org/ **| email:** jess.gillam@nesta.org.uk"
        )

    # You can use st.markdown to add text to the app:
    st.markdown(
        """
            This app shows how open source data can be mapped geographically to identify deprivation and need across England and Wales.
            We use the English indices of deprivation (IoD) published in 2019. The IoD are statistics on the relative
            deprivation in small areas in England. Data is available at Local Authority (LA) and Lower Super Output Area (LSOA) level.

            The IoD dataset provides 10 indices, with the Index of Multiple Deprivation (IMD) being a combination of the indices shown in the graphic below.
            """
    )
    iod_graphic = Image.open(f"{current_dir}/images/iod_graphic.png")
    st.image(iod_graphic)

    # How to add url hyperlinks:
    text_iod = "https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/833959/IoD2019_Infographic.pdf"
    st.markdown(
        f"<div style='text-align: center;'>Taken from the ONS infographic <a href={text_iod}> here</a>. </div>",
        unsafe_allow_html=True,
    )
    # This uses html syntax within the markdown.
    st.markdown(
        """
            For the geographic boundaries, we use the the corresponding LA (2019) and LSOA (2011) boundaries used for the creation of the IoD dataset.

            """
    )
    text_open_data = (
        "https://opendatacommunities.org/data/societal-wellbeing/imd2019/indices"
    )
    text_geography = "https://geoportal.statistics.gov.uk/search?collection=Dataset"
    github_repo = "https://raw.githubusercontent.com/j-gillam/geographical_iod_analysis"  ###### CHANGE
    st.markdown(
        f"<div> These open datasets can be found on the <a href= {text_open_data}> Open Data Community </a> and from <a href= {text_geography}> Open Geography Portal </a> . See <a href= {github_repo}> here </a> for the github repository with the linked datasets and streamlit code for this app.</div>",
        unsafe_allow_html=True,
    )
    st.markdown("""
    The Welsh Indices of Deprivation consider slightly different categories and look at LSOA level only. 
    The rank is reported with a rank of 1 for the most deprived area. We have converted these ranks to deciles.
    """)
    wales_iod_graphic = Image.open(f"{current_dir}/images/wales_iod_graphic.png")
    text_wales_iod = "https://www.gov.wales/sites/default/files/statistics-and-research/2019-11/welsh-index-multiple-deprivation-2019-results-infographic-207.pdf"
    st.image(wales_iod_graphic)
    st.markdown(
        f"<div style='text-align: center;'>Taken from the Welsh GOV infographic <a href={text_wales_iod}> here</a>. </div>",
        unsafe_allow_html=True,
    )
    text_combined_data = "https://www.gov.uk/government/statistics/indices-of-deprivation-2019-income-and-employment-domains-combined-for-england-and-wales"
    st.markdown(
        f"<div> Due to the differences in considerations for the Indices, the Welsh IoD's are not directly comparable. However, a different dataset has been published <a href= {text_combined_data}> here </a> which reports on the Income, Employment, IDACI and IDAOPI indices for both Wales and England combined. </div>",
        unsafe_allow_html=True)


# In order to password protect the rest of the app, put the rest of the code insidea a function. 
def streamlit_iod():
    # Sets a spinner so we know that the report is updating as we change the user selections.
    with st.spinner("Updating Report..."):

        # Possible regions in England.
        # Using session_state allows sharing of variables between reruns (so the app doesn't forget previous selections!)
        if "region_filter" not in st.session_state:
            st.session_state.region_filter = [
                "North East",
                "North West",
                "Yorkshire and The Humber",
                "East Midlands",
                "West Midlands",
                "South West",
                "East",
                "South East",
                "London",
            ]

        # Possible IoD domains you want to look at.
        if "iod_filter" not in st.session_state:
            st.session_state.iod_filter = iod_names
        # Loading in the IoD data at LA and LSOA level (query to insure we are only looking at the English Regions).
        data = get_english_la_iod_2019().query("region_name in @st.session_state.region_filter")
        lsoa_data = get_english_lsoa_iod_2019().query(
            "region_name in @st.session_state.region_filter"
        )
        data_wales = get_welsh_lsoa_iod_2019()
        data_welsh_english = get_english_wales_lsoa_iod_2019()

        la_melt = (
            pd.melt(
                data,
                id_vars=["lad19cd", "lad19nm", "region_name"],
                value_vars=iod_indices,
            )
            .rename(columns={"variable": "iod", "value": "decile"})
            .assign(iod_name=lambda df: df.iod.replace(iod_dict_inv))
        )

        geodata_la = get_english_la_shapefiles_2019()
        geodata_lsoa_wales = get_welsh_lsoa_shapefiles_2011()

        # For the LA Breakdown page:
        if choose == "English LA Breakdown":

            # Altair selections (allows you to select a local authority):
            la_select = alt.selection_single(fields=["lad19nm"])
            la_select_all = alt.selection_single(fields=["lad19nm"], empty="none")
            st.title("Local Authorities in England, broken down by IoD Decile")
            st.markdown(
                """
            The first map shows the overall Index of Multiple deprivation for England. The second map shows a region of England where you can select
            which IoD you wish to look at. Attached to the second map is a bar chart that shows the IoD deciles for the Local Authority (LA)
            selected on the map.

            You can click on each LA to highlight it, double-click to remove the selection and hover over the map to see the deciles.
            """
            )
            # Choose the colour palette:
            colour_choice = st.selectbox(
                "Choose a colour palette for the maps:",
                options=list(colour_palettes.keys()),
            )
            color_ = alt.condition(
                la_select,
                alt.Color(
                    f'{iod_dict["Index of Multiple Deprivation (IMD)"]}:O',
                    scale=colour_palettes[colour_choice],
                    title="Index of Multiple Deprivation (IMD)",
                    legend=alt.Legend(orient="top"),
                ),
                alt.value("lightgray"),
            )
            choro_all = (
                alt.Chart(geodata_la)
                .mark_geoshape(
                    stroke="black",
                )
                .transform_lookup(
                    lookup="properties.lad19nm",
                    from_=alt.LookupData(
                        data,
                        "lad19nm",
                        ["lad19cd", "lad19nm", "region_name"] + iod_indices,
                    ),
                )
                .transform_filter(
                    alt.FieldOneOfPredicate(
                        field="properties.lad19nm", oneOf=data.lad19nm.unique()
                    )
                )
                .encode(
                    color=color_,
                    tooltip=[alt.Tooltip("lad19nm:N", title="Local Authority")]
                    + [
                        alt.Tooltip(
                            f"{ind}:O", title=name, format="1.2f"
                        )
                        for ind, name in zip(iod_indices, iod_tooltip)
                    ],
                )
                .add_selection(la_select)
                .properties(width=500, height=500)
            )
            st.altair_chart(
                choro_all.configure_legend(
                    labelLimit=0,
                    titleLimit=0,
                    titleFontSize=13,
                    labelFontSize=13,
                    symbolStrokeWidth=1.5,
                    symbolSize=150,
                )
                .configure_view(strokeWidth=0)
                .configure_axis(
                    labelLimit=0,
                    titleLimit=0,
                ),
                use_container_width=True,
            )

            # Select box to pick the region you wish to look at.
            region_selection = st.selectbox(
                "To look in closer detail, choose a region of England:",
                options=sorted(st.session_state.region_filter),
            )
            # Select box to pick the IoD you wish to look at.
            iod_selection = st.selectbox(
                "Choose a IoD Decile to view on the map:",
                options=st.session_state.iod_filter,
            )

            st.markdown(
                "Click on one of the LAs to bring up the deciles in a graph below."
            )

            las_to_plot = list(data[data["region_name"] == region_selection].lad19nm)
            color_las = alt.condition(
                la_select,
                alt.Color(
                    f"{iod_dict[iod_selection]}:O",
                    scale=colour_palettes[colour_choice],
                    title=iod_selection,
                    legend=alt.Legend(orient="top"),
                ),
                alt.value("lightgray"),
            )

            choro_legend = (
                alt.Chart(geodata_la)
                .mark_geoshape(
                    stroke="black",
                )
                .transform_lookup(
                    lookup="properties.lad19nm",
                    from_=alt.LookupData(
                        data,
                        "lad19nm",
                        ["lad19cd", "lad19nm", "region_name"] + iod_indices,
                    ),
                )
                .transform_filter(
                    alt.FieldOneOfPredicate(
                        field="properties.lad19nm", oneOf=las_to_plot
                    )
                )
                .encode(
                    color=color_las,
                    tooltip=[alt.Tooltip("lad19nm:N", title="Local Authority")]
                    + [
                        alt.Tooltip(
                            f"{ind}:O", title=name, format="1.2f"
                        )
                        for ind, name in zip(iod_indices, iod_tooltip)
                    ],
                )
                .add_selection(la_select, la_select_all)
                .properties(width=500, height=500)
            )
            choro_bar = (
                alt.Chart(la_melt)
                .mark_bar(color=NESTA_COLOURS[1])
                .encode(
                    x=alt.X(
                        "decile:Q",
                        title="Decile",
                        scale=alt.Scale(domain=[0, 10]),
                        axis=alt.Axis(tickMinStep=1),
                    ),
                    y=alt.Y(
                        "iod_name:N",
                        title="Indices of Deprivation",
                        sort=iod_names,
                        axis=alt.Axis(titlePadding=330),
                    ),
                    # If you wanted to add a color scheme to the bars:
                    # color = alt.Color(
                    #         'decile:Q',
                    #         scale=alt.Scale(domain=domain, range=range_),
                    #         legend=None)
                )
                .transform_filter(la_select_all)
                .properties(width=400, height=400)
            )
            la_text = (
                alt.Chart(la_melt)
                .mark_text(dy=-210, size=20, color="darkgray")
                .encode(text="lad19nm:N")
                .transform_filter(la_select_all)
            )
            bar_chart = alt.layer(choro_bar, la_text)
            st.altair_chart(
                (
                    alt.vconcat(choro_legend, bar_chart, center=True)
                    .configure_legend(
                        labelLimit=0,
                        titleLimit=0,
                        titleFontSize=13,
                        labelFontSize=13,
                        symbolStrokeWidth=1.5,
                        symbolSize=150,
                    )
                    .configure_view(strokeWidth=0)
                    .configure_axis(
                        labelLimit=0,
                        titleLimit=0,
                    )
                ),
                use_container_width=True,
            )
        # Comparing different Local Authorities
        elif choose == "English LA Comparison":
            st.title("Comparing the IoD for Local Authorities in England")
            st.markdown(
                """
            This bar chart allows you to select up to five Local Authorities (LAs) across England to compare the different IoDs.
            """
            )
            if "all_las" not in st.session_state:
                st.session_state.all_las = data.lad19nm.unique()
            la_compare_select = st.multiselect(
                "Choose up to five LAs:",
                options=sorted(st.session_state.all_las),
                default=None,
                max_selections=5,
            )
            la_iod_select = st.selectbox(
                "Choose IoD Decile to view on the map:",
                options=st.session_state.iod_filter,
                key="iod_compare",
            )
            la_compare = la_melt[
                (la_melt.lad19nm.isin(la_compare_select))
                & (la_melt.iod_name == la_iod_select)
            ]

            compare_las = (
                alt.Chart(la_compare)
                .mark_bar(size=50, color=NESTA_COLOURS[1])
                .encode(
                    x=alt.X(
                        "decile:Q",
                        title="Decile",
                        scale=alt.Scale(domain=[0, 10]),
                        axis=alt.Axis(tickMinStep=1),
                    ),
                    y=alt.Y("lad19nm:N", title=None),
                    # color = alt.Color(
                    #     'lad19nm:N',
                    #     legend=None),
                )
                .properties(width=600, height=400)
            )
            st.altair_chart(
                compare_las.configure_view(strokeWidth=0).configure_axis(
                    labelLimit=0, titleLimit=0, labelFontSize=18
                ),
                use_container_width=True,
            )

        elif choose == "English LSOA Breakdown":
            st.title("Lower Super Output Areas in England, broken down by IoD Decile")
            st.markdown(
                """
            By selecting a region of England, an IoD and a Local Authority (LA), this map shows the breakdown at Lower Super Output Area (LSOA).

            You can click on each LSOA to highlight it, double-click to remove the selection and hover over the map to see the deciles.
            """
            )
            # Choose the colour palette:
            colour_choice = st.selectbox(
                "Choose a colour palette for the maps:",
                options=list(colour_palettes.keys()),
            )
            # Select box to pick the region you wish to look at.
            region_selection = st.selectbox(
                "Choose a region of England:",
                options=sorted(st.session_state.region_filter),
                key="region_lsoas",
            )
            las_to_plot = list(data[data["region_name"] == region_selection].lad19nm)
            data_lsoa = lsoa_data[lsoa_data.region_name == region_selection]
            iod_selection = st.selectbox(
                "Choose IoD Decile to view on the map:",
                options=st.session_state.iod_filter,
                key="iod",
            )
            la_selection = st.selectbox(
                "Choose a local authority from the region chosen above to see the LSOA breakdown:",
                sorted(las_to_plot),
            )
            # Dataset is larger than 5000, so we partition it into two smaller datasets.
            las_to_split = [
                "Brighton and Hove",
                "Medway",
                "Milton Keynes",
                "Southampton",
                "Portsmouth",
            ]
            if la_selection in las_to_split:
                filter_data_lsoa = data_lsoa[data_lsoa.lad19nm.isin(las_to_split)]
            else:
                filter_data_lsoa = data_lsoa[~data_lsoa.lad19nm.isin(las_to_split)]

            lsoas_to_plot = list(lsoa_data[lsoa_data.lad19nm == la_selection].lsoa11nm)
            region_dict = dict(
                zip(
                    st.session_state.region_filter,
                    preprocess_strings(pd.Series(st.session_state.region_filter)),
                )
            )
            geodata_lsoa = get_english_lsoa_shapefiles_2011(region_dict[region_selection])
            lsoa_select = alt.selection_single(fields=["lsoa11nm"])
            color_lsoa = alt.condition(
                lsoa_select,
                alt.Color(
                    f"{iod_dict[iod_selection]}:O",
                    scale=colour_palettes[colour_choice],
                    title=f"{iod_selection}",
                    legend=alt.Legend(orient="top"),
                ),
                alt.value("lightgray"),
            )
            choro_lsoa = (
                alt.Chart(geodata_lsoa)
                .mark_geoshape(
                    stroke="black",
                )
                .transform_lookup(
                    lookup="properties.lsoa11nm",
                    from_=alt.LookupData(
                        filter_data_lsoa,
                        "lsoa11nm",
                        ["lsoa11cd", "lsoa11nm", "lad19cd", "lad19nm"] + iod_indices,
                    ),
                )
                .transform_filter(
                    alt.FieldOneOfPredicate(
                        field="properties.lsoa11nm", oneOf=lsoas_to_plot
                    )
                )
                .encode(
                    color=color_lsoa,
                    tooltip=[alt.Tooltip("lsoa11nm:N", title="LSOA")]
                    + [
                        alt.Tooltip(
                            f"{ind}:O", title=name, format="1.2f"
                        )
                        for ind, name in zip(iod_indices, iod_tooltip)
                    ],
                    opacity=alt.condition(lsoa_select, alt.value(1), alt.value(0.2)),
                )
                .add_selection(lsoa_select)
                .project(type="identity", reflectY=True)
                .properties(width=500,height=500)
            )
            st.altair_chart(
                choro_lsoa.configure_legend(
                    labelLimit=0,
                    titleLimit=0,
                    titleFontSize=13,
                    labelFontSize=13,
                    symbolStrokeWidth=1.5,
                    symbolSize=150,
                )
                .configure_view(strokeWidth=0)
                .configure_axis(
                    labelLimit=0,
                    titleLimit=0,
                ),
                use_container_width=True,
            )
        elif choose == "Welsh LSOA Breakdown":
        
            st.title("Lower Super Output Areas in Wales, broken down by IoD Decile")
            st.markdown(
                """
            By selecting a region of Wales, an IoD and a Local Authority (LA), this map shows the breakdown at Lower Super Output Area (LSOA).

            You can click on each LSOA to highlight it, double-click to remove the selection and hover over the map to see the deciles.
            """
            )
            # Choose the colour palette:
            colour_choice = st.selectbox(
                "Choose a colour palette for the maps:",
                options=list(colour_palettes.keys()),
            )
            # Select box to pick the region you wish to look at.
            region_selection = st.selectbox(
                "Choose a region of Wales:",
                options=sorted(data_wales.region_name.unique()),
                key="region_lsoas_wales",
            )
            welsh_las_to_plot = list(data_wales[data_wales["region_name"] == region_selection].lad19nm.unique())
            wiod_selection = st.selectbox(
                "Choose IoD Decile to view on the map:",
                options=wiod_names,
                key="iod",
            )
            welsh_la_selection = st.selectbox(
                "Choose a local authority from the region chosen above to see the LSOA breakdown:",
                sorted(welsh_las_to_plot),
            )

            welsh_lsoas_to_plot = list(data_wales[data_wales.lad19nm == welsh_la_selection].lsoa11nm)
            lsoa_select_wales = alt.selection_single(fields=["lsoa11nm"])
            color_lsoa_wales = alt.condition(
                lsoa_select_wales,
                alt.Color(
                    f"{wiod_dict[wiod_selection]}:O",
                    scale=colour_palettes[colour_choice],
                    title=f"{wiod_selection}",
                    legend=alt.Legend(orient="top"),
                ),
                alt.value("lightgray"),
            )
            choro_lsoa = (
                alt.Chart(geodata_lsoa_wales)
                .mark_geoshape(
                    stroke="black",
                )
                .transform_lookup(
                    lookup="properties.lsoa11nm",
                    from_=alt.LookupData(
                        data_wales,
                        "lsoa11nm",
                        ["lsoa11cd", "lsoa11nm", "lad19cd", "lad19nm"] + wiod_indices,
                    ),
                )
                .transform_filter(
                    alt.FieldOneOfPredicate(
                        field="properties.lsoa11nm", oneOf=welsh_lsoas_to_plot
                    )
                )
                .encode(
                    color=color_lsoa_wales,
                    tooltip=[alt.Tooltip("lsoa11nm:N", title="LSOA")]
                    + [
                        alt.Tooltip(
                            f"{ind}:O", title=name, format="1.2f"
                        )
                        for ind, name in zip(wiod_indices, wiod_tooltip)
                    ],
                    opacity=alt.condition(lsoa_select_wales, alt.value(1), alt.value(0.2)),
                )
                .add_selection(lsoa_select_wales)
                .project(type="identity", reflectY=True)
            )
            st.altair_chart(
                choro_lsoa.configure_legend(
                    labelLimit=0,
                    titleLimit=0,
                    titleFontSize=13,
                    labelFontSize=13,
                    symbolStrokeWidth=1.5,
                    symbolSize=150,
                )
                .configure_view(strokeWidth=0)
                .configure_axis(
                    labelLimit=0,
                    titleLimit=0,
                ),
                use_container_width=True,
            )
        if choose=='Comparing Welsh and English IoD':
            st.title("Comparing IoD Deciles in England and Wales, by Lower Super Output Area (LSOA)")
            st.markdown(
            """
            The open source comparison dataset published is comprised of the domains; Income, Employment, 
            Income Deprivation Affecting Children Index (IDACI) and Income Deprivation Affecting Older People Index (IDAOPI) only.
            
            This figure allows you to compare a Local Authority (LA) in Wales to one in England for each IoD. 
            You can select a region of England and an LA to produce a map which shows the breakdown at Lower Super Output Area (LSOA).
            Similary you can select an LA from Wales to show the LSOA breakdown.

            You can hold shift and click on LSOA's from England and Wales. Selecting the LSOA's on the map will show them on the bar chart 
            below to compare the deciles. You can ouble-click to remove the all the selections and hover over the map to see the deciles.
            """
            )
            # Choose the colour palette:
            colour_choice = st.selectbox(
                "Choose a colour palette for the maps:",
                options=list(colour_palettes.keys()),
            )
            iod_combined_selection = st.selectbox(
                "Choose IoD Decile to view on the map:",
                options=iod_combined_names,
            )
            # Select box to pick the region you wish to look at.
            region_selection = st.selectbox(
                "Choose a region of England:",
                options=sorted(st.session_state.region_filter),
                key="region_lsoas",
            )
            las_to_plot = list(data_welsh_english[data_welsh_english["region_name"] == region_selection].lad19nm.unique())
            data_lsoa = data_welsh_english[data_welsh_english.region_name == region_selection]
            la_selection = st.selectbox(
                "Choose a local authority from the region chosen above to compare the LSOA breakdown:",
                sorted(las_to_plot),
            )
            welsh_la_selection = st.selectbox(
                "Choose a local authority from Wales to compare the LSOA breakdown:",
                sorted(data_wales.lad19nm.unique()),
            )
            # Dataset is larger than 5000, so we partition it into two smaller datasets.
            las_to_split = [
                "Brighton and Hove",
                "Medway",
                "Milton Keynes",
                "Southampton",
                "Portsmouth",
            ]
            if la_selection in las_to_split:
                filter_data_lsoa = data_lsoa[data_lsoa.lad19nm.isin(las_to_split)]
            else:
                filter_data_lsoa = data_lsoa[~data_lsoa.lad19nm.isin(las_to_split)]

            lsoas_to_plot = list(data_welsh_english[data_welsh_english.lad19nm == la_selection].lsoa11nm)
            region_dict = dict(
                zip(
                    st.session_state.region_filter,
                    preprocess_strings(pd.Series(st.session_state.region_filter)),
                )
            )
            geodata_lsoa = get_english_lsoa_shapefiles_2011(region_dict[region_selection])
            lsoa_select_multi = alt.selection_multi(fields=["lsoa11nm"])
            lsoa_select_multi_empty = alt.selection_multi(fields=["lsoa11nm"], empty='none')
            color_lsoa = alt.condition(
                lsoa_select_multi,
                alt.Color(
                    f"{iod_combined_dict[iod_combined_selection]}:O",
                    scale=colour_palettes[colour_choice],
                    title=f"{iod_combined_selection}",
                    legend=alt.Legend(orient="top"),
                ),
                alt.value("lightgray"),
            )
            choro_lsoa = (
                alt.Chart(geodata_lsoa)
                .mark_geoshape(
                    stroke="black",
                )
                .transform_lookup(
                    lookup="properties.lsoa11nm",
                    from_=alt.LookupData(
                        filter_data_lsoa,
                        "lsoa11nm",
                        ["lsoa11cd", "lsoa11nm", "lad19cd", "lad19nm"] + iod_combined_indices,
                    ),
                )
                .transform_filter(
                    alt.FieldOneOfPredicate(
                        field="properties.lsoa11nm", oneOf=lsoas_to_plot
                    )
                )
                .encode(
                    color=color_lsoa,
                    tooltip=[alt.Tooltip("lsoa11nm:N", title="LSOA")]
                    + [
                        alt.Tooltip(
                            f"{ind}:O", title=name, format="1.2f"
                        )
                        for ind, name in zip(iod_combined_indices, iod_combined_tooltip)
                    ],
                    opacity=alt.condition(lsoa_select_multi, alt.value(1), alt.value(0.2)),
                )
                .add_selection(lsoa_select_multi,lsoa_select_multi_empty)
                .project(type="identity", reflectY=True)
                .properties(width=500,height=500,title=la_selection)
            )

            welsh_lsoas_to_plot = list(data_welsh_english[data_welsh_english.lad19nm == welsh_la_selection].lsoa11nm)

            wales_data_comp = data_welsh_english[data_welsh_english.lsoa11nm.isin(welsh_lsoas_to_plot)]
            lsoa_select_wales_multi = alt.selection_multi(fields=["lsoa11nm"])
            lsoa_select_wales_multi_empty = alt.selection_multi(fields=["lsoa11nm"],empty='none')
            color_lsoa_wales = alt.condition(
                lsoa_select_wales_multi,
                alt.Color(
                    f"{iod_combined_dict[iod_combined_selection]}:O",
                    scale=colour_palettes[colour_choice],
                    title=f"{iod_combined_selection}",
                    legend=alt.Legend(orient="top"),
                ),
                alt.value("lightgray"),
            )
            choro_lsoa_wales = (
                alt.Chart(geodata_lsoa_wales)
                .mark_geoshape(
                    stroke="black",
                )
                .transform_lookup(
                    lookup="properties.lsoa11nm",
                    from_=alt.LookupData(
                        wales_data_comp,
                        "lsoa11nm",
                        ["lsoa11cd", "lsoa11nm", "lad19cd", "lad19nm"] + iod_combined_indices,
                    ),
                )
                .transform_filter(
                    alt.FieldOneOfPredicate(
                        field="properties.lsoa11nm", oneOf=welsh_lsoas_to_plot
                    )
                )
                .encode(
                    color=color_lsoa_wales,
                    tooltip=[alt.Tooltip("lsoa11nm:N", title="LSOA")]
                    + [
                        alt.Tooltip(
                            f"{ind}:O", title=name, format="1.2f"
                        )
                        for ind, name in zip(iod_combined_indices, iod_combined_tooltip)
                    ],
                    opacity=alt.condition(lsoa_select_wales_multi, alt.value(1), alt.value(0.2)),
                )
                .add_selection(lsoa_select_wales_multi,lsoa_select_wales_multi_empty)
                .project(type="identity", reflectY=True)
                .properties(title=welsh_la_selection)
            )
            choro_combined = alt.hconcat(choro_lsoa,choro_lsoa_wales)

            bar_chart = (
                alt.Chart(data_welsh_english)
                .mark_bar(color=NESTA_COLOURS[1])
                .encode(
                    x=alt.X(
                        f"{iod_combined_dict[iod_combined_selection]}:Q",
                        title=f"{iod_combined_selection}",
                        scale=alt.Scale(domain=[0, 10]),
                        axis=alt.Axis(tickMinStep=1),
                    ),
                    y=alt.Y(
                        "lsoa11nm:N",
                        title="LSOA Name",
                    ),
                )
                .transform_filter(lsoa_select_multi_empty | lsoa_select_wales_multi_empty)
                .properties(width=400, height=400)
            )

            st.altair_chart(
                alt.vconcat(choro_combined,bar_chart, center=True).configure_legend(
                    labelLimit=0,
                    titleLimit=0,
                    titleFontSize=13,
                    labelFontSize=13,
                    symbolStrokeWidth=1.5,
                    symbolSize=150,
                )
                .configure_view(strokeWidth=0)
                .configure_axis(
                    labelLimit=0,
                    titleLimit=0,
                ),
                use_container_width=True,
            )



# This adds on the password protection
pwd = st.sidebar.text_input("Password:", type="password")
# st.secrets reads it in from the toml folder, and then runs the streamlit_asq function if the password matches.
if pwd == st.secrets["PASSWORD"]:
    streamlit_iod()
elif pwd == "":
    pass
else:
    st.error("Password incorrect. Please try again.")
