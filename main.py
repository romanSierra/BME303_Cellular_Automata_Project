# This has the random grid, cell types, neighborhood, and basic change implementations,
# some code is redundant like my counts fuction
# This is mostly a proof of concept and the creation of a class may not be necessary

#import matplotlib as plt
import numpy as np

class Cell_Grid:

#  If you want to change the cell names, change this tuple. The code should be agnostic hopefully.
    type_key = ("Empty", "Healthy", "Damaged", "Bacteria")

    #Initalizes a 2D np.array with dimensions (row,col) with a random int pattern ranging fro 0-3 inclusive
    def __init__(self, rows, columns,):
        self.rows = rows
        self.columns = columns

        #Array Creation
        rng = np.random.default_rng()
        self.grid = rng.integers(low = 0, high = len(Cell_Grid.type_key), size = (rows, columns))
        self.grid_temp = np.zeros_like(self.grid)

    #returns the cell name based on the its number
    @staticmethod
    def check_type(value):
            return Cell_Grid.type_key[value]

   # returns the cell number based on its name
    @staticmethod
    def get_num_type(value):
        return Cell_Grid.type_key.index(value)


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
        #print(neighborhood)
        for r in neighborhood:
            for c in r:
                neighborhood_counts[Cell_Grid.check_type(c)] += 1
        neighborhood_counts[Cell_Grid.check_type(self.grid[row,col])] -= 1

        return neighborhood_counts

    # this is janky logic for testing that returns the most common cell in a cell's surroundings
    # to be used in my update method. it will change to reflect the right logic later.
    @staticmethod
    def cell_rules(neighborhood, cell_type):
        max_count = max(neighborhood.values())
        max_key = ""
        for key in neighborhood:
            if max_count == neighborhood[key]:
                max_key = key
        return Cell_Grid.get_num_type(max_key)


    #loops through the whole grid and stores an update at each position in a temp grid
    #  based on the surroundings and then changes the original grid
    # I have hard coded the logic for the surroundings but would like to make better functions for it later.
    def update_grid(self):
        for row in range(self.rows):
            for col in range(self.columns):
                current_type = self.grid[row, col]
                surroundings = self.check_neighborhood(row, col)
                self.grid_temp[row, col] = Cell_Grid.cell_rules(surroundings, current_type)
        self.grid = self.grid_temp.copy()


test_grid = Cell_Grid(5, 5)
print(test_grid.grid)
print(test_grid.get_counts())
print(test_grid.check_type(test_grid.grid[0,0]))
print(test_grid.check_neighborhood(2,2))
test_grid.update_grid()
print(test_grid.grid)
