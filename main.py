import os, math, time, threading, pprint, copy, random
from Graph import Point
from draw_graph import main_draw
from alghorithms import find_eulerian_path, find_hamiltonian_cycle
from tqdm import tqdm

UI = False
do_generate = True


def get_data_from_file(file_name='euler.txt'):
    result = ''
    file_path = os.path.join(os.getcwd(), file_name)
    try:
        with open(file_path) as f:
            result = f.read()
    except:
        pass
    return result


def convert_data(data):
    data_list = list(filter(lambda el: el == '0' or el == '1', list(data)))
    data_list = list(map(lambda el: bool(int(el)), list(data_list)))
    trans = []
    d_sqrt_len = int(math.sqrt(len(data_list)))
    for i in range(d_sqrt_len):
        to_append = []
        # for j in range(i):
        #     a = False
        #     to_append.append(a)
        # to_append.extend(data_list[i*d_sqrt_len + i:i*d_sqrt_len + d_sqrt_len])
        to_append.extend(data_list[i*d_sqrt_len:i*d_sqrt_len + d_sqrt_len])
        trans.append(to_append)
    data_list = trans
    points = []
    for i in range(len(data_list)):
        points.append(Point(data_list[i], str(i+1)))
    return points


def connect_points(points):
    for point in points:
        for i, connection in enumerate(point.connections):
            if connection:
                point.connections[i] = points[i]
        point.connections = list(filter(lambda a: type(a) == Point, point.connections))
    return points


def measure_time(fun_to_measure, *args):
    s_time = time.time_ns()
    fun_to_measure(args[0])
    return time.time_ns() - s_time


def main():
    files = []
    if do_generate:
        for i in tqdm(range(10, 41, 2)):
            files.append(generate_graph(i, 0.5))
        # for i in tqdm(range(10, 41, 2)):
        #     files.append(generate_graph(i, 0.3))
    else:
        files.append("euler.txt")
        files.append("euler copy.txt")
    all_data = []
    for file in files:
        data = get_data_from_file(file)
        if data == '':
            print(f'[ERROR] DATA FILE {file} ERROR [ERROR]')
            continue
        all_data.append(connect_points(convert_data(data)))
    if len(all_data) > 0:
        if UI:
            solve_euler_th = threading.Thread(target=solve_euler, args=[all_data], daemon=True)
            solve_euler_th.start()
            main_draw(all_data)
        else:
            solve_euler(all_data)


def generate_graph(size=4, max_percentage=1):
    result = ["1"] * int((size * (size - 1)) / 2 * max_percentage)
    for i in range(int((size * (size - 1)) / 2 * (1 - max_percentage))):
        result.insert(random.randint(0, len(result) - 1), "0")
    ret_result = [[0 for _ in range(size)] for _ in range(size)]
    r_id = 0
    while len(result) < (size * (size - 1) / 2):
        result.append("0")
    for i in range(size):
        for j in range(i + 1, size):
            ret_result[i][j] = result[r_id]
            r_id += 1
    
    for i in range(len(ret_result)):
        for j in range(len(ret_result[i])):
            ret_result[j][i] = ret_result[i][j]

    file_name = f"{size}x{size}-{str(max_percentage*100)}.txt"
    with open(os.path.join(os.getcwd(), file_name), "w") as f:
        for l in ret_result:
            f.write(str(l))
    return file_name



# def generate_graph(size=4, max_percentage=1.0):
#     # Создаём пустую матрицу смежности
#     matrix = [[0 for _ in range(size)] for _ in range(size)]

#     # Шаг 1: создаём цикл, проходящий по всем вершинам (гамильтонов цикл)
#     nodes = list(range(size))
#     random.shuffle(nodes)
#     for i in range(size):
#         a = nodes[i]
#         b = nodes[(i + 1) % size]
#         matrix[a][b] = matrix[b][a] = 1

#     # Шаг 2: добавим рёбра, пока не достигнем нужной плотности и все степени — чётные
#     def current_edge_count():
#         return sum(sum(row) for row in matrix) // 2

#     max_edges = int((size * (size - 1)) / 2 * max_percentage)

#     while current_edge_count() < max_edges:
#         a, b = random.sample(range(size), 2)
#         if matrix[a][b] == 0:
#             matrix[a][b] = matrix[b][a] = 1

#             # проверка: все степени должны быть чётными
#             degrees = [sum(row) for row in matrix]
#             if any(d % 2 != 0 for d in degrees):
#                 # отменить добавление ребра
#                 matrix[a][b] = matrix[b][a] = 0

#     # Проверка на связность (DFS)
#     def is_connected(matrix):
#         visited = set()
#         def dfs(v):
#             visited.add(v)
#             for u, edge in enumerate(matrix[v]):
#                 if edge == 1 and u not in visited:
#                     dfs(u)
#         dfs(0)
#         return len(visited) == size

#     if not is_connected(matrix):
#         return generate_eulerian_hamiltonian_graph(size, max_percentage)

#     # Запись в файл
#     file_name = f"{size}x{size}-{int(max_percentage*100)}.txt"
#     with open(os.path.join(os.getcwd(), file_name), "w") as f:
#         for row in matrix:
#             f.write(" ".join(map(str, row)) + "\n")
    
#     return file_name


def solve_euler(all_graphs):
    all_graphs_state = copy.deepcopy(all_graphs)
    results = [["" for _ in range(3)]  for _ in range(31)]
    for g_id, graph in enumerate(all_graphs):
        results[g_id + 1][0] = f'{len(graph)}x{len(graph)}'
        results[g_id + 1][1] = measure_time(find_eulerian_path, graph)
        results[g_id + 1][2] = measure_time(find_hamiltonian_cycle, graph)
        print(measure_time(find_hamiltonian_cycle, graph))
    results[0] = ['SIZE', 'EULER', 'HAMILTON']
    pprint.pprint(results)

if __name__ == '__main__':
    id = int(round(time.time(), 0))
    func_var = main
    print(f'[INFO] {func_var.__name__} WITH ID {id} --START-- [INFO]')
    func_var()
    print(f'[INFO] {func_var.__name__} WITH ID {id} ---END--- [INFO]')