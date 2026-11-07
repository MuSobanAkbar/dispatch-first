
import json

from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel

import llm
from prompts import CATEGORIES, PROMPT_V, get_prompt, get_reply_prompt, load_faq

app = FastAPI()

class CategoryRequest(BaseModel):
    email: str


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