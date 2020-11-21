# This script is to take the report data, and create bar graph svgs for each neighborhood and indicator
# SVGs will be used to populate the front report page

# Step one: import the csv into a pandas data frame
# https://www.datacamp.com/community/tutorials/pandas-to-csv
import pandas as pd 
import altair as alt
from altair_saver import save

## df = pd.read_csv("visualizations/csv/Housing and Health _data.csv")
## df = pd.read_csv("visualizations/csv/Outdoor Air and Health_data.csv")
## df = pd.read_csv("visualizations/csv/Active Design Physical Activity and Health_data.csv")
## df = pd.read_csv("visualizations/csv/Asthma and the Environment_data.csv")
df = pd.read_csv("visualizations/csv/Climate and Health_data.csv")
#print(df)
# convert End Date to date data type
df.end_date=pd.to_datetime(df.end_date)
#df.Neighborhood=df['Neighborhood'].astype(string)
#df.infer_objects().dtypes
#print(df.dtypes)

# Step two: reduce the report file to only the rows we need
# - only neighborhood level records (geo_type_name of UHF42)
df = df[df.geo_type == 'UHF42']
#df = df[df.data_field_name == 'poveACSP']
#print(df)

# - only the most recent data End Date for each data field
#
df = df.sort_values('end_date')
df = df.drop_duplicates(subset=['data_field_name','geo_join_id'],keep='last')
#df = df.sort_values('data_field_name')
df = df.sort_values('geo_join_id')
df['geo_join_id'] = df['geo_join_id'].astype(str) 
# - converted the integer to string so that I can concatenate to an image title later

#print(df)

# Step three: for each data_field_name in the data frame, create a graph and write to SVG file
# - create a list of distinct data_field_name / Neighborhood s, 
df = pd.DataFrame(df, columns = ['data_field_name','neighborhood','data_value','geo_join_id'])
# - then loop through the list
for ind in df.index: 
     # do something
     print(df['data_field_name'][ind], df['neighborhood'][ind]) 
     # - filter by data field name to create dataset
     dset = df[df.data_field_name == df['data_field_name'][ind]]
     dset = dset.sort_values('data_value')
     print(dset)
# - use Altair, the python connector to Vega-Lite
# - https://altair-viz.github.io/getting_started/overview.html
     alt.Chart(dset).mark_bar().encode(
         x=alt.X('neighborhood', sort='y', axis=None),
         y=alt.Y('data_value', axis=None),
         # The highlight will be set on the result of a conditional statement
         color=alt.condition(
             alt.datum.neighborhood == df['neighborhood'][ind],  # If the neighborhoods match this test returns True,
             alt.value('#00923E'),     # which sets the bar orange.
             alt.value('#D2D4CE')   # And if it's not true it sets the bar steelblue.
        )
     ).configure(background='transparent').configure_axis(grid=False)
          .configure_view(strokeWidth=0)
          .properties(height=100,width=300)
          .save('visualizations/images/' + df['data_field_name'][ind] +'_'+ df['geo_join_id'][ind] + '.svg')
     # - viewBox="0 0 310 110" must be removed for ModLab team
     # - https://stackoverflow.com/questions/59058521/creating-a-script-in-python-to-alter-the-text-in-an-svg-file
     Change = open('visualizations/images/' + df['data_field_name'][ind] +'_'+ df['geo_join_id'][ind] + '.svg', "rt")
     data = Change.read()
     data = data.replace('viewBox="0 0 310 110"', 'preserveAspectRatio=“none”')
     Change.close()
     Change = open('visualizations/images/' + df['data_field_name'][ind] +'_'+ df['geo_join_id'][ind] + '.svg', "wt")
     Change.write(data)
     Change.close()
# - name each SVG with the data_field_name and the Neighborhood
# - store in the images folder for now
#print(df)