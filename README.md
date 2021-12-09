# NYC Environmental Health Neighborhood Reports 
This repository includes wireframes and working files for the Environment & Health Data Portal's Neighborhood Reports.

## Python Data Management
This folder contains python scripts used to generate data files for the Neighborhood Reports. 

### Data explorer
- EXP_content_md_writer.py: converts existing subtopic content pages to markdown for the "Data Explorer"'s subtopics
- EXP_indicator_json_writer.py: writes a list of indicators and links as json
- EXP_measure_json_writer.py: writes Neighborhood Reports
- EXP_subtopic_json_writer.py: 
- indicators_json.py: writes our central Indicator/measure metadata json file.

### Neighborhood Reports
- NR_SparkBarExport.py: exports preview tiny bar charts for the Neighborhood Reports pages
- NR_content_md_writer: writes markdown for each neighborhood+report combination
- NR_data_csv_writer.py: writes the CSV files used for Neighborhood Reports data (one for each report)
- NR_json_writer.py: writes a json spec for each neighborhood+report combination (there is an update with measurementtype and units)

---

## Neighborhood Report wireframes
This repository presents prototypes and ongoing work to improve the neighborhood reports for NYC DOHMH Environmental Health. 
> - [Prototype can be accessed via Github Pages.](https://nycehs.github.io/NeighborhoodReports/NRPrototype.html)
> - [Current version of the reports can be accessed at the Environment and Health Data Portal](http://www.nyc.gov/health/environmentdata)

### Overview 
This project is to design and implement a web page to share easy to understand profiles of neighborhood environmental health data, based on an existing data/content API. 
These profiles will replace the existing profiles currently available on the Environment and Health Data Portal. They will be based on the user research and initial wireframing that our team has already done. 
The Environment & Health Data Portal team at DOHMH has been conducting research with users to understand how the Neighborhood Reports can best benefit them. From this research, we are developing design guidance for the contractor – these will include specifics about interaction, presentation, wireframes, and other initial material that the contractor will use as a starting point for this work. 
We hope that ongoing user research will continue to inform the design and development process, and Github pages can serve as a tool.

### Objectives
Users should be able to  
- Be introduced to the reports: what are they for?  
- Select a report to look at  
- Select a neighborhood in NYC that is relevant to them   

Things users should be able to do with the reports  
- See Indicator data for the selected neighborhood, with a description
- Understand the grouping of the indicators
- Find more depth of information on each indicator, by linking to EH data portal indicator pages
- Share specific reports via social media or email
- View reports on a mobile device
- Print reports

Build on existing city resources and standards  
- Styling / city design framework: the city digital blueprint, as much as possible using the [NYC Core Framework](https://github.com/CityOfNewYork/nyc-core-framework), a Bootstrap-based front-end framework with added design patterns and other components optimized for accessibility, translation, and clarity of presentation.

Accessibility: the [city’s standards and guidance](https://blueprint.cityofnewyork.us/accessibility/)

Build Mobile First  
- All components of this project need to render well in a variety of mobile browsers, both tablet and phone. At minimum, testing with all mobile form factors supported in the Chrome developer tools emulator should be covered.  

Build in the open  
- We’d like development to happen in the open in a shared github repository, so that we can participate more easily in review, etc. Our staff will need to be able to deploy the code ourselves.


