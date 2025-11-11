import random

from application.application import TTApplication
from application.path import Path

from evaluator.avb_latency_math_cost import AVBLatencyMathCost

from message.route import Unicast, UnicastCandidate

from util.helper_functions import convert_graph_to_nx_graph, create_path_as_node_list, create_path_as_edge_list
from util.path_finding_functions import dijkstra_shortest_path

def construct_initial_solution(non_tt_unicast_candidates_list, tt_unicast_list, evaluator):
    initial_solution = list(tt_unicast_list)

    shuffled_non_tt_unicast_candidates_list = list(non_tt_unicast_candidates_list)
    random.shuffle(shuffled_non_tt_unicast_candidates_list)

    for unicast_candidate in shuffled_non_tt_unicast_candidates_list:
        current_best_cost = AVBLatencyMathCost()
        current_best_unicast = None

        for candidate_path in unicast_candidate.get_candidate_path_list():
            current_unicast = Unicast(unicast_candidate.get_application(), unicast_candidate.get_target(), candidate_path)
            initial_solution.append(current_unicast)
            cost = evaluator.evaluate(initial_solution)
            if cost.get_total_cost() < current_best_cost.get_total_cost():
                current_best_cost = cost
                current_best_unicast = current_unicast
            initial_solution.remove(current_unicast)

        initial_solution.append(current_best_unicast)

    return initial_solution


def grasp(initial_solution, evaluator, non_tt_unicast_candidate_list, global_best_cost):
    solution = list(initial_solution)
    cost = evaluator.evaluate(solution)
    best_cost = cost

    mapping = dict()
    for unicast_candidate in non_tt_unicast_candidate_list:
        mapping[unicast_candidate] = unicast_candidate

    for sample in range(len(solution) // 2):
        index = random.randint(0, len(solution) - 1)

        old_unicast = solution[index]

        if old_unicast in mapping.keys():
            old_unicast_candidate = mapping[old_unicast]
        else:
            old_unicast_candidate = None

        if isinstance(old_unicast_candidate, UnicastCandidate):
            for candidate_path in old_unicast_candidate.get_candidate_path_list():
                temp_unicast = Unicast(old_unicast.get_application(), old_unicast.get_target(), candidate_path)
                solution[index] = temp_unicast
                cost = evaluator.evaluate(solution)

                if cost.get_total_cost() < best_cost.get_total_cost():
                    best_cost = cost
                    sample -= 1
                    if cost.get_total_cost() < global_best_cost.get_total_cost():
                        sample -= len(solution) // 2
                    break
                else:
                    solution[index] = old_unicast

    return solution


def find_shortest_path_for_tt_applications(graph, application_list):
    tt_unicast_list = list()
    for application in application_list:
        if isinstance(application, TTApplication):
            for target in application.get_target_list():
                if len(application.get_path_list()) != 0:
                    for path in application.get_path_list():
                        if path.get_target() == target:
                            tt_unicast_list.append(Unicast(application, target, path.get_path()))
                            break
                else:
                    g = convert_graph_to_nx_graph(graph, application.get_source(), target)
                    shortest_path_as_string_list = dijkstra_shortest_path(g, application.get_source().get_name(), target.get_name(), weight='weight')
                    shortest_path_as_node_list = create_path_as_node_list(shortest_path_as_string_list[0], shortest_path_as_string_list[1:-1], shortest_path_as_string_list[-1])
                    shortest_path = create_path_as_edge_list(shortest_path_as_node_list, graph)
                    tt_unicast_list.append(Unicast(application, target, shortest_path))

    return tt_unicast_list