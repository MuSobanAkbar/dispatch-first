from dotenv import load_dotenv

import llm
from prompts import get_prompt

load_dotenv() # get all the env variables eg groqs
email = "Hi, what times are you open on Saturdays? I need to bring in my car for a checkup."


prompt = get_prompt(email)
answer = llm.complete(prompt)
print(f"Category: {answer}")