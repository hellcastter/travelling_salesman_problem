""" Traveling salesman problem """
from pprint import pprint
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
