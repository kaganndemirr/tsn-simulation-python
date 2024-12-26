class Application:
    def __init__(self, name, type, target, source, frame_size_byte, number_of_frames, pcp, interval, deadline, message_size_mbps, message_size_byte):
        self.name = name
        self.source = source
        self.frame_size_byte = frame_size_byte
        self.number_of_frames = number_of_frames
        self.pcp = pcp
        self.interval = interval
        self.deadline = deadline
        self.type = type
        self.target = target
        self.message_size_mbps = message_size_mbps
        self.message_size_byte = message_size_byte

    def get_name(self):
        return self.name

    def get_source(self):
        return self.source

    def get_frame_size_byte(self):
        return self.frame_size_byte

    def get_number_of_frames(self):
        return self.number_of_frames

    def get_pcp(self):
        return self.pcp

    def get_interval(self):
        return self.interval

    def get_deadline(self):
        return self.deadline

    def get_type(self):
        return self.type

    def get_target(self):
        return self.target

    def get_message_size_mbps(self):
        return self.message_size_mbps

    def get_message_size_byte(self):
        return self.message_size_byte

    def __repr__(self):
        return f"Name: {self.name} Source: {self.source} -> Target: {self.target} Frame Size(B): {self.frame_size_byte} #Frames: {self.number_of_frames} Message Size(B): {self.message_size_byte} PCP: {self.pcp} Interval(us): {self.interval} Deadline(us): {self.deadline} Type: {self.type} Message Size (mbps): {self.message_size_mbps} Message Size (B): {self.message_size_byte}"

    def __eq__(self, other):
        return self.name == other.name


class SRTApplication(Application):

    def __init__(self, name, type, target, source, frame_size_byte, number_of_frames, pcp, interval, deadline, message_size_mbps, message_size_byte):
        super().__init__(name, type, target, source, frame_size_byte, number_of_frames, pcp, interval, deadline, message_size_mbps, message_size_byte)


class TTApplication(Application):
    def __init__(self, name, type, target, source, frame_size_byte, number_of_frames, pcp, interval, deadline,
                 message_size_mbps, message_size_byte):
        super().__init__(name, type, target, source, frame_size_byte, number_of_frames, pcp, interval, deadline,
                         message_size_mbps, message_size_byte)
