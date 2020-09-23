import pyodbc  ## bring in the ODBC drivers that allow me to connect to the DB

conn = pyodbc.connect('DSN=EPHT_database;Trusted_Connection=yes;')  ##'conn' holds the connection

cursor = conn.cursor()        ## Create a cursor to do things with the DB connection
cursor.execute('SELECT jsonTitle,jsonText FROM BESP_INDICATOR.dbo.ReportJSON') ##execute SQL
result = cursor.fetchall()    ## Fetch all the records from the SQL query and put in 'result'

for report in result:         ## Loop through all the items in 'result' ... each row is a report
    title='output/'+ report.jsonTitle  +'.json'  ## assign the value of the jsonTitle field to 'title' variable
    textj=report.jsonText     ## assign the report json to the 'textj' variable
    new_file=open(title,mode="w",encoding="utf-8")  ## open/create file named by title variable
    new_file.write(textj)     ## write the json to the file
    new_file.close()          ## close and create the file
    print(report.jsonTitle +' is done')       ## status report
    
