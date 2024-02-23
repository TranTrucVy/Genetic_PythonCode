import random
import time

# Define parameters
iterations = 5
population_size = 5
crossover_probability = 0.8
mutation_probability = 0.1
cities = 6
# Example distance matrix (replace it with your actual distance matrix)
distance_matrix = [
                    [0, 1930, 1484, 1096, 991, 1152],
                    [1930, 0, 684, 1091, 1211, 1582],
                    [1484, 684, 0, 459, 1427, 884],
                    [1096, 1091, 459, 0, 1046, 808],
                    [991, 1211, 1427, 1046, 0, 1619],
                    [1152, 1582, 884, 808, 1619, 0]
                ]
# '''
# Test với bộ data 74 thành phố
# '''
# # Mở file CSV
# with open('76_cities.csv', 'r') as file:
#     lines = file.readlines()
# # Tạo ma trận
# cities = len(lines)
# distance_matrix = [list(map(int, line.strip().split(','))) for line in lines]
# iterations = 100
# population_size = len(lines)

# def generate_probabilities():
#     """
#     Trả về một cặp (crossover_probability, mutation_probability) ngẫu nhiên.
#     """
#     crossover_probability = random.random()
#     mutation_probability = random.random()
#     return crossover_probability, mutation_probability

# Sử dụng hàm generate_probabilities
# crossover_probability, mutation_probability = generate_probabilities()
print("Input:")
print("Iterations:",iterations)
print("City:",cities)
print("Population size:",population_size)
print("Crossover Probability:", crossover_probability)
print("Mutation Probability:", mutation_probability)
print("Output:")

'''
Khởi tạo danh sách quần thể (population): danh sách này là một danh sách rỗng ([]).
for _ in range(population_size): sẽ lặp population_size lần.
Mỗi lần lặp, một cá thể mới (path) sẽ được tạo.
random.sample(range(1, cities + 1), cities): 
Sử dụng hàm random.sample để lấy ngẫu nhiên cities số từ khoảng từ 1 đến cities + 1. 
Điều này đảm bảo mỗi thành phố chỉ xuất hiện một lần trong đường đi, 
vì random.sample đảm bảo không có phần tử nào bị trùng lặp.
return population: Hàm trả về danh sách quần thể với population_size cá thể,
mỗi cá thể là một đường đi ngẫu nhiên.
  Individual 1: [3, 6, 5, 2, 4, 1], Length: 7385
  Individual 2: [5, 2, 3, 1, 6, 4], Length: 6385
  Individual 3: [4, 3, 1, 2, 6, 5], Length: 8120
  Individual 4: [2, 6, 5, 3, 4, 1], Length: 8113
  Individual 5: [1, 6, 3, 2, 5, 4], Length: 6073
'''
# Function to initialize a random population
# def initialize_population(population_size, cities):
#     population = []
#     for _ in range(population_size):
#         path = random.sample(range(1, cities + 1), cities)
#         population.append(path)
#     return population


def initialize_population(population_size, cities):
    population = []
    for _ in range(population_size):
        while True:
            path = random.sample(range(1, cities + 1), cities)
            if path not in population:
                population.append(path)
                break
    return population

'''
Giả sử ma trận này có kích thước NxN, trong đó N là số lượng thành phố. 
distance_matrix[i][j] chứa khoảng cách từ thành phố i đến thành phố j.
tour: đại diện cho một hành trình, một danh sách (list) trong Python.
len(tour): số lượng thành phố trong hành trình.
tour[i] và tour[(i + 1) % len(tour)]: 
Dùng để truy cập thành phố thứ i và thành phố tiếp theo trong hành trình. 
Dòng mã này xử lý trường hợp khi chúng ta đang ở thành phố cuối cùng và muốn quay lại thành phố đầu tiên. 
Dùng tour[(i + 1) % len(tour)] giúp xác định thành phố tiếp theo mà không phải lo lắng về vấn đề index out of range.
distance_matrix[tour[i] - 1][tour[(i + 1) % len(tour)] - 1]: 
Sử dụng để truy cập giá trị khoảng cách giữa thành phố tour[i] và thành phố tiếp theo tour[(i + 1) % len(tour)] 
trong ma trận khoảng cách. -1 được trừ đi để điều chỉnh vì index trong Python bắt đầu từ 0, 
trong khi số thứ tự của thành phố trong bài toán có thể bắt đầu từ 1.
total_length: Biến này tích lũy tổng chiều dài của hành trình khi duyệt qua từng cặp thành phố.
'''

# Function to calculate the total length of a tour
def tour_length(tour):
    total_length = 0
    for i in range(len(tour)):
        total_length += distance_matrix[tour[i] - 1][tour[(i + 1) % len(tour)] - 1]
    return total_length

'''
total_fitness = sum(fitness_values): 
Tính tổng fitness value của toàn bộ quần thể
cumulative_probabilities: 
Tính xác suất tích lũy cho mỗi cá thể trong quần thể.
random_number = random.random(): Tạo một số ngẫu nhiên trong khoảng từ 0 đến 1. 
Điều này sẽ được sử dụng để chọn ngẫu nhiên một cá thể từ quần thể.
Vòng lặp for i, probability in enumerate(cumulative_probabilities): 
Duyệt qua danh sách xác suất tích lũy.
if random_number <= probability: So sánh số ngẫu nhiên với giá trị xác suất tích lũy. 
Nếu số ngẫu nhiên nhỏ hơn hoặc bằng xác suất tích lũy của một cá thể cụ thể, thì cá thể đó được chọn làm cha mẹ.
return population[i]: Trả về cá thể được chọn làm cha mẹ. 
Cá thể này được chọn dựa trên xác suất, với xác suất cao hơn đối với những cá thể có sức khỏe cao hơn.
'''

# Function for parent selection using roulette wheel selection
def select_parent(population, fitness_values):
    total_fitness = sum(fitness_values)
    cumulative_probabilities = [sum(fitness_values[:i+1]) / total_fitness for i in range(len(fitness_values))]

    random_number = random.random()
    for i, probability in enumerate(cumulative_probabilities):
        if random_number <= probability:
            print(f"Selected parent index: {i}, Probability Distribution: {probability}")
            return population[i]
        

'''
if random.random() <= crossover_probability:
Nếu giá trị ngẫu nhiên nằm trong khoảng từ 0 đến xác suất lai ghép,
thì quá trình lai ghép sẽ được thực hiện.
crossover_point = random.randint(1, len(parent1) - 1)
Chọn một điểm cắt ngẫu nhiên trong chuỗi đường đi,
nằm trong khoảng từ 1 đến độ dài của chuỗi (loại bỏ điểm đầu tiên).
child1 = parent1[:crossover_point] + [city for city in parent2 if city not in parent1[:crossover_point]]
Tạo cá thể con thứ nhất (child1) bằng cách lấy một phần của cha mẹ 1 (parent1) đến điểm cắt 
và thêm vào các thành phố từ cha mẹ 2 (parent2) mà chưa xuất hiện trong phần đã chọn của cha mẹ 1.

child2 = parent2[:crossover_point] + [city for city in parent1 if city not in parent2[:crossover_point]]
Tạo cá thể con thứ hai (child2) tương tự như child1, nhưng lấy phần của cha mẹ 2 (parent2) 
đến điểm cắt và thêm vào các thành phố từ cha mẹ 1 (parent1) mà chưa xuất hiện trong phần đã chọn của cha mẹ 2.

child1 = fix_duplicates(child1, parent1) và child2 = fix_duplicates(child2, parent2): 
Gọi hàm fix_duplicates để kiểm tra và sửa chữa bất kỳ thành phố trùng lặp nào 
trong đường đi của các cá thể con. Điều này đảm bảo tính duy nhất của các thành phố trong đường đi của cá thể con.

return child1, child2: Trả về các cá thể con đã được tạo và kiểm tra. 
Nếu quá trình lai ghép không được thực hiện, thì trả về ngay hai cá thể cha mẹ.
'''
# Function for single-point crossover
# def crossover(parent1, parent2):
#     if random.random() <= crossover_probability:
#         crossover_point = random.randint(1, len(parent1) - 1)
#         child1 = parent1[:crossover_point] + [city for city in parent2 if city not in parent1[:crossover_point]]
#         child2 = parent2[:crossover_point] + [city for city in parent1 if city not in parent2[:crossover_point]]
#         return child1, child2
#     else:
#         return parent1, parent2
def crossover(parent1, parent2):
    if random.random() <= crossover_probability:
        crossover_point = random.randint(1, len(parent1) - 1)
        child1 = parent1[:crossover_point] + [city for city in parent2 if city not in parent1[:crossover_point]]
        child2 = parent2[:crossover_point] + [city for city in parent1 if city not in parent2[:crossover_point]]

        # Check for duplicates and correct them
        child1 = fix_duplicates(child1, parent1)
        child2 = fix_duplicates(child2, parent2)

        return child1, child2
    else:
        return parent1, parent2

'''
for i in range(len(child)): Duyệt qua từng thành phố trong đường đi của cá thể con (child).
if child.count(child[i]) > 1: Kiểm tra xem thành phố thứ i có xuất hiện nhiều hơn một lần trong đường đi hay không.
for city in parent:Duyệt qua từng thành phố trong đường đi của cha mẹ (parent).
if city not in child: Kiểm tra xem thành phố hiện đang xét từ cha mẹ có xuất hiện trong đường đi của cá thể con hay không.
child[i] = city: Nếu thành phố từ cha mẹ chưa xuất hiện trong đường đi của cá thể con, 
thì thay thế thành phố trùng lặp tại vị trí i trong child bằng thành phố từ cha mẹ.
return child: Trả về đường đi cá thể con đã được kiểm tra và sửa chữa.

khi có thành phố trùng lặp trong đường đi của cá thể con, 
nó sẽ được thay thế bằng các thành phố chưa xuất hiện từ cha mẹ, 
đảm bảo tính duy nhất của đường đi.
'''
def fix_duplicates(child, parent):
    # Replace duplicates in the child with cities from the parent
    for i in range(len(child)):
        if child.count(child[i]) > 1:
            for city in parent:
                if city not in child:
                    child[i] = city
                    break
    return child


'''
if random.random() <= mutation_probability:
Điều kiện kiểm tra xem có nên thực hiện đột biến hay không. 
Nếu random.random()<=mutation_probability, đột biến sẽ được thực hiện.
mutation_point1, mutation_point2 = random.sample(range(len(individual)), 2)
Chọn ngẫu nhiên hai điểm trong gen của cá thể để thực hiện đổi chỗ. 
random.sample(range(len(individual)), 2) 
một danh sách chứa hai chỉ mục ngẫu nhiên không trùng lặp từ 0 đến độ dài của cá thể (len(individual)).

individual[mutation_point1], individual[mutation_point2] = individual[mutation_point2], individual[mutation_point1]: 
Hoán đổi giá trị tại hai điểm đã chọn trong gen của cá thể.

return individual: Trả về cá thể đã trải qua đột biến.
'''
# Function for swap mutation
def mutate(individual):
    if random.random() <= mutation_probability:
        mutation_point1, mutation_point2 = random.sample(range(len(individual)), 2)
        individual[mutation_point1], individual[mutation_point2] = individual[mutation_point2], individual[mutation_point1]
    return individual

'''
combined_population = current_population + offspring_population
combined_population.sort(key=lambda x: tour_length(x)): 
Sắp xếp danh sách combined_population dựa trên chiều dài của đường đi (tour_length). 
Điều này có nghĩa là các cá thể có đường đi ngắn nhất sẽ nằm ở đầu danh sách.
return combined_population[:population_size]: 
Trả về một phần của danh sách đã sắp xếp, 
giữ lại chỉ population_size cá thể có đường đi ngắn nhất. 
Điều này thực hiện chiến lược "elitism", 
nơi chỉ những cá thể có hiệu suất tốt nhất được giữ lại trong quần thể mới.
'''
# Function for replacement using elitism (preserving the best individuals)
def replace_population(current_population, offspring_population):
    combined_population = current_population + offspring_population
    combined_population.sort(key=lambda x: tour_length(x))
    return combined_population[:population_size]

# Main genetic algorithm loop

start_time = time.time()

population = initialize_population(population_size, cities)

for iteration in range(iterations):
    print(f"Iteration {iteration + 1} - Population:")
    for i, individual in enumerate(population):
        print(f" Individual {i + 1}: {individual}, Length: {tour_length(individual)}")
    
    # Evaluate fitness of the population
    # thuật toán đánh giá fitness của từng cá thể trong quần thể bằng cách tính 
    # toán chiều dài của đường đi của chúng và lưu trữ các giá trị này trong danh sách fitness_values
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
    print(f"Best tour: {best_tour}, Length: {best_length}\n")

# Display the final best tour
final_best_tour = min(population, key=tour_length)
final_best_length = tour_length(final_best_tour)
print(f"Final Best Tour: {final_best_tour}, Length: {final_best_length}")

# Ghi lại thời điểm kết thúc
end_time = time.time()
# Tính thời gian chạy
execution_time = end_time - start_time
print(f"Thời gian chạy: {execution_time} giây")