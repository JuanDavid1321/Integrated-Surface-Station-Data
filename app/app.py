#------------------------------------------------------------------------------------------------------------------------
# Énfasis 3: Trabajo de estaciones climatológicas
# Presentado por: Juan David Carvajal Cucuñame
#------------------------------------------------------------------------------------------------------------------------
from pyspark.sql import SparkSession
from pyspark.sql.functions import regexp_replace, when, col
import json
import tkinter as tk

spark = SparkSession.builder.appName("estaciones").getOrCreate()

#------------------------------------------------------------------------------------------------------------------------

# Definir rutas
ruta_datos = '/home/jdcarvajal/trabajo_estaciones/isd-history.csv'
ruta_json = '/home/jdcarvajal/trabajo_estaciones/result.json'

#------------------------------------------------------------------------------------------------------------------------
# Leer un .csv debido a que la NOAA lo tiene formateado con estructura de datos, 
# facilitando la composición del data frame. Con el archivo de texto plano se tendría
# el problema de los espacios en blanco correspondientes a valores nulos
#------------------------------------------------------------------------------------------------------------------------

# Función de Spark que procesa el texto ingresado por el usuario
def procesar_consulta(texto):

    # Creación de lista de nombre de columnas del DF
    columnas_df = ["USAF", "WBAN", "STATION_NAME", "Country", "ST", "CALL", "Latitud", "Longitud", "ELEV", "BEGIN", "END"]

    # Leer el archivo en la ruta específica con SparkSession
    archivo = spark.read.csv(ruta_datos)

    #--------------------------------------------------------------------------------------------------------------------

    # Tener en cuenta que el * desempaqueta la lista en argumentos individuales
    archivo = archivo.toDF(*columnas_df)

    # Selección de las columnas de interés
    archivo = archivo.select(col('Country'), col('Latitud'), col('Longitud'))

    # Aplicar las transformaciones necesarias
    archivo = archivo.select(

        # Cambia el valor de los elementos nulos en la columna 'Country'
        when(archivo.Country.isNull(),'0').otherwise(archivo.Country).alias('Country'),

        # Cambia los elementos nulos, además de los elementos en ceros mal formateados en la columna 'Latitud'
        regexp_replace(when(archivo.Latitud.isNull() | 
                            (archivo.Latitud == '+00.000') | 
                            (archivo.Latitud == '+000.000'),'0.000'
                            ).otherwise(archivo.Latitud), r'^\+', ''
                        ).alias('Latitud'),

        # Cambia los elementos nulos, además de los elementos en ceros mal formateados en la columna 'Longitud'
        regexp_replace(when(archivo.Longitud.isNull() | 
                            (archivo.Longitud == '+00.000') | 
                            (archivo.Longitud == '+000.000'), '00.000'
                            ).otherwise(archivo.Longitud), r'^\+', ''
                        ).alias('Longitud')
    )

    # Eliminar los ceros a la izquierda, pero si hay signo '-' mantenerlo
    archivo = archivo.withColumn("Longitud", regexp_replace("Longitud", "^(-)?0+(?!\\.)(?=\\d)", "$1"))
    archivo = archivo.withColumn("Latitud", regexp_replace("Latitud", "^(-)?0+(?!\\.)(?=\\d)", "$1"))

    #--------------------------------------------------------------------------------------------------------------------

    query = archivo.filter(archivo['Country']==texto)
    
    # Formato de datos para conversión a json
    json_result = []
    for row in query.rdd.collect():
        json_data = {
            "country": row.Country,
            "latitude": row.Latitud,
            "longitud": row.Longitud
        }
        json_result.append(json_data)
    
    # Escribir en el archivo result.json
    with open(ruta_json, 'w') as f:
        f.write(json.dumps(json_result))
    query.show()

#------------------------------------------------------------------------------------------------------------------------

# Función que se ejecuta al presionar el botón en la interfaz gráfica
def procesar():
    texto = entrada.get().upper()
    procesar_consulta(texto)

#------------------------------------------------------------------------------------------------------------------------

# Función que se ejecuta al presionar el enlace en la interfaz gráfica
def abrir_enlace():
    import webbrowser
    webbrowser.open("localhost:5500/app/views/index.html")
    # ventana.destroy()

#------------------------------------------------------------------------------------------------------------------------

# Crear la ventana de la interfaz gráfica
ventana = tk.Tk()
ventana.title("Estaciones Climatológicas")

# Establecer configuración general de ventana
ventana.configure(background='#1b1b32')
ventana.geometry("400x320")


# Crear el campo de entrada de texto
label = tk.Label(ventana, text="Ingrese el país a filtrar:")
label.configure(foreground='#fecc4c', background='#1b1b32', font=('default', 20))
label.pack(pady=20)

entrada = tk.Entry(ventana)
entrada.configure(font=('default', 20), width=5, justify="center", fg='#f63169')
entrada.pack()

# Crear el botón para procesar el texto
boton = tk.Button(ventana, text="Procesar", command=procesar)
boton.configure(font=('default', 12))
boton.pack(pady=50)


# Crear el componente de enlace web
enlace = tk.Label(ventana, text="¡Graficar!", fg="light grey", cursor="hand2")
enlace.configure(background='#1b1b32', font=('default', 20), borderwidth=.5, relief="groove")
enlace.pack(pady=20)

# Configurar el enlace
enlace.bind("<Button-1>", lambda e: abrir_enlace())

# Ejecutar la ventana
ventana.mainloop()
