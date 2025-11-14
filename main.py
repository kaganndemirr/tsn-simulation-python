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
from util.output_functions import write_path_to_file, write_worst_case_delay_to_file, write_link_utilization_to_file, write_duration_to_file

from solver.shortest_path_solver import ShortestPathSolver
from solver.metaheuristic_solver import MetaheuristicSolver

parser = argparse.ArgumentParser(prog='tsn_simulation')
parser.add_argument('-topology', help="Use given file as topology", type=str)
parser.add_argument('-scenario', help="Use given file as scenario", type=str)
parser.add_argument('-cmi', help="CMI value for SRT Applications", type=str)

parser.add_argument('-k', help="Value of K for search-space reduction (Default: 50)", type=int)
parser.add_argument('-thread_number', help="Thread number (Default: Number of Processor Thread)", type=int)
parser.add_argument('-timeout', help="Metaheuristic algorithm timeout (Type: Second) (Default: 60", type=int)

parser.add_argument('-path_finding_method', help="Choose path finder method (Default = yen) (Choices: shortestPath, yen)", type=str)
parser.add_argument('-algorithm', help="Choose algorithm for shortestPath (Default = dijkstra) (Choices: dijkstra)", type=str)

parser.add_argument('-log', help="Log Type (Default: info) (Choices: info, debug)", type=str)
parser.add_argument('-metaheuristic_name', help="Which metaheuristic runs (Default: GRASP) (Choices: GRASP, ALO)", type=str)


args = parser.parse_args()

topology_file = args.topology
scenario_file = args.scenario

avb_latency_math = AVBLatencyMath()

if args.cmi:
    cmi = args.cmi
else:
    cmi = 125

if args.k:
    k = args.k
else:
    k = 50

if args.thread_number:
    thread_number = args.thread_number
else:
    thread_number = os.cpu_count()

if args.timeout:
    timeout = args.timeout
else:
    timeout = 60

if args.path_finding_method:
    path_finding_method = args.path_finding_method
else:
    path_finding_method = "yen"

if args.algorithm:
    algorithm = args.algorithm
else:
    algorithm = "dijkstra"

if args.log:
    if args.log == constants.INFO:
        logging.basicConfig(level=logging.INFO)

    elif args.log == constants.DEBUG:
        logging.basicConfig(level=logging.DEBUG)

else:
    logging.basicConfig(level=logging.INFO)

logger = logging.getLogger()

if args.metaheuristic_name:
    metaheuristic_name = args.metaheuristic_name
else:
    metaheuristic_name = "grasp"

bag = Bag()

logger.info(f"Parsing topology from {os.path.basename(topology_file)}!")
graph = topology_parser(topology_file)
bag.set_graph(graph)
logger.info(f"Topology successfully parsed {os.path.basename(topology_file)}!")

logger.info(f"Parsing application from {os.path.basename(scenario_file)}!")
application_list = application_parser(scenario_file, graph, cmi)
bag.set_application_list(application_list)
logger.info(f"Application successfully parsed {os.path.basename(scenario_file)}!")

logger.info(f"Finding shortest paths for TT Applications!")
tt_message_list = find_shortest_path_for_tt_applications(graph, application_list)
bag.set_tt_message_list(tt_message_list)
logger.info(f"Finding shortest paths successfully for TT Applications!")

topology_name, scenario_name = get_topology_and_scenario_name(topology_file, scenario_file)
bag.set_topology_name(topology_name)
bag.set_scenario_name(scenario_name)

if path_finding_method == "shortest_path":
    shortest_path_solver = ShortestPathSolver()

    bag.set_path_finding_method(path_finding_method)
    bag.set_algorithm(algorithm)

    logger.info(f"Creating input.json for TSNsched!")
    tsnsched = TSNsched(graph, tt_message_list)
    tsnsched_json = TSNschedInputJson(tsnsched)
    tsnsched_dict = tsnsched_json.to_dict()
    scenario_output_path = create_scenario_output_path(bag)
    tsnsched_output_path = create_tsnsched_output_path(scenario_output_path)
    with open(os.path.join(tsnsched_output_path, "input.json"), "w", encoding="utf-8") as f:
        json.dump(tsnsched_dict, f, ensure_ascii=False, indent=2)
    logger.info(f"input.json created successfully!")

    logger.info(f"Running TSNsched!")
    run_tsnsched(tsnsched_output_path)
    logger.info(f"Schedule generated!")

    logger.info(f"GCL deploying to Edges!")
    parse_output_json(tsnsched_output_path, graph)
    logger.info(f"GCL successfully deployed to Edges!")

    logger.info(create_info(bag))

    solution = shortest_path_solver.solve(bag)

    solution.get_cost().write_result_to_file(bag)

    if solution.get_message_list() is None or len(solution.get_message_list()) == 0:
        logger.info(constants.NO_SOLUTION_COULD_BE_FOUND)
    else:
        if solution.get_cost().get_total_cost() == float('inf'):
            logger.info(found_no_solution(solution))
        else:
            logger.info(found_solution(solution))

            write_path_to_file(scenario_output_path, shortest_path_solver.get_solution())
            write_worst_case_delay_to_file(scenario_output_path, solution.get_cost().get_worst_case_delay_dict(), create_result_output_path(bag))
            write_link_utilization_to_file(shortest_path_solver.get_solution(), graph, scenario_output_path, create_result_output_path(bag))
            write_duration_to_file(shortest_path_solver.get_duration_dict(), create_result_output_path(bag))

elif path_finding_method == "yen":
    metaheuristic_solver = MetaheuristicSolver()

    bag.set_path_finding_method(path_finding_method)
    bag.set_algorithm(algorithm)
    bag.set_k(k)
    bag.set_thread_number(thread_number)
    bag.set_timeout(timeout)
    bag.set_meta_heuristic_name(metaheuristic_name)

    logger.info(f"Creating input.json for TSNsched!")
    tsnsched = TSNsched(graph, tt_message_list)
    tsnsched_json = TSNschedInputJson(tsnsched)
    tsnsched_dict = tsnsched_json.to_dict()
    scenario_output_path = create_scenario_output_path(bag)
    tsnsched_output_path = create_tsnsched_output_path(scenario_output_path)
    with open(os.path.join(tsnsched_output_path, "input.json"), "w", encoding="utf-8") as f:
        json.dump(tsnsched_dict, f, ensure_ascii=False, indent=2)
    logger.info(f"input.json created successfully!")

    logger.info(f"Running TSNsched!")
    run_tsnsched(tsnsched_output_path)
    logger.info(f"Schedule generated!")

    logger.info(f"GCL deploying to Edges!")
    parse_output_json(tsnsched_output_path, graph)
    logger.info(f"GCL successfully deployed to Edges!")

    logger.info(create_info(bag))

    solution = metaheuristic_solver.solve(bag)

    solution.get_cost().write_result_to_file(bag)

    if metaheuristic_name == "GRASP":
        grasp = GRASP(k)

        # logger.info(f"Solving problem using {routing}, {path_finder_method}, {algorithm}, {k}!")
        solution = grasp.solve(graph, application_list, evaluator, thread_number, timeout)

        # solution.get_cost().write_phy_result_to_file(phy_holder)

        if solution.get_multicast_list() is None or not solution.get_multicast_list():
            logger.info("No solution could be found!")
        else:
            if solution.get_cost().get_total_cost() == float('inf'):
                logger.info(f"Found no solution: {solution.get_cost().get_detailed_string()}")
            else:
                logger.info(f"Found solution: {solution.get_cost().get_string()}")

                # phy_result_shaper = PHYResultShaper(phy_holder)
                # phy_result_shaper.write_solution_to_file(grasp.get_solution())
                # phy_result_shaper.write_worst_case_delays_to_file(solution.get_cost().get_worst_case_delay_dict())
                # phy_result_shaper.write_link_utilizations_to_file(grasp.get_solution(), graph, rate)
                # phy_result_shaper.write_duration_map(grasp.get_duration_dict())
                # phy_result_shaper.write_srt_unicast_candidate_list(grasp.get_srt_unicast_candidate_list())





