import argparse
import logging
import os
import json

from util import constants

from parser.application_parser import application_parser
from parser.topology_parser import topology_parser

from avb_latency_math.avb_latency_math import AVBLatencyMath

from tsnsched.tsnsched import TSNsched
from tsnsched.input_json import TSNschedInputJson
from tsnsched.run_tsnsched import run_tsnsched
from tsnsched.output_json import parse_output_json

from util.bag import Bag
from util.helper_functions import get_topology_and_scenario_name, create_scenario_output_path, create_tsnsched_output_path, create_result_output_path
from util.log_functions import create_info, found_solution, found_no_solution
from util.ro_functions import find_shortest_path_for_tt_applications
from util.output_functions import write_path_to_file, write_worst_case_delay_to_file, write_link_utilization_to_file, write_duration_to_file, write_srt_flow_candidate_path_list_to_file

from solver.shortest_path_solver import ShortestPathSolver
from solver.metaheuristic_solver import MetaheuristicSolver

parser = argparse.ArgumentParser(prog='tsn_simulation')
parser.add_argument('-topology', help="Use given file as topology")
parser.add_argument('-scenario', help="Use given file as scenario")
parser.add_argument('-rate', help="Edge rate (Default: 1000 mbps)", default=constants.DEFAULT_RATE, type=int)
parser.add_argument('-srt_idle_slope', help="SRT Queue Idle Slope (Default: 0.75)", default=constants.DEFAULT_NON_TT_IDLE_SLOPE, type=float)
parser.add_argument('-cmi', help="CMI value for SRT Applications (Default: 125)", default=constants.DEFAULT_CMI, type=float)

parser.add_argument('-k', help="Value of K for search-space reduction (Default: 50)", default=constants.DEFAULT_K, type=int)
parser.add_argument('-path_finding_method', help="Choose path finder method (Default = yen) (Choices: shortestPath, yen)", default=constants.YEN)

parser.add_argument('-max_iteration_number', help="Max Iteration Number (Default: 1000)", default=constants.DEFAULT_MAX_ITERATION_NUMBER, type=int)

args = parser.parse_args()

topology_file = args.topology
scenario_file = args.scenario

rate = args.rate
srt_idle_slope = args.srt_idle_slope
cmi = args.cmi
k = args.k
path_finding_method = args.path_finding_method
max_iteration_number = args.max_iteration_number

avb_latency_math = AVBLatencyMath()

bag = Bag()

print(f"Parsing topology from {os.path.basename(topology_file)}!")
graph = topology_parser(topology_file, rate, srt_idle_slope)
bag.graph = graph
print(f"Topology successfully parsed {os.path.basename(topology_file)}!")

print(f"Parsing application from {os.path.basename(scenario_file)}!")
application_list = application_parser(scenario_file, graph, cmi)
bag.application_list = application_list
print(f"Application successfully parsed {os.path.basename(scenario_file)}!")

print(f"Finding shortest paths for TT Applications!")
tt_flow_list = find_shortest_path_for_tt_applications(graph, application_list)
bag.tt_flow_list = tt_flow_list
print(f"Finding shortest paths successfully for TT Applications!")

topology_name, scenario_name = get_topology_and_scenario_name(topology_file, scenario_file)
bag.topology_name = topology_name
bag.scenario_name = scenario_name

if path_finding_method == "shortest_path":
    shortest_path_solver = ShortestPathSolver()

    bag.path_finding_method = path_finding_method

    print(f"Creating input.json for TSNsched!")
    tsnsched = TSNsched(graph, tt_flow_list)
    tsnsched_json = TSNschedInputJson(tsnsched)
    tsnsched_dict = tsnsched_json.to_dict()
    scenario_output_path = create_scenario_output_path(bag)
    tsnsched_output_path = create_tsnsched_output_path(scenario_output_path)
    with open(os.path.join(tsnsched_output_path, "input.json"), "w", encoding="utf-8") as f:
        json.dump(tsnsched_dict, f, ensure_ascii=False, indent=2)
    print(f"input.json created successfully!")

    print(f"Running TSNsched!")
    run_tsnsched(tsnsched_output_path)
    print(f"Schedule generated!")

    print(f"GCL deploying to Edges!")
    parse_output_json(tsnsched_output_path, graph)
    print(f"GCL successfully deployed to Edges!")

    print(create_info(bag))

    solution = shortest_path_solver.solve(bag)

    solution.get_cost().write_result_to_file(bag)

    if solution.get_flow_list() is None or len(solution.get_flow_list()) == 0:
        print(constants.NO_SOLUTION_COULD_BE_FOUND)
    else:
        if solution.get_cost().get_total_cost() == float('inf'):
            print(found_no_solution(solution))
        else:
            print(found_solution(solution))

            write_path_to_file(scenario_output_path, shortest_path_solver.solution)
            write_worst_case_delay_to_file(scenario_output_path, solution.cost.get_worst_case_delay_dict(), create_result_output_path(bag))
            write_link_utilization_to_file(shortest_path_solver.solution, graph, scenario_output_path, create_result_output_path(bag))
            write_duration_to_file(shortest_path_solver.duration_dict, create_result_output_path(bag))

elif path_finding_method == "yen":
    metaheuristic_solver = MetaheuristicSolver()

    bag.path_finding_method = path_finding_method
    bag.k = k
    bag.max_iteration_number = max_iteration_number

    print(f"Creating input.json for TSNsched!")
    tsnsched = TSNsched(graph, tt_flow_list)
    tsnsched_json = TSNschedInputJson(tsnsched)
    tsnsched_dict = tsnsched_json.to_dict()
    scenario_output_path = create_scenario_output_path(bag)
    tsnsched_output_path = create_tsnsched_output_path(scenario_output_path)
    with open(os.path.join(tsnsched_output_path, "input.json"), "w", encoding="utf-8") as f:
        json.dump(tsnsched_dict, f, ensure_ascii=False, indent=2)
    print(f"input.json created successfully!")

    print(f"Running TSNsched!")
    run_tsnsched(tsnsched_output_path)
    print(f"Schedule generated!")

    print(f"GCL deploying to Edges!")
    parse_output_json(tsnsched_output_path, graph)
    print(f"GCL successfully deployed to Edges!")

    print(create_info(bag))

    solution = metaheuristic_solver.solve(bag)

    solution.cost.write_result_to_file(bag)

    if solution.flow_list is None or len(solution.flow_list) == 0:
        print(constants.NO_SOLUTION_COULD_BE_FOUND)
    else:
        if solution.cost.get_total_cost() == float('inf'):
            print(found_no_solution(solution))
        else:
            print(found_solution(solution))

            write_path_to_file(scenario_output_path, metaheuristic_solver.get_solution())
            write_worst_case_delay_to_file(scenario_output_path, solution.cost.get_worst_case_delay_dict(), create_result_output_path(bag))
            write_link_utilization_to_file(metaheuristic_solver.get_solution(), graph, scenario_output_path, create_result_output_path(bag))
            write_duration_to_file(metaheuristic_solver.get_duration_dict(), create_result_output_path(bag))
            write_srt_flow_candidate_path_list_to_file(scenario_output_path, metaheuristic_solver.get_srt_flow_candidate_list())