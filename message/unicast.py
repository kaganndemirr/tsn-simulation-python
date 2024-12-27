class Unicast:
    def __init__(self, application, path):
        self.application = application
        self.path = path

    def get_application(self):
        return self.application

    def get_path(self):
        return self.path

    def __repr__(self):
        return f"App: {self.application} Path: {self.path}"

    def __eq__(self, other):
        if isinstance(other, Unicast):
            return self.application == other.application
        return False

    def __hash__(self):
        return id(self.application)