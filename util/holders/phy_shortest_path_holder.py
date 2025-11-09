class PHYShortestPathHolder:
    def __init__(self):
        self.topology_name = str()
        self.application_name = str()
        self.routing = str()
        self.path_method = str()
        self.algorithm = str()

    def get_topology_name(self):
        return self.topology_name

    def set_topology_name(self, topology_name):
        self.topology_name = topology_name

    def get_application_name(self):
        return self.application_name

    def set_application_name(self, application_name):
        self.application_name = application_name

    def get_routing(self):
        return self.routing

    def set_routing(self, routing):
        self.routing = routing

    def get_path_method(self):
        return self.path_method

    def set_path_method(self, path_method):
        self.path_method = path_method

    def get_algorithm(self):
        return self.algorithm

    def set_algorithm(self, algorithm):
        self.algorithm = algorithm