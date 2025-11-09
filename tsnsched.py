from util.holders.tsnsched_classes.device import Device


class TSNSCHED:
    def __init__(self, graph, application_list):
        self.graph = graph
        self.application_list = application_list

    def create_devices(self):
        devices = []
        for node in self.graph.get_nodes():
            devices.append(Device(node))

    def create_flows(self):
