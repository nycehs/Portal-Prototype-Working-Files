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
# combining geotype and times, then nesting those under other measure-level info vars
#-----------------------------------------------------------------------------------------#

metadata = (
    pd.merge(
        measure_geotypes,
        measure_times,
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
        "AvailableTimes"
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
