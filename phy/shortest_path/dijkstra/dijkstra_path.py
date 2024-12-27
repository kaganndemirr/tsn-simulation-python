from application import SRTApplication, TTApplication
from message.unicast import Unicast

from util.helper_functions import convert_graph_to_nx_graph, create_explicit_path_raw, convert_explicit_path_raw_to_edge

import networkx as nx


class DijkstraPath:
    def __init__(self, graph, application_list):
        self.application_list = application_list

        self.avb_unicast_list = list()

        nx_graph = convert_graph_to_nx_graph(graph)

        for application in self.application_list:
            if isinstance(application, SRTApplication):
                for target in application.get_target_list():
                    shortest_path_string = nx.shortest_path(nx_graph, application.get_source().get_name(), target.get_name(), weight='weight')
                    shortest_path_raw = create_explicit_path_raw(shortest_path_string[0], shortest_path_string[1:-1], shortest_path_string[-1])
                    shortest_path = convert_explicit_path_raw_to_edge(shortest_path_raw, graph)

                    self.avb_unicast_list.append(Unicast(application, shortest_path))


    def get_avb_unicast_list(self):
        return self.avb_unicast_list

    def get_tt_unicast_list(self):
        tt_unicast_list = list()
        for application in self.application_list:
            if isinstance(application, TTApplication):
                for explicit_path in application.get_explicit_path_list():
                    tt_unicast_list.append(Unicast(application, explicit_path))

        return tt_unicast_list