from application import SRTApplication


def find_average_with_es(solution):
    total = sum(len(unicast.get_path()) for unicast in solution if isinstance(unicast.get_application(), SRTApplication))
    count = sum(1 for unicast in solution if isinstance(unicast.get_application(), SRTApplication))
    return total / count if count else 0


def find_average_with_sw(solution):
    lengths = [len(unicast.get_path()[1:-1]) for unicast in solution if isinstance(unicast.get_application(), SRTApplication)]
    return sum(lengths) / len(lengths) if lengths else 0