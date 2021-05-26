import sys
from python import costs
from python import simulated_annealing as sa
from python import data

# MAIN FUNCTION

# Arguments should hold all instances needed to solve the sbvrp problem in csv files
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
    instance = args[5]
    starting_temperature = 1000 #int(args[6])
    exit_temperature = 100###int(args[7])
    alpha = 1 #float(args[8])
    parameters = data.read_data(args, instance)

    print("#######################################")
    print("Generating initial solution")
    print("Starting simulated annealing using following parameters")
    print("Starting temperature: "+str(starting_temperature))
    print("Exit temperature: "+str(exit_temperature))
    print("Aplha: "+str(alpha))
    print("#######################################")

    # create initial solution
    initial_solution = sa.get_initial_solution(parameters)

    # perform simulated annealing with given parameters
    best_found_solution = sa.simulated_annealing(initial_solution,
                                                 parameters,
                                                 starting_temperature,
                                                 exit_temperature,
                                                 alpha)

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
                if location["LOCATION_ID"] in customer_list:
                    customer_list.remove(location["LOCATION_ID"])
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

    for route in best_found_solution:
            for location in route:
                print(location)

    data.plot_solution(best_found_solution)
    data.write_data(best_found_solution)
