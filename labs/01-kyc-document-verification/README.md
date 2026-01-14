# Lab 1 — KYC document verification (Azure AI Document Intelligence + Vision)

## Learning objectives
- Use Azure AI Document Intelligence to extract key KYC fields from a synthetic identity document
- Interpret confidence scores and decide what needs manual review
- Use Azure AI Vision Image Analysis to extract basic signals from the image output

## Prereqs
- You have access to an Azure subscription provided for the training.
- Resource group: `skfinance`.
- Permissions: you have been added to the student group with the “Student Lab Contributor” role on the `skfinance` resource group.
- Facilitator-provisioned Azure AI resource names (in `skfinance`):
	- Document Intelligence: `skfdocint61459`
	- Vision: `skfvision61459`
	- Speech (for later labs): `skfspeech61459`
	- Language (for later labs): `skflang61459`
- You have a synthetic sample ID image file provided by the facilitator:
	- File name: `synthetic-kyc-id.jpg`
	- In this repo, the file is located at: `labs/01-kyc-document-verification/samples/synthetic-kyc-id.jpg`

## Estimated time
40 minutes

## Architecture sketch
![Lab 1 architecture diagram](assets/architecture-lab1.svg?raw=1)

- You upload a synthetic image into Document Intelligence Studio.
- Document Intelligence runs a prebuilt extraction model and returns fields + confidence.
- You capture a “manual review” decision for low-confidence fields.
- (Optional) You run the same image through Azure AI Vision Image Analysis (REST API) to capture simple signals (tags + OCR output).

## Step-by-step
1. (Browser) Open the Azure portal: https://portal.azure.com
2. (Azure portal) In the search box at the top, type `Resource groups` and select **Resource groups**. <img width="840" height="245" alt="image" src="https://github.com/user-attachments/assets/af0e7bc5-e935-4c35-b41d-c81fcc652a40" />

3. (Azure portal) Select your lab resource group. <img width="833" height="100" alt="image" src="https://github.com/user-attachments/assets/db6d24fe-84c5-430c-8bde-47fd95a7536c" />

4. (Azure portal) In the resource group **Overview**, locate your **Document Intelligence** resource. <img width="940" height="564" alt="image" src="https://github.com/user-attachments/assets/1dbb8f27-50a7-410e-bd6c-db9f8e87e103" />

5. (Azure portal) Select the Document Intelligence resource.
6. (Azure portal) Select **Keys and Endpoint**. <img width="1024" height="818" alt="image" src="https://github.com/user-attachments/assets/b1dd098a-402c-47b9-8ead-8d57fad16b5b" />

7. (Azure portal) Copy the **Endpoint** value to Notepad. Keep this tab open.
8. (Browser) Open Document Intelligence Studio: https://documentintelligence.ai.azure.com/studio **Note the url redirect to Content Understanding**
9. (Document Intelligence Studio) Select **Sign in** and sign in with the same account you used in the Azure portal. <img width="1263" height="387" alt="image" src="https://github.com/user-attachments/assets/fc08c439-a14c-439d-90ba-eb56c5db81d0" />
10. Start with "Document Intelligence" <img width="560" height="535" alt="image" src="https://github.com/user-attachments/assets/c94f7755-dd79-4ef9-84cf-29d4fd3db175" />

11. (Document Intelligence Studio) On the home page, select **Identity documents**. <img width="1130" height="421" alt="image" src="https://github.com/user-attachments/assets/db54cd01-65ef-4e6b-b381-8ab6c36a764c" />

12. If prompted choose an existing resource as shown here  <img width="973" height="658" alt="image" src="https://github.com/user-attachments/assets/97c8426e-caa6-4b0d-92d1-d8cd4389ba0a" />
13. Close any inofrmational messages
    
14. (Document Intelligence Studio) Select **Upload**. <img width="169" height="221" alt="image" src="https://github.com/user-attachments/assets/5bfd456c-a02a-44ac-ab96-d2c1b18ad375" />
Note: You can download a sample from from the samples folder here : https://github.com/LukeDuffy98/SKFinanceLab001/tree/main/labs/01-kyc-document-verification/samples

15. (Document Intelligence Studio) In the file picker, browse to `labs/01-kyc-document-verification/samples/` and select `synthetic-kyc-id.jpg`.
12. (Document Intelligence Studio) Select **Run analysis**. <img width="694" height="122" alt="image" src="https://github.com/user-attachments/assets/5a96562d-8b76-4353-a69e-52c92ddafe3a" />

13. (Document Intelligence Studio) Wait until the results panel shows extracted fields.
16. (Document Intelligence Studio) In the results, find these fields (names vary by document type):
		- Given name / First name
		- Surname / Last name
		- Date of birth
		- Document number
17. (Document Intelligence Studio) For each field above, record the **value** and the **confidence score** in the table below.
18. (Your notes) Use this rule for manual review: if confidence is **below 0.85**, mark the field as **Manual review required**.
19. (Your notes) Fill in the table:

| Field | Extracted value | Confidence | Manual review required (Yes/No) |
|---|---|---:|---|
| First name |  |  |  |
| Last name |  |  |  |
| Date of birth |  |  |  |
| Document number |  |  |  |

### Optional — Extract tags + OCR using PowerShell (no portal UI)
Use this optional section if you want a simple, repeatable way to call the Vision API without relying on portal UI labels.

20. (Azure portal) Return to your lab resource group.
21. (Azure portal) Select the **Vision** resource: `skfvision61459`.
	- Important: do **not** use the Document Intelligence resource (`skfdocint61459`) for this optional Vision step.
22. (Azure portal) Select **Keys and Endpoint**.
23. (Azure portal) Copy **KEY 1** into Notepad.
24. (Azure portal) Copy the **Endpoint** into Notepad.
25. (Windows) Open **Windows PowerShell ISE**.
26. (PowerShell ISE) Select **File** → **New**.
27. (PowerShell ISE) In the top script pane, paste the script below.
28. (PowerShell ISE) Update only these three values:
		- `$visionEndpoint`
		- `$visionKey`
		- `$repoRoot`
29. (PowerShell ISE) Select the green **Run Script** button.
30. (PowerShell ISE) Confirm you see:
		- A short table of tags
		- A **Quality proxy** summary (OCR line count + top tag confidence)
		- A file named `vision-imageanalysis-output.json` created in the repo root
31. (Your notes) You do **not** need to open the JSON file for this lab. Keep it only for troubleshooting.
32. (Your notes) Delete `vision-imageanalysis-output.json` when you finish the lab.

```powershell
# Optional: Azure AI Vision Image Analysis (REST) for a local image
# Output: tags + OCR, and a JSON file saved to the repo root

# Vision endpoint + key (from the Vision resource 'skfvision61459' in Azure portal > Keys and Endpoint)
# Important: this must be the Vision resource endpoint/key, not Document Intelligence.
$visionEndpoint = "https://skfvision61459.cognitiveservices.azure.com"
$visionKey = "<PASTE_VISION_KEY_1_HERE>"

# Normalize in case you copied an endpoint with a trailing '/'
$visionEndpoint = $visionEndpoint.TrimEnd('/')

# Set this to the folder that contains this repo (the folder that contains the 'labs' folder)
$repoRoot = "<PASTE_YOUR_REPO_ROOT_PATH_HERE>"
Set-Location $repoRoot

$imagePath = Join-Path $repoRoot "labs\01-kyc-document-verification\samples\synthetic-kyc-id.jpg"
if (-not (Test-Path $imagePath)) {
    throw "Image not found: $imagePath"
}

$uri = "$visionEndpoint/computervision/imageanalysis:analyze" +
       "?features=tags,read" +
       "&model-version=latest" +
       "&language=en" +
       "&api-version=2024-02-01"

$headers = @{ "Ocp-Apim-Subscription-Key" = $visionKey }
$bytes = [System.IO.File]::ReadAllBytes($imagePath)

$result = Invoke-RestMethod -Method Post -Uri $uri -Headers $headers -ContentType "application/octet-stream" -Body $bytes

"Top tags:" | Write-Host
$topTags = $result.tagsResult.values | Sort-Object confidence -Descending
$topTags | Select-Object -First 10 name, confidence | Format-Table

# Quick quality proxy (simple checks)
$topTagConfidence = if ($topTags.Count -gt 0) { [double]$topTags[0].confidence } else { 0.0 }
$ocrLineCount = 0
if ($null -ne $result.readResult -and $null -ne $result.readResult.blocks) {
    foreach ($block in $result.readResult.blocks) {
        if ($null -ne $block.lines) {
            $ocrLineCount += @($block.lines).Count
        }
    }
}

"Quality proxy:" | Write-Host
"- OCR lines detected: $ocrLineCount" | Write-Host
"- Top tag confidence: $([Math]::Round($topTagConfidence, 3))" | Write-Host
if ($ocrLineCount -lt 5) {
    "- Flag: LOW OCR LINE COUNT (check blur/glare/cropping)" | Write-Host
}
if ($topTagConfidence -lt 0.5) {
    "- Flag: LOW TOP TAG CONFIDENCE (check image clarity/lighting)" | Write-Host
}

$outPath = Join-Path $repoRoot "vision-imageanalysis-output.json"
$result | ConvertTo-Json -Depth 50 | Out-File -FilePath $outPath -Encoding utf8
"Saved JSON output to: $outPath" | Write-Host
```

## Validation
- Document Intelligence Studio shows extracted fields with confidence scores.
- Your table has all four fields filled with a clear Yes/No manual review decision.
- If you completed the optional PowerShell section, PowerShell ISE prints a **Quality proxy** summary and creates `vision-imageanalysis-output.json`.

## Cleanup
1. (Azure portal) Return to your lab resource group.
2. (Azure portal) If you created any resources yourself during the lab, select each one, then select **Delete**.
3. (Azure portal) In **Delete resources**, type the resource name to confirm, then select **Delete**.
4. (Azure portal) Do **not** delete shared facilitator resources unless the facilitator tells you to.

## Compliance / safety notes (RBI-aligned)
- Use synthetic documents only. Do not upload real PAN, Aadhaar, or customer identity documents.
- Treat extracted fields as sensitive data: keep them in-memory for the lab and do not store them beyond the session.
- Keep resources in approved regions and ensure access is controlled and auditable.

## References
- https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/quickstarts/get-started-studio?view=doc-intel-4.0.0
- https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/prebuilt/id-document?view=doc-intel-4.0.0
- https://learn.microsoft.com/en-us/azure/ai-services/computer-vision/how-to/call-analyze-image-40
