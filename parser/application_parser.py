import xml.etree.ElementTree as Et

from util import constants

from application import SRTApplication, TTApplication

from architecture.node import EndSystem

from util.helper_functions import compute_mbps, create_explicit_path_raw, convert_explicit_path_to_edge_list


def application_parser(app_file, graph, cmi):
    application_list = list()

    tree = Et.parse(app_file)
    root = tree.getroot()

    for srt_app in root.findall('SRTApplication'):
        name = srt_app.get('name')
        frame_size_byte = int(srt_app.find('FrameSize').text)
        number_of_frames = int(srt_app.find('NumberOfFrames').text)
        message_size_byte = frame_size_byte * number_of_frames
        message_size_mbps = compute_mbps(message_size_byte, cmi)
        deadline = int(srt_app.find('Deadline').text)
        source = graph.get_node(srt_app.find('Source').get('name'))
        target = graph.get_node(srt_app.find('Target').get('name'))
        path = srt_app.find('Path')
        explicit_path = None
        if path is not None:
            explicit_path_switch_list = [switch.get('name') for switch in path.findall('Switch')]
            explicit_path_raw = create_explicit_path_raw(source, explicit_path_switch_list, target)
            explicit_path = convert_explicit_path_to_edge_list(explicit_path_raw, graph)

        application_list.append(SRTApplication(name, frame_size_byte, number_of_frames, message_size_byte, message_size_mbps, cmi, deadline, source, target, explicit_path))

    for tt_app in root.findall('TTApplication'):
        name = tt_app.get('name')
        frame_size_byte = int(tt_app.find('FrameSize').text)
        number_of_frames = int(tt_app.find('NumberOfFrames').text)
        message_size_byte = frame_size_byte * number_of_frames
        cmi = int(tt_app.find('CMI').text)
        message_size_mbps = compute_mbps(message_size_byte, cmi)
        deadline = int(tt_app.find('Deadline').text)
        source = graph.get_node(tt_app.find('Source').get('name'))
        target = graph.get_node(tt_app.find('Target').get('name'))
        path = tt_app.find('Path')
        explicit_path = None
        if path is not None:
            explicit_path_switch_list = [switch.get('name') for switch in path.findall('Switch')]
            explicit_path_raw = create_explicit_path_raw(source, explicit_path_switch_list, target)
            explicit_path = convert_explicit_path_to_edge_list(explicit_path_raw, graph)

        application_list.append(TTApplication(name, frame_size_byte, number_of_frames, message_size_byte, message_size_mbps, cmi, deadline, source, target, explicit_path))

    return application_list