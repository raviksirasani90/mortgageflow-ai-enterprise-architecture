
@'
# MortgageFlow AI — Enterprise Mortgage Workflow Prototype

## Overview

MortgageFlow AI demonstrates enterprise architecture patterns for a mortgage application workflow. It provides REST APIs to register applications, validate basic data, identify missing documents, and route applications for human review.

**This is a synthetic-data demonstration, not a production lending or credit-decision system.**

## Business Problem

Mortgage workflows can involve fragmented application data, missing documents, manual validation, and limited visibility into case status.

This prototype demonstrates how an API-based workflow can improve consistency, traceability, and operational visibility.

## Current Features

- FastAPI REST API
- Create, list, and retrieve mortgage applications
- Pydantic input validation
- Basic application completeness and consistency checks
- Workflow statuses: `RECEIVED`, `NEEDS_INFORMATION`, and `READY_FOR_REVIEW`
- Automated tests using pytest
- Interactive API documentation using Swagger UI

## Current Architecture

```text
Client / API Consumer
        |
        v
    FastAPI API
        |
        v
Application Validation
        |
        v
In-Memory Application Store
        |
        v
Workflow Status / API Response
```

The current implementation uses in-memory storage. Application records are lost when the process restarts.

## Technology Stack

- Python
- FastAPI
- Pydantic
- Uvicorn
- pytest
- Git

## Run Locally

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

Start the API:

```powershell
python -m uvicorn app.main:app --reload
```

Open the API documentation:

- Swagger UI: http://127.0.0.1:8000/docs
- Health check: http://127.0.0.1:8000/health

Run automated tests:

```powershell
python -m pytest -v
```

## Example API Request

`POST /applications`

```json
{
  "borrower_reference": "BORROWER-1001",
  "loan_amount": 250000,
  "annual_income": 100000,
  "property_value": 350000,
  "credit_score": 720,
  "documents": [
    "income_statement",
    "property_valuation"
  ]
}
```

## Planned Roadmap

1. Add a persistent database and repository abstraction.
2. Add document ingestion and extraction.
3. Introduce configurable business rules and workflow transitions.
4. Add AI-assisted policy retrieval with source-grounded responses.
5. Implement human review, audit events, and role-based access controls.
6. Introduce event-driven integration and idempotent processing.
7. Add evaluation, observability, containerization, and CI/CD.
8. Document target-state architecture and incremental legacy modernization.

## Responsible Use

All sample data is synthetic. Validation thresholds are illustrative, not real lending policy. Future AI features will assist authorized reviewers rather than autonomously approve or reject mortgage applications.

## Project Status

**Phase 1:** Initial API and validation workflow implemented; seven automated tests passing.
'@ | Set-Content -Path README.md -Encoding utf8
