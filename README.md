# Climatological Station Spotter

[Readme en Español](README(es).md)

This application was developed as part of the Telematic Applications and Services course at the University of Cauca. The application allows users to visualize the climatological stations of a particular country on a map, using information from the 'isd-history.csv' file from the United States NOAA.

## How the app works
The application is developed in Python and uses the Tkinter library for the graphical user interface. PySpark and Open Layers are used for data manipulation and visualization.

The application consists of a main screen where the user can enter the country code according to NOAA data and click the "Process" button. This generates a dataframe with location data (latitude and longitude) of all the climatological stations corresponding to that country and generates a JSON file with the information of the selected country's climatological stations.

In addition, using Open Layers, each of these stations is graphed as red points on a map through a web interface.

## Requirements

- Python 3
- Tkinter
- PySpark
- OpenLayers
- Servidor Web (puede ser local)

## Contributions
This project was developed as part of an academic course and we do not accept external contributions. However, if you find any errors or issues in the application, you can report them through the issues in this repository.
