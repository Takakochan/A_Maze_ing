import heapq

from mazegen.cell import Cell
from mazegen.cell_value import CellValue
from mazegen.direction import Direction
from mazegen.grid import Grid
from mazegen.render.base import Renderer
from mazegen.solvers.base import Solver


class SolverAStar2(Solver):
    def solve(
        self,
        grid: Grid,
        entry: Cell,
        exit: Cell,  # noqa: A002
        renderer: Renderer,
        animation: bool,
    ) -> list[Direction]:
        grid.reset_cell_markings()
        grid.unset_parents()

        # g_costs[cell] = スタートからそのセルまでの最短ステップ数
        g_costs: dict[Cell, int] = {entry: 0}
        queue = PriorityQueue(exit)
        queue.push(entry, 0)

        if animation:
            renderer.display_cell(grid, entry)

        while not queue.is_empty():
            current = queue.pop()
            if current is None:
                break
            if current == exit:
                break

            g_current = g_costs[current]

            for neighbor in grid.get_reachable_neighbors(current):
                g_new = g_current + 1

                # より短い経路が見つかった場合のみ更新
                if neighbor not in g_costs or g_new < g_costs[neighbor]:
                    g_costs[neighbor] = g_new
                    grid.set_parent(neighbor, current)

                    f = g_new + neighbor.distance_to(exit)
                    queue.push(neighbor, f)

                    if animation:
                        renderer.display_cell(grid, neighbor)

        # ゴールから親を辿って経路を復元
        solution: list[Direction] = []
        current = exit

        while current is not entry:
            if current != exit:
                grid.set_cell_value(current, CellValue.SOLUTION)

            if animation:
                renderer.display_cell(grid, current)

            parent = grid.get_parent(current)
            if parent is None:
                break

            direction = parent.get_direction_to_neighbor(current)
            solution.insert(0, direction)

            current = parent

        grid.reset_cell_markings()
        grid.unset_parents()

        return solution


class PriorityQueue:
    def __init__(self, target: Cell) -> None:
        self._heap: list[tuple[int, int, Cell]] = []
        self._counter: int = 0
        self.target = target

    def push(self, cell: Cell, f: int) -> None:
        heapq.heappush(self._heap, (f, self._counter, cell))
        self._counter += 1

    def pop(self) -> Cell | None:
        if not self._heap:
            return None

        _, _, cell = heapq.heappop(self._heap)

        return cell

    def is_empty(self) -> bool:
        return len(self._heap) == 0
