## https://datatofish.com/how-to-connect-python-to-sql-server-using-pyodbc/
## https://github.com/mkleehammer/pyodbc/wiki/Connecting-to-SQL-Server-from-Windows#using-a-dsn
## https://datatofish.com/export-dataframe-to-csv/

## if terminal is giving a 407 proxy authentication error when using pip to install dependencies,
## ... try the following with your work login info:
## set http_proxy=http://username:password@healthproxy.health.dohmh.nycnet:8080

import pyodbc  ## bring in the ODBC drivers that allow me to connect to the DB
import pandas as pd  ## bring in the pandas library to work with data
import csv

## set up the connection using a user DSN (data source name) as per pyodbc wiki above
## 'EPHT_database' is the descriptive name i've given the DSN
conn = pyodbc.connect('DSN=EPHT_database;Trusted_Connection=yes;')  ##'conn' holds the connection

## read the public reports list view into a pandas dataframe
sql_list = pd.read_sql_query('SELECT * FROM ReportPublicList',conn)
sql_list.report_id = sql_list.report_id.astype(str) ## Convert to string to use later

for row in sql_list.itertuples():         ## Loop through all the items in 'sql_list' ... each row is a report
    fileName= 'output/'+ row.title + '_data.csv'   ## assign the value of the title field to 'title' variable
    ## next read sql into a data frame for the rows of data in the csv
    df = pd.read_sql_query('SELECT * FROM ReportData WHERE report_id = '+ row.report_id, conn)
    ## export the data frame to a csv
    df.to_csv (fileName, index = False, header=True)
    
    print(fileName +' is done')       ## status report


    
