def sumvalues(values: [int]):
    """Returns the sum of all the values in the list

    Parameters:
    values (list): List of values to be summed

    Returns:
    total (int): The sum of the values"""

    if non_numericals_present(values):
        raise Exception("Non-numerical values are present in list")

    total = 0
    for element in values:
        total += element

    return total


def maxvalue(values: [int]):
    """Returns the index of the largest value out of a list of values using one pass of bubblesort

    Parameters:
    values (list): The list of values

    Returns:
    largest_element_index (int): The index of the largest value"""

    if non_numericals_present(values):
        raise Exception("Non-numerical values are present in list")

    largest_element = values[0]
    largest_element_index = 0

    # Using first pass of bubble sort
    for index, element in enumerate(values):

        if element > largest_element:
            largest_element = element
            largest_element_index = index

    return largest_element_index


def minvalue(values: [int]):
    """Returns the index of the smallest value out of a list of values using one pass of a bubblesort

    Parameters:
    values (list): The list of values

    Returns:
    smallest_element_index (int): The index of the smallest value"""

    if non_numericals_present(values):
        raise Exception("Non-numerical values are present in list")

    smallest_element = values[0]
    smallest_element_index = 0

    # Using first pass of bubble sort
    for index, element in enumerate(values):

        if element < smallest_element:
            smallest_element = element
            smallest_element_index = index

    return smallest_element_index


def meannvalue(values: [int]):
    """Calculates the mean value of a list

    Parameters:
    values (list[int]): The list of values

    Returns:
    average (float): The mean average value of the list"""

    if non_numericals_present(values):
        raise Exception("Non-numerical values are present in list")

    total = sumvalues(values)
    length = get_length(values)

    if length == 0:
        return -1

    average = total / length
    return average


def countvalue(values: [], x):
    """Counts the number of times x occurs in the list values

    Parameters:
    values (list): The list of values being searched
    x: The term being searched for. Can be an int, string or float."""

    count = 0
    for element in values:
        if element == x:
            count += 1

    return count


# My functions

def non_numericals_present(input_list: []):
    """Checks if non-nomerical values are present in the passed list

    Parameters:
    input_list (list): The list being searched

    Returns:
    True: If there are values which aren't type int or float, true is returned
    False: If there aren't any int or float values, false is returned"""

    for element in input_list:

        element_type = type(element)

        if element_type == int or element_type == float:
            continue
        else:
            return True

    return False


def convert_list_type(input_list: [], target_type: str):
    """Converts the type of every element in a list

    Parameters:
    input_list (list): The list being converted
    target_type (str): A string representing the type the list is being converted to"""

    if target_type == "int":
        input_list = [int(element) for element in input_list]

    elif target_type == "float":
        input_list = [float(element) for element in input_list]

    elif target_type == "str":
        input_list = [str(element) for element in input_list]

    else:
        raise Exception("Invalid target type passed")

    return input_list


def round_list(input_list: [], decimal_places: int):
    """Rounds every element in a list to a given number of decimal places

    Parameters:
    input_list (list): The list being rounded
    decimal_places (int): The number of decimal places each element will be rounded to

    Returns:
    rounded_list (list): The passed list after every element was rounded
    """
    rounded_list = [round(element, decimal_places) for element in input_list]
    return rounded_list


def replace_list_value(input_list: [], old_value, new_value):
    """Replaces instances of a given value in a list with a new value.

    Parameters:
    input_list (list): The list which is having values replaced
    old_value: The value being changed in the list. Can be an int, string or float.
    new_value: The value being changed to in the list. Can be an int, string or float.

    """

    for index, element in enumerate(input_list):
        if element == old_value:
            input_list[index] = new_value

    return input_list


def is_empty(input_list: []):
    """Checks if a given list is empty. Doesn't work with numpy arrays.

    Parameters:
    input_list (list): The list being checked to be empty

    Returns:
    not input_list (bool): A bool value where it's true if the list is empty"""

    return not input_list


def get_length(structure):
    """Gets the length of a passed structure and returns it. Doesn't work for 2D structures

    Parameters:
    structure: A structure of which to get the length. Can be a string or list.

    Returns:
    counter (int): Contains the number of elements in the structure"""

    counter = 0
    for _ in structure:
        counter += 1

    return counter
