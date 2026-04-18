# Parabank - Post-Verification Report

**Base URL:** 
**Generated:** 2026-04-18T20:46:44.594062

## Summary

| Metric | Count |
|--------|-------|
| Source Tests Needing Verification | 27 |
| Full Coverage | 3 |
| Partial Coverage | 24 |
| Minimal Coverage | 0 |
| No Coverage | 0 |
| Associated Verification Tests | 33 |

### Top Coverage Gaps

- While 13.SUPCEN-002 creates the ticket and surfaces a ticket ID, it does NOT open the My Requests/ticket listing or inspect the ticket's subject, category and status. Because the execution_strategy is after_only, the verification test itself must confirm the ticket appears in the listing with correct fields; the candidate stops short of that.
- The test operates in the correct module and creates a ticket, but it explicitly has no attachment and does not open the ticket detail or check the attachments section. Because execution_strategy is after_only, the verification test must itself confirm the uploaded file is listed with a downloadable/view link — this test as written cannot do that.
- The case runs on the correct Payments module and executes a successful payment, but its expected checks focus on account balance update rather than verifying the confirmation UI or the payment_reference code. As written it cannot, by itself (after_only), confirm the required visible payment_reference and success message.
- The candidate runs in the correct module and checks the success UI notification with tracking ID, but it requests a Credit card (requirement expects Debit) and does not verify the Requests/Request History entry or the saved shipping address/card_request_status. As written it cannot alone confirm the new record's type and address.
- Matches the Accounts Overview module and inspects the account table columns (including Account Type and Account Status) but does not currently check for loan-specific details (loan amount/terms) or assert the account_type equals 'Loan/Personal'. As an after_only verification it must confirm the new loan entry and its loan details by itself, which the candidate does not currently do.
- Operates on the Request Loan module (not Accounts Overview). While it notes a displayed collateral account balance, it does not access/display the Accounts Overview available balance or any collateral_hold indicators as required by the verification scenario.
- All three candidates operate in the Manage Cards module and allow selecting a card and setting Card Status, but none include an explicit assertion that the card detail/status badge displays the new status. Because the execution_strategy is after_only, the test must confirm the outcome by itself; the candidate only confirms a success message, not the displayed card_status.
- This test runs in the correct module and already confirms the success message and returned statement data, but it targets a custom date range (not the Month/Year selection) and does not explicitly assert that the statement header lists the selected account and month/year. As written it cannot fully confirm the required header content.
- This test operates on the correct module and confirms the success message, but it does not explicitly capture or verify the created callback request record or its details (reason, scheduled date/time window, phone number). Because execution_strategy is after_only, the test must itself confirm the record and field values; the candidate only partially meets that need.
- Although the test operates on the correct module and does interact with the contact fields, as written it populates invalid formats and submits the form to verify validation errors. That submission would modify/interfere with the profile state and does not explicitly record the pre-filled field values needed for the before_after verification. Therefore it cannot be used as-is but could be adapted to serve as the observation step.

---

## Post-Verification Source Tests

### 10.INVEST-001: Execute a Buy trade successfully and update holdings

| Field | Value |
|-------|-------|
| Module | Investments |
| Workflow | Execute Trade |
| Test Type | positive |
| Priority | High |
| Coverage | full |
| Modifies State | trade_execution, cash_balance, fund_holdings |

#### Source Test Details

**Preconditions:** User is logged in and Execute Trade form is visible; customer has sufficient buying power.

**Steps:**
1. Fill all required fields (Action set to Buy, Fund Symbol selected via autocomplete, Quantity with a valid positive amount, Funding Account selected)
2. Click "Execute Trade"
3. Verify confirmation area displays success message and order details

**Expected Result:** A same-day trade is executed; confirmation displays "Trade executed successfully." with an order ID and portfolio holdings are updated.

#### Verification Mapping

| # | Ideal Verification | Status | Strategy | Matched Test | Confidence |
|---|--------------------|--------|----------|--------------|------------|
| 1 | Verify the trade confirmation is shown with a success message and an order ID | found | After Only | 10.INVEST-002 - Execute a Sell trade successfully and update holdings | 85% |
| 2 | Verify the fund holdings increased by the purchased quantity in the portfolio snapshot | found | Before/After | 10.INVEST-007 - Portfolio snapshot displays current holdings and read-only values | 90% |
| 3 | Verify the funding account's cash balance decreased by the trade cash amount | found | Before/After | 3.ACCOVE-003 - Footer displays the total balance across all accounts | 85% |

#### Execution Plan

| Step | Phase | Action | Test ID | Purpose |
|------|-------|--------|---------|---------|
| 1 | pre_verify | execute_test | 10.INVEST-007 | Record current holdings quantity for the fund in the portfolio snapshot before placing the buy order |
| 2 | navigate | navigate | - | Navigate to Accounts Overview |
| 3 | pre_verify | execute_test | 3.ACCOVE-003 | Record the funding account's current balance shown on Accounts Overview before executing the trade |
| 4 | navigate | navigate | - | Navigate to Investments |
| 5 | action | execute_test | 10.INVEST-001 | Execute the action: Execute a Buy trade successfully and update holdings |
| 6 | post_verify | execute_test | 10.INVEST-002 | Verify the trade confirmation is shown with a success message and an order ID |
| 7 | post_verify | execute_test | 10.INVEST-007 | Confirm the holdings quantity equals the recorded before value plus the purchased quantity |
| 8 | navigate | navigate | - | Navigate to Accounts Overview |
| 9 | post_verify | execute_test | 3.ACCOVE-003 | Confirm the funding account balance decreased by the executed trade cash amount and matches expec... |

---

### 10.INVEST-002: Execute a Sell trade successfully and update holdings

| Field | Value |
|-------|-------|
| Module | Investments |
| Workflow | Execute Trade |
| Test Type | positive |
| Priority | High |
| Coverage | partial |
| Modifies State | trade_execution, cash_balance, fund_holdings |

#### Source Test Details

**Preconditions:** User is logged in and Execute Trade form is visible; customer holds sufficient shares of the selected fund.

**Steps:**
1. Fill all required fields (Action set to Sell, Fund Symbol selected via autocomplete, Quantity within held shares, Destination Account selected)
2. Click "Execute Trade"
3. Verify confirmation area displays success message and order details

**Expected Result:** A same-day trade is executed; confirmation displays "Trade executed successfully." with an order ID and portfolio holdings are updated.

#### Verification Mapping

| # | Ideal Verification | Status | Strategy | Matched Test | Confidence |
|---|--------------------|--------|----------|--------------|------------|
| 1 | Verify the sell trade confirmation is shown with a success message and an order ID | partial | After Only | 10.INVEST-001 - Execute a Buy trade successfully and update holdings | 78% |
| 2 | Verify the fund holdings decreased by the sold quantity in the portfolio snapshot | found | Before/After | 10.INVEST-007 - Portfolio snapshot displays current holdings and read-only values | 90% |
| 3 | Verify proceeds from the sale increased the selected destination account's cash balance | found | Before/After | 3.ACCOVE-003 - Footer displays the total balance across all accounts | 90% |

#### Coverage Gaps

- The test targets the correct module and checks the confirmation UI (success message and order details), which is exactly what must be observed after a trade. However, it specifically executes a Buy trade rather than a Sell; the requirement demands verifying a Sell trade confirmation, so the candidate does not fully match as-is.

#### Execution Plan

| Step | Phase | Action | Test ID | Purpose |
|------|-------|--------|---------|---------|
| 1 | pre_verify | execute_test | 10.INVEST-007 | Record current holdings quantity for the fund in the portfolio snapshot before placing the sell o... |
| 2 | navigate | navigate | - | Navigate to Accounts Overview |
| 3 | pre_verify | execute_test | 3.ACCOVE-003 | Record the destination account's current balance on Accounts Overview before executing the sell |
| 4 | navigate | navigate | - | Navigate to Investments |
| 5 | action | execute_test | 10.INVEST-002 | Execute the action: Execute a Sell trade successfully and update holdings |
| 6 | post_verify | execute_test_partial | 10.INVEST-001 | Verify the sell trade confirmation is shown with a success message and an order ID |
| 7 | post_verify | execute_test | 10.INVEST-007 | Confirm the holdings quantity equals the recorded before value minus the sold quantity |
| 8 | navigate | navigate | - | Navigate to Accounts Overview |
| 9 | post_verify | execute_test | 3.ACCOVE-003 | Confirm the account balance increased by the expected proceeds amount and matches expected post-t... |

---

### 10.INVEST-003: Create recurring investment plan with Weekly frequency

| Field | Value |
|-------|-------|
| Module | Investments |
| Workflow | Create Plan |
| Test Type | positive |
| Priority | High |
| Coverage | partial |
| Modifies State | trade_execution, fund_holdings |

#### Source Test Details

**Preconditions:** User is logged in and the Create Plan form is open.

**Steps:**
1. Fill all required fields (Fund Symbol, Contribution Amount, Frequency, Start Date, Funding Account) with valid values and select Weekly frequency
2. Click "Create Plan"

**Expected Result:** Plan created successfully. The schedule is stored and a confirmation message "Plan created successfully." is shown.

#### Verification Mapping

| # | Ideal Verification | Status | Strategy | Matched Test | Confidence |
|---|--------------------|--------|----------|--------------|------------|
| 1 | Verify the recurring investment plan is created and confirmation message is shown | partial | After Only | 10.INVEST-004 - Create recurring investment plan with Monthly frequency | 65% |
| 2 | Verify the new recurring plan appears in the portfolio/plan listing (plan stored for future executions) | partial | After Only | 10.INVEST-004 - Create recurring investment plan with Monthly frequency | 60% |

#### Coverage Gaps

- Although it verifies creation and the 'Plan created successfully.' message, it uses Monthly frequency (requirement needs Weekly) and does not include checks of the scheduled plans list or the trade_status. The other candidates are validation/error cases and do not verify successful creation.
- Closest match is a create-recurring-plan test in the correct module, but it does not open the Recurring Plans listing or assert stored plan attributes. It also uses Monthly frequency in the test (mismatch with expected Weekly). As an after_only verification, the test must confirm the new record exists in the listing with the specified attributes; the candidate currently does not do that.

#### Execution Plan

| Step | Phase | Action | Test ID | Purpose |
|------|-------|--------|---------|---------|
| 1 | action | execute_test | 10.INVEST-003 | Execute the action: Create recurring investment plan with Weekly frequency |
| 2 | post_verify | execute_test_partial | 10.INVEST-004 | Verify the recurring investment plan is created and confirmation message is shown |
| 3 | post_verify | execute_test_partial | 10.INVEST-004 | Verify the new recurring plan appears in the portfolio/plan listing (plan stored for future execu... |

---

### 10.INVEST-004: Create recurring investment plan with Monthly frequency

| Field | Value |
|-------|-------|
| Module | Investments |
| Workflow | Create Plan |
| Test Type | positive |
| Priority | High |
| Coverage | partial |
| Modifies State | trade_execution, fund_holdings |

#### Source Test Details

**Preconditions:** User is logged in and the Create Plan form is open.

**Steps:**
1. Fill all required fields (Fund Symbol, Contribution Amount, Frequency, Start Date, Funding Account) with valid values and select Monthly frequency
2. Click "Create Plan"

**Expected Result:** Plan created successfully. The schedule is stored and a confirmation message "Plan created successfully." is shown.

#### Verification Mapping

| # | Ideal Verification | Status | Strategy | Matched Test | Confidence |
|---|--------------------|--------|----------|--------------|------------|
| 1 | Verify the recurring investment plan is created and confirmation message is shown | partial | After Only | 10.INVEST-003 - Create recurring investment plan with Weekly frequency | 65% |
| 2 | Verify the new recurring plan appears in the plans listing with the correct schedule | partial | After Only | 10.INVEST-003 - Create recurring investment plan with Weekly frequency | 60% |

#### Coverage Gaps

- This candidate is on the correct module and already checks for the confirmation message and that the schedule is stored, but it uses Weekly frequency (requirement expects Monthly) and does not explicitly verify the presence and full details of the scheduled plan record or the plan's trade_status in the user's Recurring/Scheduled Plans list. Therefore it cannot fully confirm the after-only expected outcome without modification.
- The candidate is on the correct module and concerns recurring plans, but it does not access the Recurring Plans listing nor assert the plan's frequency or next run date. As written it cannot, by itself, confirm the expected outcome required by an after_only verification.

#### Execution Plan

| Step | Phase | Action | Test ID | Purpose |
|------|-------|--------|---------|---------|
| 1 | action | execute_test | 10.INVEST-004 | Execute the action: Create recurring investment plan with Monthly frequency |
| 2 | post_verify | execute_test_partial | 10.INVEST-003 | Verify the recurring investment plan is created and confirmation message is shown |
| 3 | post_verify | execute_test_partial | 10.INVEST-003 | Verify the new recurring plan appears in the plans listing with the correct schedule |

---

### 11.ACCSTA-001: Generate statement using month-and-year period

| Field | Value |
|-------|-------|
| Module | Account Statements |
| Workflow | Generate Statement |
| Test Type | positive |
| Priority | High |
| Coverage | partial |
| Modifies State | statement_generation |

#### Source Test Details

**Preconditions:** User is signed in and on the Account Statements page with the form visible.

**Steps:**
1. Select Statement Period as a month-and-year
2. Select Account from the Account dropdown
3. Click "Generate Statement"

**Expected Result:** Displays 'Statement generated successfully.' and the generated statement shows the retrieved transactions for the selected month.

#### Verification Mapping

| # | Ideal Verification | Status | Strategy | Matched Test | Confidence |
|---|--------------------|--------|----------|--------------|------------|
| 1 | Verify a generated statement record exists for the selected account and month and that a success notification is shown | partial | After Only | 11.ACCSTA-002 - Generate statement using custom date range | 75% |
| 2 | Verify the generated statement's transaction list contains only transactions from the selected month and that totals ... | partial | After Only | 11.ACCSTA-002 - Generate statement using custom date range | 72% |

#### Coverage Gaps

- This test runs in the correct module and already confirms the success message and returned statement data, but it targets a custom date range (not the Month/Year selection) and does not explicitly assert that the statement header lists the selected account and month/year. As written it cannot fully confirm the required header content.
- This test operates in the correct module and displays the generated statement with the retrieved transactions for the selected date range, so it exposes the required transaction_list data. However, the test's existing expected outcome only asserts that transactions are shown and a success message is displayed; it does not validate that every transaction date falls within the selected month or that the displayed totals equal the sum of the listed transactions. Because the execution strategy is after_only, the verification test must confirm those outcomes by itself — which this candidate does not currently do.

#### Execution Plan

| Step | Phase | Action | Test ID | Purpose |
|------|-------|--------|---------|---------|
| 1 | action | execute_test | 11.ACCSTA-001 | Execute the action: Generate statement using month-and-year period |
| 2 | post_verify | execute_test_partial | 11.ACCSTA-002 | Verify a generated statement record exists for the selected account and month and that a success ... |
| 3 | post_verify | execute_test_partial | 11.ACCSTA-002 | Verify the generated statement's transaction list contains only transactions from the selected mo... |

---

### 11.ACCSTA-002: Generate statement using custom date range

| Field | Value |
|-------|-------|
| Module | Account Statements |
| Workflow | Generate Statement |
| Test Type | positive |
| Priority | High |
| Coverage | partial |
| Modifies State | statement_generation |

#### Source Test Details

**Preconditions:** User is signed in and on the Account Statements page with the form visible.

**Steps:**
1. Select Statement Period as custom date range and enter a valid start date and end date
2. Select Account from the Account dropdown
3. Click "Generate Statement"

**Expected Result:** Displays 'Statement generated successfully.' and the generated statement shows the retrieved transactions for the specified date range.

#### Verification Mapping

| # | Ideal Verification | Status | Strategy | Matched Test | Confidence |
|---|--------------------|--------|----------|--------------|------------|
| 1 | Verify a generated statement record exists for the specified custom date range and that a success notification is shown | partial | After Only | 11.ACCSTA-001 - Generate statement using month-and-year period | 72% |
| 2 | Verify the generated statement's transaction list contains only transactions within the specified date range and tota... | partial | After Only | 11.ACCSTA-001 - Generate statement using month-and-year period | 70% |

#### Coverage Gaps

- This test operates in the correct module and already checks for the success notification and generated statement content, but it uses a month-and-year period rather than a custom date range and does not explicitly assert that the statement header lists the selected account and the given start and end dates. Because the execution strategy is after_only, the verification must confirm the specific custom-date outcome and header contents — which this test does not fully cover.
- The test operates in the correct module and displays the generated statement with transactions for the selected period, but it does not currently verify that every transaction date falls within the requested start/end dates nor that the displayed totals equal the computed sum. Therefore it cannot, as written, fully confirm the required outcome in an after-only run.

#### Execution Plan

| Step | Phase | Action | Test ID | Purpose |
|------|-------|--------|---------|---------|
| 1 | action | execute_test | 11.ACCSTA-002 | Execute the action: Generate statement using custom date range |
| 2 | post_verify | execute_test_partial | 11.ACCSTA-001 | Verify a generated statement record exists for the specified custom date range and that a success... |
| 3 | post_verify | execute_test_partial | 11.ACCSTA-001 | Verify the generated statement's transaction list contains only transactions within the specified... |

---

### 11.ACCSTA-003: Save e-Statement preference with a valid email

| Field | Value |
|-------|-------|
| Module | Account Statements |
| Workflow | Save Preference |
| Test Type | positive |
| Priority | High |
| Coverage | partial |
| Modifies State | e_statement_preference |

#### Source Test Details

**Preconditions:** User is signed in and on the Account Statements page.

**Steps:**
1. Check the paperless statements checkbox and fill a valid email address in the Email Address field
2. Click "Save Preference"

**Expected Result:** Displays 'e-Statement preference updated.' and the paperless preference is saved (checkbox remains selected and the entered email is shown).

#### Verification Mapping

| # | Ideal Verification | Status | Strategy | Matched Test | Confidence |
|---|--------------------|--------|----------|--------------|------------|
| 1 | Verify the e-Statement preference is saved and the UI persists the paperless checkbox and email after saving | partial | After Only | 11.ACCSTA-008 - Save preference with invalid email format | 70% |
| 2 | Verify the saved e-statement email is reflected in the user's contact/profile information | partial | After Only | 8.UCI-001 - Update profile with all valid contact fields | 60% |

#### Coverage Gaps

- Though on the correct page and manipulating the relevant fields, the candidate test is written to validate an invalid-email failure case (expecting validation errors and that the preference is not saved). It does not confirm the successful save or persistence required by the after_only verification.
- The candidate runs on the Update Contact Info module and validates profile updates, but none of the provided test cases explicitly access or verify the email/contact email field. Because the verification must confirm the saved e-statement email after the action (after_only), the test must explicitly read and assert the email value; the current test does not.

#### Execution Plan

| Step | Phase | Action | Test ID | Purpose |
|------|-------|--------|---------|---------|
| 1 | action | execute_test | 11.ACCSTA-003 | Execute the action: Save e-Statement preference with a valid email |
| 2 | post_verify | execute_test_partial | 11.ACCSTA-008 | Verify the e-Statement preference is saved and the UI persists the paperless checkbox and email a... |
| 3 | navigate | navigate | - | Navigate to Update Contact Info |
| 4 | post_verify | execute_test_partial | 8.UCI-001 | Verify the saved e-statement email is reflected in the user's contact/profile information |

---

### 12.SECSET-001: Change password with valid current and strong matching new password

| Field | Value |
|-------|-------|
| Module | Security Settings |
| Workflow | Change Password |
| Test Type | positive |
| Priority | High |
| Coverage | full |
| Modifies State | credentials_update, password_change |

#### Source Test Details

**Preconditions:** User is authenticated and Security Settings > Change Password panel is open

**Steps:**
1. Expand the Change Password panel if collapsed
2. Fill all required fields (Current Password: valid current password, New Password: valid strong password, Confirm New Password: same as New Password)
3. Click "Change Password"

**Expected Result:** Password changed successfully and credentials are updated.

#### Verification Mapping

| # | Ideal Verification | Status | Strategy | Matched Test | Confidence |
|---|--------------------|--------|----------|--------------|------------|
| 1 | Verify the Security Settings UI shows a successful password change confirmation | found | After Only | 12.SECSET-006 - Change password using a minimally-compliant strong password | 72% |
| 2 | Verify authentication changed by confirming the old password no longer works and the new password can be used to sign in | found | Before/After | 1.LOGIN-008 - After changing password the old password no longer works | 95% |

#### Execution Plan

| Step | Phase | Action | Test ID | Purpose |
|------|-------|--------|---------|---------|
| 1 | navigate | navigate | - | Navigate to Login |
| 2 | pre_verify | execute_test | 1.LOGIN-008 | Attempt to sign out (if signed in) and perform a login with the current (old) password to confirm... |
| 3 | navigate | navigate | - | Navigate to Security Settings |
| 4 | action | execute_test | 12.SECSET-001 | Execute the action: Change password with valid current and strong matching new password |
| 5 | post_verify | execute_test | 12.SECSET-006 | Verify the Security Settings UI shows a successful password change confirmation |
| 6 | navigate | navigate | - | Navigate to Login |
| 7 | post_verify | execute_test | 1.LOGIN-008 | Sign out and attempt login with the old password (expect failure); then attempt login with the ne... |

---

### 13.SUPCEN-001: Send message successfully with required fields (no attachment)

| Field | Value |
|-------|-------|
| Module | Support Center |
| Workflow | Send Message |
| Test Type | positive |
| Priority | High |
| Coverage | partial |
| Modifies State | support_ticket_creation |

#### Source Test Details

**Preconditions:** User is logged in and the Support Center Send Message form is visible

**Steps:**
1. Fill all required fields (Subject with a valid-length subject, Category, Message Body with valid content)
2. Click "Send Message"

**Expected Result:** A success notification "Message sent successfully." is displayed and a ticket ID is shown

#### Verification Mapping

| # | Ideal Verification | Status | Strategy | Matched Test | Confidence |
|---|--------------------|--------|----------|--------------|------------|
| 1 | Verify a support ticket is created and a success notification plus ticket ID are shown | found | After Only | 13.SUPCEN-002 - Send message successfully with a valid attachment | 90% |
| 2 | Verify the created ticket appears in the user's support ticket listing with correct subject/category and initial status | partial | After Only | 13.SUPCEN-002 - Send message successfully with a valid attachment | 62% |

#### Coverage Gaps

- While 13.SUPCEN-002 creates the ticket and surfaces a ticket ID, it does NOT open the My Requests/ticket listing or inspect the ticket's subject, category and status. Because the execution_strategy is after_only, the verification test itself must confirm the ticket appears in the listing with correct fields; the candidate stops short of that.

#### Execution Plan

| Step | Phase | Action | Test ID | Purpose |
|------|-------|--------|---------|---------|
| 1 | action | execute_test | 13.SUPCEN-001 | Execute the action: Send message successfully with required fields (no attachment) |
| 2 | post_verify | execute_test | 13.SUPCEN-002 | Verify a support ticket is created and a success notification plus ticket ID are shown |
| 3 | post_verify | execute_test_partial | 13.SUPCEN-002 | Verify the created ticket appears in the user's support ticket listing with correct subject/categ... |

---

### 13.SUPCEN-002: Send message successfully with a valid attachment

| Field | Value |
|-------|-------|
| Module | Support Center |
| Workflow | Send Message |
| Test Type | positive |
| Priority | High |
| Coverage | partial |
| Modifies State | support_ticket_creation |

#### Source Test Details

**Preconditions:** User is logged in and the Support Center Send Message form is visible

**Steps:**
1. Fill all required fields (Subject with a valid-length subject, Category, Message Body with valid content) and attach a supported file type
2. Click "Send Message"

**Expected Result:** A success notification "Message sent successfully." is displayed and a ticket ID is shown

#### Verification Mapping

| # | Ideal Verification | Status | Strategy | Matched Test | Confidence |
|---|--------------------|--------|----------|--------------|------------|
| 1 | Verify a support ticket is created with attachment and a success notification plus ticket ID are shown | partial | After Only | 13.SUPCEN-001 - Send message successfully with required fields (no attachment) | 70% |
| 2 | Verify the ticket detail shows the uploaded attachment with filename and a downloadable link | partial | After Only | 13.SUPCEN-001 - Send message successfully with required fields (no attachment) | 40% |

#### Coverage Gaps

- The candidate validates the success message and ticket ID but explicitly covers a message sent without an attachment. The requirement requires confirming creation with an attachment and verifying the attachment presence, which this test does not do.
- The test operates in the correct module and creates a ticket, but it explicitly has no attachment and does not open the ticket detail or check the attachments section. Because execution_strategy is after_only, the verification test must itself confirm the uploaded file is listed with a downloadable/view link — this test as written cannot do that.

#### Execution Plan

| Step | Phase | Action | Test ID | Purpose |
|------|-------|--------|---------|---------|
| 1 | action | execute_test | 13.SUPCEN-002 | Execute the action: Send message successfully with a valid attachment |
| 2 | post_verify | execute_test_partial | 13.SUPCEN-001 | Verify a support ticket is created with attachment and a success notification plus ticket ID are ... |
| 3 | post_verify | execute_test_partial | 13.SUPCEN-001 | Verify the ticket detail shows the uploaded attachment with filename and a downloadable link |

---

### 13.SUPCEN-003: Submit Request Callback with valid inputs

| Field | Value |
|-------|-------|
| Module | Support Center |
| Workflow | Request Callback |
| Test Type | positive |
| Priority | High |
| Coverage | partial |
| Modifies State | callback_request_creation |

#### Source Test Details

**Preconditions:** User is signed in and the Request Callback form is displayed

**Steps:**
1. Fill all required fields (select Reason for Call, choose a valid Preferred Date at least the next business day, choose a Preferred Time Window, verify or edit Phone Number to a valid format)
2. Click "Request Callback"

**Expected Result:** A success message "Callback request submitted." is displayed and an email confirmation is sent.

#### Verification Mapping

| # | Ideal Verification | Status | Strategy | Matched Test | Confidence |
|---|--------------------|--------|----------|--------------|------------|
| 1 | Verify the callback request is created and a success message is displayed with request details | partial | After Only | 13.SUPCEN-010 - Submit with Preferred Date set to the next business day (boundary) | 70% |
| 2 | Verify the system recorded/sent a confirmation for the callback request (confirmation flag or outbound confirmation r... | partial | After Only | 13.SUPCEN-010 - Submit with Preferred Date set to the next business day (boundary) | 65% |

#### Coverage Gaps

- This test operates on the correct module and confirms the success message, but it does not explicitly capture or verify the created callback request record or its details (reason, scheduled date/time window, phone number). Because execution_strategy is after_only, the test must itself confirm the record and field values; the candidate only partially meets that need.
- The test operates in the correct module and exercises creating a callback request (and expects an email), but it does not include steps to open the callback request detail or verify a confirmation flag/reference in the request record — which is required for after_only verification.

#### Execution Plan

| Step | Phase | Action | Test ID | Purpose |
|------|-------|--------|---------|---------|
| 1 | action | execute_test | 13.SUPCEN-003 | Execute the action: Submit Request Callback with valid inputs |
| 2 | post_verify | execute_test_partial | 13.SUPCEN-010 | Verify the callback request is created and a success message is displayed with request details |
| 3 | post_verify | execute_test_partial | 13.SUPCEN-010 | Verify the system recorded/sent a confirmation for the callback request (confirmation flag or out... |

---

### 4.ONA-001: Open a new Checking account with valid initial deposit

| Field | Value |
|-------|-------|
| Module | Open New Account |
| Workflow | Open Account |
| Test Type | positive |
| Priority | High |
| Coverage | partial |
| Modifies State | account_opening, funding_transfer, account_status |

#### Source Test Details

**Preconditions:** User is logged in and Open New Account page is open.

**Steps:**
1. Select Account type = Checking and fill all required fields (Initial Deposit Amount: valid amount above checking minimum, Funding Source Account: account with sufficient balance)
2. Click "Open Account"

**Expected Result:** "Account opened successfully!" is displayed and user is redirected to accounts overview; the new checking account appears in the accounts listing.

#### Verification Mapping

| # | Ideal Verification | Status | Strategy | Matched Test | Confidence |
|---|--------------------|--------|----------|--------------|------------|
| 1 | Verify the Open New Account UI shows the success confirmation and redirects to the accounts overview | found | After Only | 4.ONA-002 - Open a new Savings account with valid initial deposit | 85% |
| 2 | Verify the new Checking account appears in the Accounts Overview listing with correct type and an Open status | partial | After Only | 3.ACCOVE-002 - Accounts table displays expected columns in each row | 65% |
| 3 | Verify the funding source account balance decreased by the initial deposit amount | found | Before/After | 3.ACCOVE-003 - Footer displays the total balance across all accounts | 90% |

#### Coverage Gaps

- Operates on the correct module and displays the relevant fields (account type and status), but it does not assert a specific account_type value ('Checking'), does not verify the masked account number content, and expects an 'Active' badge rather than explicitly checking for 'Open'. Therefore it cannot, by itself, confirm the after-only expected outcome.

#### Execution Plan

| Step | Phase | Action | Test ID | Purpose |
|------|-------|--------|---------|---------|
| 1 | navigate | navigate | - | Navigate to Accounts Overview |
| 2 | pre_verify | execute_test | 3.ACCOVE-003 | Record the funding source account's balance_display and total_balance on Accounts Overview before... |
| 3 | navigate | navigate | - | Navigate to Open New Account |
| 4 | action | execute_test | 4.ONA-001 | Execute the action: Open a new Checking account with valid initial deposit |
| 5 | post_verify | execute_test | 4.ONA-002 | Verify the Open New Account UI shows the success confirmation and redirects to the accounts overview |
| 6 | navigate | navigate | - | Navigate to Accounts Overview |
| 7 | post_verify | execute_test_partial | 3.ACCOVE-002 | Verify the new Checking account appears in the Accounts Overview listing with correct type and an... |
| 8 | navigate | navigate | - | Navigate to Accounts Overview |
| 9 | post_verify | execute_test | 3.ACCOVE-003 | Confirm the funding source balance_display decreased by the initial deposit amount and the total_... |

---

### 4.ONA-002: Open a new Savings account with valid initial deposit

| Field | Value |
|-------|-------|
| Module | Open New Account |
| Workflow | Open Account |
| Test Type | positive |
| Priority | High |
| Coverage | partial |
| Modifies State | account_opening, funding_transfer, account_status |

#### Source Test Details

**Preconditions:** User is logged in and Open New Account page is open.

**Steps:**
1. Select Account type = Savings and fill all required fields (Initial Deposit Amount: valid amount above savings minimum, Funding Source Account: account with sufficient balance)
2. Click "Open Account"

**Expected Result:** "Account opened successfully!" is displayed and user is redirected to accounts overview; the new savings account appears in the accounts listing.

#### Verification Mapping

| # | Ideal Verification | Status | Strategy | Matched Test | Confidence |
|---|--------------------|--------|----------|--------------|------------|
| 1 | Verify the Open New Account UI shows the success confirmation and redirects to the accounts overview | found | After Only | 4.ONA-013 - Open Savings account with deposit equal to minimum | 95% |
| 2 | Verify the new Savings account appears in the Accounts Overview listing with correct type and an Open status | partial | After Only | 4.ONA-013 - Open Savings account with deposit equal to minimum | 60% |
| 3 | Verify the funding source account balance decreased by the initial deposit amount | found | Before/After | 3.ACCOVE-003 - Footer displays the total balance across all accounts | 92% |

#### Coverage Gaps

- While 4.ONA-013 verifies that a new savings account appears in the accounts listing after opening, it does not explicitly verify the masked account number or that the account_status is 'Open'. The Accounts Overview candidates cover masking (3.ACCOVE-006) and column presence/status (3.ACCOVE-002) but none combine presence, masking, and explicit 'Open' status checks in a single after-only test.

#### Execution Plan

| Step | Phase | Action | Test ID | Purpose |
|------|-------|--------|---------|---------|
| 1 | navigate | navigate | - | Navigate to Accounts Overview |
| 2 | pre_verify | execute_test | 3.ACCOVE-003 | Record the funding source account's balance_display and total_balance on Accounts Overview before... |
| 3 | navigate | navigate | - | Navigate to Open New Account |
| 4 | action | execute_test | 4.ONA-002 | Execute the action: Open a new Savings account with valid initial deposit |
| 5 | post_verify | execute_test | 4.ONA-013 | Verify the Open New Account UI shows the success confirmation and redirects to the accounts overview |
| 6 | post_verify | execute_test_partial | 4.ONA-013 | Verify the new Savings account appears in the Accounts Overview listing with correct type and an ... |
| 7 | navigate | navigate | - | Navigate to Accounts Overview |
| 8 | post_verify | execute_test | 3.ACCOVE-003 | Confirm the funding source balance_display decreased by the initial deposit amount and the total_... |

---

### 5.TRAFUN-001: Successful internal transfer between own accounts

| Field | Value |
|-------|-------|
| Module | Transfer Funds |
| Workflow | Transfer funds |
| Test Type | positive |
| Priority | High |
| Coverage | partial |
| Modifies State | funds_transfer, account_balance |

#### Source Test Details

**Preconditions:** User is logged in, Transfer Funds page is open, and user has at least two own accounts (Checking or Savings) with sufficient balance

**Steps:**
1. Select the radio button for internal transfer (My ParaBank Account)
2. Fill all required fields (select Source Account from the Source Account dropdown, select Destination internal account from the destination options, enter a valid Transfer Amount within available balance)
3. Click the "Transfer" or "Submit" button

**Expected Result:** Confirmation message "Transfer completed successfully." is displayed and a transaction ID is shown for the transfer.

#### Verification Mapping

| # | Ideal Verification | Status | Strategy | Matched Test | Confidence |
|---|--------------------|--------|----------|--------------|------------|
| 1 | Verify the source account balance decreased by the transfer amount | found | Before/After | 3.ACCOVE-003 - Footer displays the total balance across all accounts | 90% |
| 2 | Verify the destination internal account balance increased by the transfer amount | found | Before/After | 3.ACCOVE-003 - Footer displays the total balance across all accounts | 90% |
| 3 | Verify the transfer confirmation and transaction ID appear in Transfer Funds records | partial | After Only | 5.TRAFUN-002 - Successful external transfer to matching account number | 75% |

#### Coverage Gaps

- This test operates on the correct module and already verifies the confirmation message and that a transaction ID is shown (satisfies the primary after-only check). However, it does not explicitly include steps to verify the transfer appears in recent transfer records/history, which is required by the verification action.

#### Execution Plan

| Step | Phase | Action | Test ID | Purpose |
|------|-------|--------|---------|---------|
| 1 | navigate | navigate | - | Navigate to Accounts Overview |
| 2 | pre_verify | execute_test | 3.ACCOVE-003 | Record the source account's balance_display on Accounts Overview before the transfer |
| 3 | navigate | navigate | - | Navigate to Accounts Overview |
| 4 | pre_verify | execute_test | 3.ACCOVE-003 | Record the destination account's balance_display on Accounts Overview before the transfer |
| 5 | navigate | navigate | - | Navigate to Transfer Funds |
| 6 | action | execute_test | 5.TRAFUN-001 | Execute the action: Successful internal transfer between own accounts |
| 7 | navigate | navigate | - | Navigate to Accounts Overview |
| 8 | post_verify | execute_test | 3.ACCOVE-003 | Confirm the source account's balance_display decreased by the exact transfer amount |
| 9 | navigate | navigate | - | Navigate to Accounts Overview |
| 10 | post_verify | execute_test | 3.ACCOVE-003 | Confirm the destination account's balance_display increased by the exact transfer amount |
| 11 | post_verify | execute_test_partial | 5.TRAFUN-002 | Verify the transfer confirmation and transaction ID appear in Transfer Funds records |

---

### 5.TRAFUN-002: Successful external transfer to matching account number

| Field | Value |
|-------|-------|
| Module | Transfer Funds |
| Workflow | Transfer funds |
| Test Type | positive |
| Priority | High |
| Coverage | partial |
| Modifies State | funds_transfer, account_balance, external_transfer_request |

#### Source Test Details

**Preconditions:** User is logged in, Transfer Funds page is open, and user has a Checking or Savings account with sufficient balance

**Steps:**
1. Select the radio button for external transfer (External Account)
2. Fill all required fields (select Source Account from the Source Account dropdown, enter Destination Account Number, enter Confirm Account Number matching the Destination Account Number, enter a valid Transfer Amount within available balance)
3. Click the "Transfer" or "Submit" button

**Expected Result:** Confirmation message "Transfer completed successfully." is displayed and a transaction ID is shown for the transfer.

#### Verification Mapping

| # | Ideal Verification | Status | Strategy | Matched Test | Confidence |
|---|--------------------|--------|----------|--------------|------------|
| 1 | Verify the source account balance decreased by the external transfer amount | found | Before/After | 3.ACCOVE-003 - Footer displays the total balance across all accounts | 90% |
| 2 | Verify an external transfer request/record was created with a transaction ID and matching destination account number | partial | After Only | 5.TRAFUN-001 - Successful internal transfer between own accounts | 50% |
| 3 | Verify the outgoing external transfer appears in the Account Statements transaction list for the source account | found | After Only | 11.ACCSTA-002 - Generate statement using custom date range | 90% |

#### Coverage Gaps

- None of the candidate tests explicitly perform and confirm an external transfer and then check the external_transfer_request record. 5.TRAFUN-001 already verifies a transaction ID on confirmation (useful for the 'transaction ID displayed' requirement) but targets an internal transfer rather than creating an external_transfer_request with the external destination account number. The other tests either cover validation failure (5.TRAFUN-006) or only UI input switching (5.TRAFUN-004), so they cannot confirm the required post-action record and status.

#### Execution Plan

| Step | Phase | Action | Test ID | Purpose |
|------|-------|--------|---------|---------|
| 1 | navigate | navigate | - | Navigate to Accounts Overview |
| 2 | pre_verify | execute_test | 3.ACCOVE-003 | Record the source account's balance_display on Accounts Overview before the external transfer |
| 3 | navigate | navigate | - | Navigate to Transfer Funds |
| 4 | action | execute_test | 5.TRAFUN-002 | Execute the action: Successful external transfer to matching account number |
| 5 | navigate | navigate | - | Navigate to Accounts Overview |
| 6 | post_verify | execute_test | 3.ACCOVE-003 | Confirm the source account's balance_display decreased by the exact transfer amount |
| 7 | post_verify | execute_test_partial | 5.TRAFUN-001 | Verify an external transfer request/record was created with a transaction ID and matching destina... |
| 8 | navigate | navigate | - | Navigate to Account Statements |
| 9 | post_verify | execute_test | 11.ACCSTA-002 | Verify the outgoing external transfer appears in the Account Statements transaction list for the ... |

---

### 6.PAYMEN-001: Submit valid payment and verify reference code and balance update

| Field | Value |
|-------|-------|
| Module | Payments |
| Workflow | Submit payment |
| Test Type | positive |
| Priority | High |
| Coverage | partial |
| Modifies State | bill_payment, account_balance |

#### Source Test Details

**Preconditions:** User is logged in and the Submit Payment form is open

**Steps:**
1. Fill all required fields (Payee Name, Street Address, City, State, ZIP Code, Phone Number, Payee Account Number, Confirm Account Number) with matching valid values and a valid payee contact
2. Fill Payment Amount with an amount less than the selected source account's available balance and select a Source Account from the dropdown
3. Click "Pay"

**Expected Result:** Payment submitted successfully and a reference code is displayed; the source account balance is reduced accordingly and updated on the page.

#### Verification Mapping

| # | Ideal Verification | Status | Strategy | Matched Test | Confidence |
|---|--------------------|--------|----------|--------------|------------|
| 1 | Verify the Payments UI shows a payment confirmation and displays a payment reference code | partial | After Only | 6.PAYMEN-004 - Submit payment when amount equals available funds (boundary) | 65% |
| 2 | Verify the source account balance is reduced by the payment amount | found | Before/After | 3.ACCOVE-003 - Footer displays the total balance across all accounts | 86% |
| 3 | Verify the payment transaction appears in Account Statements with payee details and reference code | partial | After Only | 11.ACCSTA-001 - Generate statement using month-and-year period | 75% |

#### Coverage Gaps

- The case runs on the correct Payments module and executes a successful payment, but its expected checks focus on account balance update rather than verifying the confirmation UI or the payment_reference code. As written it cannot, by itself (after_only), confirm the required visible payment_reference and success message.
- This test operates on the correct module (Account Statements) and displays the retrieved transactions (so it can surface the transaction_list), but the documented expected result does not explicitly assert or verify the payee details and payment_reference. For an after_only verification it must confirm the specific transaction and fields; the current test must be extended to perform that assertion.

#### Execution Plan

| Step | Phase | Action | Test ID | Purpose |
|------|-------|--------|---------|---------|
| 1 | navigate | navigate | - | Navigate to Accounts Overview |
| 2 | pre_verify | execute_test | 3.ACCOVE-003 | Record the source account's balance_display on Accounts Overview before clicking 'Pay' |
| 3 | navigate | navigate | - | Navigate to Payments |
| 4 | action | execute_test | 6.PAYMEN-001 | Execute the action: Submit valid payment and verify reference code and balance update |
| 5 | post_verify | execute_test_partial | 6.PAYMEN-004 | Verify the Payments UI shows a payment confirmation and displays a payment reference code |
| 6 | navigate | navigate | - | Navigate to Accounts Overview |
| 7 | post_verify | execute_test | 3.ACCOVE-003 | Confirm the source account's balance_display decreased by the exact payment amount |
| 8 | navigate | navigate | - | Navigate to Account Statements |
| 9 | post_verify | execute_test_partial | 11.ACCSTA-001 | Verify the payment transaction appears in Account Statements with payee details and reference code |

---

### 7.REQLOA-001: Request a Personal loan with valid inputs

| Field | Value |
|-------|-------|
| Module | Request Loan |
| Workflow | Request Loan |
| Test Type | positive |
| Priority | High |
| Coverage | partial |
| Modifies State | loan_creation, collateral_hold, loan_status |

#### Source Test Details

**Preconditions:** User is signed in and Request Loan page is open.

**Steps:**
1. Select Loan Type = Personal and fill all required fields (Loan Amount within personal range, Down Payment at or above minimum percentage but less than Loan Amount, select Collateral Account with sufficient funds, choose Interest rate)
2. Click "Submit Loan Request"

**Expected Result:** "Loan approved and created successfully!" message is displayed and the new loan account details are shown.

#### Verification Mapping

| # | Ideal Verification | Status | Strategy | Matched Test | Confidence |
|---|--------------------|--------|----------|--------------|------------|
| 1 | Verify the loan application result shows approval and the new loan details in the Request Loan module | partial | After Only | 7.REQLOA-002 - Request an Auto loan with valid inputs | 70% |
| 2 | Verify the newly created loan account appears in Accounts Overview as a loan-type account with appropriate open statu... | partial | After Only | 3.ACCOVE-002 - Accounts table displays expected columns in each row | 60% |
| 3 | Verify a collateral hold was placed against the selected collateral account by checking the available balance change | partial | Before/After | 7.REQLOA-010 - Verify no actual balance debits occur after loan creation | 60% |

#### Coverage Gaps

- The candidate operates on the correct module and verifies an approval message and loan details, but it is written for an Auto loan (not a Personal loan) and does not explicitly mention checking the loan_application_status field or named loan_terms fields. Therefore it cannot be used as-is for the Personal-loan after_only verification without small modifications.
- Matches the Accounts Overview module and inspects the account table columns (including Account Type and Account Status) but does not currently check for loan-specific details (loan amount/terms) or assert the account_type equals 'Loan/Personal'. As an after_only verification it must confirm the new loan entry and its loan details by itself, which the candidate does not currently do.
- Operates on the Request Loan module (not Accounts Overview). While it notes a displayed collateral account balance, it does not access/display the Accounts Overview available balance or any collateral_hold indicators as required by the verification scenario.

#### Execution Plan

| Step | Phase | Action | Test ID | Purpose |
|------|-------|--------|---------|---------|
| 1 | pre_verify | execute_test_partial | 7.REQLOA-010 | Record the collateral account's balance_display and any available/hold indicators on Accounts Ove... |
| 2 | action | execute_test | 7.REQLOA-001 | Execute the action: Request a Personal loan with valid inputs |
| 3 | post_verify | execute_test_partial | 7.REQLOA-002 | Verify the loan application result shows approval and the new loan details in the Request Loan mo... |
| 4 | navigate | navigate | - | Navigate to Accounts Overview |
| 5 | post_verify | execute_test_partial | 3.ACCOVE-002 | Verify the newly created loan account appears in Accounts Overview as a loan-type account with ap... |
| 6 | post_verify | execute_test_partial | 7.REQLOA-010 | Confirm the collateral account shows a deduction of the expected hold amount or a visible collate... |

---

### 7.REQLOA-002: Request an Auto loan with valid inputs

| Field | Value |
|-------|-------|
| Module | Request Loan |
| Workflow | Request Loan |
| Test Type | positive |
| Priority | High |
| Coverage | partial |
| Modifies State | loan_creation, collateral_hold, loan_status |

#### Source Test Details

**Preconditions:** User is signed in and Request Loan page is open.

**Steps:**
1. Select Loan Type = Auto and fill all required fields (Loan Amount within auto range, Down Payment at or above minimum percentage but less than Loan Amount, select Collateral Account with sufficient funds, choose Interest rate)
2. Click "Submit Loan Request"

**Expected Result:** "Loan approved and created successfully!" message is displayed and the new loan account details are shown.

#### Verification Mapping

| # | Ideal Verification | Status | Strategy | Matched Test | Confidence |
|---|--------------------|--------|----------|--------------|------------|
| 1 | Verify the Auto loan application shows approval and the new loan details in the Request Loan module | partial | After Only | 7.REQLOA-001 - Request a Personal loan with valid inputs | 65% |
| 2 | Verify the newly created auto loan account appears in Accounts Overview as a loan-type account with appropriate details | partial | After Only | 4.ONA-002 - Open a new Savings account with valid initial deposit | 60% |
| 3 | Verify a collateral hold was applied to the selected collateral account by checking balance/available funds before an... | found | Before/After | 7.REQLOA-010 - Verify no actual balance debits occur after loan creation | 75% |

#### Coverage Gaps

- The test is on the correct module (Request Loan) and already checks for an approval message and display of new loan account details, but it targets a Personal loan rather than an Auto loan. It therefore does not exactly match the required loan type and must be adapted to verify an Auto loan's status and terms.
- The candidate verifies that a newly opened account appears in Accounts Overview, so it exercises the correct page and listing behavior. However, it creates a Savings account (not an auto loan) and only asserts presence in the listing; it does not verify loan-type labeling or loan-specific details. Because the execution strategy is after_only, the test must itself confirm the auto loan entry and its loan details—this test would need modification to do that.

#### Execution Plan

| Step | Phase | Action | Test ID | Purpose |
|------|-------|--------|---------|---------|
| 1 | pre_verify | execute_test | 7.REQLOA-010 | Record the collateral account's balance_display and any existing hold indicators before submittin... |
| 2 | action | execute_test | 7.REQLOA-002 | Execute the action: Request an Auto loan with valid inputs |
| 3 | post_verify | execute_test_partial | 7.REQLOA-001 | Verify the Auto loan application shows approval and the new loan details in the Request Loan module |
| 4 | navigate | navigate | - | Navigate to Open New Account |
| 5 | post_verify | execute_test_partial | 4.ONA-002 | Verify the newly created auto loan account appears in Accounts Overview as a loan-type account wi... |
| 6 | post_verify | execute_test | 7.REQLOA-010 | Confirm the collateral account shows the expected decrease in available funds or a new collateral... |

---

### 7.REQLOA-003: Request a Home loan with valid inputs

| Field | Value |
|-------|-------|
| Module | Request Loan |
| Workflow | Request Loan |
| Test Type | positive |
| Priority | High |
| Coverage | partial |
| Modifies State | loan_creation, collateral_hold, loan_status |

#### Source Test Details

**Preconditions:** User is signed in and Request Loan page is open.

**Steps:**
1. Select Loan Type = Home and fill all required fields (Loan Amount within home range, Down Payment at or above minimum percentage but less than Loan Amount, select Collateral Account with sufficient funds, choose Interest rate)
2. Click "Submit Loan Request"

**Expected Result:** "Loan approved and created successfully!" message is displayed and the new loan account details are shown.

#### Verification Mapping

| # | Ideal Verification | Status | Strategy | Matched Test | Confidence |
|---|--------------------|--------|----------|--------------|------------|
| 1 | Verify the Home loan application shows approval and the new loan details in the Request Loan module | partial | After Only | 7.REQLOA-002 - Request an Auto loan with valid inputs | 70% |
| 2 | Verify the newly created home loan account appears in Accounts Overview as a loan-type account with appropriate details | partial | After Only | 4.ONA-002 - Open a new Savings account with valid initial deposit | 50% |
| 3 | Verify a collateral hold was applied to the selected collateral account by checking balance/available funds before an... | partial | Before/After | 7.REQLOA-010 - Verify no actual balance debits occur after loan creation | 65% |

#### Coverage Gaps

- The candidate operates in the correct module and already checks for an approval message and display of loan account details (which satisfies the after_only requirement). However, it targets an Auto loan rather than the required Home loan, so it doesn't exactly match the requested loan type. If adjusted to select Home, it would fully satisfy the verification.
- The candidate accesses Accounts Overview and checks that a newly opened account appears in the listing (good), but it opens a Savings account rather than a Home Loan and does not assert loan-type labeling or loan-specific details. Because execution_strategy is after_only, the verification must confirm the home loan entry and its loan details by itself — this test as written cannot do that.
- Closest candidate shows the collateral account balance but operates on the Request Loan page (not the required Accounts Overview) and does not explicitly capture available funds or a collateral_hold indicator. Because the before_after execution only needs to observe relevant data, showing the balance is helpful, but missing the available-funds field and hold indicator means it is not a full match.

#### Execution Plan

| Step | Phase | Action | Test ID | Purpose |
|------|-------|--------|---------|---------|
| 1 | pre_verify | execute_test_partial | 7.REQLOA-010 | Record the collateral account's balance_display and any existing hold indicators before submittin... |
| 2 | action | execute_test | 7.REQLOA-003 | Execute the action: Request a Home loan with valid inputs |
| 3 | post_verify | execute_test_partial | 7.REQLOA-002 | Verify the Home loan application shows approval and the new loan details in the Request Loan module |
| 4 | navigate | navigate | - | Navigate to Open New Account |
| 5 | post_verify | execute_test_partial | 4.ONA-002 | Verify the newly created home loan account appears in Accounts Overview as a loan-type account wi... |
| 6 | post_verify | execute_test_partial | 7.REQLOA-010 | Confirm the collateral account shows the expected decrease in available funds or a new collateral... |

---

### 7.REQLOA-010: Verify no actual balance debits occur after loan creation

| Field | Value |
|-------|-------|
| Module | Request Loan |
| Workflow | Request Loan |
| Test Type | positive |
| Priority | Medium |
| Coverage | partial |
| Modifies State | loan_creation, collateral_hold |

#### Source Test Details

**Preconditions:** User is signed in, Request Loan page is open, and a valid loan request is ready to submit.

**Steps:**
1. Fill all required fields with valid values and note the displayed Collateral Account balance
2. Click "Submit Loan Request"

**Expected Result:** Loan is created and the collateral account balance remains unchanged (no actual balance debits occur).

#### Verification Mapping

| # | Ideal Verification | Status | Strategy | Matched Test | Confidence |
|---|--------------------|--------|----------|--------------|------------|
| 1 | Verify the collateral account balance remains unchanged after loan creation (no actual debit) | partial | Before/After | 4.ONA-001 - Open a new Checking account with valid initial deposit | 50% |
| 2 | Verify the loan was created and the application status shows approved in Request Loan | found | After Only | 7.REQLOA-001 - Request a Personal loan with valid inputs | 75% |

#### Coverage Gaps

- The test is primarily an Open New Account scenario but includes a redirect to Accounts Overview; it does not explicitly access or record the specific account balance_display and available funds fields required for this verification.

#### Execution Plan

| Step | Phase | Action | Test ID | Purpose |
|------|-------|--------|---------|---------|
| 1 | navigate | navigate | - | Navigate to Open New Account |
| 2 | pre_verify | execute_test_partial | 4.ONA-001 | Record the collateral account's balance_display and available funds on Accounts Overview before s... |
| 3 | navigate | navigate | - | Navigate to Request Loan |
| 4 | action | execute_test | 7.REQLOA-010 | Execute the action: Verify no actual balance debits occur after loan creation |
| 5 | navigate | navigate | - | Navigate to Open New Account |
| 6 | post_verify | execute_test_partial | 4.ONA-001 | Confirm the collateral account's balance_display and available funds are unchanged after the loan... |
| 7 | post_verify | execute_test | 7.REQLOA-001 | Verify the loan was created and the application status shows approved in Request Loan |

---

### 8.UCI-001: Update profile with all valid contact fields

| Field | Value |
|-------|-------|
| Module | Update Contact Info |
| Workflow | Update Profile |
| Test Type | positive |
| Priority | High |
| Coverage | partial |
| Modifies State | user_profile_update, user_profile |

#### Source Test Details

**Preconditions:** User is logged in and Update Contact Info page is open.

**Steps:**
1. Fill all required fields (First Name, Last Name, Street Address, City, State, ZIP Code, Phone Number) with valid values
2. Click "Update Profile"

**Expected Result:** Profile updated successfully and the displayed contact fields are refreshed to show the new values.

#### Verification Mapping

| # | Ideal Verification | Status | Strategy | Matched Test | Confidence |
|---|--------------------|--------|----------|--------------|------------|
| 1 | Verify the user's contact profile fields are updated and persisted | partial | Before/After | 8.UCI-005 - Submit with multiple fields failing format validation | 64% |
| 2 | Verify the profile update confirmation message is displayed after submission | partial | After Only | 8.UCI-002 - Submit with all required fields empty | 60% |

#### Coverage Gaps

- Although the test operates on the correct module and does interact with the contact fields, as written it populates invalid formats and submits the form to verify validation errors. That submission would modify/interfere with the profile state and does not explicitly record the pre-filled field values needed for the before_after verification. Therefore it cannot be used as-is but could be adapted to serve as the observation step.
- All candidate tests operate on the correct module but they are negative/validation scenarios (empty or invalid fields) that expect validation errors, not a success confirmation message. Because the execution_strategy is after_only, the verification test must itself confirm the success message — none of the provided tests currently do that.

#### Execution Plan

| Step | Phase | Action | Test ID | Purpose |
|------|-------|--------|---------|---------|
| 1 | pre_verify | execute_test_partial | 8.UCI-005 | Record all visible contact_fields on the pre-filled profile form before making changes |
| 2 | action | execute_test | 8.UCI-001 | Execute the action: Update profile with all valid contact fields |
| 3 | post_verify | execute_test_partial | 8.UCI-005 | Re-open the profile form and confirm every contact field matches the new submitted values |
| 4 | post_verify | execute_test_partial | 8.UCI-002 | Verify the profile update confirmation message is displayed after submission |

---

### 9.MANCAR-001: Request a new Debit card with valid linked account and complete shipping address

| Field | Value |
|-------|-------|
| Module | Manage Cards |
| Workflow | Request Card |
| Test Type | positive |
| Priority | High |
| Coverage | partial |
| Modifies State | card_request_creation |

#### Source Test Details

**Preconditions:** User is authenticated and the Request Card form is visible

**Steps:**
1. Select Card Type as Debit
2. Select a linked account in good standing
3. Fill the complete Shipping Address
4. Click "Request Card"

**Expected Result:** A card-request ticket is opened and the UI shows "Card request submitted successfully." with a tracking ID

#### Verification Mapping

| # | Ideal Verification | Status | Strategy | Matched Test | Confidence |
|---|--------------------|--------|----------|--------------|------------|
| 1 | Verify a new card request record was created and the UI displays the success message with tracking ID | partial | After Only | 9.MANCAR-002 - Request a new Credit card with valid linked account and complete shippin... | 70% |
| 2 | Verify the card request appears as a support/ticket entry so backend/support can track it | not_found | After Only | - | - |

#### Coverage Gaps

- The candidate runs in the correct module and checks the success UI notification with tracking ID, but it requests a Credit card (requirement expects Debit) and does not verify the Requests/Request History entry or the saved shipping address/card_request_status. As written it cannot alone confirm the new record's type and address.
- None of the provided test cases both operate on the Support Center ticket listing/search page AND confirm a ticket exists referencing the card request. 13.SUPCEN-001 runs in Support Center and can show a created ticket ID for a sent message but does not search My Tickets or confirm a card-request ticket. 9.MANCAR-002 confirms a card request was submitted and shows a tracking ID in the Manage Cards UI but does not open the Support Center to verify the ticket record. 9.MANCAR-010 is irrelevant (negative case). Because the execution strategy is after_only, the verification must, by itself, confirm the ticket record in Support Center — no candidate performs that exact action.

#### Execution Plan

| Step | Phase | Action | Test ID | Purpose |
|------|-------|--------|---------|---------|
| 1 | action | execute_test | 9.MANCAR-001 | Execute the action: Request a new Debit card with valid linked account and complete shipping address |
| 2 | post_verify | execute_test_partial | 9.MANCAR-002 | Verify a new card request record was created and the UI displays the success message with trackin... |

**Manual Verification Required:**
- Purpose: Verify the card request appears as a support/ticket entry so backend/support can track it
- Suggested Step: After submitting the card request, open Support Center -> My Tickets (or use Ticket Search). Enter the card request tracking ID (or filter by recent timestamp) and locate the corresponding ticket. Verify the ticket exists, that the ticket ID/tracking ID is present, and record the ticket status and any relevant details.
- Reason: None of the provided test cases both operate on the Support Center ticket listing/search page AND confirm a ticket exists referencing the card request. 13.SUPCEN-001 runs in Support Center and can show a created ticket ID for a sent message but does not search My Tickets or confirm a card-request ticket. 9.MANCAR-002 confirms a card request was submitted and shows a tracking ID in the Manage Cards UI but does not open the Support Center to verify the ticket record. 9.MANCAR-010 is irrelevant (negative case). Because the execution strategy is after_only, the verification must, by itself, confirm the ticket record in Support Center — no candidate performs that exact action.

---

### 9.MANCAR-002: Request a new Credit card with valid linked account and complete shipping address

| Field | Value |
|-------|-------|
| Module | Manage Cards |
| Workflow | Request Card |
| Test Type | positive |
| Priority | High |
| Coverage | partial |
| Modifies State | card_request_creation |

#### Source Test Details

**Preconditions:** User is authenticated and the Request Card form is visible

**Steps:**
1. Select Card Type as Credit
2. Select a linked account in good standing
3. Fill the complete Shipping Address
4. Click "Request Card"

**Expected Result:** A card-request ticket is opened and the UI shows "Card request submitted successfully." with a tracking ID

#### Verification Mapping

| # | Ideal Verification | Status | Strategy | Matched Test | Confidence |
|---|--------------------|--------|----------|--------------|------------|
| 1 | Verify a new card request record was created and the UI displays the success message with tracking ID | partial | After Only | 9.MANCAR-001 - Request a new Debit card with valid linked account and complete shipping... | 70% |
| 2 | Verify the card request appears as a support/ticket entry for tracking by support staff | partial | After Only | 13.SUPCEN-001 - Send message successfully with required fields (no attachment) | 65% |

#### Coverage Gaps

- The candidate operates on the correct module and verifies the UI success message with a tracking ID, but it requests a Debit card (requirement expects Credit) and does not explicitly check the Requests/Request History entry for the new record or verify the stored shipping address/type. Therefore it cannot by itself confirm the required post-action state.
- Correct module (Support Center) and it does display a ticket ID on successful submission, but it does not perform the required lookup of an existing card-request ticket created earlier in the Manage Cards flow. Because execution_strategy is after_only, the verification test must itself confirm the card-request ticket exists in Support Center; 13.SUPCEN-001 as written confirms ticket creation for a message but does not verify the specific card-request ticket entry.

#### Execution Plan

| Step | Phase | Action | Test ID | Purpose |
|------|-------|--------|---------|---------|
| 1 | action | execute_test | 9.MANCAR-002 | Execute the action: Request a new Credit card with valid linked account and complete shipping add... |
| 2 | post_verify | execute_test_partial | 9.MANCAR-001 | Verify a new card request record was created and the UI displays the success message with trackin... |
| 3 | navigate | navigate | - | Navigate to Support Center |
| 4 | post_verify | execute_test_partial | 13.SUPCEN-001 | Verify the card request appears as a support/ticket entry for tracking by support staff |

---

### 9.MANCAR-003: Update spending limit with a valid amount

| Field | Value |
|-------|-------|
| Module | Manage Cards |
| Workflow | Update Controls |
| Test Type | positive |
| Priority | High |
| Coverage | full |
| Modifies State | card_control_update, spending_limit |

#### Source Test Details

**Preconditions:** An existing card is selected and the Update Controls form is open.

**Steps:**
1. Fill all required fields (Select Existing Card, New Spending Limit with a valid numeric amount, Card Status as desired) and leave Travel Notice empty
2. Click "Update Controls"

**Expected Result:** "Card controls updated successfully." is displayed and the spending limit shown in the controls reflects the new amount.

#### Verification Mapping

| # | Ideal Verification | Status | Strategy | Matched Test | Confidence |
|---|--------------------|--------|----------|--------------|------------|
| 1 | Verify the spending limit on the selected card was updated to the new numeric amount | found | Before/After | 9.MANCAR-012 - Reject non-numeric spending limit value | 78% |
| 2 | Verify the UI shows a confirmation that controls were updated successfully | found | After Only | 9.MANCAR-007 - Update controls without adding a travel notice (travel notice optional) | 92% |

#### Execution Plan

| Step | Phase | Action | Test ID | Purpose |
|------|-------|--------|---------|---------|
| 1 | pre_verify | execute_test | 9.MANCAR-012 | Record the card's current spending limit value for the selected card before submitting the update |
| 2 | action | execute_test | 9.MANCAR-003 | Execute the action: Update spending limit with a valid amount |
| 3 | post_verify | execute_test | 9.MANCAR-012 | Confirm the spending limit value now equals the new amount and differs from the recorded before v... |
| 4 | post_verify | execute_test | 9.MANCAR-007 | Verify the UI shows a confirmation that controls were updated successfully |

---

### 9.MANCAR-004: Freeze an active card by updating Card Status

| Field | Value |
|-------|-------|
| Module | Manage Cards |
| Workflow | Update Controls |
| Test Type | positive |
| Priority | High |
| Coverage | partial |
| Modifies State | card_control_update, card_status |

#### Source Test Details

**Preconditions:** An existing card currently in Active status is selected and the Update Controls form is open.

**Steps:**
1. Select Frozen in Card Status and fill all other required fields (Select Existing Card, any required numeric fields)
2. Click "Update Controls"

**Expected Result:** "Card controls updated successfully." is displayed and the card status updates to Frozen.

#### Verification Mapping

| # | Ideal Verification | Status | Strategy | Matched Test | Confidence |
|---|--------------------|--------|----------|--------------|------------|
| 1 | Verify the selected card's status changed to Frozen and is displayed as such in the card detail | partial | After Only | 9.MANCAR-007 - Update controls without adding a travel notice (travel notice optional) | 60% |
| 2 | Verify a confirmation is shown indicating controls were updated successfully | found | After Only | 9.MANCAR-007 - Update controls without adding a travel notice (travel notice optional) | 90% |

#### Coverage Gaps

- All three candidates operate in the Manage Cards module and allow selecting a card and setting Card Status, but none include an explicit assertion that the card detail/status badge displays the new status. Because the execution_strategy is after_only, the test must confirm the outcome by itself; the candidate only confirms a success message, not the displayed card_status.

#### Execution Plan

| Step | Phase | Action | Test ID | Purpose |
|------|-------|--------|---------|---------|
| 1 | action | execute_test | 9.MANCAR-004 | Execute the action: Freeze an active card by updating Card Status |
| 2 | post_verify | execute_test_partial | 9.MANCAR-007 | Verify the selected card's status changed to Frozen and is displayed as such in the card detail |
| 3 | post_verify | execute_test | 9.MANCAR-007 | Verify a confirmation is shown indicating controls were updated successfully |

---

### 9.MANCAR-006: Add a travel notice with valid dates and destination

| Field | Value |
|-------|-------|
| Module | Manage Cards |
| Workflow | Update Controls |
| Test Type | positive |
| Priority | Medium |
| Coverage | partial |
| Modifies State | card_control_update, card_controls |

#### Source Test Details

**Preconditions:** An existing card is selected and the Update Controls form is open.

**Steps:**
1. Fill all required fields (Select Existing Card, Card Status as desired) and fill Travel Notice with a valid start date, end date, and destination
2. Click "Update Controls"

**Expected Result:** "Card controls updated successfully." is displayed and the travel notice (dates and destination) is saved and shown in the controls.

#### Verification Mapping

| # | Ideal Verification | Status | Strategy | Matched Test | Confidence |
|---|--------------------|--------|----------|--------------|------------|
| 1 | Verify the travel notice (start date, end date, destination) is saved and visible in the card controls | partial | After Only | 9.MANCAR-013 - Reject travel notice with end date before start date | 60% |
| 2 | Verify the UI shows a confirmation that controls were updated successfully after adding the travel notice | partial | After Only | 9.MANCAR-007 - Update controls without adding a travel notice (travel notice optional) | 72% |

#### Coverage Gaps

- None of the provided candidates confirm that a travel notice was saved and visible in the card controls after an update. 9.MANCAR-013 interacts with travel notice fields but asserts a validation failure (travel notice not saved). The other candidates (9.MANCAR-007, 9.MANCAR-003) leave travel notice empty and therefore do not verify a stored travel notice either.
- Closest match because it verifies the success notification on the same page, but it does not add or check a travel notice. The requirement needs confirmation message plus presence of the travel notice, which this test does not cover.

#### Execution Plan

| Step | Phase | Action | Test ID | Purpose |
|------|-------|--------|---------|---------|
| 1 | action | execute_test | 9.MANCAR-006 | Execute the action: Add a travel notice with valid dates and destination |
| 2 | post_verify | execute_test_partial | 9.MANCAR-013 | Verify the travel notice (start date, end date, destination) is saved and visible in the card con... |
| 3 | post_verify | execute_test_partial | 9.MANCAR-007 | Verify the UI shows a confirmation that controls were updated successfully after adding the trave... |

---

### 9.MANCAR-007: Update controls without adding a travel notice (travel notice optional)

| Field | Value |
|-------|-------|
| Module | Manage Cards |
| Workflow | Update Controls |
| Test Type | positive |
| Priority | Medium |
| Coverage | partial |
| Modifies State | card_control_update |

#### Source Test Details

**Preconditions:** An existing card is selected and the Update Controls form is open.

**Steps:**
1. Fill all required fields (Select Existing Card, New Spending Limit or leave unchanged, Card Status as desired) and leave all Travel Notice fields empty
2. Click "Update Controls"

**Expected Result:** "Card controls updated successfully." is displayed and the update succeeds without a travel notice.

#### Verification Mapping

| # | Ideal Verification | Status | Strategy | Matched Test | Confidence |
|---|--------------------|--------|----------|--------------|------------|
| 1 | Verify Update Controls succeeds without creating a travel notice (no travel notice added) | found | Before/After | 9.MANCAR-003 - Update spending limit with a valid amount | 75% |
| 2 | Verify the UI displays a success confirmation that card controls were updated | partial | After Only | 9.MANCAR-003 - Update spending limit with a valid amount | 68% |

#### Coverage Gaps

- This test runs on the correct module and uses an empty Travel Notice (matches the scenario) and already checks for the success confirmation, but it does not currently assert that no travel notice entry was added. Because the execution_strategy is after_only, the test must explicitly confirm absence of a travel notice; as-written it only confirms the spending limit update.

#### Execution Plan

| Step | Phase | Action | Test ID | Purpose |
|------|-------|--------|---------|---------|
| 1 | pre_verify | execute_test | 9.MANCAR-003 | Record whether a travel notice exists and its details (or note 'none') for the selected card befo... |
| 2 | action | execute_test | 9.MANCAR-007 | Execute the action: Update controls without adding a travel notice (travel notice optional) |
| 3 | post_verify | execute_test | 9.MANCAR-003 | Confirm that after the update the travel notice existence/details are unchanged (still none or id... |
| 4 | post_verify | execute_test_partial | 9.MANCAR-003 | Verify the UI displays a success confirmation that card controls were updated |

---

## Associated Verification Test Cases

These are matched test cases referenced by post-verification mappings.

| TC ID | Module | Title | Type | Priority | Expected Result |
|-------|--------|-------|------|----------|------------------|
| 1.LOGIN-008 | Login | After changing password the old password no longer works | standard | High | Login with the old password fails (authentication denied); login with the new password succeeds, confirming the old p... |
| 10.INVEST-001 | Investments | Execute a Buy trade successfully and update holdings | positive | High | A same-day trade is executed; confirmation displays "Trade executed successfully." with an order ID and portfolio hol... |
| 10.INVEST-002 | Investments | Execute a Sell trade successfully and update holdings | positive | High | A same-day trade is executed; confirmation displays "Trade executed successfully." with an order ID and portfolio hol... |
| 10.INVEST-003 | Investments | Create recurring investment plan with Weekly frequency | positive | High | Plan created successfully. The schedule is stored and a confirmation message "Plan created successfully." is shown. |
| 10.INVEST-004 | Investments | Create recurring investment plan with Monthly frequency | positive | High | Plan created successfully. The schedule is stored and a confirmation message "Plan created successfully." is shown. |
| 10.INVEST-007 | Investments | Portfolio snapshot displays current holdings and read-only values | positive | Medium | Portfolio snapshot shows current fund holdings, market value, and unrealised gain or loss and is presented as read-only. |
| 11.ACCSTA-001 | Account Statements | Generate statement using month-and-year period | positive | High | Displays 'Statement generated successfully.' and the generated statement shows the retrieved transactions for the sel... |
| 11.ACCSTA-002 | Account Statements | Generate statement using custom date range | positive | High | Displays 'Statement generated successfully.' and the generated statement shows the retrieved transactions for the spe... |
| 11.ACCSTA-008 | Account Statements | Save preference with invalid email format | negative | Medium | Email field is highlighted with guidance and the preference is not saved. |
| 12.SECSET-006 | Security Settings | Change password using a minimally-compliant strong password | edge_case | Low | Password changed successfully and credentials are updated. |
| 13.SUPCEN-001 | Support Center | Send message successfully with required fields (no attachment) | positive | High | A success notification "Message sent successfully." is displayed and a ticket ID is shown |
| 13.SUPCEN-002 | Support Center | Send message successfully with a valid attachment | positive | High | A success notification "Message sent successfully." is displayed and a ticket ID is shown |
| 13.SUPCEN-010 | Support Center | Submit with Preferred Date set to the next business day (boundary) | edge_case | Medium | Request is accepted and a success message "Callback request submitted." is displayed; an email confirmation is sent. |
| 3.ACCOVE-002 | Accounts Overview | Accounts table displays expected columns in each row | positive | High | Every row contains Account Number, Account Type, Current Balance, Account Status (Active badge), and Open Date. |
| 3.ACCOVE-003 | Accounts Overview | Footer displays the total balance across all accounts | positive | High | Footer total balance equals the sum of all Current Balance values shown in the table. |
| 4.ONA-001 | Open New Account | Open a new Checking account with valid initial deposit | positive | High | "Account opened successfully!" is displayed and user is redirected to accounts overview; the new checking account app... |
| 4.ONA-002 | Open New Account | Open a new Savings account with valid initial deposit | positive | High | "Account opened successfully!" is displayed and user is redirected to accounts overview; the new savings account appe... |
| 4.ONA-013 | Open New Account | Open Savings account with deposit equal to minimum | edge_case | Low | "Account opened successfully!" is displayed and user is redirected to accounts overview; the new savings account appe... |
| 5.TRAFUN-001 | Transfer Funds | Successful internal transfer between own accounts | positive | High | Confirmation message "Transfer completed successfully." is displayed and a transaction ID is shown for the transfer. |
| 5.TRAFUN-002 | Transfer Funds | Successful external transfer to matching account number | positive | High | Confirmation message "Transfer completed successfully." is displayed and a transaction ID is shown for the transfer. |
| 6.PAYMEN-004 | Payments | Submit payment when amount equals available funds (boundary) | edge_case | Low | Payment is executed successfully and the source account balance is updated to reflect the zero (or new) available bal... |
| 7.REQLOA-001 | Request Loan | Request a Personal loan with valid inputs | positive | High | "Loan approved and created successfully!" message is displayed and the new loan account details are shown. |
| 7.REQLOA-002 | Request Loan | Request an Auto loan with valid inputs | positive | High | "Loan approved and created successfully!" message is displayed and the new loan account details are shown. |
| 7.REQLOA-010 | Request Loan | Verify no actual balance debits occur after loan creation | positive | Medium | Loan is created and the collateral account balance remains unchanged (no actual balance debits occur). |
| 8.UCI-001 | Update Contact Info | Update profile with all valid contact fields | positive | High | Profile updated successfully and the displayed contact fields are refreshed to show the new values. |
| 8.UCI-002 | Update Contact Info | Submit with all required fields empty | negative | Medium | Validation errors shown for all required fields and invalid fields are highlighted. |
| 8.UCI-005 | Update Contact Info | Submit with multiple fields failing format validation | edge_case | Low | Both invalid fields are highlighted and an inline error banner is displayed summarizing the failures. |
| 9.MANCAR-001 | Manage Cards | Request a new Debit card with valid linked account and complete shipping address | positive | High | A card-request ticket is opened and the UI shows "Card request submitted successfully." with a tracking ID |
| 9.MANCAR-002 | Manage Cards | Request a new Credit card with valid linked account and complete shipping address | positive | High | A card-request ticket is opened and the UI shows "Card request submitted successfully." with a tracking ID |
| 9.MANCAR-003 | Manage Cards | Update spending limit with a valid amount | positive | High | "Card controls updated successfully." is displayed and the spending limit shown in the controls reflects the new amount. |
| 9.MANCAR-007 | Manage Cards | Update controls without adding a travel notice (travel notice optional) | positive | Medium | "Card controls updated successfully." is displayed and the update succeeds without a travel notice. |
| 9.MANCAR-012 | Manage Cards | Reject non-numeric spending limit value | negative | Medium | Inline validation error indicates the spending limit must be numeric and the form remains editable. |
| 9.MANCAR-013 | Manage Cards | Reject travel notice with end date before start date | negative | Medium | Inline validation error indicates the date range is invalid and the form remains editable; travel notice is not saved. |
