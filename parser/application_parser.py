import xml.etree.ElementTree as Et

from util import constants

from application import SRTApplication, TTApplication

from architecture.gcl import GCL
from architecture.node import Switch, EndSystem

from util.helper_functions import compute_mbps, create_explicit_path_raw, convert_explicit_path_raw_list_to_edge

# TODO: Not Completed
def tsnrot_application_parser(app_file, graph):
    application_list = list()

    tree = Et.parse(app_file)
    root = tree.getroot()

    for app in root.findall('Application'):
        name = app.get('name')
        pcp = int(app.find('PCP').text)
        app_type = constants.PCP_TO_APP_TYPE.get(pcp)
        frame_size_byte = int(app.find('FrameSize').text)
        number_of_frames = int(app.find('NumberOfFrames').text)
        message_size_byte = frame_size_byte * number_of_frames
        cmi = float(app.find('CMI').text)
        message_size_mbps = compute_mbps(message_size_byte, cmi)
        deadline = int(app.find('Deadline').text)
        source = EndSystem(app.find('Source').get('name'))
        target_list = EndSystem(app.find('Target').get('name'))
        path_location = app.find('Path')
        if path_location is not None:
            explicit_path_switch_list = path_location.findall('Switch')
            explicit_path_raw = create_explicit_path_raw(source, explicit_path_switch_list, target)
            explicit_path = convert_to_edge(explicit_path_raw, graph)
        else:
            explicit_path = None

        if pcp < constants.TT_PCP:
            application_list.append(SRTApplication(name, pcp, app_type, frame_size_byte, number_of_frames, message_size_byte, message_size_mbps, cmi, deadline, source, target, explicit_path))

        elif pcp == constants.TT_PCP:
            application_list.append(TTApplication(name, pcp, app_type, frame_size_byte, number_of_frames, message_size_byte, message_size_mbps, cmi, deadline, source, target, explicit_path))


    return application_list

def tsncf_application_parser(app_file, rate, graph):
    application_list = list()

    tree = Et.parse(app_file)
    root = tree.getroot()

    for avb_app in root.findall('AVBApplication'):
        name = avb_app.get('name')
        pcp = constants.CLASS_A_PCP
        app_type = constants.PCP_TO_APP_TYPE.get(pcp)
        frame_size_byte = int(avb_app.find('PayloadSize').text)
        number_of_frames = int(avb_app.find('NoOfFrames').text)
        message_size_byte = frame_size_byte * number_of_frames
        cmi = float(avb_app.find('Interval').text)
        message_size_mbps = compute_mbps(message_size_byte, cmi)
        deadline = int(avb_app.find('Deadline').text)
        source_name = avb_app.find('Source').get('name')
        target_name_list = [dest.attrib.get('name') for dest in avb_app.find("Destinations").findall("Dest")]
        source = EndSystem(source_name)
        target_list = [EndSystem(target) for target in target_name_list]
        application_list.append(SRTApplication(name, pcp, app_type, frame_size_byte, number_of_frames, message_size_byte, message_size_mbps, cmi, deadline, source, target_list))

    for tt_app in root.findall('TTApplication'):
        name = tt_app.get('name')
        pcp = constants.TT_PCP
        app_type = constants.PCP_TO_APP_TYPE.get(pcp)
        frame_size_byte = 0
        number_of_frames = 0
        message_size_byte = 0
        message_size_mbps = 0
        cmi = constants.TSNCF_HYPERPERIOD
        deadline = 0
        source_name = tt_app.find('Source').get('name')
        source = EndSystem(source_name)
        destinations_element = tt_app.find('Source/Destinations')
        target_list = list()
        explicit_path_raw_list = list()
        for dest in destinations_element.findall('Dest'):
            explicit_path_switch_list = [bridge.attrib.get('name') for bridge in dest.find('Route')]

            dest_name = dest.get('name')
            target_list.append(EndSystem(dest_name))

            explicit_path_raw = create_explicit_path_raw(source_name, explicit_path_switch_list, dest_name)
            explicit_path_raw_list.append(explicit_path_raw)

        explicit_path_list = convert_explicit_path_raw_list_to_edge(explicit_path_raw_list, graph)

        for gcl in destinations_element.findall('GCL'):
            offset = float(gcl.attrib.get('offset'))
            duration = float(gcl.attrib.get('duration'))
            frequency = int(gcl.attrib.get('frequency'))

            number_of_frames = frequency

            gcl_object = GCL(offset, duration, frequency, cmi)

            set_gcl_to_edge(gcl_object, explicit_path_list)

            message_size_mbps = compute_message_size_mbps(duration, number_of_frames, cmi, rate)

        application_list.append(TTApplication(name, pcp, app_type, frame_size_byte, number_of_frames, message_size_byte, message_size_mbps, cmi, deadline, source, target_list, explicit_path_list))

    return application_list


def compute_message_size_mbps(gcl_duration, number_of_frames, hyper_period, rate):
    gate_opened_second = (constants.ONE_SECOND * (gcl_duration * number_of_frames)) / hyper_period

    message_size_mbps = int((rate * gate_opened_second) / constants.ONE_SECOND)

    return message_size_mbps


def set_gcl_to_edge(gcl, explicit_path_list):
    for explicit_path in explicit_path_list:
        i = 0
        for edge in explicit_path:
            gcl_per_edge = GCL(gcl.get_offset() + gcl.get_duration() * i, gcl.get_duration(), gcl.get_frequency(), gcl.get_hyper_period())
            edge.add_gcl(gcl_per_edge)
            i += 1