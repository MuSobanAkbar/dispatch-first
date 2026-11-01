from unittest.mock import patch

from fastapi.testclient import TestClient

from app import app

client = TestClient(app)



#test 1
def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


#test 2
def test_categorize_email():
    with patch("app.llm.complete", return_value="hours  "):
        response = client.post("/categorize", json={"email": "What time do you open on weekends?"})
        assert response.status_code == 200
        assert response.json() == {"category": "hours"}