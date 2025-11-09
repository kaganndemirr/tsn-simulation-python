class Solution:
    def __init__(self, cost, unicast_list):
        self.cost = cost
        self.unicast_list = unicast_list

    def get_unicast_list(self):
        return self.unicast_list

    def get_cost(self):
        return self.cost