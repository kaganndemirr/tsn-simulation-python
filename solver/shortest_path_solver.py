from timeit import default_timer as timer

from path_finding.shortest_path import ShortestPath

from evaluator.avb_latency_math import AVBLatencyMath

from solver.solution import Solution

from util.helper_functions import generate_multicast_if_necessary_for_shortest_path

class ShortestPathSolver:
    def __init__(self):
        self.solution = list()
        self.duration_dict = dict()

    def solve(self, graph, application_list, algorithm, tt_message_list):
        shortest_path_timer_start = timer()
        shortest_path = ShortestPath(graph, application_list, algorithm)
        shortest_path_timer_end = timer()

        non_tt_message_list = shortest_path.get_non_tt_message_list()

        message_list = non_tt_message_list + tt_message_list

        generate_multicast_if_necessary_for_shortest_path(message_list)

        self.solution = message_list

        cost = AVBLatencyMath.evaluate(self.solution)

        self.duration_dict[float(cost.get_string().split(" ")[0])] = (shortest_path_timer_end - shortest_path_timer_start)

        return Solution(cost, Multicast.generate_multicast(self.solution))

    def get_solution(self):
        return self.solution

    def get_duration_dict(self):
        return self.duration_dict