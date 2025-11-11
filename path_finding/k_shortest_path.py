from application.application import NonTTApplication

from message.route import UnicastCandidate

from util import constants
from util.helper_functions import convert_graph_to_nx_graph, create_path_as_node_list, create_path_as_edge_list

from util.path_finding_functions import yen_k_shortest_paths

class YenKShortestPath:
    def __init__(self, graph, application_list, path_finding_method, k):
        self.non_tt_unicast_candidate_list = list()

        for application in application_list:
            if isinstance(application, NonTTApplication):
                for target in application.get_target_list():
                    g = convert_graph_to_nx_graph(graph, application.get_source(), target)
                    if path_finding_method == constants.YEN:
                        yen_k_shortest_paths_as_string_list = yen_k_shortest_paths(g, application.get_source().get_name(), target.get_name(), k, weight='weight')
                        candidate_list = list()
                        for shortest_path in yen_k_shortest_paths_as_string_list:
                            shortest_path_as_node_list = create_path_as_node_list(shortest_path[0], shortest_path[1:-1], shortest_path[-1])
                            shortest_path = create_path_as_edge_list(shortest_path_as_node_list, graph)
                            candidate_list.append(shortest_path)

                        self.non_tt_unicast_candidate_list.append(UnicastCandidate(application, target, candidate_list))


    def get_srt_unicast_candidate_list(self):
        return self.non_tt_unicast_candidate_list