# Semantic Critique — Parabank

Generated: 2026-05-09T23:14:08.444772Z

## Login

**Verdict:** yes  
**Forced ship:** no  

AST captures the required fields, validations, submit behavior, success/failure outcomes, and the Forgot Password link; one minor inferred action (navigation target) is noted as a phantom.

**Missing:** none

**Phantoms (hallucinations):**

- components.Forgot_Password_Link.on_click (navigates to password reset flow not explicitly stated in description)

---

## Register

**Verdict:** yes  
**Forced ship:** no  

AST correctly captures all interactive fields, validations, and submit behavior; only minor missing detail is the explicit list of US states for the State dropdown.

**Missing:**

- components.Registration_Form.fields.State.options (list of all US states not included)

**Phantoms:** none

---

## Accounts Overview

**Verdict:** yes  
**Forced ship:** no  

AST correctly captures the customer accounts table including masked clickable Account Number (click not implemented), columns, default sort by Open_Date ascending, and footer total balance aggregator.

**Missing:** none

**Phantoms:** none

---

## Open New Account

**Verdict:** yes  
**Forced ship:** no  

AST includes the account-type selector, deposit amount field, funding account dropdown, validations (including conditional minimums), real-time validation flag, and success redirect — suitable to use.

**Missing:** none

**Phantoms:** none

---

## Transfer Funds

**Verdict:** retry (forced ship)  
**Forced ship:** yes  

External account fields lack explicit input types and the submit action has a labeled button not mentioned in the description; regenerate with those fixes.

**Missing:**

- components.Transfer_Form.fields.Destination_Account_External_Number.type
- components.Transfer_Form.fields.Destination_Account_External_Confirm.type

**Phantoms (hallucinations):**

- components.Transfer_Form.submit_actions[0].element_name (Submit Transfer button not specified in the description)

**Fixes applied:**

- Set components.Transfer_Form.fields.Destination_Account_External_Number.type to a concrete input type (e.g., "text" or "account_number") and add any explicit validation pattern if account numbers are numeric.
- Set components.Transfer_Form.fields.Destination_Account_External_Confirm.type to the same concrete input type as the external number (e.g., "text" or "account_number") so the matching constraint applies to a defined input.
- Update components.Transfer_Form.submit_actions[0].element_name to a generic "Submit" label or remove the explicit element_name; alternatively, include the submit button label in the functional description so the AST can accurately reflect the named button.

---

## Payments

**Verdict:** yes  
**Forced ship:** no  

The AST accurately captures the payment form, all specified fields, the Source Account dropdown, the Pay submit action with validation/preconditions, and success/failure behaviors; only one minor inferred constraint was added.

**Missing:** none

**Phantoms (hallucinations):**

- components.Bill_Payment_Form.fields.Payment_Amount.constraints[0] ("must be greater than 0" constraint is an inferred rule not explicitly stated in the description)

---

## Request Loan

**Verdict:** yes  
**Forced ship:** no  

AST correctly captures the loan type cards, amount/type-specific constraints, down payment and collateral fields, validation rules (including 10% min down and 20% collateral), the 80% credit-engine simulation, and success/failure outcomes with reasons; no missing or phantom interactive elements.

**Missing:** none

**Phantoms:** none

---

## Update Contact Info

**Verdict:** yes  
**Forced ship:** no  

AST includes the editable form with all seven prefilled fields, the 'Update Profile' submit action, per-field validation constraints, and success/failure behaviors, matching the description.

**Missing:** none

**Phantoms:** none

---

## Manage Cards

**Verdict:** yes  
**Forced ship:** no  

AST matches the description: both forms, all interactive fields, submit buttons, success/failure behaviors, and validations are present; only small inferred details were added.

**Missing:** none

**Phantoms (hallucinations):**

- Card_Controls_Form.fields.Travel_Notice.fields.Destinations (repeating_group structure and item_fields inferred from 'destinations')
- Card_Controls_Form.fields.New_Spending_Limit.constraints[1] (explicit 'must be <= policy maximum' phrasing inferred from 'validates numeric limits')

---

## Investments

**Verdict:** yes  
**Forced ship:** no  

The AST accurately captures both interactive forms (Trade Funds and Recurring Investment Plan), their fields, validation rules, submit actions, and success/error behaviors as described.

**Missing:** none

**Phantoms:** none

---

## Account Statements

**Verdict:** yes  
**Forced ship:** no  

AST accurately represents both forms, their fields, buttons, validation behavior, and the explicit conditional for statement period; only a couple of minor inferred constraints/conditionals were added that are not verbatim in the description.

**Missing:** none

**Phantoms (hallucinations):**

- components.Statements_Page.components.EStatement_Preference_Form.fields.Email_Address.required_when (the description does not explicitly state the Email Address is required only when Paperless_Opt_in is true)
- components.Statements_Page.components.Generate_Statement_Form.constraints[2] (the constraint 'dates must be valid and within retrievable transaction history' is an inferred detail not explicitly stated)

---

## Security Settings

**Verdict:** yes  
**Forced ship:** no  

The AST accurately represents the collapsible panel, the change-password form with all three password fields, the Change Password button, the required validation constraints, and the success/error behaviors.

**Missing:** none

**Phantoms:** none

---

## Support Center

**Verdict:** yes  
**Forced ship:** no  

AST correctly captures both forms, fields, validations, and submit behaviors; only minor field-type specifics are left unspecified.

**Missing:**

- Secure_Message_Form.fields.Message_Body.type (should be 'rich_text' per description)
- Schedule_Callback_Form.fields.Preferred_Time_Window.type (should indicate time window/time-range control)

**Phantoms:** none

---
