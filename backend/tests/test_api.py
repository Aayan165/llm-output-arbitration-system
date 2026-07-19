from unittest.mock import patch
from fastapi.testclient import TestClient

from app.main import app
from app.schemas.verdict import FinalVerdict

client = TestClient(app)

@patch("app.api.routes.service.evaluate")
def test_evaluate(mock_evaluate):
    mock_evaluate.return_value = FinalVerdict(
        overall_score=9,
        verdict="Excellent",
        summary="Great answer",
        strengths=[],
        weaknesses=[],
        improvements=[]
    )

    response = client.post(
        "/evaluate",
        json={
            "prompt": "Capital of France?",
            "response": "Paris"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["result"]["verdict"] == "Excellent"