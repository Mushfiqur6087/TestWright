# Parabank - Post-Verification Report

**Base URL:** 
**Generated:** 2026-04-18T20:46:44.594062

## Summary

| Metric | Count |
|--------|-------|
| Source Tests Needing Verification | 27 |
| Full Coverage | 1 |
| Partial Coverage | 24 |
| Minimal Coverage | 0 |
| No Coverage | 2 |
| Tests With Verification Gaps | 7 |
| Total Missing Verifications | 8 |
| Associated Verification Tests | 22 |

### Generated Verifications by Type

| Type | Count |
|------|-------|
| Existence | 25 |
| Absence | 1 |
| Field Persistence | 4 |
| Status Transition | 1 |
| Cascading Update | 6 |
| Credential Change | 1 |
| Session Persistence | 4 |
| Financial Delta | 12 |

### Generated Verifications by Strategy

| Strategy | Count |
|----------|-------|
| After Only | 31 |
| Before/After | 18 |
| Cross-User | 5 |

### Top Coverage Gaps

- The candidate operates on the correct module and shows a ticket ID on successful send, so it partially confirms creation. However it does not explicitly access the user's ticket list or view the ticket detail to confirm category and message content, which the after_only strategy requires.
- Although this test targets the correct module (Accounts Overview), it only accesses Current Balance values and the footer total. It does not currently read or display the hold/reserve indicator or held amount required by the verification. Therefore it cannot be used as-is but is the closest candidate and can be adapted.
- Correct module (Accounts Overview) but the test as written does not access or display the hold/reserve indicator or held-amount/available-balance values required by the verification. Because execution_strategy is before_after, a test that simply observes those fields would be sufficient — this one needs to be modified to capture them.
- This test operates on the correct module (Account Statements) and displays the generated transactions for a chosen period, so it can surface the transaction list. However, it does not explicitly check for the presence of a payment transaction, the payment reference code, or payee details. Because the execution strategy is after_only, the test must confirm the expected outcome by itself; as written it only generates the statement and does not assert the specific fields required.
- The candidate is on the correct module and touches the relevant UI elements, but it performs modifications and save attempts (negative validation scenario) rather than simply observing/displaying the current e_statement_preference. Because the execution_strategy is before_after, the verification test must be able to OBSERVE the checkbox state and email without causing state changes—this test as written would alter state and/or trigger validation, so it is not a full match.
- Test 12.SECSET-006 checks the password change action and success message but does not confirm persistence by performing logout and re-login. Tests 12.SECSET-004 and 12.SECSET-002 are negative validation cases and do not verify successful persistence either.
- None of the candidates explicitly exercise the admin-facing Recent Tickets view or include a search for a ticket referencing a card request/tracking ID. 13.SUPCEN-001 is the closest because it uses the Support Center and shows a generated ticket ID, but its steps only cover sending a message and confirming the success message/ID for the creator — it does not describe the admin-side observation (Recent Tickets search and status check). 9.MANCAR-002 creates the card request and returns a tracking ID but is in Manage Cards (creator action), not in the admin Support Center view. 9.MANCAR-010 is negative/blocked flow and irrelevant.
- The test displays the relevant data (portfolio holdings) but as-written it only observes read-only values and does not perform the necessary confirmation/assertion that the holding decreased by the sold quantity. Because execution_strategy is after_only, the verification must confirm the expected numeric change by itself; the candidate lacks that explicit check.
- Correct module (Accounts Overview) and reads account balances, but it does not access/display the specific hold/reserve indicator or held amount required by the before_after verification.
- All three candidates operate in the Manage Cards module and exercise the Update Controls flow, but none explicitly state that they access or display the card's current spending limit in the Controls view. They focus on validation or successful update behavior (entering new values and checking validation/success messages) rather than explicitly reading and reporting the persisted spending limit field. Because the verification requires recording the displayed spending limit before and after, these candidates do not guarantee the required observation step.

---

## Post-Verification Source Tests

### 10.INVEST-001: Execute a Buy trade successfully and update holdings

| Field | Value |
|-------|-------|
| Module | Investments |
| Workflow | Execute Trade |
| Test Type | positive |
| Priority | High |
| Coverage | partial |
| Modifies State | trade_execution, cash_balance, fund_holdings |

#### Source Test Details

**Preconditions:** User is logged in and Execute Trade form is visible; customer has sufficient buying power.

**Steps:**
1. Fill all required fields (Action set to Buy, Fund Symbol selected via autocomplete, Quantity with a valid positive amount, Funding Account selected)
2. Click "Execute Trade"
3. Verify confirmation area displays success message and order details

**Expected Result:** A same-day trade is executed; confirmation displays "Trade executed successfully." with an order ID and portfolio holdings are updated.

#### Verification Mapping

| # | Ideal Verification | Status | Type | Strategy | Matched Test | Confidence |
|---|--------------------|--------|------|----------|--------------|------------|
| 1 | Verify the executed buy trade appears in the user's trade history with the order ID, fund symbol, quantity, and execu... | partial | Existence | After Only | 10.INVEST-002 - Execute a Sell trade successfully and update holdings | 65% |
| 2 | Verify the user's cash balance decreased by the expected cash amount debited for the buy. | partial | Financial Delta | After Only | 10.INVEST-002 - Execute a Sell trade successfully and update holdings | 45% |
| 3 | Verify the fund holdings increased by the purchased quantity (or shares) in the portfolio snapshot. | partial | Financial Delta | After Only | 10.INVEST-007 - Portfolio snapshot displays current holdings and read-only values | 70% |

#### Coverage Gaps

- The candidate runs in the Investments module and captures an order ID on the confirmation screen, but it is for a Sell flow and does not navigate to the Trade History/Orders page or verify Action=Buy, execution timestamp, or status='Executed'. As an after_only verification, the test must confirm the record exists in Trade History with all required fields — the current test only partially covers this.
- The candidate is on the correct module and verifies trade execution, but it is a Sell scenario and does not read or assert the cash_balance or compute the expected debit. As written it cannot, by itself (after-only), confirm that cash_balance decreased by price*quantity+fees.
- The test is on the correct module and displays the relevant portfolio/holding data, but it does not include steps to confirm the holding increased by the executed buy quantity. Because execution_strategy is after_only, the verification must confirm the expected outcome by itself; this candidate lacks the comparison/assertion needed.

#### Execution Plan

| Step | Phase | Action | Test ID | Purpose |
|------|-------|--------|---------|---------|
| 1 | action | execute_test | 10.INVEST-001 | Execute the action: Execute a Buy trade successfully and update holdings |
| 2 | post_verify | execute_test_partial | 10.INVEST-002 | Verify the executed buy trade appears in the user's trade history with the order ID, fund symbol,... |
| 3 | post_verify | execute_test_partial | 10.INVEST-002 | Verify the user's cash balance decreased by the expected cash amount debited for the buy. |
| 4 | post_verify | execute_test_partial | 10.INVEST-007 | Verify the fund holdings increased by the purchased quantity (or shares) in the portfolio snapshot. |

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

| # | Ideal Verification | Status | Type | Strategy | Matched Test | Confidence |
|---|--------------------|--------|------|----------|--------------|------------|
| 1 | Verify the executed sell trade appears in the user's trade history with the order ID, fund symbol, quantity, and exec... | partial | Existence | After Only | 10.INVEST-001 - Execute a Buy trade successfully and update holdings | 65% |
| 2 | Verify the user's cash balance increased by the expected proceeds from the sell. | not_found | Financial Delta | After Only | - | - |
| 3 | Verify the fund holdings decreased by the sold quantity in the portfolio snapshot. | partial | Financial Delta | After Only | 10.INVEST-007 - Portfolio snapshot displays current holdings and read-only values | 75% |

#### Verification Tests Needed

| # | Type | Strategy | Target Module | Observer | Suggested Test Title |
|---|------|----------|---------------|----------|----------------------|
| 1 | Financial Delta | After Only | Investments | - | After the sell completes, in the Investments module: 1) Open the trade confirmation / order detai... |

#### Coverage Gaps

- Test 10.INVEST-001 validates a trade execution confirmation and order details but is focused on a Buy flow and the confirmation area rather than the Trade History / Orders view. Because the execution strategy is after_only, the verification must confirm the new record exists in Trade History; the candidate does not include that navigation/check, so it cannot fully confirm the required outcome as-is.
- All candidates are either buy flow or failure/validation flows and do not access or display the account cash balance or the cash transaction that results from a successful sell. The requirement is after_only and must confirm the cash increase by comparing trade proceeds minus fees to the cash credit/new balance; none of the tests extract or assert that data.
- The test displays the relevant data (portfolio holdings) but as-written it only observes read-only values and does not perform the necessary confirmation/assertion that the holding decreased by the sold quantity. Because execution_strategy is after_only, the verification must confirm the expected numeric change by itself; the candidate lacks that explicit check.

#### Execution Plan

| Step | Phase | Action | Test ID | Purpose |
|------|-------|--------|---------|---------|
| 1 | action | execute_test | 10.INVEST-002 | Execute the action: Execute a Sell trade successfully and update holdings |
| 2 | post_verify | execute_test_partial | 10.INVEST-001 | Verify the executed sell trade appears in the user's trade history with the order ID, fund symbol... |
| 3 | post_verify | execute_test_partial | 10.INVEST-007 | Verify the fund holdings decreased by the sold quantity in the portfolio snapshot. |

**Manual Verification Required:**
- Purpose: Verify the user's cash balance increased by the expected proceeds from the sell.
- Suggested Step: After the sell completes, in the Investments module: 1) Open the trade confirmation / order details and record the gross proceeds and fees (or net amount). 2) Open the Account Cash / Transaction History and locate the transaction linked to the sell (filter by order ID, timestamp, or trade reference). 3) Verify there is a cash credit entry whose amount equals proceeds - fees. 4) Verify the current/displayed cash balance reflects that credit (i.e., the balance after the transaction equals the prior balance plus the credit). If prior balance is not available in the test run, confirming the cash credit amount matches proceeds - fees and that the displayed balance corresponds to the balance shown immediately after that transaction is sufficient for after_only verification.
- Reason: All candidates are either buy flow or failure/validation flows and do not access or display the account cash balance or the cash transaction that results from a successful sell. The requirement is after_only and must confirm the cash increase by comparing trade proceeds minus fees to the cash credit/new balance; none of the tests extract or assert that data.

---

### 10.INVEST-003: Create recurring investment plan with Weekly frequency

| Field | Value |
|-------|-------|
| Module | Investments |
| Workflow | Create Plan |
| Test Type | positive |
| Priority | High |
| Coverage | partial |
| Modifies State | trade_execution |

#### Source Test Details

**Preconditions:** User is logged in and the Create Plan form is open.

**Steps:**
1. Fill all required fields (Fund Symbol, Contribution Amount, Frequency, Start Date, Funding Account) with valid values and select Weekly frequency
2. Click "Create Plan"

**Expected Result:** Plan created successfully. The schedule is stored and a confirmation message "Plan created successfully." is shown.

#### Verification Mapping

| # | Ideal Verification | Status | Type | Strategy | Matched Test | Confidence |
|---|--------------------|--------|------|----------|--------------|------------|
| 1 | Confirm the recurring investment plan exists in Investments -> Recurring Plans with Weekly frequency, contribution am... | partial | Existence | After Only | 10.INVEST-004 - Create recurring investment plan with Monthly frequency | 60% |
| 2 | Verify the plan produced a scheduled job / next-occurrence entry in the system's scheduled trades list. | partial | Cascading Update | After Only | 10.INVEST-004 - Create recurring investment plan with Monthly frequency | 65% |

#### Coverage Gaps

- The test runs in the correct module and confirms creation, but it does not inspect the Recurring Plans list or verify the specific fields required (frequency, start date, fund symbol, funding account, Plan ID). Also the candidate uses Monthly frequency rather than Weekly, so as-is it cannot confirm the expected Weekly plan.
- The candidate operates in the correct module and stores a schedule, but it does not access/display the Scheduled Jobs / Next Transactions list or verify the next-occurrence entry or the required Weekly frequency. Also the test uses Monthly frequency rather than Weekly.

#### Execution Plan

| Step | Phase | Action | Test ID | Purpose |
|------|-------|--------|---------|---------|
| 1 | action | execute_test | 10.INVEST-003 | Execute the action: Create recurring investment plan with Weekly frequency |
| 2 | post_verify | execute_test_partial | 10.INVEST-004 | Confirm the recurring investment plan exists in Investments -> Recurring Plans with Weekly freque... |
| 3 | post_verify | execute_test_partial | 10.INVEST-004 | Verify the plan produced a scheduled job / next-occurrence entry in the system's scheduled trades... |

---

### 10.INVEST-004: Create recurring investment plan with Monthly frequency

| Field | Value |
|-------|-------|
| Module | Investments |
| Workflow | Create Plan |
| Test Type | positive |
| Priority | High |
| Coverage | partial |
| Modifies State | trade_execution |

#### Source Test Details

**Preconditions:** User is logged in and the Create Plan form is open.

**Steps:**
1. Fill all required fields (Fund Symbol, Contribution Amount, Frequency, Start Date, Funding Account) with valid values and select Monthly frequency
2. Click "Create Plan"

**Expected Result:** Plan created successfully. The schedule is stored and a confirmation message "Plan created successfully." is shown.

#### Verification Mapping

| # | Ideal Verification | Status | Type | Strategy | Matched Test | Confidence |
|---|--------------------|--------|------|----------|--------------|------------|
| 1 | Confirm the recurring investment plan exists in Investments -> Recurring Plans with Monthly frequency, contribution a... | partial | Existence | After Only | 10.INVEST-003 - Create recurring investment plan with Weekly frequency | 65% |
| 2 | Verify the plan created the next scheduled trade entry reflecting Monthly frequency in the scheduled jobs list. | partial | Cascading Update | After Only | 10.INVEST-003 - Create recurring investment plan with Weekly frequency | 60% |

#### Coverage Gaps

- The candidate operates on the correct module and confirms creation, but it does not inspect the Recurring Plans listing nor verify the specific fields required (Monthly frequency, contribution amount, start date, fund symbol, funding account, Plan ID). As written it creates a Weekly plan and only checks for a confirmation message, so it cannot by itself confirm the expected post-condition for an after_only verification.
- The test operates in the correct Investments module and creates a recurring plan (so it partially addresses the requirement). However, it uses a Weekly frequency (not Monthly) and does not access or verify the Scheduled Jobs / Next Transactions list or the next-occurrence date. As written it cannot, by itself (after_only), confirm the expected scheduled trade entry exists.

#### Execution Plan

| Step | Phase | Action | Test ID | Purpose |
|------|-------|--------|---------|---------|
| 1 | action | execute_test | 10.INVEST-004 | Execute the action: Create recurring investment plan with Monthly frequency |
| 2 | post_verify | execute_test_partial | 10.INVEST-003 | Confirm the recurring investment plan exists in Investments -> Recurring Plans with Monthly frequ... |
| 3 | post_verify | execute_test_partial | 10.INVEST-003 | Verify the plan created the next scheduled trade entry reflecting Monthly frequency in the schedu... |

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

| # | Ideal Verification | Status | Type | Strategy | Matched Test | Confidence |
|---|--------------------|--------|------|----------|--------------|------------|
| 1 | Verify a generated statement record exists for the selected account and month-year and includes a populated transacti... | found | Existence | After Only | 11.ACCSTA-002 - Generate statement using custom date range | 80% |
| 2 | Verify the generated statement remains accessible after logging out and logging back in (the statement persists in th... | partial | Session Persistence | After Only | 11.ACCSTA-002 - Generate statement using custom date range | 65% |

#### Coverage Gaps

- The candidate is on the correct module and shows the generated statement data (so it can confirm the statement exists), but it does NOT include the required logout/login and re-check steps. Because execution_strategy is after_only, the test must itself confirm persistence after logout/login — currently it does not.

#### Execution Plan

| Step | Phase | Action | Test ID | Purpose |
|------|-------|--------|---------|---------|
| 1 | action | execute_test | 11.ACCSTA-001 | Execute the action: Generate statement using month-and-year period |
| 2 | post_verify | execute_test | 11.ACCSTA-002 | Verify a generated statement record exists for the selected account and month-year and includes a... |
| 3 | post_verify | execute_test_partial | 11.ACCSTA-002 | Verify the generated statement remains accessible after logging out and logging back in (the stat... |

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

| # | Ideal Verification | Status | Type | Strategy | Matched Test | Confidence |
|---|--------------------|--------|------|----------|--------------|------------|
| 1 | Verify a generated statement record exists for the selected account and custom date range and includes transactions f... | partial | Existence | After Only | 11.ACCSTA-001 - Generate statement using month-and-year period | 62% |
| 2 | Verify the generated custom-range statement persists across a logout/login and remains viewable in the statements list. | partial | Session Persistence | After Only | 11.ACCSTA-001 - Generate statement using month-and-year period | 60% |

#### Coverage Gaps

- The candidate operates on the correct module and displays transactions for a selected period, so it can confirm that displayed transactions match a requested period. However it targets a month-and-year period rather than a custom date range and does not explicitly include the step to open Statement History and validate the statement record's transaction_list contents for the custom start/end dates.
- The candidate operates in the correct module and verifies statement generation and that transactions are displayed. However, it uses a month-and-year period (not a custom date range) and does not include logout/login or a persistence check. Because the execution strategy is after_only, the verification must by itself confirm the persisted record after login — the candidate lacks those steps.

#### Execution Plan

| Step | Phase | Action | Test ID | Purpose |
|------|-------|--------|---------|---------|
| 1 | action | execute_test | 11.ACCSTA-002 | Execute the action: Generate statement using custom date range |
| 2 | post_verify | execute_test_partial | 11.ACCSTA-001 | Verify a generated statement record exists for the selected account and custom date range and inc... |
| 3 | post_verify | execute_test_partial | 11.ACCSTA-001 | Verify the generated custom-range statement persists across a logout/login and remains viewable i... |

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

| # | Ideal Verification | Status | Type | Strategy | Matched Test | Confidence |
|---|--------------------|--------|------|----------|--------------|------------|
| 1 | Record the e-Statement preference before saving, then save the paperless checkbox and email, and verify the preferenc... | partial | Field Persistence | Before/After | 11.ACCSTA-008 - Save preference with invalid email format | 72% |

#### Coverage Gaps

- The candidate is on the correct module and touches the relevant UI elements, but it performs modifications and save attempts (negative validation scenario) rather than simply observing/displaying the current e_statement_preference. Because the execution_strategy is before_after, the verification test must be able to OBSERVE the checkbox state and email without causing state changes—this test as written would alter state and/or trigger validation, so it is not a full match.

#### Execution Plan

| Step | Phase | Action | Test ID | Purpose |
|------|-------|--------|---------|---------|
| 1 | pre_verify | execute_test_partial | 11.ACCSTA-008 | Record current e_statement_preference (checkbox state and email) from Account Statements preferen... |
| 2 | action | execute_test | 11.ACCSTA-003 | Execute the action: Save e-Statement preference with a valid email |
| 3 | post_verify | execute_test_partial | 11.ACCSTA-008 | After saving, refresh and re-login then read e_statement_preference again to confirm checkbox is ... |

---

### 12.SECSET-001: Change password with valid current and strong matching new password

| Field | Value |
|-------|-------|
| Module | Security Settings |
| Workflow | Change Password |
| Test Type | positive |
| Priority | High |
| Coverage | partial |
| Modifies State | credentials_update, password_change |

#### Source Test Details

**Preconditions:** User is authenticated and Security Settings > Change Password panel is open

**Steps:**
1. Expand the Change Password panel if collapsed
2. Fill all required fields (Current Password: valid current password, New Password: valid strong password, Confirm New Password: same as New Password)
3. Click "Change Password"

**Expected Result:** Password changed successfully and credentials are updated.

#### Verification Mapping

| # | Ideal Verification | Status | Type | Strategy | Matched Test | Confidence |
|---|--------------------|--------|------|----------|--------------|------------|
| 1 | Verify credential change by confirming the old password no longer authenticates and the new password does authenticate. | not_found | Credential Change | Before/After | - | - |
| 2 | Verify the password change persists across logout/login (user can log in with the new password later). | partial | Session Persistence | After Only | 12.SECSET-006 - Change password using a minimally-compliant strong password | 72% |

#### Verification Tests Needed

| # | Type | Strategy | Target Module | Observer | Suggested Test Title |
|---|------|----------|---------------|----------|----------------------|
| 1 | Credential Change | Before/After | Security Settings | - | Implement or run a verification test that performs sign-in attempts and is safe to run before and... |

#### Coverage Gaps

- All candidates are on the correct module (Security Settings) but none exercise or display authentication results:<br>- 12.SECSET-002: Tests validation when the current password entered into the change form is incorrect. It only checks for a validation error on the change form, not whether signing in with the old/new passwords authenticates. Running this before/after will not record authentication success/failure.<br>- 12.SECSET-004: Tests mismatch between New Password and Confirm fields; only a form validation negative test. It does not attempt or display sign-in results.<br>- 12.SECSET-006: Executes a password change and expects a success result. This is an action that would alter credentials rather than merely observe them; running it BEFORE the password-change action (as a baseline) would itself change credentials and invalidate the baseline. It does not explicitly perform sign-in attempts to show whether old/new credentials authenticate. Therefore none of these can serve as the before_after verification test that must observe authentication success/failure.
- Test 12.SECSET-006 checks the password change action and success message but does not confirm persistence by performing logout and re-login. Tests 12.SECSET-004 and 12.SECSET-002 are negative validation cases and do not verify successful persistence either.

#### Execution Plan

| Step | Phase | Action | Test ID | Purpose |
|------|-------|--------|---------|---------|
| 1 | action | execute_test | 12.SECSET-001 | Execute the action: Change password with valid current and strong matching new password |
| 2 | post_verify | execute_test_partial | 12.SECSET-006 | Verify the password change persists across logout/login (user can log in with the new password la... |

**Manual Verification Required:**
- Purpose: Verify credential change by confirming the old password no longer authenticates and the new password does authenticate.
- Suggested Step: Implement or run a verification test that performs sign-in attempts and is safe to run before and after the password-change action:<br>1) BEFORE password change (baseline):<br>   - Sign out (if necessary).<br>   - Attempt to sign in with the target username and the current (old) password.<br>   - Record that sign-in succeeded (timestamp, user id/session token or success result).<br>2) AFTER password change:<br>   - Sign out (if necessary).<br>   - Attempt to sign in with the same username and the OLD password — expect failure; record failure.<br>   - Attempt to sign in with the same username and the NEW password — expect success; record success.<br>Notes: Automate these as a dedicated authentication verification test (not as a change-password form test). Ensure the test does not perform the password-change action itself when run for the baseline.
- Reason: All candidates are on the correct module (Security Settings) but none exercise or display authentication results:<br>- 12.SECSET-002: Tests validation when the current password entered into the change form is incorrect. It only checks for a validation error on the change form, not whether signing in with the old/new passwords authenticates. Running this before/after will not record authentication success/failure.<br>- 12.SECSET-004: Tests mismatch between New Password and Confirm fields; only a form validation negative test. It does not attempt or display sign-in results.<br>- 12.SECSET-006: Executes a password change and expects a success result. This is an action that would alter credentials rather than merely observe them; running it BEFORE the password-change action (as a baseline) would itself change credentials and invalidate the baseline. It does not explicitly perform sign-in attempts to show whether old/new credentials authenticate. Therefore none of these can serve as the before_after verification test that must observe authentication success/failure.

---

### 13.SUPCEN-001: Send message successfully with required fields (no attachment)

| Field | Value |
|-------|-------|
| Module | Support Center |
| Workflow | Send Message |
| Test Type | positive |
| Priority | High |
| Coverage | partial |
| Modifies State | support_ticket_creation, message_status |

#### Source Test Details

**Preconditions:** User is logged in and the Support Center Send Message form is visible

**Steps:**
1. Fill all required fields (Subject with a valid-length subject, Category, Message Body with valid content)
2. Click "Send Message"

**Expected Result:** A success notification "Message sent successfully." is displayed and a ticket ID is shown

#### Verification Mapping

| # | Ideal Verification | Status | Type | Strategy | Matched Test | Confidence |
|---|--------------------|--------|------|----------|--------------|------------|
| 1 | Verify a support ticket is created and appears in the user's Support Center ticket list with the submitted subject, c... | partial | Existence | After Only | 13.SUPCEN-002 - Send message successfully with a valid attachment | 65% |
| 2 | Verify the created ticket is visible to the support team (a support agent can observe the ticket in the Support Cente... | partial | Existence | Cross-User | 13.SUPCEN-002 - Send message successfully with a valid attachment | 65% |

#### Coverage Gaps

- The candidate operates on the correct module and shows a ticket ID on successful send, so it partially confirms creation. However it does not explicitly access the user's ticket list or view the ticket detail to confirm category and message content, which the after_only strategy requires.
- The candidate runs in the correct module and produces a ticket ID, but it is a requester-side test and does not itself open the Support Center agent queue or display the ticket details from a support_agent view. Because the execution_strategy is cross_user, the verification must be performed while logged in as a support_agent and the test must reveal agent-visible data — the candidate does not do this by itself.

#### Execution Plan

| Step | Phase | Action | Test ID | Purpose |
|------|-------|--------|---------|---------|
| 1 | action | execute_test | 13.SUPCEN-001 | Execute the action: Send message successfully with required fields (no attachment) |
| 2 | post_verify | execute_test_partial | 13.SUPCEN-002 | Verify a support ticket is created and appears in the user's Support Center ticket list with the ... |
| 3 | session | session_switch | - | Switch to observer role: support_agent |
| 4 | post_verify | execute_test_partial | 13.SUPCEN-002 | Verify the created ticket is visible to the support team (a support agent can observe the ticket ... |

---

### 13.SUPCEN-002: Send message successfully with a valid attachment

| Field | Value |
|-------|-------|
| Module | Support Center |
| Workflow | Send Message |
| Test Type | positive |
| Priority | High |
| Coverage | partial |
| Modifies State | support_ticket_creation, message_status |

#### Source Test Details

**Preconditions:** User is logged in and the Support Center Send Message form is visible

**Steps:**
1. Fill all required fields (Subject with a valid-length subject, Category, Message Body with valid content) and attach a supported file type
2. Click "Send Message"

**Expected Result:** A success notification "Message sent successfully." is displayed and a ticket ID is shown

#### Verification Mapping

| # | Ideal Verification | Status | Type | Strategy | Matched Test | Confidence |
|---|--------------------|--------|------|----------|--------------|------------|
| 1 | Verify a support ticket with an attached file is created and the ticket entry lists the attachment metadata. | partial | Existence | After Only | 13.SUPCEN-001 - Send message successfully with required fields (no attachment) | 60% |
| 2 | Verify the support agent can access the ticket and download or view the attached file from the agent queue. | partial | Existence | Cross-User | 13.SUPCEN-007 - Submit with unsupported attachment type | 50% |

#### Coverage Gaps

- The test operates on the correct module and confirms ticket creation, but it explicitly has no attachment step and does not access the ticket's attachments section. Because the execution_strategy is after_only, the verification must confirm the attachment metadata exists; this test as-written cannot do that.
- The candidate operates in the correct module and touches attachment behavior, but it does not run as a support_agent nor does it open the agent queue/ticket details to display or download an attachment. Under the cross_user execution strategy the verification must be observable while logged in as support_agent; this test lacks those observer-side steps.

#### Execution Plan

| Step | Phase | Action | Test ID | Purpose |
|------|-------|--------|---------|---------|
| 1 | action | execute_test | 13.SUPCEN-002 | Execute the action: Send message successfully with a valid attachment |
| 2 | post_verify | execute_test_partial | 13.SUPCEN-001 | Verify a support ticket with an attached file is created and the ticket entry lists the attachmen... |
| 3 | session | session_switch | - | Switch to observer role: support_agent |
| 4 | post_verify | execute_test_partial | 13.SUPCEN-007 | Verify the support agent can access the ticket and download or view the attached file from the ag... |

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

| # | Ideal Verification | Status | Type | Strategy | Matched Test | Confidence |
|---|--------------------|--------|------|----------|--------------|------------|
| 1 | Verify a callback request record is created with the selected reason, preferred date/time window and phone number and... | partial | Existence | After Only | 13.SUPCEN-010 - Submit with Preferred Date set to the next business day (boundary) | 73% |
| 2 | Verify the support agent (callback scheduler) can see the callback request in their queue and the scheduled date/time... | not_found | Existence | Cross-User | - | - |

#### Verification Tests Needed

| # | Type | Strategy | Target Module | Observer | Suggested Test Title |
|---|------|----------|---------------|----------|----------------------|
| 1 | Existence | Cross-User | Support Center | support_agent | 1) Log in as support_agent. 2) Go to Support Center -> Callback Scheduling (or Callback Requests/... |

#### Coverage Gaps

- The test operates on the correct module and creates the callback_request, but it does not access/display the user's callbacks/requests listing or the detailed record fields required by the verification (reason, preferred date/time window, phone number). Because the execution_strategy is after_only, the verification must confirm the outcome itself — this test does not.
- All candidates are end-user submission tests (or unrelated message submission) and do not navigate to or display the support agent callback scheduling queue or the callback_request details. Under the cross_user strategy the verification test must be runnable as the observer (support_agent) and reveal the created callback_request; none of the candidates meet that requirement.

#### Execution Plan

| Step | Phase | Action | Test ID | Purpose |
|------|-------|--------|---------|---------|
| 1 | action | execute_test | 13.SUPCEN-003 | Execute the action: Submit Request Callback with valid inputs |
| 2 | post_verify | execute_test_partial | 13.SUPCEN-010 | Verify a callback request record is created with the selected reason, preferred date/time window ... |

**Manual Verification Required:**
- Purpose: Verify the support agent (callback scheduler) can see the callback request in their queue and the scheduled date/time/phone details for fulfillment.
- Suggested Step: 1) Log in as support_agent. 2) Go to Support Center -> Callback Scheduling (or Callback Requests/Queue) view. 3) Use filters/sort to locate the most recent callback_request (or search by requester/email/time). 4) Open the callback_request and confirm the Preferred Date, Preferred Time Window, and Phone Number fields match the submitted values. 5) Record the request ID, timestamp, and displayed scheduling details as evidence.
- Reason: All candidates are end-user submission tests (or unrelated message submission) and do not navigate to or display the support agent callback scheduling queue or the callback_request details. Under the cross_user strategy the verification test must be runnable as the observer (support_agent) and reveal the created callback_request; none of the candidates meet that requirement.

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

| # | Ideal Verification | Status | Type | Strategy | Matched Test | Confidence |
|---|--------------------|--------|------|----------|--------------|------------|
| 1 | Confirm the newly opened Checking account appears in the Accounts Overview listing with account type = Checking and t... | partial | Existence | After Only | 3.ACCOVE-002 - Accounts table displays expected columns in each row | 70% |
| 2 | Verify the funding source account was debited by the initial deposit amount (source balance decreased by deposit). | found | Financial Delta | Before/After | 3.ACCOVE-003 - Footer displays the total balance across all accounts | 90% |
| 3 | Verify the new Checking account's balance reflects the credited initial deposit (destination balance increased by dep... | found | Financial Delta | Before/After | 3.ACCOVE-003 - Footer displays the total balance across all accounts | 90% |

#### Coverage Gaps

- 3.ACCOVE-002 operates on the correct module and displays the required columns (Account Type and Current Balance), so it can observe the needed data. However, it does not by itself search for or assert the presence of a new Checking account with a specific balance value or verify the masked account number. Because the execution_strategy is after_only, the verification must confirm the specific outcome (existence of a Checking row with balance equal to the initial deposit), which this test does not currently perform.

#### Execution Plan

| Step | Phase | Action | Test ID | Purpose |
|------|-------|--------|---------|---------|
| 1 | navigate | navigate | - | Navigate to Accounts Overview |
| 2 | pre_verify | execute_test | 3.ACCOVE-003 | Record funding source account balance in Accounts Overview before opening the new account. |
| 3 | navigate | navigate | - | Navigate to Accounts Overview |
| 4 | pre_verify | execute_test | 3.ACCOVE-003 | Confirm the Checking account does not exist or had no balance in Accounts Overview before the ope... |
| 5 | navigate | navigate | - | Navigate to Open New Account |
| 6 | action | execute_test | 4.ONA-001 | Execute the action: Open a new Checking account with valid initial deposit |
| 7 | navigate | navigate | - | Navigate to Accounts Overview |
| 8 | post_verify | execute_test_partial | 3.ACCOVE-002 | Confirm the newly opened Checking account appears in the Accounts Overview listing with account t... |
| 9 | navigate | navigate | - | Navigate to Accounts Overview |
| 10 | post_verify | execute_test | 3.ACCOVE-003 | Record funding source account balance in Accounts Overview after account opening and compute delta. |
| 11 | navigate | navigate | - | Navigate to Accounts Overview |
| 12 | post_verify | execute_test | 3.ACCOVE-003 | Record the newly created Checking account balance in Accounts Overview after the open-account act... |

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

| # | Ideal Verification | Status | Type | Strategy | Matched Test | Confidence |
|---|--------------------|--------|------|----------|--------------|------------|
| 1 | Confirm the newly opened Savings account appears in the Accounts Overview listing with account type = Savings and the... | partial | Existence | After Only | 3.ACCOVE-002 - Accounts table displays expected columns in each row | 75% |
| 2 | Verify the funding source account was debited by the initial deposit amount (source balance decreased by deposit). | found | Financial Delta | Before/After | 3.ACCOVE-003 - Footer displays the total balance across all accounts | 90% |
| 3 | Verify the new Savings account's balance reflects the credited initial deposit (destination balance increased by depo... | found | Financial Delta | Before/After | 3.ACCOVE-003 - Footer displays the total balance across all accounts | 88% |

#### Coverage Gaps

- As-written the test only verifies that the expected columns are present in each row, not that a specific newly opened Savings account exists or that a row's balance equals the initial deposit. It therefore observes the relevant fields but does not confirm the specific expected outcome by itself.

#### Execution Plan

| Step | Phase | Action | Test ID | Purpose |
|------|-------|--------|---------|---------|
| 1 | navigate | navigate | - | Navigate to Accounts Overview |
| 2 | pre_verify | execute_test | 3.ACCOVE-003 | Record funding source account balance in Accounts Overview before opening the new account. |
| 3 | navigate | navigate | - | Navigate to Accounts Overview |
| 4 | pre_verify | execute_test | 3.ACCOVE-003 | Confirm the Savings account does not exist or had no balance in Accounts Overview before the open... |
| 5 | navigate | navigate | - | Navigate to Open New Account |
| 6 | action | execute_test | 4.ONA-002 | Execute the action: Open a new Savings account with valid initial deposit |
| 7 | navigate | navigate | - | Navigate to Accounts Overview |
| 8 | post_verify | execute_test_partial | 3.ACCOVE-002 | Confirm the newly opened Savings account appears in the Accounts Overview listing with account ty... |
| 9 | navigate | navigate | - | Navigate to Accounts Overview |
| 10 | post_verify | execute_test | 3.ACCOVE-003 | Record funding source account balance in Accounts Overview after account opening and compute delta. |
| 11 | navigate | navigate | - | Navigate to Accounts Overview |
| 12 | post_verify | execute_test | 3.ACCOVE-003 | Record the newly created Savings account balance in Accounts Overview after the open-account acti... |

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

| # | Ideal Verification | Status | Type | Strategy | Matched Test | Confidence |
|---|--------------------|--------|------|----------|--------------|------------|
| 1 | Verify source account balance decreased by the transfer amount after completing an internal transfer. | found | Financial Delta | Before/After | 3.ACCOVE-003 - Footer displays the total balance across all accounts | 92% |
| 2 | Verify destination account balance increased by the transfer amount after completing an internal transfer. | found | Financial Delta | Before/After | 3.ACCOVE-003 - Footer displays the total balance across all accounts | 85% |
| 3 | Confirm a transfer transaction record appears in the transaction list (Account Statements) referencing the transfer a... | partial | Existence | After Only | 11.ACCSTA-002 - Generate statement using custom date range | 65% |

#### Coverage Gaps

- This test operates on the correct module (Account Statements) and retrieves transactions for a specified date range, so it can display the transaction list needed for verification. However its expected result only states 'retrieved transactions' and does not explicitly assert that the transaction ID is shown or that a specific transaction (amount + ID) exists, so it does not fully guarantee the required verification by itself.

#### Execution Plan

| Step | Phase | Action | Test ID | Purpose |
|------|-------|--------|---------|---------|
| 1 | navigate | navigate | - | Navigate to Accounts Overview |
| 2 | pre_verify | execute_test | 3.ACCOVE-003 | Record Source Account balance in Accounts Overview before performing the transfer. |
| 3 | navigate | navigate | - | Navigate to Accounts Overview |
| 4 | pre_verify | execute_test | 3.ACCOVE-003 | Record Destination Account balance in Accounts Overview before performing the transfer. |
| 5 | navigate | navigate | - | Navigate to Transfer Funds |
| 6 | action | execute_test | 5.TRAFUN-001 | Execute the action: Successful internal transfer between own accounts |
| 7 | navigate | navigate | - | Navigate to Accounts Overview |
| 8 | post_verify | execute_test | 3.ACCOVE-003 | Record Source Account balance in Accounts Overview after the transfer and compute delta. |
| 9 | navigate | navigate | - | Navigate to Accounts Overview |
| 10 | post_verify | execute_test | 3.ACCOVE-003 | Record Destination Account balance in Accounts Overview after the transfer and compute delta. |
| 11 | navigate | navigate | - | Navigate to Account Statements |
| 12 | post_verify | execute_test_partial | 11.ACCSTA-002 | Confirm a transfer transaction record appears in the transaction list (Account Statements) refere... |

---

### 5.TRAFUN-002: Successful external transfer to matching account number

| Field | Value |
|-------|-------|
| Module | Transfer Funds |
| Workflow | Transfer funds |
| Test Type | positive |
| Priority | High |
| Coverage | partial |
| Modifies State | external_transfer_request, account_balance |

#### Source Test Details

**Preconditions:** User is logged in, Transfer Funds page is open, and user has a Checking or Savings account with sufficient balance

**Steps:**
1. Select the radio button for external transfer (External Account)
2. Fill all required fields (select Source Account from the Source Account dropdown, enter Destination Account Number, enter Confirm Account Number matching the Destination Account Number, enter a valid Transfer Amount within available balance)
3. Click the "Transfer" or "Submit" button

**Expected Result:** Confirmation message "Transfer completed successfully." is displayed and a transaction ID is shown for the transfer.

#### Verification Mapping

| # | Ideal Verification | Status | Type | Strategy | Matched Test | Confidence |
|---|--------------------|--------|------|----------|--------------|------------|
| 1 | Verify the source account balance decreased by the external transfer amount. | found | Financial Delta | Before/After | 3.ACCOVE-003 - Footer displays the total balance across all accounts | 90% |
| 2 | Verify an external transfer request/record exists in Transfer Funds (outgoing transfers) that includes the destinatio... | not_found | Existence | After Only | - | - |

#### Verification Tests Needed

| # | Type | Strategy | Target Module | Observer | Suggested Test Title |
|---|------|----------|---------------|----------|----------------------|
| 1 | Existence | After Only | Transfer Funds | - | After submitting the external transfer, navigate to Transfer Funds -> Outgoing/External Transfers... |

#### Coverage Gaps

- Evaluated candidates:<br>- 5.TRAFUN-006: Operates in Transfer Funds and uses external transfer path, but it intentionally causes a validation failure (non-matching account numbers) and therefore does not produce a transfer record or transaction ID. Cannot confirm a successful external transfer record (not suitable for after_only verification).<br>- 5.TRAFUN-001: Confirms a successful transfer and shows a transaction ID, but it is an internal transfer between own accounts, not an external/outgoing transfer. It does not validate that an outgoing external transfer record exists or appears in the outgoing transfers list with destination account number.<br>- 5.TRAFUN-004: Verifies the UI switches to external-account input fields when transfer type changes; it does not perform or confirm a transfer nor check the outgoing/recent transfers list for a resulting record or transaction ID.<br>Because none of the candidates open the outgoing/external transfers list and assert existence of an external transfer entry with the destination account number and transaction ID, no candidate fully satisfies the after_only verification requirement.

#### Execution Plan

| Step | Phase | Action | Test ID | Purpose |
|------|-------|--------|---------|---------|
| 1 | navigate | navigate | - | Navigate to Accounts Overview |
| 2 | pre_verify | execute_test | 3.ACCOVE-003 | Record Source Account balance in Accounts Overview before initiating the external transfer. |
| 3 | navigate | navigate | - | Navigate to Transfer Funds |
| 4 | action | execute_test | 5.TRAFUN-002 | Execute the action: Successful external transfer to matching account number |
| 5 | navigate | navigate | - | Navigate to Accounts Overview |
| 6 | post_verify | execute_test | 3.ACCOVE-003 | Record Source Account balance in Accounts Overview after the external transfer and compute delta. |

**Manual Verification Required:**
- Purpose: Verify an external transfer request/record exists in Transfer Funds (outgoing transfers) that includes the destination account number and returned transaction ID/reference.
- Suggested Step: After submitting the external transfer, navigate to Transfer Funds -> Outgoing/External Transfers or Recent Transfers. Search or scan the list for an entry matching the destination account number used in the transfer. Verify that the entry exists and that it displays the transaction ID/reference for that transfer. Record the transfer row details (destination account number, transaction ID/reference, date/time, amount) as evidence.
- Reason: Evaluated candidates:<br>- 5.TRAFUN-006: Operates in Transfer Funds and uses external transfer path, but it intentionally causes a validation failure (non-matching account numbers) and therefore does not produce a transfer record or transaction ID. Cannot confirm a successful external transfer record (not suitable for after_only verification).<br>- 5.TRAFUN-001: Confirms a successful transfer and shows a transaction ID, but it is an internal transfer between own accounts, not an external/outgoing transfer. It does not validate that an outgoing external transfer record exists or appears in the outgoing transfers list with destination account number.<br>- 5.TRAFUN-004: Verifies the UI switches to external-account input fields when transfer type changes; it does not perform or confirm a transfer nor check the outgoing/recent transfers list for a resulting record or transaction ID.<br>Because none of the candidates open the outgoing/external transfers list and assert existence of an external transfer entry with the destination account number and transaction ID, no candidate fully satisfies the after_only verification requirement.

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

| # | Ideal Verification | Status | Type | Strategy | Matched Test | Confidence |
|---|--------------------|--------|------|----------|--------------|------------|
| 1 | Verify the source account balance decreased by the payment amount after submitting the bill payment. | found | Financial Delta | Before/After | 3.ACCOVE-003 - Footer displays the total balance across all accounts | 90% |
| 2 | Confirm the payment transaction appears in the Account Statements transaction list with a payment reference code and ... | partial | Existence | After Only | 11.ACCSTA-001 - Generate statement using month-and-year period | 60% |

#### Coverage Gaps

- This test operates on the correct module (Account Statements) and displays the generated transactions for a chosen period, so it can surface the transaction list. However, it does not explicitly check for the presence of a payment transaction, the payment reference code, or payee details. Because the execution strategy is after_only, the test must confirm the expected outcome by itself; as written it only generates the statement and does not assert the specific fields required.

#### Execution Plan

| Step | Phase | Action | Test ID | Purpose |
|------|-------|--------|---------|---------|
| 1 | navigate | navigate | - | Navigate to Accounts Overview |
| 2 | pre_verify | execute_test | 3.ACCOVE-003 | Record Source Account balance in Accounts Overview before submitting the payment. |
| 3 | navigate | navigate | - | Navigate to Payments |
| 4 | action | execute_test | 6.PAYMEN-001 | Execute the action: Submit valid payment and verify reference code and balance update |
| 5 | navigate | navigate | - | Navigate to Accounts Overview |
| 6 | post_verify | execute_test | 3.ACCOVE-003 | Record Source Account balance in Accounts Overview after the payment and compute delta. |
| 7 | navigate | navigate | - | Navigate to Account Statements |
| 8 | post_verify | execute_test_partial | 11.ACCSTA-001 | Confirm the payment transaction appears in the Account Statements transaction list with a payment... |

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

| # | Ideal Verification | Status | Type | Strategy | Matched Test | Confidence |
|---|--------------------|--------|------|----------|--------------|------------|
| 1 | Verify the approved Personal loan record exists and is listed with loan terms (amount, rate, status) in the Request L... | partial | Existence | After Only | 7.REQLOA-013 - Accept Personal loan request when Loan Amount equals the Personal minimum | 72% |
| 2 | Verify a collateral hold indicator or hold amount appears on the selected collateral account (related account shows a... | partial | Cascading Update | Before/After | 3.ACCOVE-003 - Footer displays the total balance across all accounts | 65% |

#### Coverage Gaps

- Test 7.REQLOA-013 uses the correct module and loan type (Personal) but its expected outcome only states the request 'may be approved' and does not include steps to view the loan listing or assert the created/approved status and displayed loan terms. The other candidates (7.REQLOA-002 and 7.REQLOA-003) are for Auto and Home loans respectively and therefore do not match the required Personal loan verification.
- Correct module (Accounts Overview) and reads account balances, but it does not access/display the specific hold/reserve indicator or held amount required by the before_after verification.

#### Execution Plan

| Step | Phase | Action | Test ID | Purpose |
|------|-------|--------|---------|---------|
| 1 | navigate | navigate | - | Navigate to Accounts Overview |
| 2 | pre_verify | execute_test_partial | 3.ACCOVE-003 | Record collateral account hold/available-balance indicators in Accounts Overview before submittin... |
| 3 | navigate | navigate | - | Navigate to Request Loan |
| 4 | action | execute_test | 7.REQLOA-001 | Execute the action: Request a Personal loan with valid inputs |
| 5 | post_verify | execute_test_partial | 7.REQLOA-013 | Verify the approved Personal loan record exists and is listed with loan terms (amount, rate, stat... |
| 6 | navigate | navigate | - | Navigate to Accounts Overview |
| 7 | post_verify | execute_test_partial | 3.ACCOVE-003 | Record collateral account hold/available-balance indicators in Accounts Overview after loan creat... |

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

| # | Ideal Verification | Status | Type | Strategy | Matched Test | Confidence |
|---|--------------------|--------|------|----------|--------------|------------|
| 1 | Verify the approved Auto loan record exists and is listed with loan terms (amount, rate, status) in the Request Loan/... | not_found | Existence | After Only | - | - |
| 2 | Verify a collateral hold indicator or hold amount appears on the selected collateral account after the Auto loan is c... | partial | Cascading Update | Before/After | 3.ACCOVE-003 - Footer displays the total balance across all accounts | 60% |

#### Verification Tests Needed

| # | Type | Strategy | Target Module | Observer | Suggested Test Title |
|---|------|----------|---------------|----------|----------------------|
| 1 | Existence | After Only | Request Loan | - | After the loan submission action completes, navigate to Request Loan -> Loan Listing (or Loan Det... |

#### Coverage Gaps

- All provided tests operate on the Request Loan module (good), but each submits Personal or Home loan types—not 'Auto'. While they expect an approval message and display new loan details, they would not validate the presence of an Auto loan record or its loan terms. Since after_only requires the verification to confirm the Auto loan exists, none of these candidates meet the requirement.
- Although this test targets the correct module (Accounts Overview), it only accesses Current Balance values and the footer total. It does not currently read or display the hold/reserve indicator or held amount required by the verification. Therefore it cannot be used as-is but is the closest candidate and can be adapted.

#### Execution Plan

| Step | Phase | Action | Test ID | Purpose |
|------|-------|--------|---------|---------|
| 1 | navigate | navigate | - | Navigate to Accounts Overview |
| 2 | pre_verify | execute_test_partial | 3.ACCOVE-003 | Record collateral account hold/available-balance indicators in Accounts Overview before submittin... |
| 3 | navigate | navigate | - | Navigate to Request Loan |
| 4 | action | execute_test | 7.REQLOA-002 | Execute the action: Request an Auto loan with valid inputs |
| 5 | navigate | navigate | - | Navigate to Accounts Overview |
| 6 | post_verify | execute_test_partial | 3.ACCOVE-003 | Record collateral account hold/available-balance indicators in Accounts Overview after loan creat... |

**Manual Verification Required:**
- Purpose: Verify the approved Auto loan record exists and is listed with loan terms (amount, rate, status) in the Request Loan/loan listing.
- Suggested Step: After the loan submission action completes, navigate to Request Loan -> Loan Listing (or Loan Details for the user). Filter or scan for entries with Loan Type = 'Auto'. Locate the entry with the expected Loan Amount and Interest Rate and verify loan_application_status is 'Approved' or 'Active' and that displayed amount and rate match the submitted values. If automating, create a new test that: 1) opens Request Loan listing, 2) searches/filters for Loan Type = Auto and the expected amount, 3) asserts interest rate equals expected value, and 4) asserts loan_application_status equals 'Approved' or 'Active'.
- Reason: All provided tests operate on the Request Loan module (good), but each submits Personal or Home loan types—not 'Auto'. While they expect an approval message and display new loan details, they would not validate the presence of an Auto loan record or its loan terms. Since after_only requires the verification to confirm the Auto loan exists, none of these candidates meet the requirement.

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

| # | Ideal Verification | Status | Type | Strategy | Matched Test | Confidence |
|---|--------------------|--------|------|----------|--------------|------------|
| 1 | Verify the approved Home loan record exists and is listed with loan terms (amount, rate, status) in the Request Loan/... | partial | Existence | After Only | 7.REQLOA-014 - Accept Home loan request when Loan Amount equals the Home maximum | 70% |
| 2 | Verify a collateral hold indicator or hold amount appears on the selected collateral account after the Home loan is c... | partial | Cascading Update | Before/After | 3.ACCOVE-003 - Footer displays the total balance across all accounts | 72% |

#### Coverage Gaps

- The candidate is the only Home-type submission among the options (so it's the best starting point), but it does not explicitly display or assert the loan listing/loan_application_status after submission. Since the execution strategy is after_only, the test must itself confirm the created/approved Home loan with matching terms; the current test does not guarantee that.
- Correct module (Accounts Overview) but the test as written does not access or display the hold/reserve indicator or held-amount/available-balance values required by the verification. Because execution_strategy is before_after, a test that simply observes those fields would be sufficient — this one needs to be modified to capture them.

#### Execution Plan

| Step | Phase | Action | Test ID | Purpose |
|------|-------|--------|---------|---------|
| 1 | navigate | navigate | - | Navigate to Accounts Overview |
| 2 | pre_verify | execute_test_partial | 3.ACCOVE-003 | Record collateral account hold/available-balance indicators in Accounts Overview before submittin... |
| 3 | navigate | navigate | - | Navigate to Request Loan |
| 4 | action | execute_test | 7.REQLOA-003 | Execute the action: Request a Home loan with valid inputs |
| 5 | post_verify | execute_test_partial | 7.REQLOA-014 | Verify the approved Home loan record exists and is listed with loan terms (amount, rate, status) ... |
| 6 | navigate | navigate | - | Navigate to Accounts Overview |
| 7 | post_verify | execute_test_partial | 3.ACCOVE-003 | Record collateral account hold/available-balance indicators in Accounts Overview after loan creat... |

---

### 7.REQLOA-010: Verify no actual balance debits occur after loan creation

| Field | Value |
|-------|-------|
| Module | Request Loan |
| Workflow | Request Loan |
| Test Type | positive |
| Priority | Medium |
| Coverage | full |
| Modifies State | loan_creation, collateral_hold, loan_status |

#### Source Test Details

**Preconditions:** User is signed in, Request Loan page is open, and a valid loan request is ready to submit.

**Steps:**
1. Fill all required fields with valid values and note the displayed Collateral Account balance
2. Click "Submit Loan Request"

**Expected Result:** Loan is created and the collateral account balance remains unchanged (no actual balance debits occur).

#### Verification Mapping

| # | Ideal Verification | Status | Type | Strategy | Matched Test | Confidence |
|---|--------------------|--------|------|----------|--------------|------------|
| 1 | Demonstrate that the collateral account's actual available balance is unchanged after loan creation (no debit), by co... | found | Cascading Update | Before/After | 3.ACCOVE-003 - Footer displays the total balance across all accounts | 90% |

#### Execution Plan

| Step | Phase | Action | Test ID | Purpose |
|------|-------|--------|---------|---------|
| 1 | navigate | navigate | - | Navigate to Accounts Overview |
| 2 | pre_verify | execute_test | 3.ACCOVE-003 | Record the collateral account available/current balance in Accounts Overview before submitting th... |
| 3 | navigate | navigate | - | Navigate to Request Loan |
| 4 | action | execute_test | 7.REQLOA-010 | Execute the action: Verify no actual balance debits occur after loan creation |
| 5 | navigate | navigate | - | Navigate to Accounts Overview |
| 6 | post_verify | execute_test | 3.ACCOVE-003 | Record the collateral account available/current balance in Accounts Overview after loan creation ... |

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

| # | Ideal Verification | Status | Type | Strategy | Matched Test | Confidence |
|---|--------------------|--------|------|----------|--------------|------------|
| 1 | Verify that updated contact fields persist after a page refresh and after logging out and logging back in (the profil... | partial | Field Persistence | Before/After | 8.UCI-002 - Submit with all required fields empty | 60% |

#### Coverage Gaps

- Although the test targets the correct module, its steps exercise validation for empty required fields and do not read or display the existing contact field values. Under a before_after execution strategy the test must OBSERVE/DISPLAY the contact_fields so they can be recorded before and after the update; this candidate does not do that.

#### Execution Plan

| Step | Phase | Action | Test ID | Purpose |
|------|-------|--------|---------|---------|
| 1 | pre_verify | execute_test_partial | 8.UCI-002 | Record existing contact fields on the profile page before performing the update. |
| 2 | action | execute_test | 8.UCI-001 | Execute the action: Update profile with all valid contact fields |
| 3 | post_verify | execute_test_partial | 8.UCI-002 | After updating, refresh the page and then perform logout/login; record contact fields after refre... |

---

### 9.MANCAR-001: Request a new Debit card with valid linked account and complete shipping address

| Field | Value |
|-------|-------|
| Module | Manage Cards |
| Workflow | Request Card |
| Test Type | positive |
| Priority | High |
| Coverage | partial |
| Modifies State | card_request_creation, card_status |

#### Source Test Details

**Preconditions:** User is authenticated and the Request Card form is visible

**Steps:**
1. Select Card Type as Debit
2. Select a linked account in good standing
3. Fill the complete Shipping Address
4. Click "Request Card"

**Expected Result:** A card-request ticket is opened and the UI shows "Card request submitted successfully." with a tracking ID

#### Verification Mapping

| # | Ideal Verification | Status | Type | Strategy | Matched Test | Confidence |
|---|--------------------|--------|------|----------|--------------|------------|
| 1 | Confirm a new card-request record exists in Manage Cards requests with the tracking ID, requested card type (Debit), ... | partial | Existence | After Only | 9.MANCAR-002 - Request a new Credit card with valid linked account and complete shippin... | 55% |
| 2 | Verify an operational ticket referencing the card request and tracking ID is visible to bank staff. | partial | Existence | Cross-User | 13.SUPCEN-001 - Send message successfully with required fields (no attachment) | 55% |

#### Coverage Gaps

- While 9.MANCAR-002 is on the correct module and confirms a tracking ID on submission, it targets Credit (not Debit) and does not inspect the Manage Cards -> Requests list or verify the linked account identifier, full shipping address, or request status. The other candidates are negative/validation tests and cannot confirm that a request was created.
- None of the candidates explicitly exercise the admin-facing Recent Tickets view or include a search for a ticket referencing a card request/tracking ID. 13.SUPCEN-001 is the closest because it uses the Support Center and shows a generated ticket ID, but its steps only cover sending a message and confirming the success message/ID for the creator — it does not describe the admin-side observation (Recent Tickets search and status check). 9.MANCAR-002 creates the card request and returns a tracking ID but is in Manage Cards (creator action), not in the admin Support Center view. 9.MANCAR-010 is negative/blocked flow and irrelevant.

#### Execution Plan

| Step | Phase | Action | Test ID | Purpose |
|------|-------|--------|---------|---------|
| 1 | action | execute_test | 9.MANCAR-001 | Execute the action: Request a new Debit card with valid linked account and complete shipping address |
| 2 | post_verify | execute_test_partial | 9.MANCAR-002 | Confirm a new card-request record exists in Manage Cards requests with the tracking ID, requested... |
| 3 | session | session_switch | - | Switch to observer role: admin |
| 4 | navigate | navigate | - | Navigate to Support Center |
| 5 | post_verify | execute_test_partial | 13.SUPCEN-001 | Verify an operational ticket referencing the card request and tracking ID is visible to bank staff. |

---

### 9.MANCAR-002: Request a new Credit card with valid linked account and complete shipping address

| Field | Value |
|-------|-------|
| Module | Manage Cards |
| Workflow | Request Card |
| Test Type | positive |
| Priority | High |
| Coverage | partial |
| Modifies State | card_request_creation, card_status |

#### Source Test Details

**Preconditions:** User is authenticated and the Request Card form is visible

**Steps:**
1. Select Card Type as Credit
2. Select a linked account in good standing
3. Fill the complete Shipping Address
4. Click "Request Card"

**Expected Result:** A card-request ticket is opened and the UI shows "Card request submitted successfully." with a tracking ID

#### Verification Mapping

| # | Ideal Verification | Status | Type | Strategy | Matched Test | Confidence |
|---|--------------------|--------|------|----------|--------------|------------|
| 1 | Confirm a new card-request record exists in Manage Cards requests with the tracking ID, requested card type (Credit),... | partial | Existence | After Only | 9.MANCAR-001 - Request a new Debit card with valid linked account and complete shipping... | 60% |
| 2 | Verify a bank-side ticket was created for the credit card request and is visible to card-ops staff. | partial | Existence | Cross-User | 13.SUPCEN-001 - Send message successfully with required fields (no attachment) | 65% |

#### Coverage Gaps

- Candidate 9.MANCAR-001 uses the correct module and returns a tracking ID on submission but requests a Debit card (not Credit) and only verifies a submission confirmation message — it does not inspect the Manage Cards Requests/Request History list to confirm the stored request row and its fields. The other candidates either expect blocked submissions or validation errors and therefore cannot verify a created request.
- Operates on the correct module and produces a ticket ID, but does not include actions to view Recent Tickets as admin or to verify that the created ticket references the credit card request/tracking ID and is in open/assigned state. Because the verification strategy is cross_user (observer = admin), the candidate needs to display the ticket in the admin-accessible Recent Tickets view — which this test does not do by itself.

#### Execution Plan

| Step | Phase | Action | Test ID | Purpose |
|------|-------|--------|---------|---------|
| 1 | action | execute_test | 9.MANCAR-002 | Execute the action: Request a new Credit card with valid linked account and complete shipping add... |
| 2 | post_verify | execute_test_partial | 9.MANCAR-001 | Confirm a new card-request record exists in Manage Cards requests with the tracking ID, requested... |
| 3 | session | session_switch | - | Switch to observer role: admin |
| 4 | navigate | navigate | - | Navigate to Support Center |
| 5 | post_verify | execute_test_partial | 13.SUPCEN-001 | Verify a bank-side ticket was created for the credit card request and is visible to card-ops staff. |

---

### 9.MANCAR-003: Update spending limit with a valid amount

| Field | Value |
|-------|-------|
| Module | Manage Cards |
| Workflow | Update Controls |
| Test Type | positive |
| Priority | High |
| Coverage | none |
| Modifies State | card_control_update, spending_limit |

#### Source Test Details

**Preconditions:** An existing card is selected and the Update Controls form is open.

**Steps:**
1. Fill all required fields (Select Existing Card, New Spending Limit with a valid numeric amount, Card Status as desired) and leave Travel Notice empty
2. Click "Update Controls"

**Expected Result:** "Card controls updated successfully." is displayed and the spending limit shown in the controls reflects the new amount.

#### Verification Mapping

| # | Ideal Verification | Status | Type | Strategy | Matched Test | Confidence |
|---|--------------------|--------|------|----------|--------------|------------|
| 1 | Record the card's current controls, update spending limit, then verify the new limit persists after refresh and re-lo... | not_found | Field Persistence | Before/After | - | - |

#### Verification Tests Needed

| # | Type | Strategy | Target Module | Observer | Suggested Test Title |
|---|------|----------|---------------|----------|----------------------|
| 1 | Field Persistence | Before/After | Manage Cards | - | Create/execute a verification test that: 1) Log in and navigate to Manage Cards. 2) Select the ta... |

#### Coverage Gaps

- All three candidates operate in the Manage Cards module and exercise the Update Controls flow, but none explicitly state that they access or display the card's current spending limit in the Controls view. They focus on validation or successful update behavior (entering new values and checking validation/success messages) rather than explicitly reading and reporting the persisted spending limit field. Because the verification requires recording the displayed spending limit before and after, these candidates do not guarantee the required observation step.

#### Execution Plan

| Step | Phase | Action | Test ID | Purpose |
|------|-------|--------|---------|---------|
| 1 | action | execute_test | 9.MANCAR-003 | Execute the action: Update spending limit with a valid amount |

**Manual Verification Required:**
- Purpose: Record the card's current controls, update spending limit, then verify the new limit persists after refresh and re-login.
- Suggested Step: Create/execute a verification test that: 1) Log in and navigate to Manage Cards. 2) Select the target existing card. 3) Open the Controls section and read/record the displayed Spending Limit value (card_controls). 4) (After the Update action runs) Refresh the page, then log out and log back in. 5) Reopen Manage Cards -> select the same card -> Controls and read the Spending Limit value again for comparison. Record both values for before/after comparison.
- Reason: All three candidates operate in the Manage Cards module and exercise the Update Controls flow, but none explicitly state that they access or display the card's current spending limit in the Controls view. They focus on validation or successful update behavior (entering new values and checking validation/success messages) rather than explicitly reading and reporting the persisted spending limit field. Because the verification requires recording the displayed spending limit before and after, these candidates do not guarantee the required observation step.

---

### 9.MANCAR-004: Freeze an active card by updating Card Status

| Field | Value |
|-------|-------|
| Module | Manage Cards |
| Workflow | Update Controls |
| Test Type | positive |
| Priority | High |
| Coverage | partial |
| Modifies State | card_status, card_control_update |

#### Source Test Details

**Preconditions:** An existing card currently in Active status is selected and the Update Controls form is open.

**Steps:**
1. Select Frozen in Card Status and fill all other required fields (Select Existing Card, any required numeric fields)
2. Click "Update Controls"

**Expected Result:** "Card controls updated successfully." is displayed and the card status updates to Frozen.

#### Verification Mapping

| # | Ideal Verification | Status | Type | Strategy | Matched Test | Confidence |
|---|--------------------|--------|------|----------|--------------|------------|
| 1 | Record the card status before freeze, apply the freeze, then verify the status badge changed to Frozen and available ... | partial | Status Transition | Before/After | 9.MANCAR-006 - Add a travel notice with valid dates and destination | 55% |

#### Coverage Gaps

- The candidate operates in the correct module and uses Update Controls, but its documented steps/expected results focus on saving controls (and travel notice) and the success message. It does not explicitly open the Card List/Card Details to display the current status badge, available action buttons, or audit/history entry, which are required to record the before/after observations.

#### Execution Plan

| Step | Phase | Action | Test ID | Purpose |
|------|-------|--------|---------|---------|
| 1 | pre_verify | execute_test_partial | 9.MANCAR-006 | Record current status badge and action buttons for the selected card in Manage Cards before update. |
| 2 | action | execute_test | 9.MANCAR-004 | Execute the action: Freeze an active card by updating Card Status |
| 3 | post_verify | execute_test_partial | 9.MANCAR-006 | After Update Controls, reload Card List and open Card Details to confirm badge reads 'Frozen', 'U... |

---

### 9.MANCAR-006: Add a travel notice with valid dates and destination

| Field | Value |
|-------|-------|
| Module | Manage Cards |
| Workflow | Update Controls |
| Test Type | positive |
| Priority | Medium |
| Coverage | none |
| Modifies State | card_control_update, card_controls |

#### Source Test Details

**Preconditions:** An existing card is selected and the Update Controls form is open.

**Steps:**
1. Fill all required fields (Select Existing Card, Card Status as desired) and fill Travel Notice with a valid start date, end date, and destination
2. Click "Update Controls"

**Expected Result:** "Card controls updated successfully." is displayed and the travel notice (dates and destination) is saved and shown in the controls.

#### Verification Mapping

| # | Ideal Verification | Status | Type | Strategy | Matched Test | Confidence |
|---|--------------------|--------|------|----------|--------------|------------|
| 1 | Confirm the travel notice entry exists in the card's controls with the exact start date, end date, and destination. | not_found | Existence | After Only | - | - |
| 2 | Verify the travel notice persists across sessions (survives logout and login). | not_found | Session Persistence | After Only | - | - |

#### Verification Tests Needed

| # | Type | Strategy | Target Module | Observer | Suggested Test Title |
|---|------|----------|---------------|----------|----------------------|
| 1 | Existence | After Only | Manage Cards | - | Manually verify after performing the add action: Open Manage Cards -> Select the target card -> C... |
| 2 | Session Persistence | After Only | Manage Cards | - | 1) Log in as the target user. 2) Go to Manage Cards and select the card that had the travel notic... |

#### Coverage Gaps

- The verification requires an after-only check that a travel notice row exists showing the exact Start Date, End Date, and Destination for the selected card. Candidate tests: 9.MANCAR-013 is a negative validation test (ensures an invalid date range is rejected) and explicitly expects the travel notice NOT to be saved; 9.MANCAR-007 and 9.MANCAR-003 update controls while leaving travel notice empty and do not inspect the travel notices list. None of them open the Controls -> Travel Notices and assert the presence and contents of the newly added notice.
- Required verification must run after the action and independently confirm the travel notice still exists after logout/login. Candidate tests: 9.MANCAR-013 operates on Manage Cards and travel notice fields but tests invalid input and non-persistence; 9.MANCAR-007 updates controls without a travel notice; 9.MANCAR-001 is unrelated (card request). None access/display an existing travel notice after a new session, so none can serve as the after_only verification.

#### Execution Plan

| Step | Phase | Action | Test ID | Purpose |
|------|-------|--------|---------|---------|
| 1 | action | execute_test | 9.MANCAR-006 | Execute the action: Add a travel notice with valid dates and destination |

**Manual Verification Required:**
- Purpose: Confirm the travel notice entry exists in the card's controls with the exact start date, end date, and destination.
- Suggested Step: Manually verify after performing the add action: Open Manage Cards -> Select the target card -> Click Controls -> Travel Notices. Locate a travel notice row that matches the exact Start Date, End Date, and Destination submitted and confirm it is associated with the selected card. Record or assert the displayed Start Date, End Date, and Destination match the submitted values.
- Reason: The verification requires an after-only check that a travel notice row exists showing the exact Start Date, End Date, and Destination for the selected card. Candidate tests: 9.MANCAR-013 is a negative validation test (ensures an invalid date range is rejected) and explicitly expects the travel notice NOT to be saved; 9.MANCAR-007 and 9.MANCAR-003 update controls while leaving travel notice empty and do not inspect the travel notices list. None of them open the Controls -> Travel Notices and assert the presence and contents of the newly added notice.
- Purpose: Verify the travel notice persists across sessions (survives logout and login).
- Suggested Step: 1) Log in as the target user. 2) Go to Manage Cards and select the card that had the travel notice. 3) Open Controls → Travel Notices and record the notice's Start Date, End Date, and Destination (or confirm presence). 4) Log out. 5) Log back in as the same user. 6) Navigate again to Manage Cards → Controls → Travel Notices. 7) Verify the same travel notice is present and that Start Date, End Date, and Destination exactly match the previously recorded values. Expected result: the travel notice remains present with identical Start Date, End Date, and Destination.
- Reason: Required verification must run after the action and independently confirm the travel notice still exists after logout/login. Candidate tests: 9.MANCAR-013 operates on Manage Cards and travel notice fields but tests invalid input and non-persistence; 9.MANCAR-007 updates controls without a travel notice; 9.MANCAR-001 is unrelated (card request). None access/display an existing travel notice after a new session, so none can serve as the after_only verification.

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

| # | Ideal Verification | Status | Type | Strategy | Matched Test | Confidence |
|---|--------------------|--------|------|----------|--------------|------------|
| 1 | Record card controls before update, perform the update without travel notice, and verify the updated control values p... | found | Field Persistence | Before/After | 9.MANCAR-003 - Update spending limit with a valid amount | 90% |
| 2 | Verify that no travel notice record was created for the card after the update (travel notice fields were left empty). | partial | Absence | After Only | 9.MANCAR-003 - Update spending limit with a valid amount | 72% |

#### Coverage Gaps

- 9.MANCAR-003 operates in the correct module and matches the scenario of leaving Travel Notice empty, but its expected checks only confirm the spending limit update and success message — it does not currently inspect the Travel Notices list to confirm absence. 9.MANCAR-006 creates a travel notice (opposite of required) and 9.MANCAR-013 checks validation for invalid dates (different negative case), so both are less suitable.

#### Execution Plan

| Step | Phase | Action | Test ID | Purpose |
|------|-------|--------|---------|---------|
| 1 | pre_verify | execute_test | 9.MANCAR-003 | Record current controls (spending limit, status) for the selected card. |
| 2 | action | execute_test | 9.MANCAR-007 | Execute the action: Update controls without adding a travel notice (travel notice optional) |
| 3 | post_verify | execute_test | 9.MANCAR-003 | After Update Controls, refresh and logout/login; reopen Controls and compare values to before to ... |
| 4 | post_verify | execute_test_partial | 9.MANCAR-003 | Verify that no travel notice record was created for the card after the update (travel notice fiel... |

---

## Associated Verification Test Cases

These are matched test cases referenced by post-verification mappings.

| TC ID | Module | Title | Type | Priority | Expected Result |
|-------|--------|-------|------|----------|------------------|
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
| 13.SUPCEN-007 | Support Center | Submit with unsupported attachment type | negative | Medium | Inline validation guidance about the attachment type is displayed and the message is not sent. |
| 13.SUPCEN-010 | Support Center | Submit with Preferred Date set to the next business day (boundary) | edge_case | Medium | Request is accepted and a success message "Callback request submitted." is displayed; an email confirmation is sent. |
| 3.ACCOVE-002 | Accounts Overview | Accounts table displays expected columns in each row | positive | High | Every row contains Account Number, Account Type, Current Balance, Account Status (Active badge), and Open Date. |
| 3.ACCOVE-003 | Accounts Overview | Footer displays the total balance across all accounts | positive | High | Footer total balance equals the sum of all Current Balance values shown in the table. |
| 7.REQLOA-013 | Request Loan | Accept Personal loan request when Loan Amount equals the Personal minimum | edge_case | Medium | Loan request is processed and may be approved; amount is accepted as within allowed Personal range. |
| 7.REQLOA-014 | Request Loan | Accept Home loan request when Loan Amount equals the Home maximum | edge_case | Medium | Loan request is processed and may be approved; amount is accepted as within allowed Home range. |
| 8.UCI-002 | Update Contact Info | Submit with all required fields empty | negative | Medium | Validation errors shown for all required fields and invalid fields are highlighted. |
| 9.MANCAR-001 | Manage Cards | Request a new Debit card with valid linked account and complete shipping address | positive | High | A card-request ticket is opened and the UI shows "Card request submitted successfully." with a tracking ID |
| 9.MANCAR-002 | Manage Cards | Request a new Credit card with valid linked account and complete shipping address | positive | High | A card-request ticket is opened and the UI shows "Card request submitted successfully." with a tracking ID |
| 9.MANCAR-003 | Manage Cards | Update spending limit with a valid amount | positive | High | "Card controls updated successfully." is displayed and the spending limit shown in the controls reflects the new amount. |
| 9.MANCAR-006 | Manage Cards | Add a travel notice with valid dates and destination | positive | Medium | "Card controls updated successfully." is displayed and the travel notice (dates and destination) is saved and shown i... |
