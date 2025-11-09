from application import SRTApplication, TTApplication
from architecture.node import EndSystem

from message.route import Unicast, UnicastCandidates

from util.helper_functions import convert_graph_to_networkx_graph, yen_k_shortest_paths, create_explicit_path_raw, convert_explicit_path_raw_to_edge

class YenKShortestPath:
    def __init__(self, graph, application_list, k):
        self.application_list = application_list
        self.tt_unicast_list = list()
        self.srt_unicast_candidate_list = list()

        for application in application_list:
            if isinstance(application, SRTApplication):
                networkx_graph = convert_graph_to_networkx_graph(graph, application.get_source(), application.get_target())
                yen_k_shortest_paths_raw = yen_k_shortest_paths(networkx_graph, application.get_source().get_name(), application.get_target().get_name(), k, weight='weight')
                candidate_list = list()
                for path in yen_k_shortest_paths_raw:
                    path_raw = create_explicit_path_raw(EndSystem(path[0]), path[1:-1], EndSystem(path[-1]))
                    path = convert_explicit_path_raw_to_edge(path_raw, graph)
                    candidate_list.append(path)

                self.srt_unicast_candidate_list.append(UnicastCandidates(application, application.get_target(), candidate_list))


    def get_srt_unicast_candidate_list(self):
        return self.srt_unicast_candidate_list

    def get_tt_unicast_list(self):
        tt_unicast_list = list()
        for application in self.application_list:
            if isinstance(application, TTApplication):
                tt_unicast_list.append(Unicast(application, application.get_target(), application.get_explicit_path()))

        return tt_unicast_list