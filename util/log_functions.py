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






