""" Traveling salesman problem """
from typing import List
from itertools import combinations
from collections.abc import Iterable

def read_csv(file_name: str) -> List[List[int]]:
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
    for index, row in enumerate(data):
        data[index] = row.split(',')
        data[index] = [int(i) - 1 for i in data[index]]

        row = data[index]
        size = max(size, row[0], row[1])

    size += 1
    matrix = [[-1] * size for _ in range(size)] # init matrix

    # fill matrix with data
    for row in data:
        first, second, weight = row

        matrix[first][second] = weight
        matrix[second][first] = weight

    # make main diagonal = 0
    for i in range(size):
        matrix[i][i] = 0

    return matrix


def distance(x_city: int, y_city: int, cities_map: List[List[int]]) -> int:
    """
    Distance between two cities
    Args:
        x_city (int): start city
        y_city (int): end city
        cities_map (List[List[int]]): city map
    Returns:
        int: distance
    """
    return cities_map[y_city][x_city]


def vertexes_to_bits(combination: Iterable[int]) -> int:
    """
    Convert vertexes to bits by adding all binaries values

    Args:
        combination (Tuple[int]): Tuple of vertexes

    Returns:
        int: Binary representation

    >>> vertexes_to_bits((1, 2, 3))
    14
    """
    bits = 0
    for i in combination:
        bits |= 1 << i

    return bits


def binary_without_vertex(vertex: int, binary: int) -> int:
    """
    get combination without vertex element
    we just set 0 in vertex-th place in binary

    Args:
        vertex (int): "deleted" vertex
        binary (int): set represented in binary

    Returns:
        int: binary without element

    >>> binary_without_vertex(3, 16)
    16
    """
    return binary & ~(1 << vertex)


def exact_tsp(cities_map: List[List[int]]) -> List[int]:
    """
    Searches the shortest way through all vertexes in graph going through
    all vertexes only once in exact way

    Args:
        cities_map (List[List[int]]): Adjacency matrix representing distances between vertexes

    Returns:
        List[int]: the shortest way

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
