import logging
import time

from avb_latency_math.avb_latency_math import AVBLatencyMath
from avb_latency_math.avb_latency_math_cost import AVBLatencyMathCost

from path_finding.k_shortest_path import KShortestPath
from solver.solution import Solution

from util import constants
from util.ro_functions import construct_initial_solution, grasp


class MetaheuristicSolver:
    def __init__(self):
        self.best_cost = AVBLatencyMathCost()
        self.best_solution = list()
        self.duration_dict = dict()
        self.srt_flow_candidate_list = None

    def run_meta_heuristic(self, bag, avb_latency_math, k_shortest_path_time):
        metaheuristic_start_time = time.time()

        initial_solution = construct_initial_solution(self.srt_flow_candidate_list, bag.tt_flow_list, avb_latency_math)
        solution = grasp(initial_solution, avb_latency_math, self.srt_flow_candidate_list, self.best_cost)

        cost = avb_latency_math.evaluate(solution)

        if cost.get_total_cost() < self.best_cost.get_total_cost():
            self.best_cost = cost
            solution_end_time = time.time()
            self.duration_dict[float(self.best_cost.get_string().split(" ")[0])] = k_shortest_path_time + (solution_end_time - metaheuristic_start_time)
            self.best_solution.clear()
            self.best_solution = list(solution)


    def solve(self, bag):
        k_shortest_paths_start = time.time()
        k_shortest_paths = KShortestPath(bag)
        k_shortest_paths_end = time.time()

        k_shortest_path_time = k_shortest_paths_end - k_shortest_paths_start

        self.srt_flow_candidate_list = k_shortest_paths.get_srt_flow_candidate_list()

        avb_latency_math = AVBLatencyMath()

        for iteration in range(1, bag.max_iteration_number + 1):
            self.run_meta_heuristic(bag, avb_latency_math, k_shortest_path_time)

            if iteration % constants.ITERATION_LOG == 0:
                print(f"Iteration {iteration}, CurrentBest {self.best_cost.get_string()}")


        return Solution(self. best_cost, self.best_solution)


    def get_solution(self):
        return self.best_solution

    def get_duration_dict(self):
        return self.duration_dict

    def get_srt_flow_candidate_list(self):
        return self.srt_flow_candidate_list

