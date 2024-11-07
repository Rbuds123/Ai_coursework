import numpy as np
import random as random

def initialize_population(pop_size, chromosome_length):
    """
    Initialize the population with random chromosomes.
    
    Args:
        pop_size (int): Number of individuals in the population.
        chromosome_length (int): Length of each chromosome.
    
    Returns:
        np.ndarray: Initialized population array.
    """
    return np.random.choice([0, 1], size=(pop_size, chromosome_length))    

def fitness(chromosome):
    """
    Calculate the fitness of a chromosome by comparing it to the target pattern.
    
    Args:
        chromosome (np.ndarray): The chromosome to evaluate.
    
    Returns:
        int: Fitness score.
    """
    target = [1] * 8 + [0] * 16 + [1] * 8
    # Calculate fitness by summing matches with the target pattern
    fitness_score = sum(
        1 for i in range(len(chromosome)) if chromosome[i] == target[i]
    )
    return fitness_score

def roulette_wheel_selection(population, fitnesses):
    """
    Select an individual from the population using roulette wheel selection.
    
    Args:
        population (np.ndarray): The current population.
        fitnesses (np.ndarray): Fitness scores of the population.
    
    Returns:
        np.ndarray: Selected parent chromosome.
    """
    min_fitness = np.min(fitnesses)
    if min_fitness < 0:
        fitnesses = fitnesses - min_fitness  # Shift all fitnesses to be non-negative

    total_fitness = np.sum(fitnesses)
    if total_fitness == 0:
        probabilities = np.ones(len(population)) / len(population)
    else:
        probabilities = fitnesses / total_fitness

    return population[np.random.choice(len(population), p=probabilities)]

def single_point_crossover(parent1, parent2):
    """
    Perform single point crossover between two parents.
    
    Args:
        parent1 (np.ndarray): First parent chromosome.
        parent2 (np.ndarray): Second parent chromosome.
    
    Returns:
        tuple: Two offspring chromosomes.
    """
    crossover_point = np.random.randint(1, len(parent1) - 1)
    offspring1 = np.concatenate([
        parent1[:crossover_point],
        parent2[crossover_point:]
    ])
    offspring2 = np.concatenate([
        parent2[:crossover_point],
        parent1[crossover_point:]
    ])
    return offspring1, offspring2

def mutate(chromosome, mutation_rate):
    """
    Mutate a chromosome based on the mutation rate.
    
    Args:
        chromosome (np.ndarray): The chromosome to mutate.
        mutation_rate (float): Probability of mutation for each gene.
    
    Returns:
        np.ndarray: Mutated chromosome.
    """
    mutation_mask = np.random.rand(len(chromosome)) < mutation_rate
    chromosome[mutation_mask] = 1 - chromosome[mutation_mask]
    return chromosome

def new_generation(population, mutation_rate):
    """
    Create a new generation from the current population.
    
    Args:
        population (np.ndarray): Current population.
        mutation_rate (float): Mutation rate.
    
    Returns:
        list: New population list.
    """
    new_pop = []
    fitnesses = [fitness(chromo) for chromo in population]
    for _ in range(len(population) // 2):
        parent1 = roulette_wheel_selection(population, fitnesses)
        parent2 = roulette_wheel_selection(population, fitnesses)
        offspring1, offspring2 = single_point_crossover(parent1, parent2)
        new_pop.extend([
            mutate(offspring1, mutation_rate),
            mutate(offspring2, mutation_rate)
        ])
    return new_pop

def genetic_algorithm(pop_size, chromosome_length, mutation_rate, generations):
    """
    Run the genetic algorithm.
    
    Args:
        pop_size (int): Population size.
        chromosome_length (int): Length of each chromosome.
        mutation_rate (float): Mutation rate.
        generations (int): Number of generations to run.
    
    Returns:
        tuple: Best solution and the generation it was found.
    """
    population = initialize_population(pop_size, chromosome_length)

    best_solution = None
    best_fitness = float('-inf')
    local_best_generation = -1

    for generation in range(generations):
        population = new_generation(population, mutation_rate)
        current_best_solution = max(population, key=fitness)
        current_best_fitness = fitness(current_best_solution)

        if current_best_fitness > best_fitness:
            best_fitness = current_best_fitness
            best_solution = current_best_solution
            local_best_generation = generation

        print(
            f"Generation {generation}, Best solution: {current_best_solution}, "
            f"Fitness: {current_best_fitness}"
        )

    print(
        f"Best solution found at generation {local_best_generation} with fitness {best_fitness}"
    )
    return best_solution, local_best_generation

best_local_solution, local_best_generation = genetic_algorithm(
    pop_size=100,
    chromosome_length=32,
    mutation_rate=0.1,
    generations=500
)
print(
    f"Best solution found: {best_local_solution} at generation {local_best_generation} "
    f"with a fitness of {fitness(best_local_solution)}"
)
