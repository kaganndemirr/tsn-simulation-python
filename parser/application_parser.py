import xml.etree.ElementTree as Et

from application import NonTTApplication, TTApplication

from util.helper_functions import compute_mbps, create_path_as_list, create_path_as_edge_list


def application_parser(app_file, graph, cmi):
    application_list = list()

    tree = Et.parse(app_file)
    root = tree.getroot()

    for non_tt_app in root.findall('NonTTApplication'):
        name = non_tt_app.find('Name').text
        deadline = int(non_tt_app.find('Deadline').text)
        frame_size_byte = int(non_tt_app.find('FrameSize').text)
        number_of_frames = int(non_tt_app.find('NumberOfFrames').text)
        message_size_byte = frame_size_byte * number_of_frames
        message_size_mbps = compute_mbps(message_size_byte, cmi)
        source = graph.get_node(non_tt_app.find('Source').text)
        target_element_list = non_tt_app.find('Targets').findall('Target')

        target_list = list()
        explicit_path_list = list()
        for target_element in target_element_list:
            target_element_name = target_element.find('Name').text
            target = graph.get_node(target_element_name)
            target_list.append(target)

            path_element = target_element.find('Path')
            if path_element is not None:
                switch_list = [switch.text for switch in path_element.findall('Switch')]
                path_as_list = create_path_as_list(source, switch_list, target)
                path_as_edge_list = create_path_as_edge_list(path_as_list, graph)
                explicit_path_list.append(path_as_edge_list)


        application_list.append(NonTTApplication(name, cmi, deadline, frame_size_byte, number_of_frames, message_size_byte, message_size_mbps, source, target_list, explicit_path_list))

    for tt_app in root.findall('TTApplication'):
        name = tt_app.find('Name').text
        cmi = float(tt_app.find('CMI').text)
        deadline = int(tt_app.find('Deadline').text)
        frame_size_byte = int(tt_app.find('FrameSize').text)
        number_of_frames = int(tt_app.find('NumberOfFrames').text)
        message_size_byte = frame_size_byte * number_of_frames
        message_size_mbps = compute_mbps(message_size_byte, cmi)
        source = graph.get_node(tt_app.find('Source').text)
        target_element_list = tt_app.find('Targets').findall('Target')

        target_list = list()
        explicit_path_list = list()
        for target_element in target_element_list:
            target_element_name = target_element.find('Name').text
            target = graph.get_node(target_element_name)
            target_list.append(target)

            path_element = target_element.find('Path')
            if path_element is not None:
                switch_list = [switch.text for switch in path_element.findall('Switch')]
                path_as_list = create_path_as_list(source, switch_list, target)
                path_as_edge_list = create_path_as_edge_list(path_as_list, graph)
                explicit_path_list.append(path_as_edge_list)

        application_list.append(TTApplication(name, cmi, deadline, frame_size_byte, number_of_frames, message_size_byte, message_size_mbps, source, target_list, explicit_path_list))

    return application_list