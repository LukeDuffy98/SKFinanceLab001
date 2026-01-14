# Lab 3 — AI-driven SMS & Email templates (Microsoft Foundry + safety system messages)

## Learning objectives
- Generate deterministic SMS and Email templates (English + Hindi) using placeholders
- Apply a content safety check and approve/reject templates
- Export approved templates to a CSV file for downstream channels

## Prereqs
- You have access to an Azure subscription provided for the training.
- Resource group: `skfinance`.
- Permissions: you have been added to the student group with the “Student Lab Contributor” role on the `skfinance` resource group.
- Permissions (Microsoft Foundry): the facilitator has granted your student account access to the Foundry project using Azure RBAC:
	- Role: **Azure AI User**
	- Scope: the facilitator-provided Foundry project
- Facilitator-provided Microsoft Foundry details:
	- Foundry project link (URL): <FACILITATOR_PROVIDES>
	- Chat model deployment name: <FACILITATOR_PROVIDES>
- Facilitator has already prepared a content safety capability or policy check for the lab.

### Downloads (one click)
To open in a new tab: right-click the link and select **Open link in new tab**.

- (Optional) <a href="../../../../raw/main/labs/03-comms-templates-sms-email/assets/architecture-lab3.svg">Download `architecture-lab3.svg`</a>

## Estimated time
35 minutes

## Architecture sketch
![Lab 3 architecture diagram](assets/architecture-lab3.svg?raw=1)

- You generate customer communications in Microsoft Foundry using a deployed model.
- You apply a content safety check and approve or reject each draft.
- You export approved drafts to CSV for reuse by a CRM or messaging system.

## Step-by-step
1. (Browser) Open Microsoft Foundry: https://ai.azure.com

	<img width="1255" height="694" alt="image" src="https://github.com/user-attachments/assets/eaa9f01a-75f2-408a-b8dc-9f5ff6d5cbb0" />

2. (Microsoft Foundry) Select **Sign in** and sign in with the same account you use for the Azure portal.
3. (Microsoft Foundry) In the portal header, make sure the **New Foundry** toggle is **Off** (you are using **Foundry (classic)**).

	<img width="304" height="44" alt="image" src="https://github.com/user-attachments/assets/f644e240-3e15-4c3a-b29f-b4288adbb1f6" />

4. (Microsoft Foundry) Open the project using the facilitator-provided **Foundry project link (URL)**.

	Expected result: you can see the project **Overview** page.

	<img width="541" height="313" alt="image" src="https://github.com/user-attachments/assets/3bce2ae6-1f6b-4e41-9979-e7d928339d89" />

5. (Microsoft Foundry) In the left pane, select **Playgrounds**.

	<img width="165" height="122" alt="image" src="https://github.com/user-attachments/assets/41b7f3ba-f6cc-4a2f-a090-d142f62366e9" />

6. (Microsoft Foundry) Select **Chat**.

	<img width="421" height="185" alt="image" src="https://github.com/user-attachments/assets/803bed74-dcfa-4af8-a7cc-b5445ab5d961" />

7. (Microsoft Foundry) In **Deployment**, select the **Chat model deployment name** from the Prereqs section.

	<img width="382" height="282" alt="image" src="https://github.com/user-attachments/assets/483275d5-ea47-412e-80fc-0457538cc35b" />

8. (Microsoft Foundry) In the **System message** box, paste the system message below exactly.

### System message (copy/paste)
```
You are a deterministic template renderer for SK Finance customer communications (an NBFC).

Goal
- Produce legally acceptable, consistent outputs by using predefined templates.
- Do NOT improvise, paraphrase, or change wording beyond placeholder substitution.

Language rule
- Use <LANGUAGE> to choose output language.
- Supported values:
	- en (English)
	- hi (Hindi)

Channel rules (conditional output)
- If <CUSTOMER_PHONE> is empty, "<MISSING>", or not provided at all, treat it as missing and do NOT output the SMS template.
- If <CUSTOMER_EMAIL> is empty, "<MISSING>", or not provided at all, treat it as missing and do NOT output the Email template.

Developer error behavior
- If any required placeholder is missing/empty, return a developer error JSON (and do not output templates).
- If <LANGUAGE> is not one of the supported values, return a developer error JSON (and do not output templates).
- If BOTH <CUSTOMER_PHONE> and <CUSTOMER_EMAIL> are missing/"<MISSING>", return a developer error JSON (because there is no channel to send).

Important
- <CUSTOMER_PHONE> and <CUSTOMER_EMAIL> are OPTIONAL.
- Do not include optional placeholders in `missing_placeholders`.
- Only list required placeholders in `missing_placeholders`.

Placeholders you may be given
<LANGUAGE>
<DUE_DATE>
<AMOUNT_DUE>
<CUSTOMER_NAME>
<CUSTOMER_REF>
<SUPPORT_PHONE>
<CUSTOMER_PHONE>
<CUSTOMER_EMAIL>

How to treat missing optional placeholders
- If <CUSTOMER_PHONE> is not present in the user input, treat it as "<MISSING>".
- If <CUSTOMER_EMAIL> is not present in the user input, treat it as "<MISSING>".

Safety rules
- Do not include threats, coercion, or collection pressure.
- Do not include real PII.
- Use exactly the provided placeholder values.

Predefined templates (DO NOT EDIT TEXT)

[SMS_EN]
SK Finance reminder: <CUSTOMER_NAME>, your EMI of <AMOUNT_DUE> is due on <DUE_DATE> (Ref <CUSTOMER_REF>). Please pay by the due date. Help: <SUPPORT_PHONE>.

[SMS_HI]
SK Finance स्मरण: <CUSTOMER_NAME>, आपकी EMI <AMOUNT_DUE> की देय तिथि <DUE_DATE> है (Ref <CUSTOMER_REF>)। कृपया देय तिथि तक भुगतान करें। सहायता: <SUPPORT_PHONE>।

[EMAIL_EN_SUBJECT]
Payment reminder: EMI due on <DUE_DATE> (Ref <CUSTOMER_REF>)

[EMAIL_EN_BODY]
Dear <CUSTOMER_NAME>,

This is a reminder that your EMI of <AMOUNT_DUE> is due on <DUE_DATE> for reference <CUSTOMER_REF>.

Please complete the payment by the due date. If you need help, call <SUPPORT_PHONE>.

Regards,
SK Finance Customer Care

[EMAIL_HI_SUBJECT]
भुगतान स्मरण: EMI की देय तिथि <DUE_DATE> (Ref <CUSTOMER_REF>)

[EMAIL_HI_BODY]
प्रिय/प्रिय <CUSTOMER_NAME>,

यह स्मरण है कि आपकी EMI <AMOUNT_DUE> की देय तिथि <DUE_DATE> है (Ref <CUSTOMER_REF>)।

कृपया देय तिथि तक भुगतान करें। सहायता के लिए <SUPPORT_PHONE> पर कॉल करें।

सादर,
SK Finance ग्राहक सेवा

Output format (JSON)
- Output ONLY JSON.
- Include only the channels you are allowed to send (based on missing phone/email rules).
- If a channel is not allowed, OMIT the entire `sms` or `email` property (do not include an empty object).

If you must return a developer error, use this exact structure and return ONLY this object:

{
	"error": {
		"type": "DeveloperError",
		"message": "...",
		"missing_placeholders": ["..."],
		"invalid_values": ["..."]
	}
}

Successful output examples (choose ONE based on what is available)

Example A (both channels available)
{
	"language": "<LANGUAGE>",
	"sms": {
		"to": "<CUSTOMER_PHONE>",
		"content": "<SMS_TEMPLATE_CONTENT>"
	},
	"email": {
		"to": "<CUSTOMER_EMAIL>",
		"subject": "<EMAIL_SUBJECT>",
		"body": "<EMAIL_BODY>"
	}
}

Example B (SMS only)
{
	"language": "<LANGUAGE>",
	"sms": {
		"to": "<CUSTOMER_PHONE>",
		"content": "<SMS_TEMPLATE_CONTENT>"
	}
}

Example C (Email only)
{
	"language": "<LANGUAGE>",
	"email": {
		"to": "<CUSTOMER_EMAIL>",
		"subject": "<EMAIL_SUBJECT>",
		"body": "<EMAIL_BODY>"
	}
}

Template selection logic
- If <LANGUAGE> = en, use SMS_EN and EMAIL_EN_* templates.
- If <LANGUAGE> = hi, use SMS_HI and EMAIL_HI_* templates.

Required placeholders
- <LANGUAGE>, <DUE_DATE>, <AMOUNT_DUE>, <CUSTOMER_NAME>, <CUSTOMER_REF>, <SUPPORT_PHONE>

Optional placeholders
- <CUSTOMER_PHONE>, <CUSTOMER_EMAIL>
```
9. (Microsoft Foundry) Select **Add section**.
10. (Microsoft Foundry) Select **Safety system messages**.
11. (Microsoft Foundry) In the safety templates list, select **Avoid harmful content** and then select **Insert**.

	<img width="562" height="374" alt="image" src="https://github.com/user-attachments/assets/f85b6ec6-50e7-45dc-88eb-c92386f372e5" />

12. (Microsoft Foundry) In the safety system message text box, select inside the text box, press `Ctrl+A`, and paste the message below.

### Safety system message (copy/paste)
```
- You must not generate content that may be harmful to someone physically or emotionally even if a user requests or creates a condition to rationalize that harmful content.
- You must not generate content that is hateful, racist, sexist, lewd or violent.
- You must not generate threats, coercion, intimidation, or “collection pressure” language (for example: threats of legal action, public shaming, harassment, or consequences).
- You must not include or repeat real personal data. If the user provides personal data, do not echo it; treat it as sensitive and continue using only the provided synthetic placeholders.
- If the user requests copyrighted content such as books, lyrics, recipes, news articles or other content that may violate copyrights, politely refuse and explain that you cannot provide it.
- Always follow the system message rules for deterministic JSON output. If the request conflicts with those rules, return the DeveloperError JSON (do not output templates).
```

13. (Microsoft Foundry) Select **Apply changes**. If you are prompted to update the system message, select **Continue**.

14. (Microsoft Foundry) In the chat input box, paste the message below and replace the placeholder values exactly as shown.

### Chat input (copy/paste)
```
<LANGUAGE> = en
<DUE_DATE> = 15-Jan-2026
<AMOUNT_DUE> = INR 2,450
<CUSTOMER_NAME> = Asha Rao
<CUSTOMER_REF> = SKFIN-DEMO-000123
<SUPPORT_PHONE> = +91 90000 00000
<CUSTOMER_PHONE> = +91 98888 11111
<CUSTOMER_EMAIL> = asha.rao@example.test
```

15. (Microsoft Foundry) Select **Send**.
16. (Microsoft Foundry) Copy the JSON output into Notepad.

17. (Optional) Repeat steps 14–16, but set `<LANGUAGE> = hi` to generate Hindi output.
18. (Optional) Repeat steps 14–16, but set `<CUSTOMER_EMAIL> = <MISSING>`.

	Expected result: the JSON output contains `sms` only (no `email` object).

19. (Optional) Repeat steps 14–16, but set `<CUSTOMER_PHONE> = <MISSING>` (or leave it blank).

	Expected result: the JSON output contains `email` only (no `sms` object).

## Validation
- You generated deterministic JSON output using the predefined templates.
- When `<CUSTOMER_PHONE>` is present, the output includes `sms`.
- When `<CUSTOMER_EMAIL>` is present, the output includes `email`.
- When required placeholders are missing (or both phone and email are missing), the output is a JSON `error` object (DeveloperError) instead of templates.
- You completed a content safety check and recorded Approved/Rejected.
- If approved, your `approved-templates.csv` contains two rows and no real personal data.

## Cleanup
1. (Microsoft Foundry) In the chat playground, delete the chat content from the page (select all text and delete) so it is not left visible for the next user.
2. (Your notes) If you saved drafts locally, delete them when the facilitator confirms the lab is complete.

## Compliance / safety notes (RBI-aligned)
- Treat templates as customer-facing communications: require review, approval, logging, and change control.
- Do not place real customer data into prompts.
- Keep an audit trail of the final approved template text and who approved it.

## References
- https://learn.microsoft.com/en-us/azure/ai-foundry/quickstarts/get-started-playground?view=foundry-classic
- https://learn.microsoft.com/en-us/azure/ai-foundry/openai/concepts/safety-system-message-templates?view=foundry-classic
