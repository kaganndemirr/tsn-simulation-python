class Multicast:
    def __init__(self, application, unicast_list):
        self.application = application
        self.unicast_list = unicast_list

    def get_unicast_list(self):
        return self.unicast_list

    def get_application(self):
        return self.application

    @staticmethod
    def generate_multicast(unicast_list):
        application_map = dict()

        for unicast in unicast_list:
            application_map[unicast.get_application()] = list()
            application_map[unicast.get_application()].append(unicast)

        multicast_list = []
        for application, unicast_list in application_map.items():
            multicast_list.append(Multicast(application, unicast_list))

        return multicast_list

    def __repr__(self):
        return f"Application: {self.application} Path List: {self.unicast_list}"

    def __eq__(self, other):
        if isinstance(other, Multicast):
            return self.application == other.application
        return False

    def __hash__(self):
        return id(self.application)