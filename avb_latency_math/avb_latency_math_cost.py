import os
from enum import Enum

from util.helper_functions import create_result_output_path


class Objective(Enum):
    ONE = 'one'
    TWO = 'two'
    THREE = 'three'


class AVBLatencyMathCost:
    def __init__(self):
        self.objective_1 = int()
        self.objective_2 = float()
        self.objective_3 = float()
        self.is_used = False
        self.worst_case_delay_dict = dict()

    def add(self, objective, value):
        match objective:
            case 'one':
                self.objective_1 += value
            case 'two':
                self.objective_2 += value
            case 'three':
                self.objective_3 += value

        self.is_used = True

    def get_total_cost(self):
        if not self.is_used:
            return float('inf')

        w_1 = 10_000
        w_2 = 3
        w_3 = 1

        return w_1 * self.objective_1 + w_2 * self.objective_2 + w_3 * self.objective_3

    def set_worst_case_delay_to_message(self, message, worst_case_delay):
        self.worst_case_delay_dict[message] = worst_case_delay

    def get_worst_case_delay_dict(self):
        return self.worst_case_delay_dict

    def get_string(self):
        return f"{self.get_total_cost()} (current o1 = {self.objective_1}, o2 = {self.objective_2}, o3 = {self.objective_3})"

    def get_detailed_string(self):
        return f"Total: {self.get_total_cost()} | o1 = {self.objective_1}, o2 = {self.objective_2}, o3 = {self.objective_3} -- {self.worst_case_delay_dict}"

    def reset(self):
        self.is_used = False
        self.objective_1 = int()
        self.objective_2 = float()
        self.objective_3 = float()

    def write_result_to_file(self, bag):
        result_output_path = create_result_output_path(bag)
        with open(os.path.join(result_output_path, "results.txt"), "a") as result_writer:
            result_writer.write(f"{bag.get_topology_name()}_{bag.get_scenario_name()}\n")
            result_writer.write(f"cost = {self.get_total_cost()}, o1 = {self.objective_1}, o2 = {self.objective_2}, o3 = {self.objective_3}\n")
