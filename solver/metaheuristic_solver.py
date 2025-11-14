import logging
import threading
import time

from avb_latency_math.avb_latency_math import AVBLatencyMath
from avb_latency_math.avb_latency_math_cost import AVBLatencyMathCost

from path_finding.k_shortest_path import KShortestPath
from solver.solution import Solution

from util import constants
from util.ro_functions import construct_initial_solution, grasp

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger()

class MetaheuristicSolver:
    def __init__(self):
        self.cost = AVBLatencyMathCost()
        self.solution = list()
        self.duration_dict = dict()
        self.non_tt_message_candidate_list = None

    def run_meta_heuristic(self, bag, avb_latency_math, k_shortest_path_time):
        metaheuristic_start_time = time.time()

        initial_solution = construct_initial_solution(self.non_tt_message_candidate_list, bag.get_tt_message_list(), avb_latency_math)

        solution = list()
        if bag.get_meta_heuristic_name() == constants.GRASP:
            solution = grasp(initial_solution, avb_latency_math, self.non_tt_message_candidate_list, self.cost)
        elif bag.get_meta_heuristic_name() == constants.ALO:
            pass

        cost = avb_latency_math.evaluate(solution)

        if cost.get_total_cost() < self.cost.get_total_cost():
            self.cost = cost
            solution_end_time = time.time()
            self.duration_dict[float(self.cost.get_string().split(" ")[0])] = k_shortest_path_time + (solution_end_time - metaheuristic_start_time)
            self.solution.clear()
            self.solution = list(solution)

        return solution


    def solve(self, bag):
        k_shortest_paths_start = time.time()
        k_shortest_paths = KShortestPath(bag)
        k_shortest_paths_end = time.time()

        k_shortest_path_time = k_shortest_paths_end - k_shortest_paths_start

        self.non_tt_message_candidate_list = k_shortest_paths.get_non_tt_message_candidate_list()

        avb_latency_math = AVBLatencyMath()

        solution = list()
        for iteration in range(1, bag.get_max_iteration_number() + 1):
            solution = self.run_meta_heuristic(bag, avb_latency_math, k_shortest_path_time)

            if iteration % 100 == 0:
                logger.info(f"Iteration {iteration}, BestCost {self.cost.get_string()}")

        self.cost = avb_latency_math.evaluate(solution)
        self.solution = solution

        return Solution(self.cost, self.solution)


    def get_solution(self):
        return self.solution

    def get_duration_dict(self):
        return self.duration_dict

    def get_non_tt_message_candidate_list(self):
        return self.non_tt_message_candidate_list

