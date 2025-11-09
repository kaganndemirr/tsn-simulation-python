from application import Application


class Route:
    def __init__(self, application, target):
        self.application = application
        self.target = target

    def get_application(self):
        return self.application

    def get_target(self):
        return self.target

    def __repr__(self):
        return f"App: {self.application} Target: {self.target}"

    def __eq__(self, other):
        if isinstance(other, Route):
            return self.application == other.application and self.target == other.target
        return False

    def __hash__(self):
        return hash(self.application) + hash(self.target)


class Unicast(Route):
    def __init__(self, application, target, path):
        super().__init__(application, target)
        self.path = path

    def get_path(self):
        return self.path

    def __repr__(self):
        return f"App: {self.application} Target: {self.target} Path: {self.path}"


class UnicastCandidates(Route):
    def __init__(self, application, target, candidate_path_list):
        super().__init__(application, target)
        self.candidate_path_list = candidate_path_list

    def get_candidate_path_list(self):
        return self.candidate_path_list

    def __repr__(self):
        return f"App: {self.application} Target: {self.target} Candidate Paths: {self.candidate_path_list}"

