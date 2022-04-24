import pandas as pd


cities_data = pd.read_csv('/home/hussein/STDS_IU/SimulatedAnnealing_TSP/cities.csv')
top_populated_cities = cities_data.sort_values('population', ascending=False, ignore_index=True)[:30]
top_populated_cities.at[0, 'city'] = 'Москва'
top_populated_cities.at[1, 'city'] = 'Санкт-Петербург'
top_populated_cities.to_csv("top_populated_cities.csv")

