import matplotlib.pylab as plt
import matplotlib.colors as pltcol
import altair as alt

# Creating dictionaries for the IoD.
iod_indices = [
    "a_index_of_multiple_deprivation_imd",
    "b_income_deprivation_domain",
    "c_employment_deprivation_domain",
    "d_education_skills_and_training_domain",
    "e_health_deprivation_and_disability_domain",
    "f_crime_domain",
    "g_barriers_to_housing_and_services_domain",
    "h_living_environment_deprivation_domain",
    "i_income_deprivation_affecting_children_index_idaci",
    "j_income_deprivation_affecting_older_people_index_idaopi",
]
iod_names = [
    "Index of Multiple Deprivation (IMD)",
    "Income Deprivation",
    "Employment Deprivation",
    "Education, Skills and Training",
    "Health Deprivation and Disability",
    "Crime",
    "Barriers to Housing and Services",
    "Living Environment Deprivation",
    "Income Deprivation Affecting Children Index (IDACI)",
    "Income Deprivation Affecting Older People Index (IDAOPI)",
]

# Creating Dictionaries to link the two indices,
iod_dict = dict(zip(iod_names, iod_indices))
iod_dict_inv = dict(zip(iod_indices, iod_names))

# Colour Pallette for the Choropleth maps
# As we are looking at the Deciles, we will have 10 points.
summer_palette = [ 
    "#f94144","#f3722c","#f8961e","#f9844a","#f9c74f","#90be6d","#43aa8b","#4d908e","#577590","#277da1"
]
winter_palette = [ 
    "#7400b8","#6930c3","#5e60ce","#5390d9","#4ea8de","#48bfe3","#56cfe1","#64dfdf","#72efdd","#80ffdb"
]
domain = [i + 1 for i in range(10)]
colour_palettes = {
    'Spring' : alt.Scale(domain=domain,scheme='yellowgreenblue',reverse=False),
    'Summer' : alt.Scale(domain=domain,range=summer_palette),
    'Autumn' : alt.Scale(domain=domain,scheme='plasma',reverse=True),
    'Winter' : alt.Scale(domain=domain,range=winter_palette,reverse=True)
}
