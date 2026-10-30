from fastapi import FastAPI
from pydantic import BaseModel
import llm 
from prompts import get_prompt

app = FastAPI()

class CategoryRequest(BaseModel):
    email: str


@app.post("/categorize")
def categorize_email(request: CategoryRequest):
    prompt = get_prompt(request.email)
    category = llm.complete(prompt)
    return {"category": category}