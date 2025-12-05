from timeit import default_timer as timer

from path_finding.shortest_path import ShortestPath

from worst_case_delay_analysis.avb_latency_math import AVBLatencyMath

from solver.solution import Solution

class ShortestPathSolver:
    def __init__(self):
        self.solution = list()
        self.duration_dict = dict()

    def solve(self, bag):
        shortest_path_timer_start = timer()
        shortest_path = ShortestPath(bag)
        shortest_path_timer_end = timer()

        srt_flow_list = shortest_path.srt_flow_list

        self.solution = srt_flow_list + bag.tt_flow_list

        cost = AVBLatencyMath.evaluate(self.solution)

        self.duration_dict[float(cost.get_string().split(" ")[0])] = (shortest_path_timer_end - shortest_path_timer_start)

        return Solution(cost, self.solution)