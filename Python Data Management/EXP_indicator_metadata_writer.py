###########################################################################################
###########################################################################################
##
## Building indicators.json using nested DataFrames
##
###########################################################################################
###########################################################################################

#=========================================================================================#
# Setting up
#=========================================================================================#

#-----------------------------------------------------------------------------------------#
# Loading libraries
#-----------------------------------------------------------------------------------------#

import pyodbc
import pandas as pd

#-----------------------------------------------------------------------------------------#
# Connecting to BESP_Indicator database
#-----------------------------------------------------------------------------------------#

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# determining which driver to use
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #

drivers_list = pyodbc.drivers()

# odbc

odbc_driver_list = list(filter(lambda dl: "ODBC Driver" in dl, drivers_list))
odbc_driver_list.sort(reverse = True)

# native

native_driver_list = list(filter(lambda dl: "SQL Server Native Client" in dl, drivers_list))
native_driver_list.sort()

# deciding & setting

if len(odbc_driver_list) > 0:

    driver = odbc_driver_list[0]
    
elif len(native_driver_list) > 0:
    
    driver = native_driver_list[0]
    
else:
    
    driver = "SQL Server"

#-----------------------------------------------------------------------------------------#
# Connecting to BESP_Indicator
#-----------------------------------------------------------------------------------------#

EHDP_odbc = pyodbc.connect("DRIVER={" + driver + "};SERVER=SQLIT04A;DATABASE=BESP_Indicator;Trusted_Connection=yes;")


#=========================================================================================#
# Pulling & writing data
#=========================================================================================#

EXP_metadata_export = (
    pd.read_sql("SELECT * FROM EXP_metadata_export", EHDP_odbc)
    .sort_values(by = ["IndicatorID", "MeasureID", "end_period"])
)

#-----------------------------------------------------------------------------------------#
# nesting vis options
#-----------------------------------------------------------------------------------------#

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# map options
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #

# On: 0/1
# RankReverse: 0/1

measure_mapping = (
    EXP_metadata_export
    .loc[:, 
        [
            "IndicatorID",
            "MeasureID",
            "Map",
            "RankReverse"
        ]
    ]    
    .drop_duplicates()
    .rename(columns = {"Map": "On"})
    .groupby(["IndicatorID", "MeasureID"], dropna = False)
    .apply(lambda x: x[["On", "RankReverse"]].to_dict("records"))
    .reset_index()
    .rename(columns = {0: "Map"})
)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# trend options
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #

# On: 0/1
# Disparities: 0/1

measure_trend = (
    EXP_metadata_export
    .loc[:, 
        [
            "IndicatorID",
            "MeasureID",
            "Trend",
            "Disparities"
        ]
    ]    
    .drop_duplicates()
    .rename(columns = {"Trend": "On"})
    .groupby(["IndicatorID", "MeasureID"], dropna = False)
    .apply(lambda x: x[["On", "Disparities"]].to_dict("records"))
    .reset_index()
    .rename(columns = {0: "Trend"})
)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# linked measures
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #

# ==== specific link view ==== #

# because left-joining these 400 rows added 12k rows to the view

MeasureID_links = (
    pd.read_sql("SELECT * FROM MeasureID_links", EHDP_odbc)
    .sort_values(by = ["BaseMeasureID", "MeasureID"])
)

# ==== nesting links ==== #

measure_links = (
    MeasureID_links
    .drop_duplicates()
    .groupby(["BaseMeasureID"], dropna = False)
    .apply(lambda x: x[["MeasureID", "Axis"]].to_dict("records"))
    .reset_index()
    .rename(columns = {0: "Links", "BaseMeasureID": "MeasureID"})
)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# combining map, trend, and links, then nesting those under VisOptions
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #

vis_options = (
    pd.merge(
        measure_mapping,
        measure_trend,
        how = "left"
    )
    .merge(
        measure_links,
        how = "left"
    )
    .groupby(
        [
            "IndicatorID",
            "MeasureID"
        ],
        dropna = False
    )
    .apply(lambda x: x[[
        "Map", 
        "Trend", 
        "Links"
    ]].to_dict('records'))
    .reset_index()
    .rename(columns = {0: "VisOptions"})
)


#-----------------------------------------------------------------------------------------#
# nesting geotypes
#-----------------------------------------------------------------------------------------#

measure_geotypes = (
    EXP_metadata_export
    .loc[:, 
        [
            "IndicatorID",
            "IndicatorName",
            "IndicatorShortname",
            "IndicatorDescription",
            "MeasureID",
            "MeasurementType",
            "how_calculated",
            "Sources",
            "DisplayType",
            "GeoType"
        ]
    ]
    .drop_duplicates()
    .groupby(
        [
            "IndicatorID",
            "IndicatorName",
            "IndicatorShortname",
            "IndicatorDescription",
            "MeasureID",
            "MeasurementType",
            "how_calculated",
            "Sources",
            "DisplayType"
        ],
        dropna = False
    )
    .apply(lambda x: x[["GeoType"]].to_dict("records"))
    .reset_index()
    .rename(columns = {0: "AvailableGeographyTypes"})
)


#-----------------------------------------------------------------------------------------#
# nesting times
#-----------------------------------------------------------------------------------------#

measure_times = (
    EXP_metadata_export
    .loc[:, 
        [
            "IndicatorID",
            "IndicatorName",
            "IndicatorShortname",
            "IndicatorDescription",
            "MeasureID",
            "MeasurementType",
            "how_calculated",
            "Sources",
            "DisplayType",
            "TimeDescription",
            "start_period",
            "end_period"
        ]
    ]
    .drop_duplicates()
    .groupby(
        [
            "IndicatorID",
            "IndicatorName",
            "IndicatorShortname",
            "IndicatorDescription",
            "MeasureID",
            "MeasurementType",
            "how_calculated",
            "Sources",
            "DisplayType"
        ],
        dropna = False
    )
    .apply(lambda x: x[["TimeDescription", "start_period", "end_period"]].to_dict("records"))
    .reset_index()
    .rename(columns = {0: "AvailableTimes"})
)


#-----------------------------------------------------------------------------------------#
# combining geotype, times, and vis options, then nesting those under other measure-level info vars
#-----------------------------------------------------------------------------------------#

metadata = (
    pd.merge(
        measure_geotypes,
        measure_times,
        how = "left"
    )
    .merge(
        vis_options,
        how = "left"
    )
    .groupby(
        [
            "IndicatorID",
            "IndicatorName",
            "IndicatorShortname",
            "IndicatorDescription"
        ],
        dropna = False
    )
    .apply(lambda x: x[[
        "MeasureID", 
        "MeasurementType", 
        "how_calculated",
        "Sources",
        "DisplayType",
        "AvailableGeographyTypes",
        "AvailableTimes",
        "VisOptions"
    ]].to_dict('records'))
    .reset_index()
    .rename(columns = {0: "Measures"})
)


#-----------------------------------------------------------------------------------------#
# saving file
#-----------------------------------------------------------------------------------------#

metadata.to_json("Data Explorer Files/indicators.json", orient = "records", indent = 2)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# #
# #                             ---- THIS IS THE END! ----
# #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
