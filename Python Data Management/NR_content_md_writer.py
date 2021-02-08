## Task list: 
## - Create neighborhood slugs from each UHF, and create a 
##   folder for each one under content\neighborhood_reports
## - Create files for each folder: 
##   - _index.md
    ## ---
    ## title: Canarsie - Flatlands
    ## type: location
    ## seo_title: "Canarsie - Flatlands"
    ## seo_description: "Neighborhood reports for the Canarsie - Flatlands neighborhood of New York City."
    ## seo_image: "/images/canarsie_flatlands.jpg"
    ## ---
##   - report_name.md x5 reports: 
    ## ---
    ## title: "Active Design and Health"
    ## neighborhood: "Canarsie - Flatlands"
    ## summary: "The design and conditions of buildings, streets, public transportation and parks influence physical activity, use of active transportation and other healthy behavior."
    ## data_json: "Active Design Physical Activity and Health in Canarsie - Flatlands"
    ## content_yml: "active_design"
    ## type: location
    ## seo_title: "Active Design and Health"
    ## seo_description: "Topics and indicators for active and healthy lifestyles in the Canarsie - Flatlands neighborhood in NYC."
    ## seo_image: "images/nyc_health_report_active_design_health.jpg"
    ## ---


import os
import json

# create neighborhood list by parsing neighborhood list json
#neighborhoodList = 
# for each neighborhood, create neighborhood 'slug' with no spaces, then
# ...use slug to create a neighborhood folder, then populate folder with necessary files
neighborhoodTitle = 'Rockaways'
neighborhoodSlug = 'Rockaways'
nPath = 'content/neighborhood_reports/' + neighborhoodSlug # path to content folder for each neighborhood

if not os.path.exists(nPath):
    os.makedirs(nPath)

try:
   f = open(nPath + "/_index.md", 'w', encoding = 'utf-8')
   # perform file operations
   f.write("---\n")
   f.write("## title: "+neighborhoodTitle+"\n")
   f.write("## type: location\n")
   f.write("## seo_title: "+"\""+neighborhoodTitle+"\"\n")
   f.write("## seo_description: "+"\"Environmental Health data profiles for the "+neighborhoodTitle+" neighborhood of NYC.\"\n")
   f.write("## seo_image: "+""+"\n")
   f.write("---\n")
finally:
   f.close()
