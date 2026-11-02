from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel

import llm
from prompts import CATEGORIES, get_prompt

app = FastAPI()

class CategoryRequest(BaseModel):
    email: str


@app.post("/categorize")
def categorize_email(request: CategoryRequest):
    prompt = get_prompt(request.email)
    category = llm.complete(prompt).lower().strip()  # Convert to lowercase and strip whitespace
    if category not in CATEGORIES:
       category = "other"  # Default to "other" if the category is not recognized

    requires_human = category == "complaint"
    
    return {"category": category, "requires_human": requires_human}

@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/")
def home():
    return FileResponse("templates/index.html")