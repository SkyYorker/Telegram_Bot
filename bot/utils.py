

async def calculate_percentage(right_answer_user, wrong_answer_user):
    total_answers = right_answer_user + wrong_answer_user
    if total_answers > 0:
        return (right_answer_user / total_answers) * 100
    else:
        return 0