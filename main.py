from os import system, name
from matplotlib import pyplot as mat_plot
import pandas as pd
import datetime
import reporting
import intelligence
import monitoring
import sys

# The different screens of the UI

main_menu_screen = """\
 ────────────────────────────
  Enter a following key:

  • R - Access the PR module
  • I - Access the MI module
  • M - Access the RM module
  
  • A - Print the About text
  • Q - Quit the application
 ────────────────────────────
"""

reporting_menu_screen = """\
 ────────────────────────────────────────────────────────────
  Enter a following key:

  Pollution Analysis for a given pollutant and station
  • A - Get the daily average ratings
  • B - Get the daily median ratings
  • C - Get the hourly average ratings
  • D - Get the monthly average ratings
  • E - Get the hour with the greatest rating for a given day

  Handling missing data for a given pollutant and station
  • F - Get the number of missing data entries
  • G - Fill missing data entries with a value

  • M - Go back to Main Menu
  • Q - Quit the application
 ────────────────────────────────────────────────────────────
"""

intelligence_menu_screen = """\
 ────────────────────────────────────────────────────────────
  Enter a following key:

  • A - Detect red pixels from image
  • B - Detect cyan pixels from image
  • C - Detect connected components
  • D - Sort connected components

  • M - Go back to Main Menu
  • Q - Quit the application
 ────────────────────────────────────────────────────────────
"""

monitoring_menu_screen = """\
 ────────────────────────────
  Enter a following key:

  • A - Generate a graph given: pollutant, station, end and start date
  • B - Check for warnings on pollutant levels
  • C - Get pollutant descriptions
  • D - Export data given: pollutant, station, end and start date

  • M - Go back to Main Menu
  • Q - Quit the application
 ────────────────────────────
"""

station_menu_screen = """\
 ────────────────────────────
 Select a monitoring station

 • A - London Harlington
 • B - London Marylebone Road
 • C - London N Kensington

 • R - Return to sub-menu
 • Q - Quit the application
 ────────────────────────────
"""

pollutant_menu_screen = """\
 ────────────────────────────
 Select a pollutant

 • A - no
 • B - pm10
 • C - pm25

 • R - Return to sub-menu
 • Q - Quit the application
 ────────────────────────────
"""

# Reading the pollution data csv files
df_harlington = pd.read_csv('data/Pollution-London Harlington.csv')
df_marylebone = pd.read_csv('data/Pollution-London Marylebone Road.csv')
df_kensington = pd.read_csv('data/Pollution-London N Kensington.csv')

pollutant_data = {
    "Harlington": df_harlington,
    "Marylebone Road": df_marylebone,
    "N Kensington": df_kensington
}



# add doc strings
# go over commenting


def main_menu():
    """Loads the main menu, only calling load_menu"""

    load_menu("main menu")


def reporting_menu():
    """Loads the reporting menu, only calling load_menu"""

    load_menu("reporting menu")


def intelligence_menu():
    """Loads the intelligence menu, only calling load_menu"""

    load_menu("intelligence menu")


def monitoring_menu():
    """Loads the monitoring menu, only calling load_menu"""

    load_menu("monitoring menu")


def about():
    """Displays project information"""

    clear_screen()
    print("\n Module Code: ECM1400\n Candidate Number: 245780")

    input("\n Press enter to go back to Main Menu\n ")
    main_menu()


def quit():
    """Quits application"""

    sys.exit()


# My functions

# Reporting functions

def get_daily_average():
    """Prints the average for every day over the year 2021 for a given pollutant and station

    Reads data from CSV files stored at dataframes in the 'pollutant_data' dict"""

    monitoring_station = get_monitoring_station_input(return_menu="R")
    pollutant = get_pollutant_input(return_menu="R")
    clear_screen()

    daily_averages = reporting.daily_average(pollutant_data, monitoring_station, pollutant)

    print(f"\n The daily average units for '{pollutant}' at {monitoring_station}:\n")
    for day, element in enumerate(daily_averages, start=1):
        print(f" Day {day:3} : {element}")

    input("\n Press enter to go back to Pollutant Reporting Menu\n ")
    reporting_menu()


def get_daily_median():
    """Prints the median for every day over the year 2021 for a given pollutant and station

    Reads data from CSV files stored at dataframes in the 'pollutant_data' dict"""

    monitoring_station = get_monitoring_station_input(return_menu="R")
    pollutant = get_pollutant_input(return_menu="R")
    clear_screen()

    daily_medians = reporting.daily_median(pollutant_data, monitoring_station, pollutant)

    print(f"\n The daily median units for '{pollutant}' at {monitoring_station}:\n")
    for day, element in enumerate(daily_medians, start=1):
        print(f" Day {day:3} : {element}")

    input("\n Press enter to go back to Pollutant Reporting Menu\n ")
    reporting_menu()


def get_hourly_average():
    """Prints the average for every hour of the day over the year 2021 for a given pollutant and station

    Reads data from CSV files stored at dataframes in the 'pollutant_data' dict"""

    monitoring_station = get_monitoring_station_input(return_menu="R")
    pollutant = get_pollutant_input(return_menu="R")
    clear_screen()

    hourly_averages = reporting.hourly_average(pollutant_data, monitoring_station, pollutant)

    print(f"\n The hourly average units for '{pollutant}' at {monitoring_station}:\n")
    for hour, element in enumerate(hourly_averages, start=1):
        print(f" Hour {hour:3}:00 - {element}")

    input("\n Press enter to go back to Pollutant Reporting Menu\n ")
    reporting_menu()


def get_monthly_average():
    """Prints the average for every month over the year 2021 for a given pollutant and station

    Reads data from CSV files stored at dataframes in the 'pollutant_data' dict"""

    monitoring_station = get_monitoring_station_input(return_menu="R")
    pollutant = get_pollutant_input(return_menu="R")
    clear_screen()

    monthly_averages = reporting.monthly_average(pollutant_data, monitoring_station, pollutant)

    print(f"\n The monthly average units for '{pollutant}' at {monitoring_station}:\n")
    for month, element in enumerate(monthly_averages, start=1):
        print(f" Month {month:3} : {element}")

    input("\n Press enter to go back to Pollutant Reporting Menu\n ")
    reporting_menu()


def get_peak_hour_data():
    """Prints the greatest value and the hour it was recorded for a given date (in 2021), pollutant and station

    Reads data from CSV files stored at dataframes in the 'pollutant_data' dict"""

    monitoring_station = get_monitoring_station_input(return_menu="R")
    pollutant = get_pollutant_input(return_menu="R")
    date = get_date_input(specific_year=True)
    clear_screen()

    peak_hour = reporting.peak_hour_date(pollutant_data, date, monitoring_station, pollutant)

    # If there is no data available, -1 will be returned
    if peak_hour == -1:
        print(" There is no data for this date. ")
    else:
        print(f"\n On {date} at {peak_hour[0]} has a peak of {peak_hour[1]} "
              f"units of '{pollutant}' at {monitoring_station}. ")

    input("\n Press enter to go back to Pollutant Reporting Menu\n ")
    reporting_menu()


def count_missing_data():
    """Prints the number of missing data entries over the year 2021 for a given pollutant and station

    Reads data from CSV files stored at dataframes in the 'pollutant_data' dict"""

    monitoring_station = get_monitoring_station_input(return_menu="R")
    pollutant = get_pollutant_input(return_menu="R")
    clear_screen()

    number_of_missing_data = reporting.count_missing_data(pollutant_data, monitoring_station, pollutant)
    print(f"\n The number of missing data entries for "
          f"'{pollutant}' at {monitoring_station} is {number_of_missing_data}. ")

    input("\n Press enter to go back to Pollutant Reporting Menu\n ")
    reporting_menu()


def fill_missing_data():
    """Prints the data after replacing every instance of missing data in the CSV with the value given,
    for a given pollutant and station

    Reads data from CSV files stored at dataframes in the 'pollutant_data' dict"""

    monitoring_station = get_monitoring_station_input(return_menu="R")
    pollutant = get_pollutant_input(return_menu="R")
    clear_screen()

    while True:
        new_value = input("\n Enter the value you want to fill empty entries with, e.g. 10\n ")
        clear_screen()

        try:
            new_value = float(new_value)
        except ValueError:
            continue

        break

    new_pollutant_data = reporting.fill_missing_data(pollutant_data, new_value, monitoring_station, pollutant)

    print(f"\n The updated table at {monitoring_station}:\n")
    print(new_pollutant_data[monitoring_station].to_string())

    input("\n Press enter to go back to Pollutant Reporting Menu\n ")
    reporting_menu()


# Intelligence functions

def find_red_pixels():
    """Identifies every red pixel in a given .png file and presents the respective binary colour map to the user

    Results are also written to map_red_pixels.jpg in the data folder"""

    clear_screen()
    file_name_input = input("\n Enter the filename of the png map you want to analyse. Do not include the '.png'\n ")
    file_name = 'data/' + file_name_input + '.png'
    clear_screen()

    try:
        red_map = intelligence.find_red_pixels(file_name)
        print("\n Task completed, output file 'map-red-pixels' saved in data folder.")
        mat_plot.imshow(red_map, cmap='gray')
        mat_plot.show()

    except FileNotFoundError:
        print("\n Task failed, filename incorrect.")

    input("\n Press enter to go back to Mobility Intelligence Menu\n ")
    intelligence_menu()


def find_cyan_pixels():
    """Identifies every cyan pixel in a given .png file and presents the respective binary colour map to the user

    Results are also written to map_cyan_pixels.jpg in the data folder"""

    clear_screen()
    file_name_input = input("\n Enter the filename of the png map you want to analyse. Do not include the '.png'\n ")
    file_name = 'data/' + file_name_input + '.png'
    clear_screen()

    try:
        cyan_map = intelligence.find_cyan_pixels(file_name)
        print("\n Task completed, output file 'map-cyan-pixels' saved in data folder.")
        mat_plot.imshow(cyan_map, cmap='gray')
        mat_plot.show()

    except FileNotFoundError:
        print("\n Task failed, filename incorrect.")

    input("\n Press enter to go back to Mobility Intelligence Menu\n ")
    intelligence_menu()


def detect_connected_components():
    """Identifies every connected component in a 2D array passed from
    'find_red_pixels' or 'find_cyan_pixels and presents a list of them to the user

    Results are also written to 'cc-output-2a' in the data folder"""
    clear_screen()
    file_name_input = input("\n Enter the filename of the png map you want to analyse. Do not include the '.png'\n ")
    file_name = 'data/' + file_name_input + '.png'
    clear_screen()

    while True:
        colour = input("\n Would you like to analyse red or cyan pixels?\n ").upper()
        clear_screen()
        if colour == "RED" or colour == "CYAN":
            break

    try:
        if colour == "RED":
            intelligence.detect_connected_components(intelligence.find_red_pixels(file_name))
        elif colour == "CYAN":
            intelligence.detect_connected_components(intelligence.find_cyan_pixels(file_name))

        print("\n Task completed, output file 'cc-output-2a' saved in data folder.")

    except FileNotFoundError:
        print("\n Task failed, filename incorrect.")

    input("\n Press enter to go back to Mobility Intelligence Menu\n ")
    intelligence_menu()


def detect_connected_components_sorted():
    """Identifies every connected component in a 2D array passed from
    'find_red_pixels' or 'find_cyan_pixels and presents a list of them, sorted descending by size to the user

    Results are also written to 'cc-output-2a' in the data folder"""

    clear_screen()
    file_name_input = input("\n Enter the filename of the png map you want to analyse. Do not include the '.png'\n ")
    file_name = 'data/' + file_name_input + '.png'
    clear_screen()

    while True:
        colour = input("\n Would you like to analyse red or cyan pixels?\n ").upper()
        clear_screen()
        if colour == "RED" or colour == "CYAN":
            break

    try:
        if colour == "RED":
            intelligence.detect_connected_components_sorted(intelligence.detect_connected_components
                                                        (intelligence.find_red_pixels(file_name)))
        elif colour == "CYAN":
            intelligence.detect_connected_components_sorted(intelligence.detect_connected_components(intelligence.find_cyan_pixels(file_name)))

        print("\n Task completed, output file 'cc-output-2b' saved in data folder.")

    except FileNotFoundError:
        print("\n Task failed, filename incorrect.")

    input("\n Press enter to go back to Mobility Intelligence Menu\n ")
    intelligence_menu()


# Monitoring functions

def pollutant_graph():
    """Presents a graph showing the value of a given pollutant at a given station on a given date"""

    monitoring_station = get_monitoring_station_input(return_menu="M")
    pollutant = get_pollutant_input(return_menu="M")
    date = get_date_input(allow_today=True)
    clear_screen()

    graph, complete = monitoring.pollutant_graph(monitoring_station, pollutant, date)
    print(graph) if complete else print(" No data for given date. ")

    input("\n Press enter to go back to Real-time Monitoring Menu\n ")
    monitoring_menu()


def pollutants_warning():
    """Checks for pollutants at stations which exceed a set value and prints an appropriate report to the user"""

    clear_screen()
    warnings_report = monitoring.pollutants_warning()
    print(warnings_report)

    input("\n Press enter to go back to Real-time Monitoring Menu\n ")
    monitoring_menu()


def pollutant_description():
    """Prints the description (which is given by the LondonAir API) of a given pollutant"""

    pollutant = get_pollutant_input(return_menu="M")
    clear_screen()

    description = monitoring.pollutant_description(pollutant)
    print(description)

    input("\n Press enter to go back to Real-time Monitoring Menu\n ")
    monitoring_menu()


def export_data():
    """Writes data (which is given by the LondonAir API) to a csv file about a given pollutant, station,
     between two given dates"""

    monitoring_station = get_monitoring_station_input(return_menu="M")
    pollutant = get_pollutant_input(return_menu="M")
    start_date = get_date_input(start=True)
    end_date = get_date_input(end=True)
    clear_screen()

    monitoring.export_data(monitoring_station, pollutant, start_date, end_date)
    print("\n Export complete.")

    input("\n Press enter to go back to Real-time Monitoring Menu\n ")
    monitoring_menu()


# Input functions

def get_monitoring_station_input(return_menu="R"):
    """Gets the user to input which station they want to analyse, includes data validation where applicable

    Parameters:
    return_menu (string): First letter of sub-menu to return to if selected, default is "R" for reporting menu"""

    while True:
        clear_screen()
        print(station_menu_screen)
        user_input = input(" ").upper()

        if user_input == "A":
            return "Harlington"
        elif user_input == "B":
            return "Marylebone Road"
        elif user_input == "C":
            return "N Kensington"
        elif user_input == "R":
            main_menu_dict[return_menu]()
        elif user_input == "Q":
            quit()


def get_pollutant_input(return_menu="R"):
    """Gets the user to input which pollutant they want to analyse, includes data validation where applicable

    Parameters:
    return_menu (string): First letter of sub-menu to return to if selected, default is "R" for reporting menu"""

    while True:
        clear_screen()
        print(pollutant_menu_screen)
        user_input = input(" ").upper()

        if user_input == "A":
            return "no"
        elif user_input == "B":
            return "pm10"
        elif user_input == "C":
            return "pm25"
        elif user_input == "R":
            main_menu_dict[return_menu]()
        elif user_input == "Q":
            quit()


def get_date_input(start=False, end=False, specific_year=False, allow_today=False):
    """Gets the user to input which date they want to analyse, includes data validation where applicable

    Parameters:
    start (bool): Changes the message to ask for the start date, default is False
    end (bool): Changes the message to ask for the end date, default is False
    specific_year (bool): Determines if the date must be in the year 2021, default is False
    allow_today (bool): Allows the user to input 'today' instead of a date, default is False
    """

    date_format = "%Y-%m-%d"

    # Determines the correct message dependent on parameters
    message = "\n Enter the date you want to analyse, e.g. 2021-03-27\n "
    if start:
        message = "\n Enter the start date you want to analyse, e.g. 2021-03-27\n "
    elif end:
        message = "\n Enter the end date you want to analyse, e.g. 2021-03-28\n "
    elif allow_today:
        message = "\n Enter the date you want to analyse, e.g. 2021-03-27 or enter 'today'\n "

    while True:
        clear_screen()
        date_input = input(message)

        # Checks if message is 'today' when its required
        if allow_today and date_input.upper() == 'TODAY':
            date_input = datetime.date.today()
            date_input = date_input.strftime('%Y-%m-%d')

        try:
            date_input = (datetime.datetime.strptime(date_input, date_format))
            # Checks if year is 2021 when its required
            if specific_year and date_input.year != 2021:
                continue

            break
        except ValueError:
            print("b")
            continue

    year = date_input.year
    month = date_input.month
    day = date_input.day

    # Formatting output
    output = f"{year}-{month:02d}-{day:02d}"
    return output


# Menu functions

def load_menu(menu_name):
    """Loads the menu screen and compares the input with the corresponding input dictionary

    Parameters:
    menu_name (str): Used to determine which screen and input dictionary to use"""

    menu_screen = screens_dict[menu_name]
    menu_dict = menus_dict[menu_name]

    clear_screen()
    print(menu_screen)
    menu_input(menu_screen, menu_dict)


def menu_input(menu_screen, menu_dict):
    """Takes input and validates it against the passed menu input

    Repeats until user enters a valid input

    Parameters:
    menu_screen (string): Used to print the screen again to the user
    menu_dict (dict): Used to validate the input with the correct menu"""

    while True:
        key_input = input(" ").upper()
        if key_input in menu_dict:
            break
        clear_screen()
        print(menu_screen)

    menu_dict[key_input]()


def clear_screen():
    """Clears the screen with a special character, doesn't work with many IDEs"""

    # For windows
    if name == 'nt':
        _ = system('cls')

    # For mac and linux
    else:
        _ = system('clear')


# Input dictionaries which determine which function to call for a given input

main_menu_dict = {
    "R": reporting_menu,
    "I": intelligence_menu,
    "M": monitoring_menu,
    "A": about,
    "Q": quit
}

reporting_menu_dict = {
    "A": get_daily_average,
    "B": get_daily_median,
    "C": get_hourly_average,
    "D": get_monthly_average,
    "E": get_peak_hour_data,
    "F": count_missing_data,
    "G": fill_missing_data,
    "M": main_menu,
    "Q": quit
}

intelligence_menu_dict = {
    "A": find_red_pixels,
    "B": find_cyan_pixels,
    "C": detect_connected_components,
    "D": detect_connected_components_sorted,
    "M": main_menu,
    "Q": quit
}

monitoring_menu_dict = {
    "A": pollutant_graph,
    "B": pollutants_warning,
    "C": pollutant_description,
    "D": export_data,
    "M": main_menu,
    "Q": quit
}

# These 2 dictionaries are used to sync up the menu screens with the corresponding dictionary
screens_dict = {
    "main menu": main_menu_screen,
    "reporting menu": reporting_menu_screen,
    "intelligence menu": intelligence_menu_screen,
    "monitoring menu": monitoring_menu_screen
}

menus_dict = {
    "main menu": main_menu_dict,
    "reporting menu": reporting_menu_dict,
    "intelligence menu": intelligence_menu_dict,
    "monitoring menu": monitoring_menu_dict
}


if __name__ == '__main__':
    main_menu()
