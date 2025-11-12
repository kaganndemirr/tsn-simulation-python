import os
import shutil
from pathlib import Path
import json


from architecture.node import Switch

def move_output_json_to_outputs(tsnsched_output_path):

    output_json_path = os.path.join(tsnsched_output_path, "output.json")

    output_json_path = Path(output_json_path)

    if output_json_path.exists():
        os.remove(output_json_path)

    shutil.move("output.json", tsnsched_output_path)

def parse_output_json(tsnsched_output_path, graph):
    move_output_json_to_outputs(tsnsched_output_path)

    output_json = json.load(open(os.path.join(tsnsched_output_path, "output.json")))

    for switch in output_json["switches"]:
        for node in graph.get_nodes():
            if isinstance(node, Switch):
                if node.get_name() == switch["name"]:
                    ports = switch["ports"]
                    for port in ports:
                        print(port)

