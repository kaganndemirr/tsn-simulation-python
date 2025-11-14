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
        self.global_best_cost = AVBLatencyMathCost()
        self.best_solution = list()
        self.cost_lock = threading.Lock()
        self.duration_dict = dict()
        self.non_tt_message_candidate_list = None
        self.running = True
        self.thread_counts = dict()
        self.start_time = time.time()

    def run_meta_heuristic(self, bag, thread_name, tt_message_list, avb_latency_math, k_shortest_path_time):
        metaheuristic_start_time = time.time()
        thread_local_count = 0

        while self.running:
            initial_solution = construct_initial_solution(self.non_tt_message_candidate_list, tt_message_list, avb_latency_math)

            solution = list()
            if bag.get_meta_heuristic_name() == constants.GRASP:
                solution = grasp(initial_solution, avb_latency_math, self.non_tt_message_candidate_list, self.global_best_cost)
            elif bag.get_meta_heuristic_name() == constants.ALO:
                pass

            cost = avb_latency_math.evaluate(solution)

            if cost.get_total_cost() < self.global_best_cost.get_total_cost():
                with self.cost_lock:
                    self.global_best_cost = cost
                    solution_end_time = time.time()
                    self.duration_dict[float(self.global_best_cost.get_string().split(" ")[0])] = k_shortest_path_time + (solution_end_time - metaheuristic_start_time)
                    self.best_solution.clear()
                    self.best_solution = list(solution)

            thread_local_count += 1

            with self.cost_lock:
                self.thread_counts[thread_name] = thread_local_count

    def log_for_each_n_seconds(self):
        while self.running:
            time.sleep(10)
            if self.running:
                elapsed_time = time.time() - self.start_time
                logger.info(f"Elapsed time: {elapsed_time:.1f}. Current Best: {self.global_best_cost.get_string()}")


    def solve(self, bag):
        k_shortest_paths_start = time.time()
        k_shortest_paths = KShortestPath(bag)
        k_shortest_paths_end = time.time()

        k_shortest_path_time = k_shortest_paths_end - k_shortest_paths_start

        self.non_tt_message_candidate_list = k_shortest_paths.get_non_tt_message_candidate_list()

        avb_latency_math = AVBLatencyMath()

        thread_list = []

        for i in range(bag.get_thread_number()):
            thread = threading.Thread(target=self.run_meta_heuristic, args=(bag, str(i + 1), bag.get_tt_message_list(), avb_latency_math, k_shortest_path_time))
            thread.daemon = True
            thread_list.append(thread)
            thread.start()

        info_thread = threading.Thread(target=self.log_for_each_n_seconds)
        info_thread.daemon = True
        info_thread.start()

        time.sleep(bag.get_timeout())

        self.running = False

        for thread in thread_list:
            thread.join(timeout=1.0)

        info_thread.join(timeout=1.0)

        with self.cost_lock:
            for thread_id in sorted(self.thread_counts.keys()):
                count = self.thread_counts[thread_id]
                logger.info(f"Thread {thread_id} finished in {count} iterations.")


        return Solution(self.global_best_cost, self.best_solution)


    def get_solution(self):
        return self.best_solution

    def get_duration_dict(self):
        return self.duration_dict

    def get_non_tt_message_candidate_list(self):
        return self.non_tt_message_candidate_list

