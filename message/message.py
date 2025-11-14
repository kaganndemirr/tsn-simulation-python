class Message:
    def __init__(self, application):
        self.application = application
        self.path = None

    def get_application(self):
        return self.application

    def get_path(self):
        return self.path

    def set_path(self, path):
        self.path = path

    def __repr__(self):
        return f"App: {self.application} Path: {self.path}"

    def __eq__(self, other):
        if isinstance(other, Message):
            return self.application == other.application and self.path == other.path
        return False

    def __hash__(self):
        return hash(self.application) + hash(str(self.path))


class MessageCandidate:
    def __init__(self, application):
        self.application = application
        self.candidate_path_list = None

    def get_application(self):
        return self.application

    def get_candidate_path_list(self):
        return self.candidate_path_list

    def set_candidate_path_list(self, candidate_path_list):
        self.candidate_path_list = candidate_path_list

    def __repr__(self):
        return f"App: {self.application} Candidate Path List: {self.candidate_path_list}"

    def __eq__(self, other):
        if isinstance(other, MessageCandidate):
            return self.application == other.application and self.candidate_path_list == other.candidate_path_list
        return False

    def __hash__(self):
        return hash(self.application) + hash(str(self.candidate_path_list))

