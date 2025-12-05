import os
import subprocess

def run_tsnsched(output_path):
    tsnsched_jar_path = os.path.join(os.path.expanduser("~"), "tsn_simulation", "libs", "TSNsched.jar")
    input_json_path = os.path.join(os.path.expanduser("~"), "tsn_simulation", output_path, "input.json")
    subprocess.run(["java", "-jar", "--enable-native-access=ALL-UNNAMED", tsnsched_jar_path, input_json_path])