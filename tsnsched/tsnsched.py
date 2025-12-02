from tsnsched.device import Device
from tsnsched.flow import Flow, Hop
from tsnsched.switch import Switch as TSNschedSwitch
from tsnsched.switch import Port

from util import constants


class TSNsched:
    def __init__(self, graph, tt_message_list):
        self.graph = graph
        self.tt_message_list = tt_message_list

    def get_device_list(self):
        device_list = []
        for end_system in self.graph.get_end_system_list():
            device_list.append(Device(end_system))

        return device_list

    def get_flow_list(self):
        flow_list = list()
        for message in self.tt_message_list:
            name = message.application.name
            if len(message.application.target_list) > 1:
                type = constants.MULTICAST
            else:
                type = constants.UNICAST
            priority_value = constants.TT_PCP
            packet_size = message.application.message_size_byte
            source_device = message.application.source.name
            end_devices = [target.name for target in message.application.target_list]
            packet_periodicity = message.application.cmi
            hard_constraint_time = message.application.deadline
            fixed_priority = constants.TRUE

            hop_list = list()
            for edge in message.path:
                hop = Hop(edge.source.name, edge.target.name)
                hop_list.append(hop)

            flow = Flow(name, type, priority_value, packet_size, source_device, end_devices, packet_periodicity, hard_constraint_time, fixed_priority, hop_list)
            flow_list.append(flow)

        return flow_list

    def get_switch_list(self):
        switch_list = list()
        for switch in self.graph.get_switch_list():
            switch_name = switch.name
            port_list = switch.port_list
            ports = list()
            for port in port_list:
                port_name = port.name
                connects_to = port.connects_to
                port_speed = self.graph.get_edge(switch, self.graph.get_node(connects_to)).rate
                schedule_type = constants.MICRO_CYCLE
                port = Port(port_name, connects_to, port_speed, schedule_type)
                ports.append(port)

            switch = TSNschedSwitch(switch_name, ports)
            switch_list.append(switch)

        return switch_list
