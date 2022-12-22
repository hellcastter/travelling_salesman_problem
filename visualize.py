from typing import List

from main import calc_path_distance, exact_tsp, genetic, nna, read_csv

def convert_to_dot(graph: List[List[int]]):
    """
    Creates graph.gv file and writes graph there
    """
    result = 'digraph {\n'

    route_exact = exact_tsp(graph)
    print("route_exact", calc_path_distance([i - 1 for i in route_exact[1:-1]], graph))

    route_nna = nna(graph)
    print("route_nna", calc_path_distance([i - 1 for i in route_nna[1:-1]], graph))

    route_genetic = genetic(graph)
    print("route_genetic", calc_path_distance([i - 1 for i in route_genetic[1:-1]], graph))

    for index, row in enumerate(graph):
        for j in range(index, len(graph)):
            col = row[j]

            if col not in (0, float('inf')):
                result += f'\t{index} -> {j} [weight={col}][dir="both"]\n'

    for route, color in zip([route_exact, route_nna, route_genetic], ['green', 'red', 'blue']):
        result += '\n'

        for i in range(1, len(route)):
            prev = route[i - 1] - 1
            current = route[i] - 1

            result += f'\t{prev} -> {current} [color={color}]\n'

    result += '}'

    with open('graph.gv', 'w', encoding='utf-8') as file:
        file.write(result)

convert_to_dot(read_csv('graph.csv'))
