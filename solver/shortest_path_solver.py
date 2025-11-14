from timeit import default_timer as timer

from path_finding.shortest_path import ShortestPath

from avb_latency_math.avb_latency_math import AVBLatencyMath

from solver.solution import Solution

class ShortestPathSolver:
    def __init__(self):
        self.solution = list()
        self.duration_dict = dict()

    def solve(self, bag):
        shortest_path_timer_start = timer()
        shortest_path = ShortestPath(bag)
        shortest_path_timer_end = timer()

        non_tt_message_list = shortest_path.get_non_tt_message_list()

        self.solution = non_tt_message_list + bag.get_tt_message_list()

        cost = AVBLatencyMath.evaluate(self.solution)

        self.duration_dict[float(cost.get_string().split(" ")[0])] = (shortest_path_timer_end - shortest_path_timer_start)

        return Solution(cost, self.solution)

    def get_solution(self):
        return self.solution

    def get_duration_dict(self):
        return self.duration_dict