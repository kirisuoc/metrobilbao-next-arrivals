![1](https://github.com/user-attachments/assets/45c6c02e-88b9-4b8d-8c66-206488175237)

# Metro Bilbao CLI Schedule Application

This is a Command-Line Interface (CLI) application to check train schedules for the Metro Bilbao system. The application provides a user-friendly interface with interactive menus, allowing you to select origin and destination stations, view real-time train schedules, and configure default trips.

The interface is enhanced using the `rich` library for better visualization.

> [!WARNING]
> This application is **NOT OFFICIAL** and is developed for educational purposes only. 
> The developers are not responsible for any misuse of this application. 
> The API used belongs to Metro Bilbao.
> 

---

## Features
- **Real-Time Train Schedules**: Fetch real-time train data between selected stations.
- **Interactive Station Selection**: Choose origin and destination stations from a list.
- **Default Trips**: Save your preferred origin and destination for quick access.
- **Clear Interface**: Automatically clears the terminal between screens for a clean user experience.
- **Beautiful Visuals**: Styled text, tables, and menus for easy navigation.

---

## Prerequisites
Ensure you have the following installed:
- Python 3.8 or higher
- Internet connection (to fetch real-time train schedules)

Required Python libraries:
- `requests`
- `rich`

Install the required libraries with:
```bash
pip install requests rich
```

---

## How to Use
### Clone the Repository
```bash
git clone https://github.com/kirisuoc/metrobilbao-now/
cd metrobilbao-now
```

### Run the Application
Execute the application with:
```bash
python metro_bilbao_schedule.py
```

---

## Menu Options
When you run the application, you'll see a menu like this:

```
1 - Travel Now
2 - Default Trip
3 - Settings
4 - Exit
```

### Option Descriptions
1. **Travel Now**: 
   - Select an origin and destination station from the list.
   - View real-time train schedules between the selected stations.

2. **Default Trip**:
   - Fetch schedules for your saved origin and destination stations.
   - You can reset these stations in the settings.

3. **Settings**:
   - Update your default origin and destination stations.

4. **Exit**:
   - Close the application.

---

## Example Usage
### Travel Now
1. Select `1 - Travel Now`.
2. Choose your origin and destination stations from the interactive list.
3. View the real-time train schedule in a neatly formatted table.

### Default Trip
1. Set your default stations in the **Settings** menu.
2. Select `2 - Default Trip` for instant schedule access.

---

## Contribution
Feel free to fork this repository and submit pull requests for improvements or additional features.

---

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

## Author
Developed by [E10Y] [kirisuoc].

For any issues or suggestions, please open a GitHub issue.
