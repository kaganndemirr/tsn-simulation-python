import os


def create_info(bag):
    result = "Path Finding Method: " + bag.path_finding_method
    if bag.algorithm is not None:
        result += ", Algorithm: " + bag.algorithm
    if bag.k is not None:
        result += ", K: " + str(bag.k)
    if bag.max_iteration_number is not None:
        result += ", Max Iteration Number: " + str(bag.max_iteration_number)
    return result

def found_solution(solution):
    return f"Found solution: {solution.cost.get_detailed_string()}"

def found_no_solution(solution):
    return f"Found no solution: {solution.cost().get_detailed_string()}"

def create_path_info(scenario_output_path):
    return f"Paths written to {os.path.join(scenario_output_path, "paths.txt")} file."

def create_worst_case_delay_scenario_info(scenario_output_path):
    return f"Worst Case Delays, Average Worst Cade Delay, Variance and Standard Deviation written to {os.path.join(scenario_output_path, "worst_case_delays.txt")} file."

def create_worst_case_delay_result_info(result_output_path):
    return f"Also Worst Case Delays, Average Worst Cade Delay, Variance and Standard Deviation written to {os.path.join(result_output_path, "Results.txt")} file."

def create_link_utilizations_sorted_by_name_info(scenario_output_path):
    return f"Link utilization's sorted by link names written to {os.path.join(scenario_output_path, "link_utilizations_sorted_by_names.txt")} file."

def create_link_utilizations_sorted_by_utilizations_info(scenario_output_path):
    return f"Link utilization's sorted by link utilizations written to {os.path.join(scenario_output_path, "link_utilizations_sorted_by_utilizations.txt")} file."

def create_link_utilizations_result_info(result_output_path):
    return f"Unused Links, Max Loaded Link Number, Max Loaded Link Utilization, Average Link Utilization, Variance and Standard Deviation written to {os.path.join(result_output_path, "Results.txt")} file."

def create_duration_info(result_output_path):
    return f"Costs and computation times written to {os.path.join(result_output_path, "Results.txt")} file."

def create_srt_candidate_paths_info(scenario_output_path):
    return f"SRT flow candidate paths written to {os.path.join(scenario_output_path, "srt_flow_candidate_paths.txt")} file."






