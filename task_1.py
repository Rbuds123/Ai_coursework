import numpy as np
import tkinter as tk

def initialize_population(pop_size, chromosome_length):
    return np.random.choice([0, 1], size=(pop_size, chromosome_length))

def fitness(chromosome):
    chromosome_1 = chromosome[:8]
    chromosome_2 = chromosome[8:24]
    chromosome_3 = chromosome[24:32]
    
    Part_1 = np.sum(chromosome_1) + np.sum(chromosome_3)
    part_2 = np.sum(chromosome_2)
    
    return Part_1 - part_2

def roulette_wheel_selection(population, fitnesses):
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
    crossover_point = np.random.randint(1, len(parent1) - 1)
    offspring1 = np.concatenate([parent1[:crossover_point], parent2[crossover_point:]])
    offspring2 = np.concatenate([parent2[:crossover_point], parent1[crossover_point:]])
    return offspring1, offspring2

def mutate(chromosome, mutation_rate):
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
        
        self.chromosome_length = 32
        self.population_size = 100
        self.mutation_rate = 0.01
        self.generation = 0
        self.best_fitness = float('-inf')
        self.best_solution = None
        
        self.population = initialize_population(self.population_size, self.chromosome_length)
        self.current_chromosome = self.population[0]
        self.draw_grid(self.current_chromosome)

        # Start the auto-loop
        self.generate()

        # Add this to your GUI setup code to create the generate button
        self.generate_button = tk.Button(self.root, text="Generate", command=self.generate)
        self.generate_button.pack()

    def draw_grid(self, chromosome):
        self.canvas.delete("all")
        for i in range(4):
            for j in range(8):
                color = "blue" if chromosome[i * 8 + j] == 1 else "green"
                self.canvas.create_rectangle(j * 40, i * 40, (j + 1) * 40, (i + 1) * 40, fill=color)
    
    def generate(self):
        if self.generation >= 100:  # Stop after 100 generations
            return

        self.generation += 1
        self.population = new_generation(self.population, self.mutation_rate)
        current_best_solution = max(self.population, key=fitness)
        current_best_fitness = fitness(current_best_solution)

        if current_best_fitness > self.best_fitness:
            self.best_fitness = current_best_fitness
            self.best_solution = current_best_solution

        print(f"Generation {self.generation}: Best Fitness: {self.best_fitness}")

        self.current_chromosome = current_best_solution
        self.draw_grid(self.current_chromosome)
        self.info_label.config(text=f"Best Fitness: {self.best_fitness}, Generation: {self.generation}")
        self.print_chromosome()

        #self.root.after(500, self.generate)
    
    def print_chromosome(self):
        print(f"Generation {self.generation}: Chromosome: {self.current_chromosome}")
        
if __name__ == "__main__":
    root = tk.Tk()
    app = GAApp(root)
    root.mainloop()