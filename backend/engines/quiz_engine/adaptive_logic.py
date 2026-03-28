def determine_difficulty(concept, risk, session_state):
    current_streak = session_state["current_streak"]
    mastery = concept["mastery"]
    p_error = risk["p_error"]

    if current_streak >= 5:
        if p_error < 0.3:
            return "HARD"
        else:
            return "MEDIUM"
    elif (current_streak >= 3):
        if (mastery > 0.7):
            return "HARD"
        else:
            return "MEDIUM"
        
    elif current_streak <= 1 or p_error > 0.6:
        return "EASY"
    else:
        return "MEDIUM"