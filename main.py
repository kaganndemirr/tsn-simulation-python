import argparse
import logging
import os
import re

from util import constants

from parser.application_parser import application_parser
from parser.topology_parser import topology_parser

from evaluator.avb_latency_math import AVBLatencyMath

from util.bag import Bag
from util.log_functions import create_info, found_solution, found_no_solution
from util.ro_functions import find_shortest_path_for_tt_applications

from solver.shortest_path_solver import ShortestPathSolver
from solver.meta_heuristic_solver import GRASP

from outputs.shapers.phy_shortest_path_result_shaper import ShortestPathResultShaper


parser = argparse.ArgumentParser(prog='tsn_simulation')
parser.add_argument('-network', help="Use given file as network", type=str)
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

network_file = args.network
scenario_file = args.scenario

evaluator = AVBLatencyMath()

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
    metaheuristic_name = "GRASP"

logger.info(f"Parsing topology from {os.path.basename(network_file)}!")
graph = topology_parser(network_file)
logger.info(f"Topology successfully parsed {os.path.basename(network_file)}!")

logger.info(f"Parsing application from {os.path.basename(scenario_file)}!")
application_list = application_parser(scenario_file, graph, cmi)
logger.info(f"Application successfully parsed {os.path.basename(scenario_file)}!")

logger.info(f"Finding shortest paths for TT Applications!")
tt_message_list = find_shortest_path_for_tt_applications(graph, application_list)
logger.info(f"Finding shortest paths successfully for TT Applications!")

topology_name = None
scenario_name = None

pattern_topology = re.compile(r"(.+?)(?=\.graphml)")
matcher_topology = pattern_topology.search(os.path.basename(network_file))
if matcher_topology:
    topology_name = matcher_topology.group(1)

pattern_scenario = re.compile(r"(?<=_)(.*?)(?=\.xml)")
matcher_scenario = pattern_scenario.search(os.path.basename(scenario_file))
if matcher_scenario:
    scenario_name = matcher_scenario.group(1)

if path_finding_method == "shortest_path":
    shortest_path_solver = ShortestPathSolver()

    bag = Bag()
    bag.set_path_finding_method(path_finding_method)
    bag.set_algorithm(algorithm)

    logger.info(create_info(bag))

    solution = shortest_path_solver.solve(graph, application_list, algorithm, tt_unicast_list)

    if solution.get_multicast_list() is None or len(solution.get_multicast_list()) == 0 :
        logger.info(constants.NO_SOLUTION_COULD_BE_FOUND)
    else:
        if solution.get_cost().get_total_cost() == float('inf'):
            logger.info(found_no_solution(solution))
        else:
            logger.info(found_solution(solution))

    if algorithm == "dijkstra":
        dijkstra = Dijkstra()

        logger.info(
            create_shortest_path_info_log(routing=routing, path_finder_method=path_finder_method, algorithm=algorithm,
                                          evaluator_name=evaluator_name))


        solution.get_cost().write_phy_shortest_path_result_to_file(routing=routing,
                                                                   path_finder_method=path_finder_method,
                                                                   algorithm=algorithm, topology_name=topology_name,
                                                                   application_name=application_name)

        if solution.get_multicast_list() is None or not solution.get_multicast_list():
            logger.info(constants.NO_SOLUTION_COULD_BE_FOUND)
        else:
            if solution.get_cost().get_total_cost() == float('inf'):
                logger.info(found_no_solution(solution))
            else:
                logger.info(found_solution(solution))

                shortest_path_result_shaper = ShortestPathResultShaper(routing=routing,
                                                                       path_finder_method=path_finder_method,
                                                                       algorithm=algorithm, topology_name=topology_name,
                                                                       application_name=application_name)
                shortest_path_result_shaper.write_solution_to_file(dijkstra.get_solution())
                shortest_path_result_shaper.write_worst_case_delays_to_file(
                    solution.get_cost().get_worst_case_delay_dict())
                shortest_path_result_shaper.write_link_utilizations_to_file(dijkstra.get_solution(), graph, rate)
                shortest_path_result_shaper.write_duration_map(dijkstra.get_duration_dict())


elif path_finder_method == "yen":
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





