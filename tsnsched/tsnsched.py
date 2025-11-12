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
                name = node.get_name()
                ports = list()
                port_id = 0
                for neighbor in self.graph.get_node_neighbor_list(node):
                    port_name = "eth" + str(port_id)
                    connectsTo = neighbor.get_name()
                    portSpeed = self.graph.get_edge(node, neighbor).get_rate()
                    scheduleType = constants.MACRO_CYCLE
                    port_id += 1
                    port = Port(port_name, connectsTo, portSpeed, scheduleType)
                    ports.append(port)

                switch = TSNschedSwitch(name, ports)
                switches.append(switch)

        return switches
