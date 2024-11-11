import numpy as np
import random

# Given weights and values from the table
weights = [3, 8, 2, 9, 7, 1, 8, 13, 10, 9]  # in tonnes
profits = [126, 154, 256, 526, 388, 245, 210, 442, 671, 348]  # in thousands of £
capacity = 35  # Lorry capacity in tonnes
num_items = len(profits)

# Define GA parameters
population_size = 50
generations = 1000
crossover_rate = 0.8
mutation_rate = 0.01

# Generate initial population (random binary strings)
def generate_population(size):
    return [np.random.randint(2, size=num_items) for _ in range(size)]

# Fitness function: calculates profit if within weight limit, else penalizes
def fitness(chromosome):
    total_weight = np.sum(chromosome * weights)
    total_profit = np.sum(chromosome * profits)
    if total_weight > capacity:
        return 0  # Penalize if over capacity
    return total_profit

# Selection: Choose parents based on fitness (roulette wheel selection)
def selection(population):
    fitnesses = np.array([fitness(chromosome) for chromosome in population])
    total_fitness = np.sum(fitnesses)
    if total_fitness == 0:  # Prevent division by zero if all have zero fitness
        return random.choice(population), random.choice(population)
    probabilities = fitnesses / total_fitness
    parent1, parent2 = np.random.choice(range(len(population)), size=2, p=probabilities, replace=False)
    parent1, parent2 = population[parent1], population[parent2]
    return parent1, parent2

# Crossover: Single-point crossover
def crossover(parent1, parent2):
    if random.random() < crossover_rate:
        point = random.randint(1, num_items - 1)
        child1 = np.concatenate((parent1[:point], parent2[point:]))
        child2 = np.concatenate((parent2[:point], parent1[point:]))
        return child1, child2
    return parent1, parent2

# Mutation: Flip bits with a given probability
def mutate(chromosome):
    for i in range(num_items):
        if random.random() < mutation_rate:
            chromosome[i] = 1 - chromosome[i]  # Flip bit
    return chromosome

# GA Main Loop
population = generate_population(population_size)
fitness_over_time = []

for generation in range(generations):
    # Record best fitness of the current generation
    current_best = max([fitness(chromosome) for chromosome in population])
    fitness_over_time.append(current_best)
    
    # Create new population
    new_population = []
    for _ in range(population_size // 2):
        parent1, parent2 = selection(population)
        child1, child2 = crossover(parent1, parent2)
        new_population.append(mutate(child1))
        new_population.append(mutate(child2))
    population = new_population

# Find the best solution in the final population
best_solution = max(population, key=fitness)
best_profit = fitness(best_solution)
total_weight = np.sum(best_solution * weights)

# Display final results
print("Optimal Solution Summary:")
print(f"Total Profit (in thousands of £): {best_profit}")
print(f"Total Weight (in tonnes): {total_weight}")
print("\nTable of Results:")
print("Item Type | Weight (tonnes) | Profit (thousands £) | Selected")
print("-------------------------------------------------------------")
for i in range(num_items):
    selected = "Yes" if best_solution[i] == 1 else "No"
    print(f"{i+1:9} | {weights[i]:15} | {profits[i]:20} | {selected}")

