""" Calculate TSP with genetic algorithm """
from typing import List
from random import shuffle, choice, randint
from utils import CITIES_MAP, PATH, distance, is_connected

def calc_path_distance(path: List[int], cities_map: CITIES_MAP) -> int | float:
    path_distance = 0

    for index in range(1, len(path)):
        city = path[index]
        prev_city = path[index - 1]
        path_distance += distance(prev_city, city, cities_map)

    path_distance += distance(0, path[0], cities_map)
    path_distance += distance(path[-1], 0, cities_map)

    return path_distance


def genetic(cities_map: CITIES_MAP, mutations: int = 10) -> PATH:
    """
    Searches the shortest way through all vertexes in graph going through
    all vertexes only once in approximate way using genetic algorithm

    Args:
        cities_map (CITIES_MAP): Adjacency matrix representing distances between vertexes

    Returns:
        PATH: one of the shortest way if exists. On the other case None
    """
    if not is_connected(cities_map):
        print('Graph is not connected.')
        print('It is impossible to go through all vertexes.')
        return None

    length = len(cities_map)

    path = list(range(1, length))
    shuffle(path)
    path_distance = calc_path_distance(path, cities_map)

    for _ in range(mutations):
        first = randint(0, length - 2)

        second_list = list(range(0, length - 1))
        second_list.remove(first)
        second = choice(second_list)

        path_copy = path[:]
        path_copy[first], path_copy[second] = path_copy[second], path_copy[first]

        temp_distance = calc_path_distance(path_copy, cities_map) # could be improved

        if temp_distance < path_distance:
            path = path_copy
            path_distance = temp_distance

    return [1] + [i + 1 for i in path]  + [1]
