class Message:
    def __init__(self, application, target_list, path):
        self.application = application
        self.target_list = target_list
        self.path = path

    def get_application(self):
        return self.application

    def get_target_list(self):
        return self.target_list

    def get_path(self):
        return self.path

    def __repr__(self):
        return f"App: {self.application} Target: {self.target_list} Path: {self.path}"

    def __eq__(self, other):
        if isinstance(other, Message):
            return self.application == other.application and self.target_list == other.target_list and self.path == other.path
        return False

    def __hash__(self):
        return hash(self.application) + hash(self.target_list) + hash(self.path)


class MessageCandidate:
    def __init__(self, application, target_list, candidate_path_list):
        self.application = application
        self.target_list = target_list
        self.candidate_path_list = candidate_path_list

    def get_application(self):
        return self.application

    def get_target_list(self):
        return self.target_list

    def get_candidate_path_list(self):
        return self.candidate_path_list

    def __repr__(self):
        return f"App: {self.application} Target: {self.target_list} Candidate Paths: {self.candidate_path_list}"

