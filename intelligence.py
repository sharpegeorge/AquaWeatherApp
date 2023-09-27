import numpy as np
from matplotlib import pyplot as mat_plot
from math import floor


def find_red_pixels(map_filename, upper_threshold=100, lower_threshold=50):
    """Searches a .png file row by row for red pixels, identifying if they are above or below certain RGB values

    Parameters:
    map_filename (str): The file name of the map being scanned
    upper_threshold (int): The upper threshold for relevant RGB values, default is 100
    lower_threshold (int): The lower threshold for relevant RGB values, default is 50

    Returns:
    output_map (np.ndarray): A 2D numpy array representing a binary colour map where 1's indicate a pixel of interest"""

    colour_map = load_colour_map(map_filename)

    # Scaling scale values [0-1] to [0-255] to avoid precision errors with threshold values
    colour_map = scale_img(colour_map, 255)

    # Unpacking sizes of the colour map and creating 2D output array
    height, width, *_ = colour_map.shape
    output_map = np.zeros((height, width))

    # Iterates through each pixel of colour map
    for row_number, row in enumerate(colour_map):
        for column_number, rgb_value in enumerate(colour_map[row_number]):

            red = rgb_value[0]
            green = rgb_value[1]
            blue =  rgb_value[2]

            # Using guard clauses to only keep pixels of interest
            if red <= upper_threshold:
                continue
            if green >= lower_threshold:
                continue
            if blue >= lower_threshold:
                continue

            output_map[row_number, column_number] = 1

    mat_plot.imsave('data/map-red-pixels.jpg', output_map, cmap='gray')
    return output_map


def find_cyan_pixels(map_filename, upper_threshold=100, lower_threshold=50):
    """Searches a .png file row by row for cyan pixels, identifying if they are above or below certain RGB values

    Parameters:
    map_filename (str): The file name of the map being scanned
    upper_threshold (int): The upper threshold for relevant RGB values, default is 100
    lower_threshold (int): The lower threshold for relevant RGB values, default is 50

    Returns:
    output_map (np.ndarray): A 2D numpy array representing a binary colour map where 1's indicate a pixel of interest"""

    colour_map = load_colour_map(map_filename)

    # Scaling scale values [0-1] to [0-255] to avoid precision errors with threshold values
    colour_map = scale_img(colour_map, 255)

    # Unpacking sizes of the colour map and creating 2D output array
    height, width, *_ = colour_map.shape
    output_map = np.empty((height, width))

    # Iterates through each pixel of colour map
    for row_number, row in enumerate(colour_map):
        for column_number, rgb_value in enumerate(row):

            red = rgb_value[0]
            green = rgb_value[1]
            blue = rgb_value[2]

            # Using guard clauses to only keep pixels of interest
            if red >= lower_threshold:
                continue
            if green <= upper_threshold:
                continue
            if blue <= upper_threshold:
                continue

            output_map[row_number, column_number] = 1

    mat_plot.imsave('data/map-cyan-pixels.jpg', output_map, cmap='gray')
    return output_map


def detect_connected_components(IMG):
    """Searches a .png file row by row for connected components (assuming 8-adjacency), then printing them and
    writing to a file 'cc-output-2a.txt'

    Parameters:
    IMG (np.ndarray): A 2D numpy array representing a binary colour map where 1's indicate a pixel of interest

    Returns:
    MARK (np.ndarray): A 2D numpy array where each pixel has its own components code assigned or a 0 if it's
                       not a pixel of interest"""

    height, width, *_ = IMG.shape
    MARK = np.zeros((height, width))
    number_of_components = 0

    print("")  # Formatting reasons
    # Used to give progress updates to user
    ten_percent_value = floor(height / 10)

    # Creating queue
    Q = np.ndarray((0, 2))

    for y, row in enumerate(IMG):

        # Gives progress updates to user
        if y % ten_percent_value == 0:
            print(f" {((y // ten_percent_value)+1) * 10}%")

        for x, pixel in enumerate(row):

            if IMG[y, x] and not MARK[y, x]:
                # The algorithm was modified here to track/group the pavement pixels into components
                number_of_components += 1
                MARK[y, x] = number_of_components
                Q = np.append(Q, [(y, x)], axis=0)

                while len(Q) != 0:
                    deleted_item = [int(Q[0][0]), int(Q[0][1])]
                    Q = np.delete(Q, 0, axis=0)

                    # For each 8-neighbour
                    for y in range(-1, 2):
                        for x in range(-1, 2):
                            new_x = deleted_item[0] + y
                            new_y = deleted_item[1] + x

                            try:
                                if IMG[new_x, new_y] and not MARK[new_x, new_y]:
                                    # Used to track the pavement pixels
                                    MARK[new_x, new_y] = number_of_components
                                    Q = np.append(Q, [(new_x, new_y)], axis=0)
                            except IndexError:
                                _ = _

    connected_components = convert_to_dict(MARK)
    with open("data/cc-output-2a.txt", "w") as file:
        for key in connected_components:
            file.writelines(f"Connected Component {int(key)}, number of pixels = {connected_components[key]}\n")
        file.writelines(f"Total number of connected components = {len(connected_components)}")

    print("")
    for key in connected_components:
        print(f" Connected Component {int(key)}, number of pixels = {connected_components[key]}")

    return MARK


def detect_connected_components_sorted(MARK):
    """Searches a .png file row by row for connected components (assuming 8-adjacency), then printing them sorted and
        writing to a file 'cc-output-2a.txt'. It also presents the two largest components in a binary colour map.

        Parameters:
        MARK (np.ndarray): A 2D numpy array where each pixel has its own components code assigned or a 0 if it's
                           not a pixel of interest"""

    components_unsorted = convert_to_dict(MARK)
    components_array = []

    for key in components_unsorted:
        components_array.append([components_unsorted[key], key])

    components_sorted = bubble_sort(components_array)

    # Writing output to file
    with open("data/cc-output-2b.txt", "w") as file:
        for index, element in enumerate(components_sorted):
            file.writelines(f"Connected Component {int(components_sorted[index][1])}, number of pixels = "
                            f"{components_sorted[index][0]}\n")
        file.writelines(f"Total number of connected components = {len(components_sorted)}")

    # Printing to user
    for index, components in enumerate(components_sorted):
        print(f" Connected Component {int(components_sorted[index][1])}, number of pixels = "
              f"{components_sorted[index][0]}")

    # Displaying two largest components in binary colour map
    two_largest_components = MARK
    for row_number, row in enumerate(two_largest_components):
        for column_number, element in enumerate(row):
            if element == 129 or element == 109:
                two_largest_components[row_number][column_number] = 1
            else:
                two_largest_components[row_number][column_number] = 0

    mat_plot.imshow(two_largest_components, cmap='gray')
    mat_plot.show()


# My functions

def bubble_sort(array):
    """Bubble sort descending algorithm modified to fit a 2D array

    Parameters:
    array (np.ndarray): 2D numpy array

    Returns:
    array (np.ndarray): 2D numpy array sorted in descending order"""

    n = len(array[:])
    swapped = False

    for i in range(n-1):
        for j in range(0, n-i-1):

            if array[j][0] < array[j+1][0]:
                # Swapping values
                temp = array[j]
                array[j] = array[j+1]
                array[j+1] = temp
                swapped = True

        if not swapped:
            return array

    return array


def convert_to_dict(input):
    """Converts a 2D numpy array to a dictionary for the 'detected_components' and 'detected_components_sorted'
    functions to use when printing.

    Parameters:
    input (np.ndarray): A 2D numpy array where each pixel has its own components code assigned or a 0 if it's
                        not a pixel of interest

    Returns:
    output_dict (dict): A dictionary where each component code is a key which points to the number of pixels
                        in that component"""

    output_dict = {}

    for y, row in enumerate(input):
        for x, element in enumerate(row):

            if not element:
                continue

            if element not in output_dict:
                output_dict[element] = 1
            else:
                output_dict[element] = output_dict[element] + 1

    return output_dict


def scale_img(colour_img, value):
    """Used to scale colour image values from range [0-1] to [0-255]

    Parameters:
    colour_img (np.ndarray): The colour image generated from the image being passed
    value (int): How much to scale the values by

    Returns:
    colour_img (np.ndarray): The same colour image as passed but with multiple values"""

    colour_img = colour_img * value
    return colour_img


def load_colour_map(map_filename):
    """Reads a file to return a colour_map as a 2D numpy array

    Parameters:
    map_filename (str): The file name of the image being loaded

    Returns:
    colour_map (np.ndarray): A 2D array representing the colour map being loaded"""

    colour_map = mat_plot.imread(map_filename)
    return colour_map
