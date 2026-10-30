from fastapi import FastAPI
from pydantic import BaseModel
import llm 
from prompts import get_prompt
from prompts import CATEGORIES
app = FastAPI()

class CategoryRequest(BaseModel):
    email: str


@app.post("/categorize")
def categorize_email(request: CategoryRequest):
    prompt = get_prompt(request.email)
    category = llm.complete(prompt).lower().strip()  # Convert to lowercase and strip whitespace
    if category not in CATEGORIES:
       catergory = "other"  # Default to "other" if the category is not recognized
    
    return {"category": category}