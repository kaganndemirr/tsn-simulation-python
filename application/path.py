class Path:
    def __init__(self, target, path):
        self.target = target
        self.path = path

    def get_target(self):
        return self.target

    def get_path(self):
        return self.path

    def __repr__(self):
        return f"Target: {self.target}, Path: {self.path}"

    def __eq__(self, other):
        if isinstance(other, Path):
            return self.target == other.target and self.path == other.path
        return False

    def __hash__(self):
        return hash(self.target) + hash(self.path)