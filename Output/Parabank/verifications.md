# Parabank — Verifications

**Base URL:** 
**Generated:** 2026-04-20T16:59:07.899493
**Source test cases:** Output/Parabank/test-cases.json
**Source spec files:**
- Dataset/Parabank/Parabank.md

## Coverage Summary

| Coverage | Count |
|----------|-------|
| Verifiable | 6 |
| Manual only | 1 |
| Not coverable | 0 |
| **Total records** | **7** |

### Breakdown by verification type

| Type | Count |
|------|-------|
| same_actor_navigation | 6 |
| out_of_band | 1 |
| cross_actor | 0 |
| unobservable_by_design | 0 |

---

## Verifications

### Module 10

#### 10.INVEST-003

- **Type:** `same_actor_navigation`
- **Coverage:** `verifiable`

**Pre-check**
- navigate_to: Investments
- observe:
  - presence of a recurring investment plan row matching the Fund Symbol entered in the test (if present)
  - total number of recurring investment plans listed

**Test case context**
- title: Create recurring investment plan with Weekly frequency
- workflow: Create recurring investment plan
- execution_page: Investments
- test_steps:
  - Fill all required fields (Fund Symbol, Contribution Amount, Frequency set to Weekly, Start Date in the future, Funding Account with adequate balance)
  - Click "Create Plan"
- expected_result: Schedule is stored and confirmation message "Plan created successfully." is displayed.

**Post-check**
- navigate_to: Investments
- observe:
  - presence of a recurring investment plan row matching the Fund Symbol entered in the test with Contribution Amount equal to the amount entered, Frequency 'Weekly', Start Date matching the selected Start Date, and Funding Account matching the selected Funding Account
  - total number of recurring investment plans listed
- expected_change: A new recurring investment plan row appears matching the Fund Symbol, Contribution Amount, Frequency 'Weekly', Start Date, and Funding Account entered during creation; the total number of recurring investment plans increases by 1 compared to the pre-check.

---

### Module 13

#### 13.SUPCEN-003

- **Type:** `out_of_band`
- **Coverage:** `manual_only`
- **Coverage note:** Confirmation email delivery and content cannot be observed within the Support Center UI. Requires access to a test inbox (Mailtrap/Mailhog) or application email logs to confirm receipt and inspect email content.

- trigger_action: Submit Request Callback form by filling Reason for Call, Preferred Date (at least next business day), Preferred Time Window, and Phone Number; click 'Request Callback'.
- channel: email
- recipient: user's email address on file (the account email or the email entered/used on the Request Callback form)
- expected_content:
  - Email subject indicating callback request (e.g., contains 'Callback request' or 'Callback request submitted')
  - Unique request reference or ticket ID
  - Reason for Call as selected in the form
  - Preferred Date (matches the date submitted)
  - Preferred Time Window (matches the time window submitted)
  - Phone Number (matches the number submitted or confirmed)
  - Clear confirmation text stating the callback request was received and any next steps or expected contact timeframe
- in_app_partial_check:
  - navigate_to: Support Center
  - observe: Confirmation message 'Callback request submitted.' displayed on the page; if a reference/ticket ID is shown on the confirmation page, note it to correlate with the email.
- verification_method: Check the test inbox (Mailtrap, Mailhog, or equivalent) for the recipient address within 2 minutes of submission and verify the expected_content items. If test inbox is unavailable, inspect application SMTP/email logs to confirm email delivery and contents; correlate any reference/ticket ID shown on the Support Center confirmation page with the email.

---

### Module 5

#### 5.TRAFUN-001

- **Type:** `same_actor_navigation`
- **Coverage:** `verifiable`

**Pre-check**
- navigate_to: Accounts Overview
- observe:
  - balance of source account
  - balance of destination account

**Test case context**
- title: Perform internal transfer between own accounts successfully
- workflow: Perform internal transfer (select from their own accounts)
- execution_page: Accounts Overview
- test_steps:
  - Select the 'My ParaBank Account' transfer type radio button
  - Fill all required fields (choose Source Account, choose Destination Account from user's own accounts, enter a valid Transfer Amount within available balance)
  - Click 'Transfer'
- expected_result: Displays "Transfer completed successfully." and a transaction ID.

**Post-check**
- navigate_to: Accounts Overview
- observe:
  - balance of source account
  - balance of destination account
- expected_change: Source account balance decreased by transfer amount; destination account balance increased by the same amount; combined total unchanged.

#### 5.TRAFUN-002

- **Type:** `same_actor_navigation`
- **Coverage:** `verifiable`

**Pre-check**
- navigate_to: Accounts Overview
- observe:
  - current balance of the source account selected for the transfer (Checking or Savings)

**Test case context**
- title: Perform external transfer with valid account numbers and sufficient funds
- workflow: Perform external transfer (enter and confirm the account number)
- execution_page: Accounts Overview
- test_steps:
  - Select the radio option for 'External Account' transfer type
  - Fill all required fields (Source Account: select a Checking or Savings account, Transfer Amount: enter an amount within available balance, External Account Number: enter valid account number, Confirm Account Number: enter the same account number)
  - Click 'Submit' or 'Transfer'
- expected_result: 'Transfer completed successfully.' message is shown and a transaction ID is displayed

**Post-check**
- navigate_to: Accounts Overview
- observe:
  - current balance of the source account selected for the transfer (Checking or Savings)
- expected_change: Source account balance decreased by the transfer amount. Destination account is external and cannot be observed within the application.

---

### Module 6

#### 6.PAYMEN-001

- **Type:** `same_actor_navigation`
- **Coverage:** `verifiable`

**Pre-check**
- navigate_to: Accounts Overview
- observe:
  - available balance of the source account that will be selected in the Payments form

**Test case context**
- title: Submit payment with valid details and sufficient funds
- workflow: Submit payment
- execution_page: Accounts Overview
- test_steps:
  - Fill all required fields (Payee Name, Street Address, City, State, ZIP Code, Phone Number, Payee Account Number, Confirm Account Number, Payment Amount, Source Account) ensuring Payee Account Number and Confirm Account Number match and Payment Amount is within available funds
  - Click "Pay"
- expected_result: Payment submitted successfully with a reference code and the source account balance is updated.

**Post-check**
- navigate_to: Accounts Overview
- observe:
  - available balance of the source account that was selected in the Payments form
- expected_change: Source account available balance decreased by the Payment Amount submitted.

#### 6.PAYMEN-002

- **Type:** `same_actor_navigation`
- **Coverage:** `verifiable`

**Pre-check**
- navigate_to: Accounts Overview
- observe:
  - available balance of source account (the account that will be selected in the Payments form)
  - total balance across all accounts

**Test case context**
- title: Form remains editable after validation errors and allows retry
- workflow: Submit payment
- execution_page: Accounts Overview
- test_steps:
  - Fill all required fields with an input that triggers a validation error (for example, mismatched account numbers)
  - Click "Pay"
  - Correct the invalid field(s) so all validations pass, then click "Pay" again
- expected_result: Validation error displayed after the first attempt, the form remains editable, and after correction the payment submits successfully with a reference code and balances update.

**Post-check**
- navigate_to: Accounts Overview
- observe:
  - available balance of source account (the account that was selected in the Payments form)
  - total balance across all accounts
- expected_change: Source account available balance decreased by the Payment Amount entered in the test; total balance across all accounts decreased by the same Payment Amount.

---

### Module 9

#### 9.MANCAR-006

- **Type:** `same_actor_navigation`
- **Coverage:** `verifiable`

**Pre-check**
- navigate_to: Manage Cards
- observe:
  - current travel notice destinations for the selected card

**Test case context**
- title: Add a travel notice with destination only (dates optional)
- workflow: Update Controls
- execution_page: Manage Cards
- test_steps:
  - Select an existing card
  - Fill Travel Notice with destination(s) only, leaving dates blank
  - Click "Update Controls"
- expected_result: The message "Card controls updated successfully." is displayed and the travel notice destination is recorded for the card.

**Post-check**
- navigate_to: Manage Cards
- observe:
  - current travel notice destinations for the selected card
- expected_change: The travel notice destination entered in the test appears in the travel notice destinations list for the selected card. If the destination did not exist in the pre_check list, the list contains one additional entry matching the entered destination.

---
