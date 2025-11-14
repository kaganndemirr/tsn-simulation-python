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
            name = message.get_application().get_name()
            if len(message.get_application().get_target_list()) > 1:
                type = constants.MULTICAST
            else:
                type = constants.UNICAST
            priority_value = constants.TT_PCP
            packet_size = message.get_application().get_message_size_byte()
            source_device = message.get_application().get_source().get_name()
            end_devices = [target.get_name() for target in message.get_application().get_target_list()]
            packet_periodicity = message.get_application().get_cmi()
            hard_constraint_time = message.get_application().get_deadline()
            fixed_priority = constants.TRUE

            hop_list = list()
            for edge in message.get_path():
                hop = Hop(edge.get_source().get_name(), edge.get_target().get_name())
                hop_list.append(hop)

            flow = Flow(name, type, priority_value, packet_size, source_device, end_devices, packet_periodicity, hard_constraint_time, fixed_priority, hop_list)
            flow_list.append(flow)

        return flow_list

    def get_switch_list(self):
        switch_list = list()
        for switch in self.graph.get_switch_list():
            switch_name = switch.get_name()
            port_list = switch.get_port_list()
            ports = list()
            for port in port_list:
                port_name = port.get_name()
                connects_to = port.get_connects_to()
                port_speed = self.graph.get_edge(switch, self.graph.get_node(connects_to)).get_rate()
                schedule_type = constants.MICRO_CYCLE
                port = Port(port_name, connects_to, port_speed, schedule_type)
                ports.append(port)

            switch = TSNschedSwitch(switch_name, ports)
            switch_list.append(switch)

        return switch_list
