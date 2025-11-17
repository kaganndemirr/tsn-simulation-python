import random

from application.application import TTApplication, NonTTApplication

from avb_latency_math.avb_latency_math_cost import AVBLatencyMathCost

from message.message import Message, MessageCandidate

from util.helper_functions import convert_graph_to_nx_graph, create_path_as_node_list, create_path_as_edge_list, generate_multicast_path_for_shortest_path
from util.path_finding_functions import dijkstra_shortest_path

def construct_initial_solution(non_tt_message_candidate_list, tt_message_list, avb_latency_math):
    initial_solution = list(tt_message_list)

    shuffled_non_tt_message_candidate_list = list(non_tt_message_candidate_list)
    random.shuffle(shuffled_non_tt_message_candidate_list)

    for message_candidate in shuffled_non_tt_message_candidate_list:
        current_best_cost = AVBLatencyMathCost()
        current_best_message = None

        for candidate_path in message_candidate.get_candidate_path_list():
            current_message = Message(message_candidate.get_application())
            current_message.set_path(candidate_path)
            initial_solution.append(current_message)
            cost = avb_latency_math.evaluate(initial_solution)
            if cost.get_total_cost() < current_best_cost.get_total_cost():
                current_best_cost = cost
                current_best_message = current_message
            initial_solution.remove(current_message)

        initial_solution.append(current_best_message)

    return initial_solution


def grasp(initial_solution, avb_latency_math, non_tt_message_candidate_list, global_best_cost):
    solution = list(initial_solution)
    cost = avb_latency_math.evaluate(solution)
    best_cost = cost

    mapping = dict()
    for message_candidate in non_tt_message_candidate_list:
        mapping[message_candidate] = message_candidate

    for sample in range(len(solution) // 2):
        index = random.randint(0, len(solution) - 1)

        old_message = solution[index]

        if isinstance(old_message.get_application(), NonTTApplication):

            old_message_candidate = None
            for message_candidate_key, message_candidate_value in mapping.items():
                if old_message.get_application() == message_candidate_key.get_application():
                    old_message_candidate = message_candidate_value
                    break

            if isinstance(old_message_candidate, MessageCandidate):
                for candidate_path in old_message_candidate.get_candidate_path_list():
                    temp_message = Message(old_message_candidate.get_application())
                    temp_message.set_path(candidate_path)
                    solution[index] = temp_message
                    cost = avb_latency_math.evaluate(solution)

                    if cost.get_total_cost() < best_cost.get_total_cost():
                        best_cost = cost
                        sample -= 1
                        if cost.get_total_cost() < global_best_cost.get_total_cost():
                            sample -= len(solution) // 2
                        break
                    else:
                        solution[index] = old_message

    return solution


def find_shortest_path_for_tt_applications(graph, application_list):
    tt_message_list = list()
    for application in application_list:
        if isinstance(application, TTApplication):
            tt_message = Message(application)

            path_list = list()

            if len(application.get_explicit_path_list()) != 0:
                for path in application.get_explicit_path_list():
                    path_list.append(path)

            else:
                for target in application.get_target_list():
                    g = convert_graph_to_nx_graph(graph, application.get_source(), target)
                    shortest_path_as_string_list = dijkstra_shortest_path(g, application.get_source().get_name(), target.get_name(), weight='weight')
                    shortest_path_as_node_list = create_path_as_node_list(shortest_path_as_string_list[0], shortest_path_as_string_list[1:-1], shortest_path_as_string_list[-1])
                    shortest_path = create_path_as_edge_list(shortest_path_as_node_list, graph)
                    path_list.append(shortest_path)

            path = generate_multicast_path_for_shortest_path(path_list)

            tt_message.set_path(path)

            tt_message_list.append(tt_message)

    return tt_message_list

def set_ant_path(ant_solution, non_tt_application, ant_path):
    for ant in ant_solution:
        if ant.get_application() == non_tt_application:
            ant.set_path(ant_path)
            break

def alo(ant_solution, ant_lion_solution, avb_latency_math, non_tt_message_candidate_list):
    elite_solution = list(ant_lion_solution)

    for non_tt_message_candidate in non_tt_message_candidate_list:
        random_ant_lion_index, random_ant_index = random.sample(range(len(non_tt_message_candidate.get_candidate_path_list())), 2)
        ant_path = non_tt_message_candidate.get_candidate_path_list()[random_ant_index]

        set_ant_path(ant_solution, non_tt_message_candidate.get_application(), ant_path)

    if avb_latency_math.evaluate(ant_solution).get_total_cost() < avb_latency_math.evaluate(ant_lion_solution).get_total_cost():
        ant_lion_solution = ant_solution

    if avb_latency_math.evaluate(ant_lion_solution).get_total_cost() < avb_latency_math.evaluate(elite_solution).get_total_cost():
        elite_solution = ant_lion_solution

    return elite_solution

