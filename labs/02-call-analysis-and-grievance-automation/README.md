# Lab 2 — Call transcription & grievance analysis (Microsoft Foundry + Azure AI Speech + Language)

## Learning objectives
- Convert a synthetic call recording into text using Azure AI Speech
- Redact obvious personal data (PII) from the transcript using Azure AI Language
- Produce a short grievance summary and classify it for routing

## Prereqs
- You have access to an Azure subscription provided for the training.
- Resource group: `skfinance`.
- Permissions: you have been added to the student group with the “Student Lab Contributor” role on the `skfinance` resource group.
- Permissions (Microsoft Foundry): the facilitator has granted your student account access to the Foundry project using Azure RBAC:
	- Role: **Azure AI User**
	- Scope: the Foundry project `proj-skfinance-nf-resource/proj-skfinance-nf`
- Facilitator-provisioned Azure AI resource names (in `skfinance`):
	- Speech: `skfspeech61459`
	- Language: `skflang61459`
- Facilitator-provided Microsoft Foundry details:
	- Foundry project link (URL): <FACILITATOR_PROVIDES>
	- Chat model deployment name: <FACILITATOR_PROVIDES>
- You have a synthetic call audio file in this lab folder:
	- File name: `synthetic-call.wav`

### Downloads (one click)
- <a href="synthetic-call.wav?raw=1" target="_blank" rel="noopener noreferrer">Download `synthetic-call.wav`</a>
- (Optional) <a href="assets/architecture-lab2.svg?raw=1" target="_blank" rel="noopener noreferrer">Download `architecture-lab2.svg`</a>

## Estimated time
40 minutes

## Architecture sketch
![Lab 2 architecture diagram](assets/architecture-lab2.svg?raw=1)

- Microsoft Foundry transcribes a synthetic audio file into text.
- Microsoft Foundry performs PII redaction.
- You create a summary and a routing label that the SK Finance operations team could act on.

## Step-by-step
1. (Browser) Open Microsoft Foundry: https://ai.azure.com
2. (Microsoft Foundry) Select **Sign in** and sign in with the same account you use for the Azure portal.
3. (Microsoft Foundry) In the portal header, make sure the **New Foundry** toggle is **Off** (you are using **Foundry (classic)**).
4. (Microsoft Foundry) Open the project using the facilitator-provided **Foundry project link (URL)**.

### Part A — Transcribe the call (Speech to text playground)
5. (Microsoft Foundry) In the left pane, select **Playgrounds**.
6. (Microsoft Foundry) Select **Try the Speech playground**.
7. (Microsoft Foundry) Select **Real-time transcription**.
8. (Microsoft Foundry) Upload `synthetic-call.wav`.
9. (Microsoft Foundry) Select **Start**.
10. (Microsoft Foundry) Copy the transcript output into Notepad.

### Part B — Redact PII (Language PII redaction playground)
11. (Microsoft Foundry) In the left pane, select **Playgrounds**.
12. (Microsoft Foundry) Select **Try Azure Language Playground**.
13. (Microsoft Foundry) Select **Extract PII from text**.
14. (Microsoft Foundry) Paste the transcript into the input area.
15. (Microsoft Foundry) In the **Configuration** pane, set **Select text language** to **English**.
16. (Microsoft Foundry) In the **Configuration** pane, set **Select types to include** to include these entity types:
    - `Person`
    - `Indian Permanent Account Number`
    - `DateTime`
    - `PhoneNumber`
    - `Email`
    - `ID`
17. (Microsoft Foundry) Select **Detect**.
18. (Microsoft Foundry) Copy the **redacted** output into Notepad.

### Part C — Summarize and route

19. (Your notes) Create a 3–5 bullet summary of the grievance using this format:
		- Customer issue:
		- Impact:
		- What the agent did:
		- Next action required:

20. (Your notes) Assign exactly one routing label from this list:
		- `Collections`
		- `Service request`
		- `Dispute`
		- `Onboarding`


21. (Your notes) Write your final output:
		- Routing label: <one label>
		- Summary: <3–5 bullets>

### Part D — Draft customer communications from the redacted call
22. (Microsoft Foundry) Open the same project using the facilitator-provided **Foundry project link (URL)**.
23. (Microsoft Foundry) In the left pane, select **Playgrounds**.
24. (Microsoft Foundry) Select **Chat**.
25. (Microsoft Foundry) In **Deployment**, select the **Chat model deployment name** from the Prereqs section.
26. (Microsoft Foundry) In the **System message** box, paste the prompt below exactly.

#### Prompt (copy/paste)
```
You are writing customer communications for SK Finance customer care (call centre).

Use only synthetic placeholders; do not invent personal data.
Use the redacted call text and the routing + summary provided.

Create TWO outputs:
1) SMS template (max 320 characters)
2) Email template (subject + body)

Scenario:
- Purpose: Acknowledge the grievance and confirm the next action
- Ticket id: <TICKET_ID>
- Routing label: <ROUTING_LABEL>

Rules:
- Do not include threats, coercion, or collection pressure.
- Do not include real PII.
- Use placeholders <CUSTOMER_NAME>, <CUSTOMER_REF>, <SUPPORT_PHONE>, and <NEXT_CONTACT_DATE>.
- Be polite, clear, and compliant.

Return the result in this exact JSON format:
{
	"sms": "...",
	"email": {
		"subject": "...",
		"body": "..."
	}
}
```

27. (Microsoft Foundry) In the chat input box, paste the prompt below, then select **Send**.

#### Chat input (copy/paste)
```
Redacted call transcript:
<PASTE_REDACTED_TRANSCRIPT_HERE>

Grievance summary (3–5 bullets):
<PASTE_YOUR_SUMMARY_HERE>

Routing label:
<PASTE_YOUR_ROUTING_LABEL_HERE>

Generate the JSON now.
```

28. (Your notes) Copy the model output into Notepad.
29. (Your notes) Replace placeholders with these synthetic values:
		- `<CUSTOMER_NAME>` = `Asha Rao`
		- `<CUSTOMER_REF>` = `SKFIN-DEMO-000123`
		- `<TICKET_ID>` = `SR-2026-0111-0001`
		- `<SUPPORT_PHONE>` = `+91 90000 00000`
		- `<NEXT_CONTACT_DATE>` = `15-Jan-2026`

## Validation
- Microsoft Foundry produces a readable transcript from `synthetic-call.wav`.
- Microsoft Foundry produces a redacted version of the transcript.
- You have:
	- a redacted transcript,
	- a 3–5 bullet grievance summary,
	- exactly one routing label,
	- a JSON output containing one SMS template and one Email subject/body.

## Cleanup
1. (Microsoft Foundry) In the Speech to text playground, remove the uploaded file (if it is still listed).
2. (Microsoft Foundry) In the PII redaction playground, clear the input (select all text and delete).
3. (Microsoft Foundry) In the Chat playground, delete the chat content from the page (select all text and delete) so it is not left visible for the next user.
4. (Azure portal) Do **not** delete shared facilitator resources unless the facilitator tells you to.

## Compliance / safety notes (RBI-aligned)
- Use synthetic recordings only. Do not upload real customer calls.
- Treat transcripts as sensitive: redact personal data and avoid storing raw transcripts beyond the lab.
- In real SK Finance (NBFC) deployments, capture consent, retention, access control, and audit trails for call analytics.

## References
- https://learn.microsoft.com/en-us/azure/ai-services/speech-service/get-started-speech-to-text
- https://learn.microsoft.com/en-us/azure/ai-services/language-service/personally-identifiable-information/quickstart
- https://learn.microsoft.com/en-us/azure/ai-foundry/quickstarts/get-started-playground?view=foundry-classic
