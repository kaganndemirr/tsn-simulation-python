from phy.shortest_path.dijkstra.dijkstra_path import DijkstraPath
from evaluator.avb_lm_tsncf_version import evaluate as avb_lm_tsncf
from solver.solution import Solution


class Dijkstra:

    def solve(self, graph, application_list):
        dijkstra_path = DijkstraPath(graph, application_list)
        avb_unicast_list = dijkstra_path.get_avb_unicast_list()
        tt_unicast_list = dijkstra_path.get_tt_unicast_list()

        unicast_list = avb_unicast_list + tt_unicast_list

        cost = avb_lm_tsncf(unicast_list, graph)

        return Solution(cost, unicast_list)