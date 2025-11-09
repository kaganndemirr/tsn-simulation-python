import copy
import logging
import threading
import time

from evaluator.avb_latency_math_cost import AVBLatencyMathCost

from solver.yen.yen_k_shortest_path import YenKShortestPath
from solver.solution import Solution

from util.tsncf_methods import construct_initial_solution, grasp_metaheuristic

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger()

class GRASP:
    def __init__(self, k):
        self.k = k
        self.cost_lock = threading.Lock()
        self.global_best_cost = AVBLatencyMathCost()
        self.best_solution = list()
        self.evaluator = None
        self.yen_k_shortest_path_time = None
        self.srt_unicast_candidate_list = None
        self.tt_unicast_list = None
        self.duration_dict = dict()
        self.timeout = int()
        self.running = True
        self.thread_counts = dict()
        self.start_time = time.time()

    def run_grasp(self, thread_name):
        grasp_start = time.time()
        thread_local_count = 0
        while self.running:
            initial_solution = construct_initial_solution(self.srt_unicast_candidate_list, self.tt_unicast_list, self.k, self.evaluator)
            solution = grasp_metaheuristic(initial_solution, self.evaluator, self.srt_unicast_candidate_list, self.global_best_cost)

            cost = self.evaluator.evaluate(solution)

            with self.cost_lock:
                if cost.get_total_cost() < self.global_best_cost.get_total_cost():
                    self.global_best_cost = cost
                    best_cost_end = time.time()
                    self.duration_dict[float(self.global_best_cost.get_string().split(" ")[0])] = self.yen_k_shortest_path_time + (best_cost_end - grasp_start)
                    self.best_solution.clear()
                    self.best_solution = copy.deepcopy(solution)

            thread_local_count += 1

            with self.cost_lock:
                self.thread_counts[thread_name] = thread_local_count

    def log_for_each_n_seconds(self):
        while self.running:
            time.sleep(10)
            if self.running:
                elapsed_time = time.time() - self.start_time
                print(f"Elapsed time: {elapsed_time:.1f}. Current Best: {self.global_best_cost}")


    def solve(self, graph, application_list, evaluator, thread_number, timeout):
        yen_k_shortest_paths_start = time.time()
        yen_k_shortest_paths = YenKShortestPath(graph, application_list, self.k)
        yen_k_shortest_paths_end = time.time()

        self.yen_k_shortest_path_time = yen_k_shortest_paths_end - yen_k_shortest_paths_start

        self.srt_unicast_candidate_list = yen_k_shortest_paths.get_srt_unicast_candidate_list()
        self.tt_unicast_list = yen_k_shortest_paths.get_tt_unicast_list()

        self.evaluator = evaluator

        threads = []

        for i in range(thread_number):
            thread = threading.Thread(target=self.run_grasp, args=(str(i + 1)))
            thread.daemon = True
            threads.append(thread)
            thread.start()

        info_thread = threading.Thread(target=self.log_for_each_n_seconds)
        info_thread.daemon = True
        info_thread.start()

        time.sleep(timeout)

        self.running = False

        for thread in threads:
            thread.join(timeout=1.0)
        info_thread.join(timeout=1.0)

        with self.cost_lock:
            for thread_id in sorted(self.thread_counts.keys()):
                count = self.thread_counts[thread_id]
                print(f"Thread {thread_id} finished in {count} iterations.")

        return Solution(self.global_best_cost, Multicast.generate_multicast(self.best_solution))


    def get_solution(self):
        return self.best_solution

    def get_duration_dict(self):
        return self.duration_dict

    def get_srt_unicast_candidate_list(self):
        return self.srt_unicast_candidate_list

