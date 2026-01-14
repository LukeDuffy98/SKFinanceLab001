import json
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential
from fastapi import FastAPI, File, Form, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

APP_DIR = Path(__file__).resolve().parent
DEMO_DIR = APP_DIR.parent
DATA_DIR = DEMO_DIR / "data"
OUT_DIR = DATA_DIR / "out"

TEMPLATES = Jinja2Templates(directory=str(APP_DIR / "templates"))

app = FastAPI(title="SK Finance Loan Decision Demo")
app.mount("/static", StaticFiles(directory=str(APP_DIR / "static")), name="static")


@dataclass(frozen=True)
class ExtractedApplication:
    application_id: str
    monthly_income: int
    requested_amount: int
    raw_text: str


def _require_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def _get_docint_client() -> DocumentIntelligenceClient:
    # PLACEHOLDER: Secrets in production
    # - Use managed identity + Key Vault.
    # - Never hardcode keys.
    endpoint = _require_env("AZURE_DOCINTEL_ENDPOINT")
    key = _require_env("AZURE_DOCINTEL_KEY")
    return DocumentIntelligenceClient(endpoint=endpoint, credential=AzureKeyCredential(key))


def _extract_text_from_document(file_bytes: bytes, content_type: Optional[str] = None) -> str:
    # PLACEHOLDER: Extraction approach
    # This demo uses Document Intelligence prebuilt-read to pull text.
    client = _get_docint_client()

    # Be tolerant of missing/unknown content types.
    safe_content_type = content_type or "application/octet-stream"

    # Use positional args to avoid SDK parameter-name drift across beta versions.
    poller = client.begin_analyze_document("prebuilt-read", file_bytes, content_type=safe_content_type)
    result = poller.result()

    return result.content or ""


def _parse_int(value: str) -> int:
    digits = re.sub(r"[^0-9]", "", value or "")
    return int(digits) if digits else 0


def _extract_fields_from_text(application_id: str, text: str) -> ExtractedApplication:
    # PLACEHOLDER: Field mapping logic
    # In production, you would use a trained extraction model or structured fields,
    # and robust validation. Here we keep it intentionally simple.

    income_match = re.search(r"Monthly\s*Income\s*[:\-]?\s*([0-9,]+)", text, re.IGNORECASE)
    requested_match = re.search(r"Requested\s*Loan\s*Amount\s*[:\-]?\s*([0-9,]+)", text, re.IGNORECASE)

    monthly_income = _parse_int(income_match.group(1) if income_match else "")
    requested_amount = _parse_int(requested_match.group(1) if requested_match else "")

    return ExtractedApplication(
        application_id=application_id,
        monthly_income=monthly_income,
        requested_amount=requested_amount,
        raw_text=text,
    )


def _load_applicant_properties(application_id: str) -> dict[str, Any]:
    # PLACEHOLDER: Database access
    # In production, this comes from a database with access controls and audit logs.
    path = DATA_DIR / "applicants.json"
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get(
        application_id,
        {
            "customer_name": "<CUSTOMER_NAME>",
            "segment": "<SEGMENT>",
            "preferred_language": "en",
            "support_number": "+91-22-4000-0000",
        },
    )


def _make_decision(monthly_income: int, requested_amount: int) -> dict[str, Any]:
    # PLACEHOLDER: Decision policy
    # Real lending decisions include many factors, human review, and governance.
    max_allowed = monthly_income * 10
    approved_amount = min(requested_amount, max_allowed)

    if monthly_income <= 0:
        decision = "Manual review"
        reason = "Income is missing or unreadable in the uploaded form."
    elif requested_amount <= 0:
        decision = "Manual review"
        reason = "Requested loan amount is missing or unreadable in the uploaded form."
    elif requested_amount <= max_allowed:
        decision = "Approved"
        reason = "Requested amount is within the current simple rule (<= 10× monthly income)."
    else:
        decision = "Declined"
        reason = (
            "Requested amount exceeds the current simple rule (max 10× monthly income). "
            "In a real workflow, we would show next steps (adjust amount, provide documents, appeal)."
        )

    # PLACEHOLDER: Transparent messaging
    # In production, ensure decision reasons are clear, consistent, and compliant.
    # Avoid leaking sensitive model logic; provide actionable next steps.

    return {
        "decision": decision,
        "reason": reason,
        "max_allowed": max_allowed,
        "approved_amount": approved_amount,
    }


def _draft_comms(applicant: dict[str, Any], application_id: str, decision: dict[str, Any]) -> tuple[str, str]:
    # PLACEHOLDER: Templates
    # In production, templates are versioned, approved, and localized.

    customer_name = applicant.get("customer_name", "<CUSTOMER_NAME>")
    support_number = applicant.get("support_number", "+91-22-4000-0000")

    if decision["decision"] == "Approved":
        sms = (
            f"Dear {customer_name}, your loan application {application_id} is approved up to "
            f"₹{decision['approved_amount']}. For help, call {support_number}."
        )
        email = (
            f"Subject: Loan application {application_id} — Approved\n\n"
            f"Dear {customer_name},\n\n"
            f"We have approved your loan application {application_id} up to ₹{decision['approved_amount']}.\n"
            f"If you have questions, contact us at {support_number}.\n\n"
            f"Regards,\nSK Finance"
        )
    elif decision["decision"] == "Declined":
        # PLACEHOLDER: Meaningful rejection messaging
        # Improve: include a reason code, next steps, and appeal path.
        sms = (
            f"Dear {customer_name}, we cannot approve loan application {application_id} for the requested amount. "
            f"You may reapply with an adjusted amount. Help: {support_number}."
        )
        email = (
            f"Subject: Loan application {application_id} — Update\n\n"
            f"Dear {customer_name},\n\n"
            f"We are unable to approve your application {application_id} for the requested amount based on the current rule.\n"
            f"Next steps: you may reapply with an adjusted amount or contact support to review options.\n"
            f"Support: {support_number}\n\n"
            f"Regards,\nSK Finance"
        )
    else:
        sms = (
            f"Dear {customer_name}, we need more information to process loan application {application_id}. "
            f"Please contact {support_number}."
        )
        email = (
            f"Subject: Loan application {application_id} — Action required\n\n"
            f"Dear {customer_name},\n\n"
            f"We could not read one or more fields in your uploaded form. Please contact support so we can help.\n"
            f"Support: {support_number}\n\n"
            f"Regards,\nSK Finance"
        )

    return sms, email


def _write_json_file(filename: str, payload: dict[str, Any]) -> str:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    safe_name = re.sub(r"[^A-Za-z0-9._-]", "_", filename.strip())
    if not safe_name.endswith(".json"):
        safe_name = f"{safe_name}.json"

    path = OUT_DIR / safe_name
    with path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    return str(path)


@app.get("/", response_class=HTMLResponse)
def index(request: Request) -> HTMLResponse:
    return TEMPLATES.TemplateResponse("index.html", {"request": request, "result": None, "error": None})


@app.post("/analyze", response_class=HTMLResponse)
async def analyze(
    request: Request,
    file: UploadFile = File(...),
    application_id: str = Form("APP-1001"),
) -> HTMLResponse:
    try:
        file_bytes = await file.read()

        raw_text = _extract_text_from_document(file_bytes, content_type=file.content_type)
        extracted = _extract_fields_from_text(application_id=application_id, text=raw_text)

        extracted_payload = {
            "application_id": extracted.application_id,
            "monthly_income": extracted.monthly_income,
            "requested_amount": extracted.requested_amount,
            "extracted_from": file.filename,
            "raw_text_excerpt": extracted.raw_text[:800],
        }
        saved_application_path = _write_json_file(f"{application_id}-application.json", extracted_payload)

        applicant = _load_applicant_properties(application_id)
        decision = _make_decision(extracted.monthly_income, extracted.requested_amount)

        decision_payload = {
            "application_id": application_id,
            "decision": decision["decision"],
            "reason": decision["reason"],
            "requested_amount": extracted.requested_amount,
            "monthly_income": extracted.monthly_income,
            "max_allowed": decision["max_allowed"],
            "approved_amount": decision["approved_amount"],
        }
        saved_decision_path = _write_json_file(f"{application_id}-decision.json", decision_payload)

        sms, email = _draft_comms(applicant=applicant, application_id=application_id, decision=decision)

        result = {
            "extracted_json": json.dumps(extracted_payload, indent=2),
            "saved_application_path": saved_application_path,
            "saved_decision_path": saved_decision_path,
            "monthly_income": extracted.monthly_income,
            "requested_amount": extracted.requested_amount,
            "max_allowed": decision["max_allowed"],
            "decision": decision["decision"],
            "sms_draft": sms,
            "email_draft": email,
        }

        return TEMPLATES.TemplateResponse("index.html", {"request": request, "result": result, "error": None})
    except Exception as exc:  # noqa: BLE001
        # PLACEHOLDER: Error handling
        # In production, return a user-safe message and log the full exception privately.
        return TEMPLATES.TemplateResponse(
            "index.html",
            {
                "request": request,
                "result": None,
                "error": str(exc),
            },
        )
