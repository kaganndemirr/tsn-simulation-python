class Flow:
    def __init__(self, name, type, priority_value, source_device, end_device, packet_periodicity, fixed_priority, hops):
        self.name = name
        self.type = type
        self.priorityValue = priority_value
        self.sourceDevice = source_device
        self.endDevices = [end_device]
        self.packetPeriodicity = packet_periodicity
        self.fixedPriority = fixed_priority
        self.hops = hops

class Hop:
    def __init__(self, current_node_name, next_node_name):
        self.currentNodeName = current_node_name
        self.nextNodeName = next_node_name
