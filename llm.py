import os
from dotenv import load_dotenv
from groq import Groq


load_dotenv() # get all the env variables eg groqs
GROQ_API_KEY = os.getenv("GROQ_API_KEY") # load the groq api key from the env file

groqClient = Groq(api_key=GROQ_API_KEY) # create a groq client instance

response  = groqClient.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages = [{"role": "user", "content": "say hello"}]
)
print(response.choices[0].message.content) # print the first message from the response

