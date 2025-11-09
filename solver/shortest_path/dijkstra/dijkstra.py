from timeit import default_timer as timer

from solver.shortest_path.dijkstra.dijkstra_path import DijkstraPath

from evaluator.avb_latency_math import AVBLatencyMath

from solver.solution import Solution


class Dijkstra:
    def __init__(self):
        self.solution = list()
        self.duration_dict = dict()

    def solve(self, graph, application_list):
        dijkstra_path_timer_start = timer()
        dijkstra_path = DijkstraPath(graph, application_list)
        dijkstra_path_timer_end = timer()

        srt_unicast_list = dijkstra_path.get_srt_unicast_list()
        tt_unicast_list = dijkstra_path.get_tt_unicast_list()

        solution_start = timer()
        self.solution = srt_unicast_list + tt_unicast_list
        solution_end = timer()

        cost = AVBLatencyMathTSNCF.evaluate(self.solution, graph)

        self.duration_dict[float(cost.get_string().split(" ")[0])] = (dijkstra_path_timer_end - dijkstra_path_timer_start) + (solution_end - solution_start)

        return Solution(cost, Multicast.generate_multicast(self.solution))

    def get_solution(self):
        return self.solution

    def get_duration_dict(self):
        return self.duration_dict