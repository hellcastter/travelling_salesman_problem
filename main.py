""" Traveling salesman problem """
import time
import math
from typing import List, Set
from itertools import permutations

def read_csv(file_path: str) -> List[List[int]]:
    """ 1 """
    return [[0, 2, 9, 10], [1, 0, 6, 4], [15, 7, 0, 8], [6, 3, 12, 0]]

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


def TSP(cities_map: List[List[int]]) -> List[int]:
    """ 1 """
    size = len(cities_map)
    minimal = math.inf

    for s in range(1, size - 1):
        cities_list = list(range(1, size))
        cities_list.remove(s)
        cities = set(cities_list)

        minimal = min(minimal, length_of_shortest_path(s, cities, cities_map) + distance(s, 0, cities_map))
        # for i in permutations(range(1, size), s):
        #     for k in i:

    print(minimal)



start = time.time()
# TSP(read_csv('graph.csv'))
TSP([[0, 141, 134, 152, 173, 289, 326, 329, 285, 401, 388, 366, 343, 305, 276], 
[141, 0, 152, 150, 153, 312, 354, 313, 249, 324, 300, 272, 247, 201, 176], 
[134, 152, 0, 24, 48, 168, 210, 197, 153, 280, 272, 257, 237, 210, 181], 
[152, 150, 24, 0, 24, 163, 206, 182, 133, 257, 248, 233, 214, 187, 158], 
[173, 153, 48, 24, 0, 160, 203, 167, 114, 234, 225, 210, 190, 165, 137], 
[289, 312, 168, 163, 160, 0, 43, 90, 124, 250, 264, 270, 264, 267, 249], 
[326, 354, 210, 206, 203, 43, 0, 108, 157, 271, 290, 299, 295, 303, 287], 
[329, 313, 197, 182, 167, 90, 108, 0, 70, 164, 183, 195, 194, 210, 201], 
[285, 249, 153, 133, 114, 124, 157, 70, 0, 141, 147, 148, 140, 147, 134], 
[401, 324, 280, 257, 234, 250, 271, 164, 141, 0, 36, 67, 88, 134, 150], 
[388, 300, 272, 248, 225, 264, 290, 183, 147, 36, 0, 33, 57, 104, 124], 
[366, 272, 257, 233, 210, 270, 299, 195, 148, 67, 33, 0, 26, 73, 96], 
[343, 247, 237, 214, 190, 264, 295, 194, 140, 88, 57, 26, 0, 48, 71], 
[305, 201, 210, 187, 165, 267, 303, 210, 147, 134, 104, 73, 48, 0, 30], 
[276, 176, 181, 158, 137, 249, 287, 201, 134, 150, 124, 96, 71, 30, 0]])
print("--- %s seconds ---" % (time.time() - start))