import os
import time
from dotenv import load_dotenv
from groq import Groq

load_dotenv() # get all the env variables eg groqs
GROQ_API_KEY = os.getenv("GROQ_API_KEY") # load the groq api key from the env file

INPUT_PRICE_PER_M = 0.15 # input price per 1 million tokens 
OUTPUT_PRICE_PER_M = 0.60 # output price per 1 million tokens

LAST_CALL_META = {
    "model": "openai/gpt-oss-120b",
    "prompt_tokens": 0,
    "completion_tokens": 0,
    "cost_usd": 0.0,
    "latency_ms": 0,
}


def complete(prompt: str) -> str:
    groqClient = Groq(api_key=GROQ_API_KEY) # create a groq client instance
    start_time = time.perf_counter() # start the timer
    response  = groqClient.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages = [{"role": "user", "content": prompt }],
    )
    latency_ms = (time.perf_counter() - start_time) * 1000 # calculate the latency in milliseconds
    prompt_tokens = response.usage.prompt_tokens # get the number of prompt tokens used
    completion_tokens = response.usage.completion_tokens # get the number of completion tokens used
    cost_usd = (prompt_tokens / 1_000_000) * INPUT_PRICE_PER_M + (completion_tokens / 1_000_000) * OUTPUT_PRICE_PER_M # 
    LAST_CALL_META["prompt_tokens"] = prompt_tokens
    LAST_CALL_META["completion_tokens"] = completion_tokens
    LAST_CALL_META["cost_usd"] = cost_usd
    LAST_CALL_META["latency_ms"] = latency_ms
    return response.choices[0].message.content

