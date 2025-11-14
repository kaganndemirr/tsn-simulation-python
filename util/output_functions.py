import math
import os

from natsort import natsorted

from application.application import NonTTApplication, TTApplication


def write_path_to_file(scenario_output_path, solution):
    with open(os.path.join(scenario_output_path, "paths.txt"), "w") as path_writer:
        path_writer.write("Non TT Messages\n")
        for message in solution:
            if isinstance(message.get_application(), NonTTApplication):
                path_writer.write(message.get_application().get_name() + "\t" + str(message.get_path()) + "\n")

        path_writer.write("\n")

        path_writer.write("TT Messages\n")
        for message in solution:
            if isinstance(message.get_application(), TTApplication):
                path_writer.write(message.get_application().get_name() + "\t" + str(message.get_path()) + "\n")

def write_worst_case_delay_to_file(scenario_output_path, worst_case_delay_dict, result_output_path):

    with open(os.path.join(scenario_output_path, "worst_case_delays.txt"), "w") as worst_case_delays_writer:
        total = 0
        for message, worst_case_delay in worst_case_delay_dict.items():
            total += worst_case_delay
            worst_case_delays_writer.write(message.get_application().get_name() + "\t" + str(message.get_application().get_deadline()) + "\t" + str(worst_case_delay) + "\n")

        mean = total / len(worst_case_delay_dict)
        worst_case_delays_writer.write("Average WCD\t" + str(mean) + ",\t")

        variance = 0
        for message, worst_case_delay in worst_case_delay_dict.items():
            variance += math.pow((worst_case_delay - mean), 2)

        variance /= len(worst_case_delay_dict)
        worst_case_delays_writer.write("Variance\t" + str(variance) + ",\t")

        standard_deviation = math.sqrt(variance)
        worst_case_delays_writer.write("Standard Deviation\t" + str(standard_deviation) + "\n")

    with open(os.path.join(result_output_path, "results.txt"), "a") as result_writer:
        result_writer.write("Average WCD\t" + str(mean) + "\t" + "Variance\t" + str(variance) + "\t" + "Standard Deviation\t" + str(standard_deviation) + "\n")

def write_link_utilization_to_file(solution, graph, scenario_output_path, result_output_path):
    utilization_dict = dict()
    for message in solution:
        for edge in message.get_path():
            if edge not in utilization_dict.keys():
                utilization_dict[edge] = 0
            else:
                utilization_dict[edge] += message.get_application().get_message_size_mbps() / edge.get_rate()

    unused_link_number = len(graph.get_edge_list()) - len(utilization_dict)

    for edge in graph.get_edge_list():
        if edge not in utilization_dict.keys():
            utilization_dict[edge] = 0

    name_sorted_utilization_dict = dict(natsorted(utilization_dict.items(),key=lambda item: item[0].get_source().get_name()))

    utilization_sorted_utilization_dict = dict(sorted(utilization_dict.items(), key=lambda item: item[1], reverse=True))

    max_loaded_link_utilization = next(iter(utilization_sorted_utilization_dict.values()), None)

    max_loaded_link_number = 0
    for edge, utilization in utilization_sorted_utilization_dict.items():
        if max_loaded_link_utilization == utilization:
            max_loaded_link_number += 1
        else:
            break

    total = 0
    for edge, utilization in utilization_dict.items():
        total += utilization


    mean = total / len(graph.get_edge_list())

    variance = 0
    for edge, utilization in utilization_dict.items():
        variance += math.pow((utilization - mean), 2)

    for i in range(0, unused_link_number):
        variance += math.pow((0 - mean), 2)

    variance /= len(graph.get_edge_list())

    standard_deviation = math.sqrt(variance)

    with open(os.path.join(scenario_output_path, "link_utilizations_sorted_by_names.txt"), "w") as link_utilizations_sorted_by_names_writer:
        for edge, utilization in name_sorted_utilization_dict.items():
            link_utilizations_sorted_by_names_writer.write(str(edge) + "\t" + str(utilization) + "\n")

        link_utilizations_sorted_by_names_writer.write("Unused Links\t" + str(unused_link_number) + "/" + str(len(graph.get_edge_list())) + ",\t")
        link_utilizations_sorted_by_names_writer.write("Max Loaded Link Number\t" + str(max_loaded_link_number) + ",\t")
        link_utilizations_sorted_by_names_writer.write("Max Loaded Link Utilization\t" + str(max_loaded_link_utilization) + ",\t")
        link_utilizations_sorted_by_names_writer.write("Average Loaded Link Number\t" + str(mean) + ",\t")
        link_utilizations_sorted_by_names_writer.write("Variance\t" + str(variance) + ",\t")
        link_utilizations_sorted_by_names_writer.write("Standard Deviation\t" + str(standard_deviation) + "\n")

    with open(os.path.join(scenario_output_path, "link_utilizations_sorted_by_utilizations.txt"), "w") as link_utilizations_sorted_by_utilizations_writer:
        for edge, utilization in utilization_sorted_utilization_dict.items():
            link_utilizations_sorted_by_utilizations_writer.write(str(edge) + "\t" + str(utilization) + "\n")

        link_utilizations_sorted_by_utilizations_writer.write("Unused Links\t" + str(unused_link_number) + "/" + str(len(graph.get_edge_list())) + ",\t")
        link_utilizations_sorted_by_utilizations_writer.write("Max Loaded Link Number\t" + str(max_loaded_link_number) + ",\t")
        link_utilizations_sorted_by_utilizations_writer.write("Max Loaded Link Utilization\t" + str(max_loaded_link_utilization) + ",\t")
        link_utilizations_sorted_by_utilizations_writer.write("Average Loaded Link Number\t" + str(mean) + ",\t")
        link_utilizations_sorted_by_utilizations_writer.write("Variance\t" + str(variance) + ",\t")
        link_utilizations_sorted_by_utilizations_writer.write("Standard Deviation\t" + str(standard_deviation) + "\n")

    with open(os.path.join(result_output_path, "results.txt"), "a") as results_writer:
        results_writer.write("Unused Links\t" + str(unused_link_number) + "/" + str(len(graph.get_edge_list())) + ",\t")
        results_writer.write("Max Loaded Link Number\t" + str(max_loaded_link_number) + ",\t")
        results_writer.write("Max Loaded Link Utilization\t" + str(max_loaded_link_utilization) + ",\t")
        results_writer.write("Average Loaded Link Number\t" + str(mean) + ",\t")
        results_writer.write("Variance\t" + str(variance) + ",\t")
        results_writer.write("Standard Deviation\t" + str(standard_deviation) + "\n")

def write_duration_to_file(duration_dict, result_output_path):
    sorted_duration_dict = dict(sorted(duration_dict.items(), key=lambda item: item[0], reverse=True))

    with open(os.path.join(result_output_path, "results.txt"), "a") as results_writer:
        results_writer.write("Costs and computation times(sec)\t" + str(sorted_duration_dict) + "\n")