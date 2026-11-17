def calculate_score(student, career):
    total_score = 0
    total_weight = 0

    for skill, required_level in career["skills"].items():
        current_level = student.get(skill, 1)

        # Give more importance to skills with higher requirements.
        weight = required_level

        skill_match = min(current_level / required_level, 1) * 100

        total_score += skill_match * weight
        total_weight += weight

    if total_weight == 0:
        skill_score = 0
    else:
        skill_score = total_score / total_weight

    # Skills contribute 85% and matching interest contributes 15%.
    final_score = skill_score * 0.85

    if student["interests"] == career["interest"]:
        final_score += 15

    return round(min(final_score, 100), 1)




def explain_recommendation(student, career):
    reasons = []

    if student["interests"] == career["interest"]:
        reasons.append("Your interests match this career.")

    for skill, required_level in career["skills"].items():
        current_level = student[skill]

        if current_level >= required_level:
            skill_name = skill.replace("_", " ").title()
            reasons.append(
                f"Your {skill_name} skill meets the required level."
            )

    if not reasons:
        reasons.append(
            "This career is included based on your overall skill scores."
        )

    return reasons[:4]



def analyze_gaps(student, career):
    gaps = []

    for skill, required_level in career["skills"].items():
        current_level = student.get(skill, 1)
        gap = required_level - current_level

        if gap > 0:
            if gap >= 3:
                level = "High"
            elif gap == 2:
                level = "Medium"
            else:
                level = "Low"

            gaps.append({
                "skill": skill.replace("_", " ").title(),
                "current": current_level,
                "required": required_level,
                "gap": gap,
                "level": level
            })

    return gaps



