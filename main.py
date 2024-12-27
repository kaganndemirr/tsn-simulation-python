import argparse
import logging

from parser.application_parser import tsncf_application_parser, tsnrot_application_parser
from parser.topology_parser import tsncf_topology_parser, tsnrot_topology_parser

from util import constants

from phy.shortest_path.dijkstra.dijkstra import Dijkstra


logging.basicConfig(level=logging.INFO)

logger = logging.getLogger()

parser = argparse.ArgumentParser(prog='tsn-simulation-python')
parser.add_argument('-app', help='Application File')
parser.add_argument('-net', help='Topology File')
parser.add_argument('-rate', help='Link Rate', type=int)
parser.add_argument('-idle_slope', type=float)
parser.add_argument('-tsn_simulation', help='Application File')

args = parser.parse_args()

app_file = args.app
net_file = args.net
rate = args.rate
idle_slope = args.idle_slope
tsn_simulation = args.tsn_simulation

if tsn_simulation == constants.TSNCF:
    logger.info(f"TSN Simulation: {tsn_simulation}")
    logger.info(f"Parsing topology from {net_file}!")
    graph = tsncf_topology_parser(net_file, rate, idle_slope)
    logger.info(f"Topology succesfully parsed {net_file}!")

    logger.info(f"Parsing application from {app_file}!")
    application_list = tsncf_application_parser(app_file, rate, graph)
    logger.info(f"Application succesfully parsed {app_file}!")
else:
    logger.info(f"TSN Simulation: {tsn_simulation}")
    logger.info(f"Parsing topology from {net_file}!")
    graph = tsnrot_topology_parser(net_file, idle_slope)
    logger.info(f"Topology succesfully parsed {net_file}!")

    logger.info(f"Parsing application from {app_file}!")
    application_list = tsnrot_application_parser(app_file, graph)
    logger.info(f"Application succesfully parsed {app_file}!")

routing = "phy"
path_finder = "shortest_path"
algorithm = "dijkstra"

if routing == "phy":
    if path_finder == "shortest_path":
        if algorithm == "dijkstra":
            dijkstra = Dijkstra()

            logger.info(f"Solving problem using {routing}, {path_finder}, {algorithm}!")

            solution = dijkstra.solve(graph, application_list)