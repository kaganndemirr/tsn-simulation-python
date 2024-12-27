class GCL:
    def __init__(self, offset, duration, frequency, hyper_period):
        self.offset = offset
        self.duration = duration
        self.frequency = frequency
        self.hyper_period = hyper_period

    def get_offset(self):
        return self.offset

    def get_duration(self):
        return self.duration

    def get_frequency(self):
        return self.frequency

    def get_hyper_period(self):
        return self.hyper_period

    def __repr__(self):
        return f"<offset {self.offset}, duration {self.duration}, frequency {self.frequency}, hyperperiod {self.hyper_period}>"

    def __eq__(self, other):
        if isinstance(other, GCL):
            return self.offset == other.offset and self.duration == other.duration and self.frequency == other.duration and self.hyper_period == other.hyper_period
        return False

    def __hash__(self):
        return id(self.offset) + id(self.duration) + id(self.frequency) + id(self.hyper_period)