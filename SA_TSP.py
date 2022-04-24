import math
import numpy as np
import visualization
from utils import *
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt


class SimulatedAnnealing():

    def __init__(self, cities, distances, cooling_ratio=0.999, temperature=None):

        self.cities = cities
        self.num_cities = len(cities)
        self.distances = distances
        self.temperature = math.sqrt(
            self.num_cities) if temperature is None else temperature
        self.cooling_ratio = cooling_ratio
        self.temperature_update_freq = 100
        self.best_solution = None
        self.min_cost = float("Inf")
        self.costs = []
        self.accept_probs = []
        self.temps = []

    def cal_cost(self, path):
        """
            Calculate the cost of the given solution
        """
        cost = 0
        for i in range(1, len(path)):
            cost += self.distances[path[i]][path[i-1]]

        return cost

    def sample_initial_state(self):
        """
            Sample the initial Path, will do this greedily, starting from a random city,
            will take the nearest neighbor iteratively until visiting all the cities
        """

        random_city = np.random.randint(self.num_cities)
        print(f"The initial city is: {random_city}")

        current_city = random_city
        not_visitied_cities = set(range(self.num_cities))
        current_path = [current_city]
        for _ in range(self.num_cities-1):
            not_visitied_cities.remove(current_city)
            nearest_neighbor = min(
                not_visitied_cities, key=lambda k: self.distances[current_city][k])
            current_path.append(nearest_neighbor)
            current_city = nearest_neighbor

        self.initial_solution = current_path
        self.initial_sol_cost = self.cal_cost(self.initial_solution)

        if self.initial_sol_cost < self.min_cost:
            self.best_solution, self.min_cost = self.initial_solution, self.initial_sol_cost

        print(
            f"The initial solution is: {self.initial_solution} === The initial cost is: {self.initial_sol_cost}")

        return current_path, self.initial_sol_cost

    def get_acceptance_ratio(self, cand_solution_cost):
        """
            Calculate the acceptance ratio (alpha)
        """
        print(abs(cand_solution_cost - self.current_cost))
        print(math.exp(-abs(cand_solution_cost - self.current_cost) / self.temperature))
        return math.exp(-abs(cand_solution_cost - self.current_cost) / self.temperature)

    def accept(self, cand_solution):

        cand_solution_cost = self.cal_cost(cand_solution)
        if cand_solution_cost < self.current_cost:
            self.current_solution = cand_solution
            self.current_cost = cand_solution_cost
            if self.current_cost < self.min_cost:
                self.best_solution, self.min_cost = self.current_solution, self.current_cost
            return 1.0
        else:
            alpha = self.get_acceptance_ratio(cand_solution_cost)
            if np.random.random() < self.get_acceptance_ratio(cand_solution_cost):
                self.current_solution, self.current_cost = cand_solution, cand_solution_cost
            return alpha

    def plot_costs(self):
        visualization.plot_cost(self.costs)

    def vis_path(self, path):
        visualization.plot_path(path, self.cities)

    def run(self):
        """
            Run the algorithm:
                1. Sample the initial state, and set the time step to 0.
                2. The initial temperature is set to the sqrt of the number of cities (might 
                    change it to the std of the costs of N random samples).
                3. Generate the next state, by swapping two randomly selected cities of the current solution.
                4. Check the acceptance criteria of the new generated sample.
                5. Decrease the temperature.
                6. increment the time step. 

        """
        t_step = 0
        self.current_solution, self.current_cost = self.sample_initial_state()

        while self.temperature > 1e-2:
            print(
                f"TIME STEP: {t_step} ==== TEMPERATURE: {self.temperature} ==== BEST COST: {self.min_cost} === CURRENT COST: {self.current_cost}")
            candidate_solution = self.current_solution
            cities_to_swap = np.random.choice(range(self.num_cities), 2, replace=False)
            temp = candidate_solution[cities_to_swap[0]]
            candidate_solution[cities_to_swap[0]] = candidate_solution[cities_to_swap[1]]
            candidate_solution[cities_to_swap[1]] = temp

            # l = np.random.randint(2, self.num_cities)
            # i = np.random.randint(0, self.num_cities)
            # candidate_solution[i: (
            #     i + l)] = reversed(candidate_solution[i: (i + l)])

            accpetance_prob = self.accept(candidate_solution)
            self.accept_probs.append(accpetance_prob)
            if t_step % self.temperature_update_freq:
                self.temperature *= self.cooling_ratio
            self.temps.append(self.temperature)
            t_step += 1

            self.costs.append(self.current_cost)

        print(f"The best obtained cost is: {self.min_cost}")
        print(f"Th initial cost is: {self.initial_sol_cost}")
        # Plot the cities (try with the russian outlies)
