import heapq

from mazegen.animation import GridDisplayer
from mazegen.cell import Cell
from mazegen.cell_value import CellValue
from mazegen.solvers.base import Solver


class PriorityQue():
    def __init__(self):
        self._heap: List[Tuple[int, Cell]] = []
        self.counter: int = 0

    def push(self, priority: int, cell: Cell) -> None:
        """
        Tie-breaking: If two items have the same priority, 
        heapq will try to compare the objects themselves. 
        To avoid TypeError, it is best to use 
        (priority, count, task_object) tuples, 
        where count is a unique, incrementing number.
        """
        heapq.heappush(self._heap, (priority, self.counter, cell))
        self.counter += 1

    
    def pop(self) -> Cell:
        if not self._heap:
            raise Exception("Open set is empty → path not found")  # Debug
        priority, counter, cell = heapq.heappop(self._heap)
        print("POP:", cell)
        return cell

    def is_empty(self)-> bool:
        if len(self._heap) == 0:
            return True
        return False

class SolverAstar(Solver):
    def solve(
        self,
        grid: GridDisplayer,
        entry: Cell,
        exit: Cell,  # noqa: A002
    ) -> None:
        self._foo = None

        open_set = PriorityQue()
        # hopeful condidates list which we gonna check
        open_set.push(0, entry)
        g_score = {(entry.x, entry.y): 0}
        # g_score: actual cost sntry to current cell

        closed_set = set()
        while not open_set.is_empty():
            current = open_set.pop()  # 一番有望なのをPOP
            print("CURRENT", current)

            if (current.x, current.y) in closed_set:  # 入っていたらもう見てる
                continue
            closed_set.add((current.x, current.y))
            # TODO 隣セルの処理

            for n, neighbor in enumerate(
                grid.get_reachable_unmarked_neighbors(current),
            ):
                print(f"In the for loop {n}th time")
                temp = g_score[current.x, current.y] + 1
                if (neighbor.x, neighbor.y) not in g_score:
                    g_score[neighbor.x, neighbor.y] = temp  
                    grid.set_parent(neighbor, current)
                open_set.push(f_score(temp, manhattan_heuristic(neighbor, exit)), neighbor)
                print("PUSH:", neighbor)
            grid.display()
        current = exit
        m = 1
        while current is not entry:
            print(g_score)
            print(f"In the while after 73 {m}th time")
            m += 1
            if current != exit:
                grid.set_cell_value(current, CellValue.SOLUTION)

            parent = grid.get_parent(current)
            if parent is None:
                break

            current = parent

            grid.display_cell(current)

        grid.reset_cell_markings()
        grid.unset_parents()


class PriorityQue:
    def __init__(self) -> None:
        self._heap: list[tuple[int, int, Cell]] = []
        self.counter: int = 0

    def push(self, priority: int, cell: Cell) -> None:
        heapq.heappush(self._heap, (priority, self.counter, cell))
        self.counter += 1

    def pop(self) -> Cell:
        if not self._heap:
            raise Exception("Open set is empty → path not found")  # Debug
        _priority, _counter, cell = heapq.heappop(self._heap)
        print("POP:", cell)
        return cell

    def is_empty(self) -> bool:
        return len(self._heap) == 0


def f_score(g_score: int, manhattan_heuristic: int) -> int:
    return g_score + manhattan_heuristic


def manhattan_heuristic(current: Cell, exit: Cell) -> int:  # noqa: A002
    return abs(current.x - exit.x) + abs(current.y - exit.y)





"""    def get_parent(self, child: Cell) -> Cell | None:
        return self._parents[child.y][child.x]
"""

