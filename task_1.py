import numpy as np
import tkinter as tk

def initialize_population(pop_size, chromosome_length):
    return np.random.choice([0, 1], size=(pop_size, chromosome_length))

def fitness(chromosome):
    # gene slicing is used to split the chromosome into 3 parts
    chromosome_1 = chromosome[:8]
    chromosome_2 = chromosome[8:24]
    chromosome_3 = chromosome[24:32]
    #we then add the sum of the first and third part and subtract the sum of the second part to get the fitness value and the maximization of 1s in the chromosome and the minimization of 0s in the chromosome
    Part_1 = np.sum(chromosome_1) + np.sum(chromosome_3)
    part_2 = np.sum(chromosome_2)
    
    return Part_1 - part_2

def roulette_wheel_selection(population, fitnesses):
    """
    Perform roulette wheel selection on a population based on their fitnesses.
    Parameters:
    population (list): A list of individuals in the population.
    fitnesses (numpy.ndarray): An array of fitness values corresponding to each individual in the population.
    Returns:
    individual: A selected individual from the population based on their fitness probabilities.
    Notes:
    - If any fitness value is negative, the fitnesses are adjusted by adding the absolute value of the minimum fitness to all fitness values.
    - If the total fitness is zero, each individual is assigned an equal probability of being selected.
    - The selection is done using numpy's random choice function with the calculated probabilities.
    """
    min_fitness = np.min(fitnesses)
    if min_fitness < 0:
        fitnesses = fitnesses - min_fitness

    total_fitness = np.sum(fitnesses)
    if total_fitness == 0:
        probabilities = np.ones(len(population)) / len(population)
    else:
        probabilities = fitnesses / total_fitness

    return population[np.random.choice(len(population), p=probabilities)]

def single_point_crossover(parent1, parent2):
    """
    Perform a single-point crossover between two parent arrays to generate two offspring arrays.

    Parameters:
    parent1 (numpy.ndarray): The first parent array.
    parent2 (numpy.ndarray): The second parent array.

    Returns:
    tuple: A tuple containing two offspring arrays resulting from the crossover.
    """
    crossover_point = np.random.randint(1, len(parent1) - 1)
    offspring1 = np.concatenate([parent1[:crossover_point], parent2[crossover_point:]])
    offspring2 = np.concatenate([parent2[:crossover_point], parent1[crossover_point:]])
    return offspring1, offspring2

def mutate(chromosome, mutation_rate):
    """
    Perform mutation on a chromosome based on the mutation rate.

    Args:
        chromosome (numpy.ndarray): The chromosome to mutate.
        mutation_rate (float): The probability of each gene being mutated.

    Returns:
        numpy.ndarray: The mutated chromosome.
    """
    mutation_mask = np.random.rand(len(chromosome)) < mutation_rate
    chromosome[mutation_mask] = 1 - chromosome[mutation_mask]
    return chromosome

def new_generation(population, mutation_rate):
    new_pop = []
    fitnesses = [fitness(chromo) for chromo in population]
    for _ in range(len(population) // 2):
        parent1 = roulette_wheel_selection(population, fitnesses)
        parent2 = roulette_wheel_selection(population, fitnesses)
        offspring1, offspring2 = single_point_crossover(parent1, parent2)
        new_pop.extend([mutate(offspring1, mutation_rate), mutate(offspring2, mutation_rate)])
    return new_pop

class GAApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Genetic Algorithm Visualization")
        
        self.canvas = tk.Canvas(root, width=320, height=160)
        self.canvas.pack()
        
        self.info_label = tk.Label(root, text="Best Fitness: 0, Generation: 0")
        self.info_label.pack()
        #initialize the intended parts of the chromosome
        self.chromosome_length = 32
        self.population_size = 100
        self.mutation_rate = 0.01
        self.generation = 0
        self.best_fitness = float('-inf')
        self.best_solution = None
        
        self.population = initialize_population(self.population_size, self.chromosome_length)
        self.current_chromosome = self.population[0]
        self.draw_grid(self.current_chromosome)

# Create a button to generate the next generation 
# this is done to show initial population as their was a bug with the program not showing the intial population leading to the chromosome acting like their was a bias in the program
        self.generate_button = tk.Button(self.root, text="Generate", command=self.generate)
        self.generate_button.pack()

        print(f"Generation {self.generation}: Initial Population")
        print(f"chromosome: {self.current_chromosome}")
        self.print_chromosome()

    def draw_grid(self, chromosome):
        self.canvas.delete("all")
        for i in range(4):
            for j in range(8):
                color = "blue" if chromosome[i + j * 4] == 1 else "green"
                self.canvas.create_rectangle(j * 40, i * 40, (j + 1) * 40, (i + 1) * 40, fill=color)
                self.canvas.create_rectangle(j * 40, i * 40, (j + 1) * 40, (i + 1) * 40, fill=color)
    
    def generate(self):
        if self.generation >= 100 or self.best_fitness == self.chromosome_length // 2:  # Stop after 100 generations or if the fitness is half the chromosome length
            return
#increment the generation by 1 and create a new generation of the population
        self.generation += 1
        self.population = new_generation(self.population, self.mutation_rate)
        current_best_solution = max(self.population, key=fitness)
        current_best_fitness = fitness(current_best_solution)
#update the best fitness and best solution if the current best fitness is greater than the best fitness
        if current_best_fitness > self.best_fitness:
            self.best_fitness = current_best_fitness
            self.best_solution = current_best_solution

        print(f"Generation {self.generation}: Best Fitness: {self.best_fitness} Chromosome: {current_best_solution}")

        self.current_chromosome = current_best_solution
        self.draw_grid(self.current_chromosome)
        self.info_label.config(text=f"Best Fitness: {self.best_fitness}, Generation: {self.generation}")
        self.print_chromosome()

        
        self.root.after(500, self.generate)

    def print_chromosome(self):
        return self.generation, self.current_chromosome
            
if __name__ == "__main__":
    root = tk.Tk()
    app = GAApp(root)
    root.mainloop()