from evaluator.avb_latency_math_cost import Objective, AVBLatencyMathCost

from application.application import NonTTApplication, TTApplication

from util.edge_functions import compute_worst_case_interference
from util import constants


class AVBLatencyMath:
    @staticmethod
    def evaluate(unicast_list):
        tt_allocation_dict = dict()
        cost = AVBLatencyMathCost()

        for unicast in unicast_list:
            if isinstance(unicast.get_application(), TTApplication):
                for edge in unicast.get_path():
                    reserved_for_tt_traffic = unicast.get_application().get_message_size_mbps()
                    tt_allocation_dict[edge] += reserved_for_tt_traffic

        edge_set = set()
        for unicast in unicast_list:
            if isinstance(unicast.get_application(), SRTApplication):
                for edge in unicast.get_path():
                    if edge not in edge_set:
                        edge_set.add(edge)

        cost.add(Objective.THREE.value, len(edge_set))

        allocation_dict = dict(tt_allocation_dict)

        for unicast in unicast_list:
            if isinstance(unicast.get_application(), SRTApplication):
                for edge in unicast.get_path():
                    if edge not in allocation_dict:
                        allocation_dict[edge] = 0

                    allocation_mbps = unicast.get_application().get_message_size_mbps()
                    allocation_dict[edge] += allocation_mbps

        for unicast in unicast_list:
            if isinstance(unicast.get_application(), SRTApplication):
                latency = 0
                for edge in unicast.get_path():
                    capacity = edge.get_idle_slope() - (compute_worst_case_interference(unicast.get_application().get_cmi(), edge.get_gcl_list()) / unicast.get_application().get_cmi() - 1)
                    # Heavy penalty
                    if capacity < 0:
                        capacity = constants.BPS

                    latency += compute_max_latency(edge, allocation_dict[edge], unicast.get_application(), capacity)

                cost.set_worst_case_delay_to_multicast(unicast, latency)
                if latency > unicast.get_application().get_deadline():
                    cost.add(Objective.ONE.value, 1)

                cost.add(Objective.TWO.value, latency / unicast.get_application().get_deadline())
        return cost


def compute_max_latency(edge, allocation, srt_application, capacity):
    t_device = constants.DEVICE_DELAY / edge.get_rate()
    
    t_max_packet_ipg_sfd = ((constants.MAX_ETHERNET_FRAME_BYTE + constants.IPG + constants.SFD) * constants.ONE_BYTE) / edge.get_rate()

    t_stream_packet_sfd_ipg = ((srt_application.get_frame_size_byte() + constants.IPG + constants.SFD) * constants.ONE_BYTE) / edge.get_rate()

    t_all_streams = allocation * srt_application.get_cmi() / edge.get_rate()

    t_stream_packet_sfd = (srt_application.get_frame_size_byte() + constants.SFD) * constants.ONE_BYTE / edge.get_rate()

    avb_latency_math = t_device + (t_max_packet_ipg_sfd + t_all_streams - t_stream_packet_sfd_ipg) * (edge.get_rate() / capacity) / 100 + t_stream_packet_sfd

    wcd = compute_worst_case_interference(avb_latency_math, edge.get_gcl_list())

    return wcd