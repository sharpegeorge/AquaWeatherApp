import numpy as np
import utils

decimal_places = 3


def daily_average(data, monitoring_station, pollutant):
    """Calculates the average for every day over the year 2021 for a given pollutant and station

    Parameters:
    data (dict): Contains all the relevant data for 2021
    monitoring_station (str): Used to select the right section of data
    pollutant (str): Used to select the right section of data

    Returns:
    rounded_daily_averages (list): Contains all the calculated values"""

    daily_averages = []

    df = data[monitoring_station]

    # If program were to be modified for different years,
    # support for leap years would need to be added
    for day in range(365):

        day_measurements = []
        for hour in range(24):

            df_table_index = (day * 24) + hour
            hour_measurement = read_df_entry(df, df_table_index, pollutant)

            if hour_measurement == "No data":
                continue
            day_measurements.append(hour_measurement)

        day_measurements = utils.convert_list_type(day_measurements, "float")

        if utils.is_empty(day_measurements):
            daily_mean = -1
        else:
            daily_mean = utils.meannvalue(day_measurements)

        daily_averages.append(daily_mean)

    rounded_daily_averages = utils.round_list(daily_averages, decimal_places)
    # -1 indicates there was no data available
    rounded_daily_averages = utils.replace_list_value(rounded_daily_averages, -1, "No data")
    return rounded_daily_averages


def daily_median(data, monitoring_station, pollutant):
    """Calculates the median for every day over the year 2021 for a given pollutant and station

    Parameters:
    data (dict): Contains all the relevant data for 2021
    monitoring_station (str): Used to select the right section of data
    pollutant (str): Used to select the right section of data

    Returns:
    rounded_daily_medians (list): Contains all the calculated values"""

    daily_medians = []
    df = data[monitoring_station]

    # If program were to be modified for different years,
    # support for leap years would need to be added
    for day in range(365):

        hourly_measurements = []
        for hour in range(24):

            # Appending the hourly measurements to hourly_measurements
            df_table_index = (day * 24) + hour
            hour_measurement = read_df_entry(df, df_table_index, pollutant)

            if hour_measurement == "No data":
                continue
            hourly_measurements.append(hour_measurement)

        hourly_measurements = utils.convert_list_type(hourly_measurements, "float")

        if utils.is_empty(hourly_measurements):
            daily_median = -1
        else:
            # Converting to numpy array
            hourly_measurements = np.array(hourly_measurements)
            daily_median = np.median(hourly_measurements)

        daily_medians.append(daily_median)

    rounded_daily_medians = utils.round_list(daily_medians, decimal_places)
    # -1 indicates there was no data available
    rounded_daily_medians = utils.replace_list_value(rounded_daily_medians, -1, "No data")
    return rounded_daily_medians


def hourly_average(data, monitoring_station, pollutant):
    """Calculates the average for every hour of the day over the year 2021 for a given pollutant and station

    Parameters:
    data (dict): Contains all the relevant data for 2021
    monitoring_station (str): Used to select the right section of data
    pollutant (str): Used to select the right section of data

    Returns:
    rounded_hourly_averages (list): Contains all the calculated values"""

    hourly_averages = []
    df = data[monitoring_station]

    for hour in range(24):

        hour_measurements = []
        for day in range(365):
            df_table_index = (day * 24) + hour

            day_measurement_for_hour = read_df_entry(df, df_table_index, pollutant)

            if day_measurement_for_hour == "No data":
                continue
            hour_measurements.append(day_measurement_for_hour)

        hour_measurements = utils.convert_list_type(hour_measurements, "float")

        if utils.is_empty(hour_measurements):
            hourly_mean = -1
        else:
            hourly_mean = utils.meannvalue(hour_measurements)

        hourly_averages.append(hourly_mean)

    rounded_hourly_averages = utils.round_list(hourly_averages, decimal_places)
    # -1 indicates there was no data available
    rounded_hourly_averages = utils.replace_list_value(rounded_hourly_averages, -1, "No data")

    return rounded_hourly_averages


def monthly_average(data, monitoring_station, pollutant):
    """Calculates the average for every month over the year 2021 for a given pollutant and station

    Parameters:
    data (dict): Contains all the relevant data for 2021
    monitoring_station (str): Used to select the right section of data
    pollutant (str): Used to select the right section of data

    Returns:
    rounded_monthly_averages (list): Contains all the calculated values"""

    # If program were to be modified for different years,
    # support for leap years would need to be added
    days_in_months = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
    monthly_averages = []
    df = data[monitoring_station]

    df_table_index = 0
    for month in range(12):

        # Iterates through
        month_measurements = []
        for days in range(days_in_months[month]):
            for hours in range(24):

                hour_measurement = read_df_entry(df, df_table_index, pollutant)
                df_table_index += 1

                if hour_measurement == "No data":
                    continue
                month_measurements.append(hour_measurement)

        month_measurements = utils.convert_list_type(month_measurements, "float")

        if utils.is_empty(month_measurements):
            month_average = -1
        else:
            month_average = utils.meannvalue(month_measurements)

        monthly_averages.append(month_average)

    rounded_monthly_averages = utils.round_list(monthly_averages, decimal_places)
    # -1 indicates there was no data available
    rounded_monthly_averages = utils.replace_list_value(rounded_monthly_averages, -1, "No data")

    return rounded_monthly_averages


def peak_hour_date(data, date, monitoring_station, pollutant):
    """Calculates the greatest value and the hour it was recorded for a given date (in 2021), pollutant and station

    Parameters:
    data (dict): Contains all the relevant data for 2021
    date (str): Used to select the right section of data
    monitoring_station (str): Used to select the right section of data
    pollutant (str): Used to select the right section of data

    Returns:
    output (tuple): Contains the peak hour itself and the value"""

    df = data[monitoring_station]
    hourly_measurements = []

    # Finding the first entry containing the passed date
    df_index = find_df_index(df, date, "date")

    # Appending all data entries for the given day
    for df_index, hour in enumerate(range(24), df_index):
        hour_measurement = read_df_entry(df, df_index, pollutant)

        if hour_measurement == "No data":
            continue
        hourly_measurements.append(hour_measurement)

    hourly_measurements = utils.convert_list_type(hourly_measurements, "float")

    # Accounting for no data available
    if utils.is_empty(hourly_measurements):
        return -1

    # Finding the largest value and its index
    peak_hour_index = utils.maxvalue(hourly_measurements)
    peak_hour_value = hourly_measurements[peak_hour_index]

    peak_hour = peak_hour_index + 1  # +1 to get actual hour from (zero-based) index
    output = (f"{peak_hour}:00", peak_hour_value)
    return output


def count_missing_data(data, monitoring_station, pollutant):
    """Calculates the number of missing data entries over the year 2021 for a given pollutant and station

    Parameters:
    data (dict): Contains all the relevant data for 2021
    monitoring_station (str): Used to select the right section of data
    pollutant (str): Used to select the right section of data

    Returns:
    count (int): Contains the number of missing data entries"""

    df = data[monitoring_station]
    count = 0

    # Iterates through whole dataframe for the column
    for index in range(24 * 365):

        # Check if the current entry data is "No data"
        entry_data = read_df_entry(df, index, pollutant)
        if entry_data == "No data":
            count += 1

    return count


def fill_missing_data(data, new_value, monitoring_station, pollutant):
    """replacing every instance of missing data in the CSV with the value given, for a given pollutant and station

    Parameters:
    data (dict): Contains all the relevant data for 2021
    new_value (int): Used to replace all instances of empty data entries
    monitoring_station (str): Used to select the right section of data
    pollutant (str): Used to select the right section of data

    Returns:
    data (dict): Contains the relevant data to be analysed"""

    df = data[monitoring_station]

    # If condition is met for a cell, the value is changed to new_value
    condition = (df == "No data") & (df.columns == pollutant)
    df = df.mask(condition, new_value)

    data[monitoring_station] = df

    return data


# My functions

def find_df_index(df, term, column):
    """Finds the index of a given term in a pandas dataframe

    Parameters:
    df (pandas dataframe): The dataframe being searched
    term (str): The term being searched for
    column (str): The column being searched

    Returns:
    index: Returns the index of the search term
    -1: Returns -1 if the term cannot be found in the dataframe"""

    for index, entry_data in enumerate(df[column]):

        if entry_data == term:
            return index

    return -1


def read_df_entry(df, df_table_index, pollutant):
    """Reads a dataframe entry for a given index and pollutant (column)

    Parameters:
    df (pandas dataframe): The dataframe being searched
    df_table_index (int): The index of entry being read
    pollutant (str): The column of the entry being read

    Returns:
    df_entry (str): Contains the dataframe entry being searched for"""

    df_entry = df.loc[df_table_index, pollutant]
    return df_entry
