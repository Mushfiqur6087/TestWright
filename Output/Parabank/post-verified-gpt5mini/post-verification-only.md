# Parabank - Post-Verification Report

**Base URL:** 
**Generated:** 2026-04-18T20:46:44.594062

## Summary

| Metric | Count |
|--------|-------|
| Source Tests Needing Verification | 27 |
| Full Coverage | 1 |
| Partial Coverage | 18 |
| Minimal Coverage | 0 |
| No Coverage | 8 |
| Tests With Verification Gaps | 11 |
| Total Missing Verifications | 12 |
| Associated Verification Tests | 16 |

### Generated Verifications by Type

| Type | Count |
|------|-------|
| Existence | 22 |
| Absence | 1 |
| Field Persistence | 10 |
| Status Transition | 1 |
| Cascading Update | 3 |
| Credential Change | 1 |
| Session Persistence | 1 |
| Financial Delta | 10 |

### Generated Verifications by Strategy

| Strategy | Count |
|----------|-------|
| After Only | 28 |
| Before/After | 20 |
| Cross-User | 1 |

### Top Coverage Gaps

- Hard module rule: the target module is Manage Cards and the required state to verify is card_control_update. All provided candidates are from different modules and their can_verify_states do not overlap with card_control_update, so they cannot observe the travel notice entries. Therefore none can be marked as a match.
- All candidate tests belong to Investments or Manage Cards modules and their can_verify_states (portfolio_snapshot, fund_holdings, card_request_status, shipping_address, etc.) do not overlap with the source test's modified state (support_ticket_creation). Per the HARD MODULE RULE, a candidate from a different module may only be 'found' if its can_verify_states overlap the modified state. They do not, so they cannot verify the Support Center attachment requirement.
- The candidate runs in the correct module and touches external transfer inputs, but it only validates UI input/option behavior rather than confirming persistence of a new external transfer record. Also its module action_states overlap the source modification (external_transfer_request), so it appears to be an action/form test rather than an observation of the resulting stored record.
- All three candidate tests operate on the Transfer Funds page and their module action_states include 'funds_transfer' (they exercise the transfer action rather than observe history). Per the HARD MODULE RULE, a candidate whose action_states overlap the source test's modifies_state should not be marked 'found' because it performs the same action instead of verifying the result. None of the candidates open transfer history or a transfer-details view or search by transaction ID (they do not access/display the required transfer record or its transaction ID), so none fully satisfies the after_only verification requirement.
- All candidate tests are for different modules and their can_verify_states (account_creation_status, transfer_status, payment_status, account_balance, etc.) do not overlap with the required modifies_state card_control_update. Per the HARD MODULE RULE, a candidate from another module can only be used if its can_verify_states overlap the target state; they do not. Therefore none are suitable.
- Right module and touches the required state fields (card_status and card_controls), but the candidate's steps perform the Update Controls action (overlaps with the source test's modifies_state). Per the rule, a test that performs the same action cannot be marked as a full verification — it must be an observer-only test.
- All provided candidates belong to other modules (Accounts Overview, Investments) and their can_verify_states do not include card_control_update. Per the Hard Module Rule, a candidate from a different module can only be considered if its can_verify_states overlaps with the source test's modifies_state (card_control_update). None do. Details: Test 3.ACCOVE-002 and 3.ACCOVE-007 are for Accounts Overview and verify account table fields (no card/travel-notice data). Test 10.INVEST-016 is for Investments and verifies plan start-date validation (no card/travel-notice data).
- The candidate operates in the correct module (Investments) but does not access or display the plan detail or scheduled occurrences required by the verification. It observes portfolio snapshot data, not recurring plan schedule or next execution date, so it cannot by itself confirm the expected weekly cadence or persistence after refresh/login.
- Not marked 'found' because the candidate performs a callback request creation (same modifies_state as the source). The after_only strategy requires a test that confirms the existing callback_request record after the action, not another submission.
- Same module (Investments) but the test inspects portfolio snapshot rather than Order History/Trades and its action_states overlap with the source test's modified states, so it cannot, as written, confirm the existence of the executed trade record after the sell action.

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
| 1 | Confirm the trade order was recorded by locating the executed trade in the user's trade history/Orders with the retur... | partial | Existence | After Only | 3.ACCOVE-002 - Accounts table displays expected columns in each row | 20% |
| 2 | Record the funding account cash balance before the buy, execute the buy, then verify the funding account cash balance... | partial | Financial Delta | Before/After | 4.ONA-011 - Real-time validation appears and clears for Initial Deposit field | 50% |
| 3 | Record the fund holdings for the bought fund before the trade, execute the buy, then verify the fund holdings increas... | found | Financial Delta | Before/After | 10.INVEST-007 - Portfolio snapshot displays current holdings and read-only values | 90% |

#### Coverage Gaps

- Required target is Investments -> Order History/Trades. The candidate is in Accounts Overview and only verifies account-level columns (account number, type, balance, status, open date). Its can_verify_states do not include trade_execution, trade_status, order_id, fund symbol, or quantity. Under the HARD MODULE RULE a different-module candidate can be 'found' only if its verifiable states overlap with the source test's modifies_state (trade_execution, cash_balance, fund_holdings); this candidate does not provide those states, so it cannot fully verify the requirement.
- Required target module is Investments. Candidate is from Open New Account; although its can_verify_states includes funding_account_balance (overlaps the required cash_balance), its action_states include funding_transfer (overlaps the source test's modifies_state). Per the HARD MODULE RULE, a different-module candidate whose action_states overlap with the source modifies_state must not be marked 'found'. Also the candidate's explicit steps do not show a direct read of the cash_balance value.

#### Execution Plan

| Step | Phase | Action | Test ID | Purpose |
|------|-------|--------|---------|---------|
| 1 | pre_verify | execute_test | 10.INVEST-007 | Record held quantity of the fund before the trade in the portfolio snapshot. |
| 2 | action | execute_test | 10.INVEST-001 | Execute the action: Execute a Buy trade successfully and update holdings |
| 3 | post_verify | execute_test | 10.INVEST-007 | Record held quantity after trade; expected increase = purchased quantity. |

**Manual Verification Required:**
- Purpose: Confirm the trade order was recorded by locating the executed trade in the user's trade history/Orders with the returned order ID, action = Buy, symbol and quantity matching the submission.
- Suggested Step: Verify in module 'Investments' — matcher chose 3.ACCOVE-002 in 'Accounts Overview' which is not the observer module.
- Reason: Module mismatch: matched test is in 'Accounts Overview', but verification should occur in 'Investments'.
- Purpose: Record the funding account cash balance before the buy, execute the buy, then verify the funding account cash balance decreased by the trade cost (expected quantity * execution price) and that the decrease persists.
- Suggested Step: Verify in module 'Investments' — matcher chose 4.ONA-011 in 'Open New Account' which is not the observer module.
- Reason: Module mismatch: matched test is in 'Open New Account', but verification should occur in 'Investments'.

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
| 1 | Confirm the sell order was recorded by locating the executed trade in the user's trade history/Orders with the return... | partial | Existence | After Only | 10.INVEST-007 - Portfolio snapshot displays current holdings and read-only values | 35% |
| 2 | Record the fund holdings for the sold fund before the trade, execute the sell, then verify the fund holdings decrease... | found | Financial Delta | Before/After | 10.INVEST-007 - Portfolio snapshot displays current holdings and read-only values | 92% |
| 3 | Record the destination account cash balance before the sell, execute the sell, then verify the destination account ca... | found | Financial Delta | Before/After | 3.ACCOVE-003 - Footer displays the total balance across all accounts | 95% |

#### Coverage Gaps

- Same module (Investments) but the test inspects portfolio snapshot rather than Order History/Trades and its action_states overlap with the source test's modified states, so it cannot, as written, confirm the existence of the executed trade record after the sell action.

#### Execution Plan

| Step | Phase | Action | Test ID | Purpose |
|------|-------|--------|---------|---------|
| 1 | pre_verify | execute_test | 10.INVEST-007 | Record held quantity of the fund before the trade in the portfolio snapshot. |
| 2 | action | execute_test | 10.INVEST-002 | Execute the action: Execute a Sell trade successfully and update holdings |
| 3 | post_verify | execute_test_partial | 10.INVEST-007 | Confirm the sell order was recorded by locating the executed trade in the user's trade history/Or... |
| 4 | post_verify | execute_test | 10.INVEST-007 | Record held quantity after trade; expected decrease = sold quantity. |

**Manual Verification Required:**
- Purpose: Record the destination account cash balance before the sell, execute the sell, then verify the destination account cash balance increased by the sale proceeds (quantity * execution price) and the increase persists.
- Suggested Step: Verify in module 'Investments' — matcher chose 3.ACCOVE-003 in 'Accounts Overview' which is not the observer module.
- Reason: Module mismatch: matched test is in 'Accounts Overview', but verification should occur in 'Investments'.

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
| 1 | Confirm the recurring investment plan was created by locating the plan in the Investments recurring plans list and ve... | not_found | Existence | After Only | - | - |
| 2 | Verify the schedule for the created Weekly plan persists after refresh and re-login and that the next scheduled execu... | partial | Field Persistence | After Only | 10.INVEST-007 - Portfolio snapshot displays current holdings and read-only values | 40% |

#### Verification Tests Needed

| # | Type | Strategy | Target Module | Observer | Suggested Test Title |
|---|------|----------|---------------|----------|----------------------|
| 1 | Existence | After Only | Investments | - | After creating the recurring plan, verify manually: 1) Log into the app and navigate to Investmen... |

#### Coverage Gaps

- All candidate tests belong to other modules (Open New Account, Payments). Their can_verify_states (account_creation_status, funding_account_balance, payment_status, etc.) do not overlap with the source test's modified state (trade_execution). Per the HARD MODULE RULE, a different-module candidate can only be used if its can_verify_states overlap; they do not. Additionally, none of the candidates display or open the Investments recurring plans list or plan detail view required to confirm frequency, fund symbol, contribution amount, start date, and funding account.
- The candidate operates in the correct module (Investments) but does not access or display the plan detail or scheduled occurrences required by the verification. It observes portfolio snapshot data, not recurring plan schedule or next execution date, so it cannot by itself confirm the expected weekly cadence or persistence after refresh/login.

#### Execution Plan

| Step | Phase | Action | Test ID | Purpose |
|------|-------|--------|---------|---------|
| 1 | action | execute_test | 10.INVEST-003 | Execute the action: Create recurring investment plan with Weekly frequency |
| 2 | post_verify | execute_test_partial | 10.INVEST-007 | Verify the schedule for the created Weekly plan persists after refresh and re-login and that the ... |

**Manual Verification Required:**
- Purpose: Confirm the recurring investment plan was created by locating the plan in the Investments recurring plans list and verifying frequency = Weekly, contribution amount, fund symbol, start date, and funding account match the submitted values.
- Suggested Step: After creating the recurring plan, verify manually: 1) Log into the app and navigate to Investments -> Recurring Plans (or Scheduled Trades). 2) Search or filter by the submitted Fund Symbol, Start Date, or Funding Account to locate the new plan. 3) Open the plan's detail view. 4) Assert the Frequency field equals 'Weekly'. 5) Assert the Contribution Amount equals the submitted amount. 6) Assert the Fund Symbol matches the submitted symbol. 7) Assert the Start Date matches the submitted date. 8) Assert the Funding Account matches the submitted funding account. If automating, implement a new Investments test that performs these steps and asserts the values.
- Reason: All candidate tests belong to other modules (Open New Account, Payments). Their can_verify_states (account_creation_status, funding_account_balance, payment_status, etc.) do not overlap with the source test's modified state (trade_execution). Per the HARD MODULE RULE, a different-module candidate can only be used if its can_verify_states overlap; they do not. Additionally, none of the candidates display or open the Investments recurring plans list or plan detail view required to confirm frequency, fund symbol, contribution amount, start date, and funding account.

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
| 1 | Confirm the recurring investment plan was created by locating the plan in the Investments recurring plans list and ve... | not_found | Existence | After Only | - | - |
| 2 | Verify the schedule for the created Monthly plan persists after refresh and re-login and that the next scheduled exec... | partial | Field Persistence | After Only | 1.LOGIN-012 - Page refresh on authenticated page retains logged-in state | 35% |

#### Verification Tests Needed

| # | Type | Strategy | Target Module | Observer | Suggested Test Title |
|---|------|----------|---------------|----------|----------------------|
| 1 | Existence | After Only | Investments | - | After creating the recurring plan, navigate to Investments -> Recurring Plans (or Scheduled Trade... |

#### Coverage Gaps

- All candidate tests are for different modules (Open New Account, Payments) and their can_verify_states do not overlap with the source test's modifies_state (trade_execution). Under the HARD MODULE RULE, a different-module candidate can only be 'found' if its can_verify_states overlap with trade_execution. None do, so none can confirm the Investments recurring plan creation.
- This candidate is for Login/session persistence and can confirm the user remains authenticated across refresh, which helps the refresh/re-login part of the requirement. However it does not operate on the Investments module nor does it read or display trade_execution (plan schedule, frequency, or next execution date). Therefore it cannot, by itself, confirm that the Monthly frequency and next scheduled execution date persisted after refresh and re-login.

#### Execution Plan

| Step | Phase | Action | Test ID | Purpose |
|------|-------|--------|---------|---------|
| 1 | action | execute_test | 10.INVEST-004 | Execute the action: Create recurring investment plan with Monthly frequency |

**Manual Verification Required:**
- Purpose: Confirm the recurring investment plan was created by locating the plan in the Investments recurring plans list and verifying frequency = Monthly, contribution amount, fund symbol, start date, and funding account match the submitted values.
- Suggested Step: After creating the recurring plan, navigate to Investments -> Recurring Plans (or Scheduled Trades). Locate the entry for the newly created plan and open its details. Verify: 1) Frequency = Monthly; 2) Fund symbol matches submitted symbol; 3) Contribution amount matches submitted amount; 4) Start date matches submitted date; 5) Funding account matches submitted account.
- Reason: All candidate tests are for different modules (Open New Account, Payments) and their can_verify_states do not overlap with the source test's modifies_state (trade_execution). Under the HARD MODULE RULE, a different-module candidate can only be 'found' if its can_verify_states overlap with trade_execution. None do, so none can confirm the Investments recurring plan creation.
- Purpose: Verify the schedule for the created Monthly plan persists after refresh and re-login and that the next scheduled execution date matches a monthly cadence from the start date.
- Suggested Step: Verify in module 'Investments' — matcher chose 1.LOGIN-012 in 'Login' which is not the observer module.
- Reason: Module mismatch: matched test is in 'Login', but verification should occur in 'Investments'.

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
| 1 | Open the generated statement for the selected account and month and inspect the statement metadata and transaction li... | partial | Existence | After Only | 3.ACCOVE-002 - Accounts table displays expected columns in each row | 15% |

#### Coverage Gaps

- Target module is 'Account Statements' and the verification requires inspecting a generated statement's statement_data and transaction_list. None of the provided candidates operate in the Account Statements module or expose statement_data/transaction_list. The Accounts Overview test's can_verify_states do not overlap with the source test's modifies_state (statement_generation), so it cannot serve as the after_only verifier.

#### Execution Plan

| Step | Phase | Action | Test ID | Purpose |
|------|-------|--------|---------|---------|
| 1 | action | execute_test | 11.ACCSTA-001 | Execute the action: Generate statement using month-and-year period |

**Manual Verification Required:**
- Purpose: Open the generated statement for the selected account and month and inspect the statement metadata and transaction list to confirm the statement contains transactions whose transaction dates fall within the selected month and are associated with the selected account.
- Suggested Step: Verify in module 'Account Statements' — matcher chose 3.ACCOVE-002 in 'Accounts Overview' which is not the observer module.
- Reason: Module mismatch: matched test is in 'Accounts Overview', but verification should occur in 'Account Statements'.

---

### 11.ACCSTA-002: Generate statement using custom date range

| Field | Value |
|-------|-------|
| Module | Account Statements |
| Workflow | Generate Statement |
| Test Type | positive |
| Priority | High |
| Coverage | none |
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
| 1 | Open the generated statement for the selected account and custom date range and verify the returned statement contain... | not_found | Existence | After Only | - | - |

#### Verification Tests Needed

| # | Type | Strategy | Target Module | Observer | Suggested Test Title |
|---|------|----------|---------------|----------|----------------------|
| 1 | Existence | After Only | Account Statements | - | After running 'Generate statement using custom date range', navigate to Account Statements → loca... |

#### Coverage Gaps

- All candidates are from different modules (Accounts Overview, Open New Account) and their can_verify_states do not include statement_generation or transaction_list. Per the Hard Module Rule, a candidate from a different module can only be 'found' if its can_verify_states overlap the source test's modifies_state (statement_generation). No overlap exists, so none can serve as the after_only verification of the generated statement.

#### Execution Plan

| Step | Phase | Action | Test ID | Purpose |
|------|-------|--------|---------|---------|
| 1 | action | execute_test | 11.ACCSTA-002 | Execute the action: Generate statement using custom date range |

**Manual Verification Required:**
- Purpose: Open the generated statement for the selected account and custom date range and verify the returned statement contains transactions only within the specified start and end dates and is tied to the selected account.
- Suggested Step: After running 'Generate statement using custom date range', navigate to Account Statements → locate the generated statement for the selected account and date range → open Statement Details → inspect statement_data.transaction_list and for each transaction verify: (1) transaction.date is >= start_date and <= end_date, and (2) transaction.account_id (or account identifier) matches the selected account. Also verify a statement record exists for the date range and that statement_data contains the filtered transaction_list.
- Reason: All candidates are from different modules (Accounts Overview, Open New Account) and their can_verify_states do not include statement_generation or transaction_list. Per the Hard Module Rule, a candidate from a different module can only be 'found' if its can_verify_states overlap the source test's modifies_state (statement_generation). No overlap exists, so none can serve as the after_only verification of the generated statement.

---

### 11.ACCSTA-003: Save e-Statement preference with a valid email

| Field | Value |
|-------|-------|
| Module | Account Statements |
| Workflow | Save Preference |
| Test Type | positive |
| Priority | High |
| Coverage | none |
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
| 1 | Record the current paperless checkbox state and email; after saving the e-Statement preference, refresh the preferenc... | not_found | Field Persistence | Before/After | - | - |

#### Verification Tests Needed

| # | Type | Strategy | Target Module | Observer | Suggested Test Title |
|---|------|----------|---------------|----------|----------------------|
| 1 | Field Persistence | Before/After | Account Statements | - | Create or run a test that opens the Account Statements > Preferences page and records the followi... |

#### Coverage Gaps

- All candidate tests are in other modules (Login, Open New Account) and their can_verify_states do not overlap with the modified state e_statement_preference. Per the Hard Module Rule, a candidate from a different module can only be used if its can_verify_states overlaps with e_statement_preference — none do. Therefore none can serve as the before/after observer for Account Statements preferences.

#### Execution Plan

| Step | Phase | Action | Test ID | Purpose |
|------|-------|--------|---------|---------|
| 1 | action | execute_test | 11.ACCSTA-003 | Execute the action: Save e-Statement preference with a valid email |

**Manual Verification Required:**
- Purpose: Record the current paperless checkbox state and email; after saving the e-Statement preference, refresh the preferences page and re-open the account (and perform a re-login) to confirm the paperless checkbox remains selected and the entered email persists.
- Suggested Step: Create or run a test that opens the Account Statements > Preferences page and records the following (this is sufficient for before_after execution):<br>1) Log in as the test user.<br>2) Navigate to Account Statements -> Preferences (or Account Statements preferences page).<br>3) Record the current state of the 'Paperless statements' checkbox (checked/unchecked) and the value in the 'Email Address' field.<br>(Record these values as the BEFORE snapshot.)<br>4) Perform the source action: check the paperless checkbox, enter the valid email, and click 'Save Preference'.<br>5) After saving, refresh the Preferences page and observe the checkbox and email field — record these values.<br>6) Log out, then log back in as the same user, re-open Account Statements -> Preferences and record the checkbox state and email field again (AFTER snapshot).<br>7) Compare BEFORE and AFTER snapshots: the paperless checkbox should be selected and the entered email should persist across refresh and re-login.<br>Note: Because the strategy is before_after, the test only needs to display/read these values (no automated assertion of change is required by the verifier).
- Reason: All candidate tests are in other modules (Login, Open New Account) and their can_verify_states do not overlap with the modified state e_statement_preference. Per the Hard Module Rule, a candidate from a different module can only be used if its can_verify_states overlaps with e_statement_preference — none do. Therefore none can serve as the before/after observer for Account Statements preferences.

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
| 1 | Attempt authentication using the old/current password and then using the new password after the change: the old passw... | found | Credential Change | After Only | 1.LOGIN-008 - After changing password the old password no longer works | 90% |
| 2 | Verify the password change persists across logout/login by logging out and then logging back in with the new password... | partial | Session Persistence | After Only | 3.ACCOVE-001 - Welcome message shows the user's name | 60% |

#### Coverage Gaps

- The requirement (after_only) needs a test that confirms the new credentials actually create a session by themselves (i.e., perform or validate login). 3.ACCOVE-001 observes session-dependent UI (good), but it does not perform the login/authentication step or explicitly verify that the new password succeeded — therefore it cannot by itself confirm the credential change persisted.

#### Execution Plan

| Step | Phase | Action | Test ID | Purpose |
|------|-------|--------|---------|---------|
| 1 | action | execute_test | 12.SECSET-001 | Execute the action: Change password with valid current and strong matching new password |
| 2 | navigate | navigate | - | Navigate to Login |
| 3 | post_verify | execute_test | 1.LOGIN-008 | Attempt authentication using the old/current password and then using the new password after the c... |
| 4 | navigate | navigate | - | Navigate to Accounts Overview |
| 5 | post_verify | execute_test_partial | 3.ACCOVE-001 | Verify the password change persists across logout/login by logging out and then logging back in w... |

---

### 13.SUPCEN-001: Send message successfully with required fields (no attachment)

| Field | Value |
|-------|-------|
| Module | Support Center |
| Workflow | Send Message |
| Test Type | positive |
| Priority | High |
| Coverage | none |
| Modifies State | support_ticket_creation |

#### Source Test Details

**Preconditions:** User is logged in and the Support Center Send Message form is visible

**Steps:**
1. Fill all required fields (Subject with a valid-length subject, Category, Message Body with valid content)
2. Click "Send Message"

**Expected Result:** A success notification "Message sent successfully." is displayed and a ticket ID is shown

#### Verification Mapping

| # | Ideal Verification | Status | Type | Strategy | Matched Test | Confidence |
|---|--------------------|--------|------|----------|--------------|------------|
| 1 | Locate the newly created support ticket in the Support Center ticket list or open the ticket detail by ticket ID and ... | not_found | Existence | After Only | - | - |

#### Verification Tests Needed

| # | Type | Strategy | Target Module | Observer | Suggested Test Title |
|---|------|----------|---------------|----------|----------------------|
| 1 | Existence | After Only | Support Center | - | After the 'Send Message' action completes, copy the returned ticket ID (or go to Support Center >... |

#### Coverage Gaps

- Execution strategy is after_only, so the verification test must, by itself, confirm that a support_ticket record exists with the submitted subject, category, and message body (by searching/opening the ticket in the Support Center). All candidate tests are for other modules (Manage Cards, Update Contact Info, Payments) and their can_verify_states do not overlap with the source test's modified state (support_ticket_creation). Per the Hard Module Rule, a candidate from a different module can be 'found' only if its can_verify_states overlap with the modified state — none do. Therefore none can verify the support_ticket outcome.

#### Execution Plan

| Step | Phase | Action | Test ID | Purpose |
|------|-------|--------|---------|---------|
| 1 | action | execute_test | 13.SUPCEN-001 | Execute the action: Send message successfully with required fields (no attachment) |

**Manual Verification Required:**
- Purpose: Locate the newly created support ticket in the Support Center ticket list or open the ticket detail by ticket ID and confirm the ticket record contains the submitted subject, category, and message body.
- Suggested Step: After the 'Send Message' action completes, copy the returned ticket ID (or go to Support Center > Recent Tickets). In Support Center: search or open the ticket by that ticket ID (or select the recent ticket). Open the ticket detail and confirm the Subject, Category, and Message Body fields exactly match the submitted values. Record the ticket ID and screenshots of the ticket detail as evidence.
- Reason: Execution strategy is after_only, so the verification test must, by itself, confirm that a support_ticket record exists with the submitted subject, category, and message body (by searching/opening the ticket in the Support Center). All candidate tests are for other modules (Manage Cards, Update Contact Info, Payments) and their can_verify_states do not overlap with the source test's modified state (support_ticket_creation). Per the Hard Module Rule, a candidate from a different module can be 'found' only if its can_verify_states overlap with the modified state — none do. Therefore none can verify the support_ticket outcome.

---

### 13.SUPCEN-002: Send message successfully with a valid attachment

| Field | Value |
|-------|-------|
| Module | Support Center |
| Workflow | Send Message |
| Test Type | positive |
| Priority | High |
| Coverage | none |
| Modifies State | support_ticket_creation |

#### Source Test Details

**Preconditions:** User is logged in and the Support Center Send Message form is visible

**Steps:**
1. Fill all required fields (Subject with a valid-length subject, Category, Message Body with valid content) and attach a supported file type
2. Click "Send Message"

**Expected Result:** A success notification "Message sent successfully." is displayed and a ticket ID is shown

#### Verification Mapping

| # | Ideal Verification | Status | Type | Strategy | Matched Test | Confidence |
|---|--------------------|--------|------|----------|--------------|------------|
| 1 | Open the created support ticket in Support Center and confirm the attached file is recorded with filename and content... | not_found | Existence | After Only | - | - |

#### Verification Tests Needed

| # | Type | Strategy | Target Module | Observer | Suggested Test Title |
|---|------|----------|---------------|----------|----------------------|
| 1 | Existence | After Only | Support Center | - | In Support Center, open the ticket detail for the returned ticket ID. Inspect the Attachments sec... |

#### Coverage Gaps

- All candidate tests belong to Investments or Manage Cards modules and their can_verify_states (portfolio_snapshot, fund_holdings, card_request_status, shipping_address, etc.) do not overlap with the source test's modified state (support_ticket_creation). Per the HARD MODULE RULE, a candidate from a different module may only be 'found' if its can_verify_states overlap the modified state. They do not, so they cannot verify the Support Center attachment requirement.

#### Execution Plan

| Step | Phase | Action | Test ID | Purpose |
|------|-------|--------|---------|---------|
| 1 | action | execute_test | 13.SUPCEN-002 | Execute the action: Send message successfully with a valid attachment |

**Manual Verification Required:**
- Purpose: Open the created support ticket in Support Center and confirm the attached file is recorded with filename and content-type metadata and that the attachment can be downloaded/opened.
- Suggested Step: In Support Center, open the ticket detail for the returned ticket ID. Inspect the Attachments section and verify: (1) the attachment is listed with the correct filename, size, and MIME/content-type metadata; (2) clicking the attachment initiates a download or opens the file and the file content matches the uploaded file. Record screenshots of metadata and confirm successful download/open and content match.
- Reason: All candidate tests belong to Investments or Manage Cards modules and their can_verify_states (portfolio_snapshot, fund_holdings, card_request_status, shipping_address, etc.) do not overlap with the source test's modified state (support_ticket_creation). Per the HARD MODULE RULE, a candidate from a different module may only be 'found' if its can_verify_states overlap the modified state. They do not, so they cannot verify the Support Center attachment requirement.

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
| 1 | Confirm a callback request record is created in Support Center with the selected reason, preferred date (at least nex... | partial | Existence | After Only | 13.SUPCEN-010 - Submit with Preferred Date set to the next business day (boundary) | 72% |
| 2 | Verify the callback request is visible to Support Center agents by having a support_agent observer view the support q... | not_found | Existence | Cross-User | - | - |

#### Verification Tests Needed

| # | Type | Strategy | Target Module | Observer | Suggested Test Title |
|---|------|----------|---------------|----------|----------------------|
| 1 | Existence | Cross-User | Support Center | support_agent | Log in as a support_agent -> Navigate to Support Center -> Open Incoming Requests / Support Queue... |

#### Coverage Gaps

- Not marked 'found' because the candidate performs a callback request creation (same modifies_state as the source). The after_only strategy requires a test that confirms the existing callback_request record after the action, not another submission.
- All provided candidate tests operate in unrelated modules (Manage Cards, Payments). Per the HARD MODULE RULE, a candidate from a different module can only be considered if its can_verify_states overlaps with the source test's modifies_state (callback_request_creation). None of the candidates list callback_request or related states in their can_verify_states, so they cannot display or verify the created callback_request in the Support Center. They also do not run in the Support Center module and therefore cannot be used for cross_user observation as a support_agent.

#### Execution Plan

| Step | Phase | Action | Test ID | Purpose |
|------|-------|--------|---------|---------|
| 1 | action | execute_test | 13.SUPCEN-003 | Execute the action: Submit Request Callback with valid inputs |
| 2 | post_verify | execute_test_partial | 13.SUPCEN-010 | Confirm a callback request record is created in Support Center with the selected reason, preferre... |

**Manual Verification Required:**
- Purpose: Verify the callback request is visible to Support Center agents by having a support_agent observer view the support queue and confirm the new callback request appears for agents to action.
- Suggested Step: Log in as a support_agent -> Navigate to Support Center -> Open Incoming Requests / Support Queue -> Filter or search for request type 'Callback' or the submitting user's name/phone -> Locate the new callback request and confirm the displayed Reason for Call, Preferred Date/Time, and Phone match the submitted values.
- Reason: All provided candidate tests operate in unrelated modules (Manage Cards, Payments). Per the HARD MODULE RULE, a candidate from a different module can only be considered if its can_verify_states overlaps with the source test's modifies_state (callback_request_creation). None of the candidates list callback_request or related states in their can_verify_states, so they cannot display or verify the created callback_request in the Support Center. They also do not run in the Support Center module and therefore cannot be used for cross_user observation as a support_agent.

---

### 4.ONA-001: Open a new Checking account with valid initial deposit

| Field | Value |
|-------|-------|
| Module | Open New Account |
| Workflow | Open Account |
| Test Type | positive |
| Priority | High |
| Coverage | full |
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
| 1 | Verify the newly opened Checking account appears in the Accounts Overview listing with type Checking, a masked accoun... | found | Existence | After Only | 3.ACCOVE-002 - Accounts table displays expected columns in each row | 85% |
| 2 | Verify funds were transferred from the selected funding source by confirming the funding account's available balance ... | found | Financial Delta | Before/After | 3.ACCOVE-003 - Footer displays the total balance across all accounts | 80% |
| 3 | Verify the new checking account's balance reflects the deposited amount (complements the funding account debit). | found | Existence | After Only | 3.ACCOVE-002 - Accounts table displays expected columns in each row | 80% |

#### Execution Plan

| Step | Phase | Action | Test ID | Purpose |
|------|-------|--------|---------|---------|
| 1 | action | execute_test | 4.ONA-001 | Execute the action: Open a new Checking account with valid initial deposit |
| 2 | navigate | navigate | - | Navigate to Accounts Overview |
| 3 | post_verify | execute_test | 3.ACCOVE-002 | Verify the newly opened Checking account appears in the Accounts Overview listing with type Check... |
| 4 | navigate | navigate | - | Navigate to Accounts Overview |
| 5 | post_verify | execute_test | 3.ACCOVE-002 | Verify the new checking account's balance reflects the deposited amount (complements the funding ... |

**Manual Verification Required:**
- Purpose: Verify funds were transferred from the selected funding source by confirming the funding account's available balance decreased by the initial deposit amount.
- Suggested Step: Verify in module 'Open New Account' — matcher chose 3.ACCOVE-003 in 'Accounts Overview' which is not the observer module.
- Reason: Module mismatch: matched test is in 'Accounts Overview', but verification should occur in 'Open New Account'.

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
| 1 | Verify the newly opened Savings account appears in the Accounts Overview listing with type Savings, a masked account ... | partial | Existence | After Only | 3.ACCOVE-002 - Accounts table displays expected columns in each row | 70% |
| 2 | Verify the funding source account was debited by the initial deposit amount used to open the Savings account. | found | Financial Delta | Before/After | 3.ACCOVE-003 - Footer displays the total balance across all accounts | 80% |
| 3 | Verify the new savings account's balance reflects the deposited amount (the created account shows the initial balance). | partial | Existence | After Only | 3.ACCOVE-003 - Footer displays the total balance across all accounts | 75% |

#### Coverage Gaps

- The candidate is in the correct module and exposes the required fields (account_list, masked_account_number, balance_display), but as written it only verifies column presence/visibility for all rows rather than locating and asserting the specific new Savings account and its exact initial balance. Because the execution_strategy is after_only, the test must by itself confirm the new record and expected balance — this test does not currently perform that confirmation.
- Candidate operates in the correct module and exposes balance_display, so it can observe the relevant data, but the test's current assertions focus on the footer total rather than confirming an individual account's balance matches the deposit amount. Therefore it cannot, as-is, confirm the expected result by itself.

#### Execution Plan

| Step | Phase | Action | Test ID | Purpose |
|------|-------|--------|---------|---------|
| 1 | action | execute_test | 4.ONA-002 | Execute the action: Open a new Savings account with valid initial deposit |
| 2 | navigate | navigate | - | Navigate to Accounts Overview |
| 3 | post_verify | execute_test_partial | 3.ACCOVE-002 | Verify the newly opened Savings account appears in the Accounts Overview listing with type Saving... |
| 4 | navigate | navigate | - | Navigate to Accounts Overview |
| 5 | post_verify | execute_test_partial | 3.ACCOVE-003 | Verify the new savings account's balance reflects the deposited amount (the created account shows... |

**Manual Verification Required:**
- Purpose: Verify the funding source account was debited by the initial deposit amount used to open the Savings account.
- Suggested Step: Verify in module 'Open New Account' — matcher chose 3.ACCOVE-003 in 'Accounts Overview' which is not the observer module.
- Reason: Module mismatch: matched test is in 'Accounts Overview', but verification should occur in 'Open New Account'.

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
| 1 | Verify the source account's balance decreased by the transfer amount. | found | Financial Delta | Before/After | 3.ACCOVE-003 - Footer displays the total balance across all accounts | 95% |
| 2 | Verify the destination internal account's balance increased by the transfer amount. | found | Financial Delta | Before/After | 3.ACCOVE-003 - Footer displays the total balance across all accounts | 95% |
| 3 | Verify a transfer record exists with the shown transaction ID in the Transfer Funds records/history. | partial | Existence | After Only | 5.TRAFUN-004 - Destination options update when changing transfer type | 30% |

#### Coverage Gaps

- All three candidate tests operate on the Transfer Funds page and their module action_states include 'funds_transfer' (they exercise the transfer action rather than observe history). Per the HARD MODULE RULE, a candidate whose action_states overlap the source test's modifies_state should not be marked 'found' because it performs the same action instead of verifying the result. None of the candidates open transfer history or a transfer-details view or search by transaction ID (they do not access/display the required transfer record or its transaction ID), so none fully satisfies the after_only verification requirement.

#### Execution Plan

| Step | Phase | Action | Test ID | Purpose |
|------|-------|--------|---------|---------|
| 1 | navigate | navigate | - | Navigate to Accounts Overview |
| 2 | pre_verify | execute_test | 3.ACCOVE-003 | Record source account available balance prior to transfer. |
| 3 | navigate | navigate | - | Navigate to Accounts Overview |
| 4 | pre_verify | execute_test | 3.ACCOVE-003 | Record destination account available balance prior to transfer. |
| 5 | navigate | navigate | - | Navigate to Transfer Funds |
| 6 | action | execute_test | 5.TRAFUN-001 | Execute the action: Successful internal transfer between own accounts |
| 7 | navigate | navigate | - | Navigate to Accounts Overview |
| 8 | post_verify | execute_test | 3.ACCOVE-003 | Record source account available balance after transfer and verify decrease equals transfer amount. |
| 9 | navigate | navigate | - | Navigate to Accounts Overview |
| 10 | post_verify | execute_test | 3.ACCOVE-003 | Record destination account available balance after transfer and verify increase equals transfer a... |
| 11 | post_verify | execute_test_partial | 5.TRAFUN-004 | Verify a transfer record exists with the shown transaction ID in the Transfer Funds records/history. |

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

| # | Ideal Verification | Status | Type | Strategy | Matched Test | Confidence |
|---|--------------------|--------|------|----------|--------------|------------|
| 1 | Verify the source account's balance decreased by the external transfer amount. | found | Financial Delta | Before/After | 3.ACCOVE-003 - Footer displays the total balance across all accounts | 93% |
| 2 | Verify an external transfer request/record was created for the provided destination account number (external transfer... | partial | Existence | After Only | 5.TRAFUN-004 - Destination options update when changing transfer type | 70% |

#### Coverage Gaps

- The candidate runs in the correct module and touches external transfer inputs, but it only validates UI input/option behavior rather than confirming persistence of a new external transfer record. Also its module action_states overlap the source modification (external_transfer_request), so it appears to be an action/form test rather than an observation of the resulting stored record.

#### Execution Plan

| Step | Phase | Action | Test ID | Purpose |
|------|-------|--------|---------|---------|
| 1 | navigate | navigate | - | Navigate to Accounts Overview |
| 2 | pre_verify | execute_test | 3.ACCOVE-003 | Record source account available balance prior to external transfer. |
| 3 | navigate | navigate | - | Navigate to Transfer Funds |
| 4 | action | execute_test | 5.TRAFUN-002 | Execute the action: Successful external transfer to matching account number |
| 5 | navigate | navigate | - | Navigate to Accounts Overview |
| 6 | post_verify | execute_test | 3.ACCOVE-003 | Record source account available balance after transfer and verify decrease equals transfer amount. |
| 7 | post_verify | execute_test_partial | 5.TRAFUN-004 | Verify an external transfer request/record was created for the provided destination account numbe... |

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
| 1 | Verify the source account's balance decreased by the payment amount after submitting the bill payment. | found | Financial Delta | Before/After | 3.ACCOVE-003 - Footer displays the total balance across all accounts | 95% |
| 2 | Verify a payment record with the referenced payment code exists and contains matching payee, amount, and source accou... | partial | Existence | After Only | 6.PAYMEN-004 - Submit payment when amount equals available funds (boundary) | 58% |

#### Coverage Gaps

- The candidate is in the correct module and exposes the relevant states (payment_reference, payee_details, account_balance), but it performs the same create action as the source test (overlapping action_states: bill_payment, account_balance). Per the hard module rule, a test that performs the action cannot be marked 'found' as the verification — we need a read-only/observational test that can confirm the payment record exists after the submit action.

#### Execution Plan

| Step | Phase | Action | Test ID | Purpose |
|------|-------|--------|---------|---------|
| 1 | navigate | navigate | - | Navigate to Accounts Overview |
| 2 | pre_verify | execute_test | 3.ACCOVE-003 | Record source account available balance prior to payment submission. |
| 3 | navigate | navigate | - | Navigate to Payments |
| 4 | action | execute_test | 6.PAYMEN-001 | Execute the action: Submit valid payment and verify reference code and balance update |
| 5 | navigate | navigate | - | Navigate to Accounts Overview |
| 6 | post_verify | execute_test | 3.ACCOVE-003 | Record source account available balance after payment and verify decrease equals payment amount. |
| 7 | post_verify | execute_test_partial | 6.PAYMEN-004 | Verify a payment record with the referenced payment code exists and contains matching payee, amou... |

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
| 1 | Verify a new Personal loan application/loan record exists and is recorded as approved/created in the Request Loan rec... | partial | Existence | After Only | 7.REQLOA-013 - Accept Personal loan request when Loan Amount equals the Personal minimum | 70% |
| 2 | Verify the selected collateral account reflects the collateral hold/reservation (related account shows hold or reserv... | partial | Cascading Update | Before/After | 3.ACCOVE-002 - Accounts table displays expected columns in each row | 60% |

#### Coverage Gaps

- The candidate test submits a Personal loan request (its action_states include loan_creation, collateral_hold, loan_status), so it performs the same state-changing action as the source test rather than observing the result. The execution_strategy is after_only and requires a test that can confirm the new record exists and shows type='Personal', approved/created status, and the chosen terms. The candidate can verify the required states but must be adapted to only read/display the loan record rather than creating one.
- The candidate is in the required Accounts Overview module and reads per-account Current Balance and status, but its listed verifiable states do not include a hold/reservation indicator or reserved_amount. Because the verification requires observing a hold/reserved indicator or reserved amount for the collateral account, this test alone is insufficient.

#### Execution Plan

| Step | Phase | Action | Test ID | Purpose |
|------|-------|--------|---------|---------|
| 1 | navigate | navigate | - | Navigate to Accounts Overview |
| 2 | pre_verify | execute_test_partial | 3.ACCOVE-002 | Record collateral account balance and any hold/reservation indicator prior to loan request. |
| 3 | navigate | navigate | - | Navigate to Request Loan |
| 4 | action | execute_test | 7.REQLOA-001 | Execute the action: Request a Personal loan with valid inputs |
| 5 | post_verify | execute_test_partial | 7.REQLOA-013 | Verify a new Personal loan application/loan record exists and is recorded as approved/created in ... |
| 6 | navigate | navigate | - | Navigate to Accounts Overview |
| 7 | post_verify | execute_test_partial | 3.ACCOVE-002 | Record collateral account balance and hold/reservation indicator after loan creation and verify t... |

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
| 1 | Verify a new Auto loan application/loan record exists and is recorded as approved/created in the Request Loan records... | partial | Existence | After Only | 7.REQLOA-009 - Reject Auto loan request when Loan Amount is above allowed maximum | 45% |
| 2 | Verify the selected collateral account reflects the collateral hold/reservation (related account shows hold or reserv... | partial | Cascading Update | Before/After | 3.ACCOVE-002 - Accounts table displays expected columns in each row | 55% |

#### Coverage Gaps

- Although this candidate touches the correct module and exposes the relevant state fields (loan_application_status, loan_terms), it is itself an action-oriented test that submits a loan request (and in this case expects rejection). Per the rules, tests whose action_states overlap the source's modifies_state cannot be marked 'found' because they perform the same action rather than observing the result. Also the expected outcome of 7.REQLOA-009 (validation error) is the opposite of the desired verification (an approved/created Auto loan record).
- The candidate operates in the required Accounts Overview module and exposes the Current Balance (needed for before/after recording) but its listed verifiable states do not include a hold/reservation indicator or reserved_amount. Because the verification strategy is before_after, the test can serve to capture balances but cannot by itself capture the hold/reservation state required to confirm collateral holds.

#### Execution Plan

| Step | Phase | Action | Test ID | Purpose |
|------|-------|--------|---------|---------|
| 1 | navigate | navigate | - | Navigate to Accounts Overview |
| 2 | pre_verify | execute_test_partial | 3.ACCOVE-002 | Record collateral account balance and any hold/reservation indicator prior to loan request. |
| 3 | navigate | navigate | - | Navigate to Request Loan |
| 4 | action | execute_test | 7.REQLOA-002 | Execute the action: Request an Auto loan with valid inputs |
| 5 | post_verify | execute_test_partial | 7.REQLOA-009 | Verify a new Auto loan application/loan record exists and is recorded as approved/created in the ... |
| 6 | navigate | navigate | - | Navigate to Accounts Overview |
| 7 | post_verify | execute_test_partial | 3.ACCOVE-002 | Record collateral account balance and hold/reservation indicator after loan creation and verify t... |

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
| 1 | Verify a new Home loan application/loan record exists and is recorded as approved/created in the Request Loan records... | partial | Existence | After Only | 7.REQLOA-014 - Accept Home loan request when Loan Amount equals the Home maximum | 65% |
| 2 | Verify the selected collateral account reflects the collateral hold/reservation (related account shows hold or reserv... | partial | Cascading Update | Before/After | 3.ACCOVE-002 - Accounts table displays expected columns in each row | 55% |

#### Coverage Gaps

- Candidate 7.REQLOA-014 is the most relevant (correct module and Home loan), but it is itself a create/action test (its action_states overlap the source test). Per the hard rule, an action-test cannot be marked as the observer-only verification. The other provided candidates are for other loan types or are also action tests and thus are not suitable.
- The candidate is in the required Accounts Overview module and exposes Current Balance and account row data, but its can_verify_states do not include a hold/reservation indicator or reserved amount. The verification requires observing a hold/reservation indicator or reserved amount on the collateral account, which this test does not explicitly access.

#### Execution Plan

| Step | Phase | Action | Test ID | Purpose |
|------|-------|--------|---------|---------|
| 1 | navigate | navigate | - | Navigate to Accounts Overview |
| 2 | pre_verify | execute_test_partial | 3.ACCOVE-002 | Record collateral account balance and any hold/reservation indicator prior to loan request. |
| 3 | navigate | navigate | - | Navigate to Request Loan |
| 4 | action | execute_test | 7.REQLOA-003 | Execute the action: Request a Home loan with valid inputs |
| 5 | post_verify | execute_test_partial | 7.REQLOA-014 | Verify a new Home loan application/loan record exists and is recorded as approved/created in the ... |
| 6 | navigate | navigate | - | Navigate to Accounts Overview |
| 7 | post_verify | execute_test_partial | 3.ACCOVE-002 | Record collateral account balance and hold/reservation indicator after loan creation and verify t... |

---

### 7.REQLOA-010: Verify no actual balance debits occur after loan creation

| Field | Value |
|-------|-------|
| Module | Request Loan |
| Workflow | Request Loan |
| Test Type | positive |
| Priority | Medium |
| Coverage | none |
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
| 1 | Verify that the collateral account's actual available balance remains unchanged after loan creation (no debit occurre... | not_found | Field Persistence | Before/After | - | - |

#### Verification Tests Needed

| # | Type | Strategy | Target Module | Observer | Suggested Test Title |
|---|------|----------|---------------|----------|----------------------|
| 1 | Field Persistence | Before/After | Accounts Overview | - | 1) Navigate to Accounts Overview while logged in as the loan requester. 2) Locate the collateral ... |

#### Coverage Gaps

- Hard Module Rule: the target module is Accounts Overview. A candidate from another module can only be used if its can_verify_states overlaps the source's modifies_state and it actually displays the required collateral account balance. Although some candidates mention account_balance, none run in Accounts Overview or explicitly expose the collateral_account available balance (or the sequence of immediate re-check, refresh, and re-login). Therefore they cannot serve as the before_after observation test for collateral_account.

#### Execution Plan

| Step | Phase | Action | Test ID | Purpose |
|------|-------|--------|---------|---------|
| 1 | action | execute_test | 7.REQLOA-010 | Execute the action: Verify no actual balance debits occur after loan creation |

**Manual Verification Required:**
- Purpose: Verify that the collateral account's actual available balance remains unchanged after loan creation (no debit occurred) and that the unchanged value persists after page refresh and re-login.
- Suggested Step: 1) Navigate to Accounts Overview while logged in as the loan requester. 2) Locate the collateral account and record its Available Balance (and Ledger Balance if shown). 3) Submit the loan request (execute 7.REQLOA-010). 4) Immediately return to Accounts Overview and record the collateral account Available Balance again. 5) Refresh the Accounts Overview page and record the Available Balance. 6) Log out and log back in, open Accounts Overview, and record the Available Balance. 7) Confirm all recorded Available Balance values are identical (no debit occurred).
- Reason: Hard Module Rule: the target module is Accounts Overview. A candidate from another module can only be used if its can_verify_states overlaps the source's modifies_state and it actually displays the required collateral account balance. Although some candidates mention account_balance, none run in Accounts Overview or explicitly expose the collateral_account available balance (or the sequence of immediate re-check, refresh, and re-login). Therefore they cannot serve as the before_after observation test for collateral_account.

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
| 1 | Verify the updated contact fields are saved and persist after refresh and after signing out and back in. | partial | Field Persistence | Before/After | 8.UCI-005 - Submit with multiple fields failing format validation | 60% |

#### Coverage Gaps

- The candidate is in the correct module and can access the required state (user_profile/contact_fields), but its defined steps perform an update (action_states overlap with the source modifies_state) rather than only observing the profile. The hard-module rule forbids marking such an action-test as a full match for an observation-only before_after verification.

#### Execution Plan

| Step | Phase | Action | Test ID | Purpose |
|------|-------|--------|---------|---------|
| 1 | pre_verify | execute_test_partial | 8.UCI-005 | Record current contact field values shown on the profile page prior to update. |
| 2 | action | execute_test | 8.UCI-001 | Execute the action: Update profile with all valid contact fields |
| 3 | post_verify | execute_test_partial | 8.UCI-005 | After update, refresh the page and re-open profile after logout/login; verify contact fields refl... |

---

### 9.MANCAR-001: Request a new Debit card with valid linked account and complete shipping address

| Field | Value |
|-------|-------|
| Module | Manage Cards |
| Workflow | Request Card |
| Test Type | positive |
| Priority | High |
| Coverage | partial |
| Modifies State | card_request_creation, card_status, card_control_update |

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
| 1 | Confirm a card-request ticket was created for the selected linked account by locating the new request in the Manage C... | partial | Existence | After Only | 9.MANCAR-015 - Submit with incomplete Shipping Address | 60% |
| 2 | Verify the provided shipping address was persisted for the created card request and remains correct after page refres... | partial | Field Persistence | After Only | 9.MANCAR-015 - Submit with incomplete Shipping Address | 62% |

#### Coverage Gaps

- The test is in the Manage Cards module and references card_request_status, but it is an action test that overlaps the source's action_states (card_request_creation) and expects request not to be submitted. It does not observe or display the Requests list or the tracking ID, so it cannot serve as an after-only verification of a successful request.
- Module matches and the candidate can access shipping_address, but its action_states overlap with the source test's modifies_state (it performs a card request submission). Per the HARD MODULE RULE, a candidate that performs the same action cannot be marked 'found' because it does not serve as a pure observer. Also, the candidate's expected outcome is a validation error for incomplete input — not a verification that a previously-created request persisted correct address data.

#### Execution Plan

| Step | Phase | Action | Test ID | Purpose |
|------|-------|--------|---------|---------|
| 1 | action | execute_test | 9.MANCAR-001 | Execute the action: Request a new Debit card with valid linked account and complete shipping address |
| 2 | post_verify | execute_test_partial | 9.MANCAR-015 | Confirm a card-request ticket was created for the selected linked account by locating the new req... |
| 3 | post_verify | execute_test_partial | 9.MANCAR-015 | Verify the provided shipping address was persisted for the created card request and remains corre... |

---

### 9.MANCAR-002: Request a new Credit card with valid linked account and complete shipping address

| Field | Value |
|-------|-------|
| Module | Manage Cards |
| Workflow | Request Card |
| Test Type | positive |
| Priority | High |
| Coverage | partial |
| Modifies State | card_request_creation, card_status, card_control_update |

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
| 1 | Confirm a card-request ticket was created for the selected linked account by locating the new request in the Manage C... | partial | Existence | After Only | 9.MANCAR-015 - Submit with incomplete Shipping Address | 65% |
| 2 | Verify the provided shipping address was persisted for the created card request and remains correct after page refres... | partial | Field Persistence | After Only | 9.MANCAR-015 - Submit with incomplete Shipping Address | 65% |

#### Coverage Gaps

- Same module and capable of verifying card_request_status and related fields, but the test currently performs a create action (card_request_creation) and expects failure — per the hard-module rule, a candidate whose action_states overlap the source's modifies_state cannot be marked 'found'. The test must be converted into a read/inspection test (no submit) to serve as a proper after-only verification.
- Same module (Manage Cards) and the test exposes shipping_address, but the candidate currently performs a create/submit action (card_request_creation overlaps the source modifies_state). Per the hard-module rule, a test that performs the same action cannot be marked as a verification-only test. Also the candidate verifies input validation for an incomplete address rather than persistence across refresh and re-login.

#### Execution Plan

| Step | Phase | Action | Test ID | Purpose |
|------|-------|--------|---------|---------|
| 1 | action | execute_test | 9.MANCAR-002 | Execute the action: Request a new Credit card with valid linked account and complete shipping add... |
| 2 | post_verify | execute_test_partial | 9.MANCAR-015 | Confirm a card-request ticket was created for the selected linked account by locating the new req... |
| 3 | post_verify | execute_test_partial | 9.MANCAR-015 | Verify the provided shipping address was persisted for the created card request and remains corre... |

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
| 1 | Record the selected card's spending limit before the update, submit the update, then verify the spending limit value ... | not_found | Field Persistence | Before/After | - | - |

#### Verification Tests Needed

| # | Type | Strategy | Target Module | Observer | Suggested Test Title |
|---|------|----------|---------------|----------|----------------------|
| 1 | Field Persistence | Before/After | Manage Cards | - | Automated or manual verification needed in Manage Cards: 1) Open Manage Cards, select the existin... |

#### Coverage Gaps

- All candidates are for other modules (Open New Account, Payments, Transfer Funds) and their can_verify_states do not include card_control_update or spending_limit. Per the Hard Module Rule, a candidate from a different module can only be considered if its verifiable states overlap the source's modified states — they do not.

#### Execution Plan

| Step | Phase | Action | Test ID | Purpose |
|------|-------|--------|---------|---------|
| 1 | action | execute_test | 9.MANCAR-003 | Execute the action: Update spending limit with a valid amount |

**Manual Verification Required:**
- Purpose: Record the selected card's spending limit before the update, submit the update, then verify the spending limit value changed to the new numeric amount and persists after refresh and re-login.
- Suggested Step: Automated or manual verification needed in Manage Cards: 1) Open Manage Cards, select the existing card and open its controls; record the current Spending Limit value. 2) Submit the Update Controls action with the new numeric limit (as in 9.MANCAR-003). 3) After update, reopen the card controls (or refresh), record the Spending Limit value. 4) Log out and log back in, reopen Manage Cards -> Existing Card controls, and record the Spending Limit again. Confirm the recorded post-update values equal the newly entered numeric amount and persist after refresh and re-login.
- Reason: All candidates are for other modules (Open New Account, Payments, Transfer Funds) and their can_verify_states do not include card_control_update or spending_limit. Per the Hard Module Rule, a candidate from a different module can only be considered if its verifiable states overlap the source's modified states — they do not.

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
| 1 | Record the card's status and available card-control actions before changing status, set Card Status to Frozen and sub... | partial | Status Transition | Before/After | 9.MANCAR-014 - Multiple simultaneous validation failures shown inline prevent update | 45% |

#### Coverage Gaps

- Right module and touches the required state fields (card_status and card_controls), but the candidate's steps perform the Update Controls action (overlaps with the source test's modifies_state). Per the rule, a test that performs the same action cannot be marked as a full verification — it must be an observer-only test.

#### Execution Plan

| Step | Phase | Action | Test ID | Purpose |
|------|-------|--------|---------|---------|
| 1 | pre_verify | execute_test_partial | 9.MANCAR-014 | Record current card status badge and available card-control buttons for the selected card before ... |
| 2 | action | execute_test | 9.MANCAR-004 | Execute the action: Freeze an active card by updating Card Status |
| 3 | post_verify | execute_test_partial | 9.MANCAR-014 | Record card status badge and available card-control buttons after update; expected badge = Frozen... |

---

### 9.MANCAR-006: Add a travel notice with valid dates and destination

| Field | Value |
|-------|-------|
| Module | Manage Cards |
| Workflow | Update Controls |
| Test Type | positive |
| Priority | Medium |
| Coverage | none |
| Modifies State | card_control_update |

#### Source Test Details

**Preconditions:** An existing card is selected and the Update Controls form is open.

**Steps:**
1. Fill all required fields (Select Existing Card, Card Status as desired) and fill Travel Notice with a valid start date, end date, and destination
2. Click "Update Controls"

**Expected Result:** "Card controls updated successfully." is displayed and the travel notice (dates and destination) is saved and shown in the controls.

#### Verification Mapping

| # | Ideal Verification | Status | Type | Strategy | Matched Test | Confidence |
|---|--------------------|--------|------|----------|--------------|------------|
| 1 | Record existing travel notice data (none or prior notices), submit the new travel notice with start/end dates and des... | not_found | Field Persistence | Before/After | - | - |

#### Verification Tests Needed

| # | Type | Strategy | Target Module | Observer | Suggested Test Title |
|---|------|----------|---------------|----------|----------------------|
| 1 | Field Persistence | Before/After | Manage Cards | - | Manual verification steps to implement/run as the before/after test: 1) Log in as the test user. ... |

#### Coverage Gaps

- Hard module rule: the target module is Manage Cards and the required state to verify is card_control_update. All provided candidates are from different modules and their can_verify_states do not overlap with card_control_update, so they cannot observe the travel notice entries. Therefore none can be marked as a match.

#### Execution Plan

| Step | Phase | Action | Test ID | Purpose |
|------|-------|--------|---------|---------|
| 1 | action | execute_test | 9.MANCAR-006 | Execute the action: Add a travel notice with valid dates and destination |

**Manual Verification Required:**
- Purpose: Record existing travel notice data (none or prior notices), submit the new travel notice with start/end dates and destination, then verify the travel notice entry appears in the card controls with the correct dates and destination and persists after refresh and re-login.
- Suggested Step: Manual verification steps to implement/run as the before/after test: 1) Log in as the test user. 2) Navigate to Manage Cards. 3) Select the card used in the update action and open its Controls/Manage Controls view. 4) Locate the Travel Notices section and record any existing entries (for each: start date, end date, destination) — this is the BEFORE snapshot. 5) After the source test runs (the Update Controls action), refresh the page, or log out and log back in, then re-open Manage Cards -> same card -> Controls. 6) Locate Travel Notices and record entries again — verify there is an entry with the submitted start date, end date, and destination, and that it persists after refresh and re-login.
- Reason: Hard module rule: the target module is Manage Cards and the required state to verify is card_control_update. All provided candidates are from different modules and their can_verify_states do not overlap with card_control_update, so they cannot observe the travel notice entries. Therefore none can be marked as a match.

---

### 9.MANCAR-007: Update controls without adding a travel notice (travel notice optional)

| Field | Value |
|-------|-------|
| Module | Manage Cards |
| Workflow | Update Controls |
| Test Type | positive |
| Priority | Medium |
| Coverage | none |
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
| 1 | Record the selected card's controls before update, submit Update Controls without travel notice fields filled, then v... | not_found | Field Persistence | Before/After | - | - |
| 2 | Verify explicitly that no travel notice record exists for the card after the update (travel notice optional and was l... | not_found | Absence | After Only | - | - |

#### Verification Tests Needed

| # | Type | Strategy | Target Module | Observer | Suggested Test Title |
|---|------|----------|---------------|----------|----------------------|
| 1 | Field Persistence | Before/After | Manage Cards | - | Manual verification steps to implement or run as an automated test:<br>1) Log into the system and na... |
| 2 | Absence | After Only | Manage Cards | - | After performing 9.MANCAR-007 (update controls leaving Travel Notice fields empty), verify manual... |

#### Coverage Gaps

- All candidate tests are for different modules and their can_verify_states (account_creation_status, transfer_status, payment_status, account_balance, etc.) do not overlap with the required modifies_state card_control_update. Per the HARD MODULE RULE, a candidate from another module can only be used if its can_verify_states overlap the target state; they do not. Therefore none are suitable.
- All provided candidates belong to other modules (Accounts Overview, Investments) and their can_verify_states do not include card_control_update. Per the Hard Module Rule, a candidate from a different module can only be considered if its can_verify_states overlaps with the source test's modifies_state (card_control_update). None do. Details: Test 3.ACCOVE-002 and 3.ACCOVE-007 are for Accounts Overview and verify account table fields (no card/travel-notice data). Test 10.INVEST-016 is for Investments and verifies plan start-date validation (no card/travel-notice data).

#### Execution Plan

| Step | Phase | Action | Test ID | Purpose |
|------|-------|--------|---------|---------|
| 1 | action | execute_test | 9.MANCAR-007 | Execute the action: Update controls without adding a travel notice (travel notice optional) |

**Manual Verification Required:**
- Purpose: Record the selected card's controls before update, submit Update Controls without travel notice fields filled, then verify the requested control changes (e.g., spending limit or status) persisted and no travel notice entry was created.
- Suggested Step: Manual verification steps to implement or run as an automated test:<br>1) Log into the system and navigate to Manage Cards.<br>2) Select the existing card to test and open its Controls/Update Controls view.<br>3) Record current values: Spending Limit, Card Status, and any Travel Notice entries (or absence thereof).<br>4) (This is the source action already run separately) Submit Update Controls with the desired changes (e.g., change spending limit or status) and leave all Travel Notice fields empty.<br>5) Refresh the page or log out and log back in, then re-open the same card's Controls view.<br>6) Record the Spending Limit, Card Status, and Travel Notice entries again.<br>7) Confirm the spending limit and/or status reflect the requested changes and persist after refresh/re-login, and confirm there is no travel notice entry present for the card.
- Reason: All candidate tests are for different modules and their can_verify_states (account_creation_status, transfer_status, payment_status, account_balance, etc.) do not overlap with the required modifies_state card_control_update. Per the HARD MODULE RULE, a candidate from another module can only be used if its can_verify_states overlap the target state; they do not. Therefore none are suitable.
- Purpose: Verify explicitly that no travel notice record exists for the card after the update (travel notice optional and was left empty).
- Suggested Step: After performing 9.MANCAR-007 (update controls leaving Travel Notice fields empty), verify manually in Manage Cards as follows:<br>1) Log into the application and navigate to Manage Cards.<br>2) Locate and select the same card used in the update (use the card identifier from the update step).<br>3) Open the card's Travel Notice section or Travel Notices list.<br>4) Inspect the list for any entries matching the update date range (or any entries at all).<br>5) Expected outcome: the Travel Notice section is empty or shows an explicit message such as 'No travel notices' and there are no entries covering the updated date range. If the UI displays entries, record their details for investigation.
- Reason: All provided candidates belong to other modules (Accounts Overview, Investments) and their can_verify_states do not include card_control_update. Per the Hard Module Rule, a candidate from a different module can only be considered if its can_verify_states overlaps with the source test's modifies_state (card_control_update). None do. Details: Test 3.ACCOVE-002 and 3.ACCOVE-007 are for Accounts Overview and verify account table fields (no card/travel-notice data). Test 10.INVEST-016 is for Investments and verifies plan start-date validation (no card/travel-notice data).

---

## Associated Verification Test Cases

These are matched test cases referenced by post-verification mappings.

| TC ID | Module | Title | Type | Priority | Expected Result |
|-------|--------|-------|------|----------|------------------|
| 1.LOGIN-008 | Login | After changing password the old password no longer works | standard | High | Login with the old password fails (authentication denied); login with the new password succeeds, confirming the old p... |
| 1.LOGIN-012 | Login | Page refresh on authenticated page retains logged-in state | standard | Medium | After refresh the user remains authenticated and the authenticated content (account details, user name, etc.) is stil... |
| 10.INVEST-007 | Investments | Portfolio snapshot displays current holdings and read-only values | positive | Medium | Portfolio snapshot shows current fund holdings, market value, and unrealised gain or loss and is presented as read-only. |
| 13.SUPCEN-010 | Support Center | Submit with Preferred Date set to the next business day (boundary) | edge_case | Medium | Request is accepted and a success message "Callback request submitted." is displayed; an email confirmation is sent. |
| 3.ACCOVE-001 | Accounts Overview | Welcome message shows the user's name | positive | High | Welcome message displays the user's name. |
| 3.ACCOVE-002 | Accounts Overview | Accounts table displays expected columns in each row | positive | High | Every row contains Account Number, Account Type, Current Balance, Account Status (Active badge), and Open Date. |
| 3.ACCOVE-003 | Accounts Overview | Footer displays the total balance across all accounts | positive | High | Footer total balance equals the sum of all Current Balance values shown in the table. |
| 4.ONA-011 | Open New Account | Real-time validation appears and clears for Initial Deposit field | edge_case | Medium | Validation messages for the Initial Deposit field appear in real-time when invalid input is entered and clear when co... |
| 5.TRAFUN-004 | Transfer Funds | Destination options update when changing transfer type | positive | Medium | Destination options change based on the selected transfer type. |
| 6.PAYMEN-004 | Payments | Submit payment when amount equals available funds (boundary) | edge_case | Low | Payment is executed successfully and the source account balance is updated to reflect the zero (or new) available bal... |
| 7.REQLOA-009 | Request Loan | Reject Auto loan request when Loan Amount is above allowed maximum | edge_case | High | Validation error indicating Loan Amount is outside the allowed Auto range. |
| 7.REQLOA-013 | Request Loan | Accept Personal loan request when Loan Amount equals the Personal minimum | edge_case | Medium | Loan request is processed and may be approved; amount is accepted as within allowed Personal range. |
| 7.REQLOA-014 | Request Loan | Accept Home loan request when Loan Amount equals the Home maximum | edge_case | Medium | Loan request is processed and may be approved; amount is accepted as within allowed Home range. |
| 8.UCI-005 | Update Contact Info | Submit with multiple fields failing format validation | edge_case | Low | Both invalid fields are highlighted and an inline error banner is displayed summarizing the failures. |
| 9.MANCAR-014 | Manage Cards | Multiple simultaneous validation failures shown inline prevent update | edge_case | Medium | Multiple inline validation errors are displayed, the form remains editable, and no changes are applied. |
| 9.MANCAR-015 | Manage Cards | Submit with incomplete Shipping Address | edge_case | Low | Validation error indicating the address is incomplete and the request is not submitted. |
