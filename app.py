from langfuse.decorators import observe
import json

from fastapi import FastAPI
from fastapi.responses import FileResponse, Response
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest
from pydantic import BaseModel

import llm
from prompts import CATEGORIES, PROMPT_V, get_prompt, get_reply_prompt, load_faq

# prometheus metrics for total emails categorized, total tokens used, total cost in USD, and latency in seconds
REQUEST_COUNT = Counter(
    "dispatch_emails_total",
    "Total emails categorized by category and human review requirement",
    ["category"], #to put it in a bucket for each category
)

TOKEN_COUNT = Counter(
    "dispatch_tokens_total",
    "Total LLM tokens used for categorization and reply generation",
    ["type"], # to put it in a bucket for prompt and completion tokens
)

COST_USD_TOTAL = Counter(
    "dispatch_cost_usd_total",
    "Total cost in USD for LLM usage for categorization and reply generation",
)
LATENCY_SECONDS = Histogram( #this will add a histogram metric to prometheus for latency in seconds
    "dispatch_latency_seconds",
    "Latency in seconds for LLM categorization and reply generation",
    
)
app = FastAPI()

class CategoryRequest(BaseModel):
    email: str



@app.get("/metrics")
def metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)
# generate_latest() takes all the counter and histogram metrics and returns them in a format that prometheus can scrape

@app.post("/categorize")
def categorize_email(request: CategoryRequest):
    llm.reset_last_call_meta() # Reset the last call metadata at the start of each request
    prompt = get_prompt(request.email)
    category = llm.complete(prompt).lower().strip()  # Convert to lowercase and strip whitespace
    if category not in CATEGORIES:
       category = "other"  # Default to "other" if the category is not recognized

    requires_human = category == "complaint"


    if requires_human:
        reply = None
    else:
        faq = load_faq()
        reply_prompt = get_reply_prompt(request.email, category, faq)
        reply = llm.complete(reply_prompt).strip()
    REQUEST_COUNT.labels(category=category).inc()
    TOKEN_COUNT.labels(type="prompt").inc(llm.LAST_CALL_META["prompt_tokens"])
    TOKEN_COUNT.labels(type="completion").inc(llm.LAST_CALL_META["completion_tokens"])
    COST_USD_TOTAL.inc(llm.LAST_CALL_META["cost_usd"])
    LATENCY_SECONDS.observe(llm.LAST_CALL_META["latency_ms"] / 1000.0)
    print(
        json.dumps(
            {
                
                "email": request.email,
                "category": category,
                "requires_human": requires_human,
                "reply": reply,
                "last_call_meta": llm.LAST_CALL_META,
                "prompt_version": PROMPT_V,
            }
        )
    )
    return {"category": category, "requires_human": requires_human, "reply": reply}

@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/")
def home():
    return FileResponse("templates/index.html")