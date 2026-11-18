# This has the random grid, cell types, neighborhood, and basic change implementations,
# some code is redundant like my counts fuction
# This is mostly a proof of concept and the creation of a class may not be necessary

import matplotlib as plt
import numpy as np

class Cell_Grid:

    #Initalizes a 2D np.array with dimensions (row,col) with a random int pattern ranging fro 0-3 inclusive
    def __init__(self, rows, columns,):
        self.rows = rows
        self.columns = columns

        #Array Creation
        rng = np.random.default_rng()
        self.grid = rng.integers(low = 0, high = 4, size = (rows, columns))

    #returns the cell type at a specific index in the matrix
    @staticmethod
    def check_type(value):
        if value == 3:
            return "Bacteria"
        elif value == 2:
            return "Damaged"
        elif value == 1:
            return "Healthy"
        else:
            return "Empty"

    #returns a dictionary with cell type and their counts
    def get_counts(self):
        type_counts = {"Empty":0, "Healthy":0, "Damaged":0, "Bacteria":0}
        for row in self.grid:
            for cell in row:
                type_counts[self.check_type(cell)] += 1
        return type_counts

    #creates a moore neighborhood and tallies the count of each cell type in the surrounding
    # returns a dictionary of cell types and their counts
    def check_neighborhood(self, row, col):

        #makes sure the bounds fall within the size of the grid
        r_start = max(0, row-1)
        r_end = min(self.rows, row + 2)
        c_start = max(0, col - 1)
        c_end = min(self.columns, col + 2)

        #slices a neighborhood window and counts the type of each cell in the window, then removes the
        #count for the  center cell
        neighborhood = self.grid[r_start:r_end, c_start:c_end]
        neighborhood_counts = {"Empty":0, "Healthy":0, "Damaged":0, "Bacteria":0}
        print(neighborhood)
        for r in neighborhood:
            for c in r:
                neighborhood_counts[Cell_Grid.check_type(c)] += 1
        neighborhood_counts[Cell_Grid.check_type(self.grid[row,col])] -= 1

        return neighborhood_counts

test_grid = Cell_Grid(5, 5)
print(test_grid.grid)
print(test_grid.get_counts())
print(test_grid.check_type(test_grid.grid[0,0]))
print(test_grid.check_neighborhood(2,2))
