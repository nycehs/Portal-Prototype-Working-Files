###########################################################################################
###########################################################################################
##
## Indicators list for Data Explorer
##
###########################################################################################
###########################################################################################


import pyodbc  ## bring in the ODBC drivers that allow me to connect to the DB
import pandas as pd

#-----------------------------------------------------------------------------------------#
# Connecting to BESP_Indicator database
#-----------------------------------------------------------------------------------------#

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# determining which driver to use
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #

drivers_list = pyodbc.drivers()

odbc_driver_list = list(filter(lambda dl: "ODBC Driver" in dl, drivers_list))
odbc_driver_list.sort(reverse = True)

native_driver_list = list(filter(lambda dl: "SQL Server Native Client" in dl, drivers_list))
native_driver_list.sort()


if len(odbc_driver_list) > 0:

    driver = odbc_driver_list[0]
    
elif len(native_driver_list) > 0:
    
    driver = native_driver_list[0]
    
else:
    
    driver = "SQL Server"


EHDP_odbc = pyodbc.connect("DRIVER={" + driver + "};SERVER=SQLIT04A;DATABASE=BESP_Indicator;Trusted_Connection=yes;")

cursor = EHDP_odbc.cursor()        ## Create a cursor to do things with the DB connection
cursor.execute('SELECT indicator_list FROM BESP_INDICATOR.dbo.Explorer_indicator_list_JSON') ##execute SQL
result = cursor.fetchall()    ## Fetch all the records from the SQL query and put in 'result'

for indlist in result:         ## Loop through all the items in 'result' ... each row is a report
    title='Python Data Management/Indicator_List.json'  ## assign the value of the jsonTitle field to 'title' variable
    textj=indlist.indicator_list     ## assign the report json to the 'textj' variable
    new_file=open(title,mode="w",encoding="utf-8")  ## open/create file named by title variable
    new_file.write(textj)     ## write the json to the file
    new_file.close()          ## close and create the file
    print(title +' is done')       ## status report as each file completes
    
