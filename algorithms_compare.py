import numpy as np
import time

class AntColony:
    def __init__(self, distances, n_ants, decay=0.95):
        self.distances = distances
        self.pheromone = np.ones(self.distances.shape) / len(distances)
        self.all_inds = np.arange(len(distances))
        self.n_ants = n_ants
        self.decay = decay

    def run(self, n_iterations):
        all_time_best_path = None
        all_time_best_distance = float('inf')

        for i in range(n_iterations):
            paths = self.gen_all_paths()
            self.spread_pheromone(paths)
            self.pheromone *= self.decay
            self.intensify_pheromone(paths)
            self.pheromone *= self.decay

            current_best_path, current_best_distance = self.find_best_path(paths)

            if current_best_distance < all_time_best_distance:
                all_time_best_path = current_best_path
                all_time_best_distance = current_best_distance

        return all_time_best_path, all_time_best_distance

    def spread_pheromone(self, paths):
        delta_pheromone = np.zeros(self.pheromone.shape)

        for path in paths:
            contribution = 1 / len(path)
            for move in path:
                int_move = int(move)
                delta_pheromone[int_move] += contribution

        self.pheromone += delta_pheromone

    def intensify_pheromone(self, paths):
        evaporation = 1 - self.decay
        self.pheromone *= evaporation

        for path in paths:
            contribution = 1 / self.total_distance(path)
            for move in path:
                int_move = int(move)
                self.pheromone[int_move] += contribution

    def find_best_path(self, paths):
        best_path = None
        best_distance = float('inf')

        for path in paths:
            distance = self.total_distance(path)
            if distance < best_distance:
                best_distance = distance
                best_path = path

        return best_path, best_distance

    def total_distance(self, path):
        total_distance = 0
        for i in range(len(path) - 1):
            total_distance += self.distances[path[i], path[i + 1]]
        total_distance += self.distances[path[-1], path[0]]  # Connect back to the starting city
        return total_distance

    def gen_path_dist(self, path):
        distance = 0
        for move in path:
            distance += self.distances[move]
        return path, distance

    def gen_all_paths(self):
        all_paths = []
        for i in range(self.n_ants):
            path = self.gen_path_dist(np.random.permutation(self.all_inds))[0]
            all_paths.append(path)
        return all_paths

# Example Usage
if __name__ == "__main__":
    with open('76_cities.csv', 'r') as file:
        lines = file.readlines()
    distance_matrix = np.array([list(map(int, line.strip().split(','))) for line in lines])
    ants = 5
    # Number of iterations
    n_iterations = 100
    start_time = time.time()
    ant_colony = AntColony(distance_matrix, ants)

    best_path, min_distance = ant_colony.run(n_iterations)
    end_time = time.time()
    # Calculate the total execution time
    execution_time = end_time - start_time
    
    print("Best Path:", best_path)
    print("Minimum Distance:", min_distance)
    print(f"Runtime: {execution_time} seconds")
