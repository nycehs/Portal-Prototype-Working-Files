# Task list:
# - Create indicator slugs from each UHF, and create a
# folder for each one under content\indicator_reports
# - Create files for each folder:
##   - _index.md
# ---
## title: Canarsie - Flatlands
## type: location
## seo_title: "Canarsie - Flatlands"
## seo_description: "indicator reports for the Canarsie - Flatlands indicator of New York City."
## seo_image: "/images/canarsie_flatlands.jpg"
# ---
# - report_name.md x5 reports:
# ---
## title: "Active Design and Health"
## indicator: "Canarsie - Flatlands"
## summary: "The design and conditions of buildings, streets, public transportation and parks influence physical activity, use of active transportation and other healthy behavior."
## data_json: "Active Design Physical Activity and Health in Canarsie - Flatlands"
## content_yml: "active_design"
## type: location
## seo_title: "Active Design and Health"
## seo_description: "Topics and indicators for active and healthy lifestyles in the Canarsie - Flatlands indicator in NYC."
## seo_image: "images/nyc_health_report_active_design_health.jpg"
# ---


import os
import json
from datetime import datetime
# from markdownify import markdownify 

# create subtopic list by parsing indicator list json
# create indicator list by parsing indicator list json
with open('Python Data Management/subtopic_list.json') as f:
    subtopicList = json.load(f)
# print(subtopicList)
with open('Python Data Management/indicator_List.json') as f:
    indicatorList = json.load(f)
# print(indicatorList)
# for each indicator, take indicator 'slug' with no spaces, then
# ...use slug to create a indicator folder, then populate folder with necessary files
for element in subtopicList:
    # print(element.get('page_name'))
    subtopicTitle = element.get('name')
    subtopicID = element.get('subtopic_id')
    subtopicInfo = element.get('more_info_data')
    subtopicInfo = str(subtopicInfo)
    subtopicSlug = subtopicTitle.replace(',','')
    subtopicSlug = subtopicSlug.replace(' ','-')
    subtopicSlug = subtopicSlug.lower()
    # path to content folder for each indicator
    nPath = 'content/data_explorer/'

    if not os.path.exists(nPath):
        os.makedirs(nPath)

    try:
        f = open(nPath + subtopicSlug + ".md", 'w', encoding='utf-8')
        # perform file operations
        f.write("---\n")
        f.write("title: "+subtopicTitle+"\n")
       # f.write("date: " + datetime.now()+"\n")
        f.write("draft: false\n")
        f.write("tags: \n")
        f.write("categories: \n")
        f.write("keywords: \n")
        f.write("---\n")
        f.write("" + subtopicInfo +"\n")  #use markdownify here to convert html to markdown
    finally:
        f.close()
   
