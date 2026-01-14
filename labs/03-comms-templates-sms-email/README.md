# Lab 3 — AI-driven SMS & Email templates (Microsoft Foundry + safety system messages)

## Learning objectives
- Generate deterministic SMS and Email templates (English + Hindi) using placeholders
- Apply a content safety check and approve/reject templates
- Export approved templates to a CSV file for downstream channels

## Prereqs
- You have access to an Azure subscription provided for the training.
- Resource group: `skfinance`.
- Permissions: you have been added to the student group with the “Student Lab Contributor” role on the `skfinance` resource group.
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
2. (Microsoft Foundry) Select **Sign in** and sign in with the same account you use for the Azure portal.
3. (Microsoft Foundry) In the portal header, make sure the **New Foundry** toggle is **Off**.
4. (Microsoft Foundry) Open the project using the facilitator-provided **Foundry project link (URL)**.
5. (Microsoft Foundry) In the left pane, select **Playgrounds**.
6. (Microsoft Foundry) Select **Chat**.
7. (Microsoft Foundry) In **Deployment**, select the **Chat model deployment name** from the Prereqs section.
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
- If <CUSTOMER_PHONE> is empty or "<MISSING>", do NOT output the SMS template.
- If <CUSTOMER_EMAIL> is empty or "<MISSING>", do NOT output the Email template.

Developer error behavior
- If any required placeholder is missing/empty, return a developer error JSON (and do not output templates).
- If <LANGUAGE> is not one of the supported values, return a developer error JSON (and do not output templates).
- If BOTH <CUSTOMER_PHONE> and <CUSTOMER_EMAIL> are missing/"<MISSING>", return a developer error JSON (because there is no channel to send).

Placeholders you will be given
<LANGUAGE>
<DUE_DATE>
<AMOUNT_DUE>
<CUSTOMER_NAME>
<CUSTOMER_REF>
<SUPPORT_PHONE>
<CUSTOMER_PHONE>
<CUSTOMER_EMAIL>

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

If you must return a developer error, use this exact structure and return ONLY this object:

{
	"error": {
		"type": "DeveloperError",
		"message": "...",
		"missing_placeholders": ["..."],
		"invalid_values": ["..."]
	}
}

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
11. (Microsoft Foundry) Select the safety system messages provided by the facilitator.
12. (Microsoft Foundry) Select **Apply changes**.
13. (Microsoft Foundry) When prompted to update the system message, select **Continue**.

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

17. (Microsoft Foundry) Run the lab’s content safety check exactly as instructed by the facilitator.

18. (Your notes) Mark the output as:
	- **Approved** if the content safety check is clean and the text follows the rules
	- **Rejected** if it fails the safety check or violates the rules

19. (Your notes) Create a CSV file named `approved-templates.csv` with this header row:

```
template_type,channel,subject_or_na,content
```

20. (Your notes) If your template is approved, add exactly two rows:
	- One row for `sms`
	- One row for `email`
21. (Your notes) Save the CSV file.

22. (Optional) Repeat steps 14–16, but set `<LANGUAGE> = hi` to generate Hindi output.
23. (Optional) Repeat steps 14–16, but set `<CUSTOMER_EMAIL> = <MISSING>`.

	Expected result: the JSON output contains `sms` only (no `email` object).

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
