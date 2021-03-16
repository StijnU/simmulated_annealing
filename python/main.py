import sys
from python import costs, simulated_annealing as sa, data

# MAIN FUNCTION

# Arguments should hold all data needed to solve the sbvrp problem in csv files
# the csv files always should have the same format with following files:
#
# DistanceTimesCoordinates.csv,
# DistanceTimesData.csv,
# Fleet.csv,
# Locations.csv,
# SwapActions.csv
#
# A solution is a list tours made by trucks


if __name__ == '__main__':
    print("#####################SIMULATED ANNEALING###################")
    print("Start Algorithm")
    print(sys.argv)
    args = sys.argv[1:]
    starting_temperature = 10000
    exit_temperature = 1000
    alpha = 100
    parameters = data.read_data(args)
    print("#######################################")
    print("Generating initial solution using simulated annealing")
    print("Starting temperature: "+str(starting_temperature))
    print("Exit temperature: "+ str(exit_temperature))
    print("Aplha: "+ str(alpha))
    print("#######################################")
    initial_solution = sa.get_initial_solution(parameters)
    best_found_solution = sa.simulated_annealing(initial_solution, parameters, 10000, 1000, 100)


    data.write_data(best_found_solution)
    print("Cost of initial solution: " + str(costs.get_cost(initial_solution, parameters)))
    print("Cost of best found solution: " + str(costs.get_cost(best_found_solution, parameters)))

    customer_list = []
    i = 1
    while i <= len(parameters["LOCATIONS"][parameters["LOCATIONS"]["LOCATION_TYPE"] == "CUSTOMER"]):
        customer_list.append("C" + str(i))
        i += 1
    total_loc = 0

    for route in best_found_solution:
        for location in route:
            if location["LOCATION_ID"] != "D1":
                customer_list.remove(location["LOCATION_ID"])
            #print(location)
            total_loc += 1

    if customer_list == list():
        print("#######################################")
        print(str(len(parameters["LOCATIONS"])) + " customers are visited.")
        print(str(len(best_found_solution)) + " trucks are needed.")
        print("#######################################")
    else:
        print("#######################################")
        print("Wrong solution!")
        print("These customers are not visited:")
        print(customer_list)
        print("#######################################")


    data.plot_solution(best_found_solution)
