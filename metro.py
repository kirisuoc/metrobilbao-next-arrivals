import json
import requests
import os
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, IntPrompt
from rich.panel import Panel
from rich.align import Align

console = Console()

# Función para limpiar la terminal
def clear_terminal():
    os.system("cls" if os.name == "nt" else "clear && printf '\033c'")

# Cargar estaciones del archivo JSON
def load_data():
    with open("stations.json", "r") as file:
        stations = json.load(file)["stations"]
    return stations

def set_data_default(origin, dest):
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
            origin, dest = set_station()
            set_data_default(origin, dest)
        return origin, dest
    
def reset_data_default():
    set_data_default(None, None)



def fetch_data(origin, destination):
    clear_terminal()
    url = f"https://api.metrobilbao.eus/metro/real-time/{origin['code']}/{destination['code']}"
    response = requests.get(url)
    data = response.json()

    # Extraer información de la respuesta
    from_station = data["trip"]["fromStation"]["name"]
    to_station = data["trip"]["toStation"]["name"]
    trains = data["trains"]

    # Mostrar datos en tabla
    console.print(Panel(f"[bold green]From:[/bold green] {from_station} [bold green]To:[/bold green] {to_station}"))
    table = Table(title="Train Schedule")
    table.add_column("Direction", justify="center", style="cyan")
    table.add_column("Time", justify="center", style="magenta")
    table.add_column("Estimated", justify="center", style="yellow")

    for train in trains:
        table.add_row(train["direction"], train["time"].split("T")[1][:5], str(train["estimated"]))

    console.print(table)
    console.input("\n[bold blue]Press ENTER to continue...[/bold blue]")
    show_menu()

def set_station():
    clear_terminal()
    stations = load_data()

    # Calcular el número máximo de estaciones por columna
    half = (len(stations) + 1) // 2

    # Dividir las estaciones en dos columnas
    column1 = stations[:half]
    column2 = stations[half:]

    # Mostrar lista de estaciones
    console.print(Panel("[bold green]Select origin station:[/bold green]"))

    # Imprimir las estaciones en dos columnas
    for i in range(half):
        col1 = f"[bold blue]{i + 1:<3}[/bold blue] {column1[i]['name']:<30}" if i < len(column1) else ""
        col2 = f"[bold blue]{i + 1 + half:<3}[/bold blue] {column2[i]['name']:<30}" if i < len(column2) else ""
        console.print(f"{col1:<45}{col2}")

    origin_index = IntPrompt.ask("[bold yellow]Enter the number of the origin station:[/bold yellow]") - 1
    origin = stations[origin_index]

    clear_terminal()
    console.print(f"[bold green]Selected origin station:[/bold green] {origin['name']}")

    console.print(Panel("[bold green]Select destination station:[/bold green]"))
    
    for i in range(half):
        col1 = ""
        col2 = ""

        # Columna 1: destacar origen si coincide
        if i < len(column1):
            if column1[i] == origin:
                col1 = f"[bold red]{i + 1:<3}[/bold red] [bold red]{column1[i]['name']:<30}[/bold red]"
            else:
                col1 = f"[bold blue]{i + 1:<3}[/bold blue] {column1[i]['name']:<30}"

        if i < len(column2):
            if column2[i] == origin:
                col2 = f"[bold red]{i + 1 + half:<3}[/bold red] [bold red]{column2[i]['name']:<30}[/bold red]"
            else:
                col2 = f"[bold blue]{i + 1 + half:<3}[/bold blue] {column2[i]['name']:<30}"

        console.print(f"{col1:<45}{col2}")

    destination_index = IntPrompt.ask("[bold yellow]Enter the number of the destination station:[/bold yellow]") - 1
    destination = stations[destination_index]

    console.print(f"[bold green]Selected destination station:[/bold green] {destination['name']}")
    if destination == origin:
        console.print("[bold red]\nError: Choose different origin and destination\n[/bold red]")
        console.input("\n[bold blue]Press ENTER to return...[/bold blue]")
        return set_station()
    return origin, destination


def settings():
    clear_terminal()
    with open("stations.json", "r") as file:
        data = json.load(file)
        start = data["default_start"]

    console.print(Panel("[bold green]Settings:[/bold green]"))
    console.print(Panel(f"[bold yellow]1 - Reset Default Trip.\n2 - Launch with Default Trip: [bold green]{start}[/bold green]\n3 - Exit.[/bold yellow]"))
    option = IntPrompt.ask("[bold cyan]Select an option:[/bold cyan]")

    if option == 1:
       reset_data_default()
       console.input("\n[bold blue]The default trip has been deleted.[/bold blue]")
       console.input("\n[bold blue]Press ENTER to return to the menu...[/bold blue]")
    elif option == 2:
        with open("stations.json", "r") as file:
            data = json.load(file)
            if data["default_start"] == True:
                data["default_start"] = False
            else:
                data["default_start"] = True
        with open("stations.json", "w") as file:
            json.dump(data, file, indent=4)
        settings()

    elif option == 3:
        show_menu()
    else:
        console.print("[bold red]\nError: Invalid option!!!\n[/bold red]")
        console.input("\n[bold blue]Press ENTER to return to the menu...[/bold blue]")
        show_menu()

def travel_now():
    origin, destination = set_station()
    fetch_data(origin, destination)

def default_trip():
    origin, dest = load_data_default()
    fetch_data(origin, dest)

def show_logo():
    clear_terminal()
    logo = """
 __  __      _                 ____  _ _ _
|  \/  | ___| |_ _ __ ___     | __ )(_) | |__   __ _  ___
| |\/| |/ _ \ __| '__/ _ \ ___|  _ \| | | '_ \ / _` |/ _ \
| |  | |  __/ |_| | | (_) |___| |_) | | | |_) | (_| | (_) |
|_|  |_|\___|\__|_|  \___/    |____/|_|_|_.__/ \__,_|\___/
    """
    console.print(Align.center(Panel(logo, title="Metro Bilbao", style="bold magenta")))

def show_menu():
    clear_terminal()
    show_logo()
    console.print(Panel("[bold yellow]1 - Travel Now.\n2 - Default Trip.\n3 - Settings.\n4 - Exit.[/bold yellow]"))
    option = IntPrompt.ask("[bold cyan]Select an option:[/bold cyan]")

    if option == 1:
        travel_now()
    elif option == 2:
        default_trip()
    elif option == 3:
        settings()
    elif option == 4:
        console.print("[bold green]Goodbye![/bold green]")
        exit()
    else:
        console.print("[bold red]\nError: Invalid option!!!\n[/bold red]")
        console.input("\n[bold blue]Press ENTER to return to the menu...[/bold blue]")
    main()

def main():
    with open("stations.json", "r") as file:
        data = json.load(file)
    
    if data["default_start"]:
        default_trip()
    else:
        show_menu()

if __name__ == "__main__":
    main()
