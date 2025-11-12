from architecture.node import Switch, EndSystem

from tsnsched.device import Device
from tsnsched.flow import Flow, Hop
from tsnsched.switch import Switch as TSNschedSwitch
from tsnsched.switch import Port

from util import constants


class TSNsched:
    def __init__(self, graph, tt_message_list):
        self.graph = graph
        self.tt_message_list = tt_message_list

    def get_devices(self):
        devices = []
        for node in self.graph.get_nodes():
            if isinstance(node, EndSystem):
                devices.append(Device(node))

        return devices

    def get_flows(self):
        flows = list()
        for message in self.tt_message_list:
            name = message.get_application().get_name()
            if len(message.get_path_list()) > 1:
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

            hops = list()
            for path in message.get_path_list():
                for edge in path:
                    hop = Hop(edge.get_source().get_name(), edge.get_target().get_name())
                    hops.append(hop)

            flow = Flow(name, type, priority_value, packet_size, source_device, end_devices, packet_periodicity, hard_constraint_time, fixed_priority, hops)
            flows.append(flow)

        return flows

    def get_switches(self):
        switches = list()
        for node in self.graph.get_nodes():
            if isinstance(node, Switch):
                switch_name = node.get_name()
                port_list = node.get_port_list()
                ports = list()
                for port in port_list:
                    port_name = port.get_name()
                    connects_to = port.get_connects_to()
                    port_speed = self.graph.get_edge(node, self.graph.get_node(connects_to)).get_rate()
                    schedule_type = constants.MICRO_CYCLE
                    port = Port(port_name, connects_to, port_speed, schedule_type)
                    ports.append(port)

                switch = TSNschedSwitch(switch_name, ports)
                switches.append(switch)

        return switches
