class Allocation:
    def __init__(self, pcp, message_size_mbps, cmi):
        self.pcp = pcp
        self.message_size_mbps = message_size_mbps
        self.cmi = cmi

    def get_pcp(self):
        return self.pcp

    def get_message_size_mbps(self):
        return self.message_size_mbps

    def set_message_size_mbps(self, message_size_mbps):
        self.message_size_mbps = message_size_mbps

    def get_cmi(self):
        return self.get_cmi