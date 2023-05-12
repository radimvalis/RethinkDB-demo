
def get_query_duration(profile: dict) -> float:

    total_duration = 0
    for task in profile:
        total_duration += task["duration(ms)"]
    
    return total_duration