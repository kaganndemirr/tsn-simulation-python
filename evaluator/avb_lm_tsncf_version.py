from evaluator.avb_latency_math_cost import Objective, AVBLatencyMathCost

from application import SRTApplication, TTApplication

from message.multicast import Multicast

from util.edge_functions import compute_reserved_for_tt_traffic

import copy

def evaluate(unicast_list, graph):
    tt_allocation_dict = dict()
    multicast_list = Multicast.generate_multicast(unicast_list)
    cost = AVBLatencyMathCost()

    for multicast in multicast_list:
        if isinstance(multicast.get_application(), TTApplication):
            for unicast in multicast.get_unicast_list():
                for edge in unicast.get_path():
                    reserved_for_tt_traffic = compute_reserved_for_tt_traffic(unicast.get_application().get_cmi(), edge.get_gcl_list(), edge.get_rate())

    edge_list = list()
    for unicast in unicast_list:
        for edge in unicast.get_path():
            if edge not in edge_list:
                edge_list.append(edge)

    cost.add(Objective.THREE.value, len(edge_list))

    allocation_dict = copy.deepcopy(tt_allocation_dict)
    for unicast in unicast_list:
        if isinstance(unicast.get_app(), SRTApplication):
            for edge in unicast.get_path():
                if edge not in allocation_dict:
                    allocation_dict[edge] = list()
                    allocation = Allocation(unicast.get_app().get_pcp(), unicast.get_app().get_message_size_mbps(),unicast.get_app().get_cmi())
                    allocation_dict[edge].append(allocation)

                else:
                    allocation_dict_copy = copy.deepcopy(allocation_dict)
                    is_found = False
                    for allocation in allocation_dict_copy[edge]:
                        if unicast.get_app().get_pcp() == allocation.get_pcp() and unicast.get_app().get_interval == allocation.get_allocation_interval():
                            allocation.set_message_size_mbps(
                                allocation.get_allocation_message_size_mbps() + unicast.get_app().get_message_size_mbps())
                            is_found = True
                            break

                    if not is_found:
                        allocation = Allocation(unicast.get_app().get_pcp(), unicast.get_app().get_message_size_mbps(),
                                                unicast.get_app().get_interval())
                        allocation_dict[edge].append(allocation)

    for unicast in unicast_list:
        if isinstance(unicast.get_app(), SRTApplication):
            latency = float()
            for edge in unicast.get_path():
                if edge in tt_allocation_dict:
                    non_tt_capacity = graph[edge[0]][edge[1]]['max_allocation'] - (
                                tt_allocation_dict[edge][0].get_allocation_message_size_mbps() /
                                graph[edge[0]][edge[1]]['rate_mbps'])
                else:
                    non_tt_capacity = graph[edge[0]][edge[1]]['max_allocation']

                if non_tt_capacity < 0:
                    print("Capacity Exceed")

                latency += AVBLatencyMath.compute_max_latency(graph, edge, allocation_dict[edge], unicast.get_app(),
                                                              non_tt_capacity)

            cost.set_worst_case_delay_to_unicast(unicast, latency)
            if latency > unicast.get_app().get_deadline():
                cost.add(Objective.ONE.value, 1)

            cost.add(Objective.TWO.value, latency / unicast.get_app().get_deadline())

    return cost



def compute_max_latency(graph, edge, allocation_list, srt_application, capacity):
    t_device = graph.nodes[edge[0]]['delay']
    t_max_packet_ipg_sfd = ((constants.MAX_ETHERNET_FRAME_BYTE + constants.IPG + constants.SFD) * 8) / \
                           graph[edge[0]][edge[1]]['rate_mbps']
    t_all_streams = 0
    for allocation in allocation_list:
        if not allocation.get_pcp() == constants.TT_PCP:
            t_all_streams += (allocation.get_allocation_message_size_mbps() * srt_application.get_interval()) / \
                             graph[edge[0]][edge[1]]['rate_mbps']

    t_stream_packet_sfd_ipg = ((srt_application.get_frame_size() + constants.IPG + constants.SFD) * 8) / \
                              graph[edge[0]][edge[1]]['rate_mbps']
    t_stream_packet = (srt_application.get_frame_size() * 8) / graph[edge[0]][edge[1]]['rate_mbps']
    avb_latency_math = t_device + t_max_packet_ipg_sfd + (t_all_streams - t_stream_packet_sfd_ipg) * (
                graph[edge[0]][edge[1]]['rate_mbps'] / (
                    capacity * graph[edge[0]][edge[1]]['rate_mbps'])) + t_stream_packet
    return compute_worst_case_interference(avb_latency_math, graph[edge[0]][edge[1]]['gcl_list'])