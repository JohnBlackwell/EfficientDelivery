# Python 2.7

import csv
from math import radians, cos, sin, asin, sqrt

test_fp = r'trucksTest.csv'
truck_fp = r'trucks.csv'
cargo_fp = r'cargo.csv'


# calculate the distance between GPS coordinates using haversine formula
def distance_between_points(lat1, lon1, lat2, lon2):
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r


# calculate the distance between a truck and the seven different cargo pickup locations
def distance_from_truck_to_all_cargoes(truck_lat, truck_lon):
    distance_to_cargo_pickup = list()
    with open(cargo_fp, 'rb') as cargo_file:
        reader = csv.DictReader(cargo_file)
        for row in reader:
            cargo_lat, cargo_lon = float(row['origin_lat']), float(row['origin_lng'])
            distance_to_cargo_pickup.append(distance_between_points(truck_lat, truck_lon, cargo_lat, cargo_lon))
    return distance_to_cargo_pickup


# create a 2D array of floats representing the distance from each truck to each cargo pickup
def create_distance_matrix(fp):
    matrix = list()
    with open(fp, 'rb') as truck_file:
        reader = csv.DictReader(truck_file)
        for row in reader:
            truck_lat, truck_lon = float(row['lat']), float(row['lng'])
            matrix.append(distance_from_truck_to_all_cargoes(truck_lat, truck_lon))
    return matrix


# go through each column of the distance matrix to find the truck closest to that cargo (each cargo is a column of the
# matrix)
# once a minimum is found, ensure that the truck associated with that minimum has not been used already
# return trucks used with associated travel distance along with the cargo indexes for later lookup
def find_minimal_distance_no_truck_used_twice(d_matrix):
    truck_used = {}
    truck_cargo = {}
    for j in range(len(d_matrix[0])):
        min_val = 10000000
        check_truck = []
        store_cargo_index = []
        for i in range(len(d_matrix)):
            if i in truck_used:
                continue
            if d_matrix[i][j] < min_val:
                min_val = d_matrix[i][j]
                if len(check_truck) > 0 and len(store_cargo_index) > 0:
                    check_truck.pop()
                    store_cargo_index.pop()
                    check_truck.append(i)
                    store_cargo_index.append(j)
                else:
                    check_truck.append(i)
                    store_cargo_index.append(j)
        truck_used[check_truck[0]] = min_val
        truck_cargo[check_truck[0]] = store_cargo_index[0]
    return truck_used, truck_cargo


# map the name of the truck that will be used to transport the cargo to the cargo itself
# map the distance traveled by the truck to the name of the truck
def map_trucks_to_cargo(t_dict, indexes):
    truck_distance_map = {}
    cargo = []
    truck_name = []
    truck_name_to_cargo = {}
    with open(cargo_fp, 'rb') as cargo_file:
        reader = csv.DictReader(cargo_file)
        for row in reader:
            cargo.append(row)
    with open(truck_fp, 'rb') as truck_file:
        reader = csv.DictReader(truck_file)
        for row in reader:
            truck_name.append(row['truck'])
    for x in t_dict:
        truck_distance_map[truck_name[x]] = t_dict[x]
        truck_name_to_cargo[truck_name[x]] = cargo[indexes[x]]
    return truck_name_to_cargo, truck_distance_map


# print out trucks with their cargoes and destinations
# sum distances for overall optimized distance
def output_truck_to_cargo_mapping_and_distance(truck_name_cargo_map, truck_distance_cargo_map):
    overall_distance_traveled_all_trucks = 0
    for truck in truck_name_cargo_map:
        individual_truck_route_distance = truck_distance_cargo_map[truck] + \
                                          distance_between_points(float(truck_name_cargo_map[truck]['origin_lat']),
                                                                  float(truck_name_cargo_map[truck]['origin_lng']),
                                                                  float(truck_name_cargo_map[truck][
                                                                            'destination_lat']),
                                                                  float(truck_name_cargo_map[truck][
                                                                            'destination_lng']))
        print truck, "will take ", truck_name_cargo_map[truck]['product'], "from", \
            truck_name_cargo_map[truck]['origin_city'], "to", \
            truck_name_cargo_map[truck]['destination_city'], "and the trip will cover", \
            individual_truck_route_distance, "kilometers"
        overall_distance_traveled_all_trucks += individual_truck_route_distance
    print

    print "Overall distance traveled will be ", overall_distance_traveled_all_trucks, "kilometers"


def main():
    distance_matrix = create_distance_matrix(truck_fp)
    trucks_to_use, cargo_indexes = find_minimal_distance_no_truck_used_twice(distance_matrix)
    truck_name_to_cargo_map, truck_distance_to_cargo = map_trucks_to_cargo(trucks_to_use, cargo_indexes)
    output_truck_to_cargo_mapping_and_distance(truck_name_to_cargo_map, truck_distance_to_cargo)


main()
