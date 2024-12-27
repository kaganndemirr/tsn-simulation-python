from architecture.gce import GCE


def compute_reserved_for_tt_traffic(duration, gcl_list, rate):
    return (compute_worst_case_interference(duration, gcl_list) / duration - 1) * rate


def compute_worst_case_interference(duration, gcl_list):
    interference = duration
    if len(gcl_list) > 0:
        gce_list = convert_gcl_to_gce_list(gcl_list)
        merged_gce_list = merge_same_gces(gce_list)
        final_gce_list = finalize_gces(merged_gce_list)
        max_interference = compute_max_interference(duration, final_gce_list)
        interference = duration + max_interference

    return interference


def convert_gcl_to_gce_list(gcl_list):
    gce_list = []
    for gcl in gcl_list:
        period = gcl.get_hyper_period() / gcl.get_frequency()
        for i in range(gcl.get_frequency()):
            start = gcl.get_offset() + i * period
            gce_list.append(GCE(start, start + gcl.get_duration(), gcl.get_hyper_period()))

    gce_list.sort(key=lambda gce: gce.get_start())

    return gce_list


def merge_same_gces(gce_list):
    fixed_gce_list = list()

    while gce_list:
        element = gce_list.pop(0)
        merged = [element]

        for other_element in list(gce_list):
            if element.get_start() == other_element.get_start():
                merged.append(other_element)
                gce_list.remove(other_element)

        if len(merged) > 1:
            total_duration = sum(gce.get_end() - gce.get_start() for gce in merged)
            new_gce = GCE(merged[0].get_start(), merged[0].get_start() + total_duration, merged[0].get_hyper_period())
            fixed_gce_list.append(new_gce)
        else:
            fixed_gce_list.append(element)

    return fixed_gce_list


def finalize_gces(merged_gce_list):
    final_gce_list = list()
    for i in range(len(merged_gce_list)):
        if i == 0:
            final_gce_list.append(merged_gce_list[i])
        else:
            previous_gce = final_gce_list[-1]
            current_gce = merged_gce_list[i]

            previous_gce_end = previous_gce.get_end()
            current_gce_start = current_gce.get_start()
            current_gce_end = current_gce.get_end()

            if current_gce_start < previous_gce_end:
                current_gce_start = previous_gce_end
                difference = current_gce_end - current_gce.get_start()
                current_gce_end = current_gce_start + difference

            final_gce_list.append(GCE(current_gce_start, current_gce_end, current_gce.get_hyper_period()))

    return final_gce_list


def get_slack(next_gce, curr_gce):
    if next_gce.get_start() < curr_gce.get_end():
        return next_gce.get_start() + curr_gce.get_hyper_period() - curr_gce.get_end()
    else:
        return next_gce.get_start() - curr_gce.get_end()


def compute_max_interference(duration, final_gce_list):
    i_max = 0
    for i in range(len(final_gce_list)):
        i_curr = 0
        rem = duration
        index = i
        while rem > 0:
            i_curr += final_gce_list[index].get_duration()
            rem -= get_slack(final_gce_list[(index + 1) % len(final_gce_list)], final_gce_list[index])
            index = (index + 1) % len(final_gce_list)
        if i_curr > i_max:
            i_max = i_curr

    return i_max