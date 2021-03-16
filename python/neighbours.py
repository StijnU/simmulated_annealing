def get_neighbours(solution, parameters):
    # Returns neighbors for given solution.
    neighbours = list()
    # VRP neighbours
    # new solutions are searched from the classical VRP problem
    # customers are added en removed from routes
    # different operators are used to find neighbours

    # relocate operator
    new_solution = solution.copy()
    neighbours += relocate_neighbour(new_solution)
    # swap operator
    new_solution = solution.copy()
    neighbours += swap_neighbour(new_solution)
    # add new route
    new_solution = solution.copy()
    neighbours += add_new_route(new_solution, parameters)
    # exchange operator
    # new_solution = solution.copy()
    # exchange_neighbours = exchange_neighbour(new_solution)
    # neighbours += exchange_neighbours
    exchange_neighbours = []
    # cross operator
    # neighbours += cross_neighbour(new_solution, parameters)

    # SB-VRP extension
    # new solutions are searched for the SB-VRP problem specific
    # swap locations and swap moves are added or removed

    return neighbours, exchange_neighbours


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
                for route_2 in solution:
                    if route_1 != route_2:
                        for location_2 in route_2:
                            if location_2["LOCATION_TYPE"] == "CUSTOMER":
                                neighbour_solutions += swap_customers_from_route(solution, route_1, route_2, location_1,
                                                                                 location_2)
    return neighbour_solutions


def swap_customers_from_route(solution, route_1, route_2, location_1, location_2):
    new_solutions = []
    # try to add the location in every route from solution
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
    while route_1_position < len(route_1):

        # add location to every add_route from solution
        filled_route_1_copy = route_1_copy[:route_1_position] + [location_2_copy] + route_1_copy[route_1_position:]
        route_2_position = 1

        while route_2_position < len(route_2):
            filled_route_2_copy = route_2_copy[:route_2_position] + [location_1_copy] + route_2_copy[route_2_position:]

            # insert route in correct position according to route_ID
            added_solution = new_solution.copy()
            added_solution = added_solution + [filled_route_1_copy] + [filled_route_2_copy]

            # add new_solution to new_solutions
            new_solutions.append(added_solution)
            route_2_position += 1
        route_1_position += 1
    return new_solutions


#########################################K-EXCHANGE OPERATOR##################################################
# Exchanges 2 different customers in the same route
def exchange_neighbour(solution):
    new_solutions = []
    location_1_pos = 1
    location_2_pos = 1
    for route in solution:
        for location_1 in route:
            for location_2 in route[:location_1[1] - 1]:
                if location_1 != location_2:
                    if location_1[4] == "CUSTOMER" and location_2[4] == "CUSTOMER":
                        new_route = route.copy()
                        new_route[location_2[1] - 1] = location_1
                        new_route[location_1[1] - 1] = location_2

                        new_solution = solution[:route[0][0] - 1] + [new_route] + solution[route[0][0] - 1:]
                        new_solutions.append(new_solution)
                        location_2_pos += 1
            location_1_pos += 1
            location_2_pos = 1

    return new_solutions


#########################################CROSS OPERATOR#######################################################
def cross_neighbour(solution, parameters):
    new_solutions = []
    for route_1 in solution:
        for route_2 in solution[:route_1[0][0] - 1]:
            if route_1 != route_2:
                if len(route_1) > 3 and len(route_2) > 3:
                    for location_1 in route_1:
                        for location_2 in route_2:
                            if location_1[4] == "CUSTOMER" and location_2[4] == "CUSTOMER":
                                new_route_1 = route_1.copy()
                                new_route_2 = route_2.copy()
                                new_solution = solution.copy()
                                new_solution.remove(route_1)
                                new_solution.remove(route_2)

                                new_route_1.remove(location_1)
                                new_route_2.remove(location_2)

                                new_route_1_length = len(new_route_1)
                                new_route_2_length = len(new_route_2)

                                insert_position_1 = 1
                                insert_position_2 = 1

                                while insert_position_1 < new_route_1_length:
                                    new_route_1 = new_route_1[:insert_position_1] + [location_2] \
                                                  + new_route_1[insert_position_1:]
                                    while insert_position_2 < new_route_2_length:
                                        new_route_2 = new_route_2[:insert_position_2] + [location_1] \
                                                      + new_route_2[insert_position_2:]
                                        new_solution += [new_route_1] + [new_route_2]
                                        new_solutions.append(new_solution)
                                        insert_position_2 += 1
                                    insert_position_1 += 1
    return new_solutions
