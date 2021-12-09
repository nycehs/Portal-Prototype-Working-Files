###########################################################################################
###########################################################################################
##
## Building indicators.json using nested DataFrames
##
###########################################################################################
###########################################################################################

import pyodbc
import keyring
import pandas as pd

EHDP_odbc = pyodbc.connect('DSN=EHDP_stage;UID=bespadmin;PWD=' + keyring.get_password("EHDP", "bespadmin"))

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
    .apply(lambda x: x[["TimeDescription", "start_period", "end_period"]].to_dict('records'))
    .reset_index()
    .rename(columns = {0: "AvailableTimes"})
)

# combining geotype and times, then nesting those under other measure-level info vars

indicators = (
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

indicators.to_json("code/indicators_py.json", orient = 'records', indent = 2)
