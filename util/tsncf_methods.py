import copy
import random

from evaluator.avb_latency_math_cost import AVBLatencyMathCost

from message.route import Unicast, UnicastCandidates

def construct_initial_solution(srt_unicast_candidates_list, tt_unicast_list, k, evaluator):
    initial_solution = list(tt_unicast_list)

    shuffled_srt_unicast_candidates_list = list(srt_unicast_candidates_list)
    random.shuffle(shuffled_srt_unicast_candidates_list)

    for unicast_candidate in shuffled_srt_unicast_candidates_list:
        current_best_cost = AVBLatencyMathCost()
        current_best_unicast = None

        for i in range(k):
            current_unicast = Unicast(unicast_candidate.get_application(), unicast_candidate.get_target(), unicast_candidate.get_candidate_path_list()[i])
            initial_solution.append(current_unicast)
            cost = evaluator.evaluate(initial_solution)
            if cost.get_total_cost() < current_best_cost.get_total_cost():
                current_best_cost = cost
                current_best_unicast = current_unicast
            initial_solution.remove(current_unicast)

        initial_solution.append(current_best_unicast)

    return initial_solution


def grasp_metaheuristic(initial_solution, evaluator, srt_unicast_candidate_list, global_best_cost):
    solution = copy.deepcopy(initial_solution)
    cost = evaluator.evaluate(solution)
    best_cost = cost

    mapping = dict()
    for unicast_candidate in srt_unicast_candidate_list:
        mapping[unicast_candidate] = unicast_candidate

    for sample in range(len(solution) // 2):
        index = random.randint(0, len(solution) - 1)

        old_unicast = solution[index]
        if old_unicast in mapping.keys():
            unicast_candidate = mapping[old_unicast]
        else:
            unicast_candidate = None

        if isinstance(unicast_candidate, UnicastCandidates):
            for candidate_path in unicast_candidate.get_candidate_path_list():
                temp_unicast = Unicast(old_unicast.get_application(), old_unicast.get_target(), candidate_path)
                solution[index] = temp_unicast
                cost = evaluator.evaluate(solution)

                if cost.get_total_cost() < best_cost.get_total_cost():
                    best_cost = cost
                    sample -= 1
                    if cost.get_total_cost() < global_best_cost.get_total_cost():
                        sample -= len(solution) // 2
                    break
                else:
                    solution[index] = old_unicast

    return solution