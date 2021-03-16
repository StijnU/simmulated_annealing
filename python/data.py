#########################################DATA RETRIEVAL/WRITING##############################################
import csv
import pandas as pd
import matplotlib.pyplot as plt
def read_data(data_file_names):
    # initialize problem parameters
    distance_times_coords = 0
    distance_times_data = 0
    fleet = 0
    locations = 0
    swap_actions = 0

    # Read different csv files for problem parameters
    for data_file in data_file_names:

        if data_file == "DistanceTimesCoordinates.csv":
            with open("data/"+data_file) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=';')
                distance_times_coords = list()
                line_count = 0
                for row in csv_reader:
                    if line_count != 0:
                        distance_times_coords.append([float(rowItem) for rowItem in row])
                    line_count += 1
            print("Reading " + data_file + " with " + str(len(distance_times_coords)*len(distance_times_coords[0])) + " attributes")
            print("Rows and columns: " + str((len(distance_times_coords), len(distance_times_coords[0]))))

        elif data_file == "DistanceTimesData.csv":
            with open("data/"+data_file) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=';')
                distance_times_data = []
                line_count = 0
                for row in csv_reader:
                    if line_count != 0:
                        distance_times_data.append([float(rowItem) for rowItem in row])
                    line_count += 1
            print("Reading " + data_file + " with " + str(
                len(distance_times_data) * len(distance_times_data[0])) + " attributes")
            print("Rows and columns: " + str((len(distance_times_data), len(distance_times_data[0]))))

        elif data_file == "Fleet.csv":
            fleet = pd.read_csv("data/"+data_file, encoding="cp1252", sep=";")
            print("Reading " + data_file + " with " + str(fleet.shape[0]) + " attributes")
            print("Rows and columns: " + str(fleet.shape))
        elif data_file == "Locations.csv":
            locations = pd.read_csv("data/"+data_file, encoding="cp1252", sep=";")
            print("Reading " + data_file + " with " + str(locations.shape[0]) + " attributes")
            print("Rows and columns: " + str(locations.shape))
        elif data_file == "SwapActions.csv":
            swap_actions = pd.read_csv("data/"+data_file, encoding="cp1252", sep=";")
            print("Reading " + data_file + " with " + str(swap_actions.shape[0]) + " attributes")
            print("Rows and columns: " + str(swap_actions.shape))
    return {'DISTANCE_TIMES_COORDINATES': distance_times_coords, 'DISTANCE_TIMES_DATA': distance_times_data,
            'FLEET': fleet, 'LOCATIONS': locations, 'SWAP_ACTIONS': swap_actions}


def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False


def write_data(solution):
    with open('solution.csv', mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(
            ["TOUR_ID", "TOUR_POSITION", "LOCATION_COORDS", "LOCATION_ID", "LOCATION_TYPE", "SEMI_TRAILER_ATTACHED",
             "SWAP_BODY_TRUCK",
             "SWAP_BODY_SEMI_TRAILER", "SWAP_ACTION", "SWAP_BODY_1_QUANTITY", "SWAP_BODY_2_QUANTITIY"])
        route_number = 1
        for route in solution:
            for stop in route:
                csv_writer.writerow(stop)
            route_number += 1
    pass

######################################PLOT SOLUTION FUNCTIONS##############################################


def plot_solution(solution):
    plt.figure("SBVRP")
    for route in solution:
        route_x = []
        route_y = []
        for location in route:
            route_x.append(location["LOCATION_POS"][0])
            route_y.append(location["LOCATION_POS"][1])

        plt.plot(route_x, route_y)
    plt.show()