# Semantic Critique — Parabank

Generated: 2026-05-09T22:02:42.235589Z

## Login

**Verdict:** yes  
**Forced ship:** no  

AST accurately captures the interactive elements (two required fields, validations, Sign In submit behavior with success/failure outcomes, and Forgot Password link) with no missing or extraneous interactive items.

**Missing:** none

**Phantoms:** none

---

## Register

**Verdict:** yes  
**Forced ship:** no  

AST accurately captures the form fields, types, validations, submit behavior, and success/failure outcomes; only the explicit list of US states for the State dropdown is not included (minor).

**Missing:**

- components.Registration_Form.fields.State.options (explicit list of all US states for the dropdown)

**Phantoms:** none

---

## Accounts Overview

**Verdict:** yes  
**Forced ship:** no  

AST matches the description with all required interactive elements present; one minor phantom (an explicitly named row action) is acceptable.

**Missing:** none

**Phantoms (hallucinations):**

- components.Accounts_Table.row_actions[0] (action_name 'Open Account' not explicitly named in description)

---

## Open New Account

**Verdict:** yes  
**Forced ship:** no  

The AST accurately captures the account type selection, deposit amount field, funding account dropdown, real-time validations (including conditional minimums and sufficient balance), and the success message with redirect.

**Missing:** none

**Phantoms:** none

---

## Transfer Funds

**Verdict:** yes  
**Forced ship:** no  

AST accurately captures the form fields, conditional destination options, validations, and success/failure behaviors described.

**Missing:** none

**Phantoms:** none

---

## Payments

**Verdict:** yes  
**Forced ship:** no  

AST accurately covers all interactive fields, the Pay button, validation rules, success/failure behaviors; only two minor inferred items noted.

**Missing:** none

**Phantoms (hallucinations):**

- Bill_Payment_Form.fields.Payment_Amount.constraints[0] (must be greater than 0) - not stated in description
- Bill_Payment_Form.submit_actions[0].preconditions[0] (available_funds in Source_Account >= Payment_Amount) - description specifies funds are checked on submit, not a precondition

---

## Request Loan

**Verdict:** yes  
**Forced ship:** no  

AST correctly represents the interactive loan type selection, amount and down-payment fields, collateral dropdown, validation rules, and submit/credit-engine behavior described.

**Missing:** none

**Phantoms:** none

---

## Update Contact Info

**Verdict:** yes  
**Forced ship:** no  

AST correctly represents the editable fields, submit action, validation, success and failure behaviors; only the presence of explicit pre-filled initial values is not represented.

**Missing:**

- components.Update_Contact_Info_Form.initial_values (pre-filled values for the form fields are not represented)

**Phantoms:** none

---

## Manage Cards

**Verdict:** yes  
**Forced ship:** no  

The AST accurately captures both forms, all interactive fields, their validations, and the submit actions (including success messages and validation failure behavior).

**Missing:** none

**Phantoms:** none

---

## Investments

**Verdict:** yes  
**Forced ship:** no  

AST correctly captures both interactive forms, their fields, validations (including conditional buy/sell checks), and success/failure behaviors; no critical elements missing or extraneous.

**Missing:** none

**Phantoms:** none

---

## Account Statements

**Verdict:** yes  
**Forced ship:** no  

The AST accurately captures both forms, their interactive fields, buttons, validation rules, and success/failure behaviors with no missing interactive elements or extraneous items.

**Missing:** none

**Phantoms:** none

---

## Security Settings

**Verdict:** yes  
**Forced ship:** no  

AST accurately represents the collapsible panel, form fields, change button, validation constraints, and success/failure behaviors described.

**Missing:** none

**Phantoms:** none

---

## Support Center

**Verdict:** yes  
**Forced ship:** no  

AST accurately captures both forms, their fields, validation rules, and submit behaviors; one minor optional attribute (explicit 'editable' flag for Phone_Number) is missing.

**Missing:**

- components.Schedule_Callback_Form.fields.Phone_Number.editable

**Phantoms:** none

---
