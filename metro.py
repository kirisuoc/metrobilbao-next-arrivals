import json
import requests
import sys
sys.path.append('./tabulate')

from tabulate import tabulate

# Cargar el archivo JSON con las estaciones
with open("stations.json", "r") as file:
    stations = json.load(file)["stations"]

# Mostrar la lista de estaciones
print("Selecciona la estación de origen:")
for i, station in enumerate(stations, start=1):
    print(f"{i}. {station['name']}")

# Leer la selección del usuario
origin_index = int(input("Introduce el número de la estación de origen: ")) - 1
origin = stations[origin_index]

print(f"Estación de origen seleccionada: {origin['name']}\n")

# Mostrar la lista de estaciones para el destino
print("Selecciona la estación de destino:")
for i, station in enumerate(stations, start=1):
    print(f"{i}. {station['name']}")

destination_index = int(input("Introduce el número de la estación de destino: ")) - 1
destination = stations[destination_index]

print(f"Estación de destino seleccionada: {destination['name']}\n")

# Construir la URL de consulta
url = f"https://api.metrobilbao.eus/metro/real-time/{origin['code']}/{destination['code']}"
response = requests.get(url)
data = response.json()

# Extraer información de la respuesta
from_station = data["trip"]["fromStation"]["name"]
to_station = data["trip"]["toStation"]["name"]
trains = data["trains"]

# Mostrar los datos en formato tabular
print(f"De: {from_station} A: {to_station}\n")
table = [[train["direction"], train["time"].split("T")[1][:5], train["estimated"]] for train in trains]
print(tabulate(table, headers=["Direction", "Time", "Estimated"], tablefmt="grid"))
