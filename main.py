import argparse
import logging

from parser.application_parser import parse as parse_application
from parser.topology_parser import parse as parse_topology

from phy.shortest_path.dijkstra.dijkstra import Dijkstra


logging.basicConfig(level=logging.INFO)

logger = logging.getLogger()

parser = argparse.ArgumentParser(prog='tsn-simulation-python')
parser.add_argument('-app', help='Application File')
parser.add_argument('-net', help='Topology File')
parser.add_argument('-rate', help='Link Rate', type=int)
parser.add_argument('-idle_slope', type=float)

args = parser.parse_args()

app_file = args.app
net_file = args.net
rate = args.rate
idle_slope = args.idle_slope

logger.info(f"Parsing topology from {net_file}!")
graph = parse_topology(net_file, rate, idle_slope)
logger.info(f"Topology succesfully parsed {net_file}!")

logger.info(f"Parsing application from {app_file}!")
application_list = parse_application(app_file, rate, graph)
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