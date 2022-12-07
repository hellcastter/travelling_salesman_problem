""" Traveling salesman problem """
import math
from typing import List, Set
from itertools import permutations

def read_csv(file_path: str) -> List[List[int]]:
    """ 1 """
    pass

def distance(x: int, y: int, cities_map: List[List[int]]) -> int:
    """
    Distance between two cities

    Args:
        x (int): start city
        y (int): end city
        cities_map (List[List[int]]): city map

    Returns:
        int: distance
    """
    return cities_map[y][x]

def length_of_shortest_path(end: int, cities_set: Set[int], cities_map: List[List[int]]) -> int:
    """
    Searches the shortest path from 0th vertex to end vertex through set_of_cities.

    Args:
        end (int): to what vertex do we want to get
        cities_set (Set[int]): through what cities we want to go through
        cities_map (List[List[int]]): our map

    Return:
        int: length of shortest path

    >>> length_of_shortest_path(2, {}, [[0,2,9,10], [1,0,6,4], [15,7,0,8], [6,3,12,0]])
    15
    >>> length_of_shortest_path(3, {2}, [[0,2,9,10], [1,0,6,4], [15,7,0,8], [6,3,12,0]])
    27
    >>> length_of_shortest_path(1, {2, 3}, [[0,2,9,10], [1,0,6,4], [15,7,0,8], [6,3,12,0]])
    20
    """
    if len(cities_set) == 0:
        return distance(0, end, cities_map)

    min_length = math.inf

    # go through all combinations of set of cities
    for permutation in permutations(cities_set):
        local_length = 0

        for city_index, city in enumerate(permutation):
            # if first city => add length between 0 and first city
            if city_index == 0:
                local_length += distance(0, city, cities_map)
                continue

            # get length between prev city and current
            prev_city = permutation[city_index - 1]
            local_length += distance(prev_city, city, cities_map)

        # add distance between last from combination and end city
        local_length += distance(permutation[-1], end, cities_map)

        min_length = min(min_length, local_length)

    return min_length
