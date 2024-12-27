class GCE:
    def __init__(self, start, end, hyper_period):
        self.start = start
        self.end = end
        self.hyper_period = hyper_period

    def get_start(self):
        return self.start

    def get_end(self):
        return self.end

    def get_duration(self):
        return self.end - self.start

    def get_hyper_period(self):
        return self.hyper_period

    def __repr__(self):
        return f"[{self.start} - {self.end}, {self.hyper_period}]"

    def __eq__(self, other):
        if isinstance(other, GCE):
            return self.start == other.start and self.end == other.end and self.hyper_period == other.hyper_period
        return False

    def __hash__(self):
        return id(self.start) + id(self.end) + id(self.hyper_period)