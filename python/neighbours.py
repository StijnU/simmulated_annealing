import itertools
from python import costs


def get_neighbours(solution, parameters):
    # Returns neighbors for given solution.
    neighbours = list()
    # VRP neighbours
    # new solutions are searched from the classical VRP problem
    # customers are added en removed from routes
    # different operators are used to find neighbours

    # relocate operator
    new_solution = solution.copy()
    relocate_neighbours = relocate_neighbour(new_solution)
    # swap operator
    new_solution = solution.copy()
    swap_neighbours = swap_neighbour(new_solution)
    # add new route
    new_solution = solution.copy()
    add_neighbours = add_new_route(new_solution, parameters)
    # exchange operator
    new_solution = solution.copy()
    ex_neighbours = exchange_neighbour(new_solution)
    # cross operator
    cross_neighbours = cross_neighbour(new_solution)

    # SB-VRP extension
    # new solutions are searched for the SB-VRP problem specific
    # swap locations and swap moves are added or removed

    # check if solutions are viable
    return relocate_neighbours, swap_neighbours, add_neighbours, ex_neighbours, cross_neighbours


##################################################ADD NEW ROUTE OPERATOR#######################################
# this operator removes a node from a route and creates a new route containing only this node
def add_new_route(solution, parameters):
    new_solutions = []
    for delete_route in solution:
        for location in delete_route:
            if location["LOCATION_TYPE"] == "CUSTOMER":

                # create copies of changing parts of solution
                new_solution = solution.copy()
                delete_route_copy = delete_route.copy()
                location_copy = location.copy()

                # remove route and location that's going to change
                new_solution.remove(delete_route)
                delete_route_copy.remove(location)

                route_id = len(solution) + 1
                locations = parameters["LOCATIONS"]
                for i in range(len(locations)):
                    if locations["LOCATION_TYPE"][i] == "DEPOT":
                        depot_id = locations["LOCATION_ID"][i]
                        depot_location = [locations["X_COORD"][i], locations["Y_COORD"][i]]

                # variables for new depot nodes
                semi_trailer_attached = 0
                swap_body_truck = 0
                swap_body_semi_trailer = 0
                swap_action = "NONE"

                # change location route_ID
                location_copy["ROUTE_ID"] = route_id

                # add route to new solution
                new_solution.append([
                    dict(
                        ROUTE_ID=route_id,
                        ROUTE_LOCATION=1,
                        LOCATION_ID=depot_id,
                        LOCATION_POS=depot_location,
                        LOCATION_TYPE="DEPOT",
                        SEMI_TRAILER_ATTACHED=semi_trailer_attached,
                        SWAP_BODY_TRUCK=swap_body_truck,
                        SWAP_BODY_SEMI_TRAILER=swap_body_semi_trailer,
                        SWAP_ACTION=swap_action,
                        SWAP_BODY_1_QUANTITY=location["SWAP_BODY_1_QUANTITY"],
                        SWAP_BODY_2_QUANTITY=location["SWAP_BODY_2_QUANTITY"]),
                    location_copy,
                    dict(
                        ROUTE_ID=route_id,
                        ROUTE_LOCATION=1,
                        LOCATION_ID=depot_id,
                        LOCATION_POS=depot_location,
                        LOCATION_TYPE="DEPOT",
                        SEMI_TRAILER_ATTACHED=semi_trailer_attached,
                        SWAP_BODY_TRUCK=swap_body_truck,
                        SWAP_BODY_SEMI_TRAILER=swap_body_semi_trailer,
                        SWAP_ACTION=swap_action,
                        SWAP_BODY_1_QUANTITY=location["SWAP_BODY_1_QUANTITY"],
                        SWAP_BODY_2_QUANTITY=location["SWAP_BODY_2_QUANTITY"])])

                # delete route if empty
                if len(delete_route_copy) > 2:
                    new_solution += [delete_route_copy]

                new_solutions.append(new_solution)
    return new_solutions


###########################################RELOCATE OPERATOR##################################################
# operator to remove a node from a route and add it to another
# this function removes given location from given route and adds it to another route in solution
def relocate_customer_from_route(solution, delete_route, add_route, location):
    new_solutions = []
    # try to add the location in every route from solution
    delete_route_copy = delete_route.copy()
    add_route_copy = add_route.copy()
    # generate new solution with 2 changing routes removed
    new_solution = solution.copy()
    new_solution.remove(delete_route)
    new_solution.remove(add_route)

    # remove location from the given route
    new_location = location.copy()
    delete_route_copy.remove(new_location)

    # change route id of new location
    new_location["ROUTE_ID"] = add_route[0]["ROUTE_ID"]
    # try every route_position in add_route for new location
    route_position = 1
    add_route_length = len(add_route)
    while route_position < add_route_length:

        # add location to every add_route from solution
        filled_add_route_copy = add_route_copy[:route_position] + [new_location] + add_route_copy[route_position:]

        # insert route in correct position according to route_ID
        added_solution = new_solution.copy()
        if len(delete_route_copy) > 2:
            added_solution = added_solution + [filled_add_route_copy] + [delete_route_copy]
        else:
            added_solution = added_solution + [filled_add_route_copy]
        # add new_solution to new_solutions
        new_solutions.append(added_solution)
        route_position += 1
    return new_solutions


def relocate_neighbour(solution):
    neighbour_solutions = []
    for delete_route in solution:
        for location in delete_route:
            if location["LOCATION_TYPE"] == "CUSTOMER":
                for add_route in solution:
                    if add_route != delete_route:
                        neighbour_solutions += relocate_customer_from_route(solution, delete_route, add_route, location)
    return neighbour_solutions


###########################################SWAP OPERATOR####################################################
# operator that swaps 2 different customers from route


def swap_neighbour(solution):
    neighbour_solutions = []
    for route_1 in solution:
        for location_1 in route_1:
            if location_1["LOCATION_TYPE"] == "CUSTOMER":
                for route_2 in solution[route_1[0]["ROUTE_ID"]:]:
                    for location_2 in route_2:
                        if location_2["LOCATION_TYPE"] == "CUSTOMER":
                            neighbour_solutions += swap_customers_from_route(solution, route_1, route_2, location_1,
                                                                             location_2)
    return neighbour_solutions


def swap_customers_from_route(solution, route_1, route_2, location_1, location_2):
    new_solutions = []
    # generate copy of routes that are being changed
    route_1_copy = route_1.copy()
    route_2_copy = route_2.copy()

    # generate new solution with 2 changing routes removed
    new_solution = solution.copy()
    new_solution.remove(route_1)
    new_solution.remove(route_2)

    # remove location from the given route
    location_1_copy = location_1.copy()
    location_2_copy = location_2.copy()
    route_1_copy.remove(location_1)
    route_2_copy.remove(location_2)

    # change route id of new location
    location_1_copy["ROUTE_ID"] = route_2[0]["ROUTE_ID"]
    location_2_copy["ROUTE_ID"] = route_1[0]["ROUTE_ID"]

    # try every route_position in add_route for new location
    route_1_position = 1
    while route_1_position < len(route_1_copy) - 1:

        # add location to every add_route from solution
        filled_route_1_copy = route_1_copy[:route_1_position] + [location_2_copy] + route_1_copy[route_1_position:]
        route_2_position = 1

        while route_2_position < len(route_2_copy) - 1:
            filled_route_2_copy = route_2_copy[:route_2_position] + [location_1_copy] + route_2_copy[route_2_position:]

            # insert route in correct position according to route_ID
            added_solution = new_solution.copy()
            added_solution = added_solution + [filled_route_1_copy] + [filled_route_2_copy]

            # add new_solution to new_solutions
            new_solutions.append(added_solution)
            route_2_position += 1
        route_1_position += 1
    return new_solutions


#########################################2-EXCHANGE OPERATOR##################################################
# Exchanges 2 different customers in the same route
def exchange_neighbour(solution):
    new_solutions = []
    for route in solution:
        for location_1 in route:
            for location_2 in route[location_1["ROUTE_LOCATION"]:]:
                if location_1["LOCATION_TYPE"] == "CUSTOMER" and location_2["LOCATION_TYPE"] == "CUSTOMER":
                    new_route = route.copy()
                    new_route[location_2["ROUTE_LOCATION"] - 1] = location_1
                    new_route[location_1["ROUTE_LOCATION"] - 1] = location_2

                    new_solution = solution[:route[0]["ROUTE_ID"] - 1] + [new_route] + solution[route[0]["ROUTE_ID"]:]
                    new_solutions.append(new_solution)
    return new_solutions


#########################################CROSS OPERATOR#######################################################
# this operator chooses 2 locations from 2 different routes than swaps them and puts them in the first position
# it then tries every combination of the other locations in the routes
def cross_neighbour(solution):
    new_solutions = []
    for route_1 in solution:
        for route_2 in solution[route_1[0]["ROUTE_ID"]:]:
            if len(route_1) > 3 and len(route_2) > 3:
                for location_1 in route_1:
                    for location_2 in route_2:
                        if location_1["LOCATION_TYPE"] == "CUSTOMER" and location_2["LOCATION_TYPE"] == "CUSTOMER":
                            new_route_1 = route_1.copy()
                            new_route_2 = route_2.copy()
                            new_solution = solution.copy()
                            new_solution.remove(route_1)
                            new_solution.remove(route_2)

                            new_route_1.remove(location_1)
                            new_route_2.remove(location_2)

                            new_routes_1 = \
                                itertools.permutations(new_route_1[1:len(new_route_1) - 1], len(new_route_1) - 2)
                            new_routes_2 = \
                                itertools.permutations(new_route_2[1:len(new_route_2) - 1], len(new_route_2) - 2)

                            for permuted_route_1 in new_routes_1:
                                for permuted_route_2 in new_routes_2:
                                    new_route_1 = [new_route_1[0]] + [location_2] + \
                                                  list(permuted_route_1) + [new_route_1[len(new_route_1) - 1]]
                                    new_route_2 = [new_route_2[0]] + [location_1] + \
                                                  list(permuted_route_2) + [new_route_2[len(new_route_2) - 1]]

                                    added_new_solution = new_solution + [new_route_1] + [new_route_2]
                                    new_solutions.append(added_new_solution)
    return new_solutions


def check_viable_solution(solution, max_amount):
    for route in solution:
        customer_amounts = [location["SWAP_BODY_1_QUANTITY"] for location in route if
                            location["LOCATION_TYPE"] == "CUSTOMER"]
        total_amount = sum(customer_amounts)

        if total_amount > max_amount:
            return False

        customer_amounts = [location["SWAP_BODY_2_QUANTITY"] for location in route if
                                location["LOCATION_TYPE"] == "CUSTOMER"]
        total_amount = sum(customer_amounts)
        if total_amount > max_amount:
            return False
    return True


def check_quantities(solution):
    for route in solution:
        last_loc_amount = 0
        customer_amounts = [location["SWAP_BODY_1_QUANTITY"] for location in route if
                                location["LOCATION_TYPE"] == "CUSTOMER"]
        total_amount = sum(customer_amounts)

        for location in route:
            if location["LOCATION_TYPE"] == "DEPOT":
                if location["ROUTE_LOCATION"] == 1:
                        location["SWAP_BODY_1_QUANTITY"] = total_amount

            if location["LOCATION_TYPE"] == "CUSTOMER":
                if last_loc_amount == 0:
                    last_loc_amount = location["SWAP_BODY_1_QUANTITY"]
                    location["SWAP_BODY_1_QUANTITY"] = total_amount
                    continue

                last_loc_amount = location["SWAP_BODY_1_QUANTITY"]
                total_amount = total_amount - last_loc_amount
                location["SWAP_BODY_1_QUANTITY"] = total_amount
