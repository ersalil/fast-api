# title to be displayed in the FastAPI docs
title = 'Embarkation Manifest Backend'

# description to be displayed in the FastAPI docs
introduction = """
A single page monitoring system of **Embarkation History** and Data Analytics for **N most recent voyages** of each ship 🚢.

## Description
+ **Database**: PostgreSQL
+ **Schema**: public
+ **Project** Table Scope:
    - embark_summary : contains the embarkation manifest data
    - voyage : contains the voyage data
    - environment : contains the environment data corresponding to each ship
    - ship : contains the ship data
"""

# tags to be displayed in the FastAPI docs
tags_metadata = [
    {
        "name": "Master Data",
        "description": "Master Data APIs, that fetches the data from the database",
    },
    {
        "name": "Lookup Data",
        "description": "Key attributes of the **Master Data**, like column names, data types, etc.",
    }
]

description = {
    "voyage":
    {
        "name": "Get Checkedin and Onboard Count for n voyages for a ship",
        "description": """The response body contains the updated CheckedIn and Onboard Count formerly distributed with respect to the time bucket of 30 minutes for N voyages of every ship. 
                        \nThis manipulation of data is the pre-requisites of Line Graph Representation on UI."""
    },
    "avg_voyage":
    {
        "name": "Get Average of CheckedIn and Onboard Count for n voyages for a ship",
        "description": """The response body contains the average of all the voyages in a particular time frame. The range of time is distributed within 30 minutes buckets. 
                        \nThis manipulation of data is the pre-requisites of Bar Graph Representation on UI"""
    },
    "overview":
    {
        "name": "Get Brief Summary of each voyage",
        "description": """The response body contains the summarized data of the latest N voyages of each Ship used for further graphs depiction and analysis."""
    },
    "table_keys":
    {
        "name": "Get Column Names of the Table",
        "description": """The response body contains the column names of the table and their coressponding keys."""
    },
    "status":
    {
        "name": "Get the status of the backend service",
        "description": """The response body contains the status of the backend service.
                        \n-> The **production version** of the backend service.
                        \n-> The **port number** of the backend service running on.
                        \n-> The **Heatlh** is either **Green** means **UP Running** or **Red** means **DOWN**.
                        \n-> The **Name** of the backend service (taken from container name).
                        """
    }
}