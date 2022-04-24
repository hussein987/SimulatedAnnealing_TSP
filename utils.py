import geopy.distance
import numpy as np


def get_name_by_idx(idx, cities):
    return cities.loc[idx]['city']

def get_coords_by_idx(idx, cities):
    return cities.loc[idx]['geo_lat'], cities.loc[idx]['geo_lon']

def dist_from_coords(city1, city2):
    return geopy.distance.geodesic(city1, city2).km

def get_distances(cities):
    num_cities = len(cities)

    dist = np.empty((num_cities, num_cities))
    for idx, row in cities.iterrows():
        coordinates1 = (row['geo_lat'], row['geo_lon'])
        for idx1, row1 in cities.iterrows():
            coordinates2 = (row1['geo_lat'], row1['geo_lon'])
            distance = dist_from_coords(coordinates1, coordinates2)
            print(f"The distance between {row['city']} and {row1['city']} is {distance} km")
            dist[idx, idx1] = distance
    return dist
