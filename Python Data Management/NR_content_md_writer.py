# Task list:
# - Create neighborhood slugs from each UHF, and create a
# folder for each one under content\neighborhood_reports
# - Create files for each folder:
##   - _index.md
# ---
## title: Canarsie - Flatlands
## type: location
## seo_title: "Canarsie - Flatlands"
## seo_description: "Neighborhood reports for the Canarsie - Flatlands neighborhood of New York City."
## seo_image: "/images/canarsie_flatlands.jpg"
# ---
# - report_name.md x5 reports:
# ---
## title: "Active Design and Health"
## neighborhood: "Canarsie - Flatlands"
## summary: "The design and conditions of buildings, streets, public transportation and parks influence physical activity, use of active transportation and other healthy behavior."
## data_json: "Active Design Physical Activity and Health in Canarsie - Flatlands"
## content_yml: "active_design"
## type: location
## seo_title: "Active Design and Health"
## seo_description: "Topics and indicators for active and healthy lifestyles in the Canarsie - Flatlands neighborhood in NYC."
## seo_image: "images/nyc_health_report_active_design_health.jpg"
# ---


import os
import json

# create neighborhood list by parsing neighborhood list json
# neighborhoodList =
with open('Python Data Management/UHF_List.json') as f:
    neighborhoodList = json.load(f)
# print(neighborhoodList)
with open('Python Data Management/Report_List.json') as f:
    reportList = json.load(f)
# print(reportList)
# for each neighborhood, take neighborhood 'slug' with no spaces, then
# ...use slug to create a neighborhood folder, then populate folder with necessary files
for element in neighborhoodList:
    # print(element.get('page_name'))
    neighborhoodTitle = element.get('UHF_name')
    neighborhoodSlug = element.get('page_name')
    # path to content folder for each neighborhood
    nPath = 'content/neighborhood_reports/' + neighborhoodSlug

    if not os.path.exists(nPath):
        os.makedirs(nPath)

    try:
        f = open(nPath + "/_index.md", 'w', encoding='utf-8')
        # perform file operations
        f.write("---\n")
        f.write("title: "+neighborhoodTitle+"\n")
        f.write("type: location\n")
        f.write("seo_title: "+"\""+neighborhoodTitle+"\"\n")
        f.write("seo_description: "+"\"Environmental Health data profiles for the " +
                neighborhoodTitle+" neighborhood of NYC.\"\n")
        f.write("seo_image: \""+""+"\"\n")
        f.write("---\n")
    finally:
        f.close()
    for report in reportList:
        # print(report.get('page_name'))
        reportName = report.get('title')
        reportTitle = report.get('title')+' in '+neighborhoodTitle
        reportDescription = report.get('report_description')
        reportPage = report.get('page_name')
        if reportPage == 'Active_Design_Physical_Activity_and_Health':
            contentYml = 'active_design'
            seoImagePath = 'images/nyc_health_report_active_design_health.jpg'
        elif reportPage == 'Housing_and_Health':
            contentYml = 'housing'
            seoImagePath = 'images/nyc_health_report_housing_and_health.jpg'
        elif reportPage == 'Outdoor_Air_and_Health':
            contentYml = 'outdoor'
            seoImagePath = 'images/nyc_health_report_outdoor_air_health.jpg'
        elif reportPage == 'Asthma_and_the_Environment':
            contentYml = 'asthma'
            seoImagePath = 'images/nyc_health_report_asthma_environment.jpg'
        elif reportPage == 'Climate_and_Health':
            contentYml = 'climate'
            seoImagePath = 'images/nyc_health_report_climate_health.jpg'
        else:
            print(reportName +
                  " needs yml and seoImage configuration. Is it a new report?")

        try:
            f = open(nPath + "/" + reportPage + ".md", 'w', encoding='utf-8')
            # perform file operations
            f.write("---\n")
            f.write("title: \""+reportName+"\"\n")
            f.write("neighborhood: \""+neighborhoodTitle+"\"\n")
            f.write("summary: \""+reportDescription+"\"\n")
            f.write("data_json: \""+reportTitle+"\"\n")
            f.write("content_yml: \""+contentYml+"\"\n")
            f.write("type: location\n")
            f.write("seo_title: "+"\""+reportTitle+"\"\n")
            f.write("seo_description: "+"\""+reportName+" data profile for the " +
                    neighborhoodTitle+" neighborhood of NYC.\"\n")
            f.write("seo_image: \""+seoImagePath+"\"\n")
            f.write("menu:\n")
            f.write("    main:\n")
            f.write("        identifier: '04'\n")
            f.write("---\n")
        finally:
            f.close()
