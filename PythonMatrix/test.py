import unittest
import main


class TestFunctions(unittest.TestCase):

    def test_distance_between_points_formula(self):
        lat1 = 36.6634467
        lng1 = -87.4773902
        lat2 = 36.876719
        lng2 = -89.5878579
        self.assertTrue(-.00001 <= main.distance_between_points(lat1, lng1, lat2, lng2) - 189.469531455 <= 0.00001)

    def test_for_successful_csv_file_import(self):
        check_cargo_file = []
        check_truck_file = []
        with open(main.cargo_fp, 'rb') as cargo_file:
            reader = main.csv.DictReader(cargo_file)
            for row in reader:
                check_cargo_file.append(row)
        with open(main.truck_fp, 'rb') as truck_file:
            reader = main.csv.DictReader(truck_file)
            for row in reader:
                check_truck_file.append(row['truck'])
        self.assertTrue(len(check_cargo_file) > 0)
        self.assertTrue(len(check_truck_file) > 0)

    def test_successful_distance_matrix_creation(self):
        self.assertTrue(len(main.create_distance_matrix(main.test_fp)) > 0)

    def test_correct_trucks_used(self):
        test_matrix = main.create_distance_matrix(main.test_fp)
        test_trucks_used, _ = main.find_minimal_distance_no_truck_used_twice(test_matrix)
        self.assertTrue(len(test_trucks_used) > 0)
        self.assertTrue(8 in test_trucks_used)
        self.assertEqual(test_trucks_used[8], 189.46953145545078)

    def test_correct_cargo_indexes(self):
        test_matrix = main.create_distance_matrix(main.test_fp)
        _, test_cargo_indexes = main.find_minimal_distance_no_truck_used_twice(test_matrix)
        self.assertTrue(len(test_cargo_indexes) > 0)
        self.assertEqual(test_cargo_indexes[6], 3)

    def test_correct_min_distance(self):
        test_matrix = main.create_distance_matrix(main.test_fp)
        trucks_with_min_distances, _ = main.find_minimal_distance_no_truck_used_twice(test_matrix)
        self.assertTrue(3 in trucks_with_min_distances)
        self.assertTrue(trucks_with_min_distances[3], 476.5170842163323)

    def test_correct_overall_distance(self):
        test_matrix = main.create_distance_matrix(main.test_fp)
        test_trucks, test_cargo_indices = main.find_minimal_distance_no_truck_used_twice(test_matrix)
        truck_cargo_map, truck_distance_cargo_map = main.map_trucks_to_cargo(test_trucks, test_cargo_indices)
        test_overall_distance_travelled = 0
        for truck in truck_cargo_map:
            individual_truck_route_distance = truck_distance_cargo_map[truck] + \
                                              main.distance_between_points(float(truck_cargo_map[truck]['origin_lat']),
                                                                      float(truck_cargo_map[truck]['origin_lng']),
                                                                      float(truck_cargo_map[truck]['destination_lat']),
                                                                      float(truck_cargo_map[truck]['destination_lng']))
            test_overall_distance_travelled += individual_truck_route_distance
        self.assertTrue(-0.000001 <= test_overall_distance_travelled - 13984.666734846624 <= 0.0000001)


if __name__ == '__main__':
    unittest.main()
