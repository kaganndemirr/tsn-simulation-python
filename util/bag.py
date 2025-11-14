class Bag:
    
    def __init__(self):
        self.graph = None
        self.application_list = None
        self.tt_message_list = None
        self.path_finding_method = None
        self.algorithm = None
        self.k = None
        self.meta_heuristic_name = None
        self.max_iteration_number = None
        self.topology_name = None
        self.scenario_name = None

    def get_graph(self):
        return self.graph

    def set_graph(self, graph):
        self.graph = graph

    def get_application_list(self):
        return self.application_list

    def set_application_list(self, application_list):
        self.application_list = application_list

    def get_tt_message_list(self):
        return self.tt_message_list

    def set_tt_message_list(self, tt_message_list):
        self.tt_message_list = tt_message_list

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

    def get_max_iteration_number(self):
        return self.max_iteration_number

    def set_max_iteration_number(self, max_iteration_number):
        self.max_iteration_number = max_iteration_number

    def get_topology_name(self):
        return self.topology_name

    def set_topology_name(self, topology_name):
        self.topology_name = topology_name

    def get_scenario_name(self):
        return self.scenario_name

    def set_scenario_name(self, scenario_name):
        self.scenario_name = scenario_name

