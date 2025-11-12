class TSNschedJson:
    def __init__(self, tsnsched):
        self.devices = tsnsched.get_devices()
        self.flow = tsnsched.get_flows()
        self.switches = tsnsched.get_switches()
    
    def to_dict(self):
        return {
            "devices": [self._device_to_dict(device) for device in self.devices],
            "flows": [self._flow_to_dict(flow) for flow in self.flow],
            "switches": [self._switch_to_dict(switch) for switch in self.switches]
        }

    @staticmethod
    def _device_to_dict(device):

        if isinstance(device, dict):
            return device
        if hasattr(device, '__dict__'):
            return vars(device)
        return {"name": str(device)}

    @staticmethod
    def _flow_to_dict(flow):
        if isinstance(flow, dict):
            return flow
        if hasattr(flow, '__dict__'):
            flow_dict = vars(flow).copy()
            if 'endDevices' in flow_dict and isinstance(flow_dict['endDevices'], list):
                flow_dict['endDevices'] = [
                    dev.name if hasattr(dev, 'name') else str(dev)
                    for dev in flow_dict['endDevices']
                ]
            if 'sourceDevice' in flow_dict and hasattr(flow_dict['sourceDevice'], 'name'):
                flow_dict['sourceDevice'] = flow_dict['sourceDevice'].name
            if 'hops' in flow_dict and isinstance(flow_dict['hops'], list):
                flow_dict['hops'] = [
                    vars(hop) if hasattr(hop, '__dict__') else hop
                    for hop in flow_dict['hops']
                ]
            return flow_dict
        return str(flow)

    @staticmethod
    def _switch_to_dict(switch):
        if isinstance(switch, dict):
            return switch
        if hasattr(switch, '__dict__'):
            switch_dict = vars(switch).copy()
            if 'ports' in switch_dict and isinstance(switch_dict['ports'], list):
                switch_dict['ports'] = [
                    vars(port) if hasattr(port, '__dict__') else port
                    for port in switch_dict['ports']
                ]
            return switch_dict
        return str(switch)
