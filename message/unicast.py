class Unicast:
    def __init__(self, app, path):
        self.app = app
        self.path = path

    def get_app(self):
        return self.app

    def get_path(self):
        return self.path

    def __repr__(self):
        return f"App: {self.app} Path: {self.path}"

    def __eq__(self, other):
        return self.app == other.app