import xml.etree.ElementTree as Et

from util import constants

from application import SRTApplication, TTApplication

from architecture.gcl import GCL

def parse(app_file, rate, graph):
    application_list = list()

    tree = Et.parse(app_file)
    root = tree.getroot()

    hyper_period = int(root.get('hyperperiod'))

    for app in root.findall('Application'):
        name = app.get('name')
        source = app.find('Source').get('name')
        target = app.find('Target').get('name')
        pcp = int(app.find('PCP').text)
        frame_size_byte = int(app.find('FrameSize').text)
        number_of_frames = int(app.find('NumberOfFrames').text)

        if pcp < constants.TT_PCP:
            cmi = float(app.find('CMI').text)
            deadline = int(app.find('Deadline').text)
            application_list.append(SRTApplication(name, constants.PCP_TO_TYPE.get(pcp), target, source, frame_size_byte, number_of_frames, pcp, cmi, deadline, message_size_mbps, message_size_byte))

        elif pcp == constants.TT_PCP:
            if hyper_period is not None:
                cmi = hyper_period

            gcl = app.find('GCL')
            if gcl is not None:
                frame_size_byte = 0
                deadline = 0
                gcl_offset = float(gcl.get('offset'))
                gcl_duration = float(gcl.get('duration'))
                gcl_frequency = int(gcl.get('frequency'))
                number_of_frames = gcl_frequency
                message_size_mbps = compute_message_size_mbps(gcl_duration, number_of_frames, hyper_period, rate)

                gcl_object = GCL(gcl_offset, gcl_duration, gcl_frequency, hyper_period)

            explicit_path_raw = create_explicit_path_raw(source,
                                                                           target.find('Path').findall('Switch'),
                                                                           target_name)

            explicit_path = convert_to_graph_path(explicit_path_raw)
            ApplicationParser.set_gcl_to_edge(gcl_object, explicit_path, graph)

            message_size_mbps = ApplicationParser.compute_mbps(gcl_duration, number_of_frames, hyper_period, rate)

            application_list.append(
                TTApplication(name, source, target_name, frame_size, number_of_frames, pcp, interval, deadline,
                              explicit_path, message_size_mbps))

    return application_list


def compute_message_size_mbps(gcl_duration, number_of_frames, hyper_period, rate):
    gate_opened_second = (constants.ONE_SECOND * (gcl_duration * number_of_frames)) / hyper_period

    message_size_mbps = int((rate * gate_opened_second) / constants.ONE_SECOND)

    return message_size_mbps