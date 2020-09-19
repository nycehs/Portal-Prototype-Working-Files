# This script is to take the report data, and create bar graph svgs for each neighborhood and indicator
# SVGs will be used to populate the front report page

# Step one: import the csv into a pandas data frame
# https://www.datacamp.com/community/tutorials/pandas-to-csv
import pandas as pd 
import altair as alt
from altair_saver import save

df = pd.read_csv("visualizations/csv/Report82Data.csv")
#print(df)
# convert End Date to date data type
df.EndDate=pd.to_datetime(df.EndDate)
#df.Neighborhood=df['Neighborhood'].astype(string)
#df.infer_objects().dtypes
#print(df.dtypes)

# Step two: reduce the report file to only the rows we need
# - only neighborhood level records (geo_type_name of UHF42)
df = df[df.geo_type_name == 'UHF42']
#df = df[df.data_field_name == 'poveACSP']
#print(df)

# - only the most recent data End Date for each data field
#
df = df.sort_values('EndDate')
df = df.drop_duplicates(subset=['data_field_name','GeoJoinID'],keep='last')
#df = df.sort_values('data_field_name')
df = df.sort_values('GeoJoinID')

#print(df)

# Step three: for each data_field_name in the data frame, create a graph and write to SVG file
# - create a list of distinct data_field_name / Neighborhood s, 
df = pd.DataFrame(df, columns = ['data_field_name','Neighborhood','Data_Value'])
# - then loop through the list
for ind in df.index: 
     # do something
     print(df['data_field_name'][ind], df['Neighborhood'][ind]) 
     # - filter by data field name to create dataset
     dset = df[df.data_field_name == df['data_field_name'][ind]]
     dset = dset.sort_values('Data_Value')
     print(dset)
# - use Altair, the python connector to Vega-Lite
# - https://altair-viz.github.io/getting_started/overview.html
     alt.Chart(dset).mark_bar().encode(
         x=alt.X('Neighborhood', sort='y', axis=None),
         y=alt.Y('Data_Value', axis=None),
         # The highlight will be set on the result of a conditional statement
         color=alt.condition(
             alt.datum.Neighborhood == df['Neighborhood'][ind],  # If the year is 1810 this test returns True,
             alt.value('orange'),     # which sets the bar orange.
             alt.value('steelblue')   # And if it's not true it sets the bar steelblue.
        )
     ).configure(background='transparent').configure_axis(grid=False).properties(height=100,width=300).save('visualizations/images/' + df['data_field_name'][ind] +' '+ df['Neighborhood'][ind] + '.svg')
# - name each SVG with the data_field_name and the Neighborhood
# - store in the images folder for now
#print(df)