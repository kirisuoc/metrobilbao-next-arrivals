#!/bin/bash

# Asignar el destino pasado como argumento
destination="$1"

# Establecer las diferentes URLs dependiendo del destino
echo "Selecione un destino:"
select destination in "San Ignacio - Urduliz" "Urduliz - San Ignacio" "San Ignazio - Barakaldo" "Barakaldo - San Ignacio"; do
	case "$destination" in
	"San Ignacio - Urduliz")
		url="https://api.metrobilbao.eus/metro/real-time/SIN/URD"  # URL para San Ignacio - Urduliz
		break
		;;
	"Urduliz - San Ignacio")
		url="https://api.metrobilbao.eus/metro/real-time/URD/SIN"  # URL para Urduliz - San Ignacio
		break
		;;
	"San Ignazio - Barakaldo")
		url="https://api.metrobilbao.eus/metro/real-time/SIN/BAR"  # URL para San Ignazio - Barakaldo
		break
		;;
	"Barakaldo - San Ignacio")
		url="https://api.metrobilbao.eus/metro/real-time/BAR/SIN"  # URL para Barakaldo - San Ignacio
		break
		;;
	*)
		echo "Opción no válida. Por favor, elige un número entre 1 y 4."
		;;
	esac
done

json=$(curl -s "$url")

#! {"co2Metro":{"co2metro":"35","co2Car":"183.69","co2DistanceMetro":614.565,"co2DistanceCar":3665.16657,"diffRaw":3050.60157,"diff":"3.050,60","metroDistance":17.559,"googleDistance":19.953},"trains":[{"wagons":5,"estimated":1,"direction":"Plentzia","time":"2024-12-03T14:22:49","timeRounded":"14:23"}],"messages":[],"trip":{"fromStation":{"code":"SIN","name":"San Ignazio"},"toStation":{"code":"URD","name":"Urduliz"},"duration":29,"line":"L1","transfer":false},"exits":{"origin":[{"id":92,"name":"Ascensor Av. Lehendakari Agirre, 170 (salida Pza Levante)","elevator":true,"nocturnal":true,"latitude":"43.28137","longitude":"-2.96265","issues":[]},{"id":93,"name":"Asturias Av. Lehendakari Agirre, 179, esq C\/Asturias","elevator":false,"nocturnal":true,"latitude":"43.28147","longitude":"-2.96300","issues":[]},{"id":94,"name":"Benita Asas Av. Lehendakari Agirre, 167, esq C\/Benita Asas","elevator":false,"nocturnal":false,"latitude":"43.27993","longitude":"-2.96214","issues":[]},{"id":95,"name":"Lekeitio Av. Lehendakari Agirre, 162, esq C\/Lekeitio","elevator":false,"nocturnal":false,"latitude":"43.28002","longitude":"-2.96187","issues":[]},{"id":96,"name":"Levante Pza. Levante, 2","elevator":false,"nocturnal":false,"latitude":"43.28144","longitude":"-2.96246","issues":[]}],"destiny":[{"id":127,"name":"Urduliz C\/ Gobela, 2","elevator":true,"nocturnal":true,"latitude":"43.37865","longitude":"-2.95905","issues":[]}]}}

#! EN OTROS LENGUAJES O LIBRERIAS CUANDO RECIBES UN JSON PUEDES PARSEARLO COMO UN OBJETO EJM JSON.METRO.HORA

# Extraer el nombre de las estaciones de origen y destino
from_station_name=$(echo "$json" | jq -r '.trip.fromStation.name')
to_station_name=$(echo "$json" | jq -r '.trip.toStation.name')

echo "------------------------------------------------------"
printf "| %-12s | %-12s |\n" "From" "$from_station_name"
printf "| %-12s | %-12s |\n" "To" "$to_station_name"
echo "------------------------------------------------------"
printf "| %-12s | %-12s | %-12s |\n" "Direction" "Hour" "Estimated"
echo "------------------------------------------------------"

# Extraer los horarios por dirección
echo "$json" | jq -r '.trains[] | "\(.direction) \(.time) \(.estimated)"' | while read -r line; do
	direction=$(echo "$line" | awk '{print $1}')
	time=$(echo "$line" | awk '{print $2}')
	estimated=$(echo "$line" | awk '{print $3}')

    hour=$(echo "$time" | awk -F'T' '{print $2}' | awk -F':' '{print $1 ":" $2}')

    printf "| %-12s | %-12s | %-12s |\n" "$direction" "$hour" "$estimated"
done

# Mostrar el final de la tabla
echo "-----------------------------"
