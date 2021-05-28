# Task list:
# 
# 
# # ---


import os
import json
from datetime import datetime
from markdownify import markdownify 

# create subtopic list by parsing indicator list json
# create indicator list by parsing indicator list json
with open('Python Data Management/subtopic_list.json') as f:
    subtopicList = json.load(f)
# print(subtopicList)
with open('Python Data Management/indicator_List.json') as f:
    indicatorList = json.load(f)
# print(indicatorList)
# remove indicator description for now - we may decide to bring back later?
for element in indicatorList:
    if 'description' in element:
        del element['description']
# for each subtopic, take subtopic 'slug' with no spaces as file name
for element in subtopicList:
    # print(element.get('page_name'))
    subtopicTitle = element.get('name')
    subtopicID = element.get('subtopic_id')
    subtopicInfo = element.get('more_info_data')
    subtopicInfo = str(subtopicInfo)
    subtopicInfo = markdownify(subtopicInfo)
    subtopicSlug = subtopicTitle.replace(',','')
    subtopicSlug = subtopicSlug.replace(' ','-')
    subtopicSlug = subtopicSlug.lower()
    # here we filter the indicators list to create an array of indicators for the current subtopic
    # Filter python objects with list comprehensions
    filteredIndicators = [x for x in indicatorList if x['subtopic_id'] == subtopicID]
    # Transform python object back into json
    filteredIndicators = json.dumps(filteredIndicators)
    # path to content folder for each indicator
    nPath = 'content/data_explorer/'

    if not os.path.exists(nPath):
        os.makedirs(nPath)

    try:
        f = open(nPath + subtopicSlug + ".md", 'w', encoding='utf-8')
        # perform file operations
        f.write("---\n")
        f.write("title: "+subtopicTitle+"\n")
        f.write("date: " + str(datetime.now())+"\n")
        f.write("draft: false\n")
        f.write("tags: \n")
        f.write("categories: []\n")
        f.write("keywords: \n")
        f.write("indicators: "+str(filteredIndicators)+"\n")
        f.write("---\n")
        f.write("# "+subtopicTitle+"\n")
        f.write("" + subtopicInfo +"\n")  #use markdownify here or earlier to convert html to markdown
    finally:
        f.close()
   
