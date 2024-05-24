from random import getrandbits, randint, choice
import random as ran
import math

## Parameters
POP_SIZE = 4
MUT_RATE = 0.1
GENES_SIZE = 8
DOMAIN = [0, 128]

## Fitness function
def fitness_function(x):
    return x**2 + 5*x - 5

## Binary to decimal
def convertion_value(chromosome):
    i = 5
    n = 0
    for gene in chromosome:
      if(gene != 0):
        n += 2**i
      i = i - 1
    return n

## Chromosomes
def create_chromosomes():
    return [getrandbits(1) for x in range(GENES_SIZE)]

## Initial population
def initialize_population():
    population = []
    for item in range(POP_SIZE):
        chromosome = create_chromosomes()
        value = convertion_value(chromosome)
        if(value > DOMAIN[1]):
          while(value > 128):
            chromosome = create_chromosomes()
            value = convertion_value(chromosome)
        population.append(chromosome)

    return population

## X values
def get_x_values(population):
    values = []
    for chromosome in population:
      values.append(convertion_value(chromosome))

    return values

## Fitness vector
def get_chromo_fitness(population):
    chromosomes_fitness = []
    for chromosome in population:
      x = convertion_value(chromosome)
      chromosomes_fitness.append(fitness_function(x))
    return chromosomes_fitness

## Relatives fitness
def get_rel_fitness(population):
    relatives_fitness = []
    chromosome_fitness = get_chromo_fitness(population)
    for c_fitness in chromosome_fitness:
        relatives_fitness.append(math.floor((c_fitness / sum(population)) * 100))
    return relatives_fitness

## Fitness sum
def sum(population):
    sum = 0
    for chromosome in population:
      x = convertion_value(chromosome)
      sum += fitness_function(x)

    return sum

## Intervals matrix
def intervals_generator(population):
    numbers = []
    intervals = []
    count = 0

    for i in get_rel_fitness(population):
      numbers.append(i)

    for i in range(POP_SIZE):
      count += numbers[i]
      if(i == 0):
        intervals.append([0, numbers[i]])
      elif(i == POP_SIZE - 1):
        intervals.append([intervals[i - 1][1], 100])
      else:
        intervals.append([intervals[i - 1][1], count])

    return intervals

def select_chain(population, item):
      intervals = intervals_generator(population)
      selected = []
      j = 0

      for i in intervals:
          if(item > i[0] and i[1] > item):
              selected.append(population[j])
          j = j + 1
      return selected

## Roulette selection
def roulette_selection(population, chromossomes):
    selected = []
    for item in chromossomes:
        chain = select_chain(population, item)
        selected.append(chain)
    return selected

## Crossover
def crossover_function(population, selected, points):

    for j in selected: # [1,3], [2,4]
      mother = population[j[0]]
      father = population[j[1]]
      for i in range(points[0], points[1]):
          population[j[0]][i] = father[i]
          population[j[1]][i] = mother[i]

    return population

## Mutation
def mutation_function(population, selected):
    position = randint(0, 5)
    for i in selected:
      value = ran.random()
      if(value <= MUT_RATE):
        if(population[i][position] == 0):
            population[i][position] = 1
        elif(population[i][position] == 1):
            population[i][position] = 0
    return population

def genetic_algorithm():
    population = initialize_population()
    print(population)
    print(get_x_values(population))
    print(get_rel_fitness(population))
    print(get_rel_fitness(population))
    print(roulette_selection(population, [12, 37, 78, 92]))
    population = crossover_function(population, [[0, 2], [1,3]], [2, 4])
    print(population)
    population = mutation_function(population, [1, 3])
    print(population)

genetic_algorithm()