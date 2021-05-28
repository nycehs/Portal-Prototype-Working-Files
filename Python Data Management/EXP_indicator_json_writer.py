import pyodbc  ## bring in the ODBC drivers that allow me to connect to the DB

conn = pyodbc.connect('DSN=EPHT_database;Trusted_Connection=yes;')  ##'conn' holds the connection

cursor = conn.cursor()        ## Create a cursor to do things with the DB connection
cursor.execute('SELECT indicator_list FROM BESP_INDICATOR.dbo.Explorer_indicator_list_JSON') ##execute SQL
result = cursor.fetchall()    ## Fetch all the records from the SQL query and put in 'result'

for indlist in result:         ## Loop through all the items in 'result' ... each row is a report
    title='Python Data Management/Indicator_List.json'  ## assign the value of the jsonTitle field to 'title' variable
    textj=indlist.indicator_list     ## assign the report json to the 'textj' variable
    new_file=open(title,mode="w",encoding="utf-8")  ## open/create file named by title variable
    new_file.write(textj)     ## write the json to the file
    new_file.close()          ## close and create the file
    print(title +' is done')       ## status report as each file completes
    
