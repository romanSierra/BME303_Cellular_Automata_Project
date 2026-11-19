# This has the random grid, cell types, neighborhood, and basic change implementations,
# some code is redundant like my counts fuction
# This is mostly a proof of concept and the creation of a class may not be necessary

#import matplotlib as plt
import numpy as np
import random
class CellGrid:

#  If you want to change the cell names, change this tuple. The code should be agnostic hopefully.
    type_key = ("Empty", "Healthy", "Damaged", "Bacteria")

    #Initalizes a 2D np.array with dimensions (row,col) with a random int pattern ranging fro 0-3 inclusive
    def __init__(self, rows, columns,):
        self.rows = rows
        self.columns = columns

        #Array Creation
        rng = np.random.default_rng()
        self.grid = rng.integers(low = 0, high = len(CellGrid.type_key), size = (rows, columns))
        self.grid_temp = np.zeros_like(self.grid)

    #returns the cell name based on the its number
    @staticmethod
    def check_type(value):
         return CellGrid.type_key[value]

   # returns the cell number based on its name
    @staticmethod
    def get_num_type(value):
        return CellGrid.type_key.index(value)


    #returns a dictionary with cell type and their counts
    def get_counts(self):
        type_counts = dict.fromkeys(self.type_key, 0)
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
        neighborhood_counts = dict.fromkeys(self.type_key, 0)
        #print(neighborhood)
        for r in neighborhood:
            for c in r:
                neighborhood_counts[CellGrid.check_type(c)] += 1
        neighborhood_counts[CellGrid.check_type(self.grid[row,col])] -= 1

        return neighborhood_counts

   #New logic reflecting the current cells. It is not name agnostic so it needs to be updated if we change the types.
    @staticmethod
    def cell_rules(neighborhood, cell_type):
        spread_threshold = 0.90
        r = random.uniform(0.0, 1.0)
        if cell_type == 3:
            if r >= 0.95:
                return 2
            return 3

        elif cell_type == 2:
            if r >= 0.8:
                return 0
            else:
                return 2

        elif cell_type == 1:
            if neighborhood["Bacteria"] == 0 and r>= 0.9:
                return 2
            else:
                return 1

        else:
            if r * neighborhood["Bacteria"]>= spread_threshold:
                return 3
            elif neighborhood["Healthy"] != 0 and r>=0.85:
                 return 1
            else:
                return 0




    #loops through the whole grid and stores an update at each position in a temp grid
    #  based on the surroundings and then changes the original grid
    # I have hard coded the logic for the surroundings but would like to make better functions for it later.
    def update_grid(self):
        for row in range(self.rows):
            for col in range(self.columns):
                current_type = self.grid[row, col]
                surroundings = self.check_neighborhood(row, col)
                self.grid_temp[row, col] = CellGrid.cell_rules(surroundings, current_type)
        self.grid = self.grid_temp.copy()



test_grid = CellGrid(5, 5)
print(test_grid.grid)
print(test_grid.get_counts())
print(test_grid.check_type(test_grid.grid[0,0]))
print(test_grid.check_neighborhood(2,2))
test_grid.update_grid()
print(test_grid.grid)
