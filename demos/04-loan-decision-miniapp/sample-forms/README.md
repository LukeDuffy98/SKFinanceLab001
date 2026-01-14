# Sample loan application forms (synthetic)

These files are **synthetic** (fake) loan application forms designed for the loan decision demo.

They are intentionally varied in layout to show that extraction is not guaranteed to be perfect, and to create good classroom discussion.

## How to use

1) Start the demo app.
2) In the browser UI, upload one of the PDFs in this folder.
3) Set **Application ID** to match the file you uploaded (for example `APP-1003`).

## Included forms

- `SKF-Loan-Form-APP-1001-layout-a.pdf`
- `SKF-Loan-Form-APP-1002-layout-b.pdf`
- `SKF-Loan-Form-APP-1003-layout-c.pdf`
- `SKF-Loan-Form-APP-1004-layout-d.pdf`
- `SKF-Loan-Form-APP-1005-layout-e.pdf`
- `SKF-Loan-Form-APP-1006-layout-f.pdf`
- `SKF-Loan-Form-APP-1007-layout-g.pdf` (challenge: label variation)
- `SKF-Loan-Form-APP-1008-layout-h.pdf` (challenge: punctuation + commas)
- `SKF-Loan-Form-APP-1009-layout-i.pdf` (challenge: poor handwriting)
- `SKF-Loan-Form-APP-1010-layout-j.pdf` (blank template for manual fill)

## Important extraction note

The demo code looks for these exact labels in the extracted text:

- `Monthly Income:`
- `Requested Loan Amount:`

All sample PDFs include those labels on purpose.

The two challenge PDFs **do not** include those exact labels on purpose. Upload them to demonstrate why validation matters and why a workflow may route to **Manual review**.

The poor handwriting PDF includes the exact labels, but the values are intentionally hard to read. Upload it to demonstrate OCR quality issues and why human-in-the-loop checks matter.
