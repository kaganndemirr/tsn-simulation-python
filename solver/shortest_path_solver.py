from timeit import default_timer as timer

from path_finding.shortest_path import ShortestPath

from evaluator.avb_latency_math import AVBLatencyMath

from solver.solution import Solution

from message.multicast import Multicast

class ShortestPathSolver:
    def __init__(self):
        self.solution = list()
        self.duration_dict = dict()

    def solve(self, graph, application_list, algorithm, tt_unicast_list):
        dijkstra_path_timer_start = timer()
        dijkstra_path = ShortestPath(graph, application_list, algorithm)
        dijkstra_path_timer_end = timer()

        non_tt_unicast_list = dijkstra_path.get_non_tt_unicast_list()

        multicast_list = Multicast.generate_multicast(non_tt_unicast_list + tt_unicast_list)

        self.solution = multicast_list

        cost = AVBLatencyMath.evaluate(self.solution)

        self.duration_dict[float(cost.get_string().split(" ")[0])] = (dijkstra_path_timer_end - dijkstra_path_timer_start)

        return Solution(cost, Multicast.generate_multicast(self.solution))

    def get_solution(self):
        return self.solution

    def get_duration_dict(self):
        return self.duration_dict