def find_hamiltonian_cycle(points):
    n = len(points)
    name_to_point = {p.name: p for p in points}
    visited = set()
    path = []

    def backtrack(current, depth):
        path.append(current.name)
        visited.add(current.name)

        if depth == n:
            if path[0] in [connection.name for connection in current.connections]:
                path.append(path[0])
                return True
            else:
                visited.remove(current.name)
                path.pop()
                return False

        for connection in current.connections:
            if connection.name not in visited:
                if backtrack(connection, depth + 1):
                    return True

        visited.remove(current.name)
        path.pop()
        return False

    for start_point in points:
        visited.clear()
        path.clear()
        if backtrack(start_point, 1):
            return path

    return None 



def find_eulerian_path(points):
    from collections import defaultdict

    graph = defaultdict(list)
    for point in points:
        for connection in point.connections:
            graph[point.name].append(connection.name)

    for node in graph:
        if len(graph[node]) % 2 != 0:
            return None 

    stack = []
    circuit = []
    current = points[0].name 

    while stack or graph[current]:
        if not graph[current]:
            circuit.append(current)
            current = stack.pop()
        else:
            stack.append(current)
            connection = graph[current].pop()
            graph[connection].remove(current) 
            current = connection

    circuit.append(current)
    return circuit[::-1]
