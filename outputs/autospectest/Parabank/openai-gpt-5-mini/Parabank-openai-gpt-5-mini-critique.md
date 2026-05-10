# Semantic Critique — Parabank

Generated: 2026-05-10T05:29:26.612651Z

## Login

**Verdict:** yes  
**Forced ship:** no  

AST captures the required fields, password constraints, sign-in action, forgot-password link, and success/failure behavior; only a minor inferred conditional on the Email/Username field was added.

**Missing:** none

**Phantoms (hallucinations):**

- Login_Form.fields.Email_Username.constraints[0] (conditional 'if value contains @ then must be a valid email format' is an inference not explicitly stated)

---

## Register

**Verdict:** yes  
**Forced ship:** no  

AST accurately captures all interactive fields, constraints, state dropdown options, submit behavior, success message and redirect, with no significant missing items or extraneous elements.

**Missing:** none

**Phantoms:** none

---

## Accounts Overview

**Verdict:** yes  
**Forced ship:** no  

AST matches the description closely; only a minor explicit representation for the clickable Account Number action is omitted.

**Missing:**

- Accounts_Table.columns.Account_Number.on_click

**Phantoms:** none

---

## Open New Account

**Verdict:** yes  
**Forced ship:** no  

AST accurately captures the form, fields, validations (including conditional minimums), real-time validation behavior, submit action, success message, and redirect as described.

**Missing:** none

**Phantoms:** none

---

## Transfer Funds

**Verdict:** yes  
**Forced ship:** no  

AST includes all interactive elements (transfer type radio, source account dropdown filtered to Checking/Savings, transfer amount, conditional internal/external destination inputs, validations, and submit actions) and matches the description.

**Missing:** none

**Phantoms:** none

---

## Payments

**Verdict:** yes  
**Forced ship:** no  

The AST accurately represents the described payment form, fields, submit action, validations, success message with reference code, balance update, and inline errors; only two minor inferred items are flagged.

**Missing:** none

**Phantoms (hallucinations):**

- Payment_Form.fields.Payment_Amount.constraints[0] (inferred 'must be greater than 0' constraint not explicitly stated in the description)
- Payment_Form.fields.ZIP_Code.type (field type set to 'number' inferred; description did not specify a type)

---

## Request Loan

**Verdict:** yes  
**Forced ship:** no  

AST accurately captures all required interactive elements, validations, and the credit simulation; only minor invented labels/reasons were added.

**Missing:** none

**Phantoms (hallucinations):**

- Loan_Request_Form.submit_actions[0] (Request Loan button label not specified in description)
- Loan_Request_Form.submit_actions[0].on_failure.possible_reasons[2] ("Failed credit simulation" reason not in description)

---

## Update Contact Info

**Verdict:** yes  
**Forced ship:** no  

AST accurately captures the editable form, all seven fields, the Update Profile submit action, validation behavior, success message with data refresh, and failure handling with highlighted fields and inline error banner.

**Missing:** none

**Phantoms:** none

---

## Manage Cards

**Verdict:** yes  
**Forced ship:** no  

AST correctly models both forms, their interactive fields, submit actions, and the described validations; only a single minor inferred constraint was added.

**Missing:** none

**Phantoms (hallucinations):**

- Card_Controls_Form.fields.Travel_Notice.constraints[0] (end_date must be on or after start_date — specific constraint inferred from 'date ranges' rather than explicitly stated)

---

## Investments

**Verdict:** yes  
**Forced ship:** no  

AST is acceptable with one minor omission: the read-only Portfolio Snapshot panel should be present as a component with empty fields.

**Missing:**

- components.Portfolio_Snapshot.fields

**Phantoms:** none

---

## Account Statements

**Verdict:** yes  
**Forced ship:** no  

The AST correctly captures both side-by-side forms, their fields, validations, submit actions, and success/failure messages as described.

**Missing:** none

**Phantoms:** none

---

## Security Settings

**Verdict:** yes  
**Forced ship:** no  

The AST accurately represents the collapsible panel, the change-password form (fields and validations), the submit action, precondition of verifying the current password, on_success behavior, and validation error display.

**Missing:** none

**Phantoms:** none

---

## Support Center

**Verdict:** yes  
**Forced ship:** no  

AST matches the described interactive elements; only one minor inferred property was added.

**Missing:** none

**Phantoms (hallucinations):**

- components.Schedule_Callback_Form.fields.Phone_Number.default_value_source (inferred 'user_profile' source not stated in description)

---
