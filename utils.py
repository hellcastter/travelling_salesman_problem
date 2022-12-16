""" Help functions """
from typing import Iterable, List

CITY = int | float
CITIES_MAP = List[List[CITY]]

def distance(x_city: int, y_city: int, cities_map: CITIES_MAP) -> int:
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


def dfs(graph: CITIES_MAP) -> List[int]:
    """
    perform dfs on the graph and store its result
    in a adjacency graph

    Args:
        graph (List[List[int]]): original graph

    Returns:
        List[int]: path

    >>> dfs([[0, 5, -1], [5, 0, 3], [-1, 3, 0]])
    [0, 1, 2]

    >>> dfs([[0, 5, 0, -1], [5, 0, 3, -1], [0, 3, 0, -1], [-1, -1, -1, 0]])
    [0, 1, 2]
    """
    result = [0]
    stack = [0]

    while stack:
        key = stack[-1]
        vertices = graph[key]

        for index, vertex in enumerate(vertices):
            if vertex in (0, -1):
                continue

            if index not in result:
                result.append(index)
                stack.append(index)
                break
        else:
            # delete only in case we didn't find a vertex,
            # which is not in result. In this case, if break statement
            # wasn't called
            del stack[-1]

    return result


def is_connected(graph: CITIES_MAP) -> bool:
    """
    Checks wether graph is connected

    Args:
        graph (List[List[int]]): original graph

    Returns:
        bool: is connected

    >>> is_connected([[0, 5, -1], [5, 0, 3], [-1, 3, 0]])
    True

    >>> is_connected([[0, 5, 0, -1], [5, 0, 3, -1], [0, 3, 0, -1], [-1, -1, -1, 0]])
    False
    """
    dfs_result = dfs(graph)
    return len(dfs_result) == len(graph)