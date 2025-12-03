import os
import shutil
from pathlib import Path
import json

from architecture.gcl import GCL

def move_output_json_to_outputs(tsnsched_output_path):

    output_json_path = os.path.join(tsnsched_output_path, "output.json")

    output_json_path = Path(output_json_path)

    if output_json_path.exists():
        os.remove(output_json_path)

    shutil.move("output.json", tsnsched_output_path)


def get_tsnsched_switch(node, output_json):
    node_name = node.name
    for tsnsched_switch in output_json["switches"]:
        if node_name == tsnsched_switch["name"]:
            return tsnsched_switch
    return None


def get_port_list_have_gcl(tsnsched_switch):
    port_list_have_gcl = list()
    for port in tsnsched_switch["ports"]:
        if port["cycleDuration"] != float(0):
            port_list_have_gcl.append((port["cycleDuration"], port))
    return port_list_have_gcl


def get_edge(graph, switch, port_name):
    target = None
    for port in switch.get_port_list():
        if port_name == port.name:
            target_name = port.connects_to
            target = graph.get_node(target_name)

    edge = graph.get_edge(switch, target)
    return edge

def parse_output_json(tsnsched_output_path, graph):
    move_output_json_to_outputs(tsnsched_output_path)

    output_json = json.load(open(os.path.join(tsnsched_output_path, "output.json")))

    for switch in graph.get_switch_list():
        tsnsched_switch = get_tsnsched_switch(switch, output_json)
        port_list_have_gcl = get_port_list_have_gcl(tsnsched_switch)
        for cycle_duration, port in port_list_have_gcl:
            first_cycle_start = port["firstCycleStart"]
            port_name = port["name"]
            for priority_slot in port["prioritySlotsData"]:
                for slot_data in priority_slot["slotsData"]:
                    gcl = GCL(first_cycle_start + slot_data["slotStart"], first_cycle_start + slot_data["slotStart"] + slot_data["slotDuration"], cycle_duration)
                    edge = get_edge(graph, switch, port_name)
                    edge.add_gcl(gcl)