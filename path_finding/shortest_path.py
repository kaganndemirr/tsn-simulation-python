from application.application import NonTTApplication

from message.message import Message

from util import constants
from util.helper_functions import convert_graph_to_nx_graph, create_path_as_node_list, create_path_as_edge_list
from util.path_finding_functions import dijkstra_shortest_path


class ShortestPath:
    def __init__(self, graph, application_list, algorithm):
        self.non_tt_message_list = list()

        for application in application_list:
            if isinstance(application, NonTTApplication):
                non_tt_message = Message(application)
                target_list = list()
                path_list = list()
                for target in application.get_target_list():
                    target_list.append(target)
                    g = convert_graph_to_nx_graph(graph, application.get_source(), target)
                    shortest_path_as_string_list = list()
                    if algorithm == constants.DIJKSTRA:
                        shortest_path_as_string_list = dijkstra_shortest_path(g, application.get_source().get_name(), target.get_name(), weight='weight')

                    shortest_path_as_node_list = create_path_as_node_list(shortest_path_as_string_list[0], shortest_path_as_string_list[1:-1],shortest_path_as_string_list[-1])
                    shortest_path = create_path_as_edge_list(shortest_path_as_node_list, graph)
                    path_list.append(shortest_path)

                non_tt_message.set_target_list(target_list)
                non_tt_message.set_path_list(path_list)

                self.non_tt_message_list.append(non_tt_message)



    def get_non_tt_message_list(self):
        return self.non_tt_message_list