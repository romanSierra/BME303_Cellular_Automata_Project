# This has the random grid, cell types, neighborhood, and basic change implementations,
# some code is redundant like my counts fuction
# This is mostly a proof of concept and the creation of a class may not be necessary

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap
from pathlib import Path
from PIL import Image

class CellGrid:

#  keys for the current grid. Each key's index is used in the grid so it can be a proper np array
    type_key = ("Empty", "Healthy", "Damaged", "Bacteria", "Immune")

    #Creates folders to store the outputs from matplotlib
    grid_outputs = Path("grid_frames")
    grid_outputs.mkdir(parents = True, exist_ok = True)
    graph_outputs = Path("graph_frames")
    graph_outputs.mkdir(parents = True, exist_ok = True)

    #Initalizes a 2D np.array with dimensions (row,col) with a random int pattern ranging fro 0-3 inclusive
    def __init__(self, rows, columns, wound_radius = 0, wound_type = "", immune_system = True):
        self.immune_system = immune_system
        self.rows = rows
        self.columns = columns

        # randomizer for this object
        self.rng = np.random.default_rng(seed = 12042)


        #Creation of grid using np arrays
        if wound_type == "uninfected":
            self.grid = np.ones((rows, columns), dtype = int)
            for i in range(wound_radius + 1):
                self.grid[rows // 2 +i], self.grid[rows//2 - i] = 2, 2

        elif wound_type == "infected":
            if immune_system:
                self.grid = np.ones((rows, columns), dtype = int)
                for i in range(wound_radius + 1):
                    self.grid[rows // 2 + i], self.grid[rows//2 - i] = 2, 2
                    self.grid[rows // 2] = self.rng.choice([2, 3, 4], size=columns, p=[0.5, .25, .25])
            else:
                self.grid = np.ones((rows, columns), dtype = int)
                for i in range(wound_radius + 1):
                    self.grid[rows // 2 + i], self.grid[rows//2 - i] = 2, 2
                self.grid[rows // 2] = self.rng.choice([2, 3], size=columns, p=[0.8, 0.2])

        else:
            self.grid = self.rng.integers(low = 0, high = len(CellGrid.type_key), size = (rows, columns))

        self.grid_temp = np.zeros_like(self.grid)

         # tracker variables
        starting_counts = self.get_counts()
        self.empty_counts = [starting_counts["Empty"]]
        self.healthy_counts = [starting_counts["Healthy"]]
        self.damaged_counts = [starting_counts["Damaged"]]
        self.bacteria_counts = [starting_counts["Bacteria"]]
        self.immune_counts = [starting_counts["Immune"]]
        self.time = 0


    #returns the cell name based on the its number
    @staticmethod
    def check_type(value):
         return CellGrid.type_key[value]
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

   #Cell logic for all cells. Takes the an int and the current neighborhood, and then returns a int.
   # To be used with update grid
    def cell_rules(self, neighborhood, cell_type_num):
       cell_type = CellGrid.type_key[cell_type_num]

       if cell_type == "Empty":
           p_healthy = 0.05 * neighborhood["Healthy"]
           p_immune =  neighborhood["Immune"] * 0.12 + (neighborhood["Bacteria"] + neighborhood["Damaged"]) * 0.04

           if neighborhood["Bacteria"] == 0 and self.rng.random() < p_healthy:
                return CellGrid.type_key.index("Healthy")
           elif self.rng.random() < p_immune and self.immune_system:
                return CellGrid.type_key.index("Immune")
           else:
               return CellGrid.type_key.index("Empty")

       elif cell_type == "Healthy":
           if self.rng.random() < 0.08 * neighborhood["Bacteria"]:
               return CellGrid.type_key.index("Damaged")
           else:
               return CellGrid.type_key.index("Healthy")


       elif cell_type == "Damaged":
           p_bac = neighborhood["Bacteria"] * 0.14
           p_empty = 0.05 + 0.1 * neighborhood["Immune"] #+ 0.01 * self.time
           if self.rng.random() < p_bac:
               return CellGrid.type_key.index("Bacteria")
           elif neighborhood["Bacteria"] == 0 and self.rng.random() < p_empty:
               return CellGrid.type_key.index("Empty")
           else:
               return CellGrid.type_key.index("Damaged")


       elif cell_type == "Bacteria":
           p_empty = 0.13 * neighborhood["Immune"]
           if self.rng.random() < p_empty:
               return CellGrid.type_key.index("Empty")
           else:
               return CellGrid.type_key.index("Bacteria")

       else:
           p_empty = 0.35
           if neighborhood["Bacteria"] == 0 and self.rng.random() < p_empty:
               return CellGrid.type_key.index("Empty")
           else:
               return CellGrid.type_key.index("Immune")



    #loops through the whole grid and stores an update at each position in a temp grid
    # based on the surroundings and then changes the original grid
    # updates the counts lists as well
    def update_grid(self):
        for row in range(self.rows):
            for col in range(self.columns):
                current_type = self.grid[row, col]
                surroundings = self.check_neighborhood(row, col)
                self.grid_temp[row, col] = self.cell_rules(surroundings, current_type)
        self.grid = self.grid_temp.copy()
        counts = self.get_counts()
        self.empty_counts.append(counts["Empty"])
        self.healthy_counts.append(counts["Healthy"])
        self.damaged_counts.append(counts["Damaged"])
        self.bacteria_counts.append(counts["Bacteria"])
        self.immune_counts.append(counts["Immune"])

        self.time += 1

# saves all the grid snapshots you take to a folder called grid_frames
    def save_grid(self) :
        fig, ax = plt.subplots(figsize = (6,6))
        cmap = ListedColormap ([ "xkcd:dark taupe" , "xkcd:dark sage" , "xkcd:camel" , "xkcd:clay", "xkcd:dark brown" ])
        vmax = 4
        image = ax.pcolormesh(self.grid, cmap = cmap, vmin = -0.5 ,
            vmax = vmax + 0.5, edgecolor = "xkcd:black", linewidth = 1)
        if self.time == 0:
            ax.set_title("Cell Grid at the Beginning")
        else:
            ax.set_title(f"Cell Grid at {self.time} hours")
        ax.set_aspect("equal", anchor = "C")
        cbar = fig.colorbar(image, ax = ax, shrink = 0.8, ticks = np.arange(vmax + 1), panchor = False)
        cbar.ax.set_yticklabels(CellGrid.type_key)
        ax.set_axis_off()
        ax.invert_yaxis()
        plt.savefig(CellGrid.grid_outputs / f"BME303_Cellular_Automata_Project_Grids_t{self.time:03d}")
        plt.close("all")

# saves all the graph snapshots you take to a folder called graph_frams
    def save_graph(self, duration):
        fig, ax = plt.subplots(figsize = (6,5))
        ax.plot(np.array(self.empty_counts), label = CellGrid.type_key[0], color = "xkcd:dark taupe", linewidth = 2.5)
        ax.plot(np.array(self.healthy_counts), label = CellGrid.type_key[1], color = "xkcd:dark sage", linewidth = 2.5)
        ax.plot(np.array(self.damaged_counts), label = CellGrid.type_key[2], color = "xkcd:camel", linewidth = 2.5)
        ax.plot(np.array(self.bacteria_counts), label = CellGrid.type_key[3],color = "xkcd:clay", linewidth = 2.5)
        ax.plot(np.array(self.immune_counts), label = CellGrid.type_key[4],color = "xkcd:dark brown", linewidth = 2.5)
        ax.set_title("Counts of Each Type Over Time")
        ax.set_xlim(0, duration)
        ax.set_ylim(0, 2500)
        ax.set_xlabel("Time (hours)")
        ax.set_ylabel("Count")
        ax.legend(loc = "upper left" , ncols = 2)
        plt.savefig(CellGrid.graph_outputs / f"BME303_Cellular_Automata_Project_LineGraph_t{self.time:03d}")
        plt.close("all")


# runs a simulation for a given CellGrid over the specified period
# each value in Times is a time that a snapshot is taken.
    def run(self,duration, times = ()):
        for item in CellGrid.graph_outputs.iterdir():
            if item.is_file() or item.is_symlink():
                item.unlink()
        for item in CellGrid.grid_outputs.iterdir():
            if item.is_file() or item.is_symlink():
                item.unlink()

        for i in range(duration+1):
            if i == 0:
                self.save_grid()
            elif i in times:
                self.save_grid()
                self.save_graph(duration + 1)
            self.update_grid()

        #creates gifs showing the automata grid and graph changing over time
        grid_snapshots = sorted(CellGrid.grid_outputs.glob("*.png"))
        frames = [Image.open(path) for path in grid_snapshots]
        frames[0].save(
            CellGrid.grid_outputs / "cell_grid_animation.gif",
            save_all=True,
            append_images=frames[1:],
            duration=250,
            loop=0,
        )
        graph_snapshots = sorted(CellGrid.graph_outputs.glob("*.png"))
        frames = [Image.open(path) for path in graph_snapshots]
        frames[0].save(
            CellGrid.graph_outputs / "cell_graph_animation.gif",
            save_all=True,
            append_images=frames[1:],
            duration=250,
            loop=0,
        )





test_grid = CellGrid(50, 50, wound_radius = 8, wound_type = "infected", immune_system=False)
test_grid.run(120, (range(0,121, 5)))
