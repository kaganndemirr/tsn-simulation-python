import math
import os

from application.application import NonTTApplication, TTApplication


def write_path_to_file(scenario_output_path, solution):
    with open(os.path.join(scenario_output_path, "Paths.txt"), "w") as path_writer:
        path_writer.write("Non TT Messages\n")
        for message in solution:
            if isinstance(message.get_application(), NonTTApplication):
                path_writer.write(message.get_application().get_name() + "\t" + str(message.get_path_list()[0]) + "\n")

        path_writer.write("\n")

        path_writer.write("TT Messages\n")
        for message in solution:
            if isinstance(message.get_application(), TTApplication):
                path_writer.write(message.get_application().get_name() + "\t" + str(message.get_path_list()[0]) + "\n")

def write_worst_case_delay_to_file(scenario_output_path, worst_case_delay_dict, result_output_path):

    with open(os.path.join(scenario_output_path, "WorstCaseDelays.txt"), "w") as worst_case_delay_writer:
        total = 0
        for message, worst_case_delay in worst_case_delay_dict.items():
            total += worst_case_delay
            worst_case_delay_writer.write(message.get_application().get_name() + "\t" + str(message.get_application().get_deadline()) + "\t" + str(worst_case_delay) + "\n")

        mean = total / len(worst_case_delay_dict)
        worst_case_delay_writer.write("Average WCD\t" + str(mean) + ",\t")

        variance = 0
        for message, worst_case_delay in worst_case_delay_dict.items():
            variance += math.pow((worst_case_delay - mean), 2)

        variance /= len(worst_case_delay_dict)
        worst_case_delay_writer.write("Variance\t" + str(variance) + ",\t")

        standard_deviation = math.sqrt(variance)
        worst_case_delay_writer.write("Standard Deviation\t" + str(standard_deviation) + "\n")


    with open(os.path.join(result_output_path, "Results.txt"), "a") as result_writer:
        result_writer.write("Average WCD\t" + str(mean) + "\t" + "Variance\t" + str(variance) + "\t" + "Standard Deviation\t" + str(standard_deviation))


def write_link_utilization_to_file(solution, graph):
    utilization_dict = dict()
    for message in solution:
        for edge in message.get_path_list()[0]:
            if edge not in utilization_dict.keys():
                utilization_dict[edge] = 0
            else:
                utilization_dict[edge] += message.get_application().get_message_size_mbps() / edge.get_rate()

    total = 0
    for edge, utilization in utilization_dict.items():
        total += utilization

    unused_link_number = len(graph.get_edge_list()) - len(utilization_dict)

    for edge in graph.get_edge_list():
        if edge not in utilization_dict.keys():
            utilization_dict[edge] = 0
