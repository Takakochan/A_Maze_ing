from mazegen.cell import Cell
from mazegen.grid import Grid
from mazegen.solvers.base import Solver
import heapq
from mazegen.cell_value import CellValue


class PriorityQue():
    def __init__(self):
        self._heap: List[Tuple[int, Cell]] = []
        self.counter: int = 0
    
    def push(self, priority: int, cell: Cell) -> None:
        """heappush adding to _heap list"""
        heapq.heappush(self._heap, (priority, self.counter, cell))
        self.counter += 1
    
    def pop(self) -> Cell:
        _, _, cell = heapq.heappop(self._heap)
        return cell

    def is_empty(self)-> bool:
        if len(self._heap) == 0:
            return True
        return False

class SolverAstar(Solver):
    def solve(
        self,
        grid: Grid,
        entry: Cell,
        exit: Cell,  # noqa: A002
    ) -> None:
        open_set = PriorityQue()
        """ hopeful condidates list which we gonna check """
        open_set.push(0, entry)
        g_score = {(entry.x, entry.y): 0}
        """g_score: actual cost sntry to current cell"""

        closed_set = set()
        while not open_set.is_empty():
            """Main loop"""
            current = open_set.pop() # 一番有望なのをPOP
            if (current.x, current.y) in closed_set: # 入っていたらもう見てる
                continue
            closed_set.add((current.x, current.y))
            print(f"current: {current.x}, {current.y}")
            print(f"neighbors: {grid.get_reachable_unmarked_neighbors(current)}")
            print(f"g_score: {g_score}")
            #TODO 隣セルの処理
            for neighbor in grid.get_reachable_unmarked_neighbors(current):
                temp = g_score[current.x, current.y] + 1 # because it is one step next
                g_score[neighbor.x, neighbor.y] = temp
                grid.set_parent(neighbor, current)
                
                f = f_score(temp, manhattan_heuristic(neighbor, exit))
                open_set.push(f, neighbor)

        current = exit

        while current is not entry:
            if current != exit:
                grid.set_cell_value(current, CellValue.SOLUTION)

            parent = grid.get_parent(current)
            if parent is None:
                break

            current = parent

            grid.display()

        grid.reset_cell_markings()
        grid.unset_parents()




def f_score(g_score: int, manhattan_heuristic: int) -> int:
    return g_score + manhattan_heuristic
        
def manhattan_heuristic(current: Cell, exit: Cell) -> int:
    return abs(current.x - exit.x) + abs(current.y - exit.y)




