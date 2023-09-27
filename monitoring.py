import requests
import datetime
import os
import csv

codes_dict = {
    "Harlington": "LH0",
    "Marylebone Road": "MY1",
    "N Kensington": "KC1",
    "no": "NO",
    "pm10": "PM10",
    "pm25": "PM25"
}


def get_live_data_from_api(site_code='LH0',species_code='PM25',start_date=None,end_date=None):
    """Return data from the LondonAir API using its AirQuality API.

    Parameters:
    site_code (str): Site code to get data about, default is 'LH0'
    species_code (str): Code for pollutant to get data about, default is 'PM25'
    start_date (str): The start date for the data to retrieve, default is None
    end_date (str): The end date for the data to retrieve, default is None

    Returns:
    res.json() (dict): Contains the data being retrieved from the API"""

    start_date = datetime.date.today() if start_date is None else start_date
    end_date = start_date + datetime.timedelta(days=1) if end_date is None else end_date
    
    endpoint = "https://api.erg.ic.ac.uk/AirQuality/Data/SiteSpecies/SiteCode={site_code}/" \
               "SpeciesCode={species_code}/StartDate={start_date}/EndDate={end_date}/Json"
   
    url = endpoint.format(
        site_code = site_code,
        species_code = species_code,
        start_date = start_date,
        end_date = end_date
    )
    
    res = requests.get(url)
    return res.json()


def pollutant_graph(station, pollutant, date):
    """Returns a text-based graph for a given pollutant, station and date

    Parameters:
    station (str): Specifies what station to get data about from API
    pollutant (str): Specifies what pollutant to get data about from API
    date (str): Specifies what date to get data about from API

    Returns:
    graph (str): A text-based graph for the given pollutant, station and date"""

    # Formatting inputs
    station = convert_codes(station)
    pollutant = convert_codes(pollutant)

    start_date = convert_to_datetime(date)
    end_date = start_date + datetime.timedelta(days=1)

    # Retrieving Data
    raw_data = get_live_data_from_api(station, pollutant, start_date, end_date)
    data = extract_data(raw_data)

    # Generating and returning graph
    graph = generate_graph(data)
    return graph


def pollutants_warning():
    """Compares the values of the 3 pollutants for the 3 stations against set thresholds and returns a report

    Returns:
    report (str): A report of any pollutants with too high values at which station)"""

    warnings = []

    stations = ["Harlington", "Marylebone Road", "N Kensington"]
    for station in stations:
        station_code = codes_dict[station]

        # Retrieves the most recent data (that isn't empty) for each pollutant
        no_raw_data = get_live_data_from_api(station_code, "NO")
        no_value = float(get_most_recent_value(no_raw_data))

        pm10_raw_data = get_live_data_from_api(station_code, "PM10")
        pm10_value = float(get_most_recent_value(pm10_raw_data))

        pm25_raw_data = get_live_data_from_api(station_code, "PM25")
        pm25_value = float(get_most_recent_value(pm25_raw_data))

        # Checks values against benchmarks found from research
        # Assigns a warning level with 0 being the most critical

        if no_value > 30000:
            warnings.append((station, "NO", 0))
        elif no_value > 120000:
            warnings.append((station, "NO", 0))

        if pm10_value > 54:
            warnings.append((station, "PM10", 3))
        elif pm10_value > 154:
            warnings.append((station, "PM10", 2))
        elif pm10_value > 254:
            warnings.append((station, "PM10", 1))
        elif pm10_value > 354:
            warnings.append((station, "PM10", 0))

        if pm25_value > 12:
            warnings.append((station, "PM25", 3))
        elif pm25_value > 35.4:
            warnings.append((station, "PM25", 2))
        elif pm25_value > 55.4:
            warnings.append((station, "PM25", 1))
        elif pm25_value > 150.4:
            warnings.append((station, "PM25", 0))

    # Generates warning messages
    warnings_messages = ""
    for warning in warnings:
        station = warning[0]
        pollutant = warning[1]
        level = warning[2]

        if level == 0:
            warnings_messages += (f"\n -A critical risk of {pollutant} at {station} station. ")
        elif level == 1:
            warnings_messages += (f"\n -A serious risk of {pollutant} at {station} station. ")
        elif level == 2:
            warnings_messages += (f"\n -A risk to vulnerable people of {pollutant} at {station} station. ")
        elif level == 3:
            warnings_messages += (f"\n -A moderate risk of {pollutant} at {station} station. ")

    if not warnings:
        report = f"""
  Pollutants Level Report
 -------------------------
 
 The most recent data suggests:
 
 -No dangerous levels of NO, PM10, PM25 at any station.
"""
    else:
        report = f"""
  Pollutants Level Report
 -------------------------

 The most recent data suggests: {warnings_messages}"""

    return report


def pollutant_description(pollutant):
    """Gives a description of a given pollutant which is retrieved from the LondonAir API

    Parameters:
    pollutant (str): Specifies what pollutant to get a description of

    Returns:
    output (str): A formatted description of the pollutant"""

    if pollutant == "no":
        output = "\n There is no data available for 'NO'"
        return output

    # Getting data from API
    pollutant_code = pollutant.upper()
    endpoint = "http://api.erg.ic.ac.uk/AirQuality/Information/Species/SpeciesCode={species_code}/Json"

    url = endpoint.format(
        species_code = pollutant_code
    )

    res = requests.get(url)
    data = res.json()

    description = data['AirQualitySpecies']['Species']['@Description']
    output = f"""
 {pollutant.upper()} description:
 {description}"""

    return output


def export_data(station, pollutant, start_date, end_date):
    """Exports data from the LondonAir API to a CSV file for a given pollutant, station, start and end date

    Parameters:
    station (str): Specifies which station to get data of
    pollutant (str): Specifies which pollutant to get data of
    start_date (str): Specifies the start date to get data from
    end_date (str): Specifies the end date to get data from

    Returns:
    True: If it successfully exports.
    """

    # Formatting inputs
    station = convert_codes(station)
    pollutant = convert_codes(pollutant)

    start_date = convert_to_datetime(start_date)
    end_date = convert_to_datetime(end_date)

    # Retrieving data
    raw_data = get_live_data_from_api(station, pollutant, start_date, end_date)
    data = extract_data(raw_data)

    # Selecting file name
    counter = 0
    file_name = f"data/Output File {station} {pollutant}.csv"
    while file_exists(file_name):
        counter += 1
        file_name = f"data/Output File {station} {pollutant} ({counter}).csv"

    # Writing to file
    header = ["date", "time", f"{pollutant.lower()} (ug/m^3)"]

    with open(file_name, 'w', newline='') as f:
        writer = csv.writer(f)

        writer.writerow(header)

        date = start_date
        for index, element in enumerate(data):

            # Calculate hour and increment date accordingly
            hour = index % 24
            if hour == 1:
                date = date + datetime.timedelta(days=1)

            writer.writerow([date, f"{hour:02d}:00", element])

    return True


# My functions

def generate_graph(data):
    """Generates a text-based graph for the passed data
    
    Parameters:
    data (list): Contains pollutant data to be inputted a graph
    
    Returns:
    graph (str): A text-based graph 
    complete (bool): Indicates whether it was successful"""

    graph_data = [[" "] * 24 for _ in range(24)]
    additional_values = []
    complete = False

    # Iterating through data passed
    for hour, value in enumerate(data):

        # Checking for no data
        try:
            value = float(value)
            complete = True
        except ValueError:
            value = 0

        # Rounding data to multiples of 2.5 to fit the graph
        rounded_value = 2.5 * round(value / 2.5)

        # Making sure values fit in the graphs y axis
        if rounded_value <= 50:
            row = int(rounded_value // 2.5) - 1
            graph_data[row][hour] = '*'

        # If the value of the data is out of range of the graph
        else:
            additional_values.append((rounded_value, hour))

    # Sorting additional values in descending order
    additional_rows = "\n"
    additional_values.sort(key=lambda x: x[0], reverse=True)

    # Creating additional rows for values out of bounds
    for rounded_value, hour in additional_values:
        additional_rows += f"""\
  {rounded_value:4}+ {' ' * (hour - 1)} * {' ' * (22 - hour)}
      | {' ' * 22}
"""

    graph = additional_rows + f"""\
   50 +  {'  '.join(graph_data[19]):70}
      |  {'  '.join(graph_data[18]):70}
   45 +  {'  '.join(graph_data[17]):70}
      |  {'  '.join(graph_data[16]):70}
   40 +  {'  '.join(graph_data[15]):70}
      |  {'  '.join(graph_data[14]):70}
   35 +  {'  '.join(graph_data[13]):70}
      |  {'  '.join(graph_data[12]):70}
   30 +  {'  '.join(graph_data[11]):70}
      |  {'  '.join(graph_data[10]):70}
   25 +  {'  '.join(graph_data[9]):70}
      |  {'  '.join(graph_data[8]):70}
   20 +  {'  '.join(graph_data[7]):70}
      |  {'  '.join(graph_data[6]):70}
   15 +  {'  '.join(graph_data[5]):70}
      |  {'  '.join(graph_data[4]):70}
   10 +  {'  '.join(graph_data[3]):70}
      |  {'  '.join(graph_data[2]):70}
    5 +  {'  '.join(graph_data[1]):70}
      |  {'  '.join(graph_data[0]):70}
    0 +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
       00:00 02:00 04:00 06:00 08:00 10:00 12:00 14:00 16:00 18:00 20:00 22:00 
"""

    return graph, complete


def extract_data(raw_data):
    """Extracts data from a nested dictionary

    Parameters:
    raw_data (dict): A nested dictionary containing data to be extracted

    Returns:
    data (list): Contains the relevant data"""

    raw_data = raw_data["RawAQData"]
    data = []

    for element in raw_data["Data"]:
        data.append(element['@Value'])

    return data


def get_most_recent_value(raw_data):
    """Some values aren't ratified and are passed as empty from API, so finds most recent non-empty value

    Parameters:
    raw_data (dict):

    Returns:
    data[-1] (int): Returns the most recent non-empty value from the passed data
    0 (int): Returns 0 if the raw_data had no valuable data"""
    # Extracts and removes empty values
    data = [i for i in extract_data(raw_data) if i]

    # Either returns last entry or 0 if its empty
    return data[-1] if data else 0


def convert_codes(code):
    """Converts codes from main.py to be compatible with get_live_data_from_api

    Parameters:
    code (str): Code from main.py

    Returns:
    codes_dict[code] (str): A code that is compatible with get_live_data_from_api"""
    return codes_dict[code]


def convert_to_datetime(date):
    """Converts a string to a datetime object

    Parameters:
    date (str): Date being converted

    Returns:
    output (datetime.date): Date as a datetime object"""
    output = datetime.datetime.strptime(date, '%Y-%m-%d').date()
    return output


def file_exists(name):
    """Checks if a file exists with the given name

    Parameters:
    name (str): The name of the file being checked

    Returns:
    exists (bool): Determines whether the file already exists"""

    exists = os.path.exists(name)
    return exists

