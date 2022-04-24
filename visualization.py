import matplotlib.pyplot as plt
from utils import *
import json # or import geojson
import matplotlib.gridspec as gridspec




def plot_cost(costs_list):
    costs_list = np.array(costs_list)
    plt.plot(costs_list / costs_list.max())
    plt.ylabel("Cost")
    plt.xlabel("time_step")
    plt.show()

def plot_path(path, cities, num_iters=1):

    x = []; y = []
    for city in path:
        coords = get_coords_by_idx(path[city], cities)
        y.append(coords[0])
        x.append(coords[1])

    fig, ax = plt.subplots(1, 1, figsize=(20, 8))

    ax.plot(x, y, 'ro')

    a_scale = float(max(x))/float(100)

    ax.arrow(x[-1], y[-1], (x[0] - x[-1]), (y[0] - y[-1]), head_width = 0,
            color ='#6699cc', length_includes_head=False)
    for i in range(0,len(x)-1):
        ax.arrow(x[i], y[i], (x[i+1] - x[i]), (y[i+1] - y[i]), head_width = 0,
                color = '#6699cc', length_includes_head = False)


    # Plot the overlay
    with open("/home/hussein/STDS_IU/SimulatedAnnealing_TSP/russia.json") as json_file:
        json_data = json.load(json_file)[0]
    coordinates = json_data['geojson']['coordinates']
    geo_coords = []
    x, y = [], []

    for list1 in coordinates:
        for list2 in list1:
            for item in list2:
                geo_coords.append(item)
                if item[0] < 0:
                    item[0] += 360
                x.append(item[0])
                y.append(item[1])

    ax.scatter(x, y)

    plt.show()


def plot_all(costs_list, cities, path, temps, alphas):

     # plot initializations
    gs = gridspec.GridSpec(3, 3, height_ratios=[3, 1, 3])
    gs.update(wspace=0.2, hspace=0.2)

    fig = plt.figure(figsize=(20, 13))
    ax1 = fig.add_subplot(gs[0:2, 0:2])  # Map
    ax2 = fig.add_subplot(gs[0, 2])  # Fitness function
    ax3 = fig.add_subplot(gs[2, 0:2])  # alpha
    ax4 = fig.add_subplot(gs[2, 2])  # temperature

    ax1.set_title('Map', fontsize=15)
    ax2.set_title('Fitness function', fontsize=15)
    ax3.set_title('acceptance probability', fontsize=15)
    ax4.set_title('temperature', fontsize=15)

    #####################################################################################
    # plot the cost function
    #####################################################################################
    costs_list = np.array(costs_list)
    # ax2.plot(costs_list / costs_list.max())
    from scipy.ndimage.filters import gaussian_filter1d
    x = [i for i in range(len(costs_list))]
    ysmoothed = gaussian_filter1d(costs_list, sigma=100)
    ax2.plot(x, ysmoothed)
    

    #####################################################################################
    # plot the map
    #####################################################################################
    x = []; y = []
    for city in path:
        coords = get_coords_by_idx(city, cities)
        y.append(coords[0])
        x.append(coords[1])

    ax1.plot(x, y, 'ro', ms=4)
    for city in path:
        coords = get_coords_by_idx(city, cities)
        ax1.text(x=coords[1], y=coords[0], s=get_name_by_idx(city, cities), color='black', size=6)

    ax1.arrow(x[-1], y[-1], (x[0] - x[-1]), (y[0] - y[-1]), head_width = 0,
            color ='g', length_includes_head=False)
    for i in range(0,len(x)-1):
        ax1.arrow(x[i], y[i], (x[i+1] - x[i]), (y[i+1] - y[i]), head_width = 0,
                color = 'g', length_includes_head = False)

    with open("/home/hussein/STDS_IU/SimulatedAnnealing_TSP/russia.json") as json_file:
        json_data = json.load(json_file)[0]
    coordinates = json_data['geojson']['coordinates']
    geo_coords = []
    x, y = [], []

    for list1 in coordinates:
        for list2 in list1:
            for item in list2:
                geo_coords.append(item)
                if item[0] < 0:
                    item[0] *= -1
                x.append(item[0])
                y.append(item[1])

    ax1.scatter(x, y, s=6)

    #####################################################################################
    # plot the temperature
    #####################################################################################
    temps = np.array(temps)
    ax4.plot(temps / temps.max())

    #####################################################################################
    # plot the acceptance probability
    #####################################################################################
    alphas = np.array(alphas)
    ax3.scatter([i for i in range(len(alphas))], alphas / alphas.max(), s = 8)

    plt.show()