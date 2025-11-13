class Message:
    def __init__(self, application):
        self.application = application
        self.path_list = None

    def get_application(self):
        return self.application

    def get_path_list(self):
        return self.path_list

    def set_path_list(self, path_list):
        self.path_list = path_list

    def __repr__(self):
        return f"App: {self.application} Path List: {self.path_list}"

    def __eq__(self, other):
        if isinstance(other, Message):
            return self.application == other.application and self.path_list == other.path_list
        return False

    def __hash__(self):
        return hash(self.application) + hash(str(self.path_list))


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

