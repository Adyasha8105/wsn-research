## Find forwarder
# Symbols used
# Notation Description 
# N Number of sensors 
# n Number of node in forward area
# R Transmission range 
# rk kth route
# Tk End-to-end delay of kth route 
# FZ Forward zone
# Ek Energy consumption of kth route 
# Rz Forward zone radius
# Pc (l), Connectivity probability 
# Ci A ith chromosome (path)
# Ed(y) Expected distance 
# E(Fi) Fitness function for energy consumption
# E(tcost). Expected computational cost 
# Etrans Transmission energy
# E(Etotal) Expected energy consumption
# Erec Receiving energy
# φ Density of sensors 
# PSD Probability of success delivery

import sys
from math import e, factorial

import random

from torch import randint
from forward_zone_coord import *
from plotting import *

def gen_coord(s, d): 
    """
    Generate random coordinates which represent
    the location of sensor nodes scattered around
    """
    smallest_x = s[0]
    greatest_x = d[0]
    smallest_y = s[1]
    greatest_y = d[1]
    if s[0] > d[0]: 
        smallest_x = d[0]
        greatest_x = s[0]
    if s[1] > d[1]: 
        smallest_y = d[1]
        greatest_y = s[1]

    x = random.uniform(smallest_x, greatest_x)
    y = random.uniform(smallest_y, greatest_y)
    return (int(x), int(y))    

def gen_random_coords(s, d, n):
    """
    Compiles the randomly generated coordinates
    """
    coord = []
    while True:
        if len(coord) == n: 
            break
        new_coord = gen_coord(s, d)
        if new_coord not in coord:
            coord.append(gen_coord(s, d))
        else:
            pass
    return coord

def calc_dist(x, y): 
    """
    Calculate the distance between two sensor nodes
    """
    return ((x[0]-y[0])**2 + (x[1]-y[1])**2)**0.5

def count_nodes_inside_forward_zone(coord, forward_zone):
    """
    Return the number of nodes inside the forward zone
    """
    count = 0
    for i in range(len(coord)): 
        if inside_polygon(forward_zone, coord[i]):
            count = count + 1
    return count

def find_forwarder(s, d, r, coord, forward_zone): 
    """
    Find the forwarder node
    """
    forwarder_list = []
    forwarder_node = ()
    for i in coord: 
        # the condition for finding the next best node for the path
        if calc_dist(s, i) <= r and (calc_dist(i, d) < calc_dist(s, d)) and inside_polygon(forward_zone, i):
            forwarder_list.append(i)
    if d in forwarder_list or len(forwarder_list) == 0:
        forwarder_node = d
    else: 
        forwarder_node = random.choice(forwarder_list)
    return forwarder_node

def chromosome_form(s, d, r, coord, forward_zone):
    """
    Generate a path for transmission of signal
    """
    chromosome = []
    chromosome.append(s)
    # creating a path
    # adding nodes to an array (the path) till the destination node is reached
    while s != d: 
        c2 = find_forwarder(s, d, r, coord, forward_zone)
        if c2 == ():
            break
        chromosome.append(c2)
        s = c2
    return chromosome

def population_form(s, d, r, coord, p, forward_zone):
    """
    Generate a population of paths
    """
    population = []
    for i in range(p):
        path = chromosome_form(s, d, r, coord, forward_zone)
        in_range = calc_dist(path[-2], d) <= r
        if in_range == False:
            return False
        else: 
            population.append(path)

    return population

def calc_fitness(path):
    """
    Calculate and return the fitness of each path
    """
    # energy dissipated to run the transmitter
    elec = 50
    # energy required to for transmit amplifier
    amp = 100
    # value usually lies between the range of 2 to 4
    phi = 2
    # bits of data to be transferred
    k = 512
    # number of links along the route from S to D
    hc = len(path) - 1
    total_energy = 0
    
    for i in range(len(path) - 1):
        current_energy = (2 * elec * amp * (calc_dist(path[i], path[i + 1]) ** phi)) * k * hc
        total_energy = total_energy + current_energy
    
    return total_energy

def forward_zone_probability(n, r, d):
    """
    Calculate and return the probability of n nodes in forward zone
    """
    phi = 2 
    area = 2 * r * d
    probability = ((phi * area) ** 34) / (factorial(n) * (phi ** n))
    return probability

def run_simulation(): 
    n = 200
    s = (5, 8)
    d = (23, 32)
    r = 4
    coord = gen_random_coords(s, d, n)
    
    # defines the forward zone
    forward_zone = point_of_intersection(r, s, d)
    # one of the possilble paths to go from S to D
    chromosome_path = chromosome_form(s, d, r, coord, forward_zone)
    # generate the initial population for crossover
    population = population_form(s, d, r, coord, 60, forward_zone)
    while(population == False):
        coord = gen_random_coords(s, d, n)
        population = population_form(s, d, r, coord, 60, forward_zone)

    optimal = []
    optimal_fitness = sys.maxsize
    for i in range(len(population)):
        fitness_value = calc_fitness(population[i])
        if fitness_value < optimal_fitness: 
            optimal_fitness = fitness_value
            optimal = population[i]
    
    print("The optimal path:")
    print(optimal)
    node_simulation(coord, s, d, r, optimal, population, forward_zone)
    # forward_zone_simulation(coord, s, d, r, forward_zone)
    
run_simulation()