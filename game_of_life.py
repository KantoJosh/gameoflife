import numpy as np
import sys
from collections import defaultdict

INT_64_MAX = 9223372036854775807
INT_64_MIN = -9223372036854775808

def get_alive_coordinates():
    """
    Returns set of alive coordinates from standard input
    Refer to sample input above for expected input format
    """
    alive_coordinates = set()
    for line in sys.stdin:
        # parse coordinate
        x,y = line.strip("()\n").split(", ")
        # convert from strings -> fixed size ints
        # print(x,y)
        coordinate = (np.int64(x), np.int64(y))
        alive_coordinates.add(coordinate)

    return alive_coordinates


def get_neighbors(cell_coordinate):
    """
    Returns neighboring cells around cell_coordinate
    and filters any neighboring cells that are not on the board,
    which is limited by the min/max values of a 64 bit signed int
    """
    row,column = cell_coordinate
    neighbors = [
        (row - 1, column - 1),
        (row - 1, column),
        (row - 1, column + 1),
        (row, column - 1),
        (row, column + 1),
        (row + 1, column - 1),
        (row + 1, column),
        (row + 1, column + 1)
    ]
    return list(filter(lambda n: INT_64_MIN < n[0] < INT_64_MAX and INT_64_MIN < n[1] < INT_64_MAX ,neighbors))


def update_alive_cells(alive_cells):
    cell_neighbor_freq = defaultdict(int)
    for cell in alive_cells:
        neighbors = get_neighbors(cell)
        for n in neighbors:
            cell_neighbor_freq[n] += 1
    
    new_alive_cells = set()
    for cell in cell_neighbor_freq:
            # dead --> stay alive
        if (cell_neighbor_freq[cell] == 3 or cell_neighbor_freq[cell] == 2) or (
            # alive --> alive
            cell in alive_cells and cell_neighbor_freq[cell] == 2):
            new_alive_cells.add(cell)
    
    return new_alive_cells

def game_of_life(alive_cells, iterations):
    # print(alive_cells)
    for _ in range(iterations):
        alive_cells = update_alive_cells(alive_cells)
        # print(alive_cells)
    return alive_cells


def output(alive_coordinates):
    # Life 1.06 format: 
    # https://conwaylife.com/wiki/Life_1.06#:~:text=The%20Life%201.06%20file%20format,lif%20or%20.
    print("#Life 1.06")
    for x,y in alive_coordinates:
        print(f"{x} {y}")

if __name__ == "__main__":
    # Sample input:
    # (0, 1)
    # (1, 2)
    # (2, 0)
    # (2, 1)
    # (2, 2)
    # (-2000000000000, -2000000000000)
    # (-2000000000001, -2000000000001)
    NUM_ITERATIONS = 1
    alive_cells = game_of_life(get_alive_coordinates(), NUM_ITERATIONS)
    
    output(alive_cells)