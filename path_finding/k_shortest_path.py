from application.application import NonTTApplication

from message.message import MessageCandidate

from util import constants
from util.helper_functions import convert_graph_to_nx_graph, create_path_as_node_list, create_path_as_edge_list, generate_multicast_path_for_k_shortest_path

from util.path_finding_functions import yen_k_shortest_paths

class KShortestPath:
    def __init__(self, bag):
        self.non_tt_message_candidate_list = list()

        for application in bag.get_application_list():
            if isinstance(application, NonTTApplication):
                message_candidate = MessageCandidate(application)
                candidate_path_list_for_all_targets = list()
                for target in application.get_target_list():
                    candidate_path_list = list()
                    g = convert_graph_to_nx_graph(bag.get_graph(), application.get_source(), target)
                    if bag.get_path_finding_method() == constants.YEN:
                        yen_k_shortest_paths_as_string_list = yen_k_shortest_paths(g, application.get_source().get_name(), target.get_name(), bag.get_k(), weight='weight')
                        for shortest_path in yen_k_shortest_paths_as_string_list:
                            shortest_path_as_node_list = create_path_as_node_list(shortest_path[0], shortest_path[1:-1], shortest_path[-1])
                            shortest_path = create_path_as_edge_list(shortest_path_as_node_list, bag.get_graph())
                            candidate_path_list.append(shortest_path)

                    candidate_path_list_for_all_targets.append(candidate_path_list)

                candidate_path_list = generate_multicast_path_for_k_shortest_path(candidate_path_list_for_all_targets)

                message_candidate.set_candidate_path_list(candidate_path_list)
                self.non_tt_message_candidate_list.append(message_candidate)


    def get_non_tt_message_candidate_list(self):
        return self.non_tt_message_candidate_list