from application.application import NonTTApplication

from message.message import Message

from util import constants
from util.helper_functions import convert_graph_to_nx_graph, create_path_as_node_list, create_path_as_edge_list, generate_multicast_path_for_shortest_path
from util.path_finding_functions import dijkstra_shortest_path


class ShortestPath:
    def __init__(self, bag):
        self.non_tt_message_list = list()

        for application in bag.get_application_list():
            if isinstance(application, NonTTApplication):
                non_tt_message = Message(application)
                path_list = list()
                for target in application.get_target_list():
                    g = convert_graph_to_nx_graph(bag.get_graph(), application.get_source(), target)
                    shortest_path_as_string_list = list()
                    if bag.get_algorithm() == constants.DIJKSTRA:
                        shortest_path_as_string_list = dijkstra_shortest_path(g, application.get_source().get_name(), target.get_name(), weight='weight')

                    shortest_path_as_node_list = create_path_as_node_list(shortest_path_as_string_list[0], shortest_path_as_string_list[1:-1],shortest_path_as_string_list[-1])
                    shortest_path = create_path_as_edge_list(shortest_path_as_node_list, bag.get_graph())
                    path_list.append(shortest_path)

                path = generate_multicast_path_for_shortest_path(path_list)
                non_tt_message.set_path(path)

                self.non_tt_message_list.append(non_tt_message)

    def get_non_tt_message_list(self):
        return self.non_tt_message_list