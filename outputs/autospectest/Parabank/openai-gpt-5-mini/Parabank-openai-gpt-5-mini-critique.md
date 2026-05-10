# Semantic Critique — Parabank

Generated: 2026-05-10T04:51:47.280407Z

## Login

**Verdict:** yes  
**Forced ship:** no  

AST correctly models the login form, both fields with required validations, the Sign In submit behavior (success and failure), and the Forgot Password link; only a minor inferred navigation target was added for the link.

**Missing:** none

**Phantoms (hallucinations):**

- components.Forgot_Password_Link.navigates_to (destination 'Forgot Password page' inferred but not explicitly named in the description)

---

## Register

**Verdict:** yes  
**Forced ship:** no  

AST accurately includes all required form fields, validation constraints (patterns, formats, password rules), state options, Register submit action with success message and redirect, and failure behavior.

**Missing:** none

**Phantoms:** none

---

## Accounts Overview

**Verdict:** yes  
**Forced ship:** no  

AST is acceptable with two minor omissions (Account Status column and the footer total balance) that can be added without structural changes.

**Missing:**

- Accounts_Table.columns[Account Status] (column for Account Status / Active badge is absent)
- Accounts_Table.footer_row.Total_Balance (footer row showing total balance across all accounts is absent)

**Phantoms:** none

---

## Open New Account

**Verdict:** yes  
**Forced ship:** no  

AST accurately represents the interactive elements, validations, real-time errors, and success redirect described.

**Missing:** none

**Phantoms:** none

---

## Transfer Funds

**Verdict:** yes  
**Forced ship:** no  

AST accurately captures the interactive elements, conditional logic, and validations from the description; only two minor inferred artifacts were added.

**Missing:** none

**Phantoms (hallucinations):**

- Transfer_Form.fields.Transfer_Amount.constraints[0] ("must be greater than 0" is an inferred constraint not explicitly stated in the description)
- Transfer_Form.submit_actions[0].element_name ("unspecified_submit"—submit button name/label was not provided in the description)

---

## Payments

**Verdict:** yes  
**Forced ship:** no  

AST includes all interactive fields, the Pay button, validation rules (account match and funds check), and success/error behaviors as described.

**Missing:** none

**Phantoms:** none

---

## Request Loan

**Verdict:** yes  
**Forced ship:** no  

AST includes all interactive elements (loan type selection, amount, down payment, collateral account), required validations, credit engine simulation, and success/denial outcomes as described.

**Missing:** none

**Phantoms:** none

---

## Update Contact Info

**Verdict:** yes  
**Forced ship:** no  

AST correctly models the editable prefilled profile form, required fields, submit action, validation, success message and failure handling.

**Missing:** none

**Phantoms:** none

---

## Manage Cards

**Verdict:** yes  
**Forced ship:** no  

AST is acceptable with only minor inferred items (travel notice modeled as a repeating group and an explicit failure action for the Request Card submit) that do not require regeneration.

**Missing:** none

**Phantoms (hallucinations):**

- Card_Controls_Form.fields.Travel_Notice (modeled as a repeating_group — description only mentions 'Travel Notice (optional dates and destinations)' without explicit multiplicity)
- Card_Request_Form.submit_actions[0].on_failure (explicit failure behavior for Request Card is not described in the text)

---

## Investments

**Verdict:** yes  
**Forced ship:** no  

AST correctly captures both interactive forms, their fields, validations (including the Action-dependent buy/sell checks), submit actions, and success/failure behaviors; no critical items missing or extraneous.

**Missing:** none

**Phantoms:** none

---

## Account Statements

**Verdict:** yes  
**Forced ship:** no  

AST correctly captures both forms, their fields, validation rules, conditional behaviors, and success/failure messages as described.

**Missing:** none

**Phantoms:** none

---

## Security Settings

**Verdict:** yes  
**Forced ship:** no  

The AST correctly models the collapsible panel, the change-password form with three password fields, the Change Password button, the required validations (current-password verification, strong-password policy, matching confirmation), success message, credential update, and field-level validation errors.

**Missing:** none

**Phantoms:** none

---

## Support Center

**Verdict:** yes  
**Forced ship:** no  

The AST accurately represents both forms, their interactive fields, validations, and submit behaviors described; no critical elements are missing and there are no extraneous items.

**Missing:** none

**Phantoms:** none

---
