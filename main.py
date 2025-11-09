import argparse
import logging
import os
import re

from parser.application_parser import application_parser
from parser.topology_parser import topology_parser

from util import constants
from util.helper_functions import create_shortest_path_info_log, found_no_solution, found_solution

from solver.shortest_path.dijkstra.dijkstra import Dijkstra
from solver.yen.metaheuristic.grasp import GRASP

from outputs.shapers.phy_shortest_path_result_shaper import ShortestPathResultShaper

from evaluator.avb_latency_math import AVBLatencyMath

parser = argparse.ArgumentParser(prog='tsn_simulation')
parser.add_argument('-network', help="Use given file as network")
parser.add_argument('-scenario', help="Use given file as scenario")
parser.add_argument('-cmi', help="CMI value for SRT Applications")

parser.add_argument('-k', help="Value of K for search-space reduction (Default: 50)", type=int)
parser.add_argument('-thread_number', help="Thread number (Default: Number of Processor Thread)", type=int)
parser.add_argument('-timeout', help="Metaheuristic algorithm timeout (Type: Second) (Default: 60", type=int)

parser.add_argument('-path_finder_method', help="Choose path finder method (Default = yen) (Choices: shortestPath, yen)")
parser.add_argument('-algorithm', help="Choose algorithm for shortestPath (Default = dijkstra) (Choices: dijkstra)")

parser.add_argument('-log', help="Log Type (Default: No Log) (Choices: info, debug)")
parser.add_argument('-metaheuristic_name', help="Which metaheuristic runs (Default: GRASP) (Choices: GRASP, ALO)")


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

if args.path_finder_method:
    path_finder_method = args.path_finder_method
else:
    path_finder_method = "yen"

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

logger.info(f"Finding explicit paths for TT Applications!")


network_name = None
scenario_name = None

pattern_topology = re.compile(r"(.+?)(?=\.graphml)")
matcher_topology = pattern_topology.search(os.path.basename(network_file))
if matcher_topology:
    topology_name = matcher_topology.group(1)

pattern_application = re.compile(r"(?<=_)(.*?)(?=\.xml)")
matcher_application = pattern_application.search(os.path.basename(scenario_file))
if matcher_application:
    application_name = matcher_application.group(1)



if path_finder_method == "shortest_path":
    if algorithm == "dijkstra":
        dijkstra = Dijkstra()

        logger.info(
            create_shortest_path_info_log(routing=routing, path_finder_method=path_finder_method, algorithm=algorithm,
                                          evaluator_name=evaluator_name))
        solution = dijkstra.solve(graph, application_list)

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





