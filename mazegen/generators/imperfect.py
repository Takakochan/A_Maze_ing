from mazegen.animation import GridDisplayer
from mazegen.generators.base import Generator
from mazegen.cell import Cell
from mazegen.generators.dfs import GeneratorDFS
from mazegen.direction import Direction
from mazegen.wall_state import WallState
import random

class GeneratorImperfect(Generator):
    def generate(self, grid: GridDisplayer) -> None:
        self._foo = None
        GeneratorDFS().generate(grid)

    def _collect_closed_walls(self, grid)-> list:
        closed_walls = []
        for x in range(grid.width):
            for y in range(grid.height):
                cell = Cell(x, y)
                if y < grid.height - 1 and grid.get_wall_state(cell, Direction.SOUTH) == WallState.CLOSED:
                        print(cell, Direction.SOUTH)
                        closed_walls.append((cell, Direction.SOUTH))
                if x > 0 and grid.get_wall_state(cell, Direction.WEST) == WallState.CLOSED:
                     closed_walls.append((cell, Direction.WEST))

    def _open_random_walls(self, grid: GridDisplayer, closed_walls: list) -> None:
        random.choice(closed_walls)