###########################################################################################-
###########################################################################################-
##
##  Writing neighborhod report data
##
###########################################################################################-
###########################################################################################-

# This script writes data for the neighborhood reports, all saved as CSV. The data files
#   contain data broken out by report (e.g., Asthma and the Environment) and by
#   Measure (i.e., Indicator x Time Period)

#=========================================================================================#
# Setting up ----
#=========================================================================================#

#-----------------------------------------------------------------------------------------#
# Loading libraries
#-----------------------------------------------------------------------------------------#

library(tidyverse)
library(DBI)
library(dbplyr)
library(odbc)
library(lubridate)
library(fs)

#-----------------------------------------------------------------------------------------#
# Connecting to BESP_Indicator database
#-----------------------------------------------------------------------------------------#

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# determining which driver to use
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #

odbc_driver <- 
    odbcListDrivers() %>% 
    pull(name) %>% 
    unique() %>% 
    str_subset("ODBC Driver") %>% 
    sort(decreasing = TRUE) %>% 
    head(1)

if (length(odbc_driver) == 0) odbc_driver <- "SQL Server"


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# connecting using Windows auth with no DSN
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #

EHDP_odbc <-
    dbConnect(
        drv = odbc::odbc(),
        driver = paste0("{", odbc_driver, "}"),
        server = "SQLIT04A",
        database = "BESP_Indicator",
        trusted_connection = "yes"
    )


#=========================================================================================#
# Pulling and saving data ----
#=========================================================================================#

#-----------------------------------------------------------------------------------------#
# Pulling
#-----------------------------------------------------------------------------------------#

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# getting list of neighborhood reports
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #

report_list <- 
    EHDP_odbc %>% 
    tbl("ReportPublicList") %>% 
    collect()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# getting neighborhood report data
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #

# also joining report names to report data

report_data <- 
    EHDP_odbc %>% 
    tbl("ReportData") %>% 
    collect() %>% 
    left_join(
        report_list %>% select(report_id, title),
        .,
        by = "report_id"
    )


#-----------------------------------------------------------------------------------------#
# Saving
#-----------------------------------------------------------------------------------------#

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# saving big report data files
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #

# split by report_id, named using title

report_data_list <- 
    report_data %>% 
    group_by(report_id) %>% 
    group_split() %>% 
    walk(
        ~ write_csv(
            select(.x, -data_field_name),
            paste0("visualizations/csv/", unique(.x$title), "_data.csv")
            
        )
    )


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# saving measure-specific data
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #

measure_data_list <-
    report_data %>% 
    select(
        data_field_name,
        end_date,
        geo_join_id, 
        neighborhood,
        data_value, 
        message
    ) %>% 
    group_by(data_field_name, neighborhood) %>% 
    arrange(desc(end_date)) %>% 
    slice(1) %>% 
    select(-end_date) %>% 
    group_by(data_field_name) %>% 
    group_split() %>% 
    walk(
        ~ write_csv(
            select(.x, -data_field_name),
            paste0("visualizations/csv/", unique(.x$data_field_name), ".csv")
        )
    )


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# saving measure-specific data with trend variables
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #

measure_data_trend_list <- 
    report_data %>% 
    select(
        data_field_name,
        start_date, 
        time, 
        geo_join_id, 
        neighborhood,
        data_value, 
        message
    ) %>% 
    group_by(data_field_name) %>% 
    group_split() %>% 
    walk(
        ~ write_csv(
            select(.x, -data_field_name), 
            paste0("visualizations/csv/", unique(.x$data_field_name), "_trend.csv")
            
        )
    )


#=========================================================================================#
# Cleaning up----
#=========================================================================================#

dbDisconnect(EHDP_odbc)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# #
# #                             ---- THIS IS THE END! ----
# #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
