import json
from fastapi import FastAPI
import pandas

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/get_data")
def read_csv():
    #Leemos el archivo csv
    data = pandas.read_csv('sensor.csv')

    #Convertimos la columna "timestamp" a formato fecha datetime
    data["timestamp"] = pandas.to_datetime(data["timestamp"])

    #Filtramos los datos por el mes de abril y año 2018
    data_filtered = data[(data["timestamp"].dt.month == 4) & (data["timestamp"].dt.year == 2018)]

    #Filtramos las mediciones de los sensores 07 y 47 con las columnas timestamp y machine_status
    data_filtered_sensor_07 = data_filtered[["timestamp", "machine_status", "sensor_07"]]
    data_filtered_sensor_47 = data_filtered[["timestamp", "machine_status", "sensor_47"]]
    # data_filtered = data_filtered[["timestamp", "machine_status", "sensor_07", "sensor_47"]]

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
    # df = pandas.concat([df_filtered_sensor_07, df_filtered_sensor_47])

    #Separamos los casos en filas individuales
    # exploded = df.explode(["sensor_07", "sensor_47"])

    #Convertimos los datos a formato json
    result_07 = df_filtered_sensor_07.to_json(orient="records", date_format="iso")
    result_47 = df_filtered_sensor_47.to_json(orient="records", date_format="iso")
    # result_07 = df_filtered_sensor_07[["timestamp", "machine_status", "medición"]].to_json(orient="records", date_format="iso")
    # result_47 = df_filtered_sensor_47[["timestamp", "machine_status", "medición"]].to_json(orient="records", date_format="iso")
    return {"sensor_07": json.loads(result_07), "sensor_47": json.loads(result_47)}