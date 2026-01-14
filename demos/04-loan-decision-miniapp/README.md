# Loan decision mini-app demo (FastAPI)

This demo shows an end-to-end **loan decision workflow** using the same patterns we teach in the labs:
- upload → extract → decide → record → communicate

## What it does

1) Shows a simple web page.
2) Lets you upload a synthetic loan application form (PDF/image).
3) Extracts values from the form and stores them as JSON (real world: database).
4) Loads applicant properties from a JSON file (real world: database).
5) Makes a decision using a simple rule: **max approved amount = 10 × monthly income**.
6) Displays the result on screen.
7) Shows a comms area with editable text boxes prefilled from templates.

## Prereqs

- A facilitator-provisioned **Azure AI Document Intelligence** resource.
- You must have the endpoint and key.

Set these environment variables in your PowerShell session:

```powershell
$env:AZURE_DOCINTEL_ENDPOINT = "<YOUR_ENDPOINT>"
$env:AZURE_DOCINTEL_KEY      = "<YOUR_KEY>"
```

## Run locally (Windows)

From repo root:

```powershell
cd demos/04-loan-decision-miniapp
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
py -m uvicorn app.main:app --reload --port 8004
```

Open:
- http://127.0.0.1:8004

## Files

- `app/main.py` — FastAPI app + extraction/decision logic.
- `app/templates/index.html` — upload UI, decision output, comms boxes.
- `data/applicants.json` — synthetic applicant properties (stand-in for DB).
- `data/out/` — JSON outputs written during the demo.

## Sample application forms

Use the ready-made PDFs in `sample-forms/`.

## Responsible AI / production improvements

This demo is intentionally simple. In production, we would add:

- **Meaningful decision messages**: clear reason codes and what the applicant can do next (appeal, resubmit, documents).
- **Human review + overrides**: escalation for borderline cases and exceptions.
- **Audit trail**: log inputs/outputs, model versions, and who approved what.
- **Privacy controls**: redact PII before storing or sending to any generative step.
- **Fairness and monitoring**: measure approval rates and errors by segment, watch drift, track complaints.
- **Security**: managed identity, key vault, least privilege, and access logging.

Code call-outs are marked with `PLACEHOLDER:` blocks so you can point to them live.
