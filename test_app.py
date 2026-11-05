from unittest.mock import patch
from fastapi.testclient import TestClient

from app import app

client = TestClient(app)



def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}



def test_categorize_email():
    with patch(
        "app.llm.complete",
        side_effect=["hours  ", "We open at 10am on Saturday."],
    ):
        response = client.post(
            "/categorize",
            json={"email": "What time do you open on weekends?"},
        )
        assert response.status_code == 200
        assert response.json() == {
            "category": "hours",
            "requires_human": False,
            "reply": "We open at 10am on Saturday.",
        }



def test_complaint_triggers_human_guardrail():
    with patch("app.llm.complete", return_value="complaint"):
        response = client.post(
            "/categorize",
            json={"email": "My brakes still squeal after paying $75!"},
        )
        assert response.status_code == 200
        assert response.json() == {
            "category": "complaint",
            "requires_human": True,
            "reply": None,
        }