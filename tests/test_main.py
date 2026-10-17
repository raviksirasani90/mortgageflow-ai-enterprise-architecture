
import pytest
from fastapi.testclient import TestClient

from app.main import app, applications

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_applications():
    applications.clear()
    yield
    applications.clear()


def sample_application(**overrides):
    data = {
        "borrower_reference": "BORROWER-1001",
        "loan_amount": 250000,
        "annual_income": 100000,
        "property_value": 350000,
        "credit_score": 720,
        "documents": ["income_statement", "property_valuation"],
    }
    data.update(overrides)
    return data


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_create_complete_application():
    response = client.post(
        "/applications",
        json=sample_application(),
    )

    assert response.status_code == 201
    assert response.json()["status"] == "READY_FOR_REVIEW"
    assert response.json()["validation_issues"] == []
    assert response.json()["application_id"]


def test_missing_documents_require_more_information():
    response = client.post(
        "/applications",
        json=sample_application(documents=[]),
    )

    assert response.status_code == 201
    assert response.json()["status"] == "NEEDS_INFORMATION"
    assert "Supporting documents have not been provided." in (
        response.json()["validation_issues"]
    )


def test_loan_above_property_value_is_flagged():
    response = client.post(
        "/applications",
        json=sample_application(
            loan_amount=400000,
            property_value=350000,
        ),
    )

    assert response.status_code == 201
    assert response.json()["status"] == "NEEDS_INFORMATION"
    assert any(
        "exceeds the stated property value"
        in issue
        for issue in response.json()["validation_issues"]
    )


def test_invalid_credit_score_is_rejected():
    response = client.post(
        "/applications",
        json=sample_application(credit_score=200),
    )

    assert response.status_code == 422


def test_get_unknown_application_returns_404():
    response = client.get(
        "/applications/00000000-0000-0000-0000-000000000000"
    )

    assert response.status_code == 404


def test_list_applications():
    client.post("/applications", json=sample_application())

    response = client.get("/applications")

    assert response.status_code == 200
    assert len(response.json()) == 1
