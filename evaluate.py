from turtle import distance
from SA_TSP import SimulatedAnnealing
import pandas as pd
import numpy as np
from utils import *
import json
import visualization


if __name__ == "__main__":

    
    cities = pd.read_csv('top_populated_cities.csv')
    distances = get_distances(cities)
    sa_tsp = SimulatedAnnealing(cities, distances, temperature=30000)
    sa_tsp.run()
    visualization.plot_all(sa_tsp.costs, sa_tsp.cities, sa_tsp.best_solution, sa_tsp.temps, sa_tsp.accept_probs)

