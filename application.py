class Application:
    def __init__(self, name, pcp, application_type, frame_size_byte, number_of_frames, message_size_byte, message_size_mbps, cmi, deadline, source, target_list, explicit_path_list = None):
        self.name = name
        self.pcp = pcp
        self.application_type = application_type
        self.frame_size_byte = frame_size_byte
        self.number_of_frames = number_of_frames
        self.message_size_byte = message_size_byte
        self.message_size_mbps = message_size_mbps
        self.cmi = cmi
        self.deadline = deadline
        self.source = source
        self.target_list = target_list
        self.explicit_path_list = explicit_path_list


    def get_name(self):
        return self.name

    def get_pcp(self):
        return self.pcp

    def get_application_type(self):
        return self.application_type

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

    def get_target_list(self):
        return self.target_list

    def get_explicit_path_list(self):
        return self.explicit_path_list

    def __repr__(self):
        return f"Name: {self.name} PCP: {self.pcp} Application Type: {self.application_type} Frame Size(B): {self.frame_size_byte} #Frames: {self.number_of_frames} Message Size (B): {self.message_size_byte} Message Size (mbps): {self.message_size_mbps} CMI(us): {self.cmi} Deadline(us): {self.deadline} Source: {self.source.get_name()} -> Target: {self.target_list} Explicit Path List: {self.explicit_path_list}"

    def __eq__(self, other):
        if isinstance(other, Application):
            return self.name == other.name
        return False

    def __hash__(self):
        return id(self.name)

class SRTApplication(Application):

    def __init__(self, name, pcp, application_type, frame_size_byte, number_of_frames, message_size_byte, message_size_mbps, cmi, deadline, source, target, explicit_path = None):
        super().__init__(name, pcp, application_type, frame_size_byte, number_of_frames, message_size_byte, message_size_mbps, cmi, deadline, source, target, explicit_path)


class TTApplication(Application):
    def __init__(self, name, pcp, application_type, frame_size_byte, number_of_frames, message_size_byte, message_size_mbps, cmi, deadline, source, target, explicit_path = None):
        super().__init__(name, pcp, application_type, frame_size_byte, number_of_frames, message_size_byte, message_size_mbps, cmi, deadline, source, target, explicit_path)
