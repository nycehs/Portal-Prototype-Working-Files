## first pull the data out of the database into pandas dataframes
## use group by and lambda functions to create first layer
## Append place nodes to each measure
## Append time nodes to each measure
## Loop through and write JSON file for each indicator


import pyodbc  ## bring in the ODBC drivers that allow me to connect to the DB
import pandas as pd  ## bring in the pandas library to work with data
import os
import json
from datetime import datetime


##conn = pyodbc.connect('DSN=EPHT_prod;Trusted_Connection=yes;')  ##'conn' holds the connection
conn = pyodbc.connect('DSN=EPHT_staging;Trusted_Connection=yes;')  ##'conn' holds the connection

## read the measures list view into a pandas dataframe
measures = pd.read_sql_query('SELECT * FROM BESP_INDICATORANALYSIS.dbo.IndicatorMeasureMetadata',conn)

## read the measure places list view into a pandas dataframe
mPlace = pd.read_sql_query('SELECT * FROM BESP_INDICATORANALYSIS.dbo.measurePlaces',conn)

## read the measure times list view into a pandas dataframe
mTime = pd.read_sql_query('SELECT * FROM BESP_INDICATORANALYSIS.dbo.measureTimes',conn)

