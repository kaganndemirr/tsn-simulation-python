class Bag:
    
    def __init__(self):
        self.path_finding_method = None
        self.algorithm = None
        self.k = None
        self.meta_heuristic_name = None
        self.thread_number = None
        self.timeout = None
        self.topology_name = None
        self.scenario_name = None

    def get_path_finding_method(self):
        return self.path_finding_method
    
    def set_path_finding_method(self, path_finding_method):
        self.path_finding_method = path_finding_method

    def get_algorithm(self):
        return self.algorithm

    def set_algorithm(self, algorithm):
        self.algorithm = algorithm

    def get_k(self):
        return self.k

    def set_k(self, k):
        self.k = k

    def get_meta_heuristic_name(self):
        return self.meta_heuristic_name

    def set_meta_heuristic_name(self, meta_heuristic_name):
        self.meta_heuristic_name = meta_heuristic_name

    def get_thread_number(self):
        return self.thread_number

    def set_thread_number(self, thread_number):
        self.thread_number = thread_number

    def get_timeout(self):
        return self.timeout

    def set_timeout(self, timeout):
        self.timeout = timeout

    def get_topology_name(self):
        return self.topology_name

    def set_topology_name(self, topology_name):
        self.topology_name = topology_name

    def get_scenario_name(self):
        return self.scenario_name

    def set_scenario_name(self, scenario_name):
        self.scenario_name = scenario_name

