# Student handout — Sign in using Temporary Access Pass (TAP)

## Purpose
Use a **Temporary Access Pass (TAP)** to set up your sign-in security for the lab accounts, so you can sign in to the Azure portal without getting blocked.

## What you need (from the facilitator)
You must get these three values from the facilitator:
- **Username (UPN)**: `SKStudentNNN@quill.com.au`
- **Password**: a temporary password provided to you
- **Temporary Access Pass (TAP)**: a time-limited code provided to you

## Step-by-step
1. (Browser) Open **Security info**: https://aka.ms/mysecurityinfo
2. (Security info page) In the sign-in box, type your **Username (UPN)** (example: `SKStudent001@quill.com.au`), then select **Next**.
3. (Security info page) When you are prompted for a **Temporary Access Pass**, paste the TAP provided by the facilitator, then select **Sign in**.
4. (Security info page) When you see the Security info page, select **Add sign-in method**.
5. (Security info page) Select **Microsoft Authenticator**.
6. (Security info page) Select **Add**, then follow the on-screen steps to:
   - Install Microsoft Authenticator on your phone
   - Add your work/school account
   - Approve the test notification
7. (Browser) Open the Azure portal: https://portal.azure.com
8. (Azure portal) Sign in using your **Username (UPN)** and **Password**.

## Validation
- You can open https://portal.azure.com and sign in successfully.
- In https://aka.ms/mysecurityinfo you can see at least one sign-in method (for example, Microsoft Authenticator).

## Safety rules (must follow)
- Do not share your password or TAP with anyone.
- Do not store passwords/TAPs in chat messages or screenshots.
- When the facilitator confirms the lab is finished, delete any local notes that contain passwords/TAPs.

## Reference
- https://learn.microsoft.com/en-us/entra/identity/authentication/howto-authentication-temporary-access-pass
