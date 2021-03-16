def get_cost(solution, parameters):
    # Calculates cost for a certain solution
    costs_list = extract_costs(parameters["FLEET"])
    distances_list = parameters["DISTANCE_TIMES_DATA"]
    locations_list = parameters["DISTANCE_TIMES_COORDINATES"]

    distance_cost = 0
    fixed_costs = 0
    hourly_costs = 0
    for route in solution:
        # FIXED COSTS
        # costs for truck
        # route[0] is used because every fleet type that leaves the depot has the fixed costs associated with it
        fixed_costs += costs_list["TRUCK"]["OPERATING_TIME"]

        # costs if swap bodies are attached
        fixed_costs += costs_list["SWAP_BODY"]["OPERATING_TIME"] * (route[0]["SWAP_BODY_TRUCK"] +
                                                                    route[0]["SWAP_BODY_SEMI_TRAILER"])

        # costs if semi_trailer is attacked
        fixed_costs += costs_list["TRAILER"]["OPERATING_TIME"] * (route[0]["SEMI_TRAILER_ATTACHED"])

        # COST PER HOUR
        # route[0] is used because every fleet type that leaves the depot has the hourly costs associated with it
        # costs for truck
        # TODO hourly costs kloppen nog niet
        hourly_costs += costs_list["TRUCK"]["HOURLY_COSTS"]

        # costs if swap bodies are attached
        hourly_costs += costs_list["SWAP_BODY"]["HOURLY_COSTS"] * (route[0]["SWAP_BODY_TRUCK"] +
                                                                   route[0]["SWAP_BODY_SEMI_TRAILER"])

        # costs if semi_trailer is attacked
        hourly_costs += costs_list["TRAILER"]["HOURLY_COSTS"] * (route[0]["SEMI_TRAILER_ATTACHED"])

        # COSTS PER KM
        last_loc_nr = -1
        for location in route:
            loc_nr = 0
            for loc in locations_list:
                if location["LOCATION_POS"] == loc:
                    break
                loc_nr += 1
            if location["ROUTE_LOCATION"] == 1:
                first_loc = loc_nr

            if last_loc_nr != -1:
                # costs for truck
                distance_cost += costs_list["TRUCK"]["DISTANCE_COSTS"] * distances_list[loc_nr][last_loc_nr]

                # costs if swap bodies are attached
                distance_cost += (location["SWAP_BODY_TRUCK"] + location["SWAP_BODY_SEMI_TRAILER"]) * \
                                 costs_list["SWAP_BODY"]["DISTANCE_COSTS"] * distances_list[loc_nr][last_loc_nr]

                # costs if semi_trailer is attached
                distance_cost += (location["SEMI_TRAILER_ATTACHED"]) * costs_list["TRAILER"]["DISTANCE_COSTS"] * \
                                 distances_list[loc_nr][last_loc_nr]

            last_loc_nr = loc_nr

        # costs for return to depot
        # costs for truck
        distance_cost += costs_list["TRUCK"]["DISTANCE_COSTS"] * distances_list[last_loc_nr][first_loc]

        # costs if swap bodies are attached
        distance_cost += (location["SWAP_BODY_TRUCK"] + location["SWAP_BODY_SEMI_TRAILER"]) * \
                         costs_list["SWAP_BODY"]["DISTANCE_COSTS"] * distances_list[last_loc_nr][first_loc]

        # costs if semi_trailer is attached
        distance_cost += (location["SEMI_TRAILER_ATTACHED"]) * costs_list["TRAILER"]["DISTANCE_COSTS"] * \
                         distances_list[last_loc_nr][first_loc]

    return distance_cost + hourly_costs + fixed_costs


def extract_costs(costs):
    costs_list = dict()
    for i in range(len(costs)):
        if costs["TYPE"][i] == "TRUCK":
            costs_list["TRUCK"] = (dict(DISTANCE_COSTS=costs["COSTS [MU/km]"][i],
                                        HOURLY_COSTS=costs["COSTS [MU/h]"][i],
                                        FIXED_COSTS=costs["COSTS [MU/USAGE]"][i],
                                        OPERATING_TIME=costs["OPERATING_TIME [s]"][i]))
        elif costs["TYPE"][i] == "SEMI_TRAILER":
            costs_list["TRAILER"] = (dict(DISTANCE_COSTS=costs["COSTS [MU/km]"][i],
                                               HOURLY_COSTS=costs["COSTS [MU/h]"][i],
                                               FIXED_COSTS=costs["COSTS [MU/USAGE]"][i],
                                               OPERATING_TIME=costs["OPERATING_TIME [s]"][i]))
        elif costs["TYPE"][i] == "SWAP_BODY":
            costs_list["SWAP_BODY"] = (dict(DISTANCE_COSTS=costs["COSTS [MU/km]"][i],
                                            HOURLY_COSTS=costs["COSTS [MU/h]"][i],
                                            FIXED_COSTS=costs["COSTS [MU/USAGE]"][i],
                                            OPERATING_TIME=costs["OPERATING_TIME [s]"][i]))
    if len(costs_list) != 3:
        print("INVALID COSTS.CSV FILE")

    return costs_list
