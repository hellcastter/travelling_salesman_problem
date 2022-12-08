""" Traveling salesman problem """
import math
from typing import List

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

    # File must have n^2 - n rows, where n is count of cities,
    # because n^2 is every-to-every city and n is and empty diagonal
    data_size = len(data)
    discriminant = 1 + 4 * data_size

    # count of cities
    size = int((1 + math.sqrt(discriminant)) // 2)

    # init resulted matrix
    result = [[0] * size for _ in range(size)]

    for row in data:
        row = list(map(int, row.split(",")))
        result[row[0]][row[1]] = row[2]

    return result
