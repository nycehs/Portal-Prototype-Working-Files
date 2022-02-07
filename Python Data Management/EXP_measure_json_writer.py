###########################################################################################
###########################################################################################
##
## Building indicators.json using nested DataFrames
##
###########################################################################################
###########################################################################################

import pyodbc
import pandas as pd

EHDP_odbc = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=SQLIT04A;DATABASE=BESP_Indicator;Trusted_Connection=yes;')

metadata = (
    pd.read_sql("SELECT * FROM metadata_for_indicators_json", EHDP_odbc)
    .sort_values(by = ["IndicatorID", "MeasureID", "end_period"])
)

# nesting geotypes and times

measure_geotypes = (
    metadata
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
    .apply(lambda x: x[["GeoType"]].to_dict('records'))
    .reset_index()
    .rename(columns = {0: "AvailableGeographyTypes"})
)

measure_times = (
    metadata
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
            "end_period",
            "TimeType"
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
    .apply(lambda x: x[["TimeDescription", "start_period", "end_period", "TimeType"]].to_dict('records'))
    .reset_index()
    .rename(columns = {0: "AvailableTimes"})
)

# combining geotype and times, then nesting those under other measure-level info vars

measures = (
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

# saving file

measures.to_json("Data Explorer Files/indicators.json", orient = 'records', indent = 2)
