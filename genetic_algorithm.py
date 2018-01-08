#!/usr/bin/python

import numpy as np

import math

c1 = [1, 1, 0, 0, 1, 1, 0, 0]

c2 = [1, 0, 1, 0, 1, 0, 1, 0]

def init_chromosome(len):
    """initialize a chromosome as a list of random 0 or 1 values"""
    c = []
    for i in range(len):
        if np.random.random() < 0.5:
            val = 0
        else:
            val = 1
        c.append(val)
    return c

def init_population(chromosome_length, population_length):
    """initialize a population as a list of chromosomes"""
    pop = []
    for i in range(population_length):
        pop.append(init_chromosome(chromosome_length))
    return pop

def mutate_punctual(c):
    """mutate a chromosome (list) of 0 or 1 values"""
    for i in range(len(c)):
        if np.random.random() < 0.1:
            c[i] = 1 - c[i]
    return c

def mutate_circular(c):
    """mutate a chromosome (list) as if it were a circular list"""
    if np.random.random() < 0.1:
        i = np.random.randint(len(c))
        c = c[i:] + c[0:i]
    return c

def mutate_by_crossover(c1,c2):
    """mutate two chromosomes by crossing over
    returns a tuple of chromosomes"""
    if np.random.random() < 0.1:
        i = np.random.randint(len(c1))
        j = np.random.randint(len(c2))
        print(i,j)
        c1_mutated = c1[0:i] + c2[i:]
        c2_mutated = c2[0:j] + c1[j:]
        return(c1_mutated,c2_mutated)
    else:
        return(c1,c2)

def mutate_population_by_crossover(sorted_population):
    l = len(sorted_population)
    index_good = np.random.randint(math.floor(float(l)/4.0))
    good_chromo = sorted_population[index_good]
    index_any = np.random.randint(l)
    any_chromo = sorted_population[index_any]
    return mutate_by_crossover(good_chromo,any_chromo)

def evoluate(population, times):
    """best if mutation rate decreases according to time cf. sigmoid function"""
    l = len(population)
    for i in range(times):
        crossover = list(mutate_population_by_crossover(population))
        population.append(crossover[0])
        population.append(crossover[1])
        for j in range(l):
            c = population[j]
            population.append(mutate_punctual(c))
            population.append(mutate_circular(c))
        population.sort(key=fitness)
        population = population[0:l] # limit population size
        print(population)

def chromosome_to_int(c):
    sum = 0
    for i in range(len(c)):
        sum += c[i] * 2**i
    return sum

def fitness(c):
    return(f(chromosome_to_int(c)))

def f(x):
    return((x*x) - 2)

def sigmoid(l, x):
    return(1 / (1 + math.exp(- l * x)))

def main():
    pop = init_population(5,50)
    evoluate(pop,100)

main()