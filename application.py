class Application:
    def __init__(self, name, frame_size_byte, number_of_frames, message_size_byte, message_size_mbps, cmi, deadline, source, target, explicit_path):
        self.name = name
        self.frame_size_byte = frame_size_byte
        self.number_of_frames = number_of_frames
        self.message_size_byte = message_size_byte
        self.message_size_mbps = message_size_mbps
        self.cmi = cmi
        self.deadline = deadline
        self.source = source
        self.target= target
        self.explicit_path = explicit_path


    def get_name(self):
        return self.name

    def get_frame_size_byte(self):
        return self.frame_size_byte

    def get_number_of_frames(self):
        return self.number_of_frames

    def get_message_size_byte(self):
        return self.message_size_byte

    def get_message_size_mbps(self):
        return self.message_size_mbps

    def get_cmi(self):
        return self.cmi

    def get_deadline(self):
        return self.deadline

    def get_source(self):
        return self.source

    def get_target(self):
        return self.target

    def get_explicit_path(self):
        return self.explicit_path

    def __repr__(self):
        return f"Name: {self.name} Frame Size(B): {self.frame_size_byte} #Frames: {self.number_of_frames} Message Size (B): {self.message_size_byte} Message Size (mbps): {self.message_size_mbps} CMI(us): {self.cmi} Deadline(us): {self.deadline} Source: {self.source.get_name()} -> Target: {self.target} Explicit Path: {self.explicit_path}"

    def __eq__(self, other):
        if isinstance(other, Application):
            return self.name == other.name
        return False

    def __hash__(self):
        return hash(self.name)

class SRTApplication(Application):

    def __init__(self, name, frame_size_byte, number_of_frames, message_size_byte, message_size_mbps, cmi, deadline, source, target, explicit_path):
        super().__init__(name, frame_size_byte, number_of_frames, message_size_byte, message_size_mbps, cmi, deadline, source, target, explicit_path)


class TTApplication(Application):
    def __init__(self, name, frame_size_byte, number_of_frames, message_size_byte, message_size_mbps, cmi, deadline, source, target, explicit_path):
        super().__init__(name, frame_size_byte, number_of_frames, message_size_byte, message_size_mbps, cmi, deadline, source, target, explicit_path)
