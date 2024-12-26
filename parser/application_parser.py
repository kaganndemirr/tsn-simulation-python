import xml.etree.ElementTree as Et

from util import constants

from application import SRTApplication, TTApplication

from architecture.gcl import GCL
from architecture.node import Switch, EndSystem

from util.helper_functions import convert_to_edge, compute_mbps, create_explicit_path_raw

def parse(app_file, rate, graph):
    application_list = list()

    tree = Et.parse(app_file)
    root = tree.getroot()

    hyper_period = root.get('hyperperiod')

    for app in root.findall('Application'):
        name = app.get('name')
        pcp = int(app.find('PCP').text)
        app_type = constants.PCP_TO_APP_TYPE.get(pcp)
        source = EndSystem(app.find('Source').get('name'))
        target = EndSystem(app.find('Target').get('name'))
        path_location = app.find('Path')
        if path_location is not None:
            explicit_path_switch_list = path_location.findall('Switch')
        else:
            explicit_path_switch_list = None

        if pcp < constants.TT_PCP:
            frame_size_byte = int(app.find('FrameSize').text)
            number_of_frames = int(app.find('NumberOfFrames').text)
            message_size_byte = frame_size_byte * number_of_frames
            cmi = float(app.find('CMI').text)
            deadline = int(app.find('Deadline').text)
            message_size_mbps = compute_mbps(message_size_byte, cmi)
            application_list.append(SRTApplication(name, pcp, app_type, frame_size_byte, number_of_frames, message_size_byte, message_size_mbps, cmi, deadline, source, target))

        elif pcp == constants.TT_PCP:
            if hyper_period is not None:
                cmi = int(hyper_period)

            else:
                cmi_xml = app.find('CMI')
                if cmi_xml is None:
                    cmi = 500
                else:
                    cmi = int(cmi_xml.text)


            gcl = app.find('GCL')
            if gcl is not None:
                frame_size_byte = 0
                gcl_offset = float(gcl.get('offset'))
                gcl_duration = float(gcl.get('duration'))
                gcl_frequency = int(gcl.get('frequency'))
                gcl_object = GCL(gcl_offset, gcl_duration, gcl_frequency, hyper_period)
                number_of_frames = gcl_frequency
                message_size_byte = 0
                message_size_mbps = compute_message_size_mbps(gcl_duration, number_of_frames, cmi, rate)
                deadline = 0

                explicit_path_raw = create_explicit_path_raw(source, explicit_path_switch_list, target)

                explicit_path = convert_to_edge(explicit_path_raw, graph)
                set_gcl_to_edge(gcl_object, explicit_path)

            else:
                frame_size_byte = int(app.find('FrameSize').text)
                number_of_frames = int(app.find('NumberOfFrames').text)
                message_size_byte = frame_size_byte * number_of_frames
                deadline = int(app.find('Deadline').text)
                message_size_mbps = compute_mbps(message_size_byte, cmi)

            application_list.append(TTApplication(name, pcp, app_type, frame_size_byte, number_of_frames, message_size_byte, message_size_mbps, cmi, deadline, source, target))

    return application_list


def compute_message_size_mbps(gcl_duration, number_of_frames, hyper_period, rate):
    gate_opened_second = (constants.ONE_SECOND * (gcl_duration * number_of_frames)) / hyper_period

    message_size_mbps = int((rate * gate_opened_second) / constants.ONE_SECOND)

    return message_size_mbps





def set_gcl_to_edge(gcl, explicit_path):
    i = 0
    for edge in explicit_path:
        gcl_per_edge = GCL(gcl.get_offset() + gcl.get_duration() * i, gcl.get_duration(), gcl.get_frequency(), gcl.get_hyper_period())
        edge.add_gcl(gcl_per_edge)
        i += 1