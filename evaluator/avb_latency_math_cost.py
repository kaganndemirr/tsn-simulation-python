import os
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
        if self.is_used:
            return float('inf')

        w_1 = 10_000
        w_2 = 3
        w_3 = 1

        return w_1 * self.objective_1 + w_2 * self.objective_2 + w_3 * self.objective_3

    def set_worst_case_delay_to_multicast(self, multicast, worst_case_delay):
        self.worst_case_delay_dict[multicast] = worst_case_delay

    def get_worst_case_delay_dict(self):
        return self.worst_case_delay_dict

    def get_string(self):
        return f"{self.get_total_cost()} (current o1 = {self.objective_1}, o2 {self.objective_2}, o3 {self.objective_3})"

    def get_detailed_string(self):
        return f"Total: {self.get_total_cost()} | o1 = {self.objective_1}, o2 = {self.objective_2}, o3 = {self.objective_3} -- {self.worst_case_delay_dict}"

    def reset(self):
        self.is_used = False
        self.objective_1 = int()
        self.objective_2 = float()
        self.objective_3 = float()

    def write_phy_shortest_path_result_to_file(self, routing, path_finder_method, algorithm, topology_name, application_name):
        main_folder_output_location = os.path.join("results", routing, path_finder_method, algorithm, topology_name + "_" +  application_name)
        os.makedirs(main_folder_output_location, exist_ok=True)

        result_file_output_location = os.path.join("results", routing, path_finder_method, algorithm)

        with open(os.path.join(result_file_output_location, "Results.txt"), "a") as result_writer:
            result_writer.write(f"{topology_name}_{application_name}\n")
            result_writer.write(f"cost = {self.get_total_cost()}, o1 = {self.objective_1}, o2 = {self.objective_2}, o3 = {self.objective_3}\n")

    def write_phy_result_to_file(self, phy_holder):
        main_folder_output_location = os.path.join("results", phy_holder.get_routing(),
                                                   phy_holder.get_path_method(),
                                                   phy_holder.get_algorithm(),
                                                   str(phy_holder.get_k()),
                                                   phy_holder.get_topology_name() + "_" + phy_holder.get_application_name())
        os.makedirs(main_folder_output_location, exist_ok=True)

        result_file_output_location = os.path.join("results", phy_holder.get_routing(),
                                                   phy_holder.get_path_method(),
                                                   phy_holder.get_algorithm(),
                                                   str(phy_holder.get_k()))

        with open(os.path.join(result_file_output_location, "Results.txt"), "a") as result_writer:
            result_writer.write(
                f"{phy_holder.get_topology_name()}_{phy_holder.get_application_name()}\n")
            result_writer.write(
                f"cost = {self.get_total_cost()}, o1 = {self.objective_1}, o2 = {self.objective_2}, o3 = {self.objective_3}\n")

    def write_phy_wpm_result_to_file(self, phy_wpm_holder):
        main_folder_output_location = os.path.join("results", phy_wpm_holder.get_routing(),
                                                   phy_wpm_holder.get_path_method(),
                                                   phy_wpm_holder.get_algorithm(),
                                                   str(phy_wpm_holder.get_k()),
                                                   phy_wpm_holder.get_wpm_objective(),
                                                   str(phy_wpm_holder.get_w_srt()),
                                                   str(phy_wpm_holder.get_w_tt()),
                                                   str(phy_wpm_holder.get_w_length()),
                                                   str(phy_wpm_holder.get_w_util()),
                                                   phy_wpm_holder.get_wpm_version(),
                                                   phy_wpm_holder.get_wpm_value_type(),
                                                   phy_wpm_holder.get_topology_name() + "_" + phy_wpm_holder.get_application_name())
        os.makedirs(main_folder_output_location, exist_ok=True)

        result_file_output_location = os.path.join("results", phy_wpm_holder.get_routing(),
                                                   phy_wpm_holder.get_path_method(),
                                                   phy_wpm_holder.get_algorithm(),
                                                   str(phy_wpm_holder.get_k()),
                                                   phy_wpm_holder.get_wpm_objective(),
                                                   str(phy_wpm_holder.get_w_srt()),
                                                   str(phy_wpm_holder.get_w_tt()),
                                                   str(phy_wpm_holder.get_w_length()),
                                                   str(phy_wpm_holder.get_w_util()),
                                                   phy_wpm_holder.get_wpm_version(),
                                                   phy_wpm_holder.get_wpm_value_type())

        with open(os.path.join(result_file_output_location, "Results.txt"), "a") as result_writer:
            result_writer.write(f"{phy_wpm_holder.get_topology_name()}_{phy_wpm_holder.get_application_name()}\n")
            result_writer.write(f"cost = {self.get_total_cost()}, o1 = {self.objective_1}, o2 = {self.objective_2}, o3 = {self.objective_3}\n")