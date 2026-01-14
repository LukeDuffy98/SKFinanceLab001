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
To open in a new tab: right-click the link and select **Open link in new tab**.

- <a href="../../../../raw/main/labs/02-call-analysis-and-grievance-automation/synthetic-call.wav">Download `synthetic-call.wav`</a>
- (Optional) <a href="../../../../raw/main/labs/02-call-analysis-and-grievance-automation/assets/architecture-lab2.svg">Download `architecture-lab2.svg`</a>

## Estimated time
40 minutes

## Architecture sketch
![Lab 2 architecture diagram](assets/architecture-lab2.svg?raw=1)

- Microsoft Foundry transcribes a synthetic audio file into text.
- Microsoft Foundry performs PII redaction.
- You create a summary and a routing label that the SK Finance operations team could act on.

## Step-by-step
1. (Browser) Open Microsoft Foundry: https://ai.azure.com <img width="1255" height="694" alt="image" src="https://github.com/user-attachments/assets/eaa9f01a-75f2-408a-b8dc-9f5ff6d5cbb0" />

2. (Microsoft Foundry) Select **Sign in** and sign in with the same account you use for the Azure portal.
3. (Microsoft Foundry) In the portal header, make sure the **New Foundry** toggle is **Off** (you are using **Foundry (classic)**).  <img width="304" height="44" alt="image" src="https://github.com/user-attachments/assets/f644e240-3e15-4c3a-b29f-b4288adbb1f6" />

4. (Microsoft Foundry) Open the project using the facilitator-provided **Foundry project link (URL)**.
   https://ai.azure.com/foundryProject/overview?tid=6a450216-13ff-486c-8de5-6bbef7b20ae2&wsid=/subscriptions/782036da-846b-492b-99f4-43f86a3e5697/resourceGroups/skfinance/providers/Microsoft.CognitiveServices/accounts/proj-skfinance-nf-resource/projects/proj-skfinance-nf
   <img width="541" height="313" alt="image" src="https://github.com/user-attachments/assets/3bce2ae6-1f6b-4e41-9979-e7d928339d89" />


### Part A — Transcribe the call (Speech to text playground)
5. (Microsoft Foundry) In the left pane, select **Playgrounds**. <img width="165" height="122" alt="image" src="https://github.com/user-attachments/assets/41b7f3ba-f6cc-4a2f-a090-d142f62366e9" />

6. (Microsoft Foundry) Select **Try the Speech playground**. <img width="995" height="442" alt="image" src="https://github.com/user-attachments/assets/8667834a-8db9-4fd0-aebe-20918ca9557d" />

7. (Microsoft Foundry) Select **Fast transcription**.
8. (Microsoft Foundry) Expand Advanced Options and toggle "Speaker diarization" to on and select "Maximum number of speakers" to 2 <img width="271" height="543" alt="image" src="https://github.com/user-attachments/assets/602f041b-6b4e-4913-b75f-2670e8630555" />

9. (Microsoft Foundry) Upload `synthetic-call.wav`. <img width="254" height="166" alt="image" src="https://github.com/user-attachments/assets/573b623a-74f9-4e86-9fa7-f3876e5bb394" />

10. (Microsoft Foundry) Notice it will start automatically.
11. (Microsoft Foundry) Copy the transcript output into Notepad. There is a copy button to copy the transcript. It is different to the download buttin which downloads the wav file. <img width="509" height="118" alt="image" src="https://github.com/user-attachments/assets/72a9a9f8-d39c-4a8a-8dcc-cdf5fef0cf97" />


### Part B — Redact PII (Language PII redaction playground)
11. (Microsoft Foundry) In the left pane, select **Playgrounds**.
12. (Microsoft Foundry) Select **Try Azure Language Playground**.
13. (Microsoft Foundry) Select **Extract PII from text**. You may need to scroll to the right. <img width="924" height="344" alt="image" src="https://github.com/user-attachments/assets/2013e666-6d2c-4cef-89e8-841471c2a685" />

14. (Microsoft Foundry) Paste the transcript into the input area. Notice this text has no speakers identified. It is just the text. You can either copy and paste the previous output form teh crseen, capturing the "Speaker 1" and "Spaeker 2 tags" or we recomend using the "Banking" sample <img width="358" height="223" alt="image" src="https://github.com/user-attachments/assets/ac42e493-3c3a-4f2d-855f-3e5be03b2f3a" />

15. (Microsoft Foundry) In the **Configuration** pane, set **Select text language** to **English**.
16. (Microsoft Foundry) In the **Configuration** pane, set **Select types to include** to include these entity types:
    - `Person`
    - `Indian Permanent Account Number`
    - `DateTime`
    - `PhoneNumber`
    - `Email`
<img width="280" height="168" alt="image" src="https://github.com/user-attachments/assets/27f395b5-6d56-4649-b224-24d7c69c6bb8" />

17. (Microsoft Foundry) Select **Run**. <img width="595" height="91" alt="image" src="https://github.com/user-attachments/assets/71dfdf5d-2db1-4867-bf32-9459db34894e" />

18. (Microsoft Foundry) Set the **Hide PII** and copty output into Notepad. <img width="364" height="40" alt="image" src="https://github.com/user-attachments/assets/8de1a205-61da-4446-9620-eb9289b00436" />


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
24. (Microsoft Foundry) Select **Chat**. <img width="421" height="185" alt="image" src="https://github.com/user-attachments/assets/803bed74-dcfa-4af8-a7cc-b5445ab5d961" />

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
