# Observador de estaciones climatológicas

[Readme in English](README.md)

Esta aplicación ha sido desarrollada como parte del curso de Aplicaciones y Servicios Telemáticos de la Universidad del Cauca. La aplicación permite visualizar en un mapa las estaciones climatológicas de un país en particular a partir de la información contenida en el archivo 'isd-history.csv' de la NOAA de Estados Unidos.

## Funcionamiento de la app
La aplicación está desarrollada en Python y utiliza la biblioteca Tkinter para la interfaz gráfica de usuario. Para la manipulación y visualización de datos se utiliza PySpark y Open Layers.

La aplicación consta de una pantalla principal en la que el usuario puede ingresar el código de país según los datos de la NOAA y hacer clic en el botón "Procesar". Al hacerlo, se genera un dataframe con los datos de ubicación (latitud y longitud) de todas las estaciones climatológicas correspondientes a ese país y genera un archivo JSON con la información de las estaciones climatológicas del país seleccionado.

Además, se grafican con ayuda de Open Layers cada una de estas estaciones como puntos rojos en el mapa, esta funcionalidad, através de una interfaz web.

## Requerimientos

- Python 3
- Tkinter
- PySpark
- OpenLayers
- Servidor Web (puede ser local)

## Contribuciones
Este proyecto ha sido desarrollado como parte de un curso académico y no aceptamos contribuciones externas. Sin embargo, si encuentra algún error o problema en la aplicación, puede informarlo a través de los issues en este repositorio.
