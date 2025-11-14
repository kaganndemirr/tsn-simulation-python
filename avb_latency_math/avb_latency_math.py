from application.application import NonTTApplication, TTApplication

from avb_latency_math.avb_latency_math_cost import Objective, AVBLatencyMathCost

from util import constants
from util.edge_functions import compute_worst_case_interference


class AVBLatencyMath:
    @staticmethod
    def evaluate(message_list):
        tt_allocation_dict = dict()
        cost = AVBLatencyMathCost()

        for message in message_list:
            if isinstance(message.get_application(), TTApplication):
                for edge in message.get_path():
                    tt_message_size = message.get_application().get_message_size_mbps()
                    if edge not in tt_allocation_dict.keys():
                        tt_allocation_dict[edge] = 0
                    else:
                        tt_allocation_dict[edge] += tt_message_size

        edge_set = set()
        for message in message_list:
            if isinstance(message.get_application(), NonTTApplication):
                for edge in message.get_path():
                    if edge not in edge_set:
                        edge_set.add(edge)

        cost.add(Objective.THREE.value, len(edge_set))

        allocation_dict = dict(tt_allocation_dict)

        for message in message_list:
            if isinstance(message.get_application(), NonTTApplication):
                for edge in message.get_path():
                    if edge not in allocation_dict:
                        allocation_dict[edge] = 0

                    allocation_mbps = message.get_application().get_message_size_mbps()
                    allocation_dict[edge] += allocation_mbps

        for message in message_list:
            if isinstance(message.get_application(), NonTTApplication):
                latency = 0
                for edge in message.get_path():
                    capacity = edge.get_idle_slope()
                    if edge.get_gcl() is not None:
                        capacity = edge.get_idle_slope() - (tt_allocation_dict[edge] / edge.get_rate())

                    # Heavy penalty
                    if capacity < 0:
                        capacity = constants.BPS

                    latency += compute_max_latency(edge, allocation_dict[edge], message.get_application(), capacity)

                cost.set_worst_case_delay_to_message(message, latency)
                if latency > message.get_application().get_deadline():
                    cost.add(Objective.ONE.value, 1)

                cost.add(Objective.TWO.value, latency / message.get_application().get_deadline())
        return cost


def compute_max_latency(edge, allocation, non_tt_application, capacity):
    t_device = constants.DEVICE_DELAY / edge.get_rate()
    
    t_max_packet_ipg_sfd = ((constants.MAX_ETHERNET_FRAME_BYTE + constants.IPG + constants.SFD) * constants.ONE_BYTE) / edge.get_rate()

    t_stream_packet_sfd_ipg = ((non_tt_application.get_frame_size_byte() + constants.IPG + constants.SFD) * constants.ONE_BYTE) / edge.get_rate()

    t_stream_packet_sfd = (non_tt_application.get_frame_size_byte() + constants.SFD) * constants.ONE_BYTE / edge.get_rate()

    t_all_streams = allocation * non_tt_application.get_cmi() / edge.get_rate()

    avb_latency_math = t_device + (t_max_packet_ipg_sfd + t_all_streams - t_stream_packet_sfd_ipg) * (edge.get_rate() / capacity) / 100 + t_stream_packet_sfd

    worst_case_delay = compute_worst_case_interference(avb_latency_math, edge.get_gcl())

    return worst_case_delay