#!/bin/bash

# Cargar el archivo JSON con las estaciones
stations_file="stations.json"

# Determinar el número de columnas (por ejemplo, 3)
columns=3

# Mostrar la lista de estaciones
echo "Selecciona la estación de origen:"
jq -r '.stations[] | "\(.name)"' "$stations_file" | nl # | pr -t -${columns} <-- Separar lista en columnas

# Leer la selección del usuario para la estación de origen
read -p "Introduce el número de la estación de origen: " origin_index
origin_code=$(jq -r ".stations[$((origin_index - 1))].code" "$stations_file")
origin_name=$(jq -r ".stations[$((origin_index - 1))].name" "$stations_file")

# Verificar si la selección es válida
if [ -z "$origin_code" ]; then
	echo "		Selección inválida para la estación de origen."
	exit 1
fi

echo "Estación de origen seleccionada: $origin_name"
echo

# Mostrar la lista de estaciones para el destino
echo "Selecciona la estación de destino:"
jq -r '.stations[] | "\(.name)"' "$stations_file" | nl # | pr -t -${columns} <-- Separar lista en columnas

# Leer la selección del usuario para la estación de origen
read -p "Introduce el número de la estación de destino: " destination_index
destination_code=$(jq -r ".stations[$((destination_index - 1))].code" "$stations_file")
destination_name=$(jq -r ".stations[$((destination_index - 1))].name" "$stations_file")

# Verificar si la selección es válida
if [ -z "$destination_code" ]; then
	echo "Selección inválida para la estación de destino."
	exit 1
fi

echo "Estación de destino seleccionada: $destination_name"
echo

# Construir la URL de consulta
url="https://api.metrobilbao.eus/metro/real-time/${origin_code}/${destination_code}"
json=$(curl -s "$url")

#! {"co2Metro":{"co2metro":"35","co2Car":"183.69","co2DistanceMetro":614.565,"co2DistanceCar":3665.16657,"diffRaw":3050.60157,"diff":"3.050,60","metroDistance":17.559,"googleDistance":19.953},"trains":[{"wagons":5,"estimated":1,"direction":"Plentzia","time":"2024-12-03T14:22:49","timeRounded":"14:23"}],"messages":[],"trip":{"fromStation":{"code":"SIN","name":"San Ignazio"},"toStation":{"code":"URD","name":"Urduliz"},"duration":29,"line":"L1","transfer":false},"exits":{"origin":[{"id":92,"name":"Ascensor Av. Lehendakari Agirre, 170 (salida Pza Levante)","elevator":true,"nocturnal":true,"latitude":"43.28137","longitude":"-2.96265","issues":[]},{"id":93,"name":"Asturias Av. Lehendakari Agirre, 179, esq C\/Asturias","elevator":false,"nocturnal":true,"latitude":"43.28147","longitude":"-2.96300","issues":[]},{"id":94,"name":"Benita Asas Av. Lehendakari Agirre, 167, esq C\/Benita Asas","elevator":false,"nocturnal":false,"latitude":"43.27993","longitude":"-2.96214","issues":[]},{"id":95,"name":"Lekeitio Av. Lehendakari Agirre, 162, esq C\/Lekeitio","elevator":false,"nocturnal":false,"latitude":"43.28002","longitude":"-2.96187","issues":[]},{"id":96,"name":"Levante Pza. Levante, 2","elevator":false,"nocturnal":false,"latitude":"43.28144","longitude":"-2.96246","issues":[]}],"destiny":[{"id":127,"name":"Urduliz C\/ Gobela, 2","elevator":true,"nocturnal":true,"latitude":"43.37865","longitude":"-2.95905","issues":[]}]}}

# Extraer el nombre de las estaciones de origen y destino
from_station_name=$(echo "$json" | jq -r '.trip.fromStation.name')
to_station_name=$(echo "$json" | jq -r '.trip.toStation.name')

echo "----------------------------------------------"
printf "| %-12s | %-12s |\n" "From" "$from_station_name"
printf "| %-12s | %-12s |\n" "To" "$to_station_name"
echo "----------------------------------------------"
printf "| %-12s | %-12s | %-12s |\n" "Direction" "Time" "Estimated"
echo "----------------------------------------------"

# Extraer los horarios por dirección
echo "$json" | jq -r '.trains[] | "\(.direction) \(.time) \(.estimated)"' | while read -r line; do
	direction=$(echo "$line" | awk '{print $1}')
	time=$(echo "$line" | awk '{print $2}')
	estimated=$(echo "$line" | awk '{print $3}')

    hour=$(echo "$time" | awk -F'T' '{print $2}' | awk -F':' '{print $1 ":" $2}')

    printf "| %-12s | %-12s | %-12s |\n" "$direction" "$hour" "$estimated"
done

# Mostrar el final de la tabla
echo "----------------------------------------------"
