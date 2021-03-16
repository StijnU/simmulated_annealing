import random
import math
from python import costs, neighbours as nbs


############################## SIMULATED ANNEALING #######################################

# performs simulated annealing that starts with a given initial solution
def simulated_annealing(initial_state, parameters, initial_temp, exit_temp, alpha):
    initial_temp = initial_temp
    exit_temp = exit_temp
    alpha = alpha

    current_temp = initial_temp

    # Start by initializing the current state with the initial state
    current_state = initial_state
    solution = current_state
    count = 0

    while current_temp > exit_temp:
        # rearrange solution so that routeID's and route positions are correct
        solution = rearrange_routeID(solution)
        neighbours, exchange_neighbours = nbs.get_neighbours(solution, parameters)
        if neighbours == list():
            return solution
        neighbour = random.choice(neighbours)

        # Check if neighbor is best so far
        cost_diff = costs.get_cost(current_state, parameters) - costs.get_cost(neighbour, parameters)

        # if the new solution is better, accept it
        if cost_diff > 0:
            solution = rearrange_routeID(neighbour)
        # if the new solution is not better, accept it with a probability of e^(-cost/temp)
        else:
            if random.uniform(0, 1) < math.exp(cost_diff / current_temp):
                print("worse accepted")
                solution = rearrange_routeID(neighbour)
        # decrement the temperature
        current_temp -= alpha
        if current_temp%1000 == 0:
            print("Current temperature: "+ str(current_temp))
        count += 1
    return solution


def check_routeID_and_routeNR(solution):
    routeID = 1
    routeNR = 1
    check = True
    for route in solution:
        for location in route:
            if location["ROUTE_ID"] != routeID or location["ROUTE_LOCATION"] != routeNR:
                print("FALSE LOCATION!!!")
                print(location)
                print("ROUDE ID SHOULD BE:")
                print("LOCATION NR SHOULD BE:")
                print(location[1])
                check = False
            routeNR += 1
        routeID += 1
        routeNR = 1
    return check


def rearrange_routeID(solution):
    routeID = 1
    for route in solution:
        route_step = 1
        for location in route:
            location["ROUTE_ID"] = routeID
            location["ROUTE_LOCATION"] = route_step
            route_step += 1
        routeID += 1
    return solution


###########################################INITIAL SOLUTION####################################################
# takes all the parameters and gives an initial solution
# Parameters is a list of lists with data from csv files
# Parameters = [ DistanceTimesCoords,
#                 DistanceTimesData,
#                 Fleet,
#                 Locations,
#                 SwapActions ]

def get_initial_solution(parameters):

    initial_solution = []

    # Only locations needed for initial solution
    # Location =
    #
    # LOCATION_TYPE         object
    # LOCATION_ID           object
    # POST_CODE              int64
    # CITY                  object
    # X_COORD              float64
    # Y_COORD              float64
    # QUANTITY               int64
    # TRAIN_POSSIBLE         int64
    # SERVICE_TIME [s]       int64

    route_id = 1
    locations = parameters["LOCATIONS"]
    for i in range(len(locations)):
        if locations["LOCATION_TYPE"][i] == "DEPOT":
            depot_location = [locations["X_COORD"][i], locations["Y_COORD"][i]]
            depot_id = locations["LOCATION_ID"][i]

            # Round coords
            depot_location = [round(depot_location[0], 6), round(depot_location[1], 6)]

        if locations["QUANTITY"][i] > 0:
            if locations["TRAIN_POSSIBLE"][i] == 0:
                location_id = locations["LOCATION_ID"][i]
                location_pos = [locations["X_COORD"][i], locations["Y_COORD"][i]]
                location_type = locations["LOCATION_TYPE"][i]
                semi_trailer_attached = 0
                swap_body_truck = 0
                swap_body_semi_trailer = 0
                swap_action = "NONE"
                swap_body_1_quantity = locations["QUANTITY"][i]
                swap_body_2_quantity = 0

                # Round coords
                location_pos = [round(location_pos[0], 6), round(location_pos[1], 6)]

                add_route = \
                    [dict(ROUTE_ID=route_id, ROUTE_LOCATION=1, LOCATION_ID=depot_id, LOCATION_POS=depot_location,
                          LOCATION_TYPE="DEPOT", SEMI_TRAILER_ATTACHED=semi_trailer_attached,
                          SWAP_BODY_TRUCK=swap_body_truck, SWAP_BODY_SEMI_TRAILER=swap_body_semi_trailer,
                          SWAP_ACTION=swap_action, SWAP_BODY_1_QUANTITY=swap_body_1_quantity,
                          SWAP_BODY_2_QUANTITY=swap_body_2_quantity),
                     dict(ROUTE_ID=route_id, ROUTE_LOCATION=2, LOCATION_ID=location_id, LOCATION_POS=location_pos,
                          LOCATION_TYPE=location_type, SEMI_TRAILER_ATTACHED=semi_trailer_attached,
                          SWAP_BODY_TRUCK=swap_body_truck, SWAP_BODY_SEMI_TRAILER=swap_body_semi_trailer,
                          SWAP_ACTION=swap_action, SWAP_BODY_1_QUANTITY=swap_body_1_quantity,
                          SWAP_BODY_2_QUANTITY=swap_body_2_quantity),
                     dict(ROUTE_ID=route_id, ROUTE_LOCATION=3, LOCATION_ID=depot_id, LOCATION_POS=depot_location,
                          LOCATION_TYPE="DEPOT", SEMI_TRAILER_ATTACHED=semi_trailer_attached,
                          SWAP_BODY_TRUCK=swap_body_truck, SWAP_BODY_SEMI_TRAILER=swap_body_semi_trailer,
                          SWAP_ACTION=swap_action, SWAP_BODY_1_QUANTITY=0, SWAP_BODY_2_QUANTITY=0)]

                initial_solution.append(add_route)

            if locations["TRAIN_POSSIBLE"][i] == 1:
                location_id = locations["LOCATION_ID"][i]
                location_pos = [locations["X_COORD"][i], locations["Y_COORD"][i]]
                location_type = locations["LOCATION_TYPE"][i]
                semi_trailer_attached = 0
                swap_body_truck = 0
                swap_body_semi_trailer = 0
                swap_action = "NONE"
                swap_body_1_quantity = locations["QUANTITY"][i]
                swap_body_2_quantity = 0

                # Round coords
                location_pos = [round(location_pos[0], 6), round(location_pos[1], 6)]

                add_route = \
                    [dict(ROUTE_ID=route_id, ROUTE_LOCATION=1, LOCATION_ID=depot_id, LOCATION_POS=depot_location,
                          LOCATION_TYPE="DEPOT", SEMI_TRAILER_ATTACHED=semi_trailer_attached,
                          SWAP_BODY_TRUCK=swap_body_truck, SWAP_BODY_SEMI_TRAILER=swap_body_semi_trailer,
                          SWAP_ACTION=swap_action, SWAP_BODY_1_QUANTITY=swap_body_1_quantity,
                          SWAP_BODY_2_QUANTITY=swap_body_2_quantity),
                     dict(ROUTE_ID=route_id, ROUTE_LOCATION=2, LOCATION_ID=location_id, LOCATION_POS=location_pos,
                          LOCATION_TYPE=location_type, SEMI_TRAILER_ATTACHED=semi_trailer_attached,
                          SWAP_BODY_TRUCK=swap_body_truck, SWAP_BODY_SEMI_TRAILER=swap_body_semi_trailer,
                          SWAP_ACTION=swap_action, SWAP_BODY_1_QUANTITY=swap_body_1_quantity,
                          SWAP_BODY_2_QUANTITY=swap_body_2_quantity),
                     dict(ROUTE_ID=route_id, ROUTE_LOCATION=3, LOCATION_ID=depot_id, LOCATION_POS=depot_location,
                          LOCATION_TYPE="DEPOT", SEMI_TRAILER_ATTACHED=semi_trailer_attached,
                          SWAP_BODY_TRUCK=swap_body_truck, SWAP_BODY_SEMI_TRAILER=swap_body_semi_trailer,
                          SWAP_ACTION=swap_action, SWAP_BODY_1_QUANTITY=0, SWAP_BODY_2_QUANTITY=0)]

                initial_solution.append(add_route)

            route_id += 1
    return initial_solution






