from application import SRTApplication

from flow import Flow

from util import constants
from util.helper_functions import convert_graph_to_nx_graph, create_path_as_node_list, create_path_as_edge_list, generate_multicast_path_for_shortest_path
from util.path_finding_functions import dijkstra_shortest_path


class ShortestPath:
    def __init__(self, bag):
        self.srt_flow_list = list()

        for application in bag.application_list:
            if isinstance(application, SRTApplication):
                srt_flow = Flow(application)
                path_list = list()
                for target in application.target_list:
                    g = convert_graph_to_nx_graph(bag.graph, application.source, target)
                    shortest_path_as_string_list = dijkstra_shortest_path(g, application.source.name, target.name, weight='weight')
                    shortest_path_as_node_list = create_path_as_node_list(shortest_path_as_string_list[0], shortest_path_as_string_list[1:-1],shortest_path_as_string_list[-1])
                    shortest_path = create_path_as_edge_list(shortest_path_as_node_list, bag.graph)
                    path_list.append(shortest_path)

                path = generate_multicast_path_for_shortest_path(path_list)
                srt_flow.path = path

                self.srt_flow_list.append(srt_flow)