""" Traveling salesman problem """
from typing import List
from itertools import combinations
from utils import CITIES_MAP, binary_without_vertex, distance, is_connected, vertexes_to_bits


def read_csv(file_name: str) -> CITIES_MAP:
    """
    Read matrix from .csv file. CSV file must be in format
    first_city,second_city,length

    Args:
        file_name (str): path to file

    Returns:
        List[List[int]]: matrix of length
    """
    with open(file_name, 'r', encoding='utf-8') as file:
        data = file.read().strip().split('\n')

    # get matrix size (max element) and convert all to int
    size = 0
    data_int = []
    for row in data:
        row_int = [int(i) for i in row.split(',')]
        data_int.append(row_int)

        size: int = max(size, row_int[0], row_int[1])

    matrix = [[float('inf')] * size for _ in range(size)] # init matrix

    # fill matrix with data
    for row in data_int:
        first, second, weight = row

        matrix[first - 1][second - 1] = weight
        matrix[second - 1][first - 1] = weight

    # make main diagonal = 0
    for i in range(size):
        matrix[i][i] = 0

    return matrix


def exact_tsp(cities_map: CITIES_MAP) -> List[int] | None:
    """
    Searches the shortest way through all vertexes in graph going through
    all vertexes only once in exact way

    Args:
        cities_map (List[List[int]]): Adjacency matrix representing distances between vertexes

    Returns:
        List[int] | None: the shortest way if exists. On the other case None

    >>> exact_tsp([[0, 4, -1, -1], [4, 0, -1, -1], [-1, -1, 0, 5], [-1, -1, 5, 0]])
    Graph is not connected.
    It is impossible to go through all vertexes.

    >>> exact_tsp([[0, 2, 9, 10], [1, 0, 6, 4], [15, 7, 0, 8], [6, 3, 12, 0]])
    [1, 2, 4, 3, 1]

    11x11, execution time +- 0.01914471669998602s
    >>> exact_tsp([[0, 29, 20, 21, 16, 31, 100, 12, 4, 31, 18],
    ...     [29, 0, 15, 29, 28, 40, 72, 21, 29, 41, 12],
    ...     [20, 15, 0, 15, 14, 25, 81, 9, 23, 27, 13],
    ...     [21, 29, 15, 0, 4, 12, 92, 12, 25, 13, 25],
    ...     [16, 28, 14, 4, 0, 16, 94, 9, 20, 16, 22],
    ...     [31, 40, 25, 12, 16, 0, 95, 24, 36, 3, 37],
    ...     [100, 72, 81, 92, 94, 95, 0, 90, 101, 99, 84],
    ...     [12, 21, 9, 12, 9, 24, 90, 0, 15, 25, 13],
    ...     [4, 29, 23, 25, 20, 36, 101, 15, 0, 35, 18],
    ...     [31, 41, 27, 13, 16, 3, 99, 25, 35, 0, 38],
    ...     [18, 12, 13, 25, 22, 37, 84, 13, 18, 38, 0]])
    [1, 9, 11, 2, 7, 3, 6, 10, 4, 5, 8, 1]

    15x15, execution time +- 0.606215979999979s
    >>> exact_tsp([[0, 141, 134, 152, 173, 289, 326, 329, 285, 401, 388, 366, 343, 305, 276],
    ...     [141, 0, 152, 150, 153, 312, 354, 313, 249, 324, 300, 272, 247, 201, 176],
    ...     [134, 152, 0, 24, 48, 168, 210, 197, 153, 280, 272, 257, 237, 210, 181],
    ...     [152, 150, 24, 0, 24, 163, 206, 182, 133, 257, 248, 233, 214, 187, 158],
    ...     [173, 153, 48, 24, 0, 160, 203, 167, 114, 234, 225, 210, 190, 165, 137],
    ...     [289, 312, 168, 163, 160, 0, 43, 90, 124, 250, 264, 270, 264, 267, 249],
    ...     [326, 354, 210, 206, 203, 43, 0, 108, 157, 271, 290, 299, 295, 303, 287],
    ...     [329, 313, 197, 182, 167, 90, 108, 0, 70, 164, 183, 195, 194, 210, 201],
    ...     [285, 249, 153, 133, 114, 124, 157, 70, 0, 141, 147, 148, 140, 147, 134],
    ...     [401, 324, 280, 257, 234, 250, 271, 164, 141, 0, 36, 67, 88, 134, 150],
    ...     [388, 300, 272, 248, 225, 264, 290, 183, 147, 36, 0, 33, 57, 104, 124],
    ...     [366, 272, 257, 233, 210, 270, 299, 195, 148, 67, 33, 0, 26, 73, 96],
    ...     [343, 247, 237, 214, 190, 264, 295, 194, 140, 88, 57, 26, 0, 48, 71],
    ...     [305, 201, 210, 187, 165, 267, 303, 210, 147, 134, 104, 73, 48, 0, 30],
    ...     [276, 176, 181, 158, 137, 249, 287, 201, 134, 150, 124, 96, 71, 30, 0]])
    [1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 2, 1]
    """
    # in this dict we will store all the shortest distances in format
    # {(bits, end): distance}, where:
    # bits = set of vertexes which we have to go through but in bits form
    # end = end vertex
    # distance = distance from 0 to end through bits
    if not is_connected(cities_map):
        print('Graph is not connected.')
        print('It is impossible to go through all vertexes.')
        return

    minimal_distances = {}
    cities_count = len(cities_map)

    vertexes_without_first = range(1, cities_count)

    # init distances from 0 to every vertex (adjacency vertexes only)
    for vertex in range(1, cities_count):
        minimal_distances[(1 << vertex, vertex)] = (distance(0, vertex, cities_map), 0)

    for size in range(2, cities_count):
        for combination in combinations(vertexes_without_first, size):
            bits = vertexes_to_bits(combination)

            for vertex in combination:
                local_shortest = []

                for i in combination:
                    if i == vertex:
                        continue

                    # get combination without vertex element
                    # we just set 0 in vertex-th place
                    prev = binary_without_vertex(vertex, bits)

                    distance_through_i = minimal_distances[(prev, i)][0]
                    distance_through_i += distance(i, vertex, cities_map)

                    local_shortest.append((distance_through_i, i))

                minimal_distances[(bits, vertex)] = min(local_shortest, key=lambda x: x[0])

    # get all distances through all vertexes
    local_shortest = []
    full_cities_bits = vertexes_to_bits(vertexes_without_first)

    for vertex in vertexes_without_first:
        distance_through_vertex = minimal_distances[(full_cities_bits, vertex)][0]
        distance_through_vertex += distance(vertex, 0, cities_map)

        local_shortest.append((distance_through_vertex, vertex))

    # reconstruct the shortest way
    # [0] is the shortest distance
    _, parent = min(local_shortest, key=lambda x: x[0])

    path = []
    for _ in vertexes_without_first:
        path.append(parent)

        binary_path_new = binary_without_vertex(parent, full_cities_bits)
        parent = minimal_distances[(full_cities_bits, parent)][1]
        full_cities_bits = binary_path_new

    path = reversed(path)
    # we need to start from 1, so add 1 to every vertex
    path = [i + 1 for i in path]

    return [1] + path + [1]


def nna(cities_map: CITIES_MAP) -> List[int] | None:
    """
    Searches the shortest way through all vertexes in graph going through
    all vertexes only once in approximate way using nearest neighbor algorithm

    Args:
        cities_map (CITIES_MAP): Adjacency matrix representing distances between vertexes

    Returns:
        List[int] | None: one of the shortest way if exists. On the other case None

    >>> nna([[0, 141, 134, 152, 173, 289, 326, 329, 285, 401, 388, 366, 343, 305, 276],
    ...     [141, 0, 152, 150, 153, 312, 354, 313, 249, 324, 300, 272, 247, 201, 176],
    ...     [134, 152, 0, 24, 48, 168, 210, 197, 153, 280, 272, 257, 237, 210, 181],
    ...     [152, 150, 24, 0, 24, 163, 206, 182, 133, 257, 248, 233, 214, 187, 158],
    ...     [173, 153, 48, 24, 0, 160, 203, 167, 114, 234, 225, 210, 190, 165, 137],
    ...     [289, 312, 168, 163, 160, 0, 43, 90, 124, 250, 264, 270, 264, 267, 249],
    ...     [326, 354, 210, 206, 203, 43, 0, 108, 157, 271, 290, 299, 295, 303, 287],
    ...     [329, 313, 197, 182, 167, 90, 108, 0, 70, 164, 183, 195, 194, 210, 201],
    ...     [285, 249, 153, 133, 114, 124, 157, 70, 0, 141, 147, 148, 140, 147, 134],
    ...     [401, 324, 280, 257, 234, 250, 271, 164, 141, 0, 36, 67, 88, 134, 150],
    ...     [388, 300, 272, 248, 225, 264, 290, 183, 147, 36, 0, 33, 57, 104, 124],
    ...     [366, 272, 257, 233, 210, 270, 299, 195, 148, 67, 33, 0, 26, 73, 96],
    ...     [343, 247, 237, 214, 190, 264, 295, 194, 140, 88, 57, 26, 0, 48, 71],
    ...     [305, 201, 210, 187, 165, 267, 303, 210, 147, 134, 104, 73, 48, 0, 30],
    ...     [276, 176, 181, 158, 137, 249, 287, 201, 134, 150, 124, 96, 71, 30, 0]])
    [1, 3, 4, 5, 9, 8, 6, 7, 10, 11, 12, 13, 14, 15, 2, 1]
    """
    if not is_connected(cities_map):
        print('Graph is not connected.')
        print('It is impossible to go through all vertexes.')
        return None

    result = [0]

    for _ in range(len(cities_map)):
        city = result[-1]
        neighbors = cities_map[city]

        closest = (float('inf'), float('inf'))

        for neighbor, neighbor_distance in enumerate(neighbors):
            if neighbor in result:
                continue

            closest = min([closest, (neighbor, neighbor_distance)], key=lambda x: x[1])

        if closest[1] != float('inf'):
            result.append(closest[0])

    result.append(0)
    result = [i + 1 for i in result]

    return result
