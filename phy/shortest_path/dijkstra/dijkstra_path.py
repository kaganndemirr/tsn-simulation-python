from application import SRTApplication, TTApplication
from message.unicast import Unicast

from util.helper_functions import convert_to_edge, convert_graph_to_nx_graph, create_path_raw

import networkx as nx


class DijkstraPath:
    def __init__(self, graph, application_list):
        self.application_list = application_list

        self.avb_unicast_list = list()

        nx_graph = convert_graph_to_nx_graph(graph)

        for application in self.application_list:
            if isinstance(application, SRTApplication):
                shortest_path_string = nx.shortest_path(nx_graph, application.get_source().get_name(), application.get_target().get_name(), weight='weight')
                shortest_path_raw = create_path_raw(shortest_path_string)
                shortest_path = convert_to_edge(shortest_path_raw, graph)

                self.avb_unicast_list.append(Unicast(application, shortest_path))


    def get_avb_unicast_list(self):
        return self.avb_unicast_list

    def get_tt_unicast_list(self):
        tt_unicast_list = list()
        for application in self.application_list:
            if isinstance(application, TTApplication):
                tt_unicast_list.append(Unicast(application, application.get_explicit_path()))
        return tt_unicast_list