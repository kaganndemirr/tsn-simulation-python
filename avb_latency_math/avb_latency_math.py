from application import NonTTApplication, TTApplication

from avb_latency_math.avb_latency_math_cost import Objective, AVBLatencyMathCost

from util import constants
from util.edge_functions import compute_worst_case_interference


class AVBLatencyMath:
    @staticmethod
    def evaluate(message_list):
        tt_allocation_dict = dict()
        cost = AVBLatencyMathCost()

        for message in message_list:
            if isinstance(message.application, TTApplication):
                for edge in message.path:
                    tt_message_size = message.application.message_size_mbps
                    if edge not in tt_allocation_dict.keys():
                        tt_allocation_dict[edge] = 0
                    else:
                        tt_allocation_dict[edge] += tt_message_size

        edge_set = set()
        for message in message_list:
            if isinstance(message.application, NonTTApplication):
                for edge in message.path:
                    if edge not in edge_set:
                        edge_set.add(edge)

        cost.add(Objective.THREE.value, len(edge_set))

        allocation_dict = dict(tt_allocation_dict)

        for message in message_list:
            if isinstance(message.application, NonTTApplication):
                for edge in message.path:
                    if edge not in allocation_dict:
                        allocation_dict[edge] = 0

                    allocation_mbps = message.application.message_size_mbps
                    allocation_dict[edge] += allocation_mbps

        for message in message_list:
            if isinstance(message.application, NonTTApplication):
                latency = 0
                for edge in message.path:
                    capacity = edge.non_tt_idle_slope
                    if edge.gcl is not None:
                        capacity = edge.non_tt_idle_slope - (tt_allocation_dict[edge] / edge.rate)

                    # Heavy penalty
                    if capacity < 0:
                        capacity = constants.BPS

                    latency += compute_max_latency(edge, allocation_dict[edge], message.application, capacity)

                cost.set_worst_case_delay_to_message(message, latency)
                if latency > message.application.deadline:
                    cost.add(Objective.ONE.value, 1)

                cost.add(Objective.TWO.value, latency / message.application.deadline)
        return cost


def compute_max_latency(edge, allocation, non_tt_application, capacity):
    t_device = constants.DEVICE_DELAY / edge.rate
    
    t_max_packet_ipg_sfd = ((constants.MAX_ETHERNET_FRAME_BYTE + constants.IPG + constants.SFD) * constants.ONE_BYTE) / edge.rate

    t_stream_packet_sfd_ipg = ((non_tt_application.frame_size_byte + constants.IPG + constants.SFD) * constants.ONE_BYTE) / edge.rate

    t_stream_packet_sfd = (non_tt_application.frame_size_byte + constants.SFD) * constants.ONE_BYTE / edge.rate

    t_all_streams = allocation * non_tt_application.cmi / edge.rate

    avb_latency_math = t_device + (t_max_packet_ipg_sfd + t_all_streams - t_stream_packet_sfd_ipg) * (edge.rate / capacity) / 100 + t_stream_packet_sfd

    worst_case_delay = compute_worst_case_interference(avb_latency_math, edge.gcl)

    return worst_case_delay