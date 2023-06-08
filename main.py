import json
from fastapi import FastAPI
import pandas

app = FastAPI(title="API para el manejo de datos de sensores", version="1.0")


@app.get("/get_data")
def read_csv():
    """
    Función que lee el archivo csv y devuelve los datos filtrados por el mes de abril y año 2018
    de los sensores 07 y 47 con las columnas timestamp y machine_status
    Returns:
        [json]: [datos filtrados]
    """
    #Leemos el archivo csv
    data = pandas.read_csv('sensor.csv')

    #Convertimos la columna "timestamp" a formato fecha datetime
    data["timestamp"] = pandas.to_datetime(data["timestamp"])

    #Filtramos los datos por el mes de abril y año 2018
    data_filtered = data[(data["timestamp"].dt.month == 4) & (data["timestamp"].dt.year == 2018)]

    #Filtramos las mediciones de los sensores 07 y 47 con las columnas timestamp y machine_status
    data_filtered_sensor_07 = data_filtered[["timestamp", "machine_status", "sensor_07"]]
    data_filtered_sensor_47 = data_filtered[["timestamp", "machine_status", "sensor_47"]]

    #Convertimos los datos de la lista a un dataframe
    df_sensor_07 = pandas.DataFrame(data_filtered_sensor_07)
    df_sensor_47 = pandas.DataFrame(data_filtered_sensor_47)

    #Filtramos por los valores mayores a 20 y menores a 30
    df_filtered_sensor_07 = df_sensor_07[(df_sensor_07["sensor_07"] > 20) & (df_sensor_07["sensor_07"] < 30)]
    df_filtered_sensor_47 = df_sensor_47[(df_sensor_47["sensor_47"] > 20) & (df_sensor_47["sensor_47"] < 30)]

    #Cambiar nombre de columna sensor_07 y sensor_47
    df_filtered_sensor_07 = df_filtered_sensor_07.rename(columns={"sensor_07": "medición"})
    df_filtered_sensor_47 = df_filtered_sensor_47.rename(columns={"sensor_47": "medición"})

    #Unimos los dataframes
    df = pandas.concat([df_filtered_sensor_07, df_filtered_sensor_47])

    #Separamos los casos en filas individuales
    # exploded = df.explode(["sensor_07", "sensor_47"])

    #Convertimos los datos a formato json
    result_07 = df.to_json(orient="records", date_format="iso")
    result_47 = df.to_json(orient="records", date_format="iso")

    return {"sensor_07": json.loads(result_07), "sensor_47": json.loads(result_47)}

@app.post("/parser_data")
def parser_data(data: dict):
    """
    Función que recibe los datos en formato json y los convierte en un dataframe
    con las columnas:
    fecha: fecha de la medición en formato YYYY-MM-DD
    hora: hora de la medición en formato HH:MM:SS
    sensor: número del sensor
    medicion: valor de la medición
    estado: estado de la máquina
    Args:
        data ([json]): [datos en formato json]
    Returns:
        [dataframe]: [datos en formato dataframe]
    """
    try:
        #Convertimos los datos a formato dataframe
        df_07 = pandas.DataFrame(data['sensor_07'])
        df_47 = pandas.DataFrame(data['sensor_47'])

        #Agregamos la columna "sensor" con el número del sensor
        df_07["sensor"] = '07'
        df_47["sensor"] = '47'

        #Unimos los dataframes
        df = pandas.concat([df_07, df_47])

        #Convertimos la columna "timestamp" a formato fecha datetime
        df["timestamp"] = pandas.to_datetime(df["timestamp"])

        #Separamos la columna "timestamp" en fecha y hora
        df["fecha"] = df["timestamp"].dt.date
        df["hora"] = df["timestamp"].dt.time

        #Eliminamos la columna "timestamp"
        df = df.drop(columns=["timestamp"])

        #Cambiamos el nombre de la columna "machine_status" a "estado"
        df = df.rename(columns={"machine_status": "estado"})
        #Ordenamos las columnas
        df = df[["fecha", "hora", "sensor", "medición", "estado"]]
        print("*"*50)
        #Imprimimos los datos
        print(df)
        #Generamos un archivo csv con los datos
        df.to_csv("datos.csv", index=False)
        return {"mensaje": "Datos guardados satisfactoriamente en el archivo datos.csv",
                "data": json.loads(df.to_json(orient="records", date_format="iso"))}
    except Exception as e:
        print(e)
        return {"mensaje": "Hubo un error al guardar los datos en el archivo datos.csv"}
