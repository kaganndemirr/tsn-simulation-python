from pathlib import Path

def create_info(bag):
    result = "Path Finding Method: " + bag.get_path_finding_method()
    result += ", Algorithm: " + bag.get_algorithm()
    if bag.get_k() is not None:
        result += ", K: " + str(bag.get_k())
    if bag.get_meta_heuristic_name() is not None:
        result += ", Metaheuristic Name: " + bag.get_meta_heuristic_name()
    if bag.get_thread_number() is not None:
        result += ", Thread Number: " + str(bag.get_thread_number())
    if bag.get_timeout() is not None:
        result += ", Timeout: " + str(bag.get_timeout())
    return result

def found_solution(solution):
    return f"Found solution: {solution.get_cost().get_detailed_string()}"

def found_no_solution(solution):
    return f"Found no solution: {solution.get_cost().get_detailed_string()}"

def create_scenario_output_path(bag):
    result_list = list()

    result_list.append("outputs")
    result_list.append("PathFindingMethod=" + bag.get_path_finding_method())
    result_list.append("Algorithm=" + bag.get_algorithm())
    if bag.get_k() is not None:
        result_list.append("K=" + bag.get_k())
    if bag.get_meta_heuristic_name() is not None:
        result_list.append("Metaheuristic Name=" + bag.get_meta_heuristic_name())

    result_list.append(bag.get_topology_name() + "_" + bag.get_scenario_name())

    output_path = Path(*result_list)

    if not output_path.exists():
        output_path.mkdir(parents=True)

    return output_path




