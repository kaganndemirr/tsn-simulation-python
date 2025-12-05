from application import SRTApplication, TTApplication

from worst_case_delay_analysis.avb_latency_math_cost import Objective, AVBLatencyMathCost

from util import constants
from util.edge_functions import compute_worst_case_interference


class AVBLatencyMath:
    @staticmethod
    def evaluate(flow_list):
        tt_allocation_dict = dict()
        cost = AVBLatencyMathCost()

        for flow in flow_list:
            if isinstance(flow.application, TTApplication):
                for edge in flow.path:
                    tt_flow_size = flow.application.flow_size_mbps
                    if edge not in tt_allocation_dict.keys():
                        tt_allocation_dict[edge] = 0
                    else:
                        tt_allocation_dict[edge] += tt_flow_size

        edge_set = set()
        for flow in flow_list:
            if isinstance(flow.application, SRTApplication):
                for edge in flow.path:
                    if edge not in edge_set:
                        edge_set.add(edge)

        cost.add(Objective.THREE.value, len(edge_set))

        allocation_dict = dict(tt_allocation_dict)

        for flow in flow_list:
            if isinstance(flow.application, SRTApplication):
                for edge in flow.path:
                    if edge not in allocation_dict:
                        allocation_dict[edge] = 0

                    allocation_mbps = flow.application.flow_size_mbps
                    allocation_dict[edge] += allocation_mbps

        for flow in flow_list:
            if isinstance(flow.application, SRTApplication):
                latency = 0
                for edge in flow.path:
                    capacity = edge.srt_idle_slope
                    if edge.gcl is not None:
                        capacity = edge.srt_idle_slope - (tt_allocation_dict[edge] / edge.rate)

                    # Heavy penalty
                    if capacity < 0:
                        capacity = constants.BPS

                    latency += compute_max_latency(edge, allocation_dict[edge], flow.application, capacity)

                cost.set_worst_case_delay_to_flow(flow, latency)
                if latency > flow.application.deadline:
                    cost.add(Objective.ONE.value, 1)

                cost.add(Objective.TWO.value, latency / flow.application.deadline)
        return cost


def compute_max_latency(edge, allocation, srt_application, capacity):
    t_device = constants.DEVICE_DELAY / edge.rate
    
    t_max_packet_ipg_sfd = ((constants.MAX_ETHERNET_FRAME_BYTE + constants.IPG + constants.SFD) * constants.ONE_BYTE) / edge.rate

    t_stream_packet_sfd_ipg = ((srt_application.frame_size_byte + constants.IPG + constants.SFD) * constants.ONE_BYTE) / edge.rate

    t_stream_packet_sfd = (srt_application.frame_size_byte + constants.SFD) * constants.ONE_BYTE / edge.rate

    t_all_streams = allocation * srt_application.cmi / edge.rate

    avb_latency_math = t_device + (t_max_packet_ipg_sfd + t_all_streams - t_stream_packet_sfd_ipg) * (edge.rate / capacity) / 100 + t_stream_packet_sfd

    worst_case_delay = compute_worst_case_interference(avb_latency_math, edge.gcl)

    return worst_case_delay