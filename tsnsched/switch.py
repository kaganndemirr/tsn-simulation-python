class Switch:
    def __init__(self, name, ports):
        self.name = name
        self.ports = ports

class Port:
    def __init__(self, name, connects_to, port_speed, schedule_type):
        self.name = name
        self.connectsTo = connects_to
        self.portSpeed = port_speed
        self.scheduleType = schedule_type
