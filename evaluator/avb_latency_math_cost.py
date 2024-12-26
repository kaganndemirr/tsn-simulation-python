import sys
from enum import Enum


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
        if self.is_used is not True:
            return sys.float_info.max

        w_1 = 10_000
        w_2 = 3
        w_3 = 1

        return w_1 * self.objective_1 + w_2 * self.objective_2 + w_3 * self.objective_3

    def set_worst_case_delay_to_unicast(self, unicast, worst_case_delay):
        self.worst_case_delay_dict[unicast] = worst_case_delay

    def get_worst_case_delay_dict(self):
        return self.worst_case_delay_dict

    def get_detailed_string(self):
        return f"Total: {self.get_total_cost()} | o1 {self.objective_1}, o2 {self.objective_2}, o3 {self.objective_3} -- {self.worst_case_delay_dict}"

    def reset(self):
        self.is_used = False
        self.objective_1 = int()
        self.objective_2 = float()
        self.objective_3 = float()