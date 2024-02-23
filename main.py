import time
from genetic_algorithm import *

if checkFile == False:
    print("File doesn't exist!")
else:
    # Print input parameters and probabilities
    print("Input:")
    print("Iterations:", iterations)
    print("City:", cities)
    print("Population size:", population_size)
    print("Crossover Probability:", crossover_probability)
    print("Mutation Probability:", mutation_probability)
    print("Output:")

    # Main genetic algorithm loop
    population = initialize_population(population_size, cities)

    start_time = time.time()

    for iteration in range(iterations):
        # print(f"Iteration {iteration + 1} - Population:")
        # for i, individual in enumerate(population):
            # print(f" Individual {i + 1}: {individual}, Length: {tour_length(individual)}")

        # Evaluate fitness of the population
        fitness_values = [tour_length(individual) for individual in population]

        # Parent selection
        parents = [select_parent(population, fitness_values) for _ in range(population_size)]

        # Reproduction (Crossover and Mutation)
        offspring_population = []
        for i in range(0, population_size - 1, 2):
            parent1 = parents[i]
            parent2 = parents[i + 1]

            # Crossover
            child1, child2 = crossover(parent1, parent2)
            # Mutation
            child1 = mutate(child1)
            child2 = mutate(child2)

            offspring_population.extend([child1, child2])

        # Replacement
        population = replace_population(population, offspring_population)
        # Display the best tour in the current population
        best_tour = min(population, key=tour_length)
        best_length = tour_length(best_tour)
        # print(f"Best tour: {best_tour}, Length: {best_length}\n")

    # Display the final best tour
    final_best_tour = min(population, key=tour_length)
    final_best_length = tour_length(final_best_tour)
    print(f"Final Best Tour: {final_best_tour}, Length: {final_best_length}")

    # Record the end time
    end_time = time.time()
    # Calculate the total execution time
    execution_time = end_time - start_time
    print(f"Runtime: {execution_time} seconds")