def get_slack(gcl):
    return gcl.get_start() + gcl.get_cycle_duration() - gcl.get_end()

def compute_max_interference(duration, gcl):
    interference_max = 0
    interference_current = 0
    remaining = duration
    while remaining > 0:
        interference_current += gcl.get_duration()
        remaining -= get_slack(gcl)

    if interference_current > interference_max:
        interference_max = interference_current

    return interference_max

def compute_worst_case_interference(duration, gcl):
    interference = duration
    if gcl is not None:
        max_interference = compute_max_interference(duration, gcl)
        interference = duration + max_interference

    return interference





