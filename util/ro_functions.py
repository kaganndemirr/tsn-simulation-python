import random

from application import TTApplication, SRTApplication

from avb_latency_math.avb_latency_math_cost import AVBLatencyMathCost

from flow import Flow, FlowCandidate

from util.helper_functions import convert_graph_to_nx_graph, create_path_as_node_list, create_path_as_edge_list, generate_multicast_path_for_shortest_path
from util.path_finding_functions import dijkstra_shortest_path

def construct_initial_solution(srt_flow_candidate_list, tt_flow_list, avb_latency_math):
    initial_solution = list(tt_flow_list)

    shuffled_srt_flow_candidate_list = list(srt_flow_candidate_list)
    random.shuffle(shuffled_srt_flow_candidate_list)

    for flow_candidate in shuffled_srt_flow_candidate_list:
        current_best_cost = AVBLatencyMathCost()
        current_best_flow = None

        for candidate_path in flow_candidate.candidate_path_list:
            current_flow = Flow(flow_candidate.application)
            current_flow.path = candidate_path
            initial_solution.append(current_flow)
            cost = avb_latency_math.evaluate(initial_solution)
            if cost.get_total_cost() < current_best_cost.get_total_cost():
                current_best_cost = cost
                current_best_flow = current_flow
            initial_solution.remove(current_flow)

        initial_solution.append(current_best_flow)

    return initial_solution


def grasp(initial_solution, avb_latency_math, srt_flow_candidate_list, global_best_cost):
    solution = list(initial_solution)
    cost = avb_latency_math.evaluate(solution)
    best_cost = cost

    mapping = dict()
    for flow_candidate in srt_flow_candidate_list:
        mapping[flow_candidate] = flow_candidate

    for sample in range(len(solution) // 2):
        index = random.randint(0, len(solution) - 1)

        old_flow = solution[index]

        if isinstance(old_flow.application, SRTApplication):

            old_flow_candidate = None
            for flow_candidate_key, flow_candidate_value in mapping.items():
                if old_flow.application == flow_candidate_key.application:
                    old_flow_candidate = flow_candidate_value
                    break

            if isinstance(old_flow_candidate, FlowCandidate):
                for candidate_path in old_flow_candidate.candidate_path_list:
                    temp_flow = Flow(old_flow_candidate.application)
                    temp_flow.path = candidate_path
                    solution[index] = temp_flow
                    cost = avb_latency_math.evaluate(solution)

                    if cost.get_total_cost() < best_cost.get_total_cost():
                        best_cost = cost
                        sample -= 1
                        if cost.get_total_cost() < global_best_cost.get_total_cost():
                            sample -= len(solution) // 2
                        break
                    else:
                        solution[index] = old_flow

    return solution


def find_shortest_path_for_tt_applications(graph, application_list):
    tt_flow_list = list()
    for application in application_list:
        if isinstance(application, TTApplication):
            tt_flow = Flow(application)

            path_list = list()

            if len(application.explicit_path_list) != 0:
                for path in application.explicit_path_list:
                    path_list.append(path)

            else:
                for target in application.target_list:
                    g = convert_graph_to_nx_graph(graph, application.source, target)
                    shortest_path_as_string_list = dijkstra_shortest_path(g, application.source.name, target.name, weight='weight')
                    shortest_path_as_node_list = create_path_as_node_list(shortest_path_as_string_list[0], shortest_path_as_string_list[1:-1], shortest_path_as_string_list[-1])
                    shortest_path = create_path_as_edge_list(shortest_path_as_node_list, graph)
                    path_list.append(shortest_path)

            tt_flow.path = generate_multicast_path_for_shortest_path(path_list)

            tt_flow_list.append(tt_flow)

    return tt_flow_list

