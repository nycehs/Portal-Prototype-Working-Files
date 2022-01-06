import pyodbc  ## bring in the ODBC drivers that allow me to connect to the DB

EHDP_odbc = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=SQLIT04A;DATABASE=BESP_Indicator;Trusted_Connection=yes;')

cursor = EHDP_odbc.cursor()        ## Create a cursor to do things with the DB connection
cursor.execute('SELECT subtopic_list FROM BESP_INDICATOR.dbo.Explorer_subtopic_list_JSON') ##execute SQL
result = cursor.fetchall()    ## Fetch all the records from the SQL query and put in 'result'

for subtopiclist in result:         ## Loop through all the items in 'result' ... each row is a report
    title='Python Data Management/Subtopic_List.json'  ## assign the value of the jsonTitle field to 'title' variable
    textj=subtopiclist.subtopic_list     ## assign the  json to the 'textj' variable
    new_file=open(title,mode="w",encoding="utf-8")  ## open/create file named by title variable
    new_file.write(textj)     ## write the json to the file
    new_file.close()          ## close and create the file
    print(title +' is done')       ## status report as each file completes
    
