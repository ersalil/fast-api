# title to be displayed in the FastAPI docs
title = 'Embarkation Manifest Backend'

# description to be displayed in the FastAPI docs
description = """
Embarkation Manifest. 🚀

## Description

You can **Analyse Embarkation Manifest**.

"""

# tags to be displayed in the FastAPI docs
tags_metadata = [
    {
        "name": "ship",
        "description": "Operations with users. The **login** logic is also here.",
    },
    {
        "name": "model",
        "description": "Column model for table.",
    }
]

ship_data = """
    NAME: SHIP DATA
    DESCRIPTION: The response body includes ShipID, ShipName and ShipCode of all the ships.
    """

embark_data = """
    NAME: EMBARKATION DATA
    DESCRIPTION: The response body contains the embarkation summary of all the ships viz unique voyageId, added Date and Time, OCI Count, MOCI Count, CheckedIn and Onboard Count, Ship Number and Code.
    """
data_overview= """
    NAME: LATEST VOYAGES
    DESCRIPTION: The response body contains the data of the latest 10 voyages of each Ship for further graphs depiction and analysis.
    """
voyage_data= """
    NAME: VOYAGE DATA
    DESCRIPTION: The response body contains the updated CheckedIn and Onboard Count formerly distributed with respect to the time bucket of 30 minutes for every voyage of every ship. This manipulation of data is the pre-requisites of Line Graph Representation on UI.
    """
avg_voyage_data= """
    NAME: AVERAGE VOYAGE DATA
    DESCRIPTION: The response body contains the average of all the voyages in a particular time frame. The range of time is distributed within 30 minutes buckets. This manipulation of data is the pre-requisites of Bar Graph Representation on UI.
    """
table_columns= """
    NAME: COLUMN NAMES OF TABLE
    DESCRIPTION: The response body contains the name of title of the column with the unique key created for every field.
    """
home= """
    NAME: ROOT PAGE
    DESCRIPTION: The home or the root link for accessing the backend contains the version, port and name of the application created.
    """
logs_stream= """
    NAME: LOGS
    DESCRIPTION: The log file is a computer-generated data file that contains information about usage patterns, activities, and operations within the application and is the primary data source for network observability.
    """
