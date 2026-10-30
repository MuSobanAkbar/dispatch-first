PROMPT_V = "v1"

CATEGORIES = {
    "booking": "wants to book a repair or service appointment",
    "status": "asking whether their repair is done, or where it is",
    "pricing": "asking how much something costs",
    "hours": "asking about opening hours or location",
    "complaint": "unhappy with a repair, a price, the service or staff",
    "other": "anything that doesn't fit the categories above",
}


def get_prompt(email_body: str) -> str:
    categories = ""
    for name, description in CATEGORIES.items():
        categories += f"{name}: {description}\n"
    prompt = f""" You sort customer emails into cateogories.
    Categories are:
    {categories}
    the email you sort:
    <email>
    email: {email_body}
    </email>
    Your response should be a single word, the name of the category that best fits the email, no other words.
    """
    return prompt