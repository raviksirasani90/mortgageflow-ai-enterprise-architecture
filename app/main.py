
from datetime import datetime, timezone
from enum import Enum
from typing import Optional
from uuid import uuid4

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field


app = FastAPI(
    title="MortgageFlow AI",
    description=(
        "A demonstration mortgage workflow platform "
        "with application validation and human-review routing."
    ),
    version="0.1.0",
)


class ApplicationStatus(str, Enum):
    RECEIVED = "RECEIVED"
    NEEDS_INFORMATION = "NEEDS_INFORMATION"
    READY_FOR_REVIEW = "READY_FOR_REVIEW"


class MortgageApplicationCreate(BaseModel):
    borrower_reference: str = Field(min_length=3, max_length=50)
    loan_amount: float = Field(gt=0, le=10_000_000)
    annual_income: float = Field(gt=0, le=10_000_000)
    property_value: float = Field(gt=0, le=100_000_000)
    credit_score: int = Field(ge=300, le=850)
    documents: list[str] = Field(default_factory=list)


class MortgageApplication(BaseModel):
    application_id: str
    borrower_reference: str
    loan_amount: float
    annual_income: float
    property_value: float
    credit_score: int
    documents: list[str]
    status: ApplicationStatus
    validation_issues: list[str]
    created_at: datetime


# In-memory storage for the first prototype.
# Data will be lost when the application restarts.
applications: dict[str, MortgageApplication] = {}


def validate_application(
    application: MortgageApplicationCreate,
) -> list[str]:
    issues = []

    if not application.documents:
        issues.append("Supporting documents have not been provided.")

    if application.loan_amount > application.property_value:
        issues.append("Loan amount exceeds the stated property value.")

    if application.loan_amount > application.annual_income * 5:
        issues.append(
            "Loan amount exceeds the prototype's income review threshold."
        )

    return issues


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "mortgageflow-ai",
        "version": "0.1.0",
    }


@app.post(
    "/applications",
    response_model=MortgageApplication,
    status_code=status.HTTP_201_CREATED,
)
def create_application(
    request: MortgageApplicationCreate,
) -> MortgageApplication:
    issues = validate_application(request)

    application = MortgageApplication(
        application_id=str(uuid4()),
        borrower_reference=request.borrower_reference,
        loan_amount=request.loan_amount,
        annual_income=request.annual_income,
        property_value=request.property_value,
        credit_score=request.credit_score,
        documents=request.documents,
        status=(
            ApplicationStatus.NEEDS_INFORMATION
            if issues
            else ApplicationStatus.READY_FOR_REVIEW
        ),
        validation_issues=issues,
        created_at=datetime.now(timezone.utc),
    )

    applications[application.application_id] = application
    return application


@app.get("/applications")
def list_applications():
    return list(applications.values())


@app.get("/applications/{application_id}")
def get_application(application_id: str):
    application = applications.get(application_id)

    if application is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mortgage application not found.",
        )

    return application
