# cdr-processing
A set of python scripts to simulate telecoms call detail record (CDR) creation and processing. Developed using Python 3.8.3 and with minimal use of third party packages.  The aim of this project is to code everything in Python to keep the codebase small and to demonstrate how much functionality we can achieve with minimal amount of code.

The CDR file created is structured as follows, will all fields enclosed in double quotes.

| Field                    | Description              | Example                               |
|--------------------------|--------------------------|---------------------------------------|
| Call Type                | Mobile or fixed          | M                                     |
| Customer Identifier      | Calling number           | +447969789881                         |
| Telephone Number Dialed  | Called number            | +447933401840                         |
| Call Date                | Date call made           | 05/06/2020                            |
| Call Time                | Time of call             | 15:29:31                              |
| Duration                 | In seconds               | 327                                   |
| Country of Origin        | Call made from           | GBR                                   |
| Network                  | Network Operator         | Virgin Mobile                         |
| Ring Time                | Seconds before answer    |                                       |
| RecordID                 | Unique ID for record     | 0ee76862-bdd7-4dae-8d37-57378fac6978  |
| Cell ID                  | ID of cell tower         | 1                                     |
| Call Lat                 | Latitude call made from  | 52.514627                             |
| Call Long                | Longitude call made from | -2.143291                             |


## gencdr.py

This creates a user specified number of random call detail records.  A small number of records are created for a single calling phone with random geographic coordinates to simulate caller movement.  This is based on a provided latitude and longitude with each subsequent record randomised to be located within a five-mile radius of the previous record.  If a GeoJSON file is provided that represent a geographic boundary the random locations will be constrained to be within that boundary.  A set of GeoJSON files representing different countries are filed under the data folder.

The header row would be:
```
"Call Type","Customer Identifier","Telephone Number Dialed","Call Date","Call Time","Duration","Country of Origin","Network","Ring Time","RecordID","Cell ID","Cell Lat","Cell Long"
```
Each record created would appear as follows with all of the data randomised.
```
"M","+447969789881","+447933401840","05/06/2020","15:29:31","349","GBR","Virgin Mobile","3","4891ffee-bc4c-4f1c-9fe9-405d55a89817","0","52.514627","-2.143291"
```

## data.py

Supporting data for the gencdr.py script.  Data includes a list of mobile operators, UK and WiFi (tables) mobile phone codes, a few locations and a full list of UK towns.

## geo.py

Utility functions that perform the geo randomisation, validation and calculate the distance between locations.

## map.py

The is a command line utility to read a file of CDR records that contain latitude and longitude coordinates specified in WGS 84 and create a GeoJSON output.  This can be used to visualise the location from where a call was made or the cell tower that was used.  There command line options are:

-m an optional flag that will generate a minimised GeoJSON file.
-i used to specify the input files
-x used to specify the field in the file that holds the latitude
-y used to specify the field in the file that holds the longitude

  
