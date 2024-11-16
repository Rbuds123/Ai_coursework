import numpy as np
import random
import tkinter as tk

# Given weights and values from the table
weights = [3, 8, 2, 9, 7, 1, 8, 13, 10, 9]  # in tonnes
profits = [126000, 154000, 256000, 526000, 388000, 245000, 210000, 442000, 671000, 348000]  
capacity = 35  # Lorry capacity in tonnes
num_items = len(profits)

# Define GA parameters
population_size = 100
generations = 200
crossover_rate = 0.8
mutation_rate = 0.02

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
def selection(population, fitnesses):
    total_fitness = np.sum(fitnesses)
    if total_fitness == 0:  # Prevent division by zero if all have zero fitness
        return random.choice(population), random.choice(population)
    probabilities = fitnesses / total_fitness
    parent1_idx, parent2_idx = np.random.choice(range(len(population)), size=2, p=probabilities, replace=False)
    return population[parent1_idx], population[parent2_idx]


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
    # Precompute fitness values for the current population
    fitnesses = np.array([fitness(chromosome) for chromosome in population])

    # Record best fitness of the current generation
    current_best = np.max(fitnesses)
    fitness_over_time.append(current_best)

    # Find and display the best chromosome in this generation
    best_chromosome = population[np.argmax(fitnesses)]
    #print(f"Generation {generation + 1}: Best Fitness = {current_best}")
    #print("Best Chromosome:", best_chromosome)

    # Create new population
    new_population = []
    for _ in range(population_size // 2):
        parent1, parent2 = selection(population, fitnesses)
        child1, child2 = crossover(parent1, parent2)
        new_population.append(mutate(child1))
        new_population.append(mutate(child2))
    population = new_population
    fitnesses = np.array([fitness(chromosome) for chromosome in population])

# Find the best solution in the final population
best_solution = max(population, key=fitness)
best_profit = fitness(best_solution)
total_weight = np.sum(best_solution * weights)

def draw_van_with_crates_color_coded():

    root = tk.Tk()
    root.title("Van Diagram")
    canvas = tk.Canvas(root, width=800, height=500, bg="white")
    canvas.pack()

    # Draw van parts
    canvas.create_rectangle(200, 150, 600, 300, outline="black", width=3, fill="#C0C0C0") 
    canvas.create_rectangle(600, 200, 700, 300, outline="black", width=3, fill="#A9A9A9")  
    canvas.create_oval(220, 290, 270, 330, fill="black") 
    canvas.create_oval(530, 290, 580, 330, fill="black") 
    canvas.create_oval(630, 290, 680, 330, fill="black") 


    canvas.create_text(400, 130, text="Van Loaded with Selected Crates", font=("Arial", 16))

    # Draw crates inside the van for selected items
    x_start, y_start = 210, 160  # Start position inside the van
    crate_width, crate_height = 50, 30
    gap = 10

    for i in range(num_items):
        if best_solution[i] == 1:  # Selected crates go inside the van
            canvas.create_rectangle(
                x_start, y_start, x_start + crate_width, y_start + crate_height,
                fill="green", outline="black"
            )
            # Label the crate with its number
            canvas.create_text(
                x_start + crate_width / 2, y_start + crate_height / 2,
                text=str(i + 1), font=("Arial", 10)
            )
            y_start += crate_height + gap
            if y_start + crate_height > 300:  # If crates go beyond van height, move to next column
                y_start = 160
                x_start += crate_width + gap

    # Draw unselected crates outside the van
    x_start, y_start = 50, 350  # Start position outside the van
    for i in range(num_items):
        if best_solution[i] == 0:  # Unselected crates go outside the van
            canvas.create_rectangle(
                x_start, y_start, x_start + crate_width, y_start + crate_height,
                fill="red", outline="black"
            )
            # Label the crate with its number
            canvas.create_text(
                x_start + crate_width / 2, y_start + crate_height / 2,
                text=str(i + 1), font=("Arial", 10)
            )
            x_start += crate_width + gap
            if x_start + crate_width > 750:  # If crates go beyond canvas width, move to next row
                x_start = 50
                y_start += crate_height + gap

    # Display total profit and weight
    canvas.create_text(400, 50, text=f"Total Profit: £{best_profit:,.2f}k", font=("Arial", 14), fill="blue")
    canvas.create_text(400, 80, text=f"Total Weight: {total_weight} tonnes", font=("Arial", 14), fill="blue")

    root.mainloop()


#print("\nOptimal Solution Summary:")
#print(f"Total Profit (in thousands of £): {best_profit}")
#print(f"Total Weight (in tonnes): {total_weight}")
#print("\nTable of Results:")
#print("Item Type | Weight (tonnes) | Profit | Selected")
#print("-------------------------------------------------------------")
#for i in range(num_items):
#    selected = "Yes" if best_solution[i] == 1 else "No"
#    print(f"{i+1:9} | {weights[i]:15} | {profits[i]:20} | {selected}")

# Show van diagram
draw_van_with_crates_color_coded()