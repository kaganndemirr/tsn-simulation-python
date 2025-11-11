import networkx as nx

from application.application import NonTTApplication, TTApplication

from message.route import Unicast

from util import constants
from util.helper_functions import convert_graph_to_nx_graph, create_path_as_node_list, create_path_as_edge_list
from util.path_finding_functions import dijkstra_shortest_path


class ShortestPath:
    def __init__(self, graph, application_list, algorithm):
        self.non_tt_unicast_list = list()

        for application in application_list:
            if isinstance(application, NonTTApplication):
                for target in application.get_target_list():
                    g = convert_graph_to_nx_graph(graph, application.get_source(), target)
                    shortest_path_as_string_list = list()
                    if algorithm == constants.DIJKSTRA:
                        shortest_path_as_string_list = dijkstra_shortest_path(g, application.get_source().get_name(), target.get_name(), weight='weight')

                    shortest_path_as_node_list = create_path_as_node_list(shortest_path_as_string_list[0], shortest_path_as_string_list[1:-1],shortest_path_as_string_list[-1])
                    shortest_path = create_path_as_edge_list(shortest_path_as_node_list, graph)

                    self.non_tt_unicast_list.append(Unicast(application, target, shortest_path))



    def get_non_tt_unicast_list(self):
        return self.non_tt_unicast_list