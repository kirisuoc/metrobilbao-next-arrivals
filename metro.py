import json
from colorama import Fore, Style
import sys
sys.path.append('./tabulate')

from tabulate import tabulate

# Cargar el archivo JSON con las estaciones
# E: Recuerda que en este caso al usar With si te sirve pero si hacer un open normal hacer close igual que en C

def load_data():
    with open("stations.json", "r") as file:
        stations = json.load(file)["stations"]
    return stations

def set_data_default(origin,dest):
    with open("stations.json", "r") as file:
        data = json.load(file)
    
        data["default_origin"] = origin
        data["default_dest"] = dest
    
    with open("stations.json", "w") as file:
        json.dump(data, file, indent=4)

def load_data_default():
    with open("stations.json", "r") as file:
        data = json.load(file)
        origin = data["default_origin"]
        dest = data["default_dest"]
        if not origin or not dest:
            origin,dest = set_station()
            set_data_default(origin,dest)
        return (origin, dest)


def fetch_data(origin,destination):
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
    input("\nPress ENTER to continue...")
    main()

def set_station():
    stations = load_data()
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
    return origin,destination


def travel_now():
    origin,destination = set_station()
    fetch_data(origin,destination)


def default_trip():
    origin,dest = load_data_default()
    fetch_data(origin, dest)
    

def show_logo():
    print(Style.BRIGHT + """
 __  __      _                 ____  _ _ _                 
|  \/  | ___| |_ _ __ ___     | __ )(_) | |__   __ _  ___  
| |\/| |/ _ \ __| '__/ _ \ ___|  _ \| | | '_ \ / _` |/ _ \ 
| |  | |  __/ |_| | | (_) |___| |_) | | | |_) | (_| | (_) |
|_|  |_|\___|\__|_|  \___/    |____/|_|_|_.__/ \__,_|\___/ 
    """ + Style.RESET_ALL)
    print("╔═══════════════════════════════════════════════════════╗")
    print("║             << Time Table Metro Bilbao >>             ║" )
    print("╚═══════════════════════════════════════════════════════╝")

def show_menu():
    print("1 - Travel now.")
    print("2 - Default trip.")
    print("3 - Settings.")
    print("4 - Exit.")
    option = input("Select an option: ")

    if option == "1":
        travel_now()
    elif option == "2":
        default_trip()
    elif option == "3":
        print("Haz c")
    else:
        print(Fore.RED + Style.BRIGHT + "\nError: No valid option!!!\n" + Style.RESET_ALL)
        show_menu()



#E: Es muy buena practica decirle donde arrancar
def main():
    show_logo()
    show_menu()

if __name__ == "__main__":
    main()