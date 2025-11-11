import math
import os

from application import SRTApplication

from util.shaper_methods import find_average_with_es, find_average_with_sw

class PHYWPMResultShaper:
    def __init__(self, phy_wpm_holder):
        self.topology_output_location = os.path.join("results", phy_wpm_holder.get_routing(),
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

        self.result_output_location = os.path.join("results", phy_wpm_holder.get_routing(),
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
        self.utilization_dict = dict()

    def write_solution_to_file(self, solution):
        file_path = os.path.join(self.topology_output_location, "Routes.txt")
        with open(file_path, "w") as writer:
            for unicast in solution:
                if isinstance(unicast.get_application(), SRTApplication):
                    writer.write(f"{unicast.get_application().get_name()}: {unicast.get_path()}\n")

            writer.write(f"Average Length (ESs included): {find_average_with_es(solution)}\n")
            writer.write(f"Average Length (between switches): {find_average_with_sw(solution)}\n")

    def write_worst_case_delays_to_file(self, worst_case_delay_dict):
        worst_case_delay_file_path = os.path.join(self.topology_output_location, "WCDs.txt")
        main_results_path = os.path.join(self.result_output_location, "Results.txt")
        total = sum(worst_case_delay_dict.values())
        mean = total / len(worst_case_delay_dict)
        variance = sum((v - mean) ** 2 for v in worst_case_delay_dict.values()) / len(worst_case_delay_dict)
        std = math.sqrt(variance)

        with open(worst_case_delay_file_path, "w") as worst_case_delay_writer, open(main_results_path, "a") as main_result_writer:
            for key, value in worst_case_delay_dict.items():
                worst_case_delay_writer.write(f"{key.get_application().get_name()}: {key.get_application().get_deadline()} {value}\n")
            worst_case_delay_writer.write(f"\nAverage WCD: {mean}\nVariance: {variance}\nStd: {std}\n")
            main_result_writer.write(f"Average WCD: {mean}, Variance: {variance}, Std: {std}\n")

    def write_link_utilizations_to_file(self, solution, graph, rate):
        for unicast in solution:
            for edge in unicast.get_path():
                self.utilization_dict[edge] = self.utilization_dict.get(edge, 0) + unicast.get_application().get_message_size_mbps() / rate

        total = sum(self.utilization_dict.values())
        unused_links = len(graph.get_edges()) - len(self.utilization_dict)
        mean = total / len(graph.get_edges())
        variance = sum((util - mean) ** 2 for util in self.utilization_dict.values())
        variance += unused_links * (mean ** 2)
        variance /= len(graph.get_edges())
        std = math.sqrt(variance)

        main_results_path = os.path.join(self.result_output_location, "Results.txt")
        with open(main_results_path, "a") as main_result_writer:
            main_result_writer.write(f"Unused Links: {unused_links} / {len(graph.get_edges())}, Average Utilization: {mean}, Std: {std}\n")

    def write_duration_map(self, duration_dict):
        sorted_duration_list = sorted(duration_dict.items())

        main_results_path = os.path.join(self.result_output_location, "Results.txt")
        with open(main_results_path, "a") as main_result_writer:
            main_result_writer.write(f"Costs and computation times(sec): {sorted_duration_list}\n")

    def write_srt_unicast_candidate_list(self, srt_unicat_candidate_list):
        srt_unicast_candidate_list_path = os.path.join(self.topology_output_location, "SRRCandidateRoutes.txt")
        with open(srt_unicast_candidate_list_path, 'w') as srt_unicast_candidate_list_writer:
            for unicast_candidate in srt_unicat_candidate_list:
                i = 0
                for candidate_path in unicast_candidate.get_candidate_path_list():
                    srt_unicast_candidate_list_writer.write(f"{unicast_candidate.get_application().get_name()}_{i}\t{candidate_path}\n")
                    i += 1
