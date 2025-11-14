class Application:
    def __init__(self, name, cmi, deadline, frame_size_byte, number_of_frames, message_size_byte, message_size_mbps, source, target_list, explicit_path_list):
        self.name = name
        self.cmi = cmi
        self.deadline = deadline
        self.frame_size_byte = frame_size_byte
        self.number_of_frames = number_of_frames
        self.message_size_byte = message_size_byte
        self.message_size_mbps = message_size_mbps
        self.source = source
        self.target_list = target_list
        self.explicit_path_list = explicit_path_list


    def get_name(self):
        return self.name

    def get_cmi(self):
        return self.cmi

    def get_deadline(self):
        return self.deadline

    def get_frame_size_byte(self):
        return self.frame_size_byte

    def get_number_of_frames(self):
        return self.number_of_frames

    def get_message_size_byte(self):
        return self.message_size_byte

    def get_message_size_mbps(self):
        return self.message_size_mbps

    def get_source(self):
        return self.source

    def get_target_list(self):
        return self.target_list

    def get_explicit_path_list(self):
        return self.explicit_path_list

    def __repr__(self):
        return f"Name: {self.name} CMI(us): {self.cmi} Deadline(us): {self.deadline} Frame Size(B): {self.frame_size_byte} #Frames: {self.number_of_frames} Message Size (B): {self.message_size_byte} Message Size (mbps): {self.message_size_mbps} Source: {self.source.get_name()} Target List: {self.target_list} Explicit Path List: {self.explicit_path_list}"

    def __eq__(self, other):
        if isinstance(other, Application):
            return self.name == other.name
        return False

    def __hash__(self):
        return hash(self.name)

class NonTTApplication(Application):

    def __init__(self, name, cmi, deadline, frame_size_byte, number_of_frames, message_size_byte, message_size_mbps,  source, target_list, explicit_path_list):
        super().__init__(name, cmi, deadline, frame_size_byte, number_of_frames, message_size_byte, message_size_mbps, source, target_list, explicit_path_list)


class TTApplication(Application):
    def __init__(self, name, cmi, deadline, frame_size_byte, number_of_frames, message_size_byte, message_size_mbps, source, target_list, explicit_path_list):
        super().__init__(name, cmi, deadline, frame_size_byte, number_of_frames, message_size_byte, message_size_mbps, source, target_list, explicit_path_list)
