class Flow:
    def __init__(self, name, type, priority_value, packet_size, source_device, end_devices, packet_periodicity, hard_constraint_time, fixed_priority, hops):
        self.name = name
        self.type = type
        self.priorityValue = priority_value
        self.packetSize = packet_size
        self.sourceDevice = source_device
        self.endDevices = end_devices
        self.packetPeriodicity = packet_periodicity
        self.hardConstraintTime = hard_constraint_time
        self.fixedPriority = fixed_priority
        self.hops = hops

class Hop:
    def __init__(self, current_node_name, next_node_name):
        self.currentNodeName = current_node_name
        self.nextNodeName = next_node_name
