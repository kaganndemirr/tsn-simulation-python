class Multicast:
    def __init__(self, application, unicast_list):
        self.application = application
        self.unicast_list = unicast_list

    def get_application(self):
        return self.application

    def get_unicast_list(self):
        return self.unicast_list

    @staticmethod
    def generate_multicast(unicast_list):
        multicast_dict = dict()

        for unicast in unicast_list:
            if unicast not in multicast_dict.keys():
                multicast_dict[unicast] = list()

            multicast_dict[unicast].append(unicast)


    def __repr__(self):
        return f"Application: {self.application}, Unicast list: {self.unicast_list}"

    def __eq__(self, other):
        if isinstance(other, Multicast):
            return self.application == other.application and self.unicast_list == other.unicast_list
        return False

    def __hash__(self):
        return hash(self.application) + hash(self.unicast_list)