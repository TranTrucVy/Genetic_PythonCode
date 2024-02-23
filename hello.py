import csv
import itertools

def load_matrix_from_csv(file_path):
    matrix = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            row_values = [int(cell) for cell in row[0].split(',')]
            matrix.append(row_values)
    return matrix

def calculate_total_distance(path, distance_matrix):
    total_distance = 0
    for i in range(len(path)):
        if i == len(path) - 2:
            break
        total_distance += distance_matrix[path[i]][path[i + 1]]
    total_distance += distance_matrix[path[-1]][path[0]]  # Connect back to the starting city
    return total_distance

def tsp_bruteforce(distance_matrix):
    cities = len(distance_matrix)
    all_permutations = itertools.permutations(range(cities))

    min_distance = float('inf')
    best_path = None

    for path in all_permutations:
        distance = calculate_total_distance(path, distance_matrix)
        if distance < min_distance:
            min_distance = distance
            best_path = path

    return best_path, min_distance

if __name__ == "__main__":
    file_path = 'test.csv'  # Replace with the actual path to your CSV file
    distance_matrix = load_matrix_from_csv(file_path)

    best_path, min_distance = tsp_bruteforce(distance_matrix)

    print("Best Path:", best_path)
    print("Minimum Distance:", min_distance)
