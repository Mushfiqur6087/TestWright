# Parabank

**Base URL:** 
**Generated:** 2026-04-18T20:46:44.594062

## Summary

| Metric | Count |
|--------|-------|
| **Total Tests** | 132 |

### By Type

| Type | Count |
|------|-------|
| Positive | 38 |
| Negative | 64 |
| Edge Case | 22 |
| Standard | 8 |

### By Priority

| Priority | Count |
|----------|-------|
| High | 50 |
| Medium | 70 |
| Low | 12 |

### Post-Verification Coverage

| Metric | Count |
|--------|-------|
| Tests Needing Verification | 27 |
| Full Coverage | 3 |
| Partial Coverage | 24 |
| No Coverage | 0 |
| Tests With Verification Gaps | 0 |
| Total Missing Verifications | 0 |

### Execution Plans

| Metric | Value |
|--------|-------|
| Total Plans | 27 |
| Automated Steps | 81 |
| Manual Steps | 1 |
| Automation Rate | 98.8% |
| Before/After Plans | 15 |
| After-Only Plans | 12 |
| Cross-User Plans | 0 |

---

## Test Cases

### Login

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 1.LOGIN-001 | Sign in with valid email and password | A registered user exists with a valid email and password | 1. Fill all required fields (Email/Username with a valid email address, Password with a valid password meeting complexity rules)<br>2. Click "Sign In" | User is redirected to the Accounts Overview page and the system flashes "Signed in successfully." | High |
| 1.LOGIN-002 | Sign in with valid username and password | A registered user exists with a username and password | 1. Fill all required fields (Email/Username with a valid username, Password with a valid password meeting complexity rules)<br>2. Click "Sign In" | User is redirected to the Accounts Overview page and the system flashes "Signed in successfully." | High |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 1.LOGIN-003 | Sign in with incorrect credentials shows error and clears password | A registered user exists | 1. Fill all required fields (Email/Username with a registered email or username, Password with an incorrect password)<br>2. Click "Sign In" | System shows the authentication error message, clears the password field, and allows another attempt. | High |
| 1.LOGIN-009 | Submit with all required fields empty | None | 1. Leave all required fields empty<br>2. Click "Sign In" | Validation errors shown for all required fields. | Medium |
| 1.LOGIN-010 | Submit with invalid email format | None | 1. Fill all required fields (Email/Username with an invalid email format, Password with a valid password)<br>2. Click "Sign In" | Validation error shown indicating invalid email format and sign-in is prevented. | Medium |
| 1.LOGIN-011 | Submit with password not meeting complexity requirements | None | 1. Fill all required fields (Email/Username with a valid email or username, Password that does not meet complexity requirements)<br>2. Click "Sign In" | Validation error shown indicating password does not meet complexity requirements and sign-in is prevented. | Medium |

#### Edge Case Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 1.LOGIN-014 | Sign in with password exactly at minimum length meeting complexity | A registered user exists with a password exactly at the minimum length meeting complexity | 1. Fill all required fields (Email/Username with a valid credential, Password exactly at the minimum length and including required character types)<br>2. Click "Sign In" | Authentication succeeds and the system flashes "Signed in successfully." with redirect to Accounts Overview. | Low |
| 1.LOGIN-015 | Submit with password one character below minimum length | None | 1. Fill all required fields (Email/Username with a valid credential, Password one character shorter than the required minimum)<br>2. Click "Sign In" | Validation error shown indicating the password does not meet the minimum length/complexity and sign-in is prevented. | Low |

#### Standard Quality Patterns

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 1.LOGIN-004 | Post-logout redirect to login when revisiting previous authenticated page | User account exists and user can log in | 1. Log in to the application using valid credentials<br>2. Navigate to a protected page (e.g., Accounts Overview) and note the page URL<br>3. Click the application's Logout control<br>4. Attempt to navigate to the noted protected page URL (paste into address bar or click a bookmarked link) | The application redirects to the login page (or shows the login form) instead of granting access to the protected content | High |
| 1.LOGIN-005 | Browser back button after logout does not show authenticated content | User is able to log in and reach an authenticated page | 1. Log in with valid credentials and navigate to an authenticated page (e.g., Accounts Overview)<br>2. Click Logout in the application<br>3. Press the browser Back button once or more to attempt to return to the previously viewed page | Browser does not display cached authenticated content; user is shown the login page or an explicit logged-out state (no account data visible) | High |
| 1.LOGIN-006 | Submitting a form after forced session expiry shows expiry notice or redirects to login | User can log in and access a multi-step form (e.g., Transfer Funds or Update Contact Info) | 1. Log in and open a multi-field form (e.g., start a Transfer Funds or Update Contact Info flow)<br>2. Simulate session expiry by clearing the site's session/authentication cookies from the browser developer tools or by waiting until the session timeout elapses<br>3. Attempt to submit the form after the session has been invalidated | The application prevents the action and either shows a session-expired message instructing the user to log in again or redirects the user to the login page before processing the submission | High |
| 1.LOGIN-007 | Password reset link expires and shows an error when used after expiry | Password reset functionality is available and reset links are time-limited | 1. On the login page request a password reset for a valid account and capture the reset link sent to the account email<br>2. Wait until the documented reset-link expiry window has passed (or use a test mailbox entry that is older than the expiry window)<br>3. Open the expired reset link in a browser and attempt to set a new password | The application rejects the expired reset link and displays an appropriate message indicating the link has expired or is invalid; it does not allow setting a new password using the expired token | High |
| 1.LOGIN-008 | After changing password the old password no longer works | User can log in and access the change-password flow | 1. Log in with the current credentials and perform a password change using the application's password change flow (provide current password, set a new password)<br>2. Log out from the application<br>3. Attempt to log in using the previous (old) password, then attempt to log in using the new password | Login with the old password fails (authentication denied); login with the new password succeeds, confirming the old password no longer authenticates | High |
| 1.LOGIN-012 | Page refresh on authenticated page retains logged-in state | User can log in and reach an authenticated page | 1. Log in with valid credentials and navigate to an authenticated page (e.g., Accounts Overview)<br>2. Click the browser Refresh/Reload button or press F5 to reload the page | After refresh the user remains authenticated and the authenticated content (account details, user name, etc.) is still visible without requiring a new login | Medium |
| 1.LOGIN-013 | Forgot-password displays clear error for an unregistered email | Tester has access to the Forgot Password form on the login page | 1. On the login page open the Forgot Password/Reset form<br>2. Enter an email address that is not registered in the application (e.g., noaccount@example.com) and submit the form | The application displays a clear, user-facing error indicating the email address is not registered (not a silent success or ambiguous message) | Medium |

---

### Register

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 2.REGIST-001 | Register successfully with valid required data | None | 1. Fill all required fields with valid values (First Name, Last Name, Street Address, City, State, ZIP Code (5-digit), Phone Number, Social Security Number, Username as a valid email, Password meeting length requirement, Confirm Password matching Password)<br>2. Click "Register" | Account created successfully; user is redirected to the login page and prompted to sign in. | High |
| 2.REGIST-002 | Register successfully using ZIP Code in 5+4 format | None | 1. Fill all required fields with valid values using a ZIP Code in 5+4 format (ZIP+4)<br>2. Click "Register" | Account created successfully and user is redirected to the login page. | Medium |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 2.REGIST-003 | Submit with all required fields empty | None | 1. Leave all required fields empty<br>2. Click "Register" | Validation errors shown for all required fields. | Medium |
| 2.REGIST-004 | Register with invalid email format for Username | None | 1. Fill all other required fields with valid values, enter an invalid email in the Username field<br>2. Click "Register" | Validation error displayed for Username indicating an invalid email format. | Medium |
| 2.REGIST-005 | Register with Password shorter than minimum length | None | 1. Fill all other required fields with valid values, enter a Password shorter than the minimum length and repeat the same short value in Confirm Password<br>2. Click "Register" | Validation error indicating the password does not meet the minimum length requirement. | Medium |
| 2.REGIST-006 | Register with mismatched Confirm Password | None | 1. Fill all required fields with valid values, enter a valid Password and enter a different value in Confirm Password<br>2. Click "Register" | Validation error indicating Confirm Password must match the Password field. | Medium |
| 2.REGIST-007 | Register with invalid ZIP Code format | None | 1. Fill all other required fields with valid values, enter a ZIP Code that does not match allowed formats<br>2. Click "Register" | Validation error shown for ZIP Code indicating the acceptable formats. | Medium |
| 2.REGIST-008 | Register with invalid Phone Number format | None | 1. Fill all other required fields with valid values, enter a Phone Number that does not conform to the required pattern<br>2. Click "Register" | Validation error shown for Phone Number indicating the required format. | Medium |
| 2.REGIST-009 | Register with invalid SSN format | None | 1. Fill all other required fields with valid values, enter an SSN that does not match the required pattern<br>2. Click "Register" | Validation error shown for SSN indicating the required format. | Medium |

#### Edge Case Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 2.REGIST-010 | Phone Number field auto-formats digits into required pattern | None | 1. Enter only digits into the Phone Number field (unformatted)<br>2. Move focus away from the Phone Number field | Phone Number is automatically formatted to the required pattern in the field. | Low |
| 2.REGIST-011 | SSN field auto-formats digits into required pattern | None | 1. Enter only digits into the Social Security Number field (unformatted)<br>2. Move focus away from the Social Security Number field | SSN is automatically formatted to the required pattern in the field. | Low |

---

### Accounts Overview

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 3.ACCOVE-001 | Welcome message shows the user's name | User is logged in and Accounts Overview page is visible. | 1. Locate the welcome message area on the Accounts Overview page<br>2. Verify the welcome message includes the logged-in user's name | Welcome message displays the user's name. | High |
| 3.ACCOVE-002 | Accounts table displays expected columns in each row | User is logged in and Accounts Overview page is visible. | 1. Locate the accounts table on the page<br>2. Verify each table row shows Account Number (clickable but not implemented yet), Account Type, Current Balance, Account Status (Active badge), and Open Date | Every row contains Account Number, Account Type, Current Balance, Account Status (Active badge), and Open Date. | High |
| 3.ACCOVE-003 | Footer displays the total balance across all accounts | User is logged in and Accounts Overview page is visible with at least one account row. | 1. Read the Current Balance value from each account row and compute their sum<br>2. Compare the computed sum to the footer row's displayed total balance | Footer total balance equals the sum of all Current Balance values shown in the table. | High |
| 3.ACCOVE-004 | Rows ordered by account creation date (earliest first) | User is logged in and Accounts Overview page is visible with multiple accounts having Open Dates. | 1. Inspect the Open Date values in the table rows from top to bottom<br>2. Verify the sequence of Open Date values is in ascending order (earliest first) | Table rows are ordered by account creation date with the earliest open date first. | High |
| 3.ACCOVE-006 | Account numbers are masked showing only last four digits | User is logged in and Accounts Overview page is visible. | 1. Locate the Account Number values in the table<br>2. Verify each Account Number is masked for security, displaying only the last four digits | All Account Number values are masked except for the last four digits (e.g., ****1234). | Medium |

#### Edge Case Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 3.ACCOVE-007 | Clicking Account Number shows no implemented navigation (Account Number is clickable but not implemented yet) | User is logged in and Accounts Overview page is visible. | 1. Click an Account Number value in any table row<br>2. Observe the page behavior after the click | Clicking the Account Number does not navigate away or perform an implemented action; the user remains on the Accounts Overview page or sees a not-implemented indication. | Medium |

#### Standard Quality Patterns

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 3.ACCOVE-005 | Direct URL access to protected page while logged out redirects to login | Tester is logged out (no active session) and has the direct URL for the Accounts Overview page | 1. Ensure the browser session is logged out (clear site cookies or use a fresh private window)<br>2. Enter the direct URL for the Accounts Overview page in the address bar and navigate to it | The application redirects to the login page (or displays the login form) instead of showing the Accounts Overview content | High |

---

### Open New Account

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 4.ONA-001 | Open a new Checking account with valid initial deposit | User is logged in and Open New Account page is open. | 1. Select Account type = Checking and fill all required fields (Initial Deposit Amount: valid amount above checking minimum, Funding Source Account: account with sufficient balance)<br>2. Click "Open Account" | "Account opened successfully!" is displayed and user is redirected to accounts overview; the new checking account appears in the accounts listing. | High |
| 4.ONA-002 | Open a new Savings account with valid initial deposit | User is logged in and Open New Account page is open. | 1. Select Account type = Savings and fill all required fields (Initial Deposit Amount: valid amount above savings minimum, Funding Source Account: account with sufficient balance)<br>2. Click "Open Account" | "Account opened successfully!" is displayed and user is redirected to accounts overview; the new savings account appears in the accounts listing. | High |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 4.ONA-003 | Submit with all required fields empty | User is logged in and Open New Account page is open. | 1. Leave all required fields empty<br>2. Click "Open Account" | Validation errors shown for all required fields. | Medium |
| 4.ONA-004 | Submit with Account type not selected | User is logged in and Open New Account page is open. | 1. Fill all other required fields (Initial Deposit Amount: valid amount, Funding Source Account: selected), leave Account type unselected<br>2. Click "Open Account" | Validation error indicating account type must be selected. | Medium |
| 4.ONA-005 | Submit with Initial Deposit Amount empty | User is logged in and Open New Account page is open. | 1. Fill all other required fields (select Account type, Funding Source Account), leave Initial Deposit Amount empty<br>2. Click "Open Account" | Validation error indicating Initial Deposit Amount is required and must be numeric. | Medium |
| 4.ONA-006 | Submit with Funding Source Account not selected | User is logged in and Open New Account page is open. | 1. Fill all other required fields (select Account type, Initial Deposit Amount: valid amount), leave Funding Source Account unselected<br>2. Click "Open Account" | Validation error indicating a funding source must be selected or that funding is insufficient. | Medium |
| 4.ONA-007 | Enter non-numeric Initial Deposit Amount | User is logged in and Open New Account page is open. | 1. Fill all required fields with valid selections except enter a non-numeric value into Initial Deposit Amount<br>2. Click "Open Account" | Real-time or submission validation error indicating Initial Deposit Amount must be numeric. | Medium |
| 4.ONA-008 | Initial Deposit below minimum for Checking | User is logged in and Open New Account page is open. | 1. Select Account type = Checking and fill all required fields (Initial Deposit Amount: amount below checking minimum, Funding Source Account: account with sufficient balance)<br>2. Click "Open Account" | Validation error indicating Initial Deposit Amount does not meet the checking minimum. | Medium |
| 4.ONA-009 | Initial Deposit below minimum for Savings | User is logged in and Open New Account page is open. | 1. Select Account type = Savings and fill all required fields (Initial Deposit Amount: amount below savings minimum, Funding Source Account: account with sufficient balance)<br>2. Click "Open Account" | Validation error indicating Initial Deposit Amount does not meet the savings minimum. | Medium |
| 4.ONA-010 | Funding Source Account has insufficient balance | User is logged in and Open New Account page is open. | 1. Fill all required fields with a valid deposit amount and select a Funding Source Account whose balance is less than the entered deposit<br>2. Click "Open Account" | Validation error indicating the selected funding source does not have sufficient balance. | Medium |

#### Edge Case Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 4.ONA-011 | Real-time validation appears and clears for Initial Deposit field | User is logged in and Open New Account page is open. | 1. Enter a non-numeric value into Initial Deposit Amount and observe validation feedback<br>2. Replace with a valid numeric amount meeting the applicable minimum and observe the validation feedback clears | Validation messages for the Initial Deposit field appear in real-time when invalid input is entered and clear when corrected without form submission. | Medium |
| 4.ONA-012 | Open Checking account with deposit equal to minimum | User is logged in and Open New Account page is open. | 1. Select Account type = Checking and fill all required fields (Initial Deposit Amount: amount equal to checking minimum, Funding Source Account: account with sufficient balance)<br>2. Click "Open Account" | "Account opened successfully!" is displayed and user is redirected to accounts overview; the new checking account appears in the accounts listing. | Low |
| 4.ONA-013 | Open Savings account with deposit equal to minimum | User is logged in and Open New Account page is open. | 1. Select Account type = Savings and fill all required fields (Initial Deposit Amount: amount equal to savings minimum, Funding Source Account: account with sufficient balance)<br>2. Click "Open Account" | "Account opened successfully!" is displayed and user is redirected to accounts overview; the new savings account appears in the accounts listing. | Low |

---

### Transfer Funds

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 5.TRAFUN-001 | Successful internal transfer between own accounts | User is logged in, Transfer Funds page is open, and user has at least two own accounts (Checking or Savings) with sufficient balance | 1. Select the radio button for internal transfer (My ParaBank Account)<br>2. Fill all required fields (select Source Account from the Source Account dropdown, select Destination internal account from the destination options, enter a valid Transfer Amount within available balance)<br>3. Click the "Transfer" or "Submit" button | Confirmation message "Transfer completed successfully." is displayed and a transaction ID is shown for the transfer. | High |
| 5.TRAFUN-002 | Successful external transfer to matching account number | User is logged in, Transfer Funds page is open, and user has a Checking or Savings account with sufficient balance | 1. Select the radio button for external transfer (External Account)<br>2. Fill all required fields (select Source Account from the Source Account dropdown, enter Destination Account Number, enter Confirm Account Number matching the Destination Account Number, enter a valid Transfer Amount within available balance)<br>3. Click the "Transfer" or "Submit" button | Confirmation message "Transfer completed successfully." is displayed and a transaction ID is shown for the transfer. | High |
| 5.TRAFUN-004 | Destination options update when changing transfer type | User is logged in and Transfer Funds page is open | 1. Select the radio button for internal transfer (My ParaBank Account)<br>2. Verify destination shows selectable own accounts<br>3. Select the radio button for external transfer (External Account)<br>4. Verify destination changes to input fields for account number and confirm account number | Destination options change based on the selected transfer type. | Medium |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 5.TRAFUN-003 | Transfer fails when insufficient funds | User is logged in, Transfer Funds page is open, and Source Account has a known available balance | 1. Select appropriate transfer type and fill all required fields (select Source Account, select or enter Destination, enter a Transfer Amount greater than the Source Account available balance)<br>2. Click the "Transfer" or "Submit" button | A contextual error indicating insufficient funds is displayed and the transfer is not completed. | High |
| 5.TRAFUN-005 | Submit with all required fields empty | User is logged in and Transfer Funds page is open | 1. Leave all required fields empty<br>2. Click the "Transfer" or "Submit" button | Validation errors shown for all required fields. | Medium |
| 5.TRAFUN-006 | External transfer fails when account numbers do not match | User is logged in and Transfer Funds page is open | 1. Select the radio button for external transfer (External Account)<br>2. Fill all required fields (select Source Account, enter Destination Account Number, enter a non-matching Confirm Account Number, enter a valid Transfer Amount)<br>3. Click the "Transfer" or "Submit" button | Validation error displayed stating that the account numbers do not match and the transfer is not processed. | Medium |

#### Edge Case Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 5.TRAFUN-007 | Source Account dropdown shows only Checking and Savings accounts | User is logged in, Transfer Funds page is open, and user has multiple account types including Checking or Savings and at least one non-checking/savings account | 1. Open the Source Account dropdown on the Transfer Funds page<br>2. Inspect the list of accounts presented in the dropdown | The Source Account dropdown lists only Checking and Savings accounts for selection. | Medium |
| 5.TRAFUN-008 | Reject transfer when transfer amount format is invalid | User is logged in and Transfer Funds page is open | 1. Select appropriate transfer type and fill all other required fields correctly (select Source Account, select or enter Destination, enter an invalid-format value into the Transfer Amount field)<br>2. Click the "Transfer" or "Submit" button | Validation error shown for the Transfer Amount field indicating invalid amount format and the transfer is blocked. | Medium |

---

### Payments

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 6.PAYMEN-001 | Submit valid payment and verify reference code and balance update | User is logged in and the Submit Payment form is open | 1. Fill all required fields (Payee Name, Street Address, City, State, ZIP Code, Phone Number, Payee Account Number, Confirm Account Number) with matching valid values and a valid payee contact<br>2. Fill Payment Amount with an amount less than the selected source account's available balance and select a Source Account from the dropdown<br>3. Click "Pay" | Payment submitted successfully and a reference code is displayed; the source account balance is reduced accordingly and updated on the page. | High |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 6.PAYMEN-002 | Fail submission when payee account numbers do not match | User is logged in and the Submit Payment form is open | 1. Fill all required fields (Payee Name, Street Address, City, State, ZIP Code, Phone Number, Payee Account Number, Confirm Account Number) with valid values but enter non-matching values for Payee Account Number and Confirm Account Number<br>2. Fill Payment Amount with an amount less than the selected source account's available balance and select a Source Account<br>3. Click "Pay" | Inline error indicating the account numbers do not match is displayed and the form remains editable for correction. | High |
| 6.PAYMEN-003 | Submit with all required fields empty | User is logged in and the Submit Payment form is open | 1. Leave all required fields empty<br>2. Click "Pay" | Validation errors shown for all required fields. | Medium |

#### Edge Case Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 6.PAYMEN-004 | Submit payment when amount equals available funds (boundary) | User is logged in and the Submit Payment form is open with knowledge of the source account's available balance | 1. Fill all required fields (Payee Name, Street Address, City, State, ZIP Code, Phone Number, Payee Account Number, Confirm Account Number) with matching valid values<br>2. Fill Payment Amount to exactly match the selected source account's available balance and select that Source Account<br>3. Click "Pay" | Payment is executed successfully and the source account balance is updated to reflect the zero (or new) available balance after the transaction. | Low |

---

### Request Loan

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 7.REQLOA-001 | Request a Personal loan with valid inputs | User is signed in and Request Loan page is open. | 1. Select Loan Type = Personal and fill all required fields (Loan Amount within personal range, Down Payment at or above minimum percentage but less than Loan Amount, select Collateral Account with sufficient funds, choose Interest rate)<br>2. Click "Submit Loan Request" | "Loan approved and created successfully!" message is displayed and the new loan account details are shown. | High |
| 7.REQLOA-002 | Request an Auto loan with valid inputs | User is signed in and Request Loan page is open. | 1. Select Loan Type = Auto and fill all required fields (Loan Amount within auto range, Down Payment at or above minimum percentage but less than Loan Amount, select Collateral Account with sufficient funds, choose Interest rate)<br>2. Click "Submit Loan Request" | "Loan approved and created successfully!" message is displayed and the new loan account details are shown. | High |
| 7.REQLOA-003 | Request a Home loan with valid inputs | User is signed in and Request Loan page is open. | 1. Select Loan Type = Home and fill all required fields (Loan Amount within home range, Down Payment at or above minimum percentage but less than Loan Amount, select Collateral Account with sufficient funds, choose Interest rate)<br>2. Click "Submit Loan Request" | "Loan approved and created successfully!" message is displayed and the new loan account details are shown. | High |
| 7.REQLOA-010 | Verify no actual balance debits occur after loan creation | User is signed in, Request Loan page is open, and a valid loan request is ready to submit. | 1. Fill all required fields with valid values and note the displayed Collateral Account balance<br>2. Click "Submit Loan Request" | Loan is created and the collateral account balance remains unchanged (no actual balance debits occur). | Medium |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 7.REQLOA-004 | Reject request when Down Payment is equal to or greater than Loan Amount | User is signed in and Request Loan page is open. | 1. Select a Loan Type and fill all other required fields, set Down Payment equal to or greater than the Loan Amount<br>2. Click "Submit Loan Request" | Validation error indicating Down Payment must be less than Loan Amount. | High |
| 7.REQLOA-005 | Reject request when Down Payment is below minimum percentage | User is signed in and Request Loan page is open. | 1. Select a Loan Type and fill all other required fields, set Down Payment below the minimum required percentage<br>2. Click "Submit Loan Request" | Validation error indicating Down Payment does not meet the minimum percentage requirement. | High |
| 7.REQLOA-006 | Deny loan when collateral value is inadequate relative to loan | User is signed in and Request Loan page is open. | 1. Select a Loan Type and fill all required fields, choose a Collateral Account whose available value results in collateral value below required threshold<br>2. Click "Submit Loan Request" | Loan denial with message indicating inadequate collateral value. | High |
| 7.REQLOA-007 | Reject request when selected Collateral Account lacks sufficient funds | User is signed in and Request Loan page is open. | 1. Select a Loan Type and fill all other required fields, select Collateral Account with insufficient funds for the required collateral percentage<br>2. Click "Submit Loan Request" | Validation error or denial indicating insufficient collateral funds. | High |
| 7.REQLOA-011 | Submit with all required fields empty | Request Loan page is open. | 1. Leave all required fields empty<br>2. Click "Submit Loan Request" | Validation errors shown for all required fields. | Medium |
| 7.REQLOA-012 | Handle credit engine denial (Insufficient credit history) for an otherwise valid request | User is signed in and Request Loan page is open. | 1. Fill all required fields with valid values that otherwise meet collateral and down payment rules<br>2. Click "Submit Loan Request" | Loan denial with a specific reason such as "Insufficient credit history" displayed. | Medium |

#### Edge Case Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 7.REQLOA-008 | Reject Personal loan request when Loan Amount is below allowed minimum | User is signed in and Request Loan page is open. | 1. Select Loan Type = Personal and fill all other required fields, set Loan Amount below the Personal minimum<br>2. Click "Submit Loan Request" | Validation error indicating Loan Amount is outside the allowed Personal range. | High |
| 7.REQLOA-009 | Reject Auto loan request when Loan Amount is above allowed maximum | User is signed in and Request Loan page is open. | 1. Select Loan Type = Auto and fill all other required fields, set Loan Amount above the Auto maximum<br>2. Click "Submit Loan Request" | Validation error indicating Loan Amount is outside the allowed Auto range. | High |
| 7.REQLOA-013 | Accept Personal loan request when Loan Amount equals the Personal minimum | User is signed in and Request Loan page is open. | 1. Select Loan Type = Personal and fill all required fields, set Loan Amount exactly at the Personal minimum and set Down Payment to a valid percentage<br>2. Click "Submit Loan Request" | Loan request is processed and may be approved; amount is accepted as within allowed Personal range. | Medium |
| 7.REQLOA-014 | Accept Home loan request when Loan Amount equals the Home maximum | User is signed in and Request Loan page is open. | 1. Select Loan Type = Home and fill all required fields, set Loan Amount exactly at the Home maximum and set Down Payment to a valid percentage<br>2. Click "Submit Loan Request" | Loan request is processed and may be approved; amount is accepted as within allowed Home range. | Medium |

---

### Update Contact Info

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 8.UCI-001 | Update profile with all valid contact fields | User is logged in and Update Contact Info page is open. | 1. Fill all required fields (First Name, Last Name, Street Address, City, State, ZIP Code, Phone Number) with valid values<br>2. Click "Update Profile" | Profile updated successfully and the displayed contact fields are refreshed to show the new values. | High |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 8.UCI-002 | Submit with all required fields empty | User is logged in and Update Contact Info page is open. | 1. Leave all required fields empty<br>2. Click "Update Profile" | Validation errors shown for all required fields and invalid fields are highlighted. | Medium |
| 8.UCI-003 | Submit with invalid ZIP Code format | User is logged in and Update Contact Info page is open. | 1. Fill all required fields with valid values except enter an invalid format in ZIP Code<br>2. Click "Update Profile" | ZIP Code field is highlighted and an inline error banner is displayed indicating format validation failure. | Medium |
| 8.UCI-004 | Submit with invalid Phone Number format | User is logged in and Update Contact Info page is open. | 1. Fill all required fields with valid values except enter an invalid format in Phone Number<br>2. Click "Update Profile" | Phone Number field is highlighted and an inline error banner is displayed indicating format validation failure. | Medium |

#### Edge Case Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 8.UCI-005 | Submit with multiple fields failing format validation | User is logged in and Update Contact Info page is open. | 1. Fill all required fields, but enter invalid formats for ZIP Code and Phone Number<br>2. Click "Update Profile" | Both invalid fields are highlighted and an inline error banner is displayed summarizing the failures. | Low |

---

### Manage Cards

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 9.MANCAR-001 | Request a new Debit card with valid linked account and complete shipping address | User is authenticated and the Request Card form is visible | 1. Select Card Type as Debit<br>2. Select a linked account in good standing<br>3. Fill the complete Shipping Address<br>4. Click "Request Card" | A card-request ticket is opened and the UI shows "Card request submitted successfully." with a tracking ID | High |
| 9.MANCAR-002 | Request a new Credit card with valid linked account and complete shipping address | User is authenticated and the Request Card form is visible | 1. Select Card Type as Credit<br>2. Select a linked account in good standing<br>3. Fill the complete Shipping Address<br>4. Click "Request Card" | A card-request ticket is opened and the UI shows "Card request submitted successfully." with a tracking ID | High |
| 9.MANCAR-003 | Update spending limit with a valid amount | An existing card is selected and the Update Controls form is open. | 1. Fill all required fields (Select Existing Card, New Spending Limit with a valid numeric amount, Card Status as desired) and leave Travel Notice empty<br>2. Click "Update Controls" | "Card controls updated successfully." is displayed and the spending limit shown in the controls reflects the new amount. | High |
| 9.MANCAR-004 | Freeze an active card by updating Card Status | An existing card currently in Active status is selected and the Update Controls form is open. | 1. Select Frozen in Card Status and fill all other required fields (Select Existing Card, any required numeric fields)<br>2. Click "Update Controls" | "Card controls updated successfully." is displayed and the card status updates to Frozen. | High |
| 9.MANCAR-006 | Add a travel notice with valid dates and destination | An existing card is selected and the Update Controls form is open. | 1. Fill all required fields (Select Existing Card, Card Status as desired) and fill Travel Notice with a valid start date, end date, and destination<br>2. Click "Update Controls" | "Card controls updated successfully." is displayed and the travel notice (dates and destination) is saved and shown in the controls. | Medium |
| 9.MANCAR-007 | Update controls without adding a travel notice (travel notice optional) | An existing card is selected and the Update Controls form is open. | 1. Fill all required fields (Select Existing Card, New Spending Limit or leave unchanged, Card Status as desired) and leave all Travel Notice fields empty<br>2. Click "Update Controls" | "Card controls updated successfully." is displayed and the update succeeds without a travel notice. | Medium |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 9.MANCAR-005 | Reject spending limit above allowed policy | The Update Controls form is open and an existing card is selected. | 1. Fill all required fields (Select Existing Card, New Spending Limit with an amount above the allowed policy, Card Status as desired)<br>2. Click "Update Controls" | Inline validation error indicates the spending limit exceeds policy and the form remains editable; update is not applied. | High |
| 9.MANCAR-008 | Submit with all required fields empty | User is authenticated and the Request Card form is visible | 1. Leave all required fields empty<br>2. Click "Request Card" | Validation errors shown for all required fields and the request is not submitted. | Medium |
| 9.MANCAR-009 | Submit with Shipping Address empty | User is authenticated and the Request Card form is visible | 1. Select a Card Type and select a linked account in good standing, leave Shipping Address empty<br>2. Click "Request Card" | Validation error indicating the Shipping Address is required and the request is not submitted. | Medium |
| 9.MANCAR-010 | Attempt to request a card using an account not in good standing | User is authenticated and the Request Card form is visible | 1. Select a Card Type<br>2. Select a linked account that is not in good standing<br>3. Fill the complete Shipping Address<br>4. Click "Request Card" | The system blocks submission and shows an error indicating the selected account is ineligible; no card-request ticket is opened. | Medium |
| 9.MANCAR-011 | Submit with all required fields empty | The Update Controls form is open. | 1. Leave all required fields empty<br>2. Click "Update Controls" | Validation errors are shown inline for required fields and the form remains editable. | Medium |
| 9.MANCAR-012 | Reject non-numeric spending limit value | The Update Controls form is open and an existing card is selected. | 1. Fill all required fields (Select Existing Card, New Spending Limit with a non-numeric value, Card Status as desired)<br>2. Click "Update Controls" | Inline validation error indicates the spending limit must be numeric and the form remains editable. | Medium |
| 9.MANCAR-013 | Reject travel notice with end date before start date | The Update Controls form is open and an existing card is selected. | 1. Fill all required fields (Select Existing Card, Card Status as desired) and enter a Travel Notice with an end date earlier than the start date<br>2. Click "Update Controls" | Inline validation error indicates the date range is invalid and the form remains editable; travel notice is not saved. | Medium |

#### Edge Case Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 9.MANCAR-014 | Multiple simultaneous validation failures shown inline prevent update | The Update Controls form is open and an existing card is selected. | 1. Fill all required fields (Select Existing Card), set New Spending Limit above policy, and enter a Travel Notice with an invalid date range<br>2. Click "Update Controls" | Multiple inline validation errors are displayed, the form remains editable, and no changes are applied. | Medium |
| 9.MANCAR-015 | Submit with incomplete Shipping Address | User is authenticated and the Request Card form is visible | 1. Select a Card Type and select a linked account in good standing<br>2. Fill the Shipping Address with incomplete details<br>3. Click "Request Card" | Validation error indicating the address is incomplete and the request is not submitted. | Low |

---

### Investments

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 10.INVEST-001 | Execute a Buy trade successfully and update holdings | User is logged in and Execute Trade form is visible; customer has sufficient buying power. | 1. Fill all required fields (Action set to Buy, Fund Symbol selected via autocomplete, Quantity with a valid positive amount, Funding Account selected)<br>2. Click "Execute Trade"<br>3. Verify confirmation area displays success message and order details | A same-day trade is executed; confirmation displays "Trade executed successfully." with an order ID and portfolio holdings are updated. | High |
| 10.INVEST-002 | Execute a Sell trade successfully and update holdings | User is logged in and Execute Trade form is visible; customer holds sufficient shares of the selected fund. | 1. Fill all required fields (Action set to Sell, Fund Symbol selected via autocomplete, Quantity within held shares, Destination Account selected)<br>2. Click "Execute Trade"<br>3. Verify confirmation area displays success message and order details | A same-day trade is executed; confirmation displays "Trade executed successfully." with an order ID and portfolio holdings are updated. | High |
| 10.INVEST-003 | Create recurring investment plan with Weekly frequency | User is logged in and the Create Plan form is open. | 1. Fill all required fields (Fund Symbol, Contribution Amount, Frequency, Start Date, Funding Account) with valid values and select Weekly frequency<br>2. Click "Create Plan" | Plan created successfully. The schedule is stored and a confirmation message "Plan created successfully." is shown. | High |
| 10.INVEST-004 | Create recurring investment plan with Monthly frequency | User is logged in and the Create Plan form is open. | 1. Fill all required fields (Fund Symbol, Contribution Amount, Frequency, Start Date, Funding Account) with valid values and select Monthly frequency<br>2. Click "Create Plan" | Plan created successfully. The schedule is stored and a confirmation message "Plan created successfully." is shown. | High |
| 10.INVEST-007 | Portfolio snapshot displays current holdings and read-only values | User is logged in and the Execute Trade page is visible. | 1. Observe the portfolio snapshot panel<br>2. Verify it shows current fund holdings, market value, and unrealised gain or loss and that no editable inputs are present within the snapshot | Portfolio snapshot shows current fund holdings, market value, and unrealised gain or loss and is presented as read-only. | Medium |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 10.INVEST-005 | Buy blocked when customer lacks sufficient buying power | User is logged in and Execute Trade form is visible; customer does not have sufficient buying power for the requested buy amount. | 1. Fill all required fields for a Buy (select Fund Symbol, set Quantity that exceeds buying power, select Funding Account)<br>2. Click "Execute Trade" | An inline error prevents the trade and indicates insufficient buying power; no trade is executed. | High |
| 10.INVEST-006 | Sell blocked when customer lacks sufficient share balance | User is logged in and Execute Trade form is visible; customer does not hold enough shares of the selected fund. | 1. Fill all required fields for a Sell (select Fund Symbol, set Quantity exceeding held shares, select Destination Account)<br>2. Click "Execute Trade" | An inline error prevents the trade and indicates insufficient share balance; no trade is executed. | High |
| 10.INVEST-008 | Submit with all required fields empty | User is logged in and Execute Trade form is visible. | 1. Leave all required fields empty<br>2. Click "Execute Trade" | Validation errors shown for all required fields. | Medium |
| 10.INVEST-009 | Attempt execute with a non-existent fund symbol | User is logged in and Execute Trade form is visible. | 1. Fill all other required fields with valid values, enter a fund symbol that does not exist in the autocomplete<br>2. Click "Execute Trade" | An inline validation error indicates the fund symbol is invalid and the trade is not executed. | Medium |
| 10.INVEST-010 | Attempt execute with zero or negative quantity | User is logged in and Execute Trade form is visible. | 1. Fill all other required fields with valid values, set Quantity to zero or a negative number<br>2. Click "Execute Trade" | An inline validation error indicates quantity must be greater than zero and the trade is not executed. | Medium |
| 10.INVEST-011 | Submit with all required fields empty | User is logged in and the Create Plan form is open. | 1. Leave all required fields empty<br>2. Click "Create Plan" | Validation errors shown for all required fields; problematic fields are highlighted. | Medium |
| 10.INVEST-012 | Submit with Start Date in the past | User is logged in and the Create Plan form is open. | 1. Fill all required fields with valid values except set Start Date to a past date<br>2. Click "Create Plan" | Validation error displayed indicating invalid Start Date and the Start Date field is highlighted. | Medium |
| 10.INVEST-013 | Submit with Contribution Amount below minimum | User is logged in and the Create Plan form is open. | 1. Fill all required fields with valid values but set Contribution Amount below the required minimum<br>2. Click "Create Plan" | Validation error shown for Contribution Amount and the field is highlighted. | Medium |
| 10.INVEST-014 | Submit with Funding Account lacking sufficient balance | User is logged in and the Create Plan form is open. | 1. Fill all required fields with valid values but select a Funding Account with insufficient balance<br>2. Click "Create Plan" | Validation error indicating insufficient funds and the Funding Account field is highlighted. | Medium |

#### Edge Case Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 10.INVEST-015 | Portfolio snapshot enforces read-only behavior when interacting with holdings | User is logged in and the Execute Trade page is visible. | 1. Attempt to edit a value or field within the portfolio snapshot panel (e.g., click to enter edit mode or type into a displayed holding)<br>2. Observe the UI behavior | The portfolio snapshot cannot be edited and no changes are accepted in the snapshot panel. | Low |
| 10.INVEST-016 | Submit with Start Date set to today (not a future date) | User is logged in and the Create Plan form is open. | 1. Fill all required fields with valid values but set Start Date to today's date<br>2. Click "Create Plan" | Validation error displayed stating the Start Date must be in the future and the Start Date field is highlighted. | Low |

---

### Account Statements

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 11.ACCSTA-001 | Generate statement using month-and-year period | User is signed in and on the Account Statements page with the form visible. | 1. Select Statement Period as a month-and-year<br>2. Select Account from the Account dropdown<br>3. Click "Generate Statement" | Displays 'Statement generated successfully.' and the generated statement shows the retrieved transactions for the selected month. | High |
| 11.ACCSTA-002 | Generate statement using custom date range | User is signed in and on the Account Statements page with the form visible. | 1. Select Statement Period as custom date range and enter a valid start date and end date<br>2. Select Account from the Account dropdown<br>3. Click "Generate Statement" | Displays 'Statement generated successfully.' and the generated statement shows the retrieved transactions for the specified date range. | High |
| 11.ACCSTA-003 | Save e-Statement preference with a valid email | User is signed in and on the Account Statements page. | 1. Check the paperless statements checkbox and fill a valid email address in the Email Address field<br>2. Click "Save Preference" | Displays 'e-Statement preference updated.' and the paperless preference is saved (checkbox remains selected and the entered email is shown). | High |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 11.ACCSTA-004 | Submit with all required fields empty | User is signed in and on the Account Statements page with the form visible. | 1. Leave all required fields empty<br>2. Click "Generate Statement" | Validation errors shown for all required fields. | Medium |
| 11.ACCSTA-005 | Failing generation shows failure message | User is signed in and on the Account Statements page with the form visible. | 1. Fill Statement Period with a valid month-or-date-range and select an Account<br>2. Click "Generate Statement" | Shows 'Unable to generate statement — please try again later.' when generation fails. | Medium |
| 11.ACCSTA-006 | Prevent generation when custom start date is after end date | User is signed in and on the Account Statements page with the form visible. | 1. Select Statement Period as custom date range and enter a start date that is after the end date<br>2. Select Account from the Account dropdown<br>3. Click "Generate Statement" | Validation error shown indicating the date range is invalid and statement is not generated. | Medium |
| 11.ACCSTA-007 | Submit with all required fields empty | User is signed in and on the Account Statements page. | 1. Leave all required fields empty<br>2. Click "Save Preference" | Validation errors shown for all required fields. | Medium |
| 11.ACCSTA-008 | Save preference with invalid email format | User is signed in and on the Account Statements page. | 1. Check the paperless statements checkbox and fill an invalid email address in the Email Address field<br>2. Click "Save Preference" | Email field is highlighted with guidance and the preference is not saved. | Medium |

---

### Security Settings

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 12.SECSET-001 | Change password with valid current and strong matching new password | User is authenticated and Security Settings > Change Password panel is open | 1. Expand the Change Password panel if collapsed<br>2. Fill all required fields (Current Password: valid current password, New Password: valid strong password, Confirm New Password: same as New Password)<br>3. Click "Change Password" | Password changed successfully and credentials are updated. | High |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 12.SECSET-002 | Reject change when current password is incorrect | User is authenticated and Security Settings > Change Password panel is open | 1. Fill all required fields (Current Password: incorrect value, New Password: valid strong password, Confirm New Password: same as New Password)<br>2. Click "Change Password" | Validation error indicates the current password is incorrect and credentials are not updated. | High |
| 12.SECSET-003 | Submit with all required fields empty | User is authenticated and Security Settings > Change Password panel is open | 1. Leave all required fields empty<br>2. Click "Change Password" | Validation errors shown for all required fields. | Medium |
| 12.SECSET-004 | Reject change when New Password and Confirm New Password do not match | User is authenticated and Security Settings > Change Password panel is open | 1. Fill all required fields (Current Password: valid current password, New Password: valid strong password, Confirm New Password: different value)<br>2. Click "Change Password" | Validation error indicating New Password and Confirm New Password must match. | Medium |
| 12.SECSET-005 | Reject weak new password that does not meet strength policy | User is authenticated and Security Settings > Change Password panel is open | 1. Fill all required fields (Current Password: valid current password, New Password: weak password that fails policy, Confirm New Password: same weak password)<br>2. Click "Change Password" | Validation error indicating the new password does not meet the strong-password requirements. | Medium |

#### Edge Case Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 12.SECSET-006 | Change password using a minimally-compliant strong password | User is authenticated and Security Settings > Change Password panel is open | 1. Fill all required fields (Current Password: valid current password, New Password: minimally-compliant strong password, Confirm New Password: same as New Password)<br>2. Click "Change Password" | Password changed successfully and credentials are updated. | Low |

---

### Support Center

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 13.SUPCEN-001 | Send message successfully with required fields (no attachment) | User is logged in and the Support Center Send Message form is visible | 1. Fill all required fields (Subject with a valid-length subject, Category, Message Body with valid content)<br>2. Click "Send Message" | A success notification "Message sent successfully." is displayed and a ticket ID is shown | High |
| 13.SUPCEN-002 | Send message successfully with a valid attachment | User is logged in and the Support Center Send Message form is visible | 1. Fill all required fields (Subject with a valid-length subject, Category, Message Body with valid content) and attach a supported file type<br>2. Click "Send Message" | A success notification "Message sent successfully." is displayed and a ticket ID is shown | High |
| 13.SUPCEN-003 | Submit Request Callback with valid inputs | User is signed in and the Request Callback form is displayed | 1. Fill all required fields (select Reason for Call, choose a valid Preferred Date at least the next business day, choose a Preferred Time Window, verify or edit Phone Number to a valid format)<br>2. Click "Request Callback" | A success message "Callback request submitted." is displayed and an email confirmation is sent. | High |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 13.SUPCEN-004 | Submit with all required fields empty | User is logged in and the Support Center Send Message form is visible | 1. Leave all required fields empty<br>2. Click "Send Message" | Validation errors shown for all required fields. | Medium |
| 13.SUPCEN-005 | Submit with Message Body empty | User is logged in and the Support Center Send Message form is visible | 1. Fill all other required fields (Subject, Category), leave Message Body empty<br>2. Click "Send Message" | Inline validation error indicating Message Body is required is displayed. | Medium |
| 13.SUPCEN-006 | Submit with Subject exceeding allowed length | User is logged in and the Support Center Send Message form is visible | 1. Fill all required fields (Subject exceeding allowed length, Category, Message Body with valid content)<br>2. Click "Send Message" | Inline validation guidance is shown for Subject length and the message is not sent. | Medium |
| 13.SUPCEN-007 | Submit with unsupported attachment type | User is logged in and the Support Center Send Message form is visible | 1. Fill all required fields (Subject, Category, Message Body with valid content) and attach an unsupported file type<br>2. Click "Send Message" | Inline validation guidance about the attachment type is displayed and the message is not sent. | Medium |
| 13.SUPCEN-008 | Submit with all required fields empty | User is signed in and the Request Callback form is displayed | 1. Leave all required fields empty<br>2. Click "Request Callback" | Validation errors shown inline for the required fields. | Medium |
| 13.SUPCEN-009 | Submit with Preferred Date earlier than allowed | User is signed in and the Request Callback form is displayed | 1. Fill all other required fields with valid values, set Preferred Date to a date earlier than the next business day<br>2. Click "Request Callback" | Inline validation error shown indicating the Preferred Date is invalid and request is not submitted. | Medium |

#### Edge Case Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 13.SUPCEN-010 | Submit with Preferred Date set to the next business day (boundary) | User is signed in and the Request Callback form is displayed | 1. Fill all required fields (select Reason for Call, set Preferred Date to the next business day, choose a Preferred Time Window, ensure Phone Number is valid)<br>2. Click "Request Callback" | Request is accepted and a success message "Callback request submitted." is displayed; an email confirmation is sent. | Medium |

---

## Post-Verification Details

This section shows verification requirements for tests that modify application state.
Tests using the **before/after** strategy require running a verification test BEFORE
and AFTER the action to compare values.

### 4.ONA-001: Open a new Checking account with valid initial deposit

**Coverage:** PARTIAL Partial
**Modifies State:** account_opening, funding_transfer, account_status

**1. Verify the Open New Account UI shows the success confirmation and redirects to the accounts overview**

- **Status:** FOUND found
- **Type:** -
- **Strategy:** After Only
- **Matched Test:** 4.ONA-002 (Open a new Savings account with valid initial deposit)
- **Confidence:** 85%
- **Execution Note:** Use this test as the after-only verification: execute the Open New Account flow, then assert the page displays the exact message 'Account opened successfully!' and that the app navigates to the Accounts Overview (verify by URL, page title, or presence of Accounts Overview UI). Additionally confirm the new account appears in the accounts listing or that account_creation_status is set to success.

**2. Verify the new Checking account appears in the Accounts Overview listing with correct type and an Open status**

- **Status:** PARTIAL partial
- **Type:** -
- **Strategy:** After Only
- **Matched Test:** 3.ACCOVE-002 (Accounts table displays expected columns in each row)
- **Confidence:** 65%
- **Execution Note:** This test runs on the Accounts Overview and verifies the table shows Account Number, Account Type, Current Balance, Account Status, and Open Date. For after_only verification, the test must be extended to assert the existence of a row where Account Type == 'Checking', Account Number matches the masked pattern (e.g., ****1234), and Account Status == 'Open'. As-is it only confirms the presence of columns/fields, not the specific new Checking account or the exact 'Open' status/value.
- **Reason:** Operates on the correct module and displays the relevant fields (account type and status), but it does not assert a specific account_type value ('Checking'), does not verify the masked account number content, and expects an 'Active' badge rather than explicitly checking for 'Open'. Therefore it cannot, by itself, confirm the after-only expected outcome.
- **Manual Step:** Open Accounts Overview. Scan table rows to find an entry where Account Type = 'Checking'. For that row, verify the Account Number is masked (only last four digits visible, e.g., ****1234) and that the Account Status displays 'Open' (or the equivalent open/active badge). If automating, add assertions to the test: locate a row with Account Type 'Checking' AND Account Status text 'Open' AND Account Number matching /^\*{2,}\d{4}$/.

**3. Verify the funding source account balance decreased by the initial deposit amount**

- **Status:** FOUND found
- **Type:** -
- **Strategy:** Before/After
- **Matched Test:** 3.ACCOVE-003 (Footer displays the total balance across all accounts)
- **Confidence:** 90%
- **Before Action:** Record the funding source account's balance_display and total_balance on Accounts Overview before clicking 'Open Account'
- **After Action:** Confirm the funding source balance_display decreased by the initial deposit amount and the total_balance decreased accordingly
- **Execution Note:** Use this Accounts Overview test to read the Current Balance value for the funding source account row and the footer total_balance. Run it once BEFORE clicking 'Open Account' to record the funding_account_balance (balance_display) and total_balance, then run it AGAIN AFTER the Open Account action and compare the recorded values to verify the funding account decreased by the initial deposit and the footer total reflects the deduction.

**Coverage Gaps:**
- Operates on the correct module and displays the relevant fields (account type and status), but it does not assert a specific account_type value ('Checking'), does not verify the masked account number content, and expects an 'Active' badge rather than explicitly checking for 'Open'. Therefore it cannot, by itself, confirm the after-only expected outcome.

#### Execution Plan

> **Strategy:** Run verification tests BEFORE and AFTER the action to compare values.

**1. [NAVIGATE]** Navigate to Accounts Overview
   > Navigate from Open New Account to Accounts Overview to record baseline data

**2. [PRE-VERIFY] 3.ACCOVE-003** -- Footer displays the total balance across all accounts
   > Run 3.ACCOVE-003 and RECORD the current values before the action

**3. [NAVIGATE]** Navigate to Open New Account
   > Return to Open New Account to execute the action

**4. [ACTION] 4.ONA-001** -- Open a new Checking account with valid initial deposit
   > Run 4.ONA-001 — this is the state-changing action being verified

**5. [POST-VERIFY] 4.ONA-002** -- Open a new Savings account with valid initial deposit
   > Use this test as the after-only verification: execute the Open New Account flow, then assert the page displays the exact message 'Account opened successfully!' and that the app navigates to the Accounts Overview (verify by URL, page title, or presence of Accounts Overview UI). Additionally confirm the new account appears in the accounts listing or that account_creation_status is set to success.

**6. [NAVIGATE]** Navigate to Accounts Overview
   > Navigate from Open New Account to Accounts Overview

**7. [POST-VERIFY] 3.ACCOVE-002** -- Accounts table displays expected columns in each row
   > This test runs on the Accounts Overview and verifies the table shows Account Number, Account Type, Current Balance, Account Status, and Open Date. For after_only verification, the test must be extended to assert the existence of a row where Account Type == 'Checking', Account Number matches the masked pattern (e.g., ****1234), and Account Status == 'Open'. As-is it only confirms the presence of columns/fields, not the specific new Checking account or the exact 'Open' status/value.
   > Limitation: Operates on the correct module and displays the relevant fields (account type and status), but it does not assert a specific account_type value ('Checking'), does not verify the masked account number content, and expects an 'Active' badge rather than explicitly checking for 'Open'. Therefore it cannot, by itself, confirm the after-only expected outcome.

**8. [NAVIGATE]** Navigate to Accounts Overview
   > Navigate from Open New Account to Accounts Overview to verify the change

**9. [POST-VERIFY] 3.ACCOVE-003** -- Footer displays the total balance across all accounts
   > Run 3.ACCOVE-003 AGAIN and COMPARE with baseline values recorded in pre-verify

**Notes:** PRE: Record baseline with 3.ACCOVE-003 → ACTION: Execute 4.ONA-001 → POST: Verify with 4.ONA-002, 3.ACCOVE-002, 3.ACCOVE-003 (compare against baseline)

---

### 4.ONA-002: Open a new Savings account with valid initial deposit

**Coverage:** PARTIAL Partial
**Modifies State:** account_opening, funding_transfer, account_status

**1. Verify the Open New Account UI shows the success confirmation and redirects to the accounts overview**

- **Status:** FOUND found
- **Type:** -
- **Strategy:** After Only
- **Matched Test:** 4.ONA-013 (Open Savings account with deposit equal to minimum)
- **Confidence:** 95%
- **Execution Note:** Use test 4.ONA-013 as the after-only verification: after submitting the Open Savings account flow, assert the page displays the exact string 'Account opened successfully!', verify the UI redirected to Accounts Overview (e.g., by checking the URL, page title/header, or presence of the accounts overview element), and confirm the new savings account appears in the accounts listing or that account_creation_status indicates success.

**2. Verify the new Savings account appears in the Accounts Overview listing with correct type and an Open status**

- **Status:** PARTIAL partial
- **Type:** -
- **Strategy:** After Only
- **Matched Test:** 4.ONA-013 (Open Savings account with deposit equal to minimum)
- **Confidence:** 60%
- **Execution Note:** This test opens a Savings account and explicitly checks that the new savings account appears in the accounts listing (redirects to Accounts Overview). Use this test as the after-only verification but extend its verification steps on the Accounts Overview page to assert: (1) the new row shows Account Type = 'Savings', (2) the Account Number is masked (****1234 style) and matches the newly created account's last 4 digits, and (3) the Account Status displays 'Open'.
- **Reason:** While 4.ONA-013 verifies that a new savings account appears in the accounts listing after opening, it does not explicitly verify the masked account number or that the account_status is 'Open'. The Accounts Overview candidates cover masking (3.ACCOVE-006) and column presence/status (3.ACCOVE-002) but none combine presence, masking, and explicit 'Open' status checks in a single after-only test.
- **Manual Step:** After opening the Savings account, navigate to Accounts Overview. Locate the new entry (by matching last-4 digits or other identifier), confirm Account Type = 'Savings', confirm the Account Number is masked (only last four digits visible), and confirm Account Status is 'Open'.

**3. Verify the funding source account balance decreased by the initial deposit amount**

- **Status:** FOUND found
- **Type:** -
- **Strategy:** Before/After
- **Matched Test:** 3.ACCOVE-003 (Footer displays the total balance across all accounts)
- **Confidence:** 92%
- **Before Action:** Record the funding source account's balance_display and total_balance on Accounts Overview before clicking 'Open Account'
- **After Action:** Confirm the funding source balance_display decreased by the initial deposit amount and the total_balance decreased accordingly
- **Execution Note:** Run this Accounts Overview test BEFORE the Open Account action to record the funding account's Current Balance (balance_display) from the account row and the footer total_balance. After opening the Savings account, re-run the same test to capture the post-action Current Balance and footer total_balance. Compare the funding account row's balance_display before vs after to ensure it decreased by the initial deposit amount, and verify the footer total_balance decreased accordingly.

**Coverage Gaps:**
- While 4.ONA-013 verifies that a new savings account appears in the accounts listing after opening, it does not explicitly verify the masked account number or that the account_status is 'Open'. The Accounts Overview candidates cover masking (3.ACCOVE-006) and column presence/status (3.ACCOVE-002) but none combine presence, masking, and explicit 'Open' status checks in a single after-only test.

#### Execution Plan

> **Strategy:** Run verification tests BEFORE and AFTER the action to compare values.

**1. [NAVIGATE]** Navigate to Accounts Overview
   > Navigate from Open New Account to Accounts Overview to record baseline data

**2. [PRE-VERIFY] 3.ACCOVE-003** -- Footer displays the total balance across all accounts
   > Run 3.ACCOVE-003 and RECORD the current values before the action

**3. [NAVIGATE]** Navigate to Open New Account
   > Return to Open New Account to execute the action

**4. [ACTION] 4.ONA-002** -- Open a new Savings account with valid initial deposit
   > Run 4.ONA-002 — this is the state-changing action being verified

**5. [POST-VERIFY] 4.ONA-013** -- Open Savings account with deposit equal to minimum
   > Use test 4.ONA-013 as the after-only verification: after submitting the Open Savings account flow, assert the page displays the exact string 'Account opened successfully!', verify the UI redirected to Accounts Overview (e.g., by checking the URL, page title/header, or presence of the accounts overview element), and confirm the new savings account appears in the accounts listing or that account_creation_status indicates success.

**6. [POST-VERIFY] 4.ONA-013** -- Open Savings account with deposit equal to minimum
   > This test opens a Savings account and explicitly checks that the new savings account appears in the accounts listing (redirects to Accounts Overview). Use this test as the after-only verification but extend its verification steps on the Accounts Overview page to assert: (1) the new row shows Account Type = 'Savings', (2) the Account Number is masked (****1234 style) and matches the newly created account's last 4 digits, and (3) the Account Status displays 'Open'.
   > Limitation: While 4.ONA-013 verifies that a new savings account appears in the accounts listing after opening, it does not explicitly verify the masked account number or that the account_status is 'Open'. The Accounts Overview candidates cover masking (3.ACCOVE-006) and column presence/status (3.ACCOVE-002) but none combine presence, masking, and explicit 'Open' status checks in a single after-only test.

**7. [NAVIGATE]** Navigate to Accounts Overview
   > Navigate from Open New Account to Accounts Overview to verify the change

**8. [POST-VERIFY] 3.ACCOVE-003** -- Footer displays the total balance across all accounts
   > Run 3.ACCOVE-003 AGAIN and COMPARE with baseline values recorded in pre-verify

**Notes:** PRE: Record baseline with 3.ACCOVE-003 → ACTION: Execute 4.ONA-002 → POST: Verify with 4.ONA-013, 4.ONA-013, 3.ACCOVE-003 (compare against baseline)

---

### 5.TRAFUN-001: Successful internal transfer between own accounts

**Coverage:** PARTIAL Partial
**Modifies State:** funds_transfer, account_balance

**1. Verify the source account balance decreased by the transfer amount**

- **Status:** FOUND found
- **Type:** -
- **Strategy:** Before/After
- **Matched Test:** 3.ACCOVE-003 (Footer displays the total balance across all accounts)
- **Confidence:** 90%
- **Before Action:** Record the source account's balance_display on Accounts Overview before the transfer
- **After Action:** Confirm the source account's balance_display decreased by the exact transfer amount
- **Execution Note:** Use this Accounts Overview test to read and record the 'Current Balance' (balance_display) for the specific source account row before the transfer. After performing the internal transfer, re-run the same test (or reopen Accounts Overview and read the same account's Current Balance) to capture the after value for comparison. The test already reads Current Balance values for each account row, which satisfies the before/after observation requirement.

**2. Verify the destination internal account balance increased by the transfer amount**

- **Status:** FOUND found
- **Type:** -
- **Strategy:** Before/After
- **Matched Test:** 3.ACCOVE-003 (Footer displays the total balance across all accounts)
- **Confidence:** 90%
- **Before Action:** Record the destination account's balance_display on Accounts Overview before the transfer
- **After Action:** Confirm the destination account's balance_display increased by the exact transfer amount
- **Execution Note:** Use this Accounts Overview test to read the Current Balance value from each account row. Before the transfer, locate the destination account row (by account number) and capture its Current Balance (balance_display). After the transfer, re-run the same test and capture the destination account's Current Balance again and compare the two values: the increase should equal the transfer amount.

**3. Verify the transfer confirmation and transaction ID appear in Transfer Funds records**

- **Status:** PARTIAL partial
- **Type:** -
- **Strategy:** After Only
- **Matched Test:** 5.TRAFUN-002 (Successful external transfer to matching account number)
- **Confidence:** 75%
- **Execution Note:** Use 5.TRAFUN-002 to confirm the post-transfer confirmation area: execute the transfer, verify the onscreen message 'Transfer completed successfully.' and capture the displayed transaction ID. Then extend the test to locate the transfer in Recent Transfers/Transfer History and assert the recorded transaction shows the same transaction ID and status.
- **Reason:** This test operates on the correct module and already verifies the confirmation message and that a transaction ID is shown (satisfies the primary after-only check). However, it does not explicitly include steps to verify the transfer appears in recent transfer records/history, which is required by the verification action.
- **Manual Step:** After capturing the onscreen confirmation and transaction ID, navigate to the Recent Transfers or Transfer History page, search/filter for the captured transaction ID (or newest transfers), and verify a record exists with the same transaction ID and status 'Transfer completed successfully.' Ensure the transaction ID field is non-empty in the record.

**Coverage Gaps:**
- This test operates on the correct module and already verifies the confirmation message and that a transaction ID is shown (satisfies the primary after-only check). However, it does not explicitly include steps to verify the transfer appears in recent transfer records/history, which is required by the verification action.

#### Execution Plan

> **Strategy:** Run verification tests BEFORE and AFTER the action to compare values.

**1. [NAVIGATE]** Navigate to Accounts Overview
   > Navigate from Transfer Funds to Accounts Overview to record baseline data

**2. [PRE-VERIFY] 3.ACCOVE-003** -- Footer displays the total balance across all accounts
   > Run 3.ACCOVE-003 and RECORD the current values before the action

**3. [NAVIGATE]** Navigate to Accounts Overview
   > Navigate from Transfer Funds to Accounts Overview to record baseline data

**4. [PRE-VERIFY] 3.ACCOVE-003** -- Footer displays the total balance across all accounts
   > Run 3.ACCOVE-003 and RECORD the current values before the action

**5. [NAVIGATE]** Navigate to Transfer Funds
   > Return to Transfer Funds to execute the action

**6. [ACTION] 5.TRAFUN-001** -- Successful internal transfer between own accounts
   > Run 5.TRAFUN-001 — this is the state-changing action being verified

**7. [NAVIGATE]** Navigate to Accounts Overview
   > Navigate from Transfer Funds to Accounts Overview to verify the change

**8. [POST-VERIFY] 3.ACCOVE-003** -- Footer displays the total balance across all accounts
   > Run 3.ACCOVE-003 AGAIN and COMPARE with baseline values recorded in pre-verify

**9. [NAVIGATE]** Navigate to Accounts Overview
   > Navigate from Transfer Funds to Accounts Overview to verify the change

**10. [POST-VERIFY] 3.ACCOVE-003** -- Footer displays the total balance across all accounts
   > Run 3.ACCOVE-003 AGAIN and COMPARE with baseline values recorded in pre-verify

**11. [POST-VERIFY] 5.TRAFUN-002** -- Successful external transfer to matching account number
   > Use 5.TRAFUN-002 to confirm the post-transfer confirmation area: execute the transfer, verify the onscreen message 'Transfer completed successfully.' and capture the displayed transaction ID. Then extend the test to locate the transfer in Recent Transfers/Transfer History and assert the recorded transaction shows the same transaction ID and status.
   > Limitation: This test operates on the correct module and already verifies the confirmation message and that a transaction ID is shown (satisfies the primary after-only check). However, it does not explicitly include steps to verify the transfer appears in recent transfer records/history, which is required by the verification action.

**Notes:** PRE: Record baseline with 3.ACCOVE-003, 3.ACCOVE-003 → ACTION: Execute 5.TRAFUN-001 → POST: Verify with 3.ACCOVE-003, 3.ACCOVE-003, 5.TRAFUN-002 (compare against baseline)

---

### 5.TRAFUN-002: Successful external transfer to matching account number

**Coverage:** PARTIAL Partial
**Modifies State:** funds_transfer, account_balance, external_transfer_request

**1. Verify the source account balance decreased by the external transfer amount**

- **Status:** FOUND found
- **Type:** -
- **Strategy:** Before/After
- **Matched Test:** 3.ACCOVE-003 (Footer displays the total balance across all accounts)
- **Confidence:** 90%
- **Before Action:** Record the source account's balance_display on Accounts Overview before the external transfer
- **After Action:** Confirm the source account's balance_display decreased by the exact transfer amount
- **Execution Note:** Run this test on Accounts Overview to read the Current Balance value from each account row. In the BEFORE run, capture the source account's Current Balance (balance_display). After performing the external transfer, re-open Accounts Overview and run again to capture the source account's Current Balance. Compare the two captured values to confirm the decrease equals the transfer amount.

**2. Verify an external transfer request/record was created with a transaction ID and matching destination account number**

- **Status:** PARTIAL partial
- **Type:** -
- **Strategy:** After Only
- **Matched Test:** 5.TRAFUN-001 (Successful internal transfer between own accounts)
- **Confidence:** 50%
- **Execution Note:** This test runs the Transfer Funds flow and verifies a confirmation message and transaction ID, but it is for an internal transfer. To use it for this verification, modify the test to select External Account (external transfer), enter the external destination account number (and confirm), submit the transfer, then verify the confirmation page displays a transaction ID and that an external_transfer_request record exists for the submitted destination account with transfer_status = success.
- **Reason:** None of the candidate tests explicitly perform and confirm an external transfer and then check the external_transfer_request record. 5.TRAFUN-001 already verifies a transaction ID on confirmation (useful for the 'transaction ID displayed' requirement) but targets an internal transfer rather than creating an external_transfer_request with the external destination account number. The other tests either cover validation failure (5.TRAFUN-006) or only UI input switching (5.TRAFUN-004), so they cannot confirm the required post-action record and status.
- **Manual Step:** After performing the external transfer action, open the Transfer Funds confirmation page and confirm a transaction ID is shown. Then query the transfer records (or admin/transactions view or database) for an external_transfer_request with the submitted destination account number and verify transfer_status = 'success' and that the record includes the transaction ID shown on the confirmation.

**3. Verify the outgoing external transfer appears in the Account Statements transaction list for the source account**

- **Status:** FOUND found
- **Type:** -
- **Strategy:** After Only
- **Matched Test:** 11.ACCSTA-002 (Generate statement using custom date range)
- **Confidence:** 90%
- **Execution Note:** Use the 'Generate statement using custom date range' test after performing the external transfer. Select the source account, enter a start and end date that include the transfer date, click 'Generate Statement', then inspect the generated transaction list to confirm a transaction row exists for the outgoing external transfer with the expected amount and reference.

**Coverage Gaps:**
- None of the candidate tests explicitly perform and confirm an external transfer and then check the external_transfer_request record. 5.TRAFUN-001 already verifies a transaction ID on confirmation (useful for the 'transaction ID displayed' requirement) but targets an internal transfer rather than creating an external_transfer_request with the external destination account number. The other tests either cover validation failure (5.TRAFUN-006) or only UI input switching (5.TRAFUN-004), so they cannot confirm the required post-action record and status.

#### Execution Plan

> **Strategy:** Run verification tests BEFORE and AFTER the action to compare values.

**1. [NAVIGATE]** Navigate to Accounts Overview
   > Navigate from Transfer Funds to Accounts Overview to record baseline data

**2. [PRE-VERIFY] 3.ACCOVE-003** -- Footer displays the total balance across all accounts
   > Run 3.ACCOVE-003 and RECORD the current values before the action

**3. [NAVIGATE]** Navigate to Transfer Funds
   > Return to Transfer Funds to execute the action

**4. [ACTION] 5.TRAFUN-002** -- Successful external transfer to matching account number
   > Run 5.TRAFUN-002 — this is the state-changing action being verified

**5. [NAVIGATE]** Navigate to Accounts Overview
   > Navigate from Transfer Funds to Accounts Overview to verify the change

**6. [POST-VERIFY] 3.ACCOVE-003** -- Footer displays the total balance across all accounts
   > Run 3.ACCOVE-003 AGAIN and COMPARE with baseline values recorded in pre-verify

**7. [POST-VERIFY] 5.TRAFUN-001** -- Successful internal transfer between own accounts
   > This test runs the Transfer Funds flow and verifies a confirmation message and transaction ID, but it is for an internal transfer. To use it for this verification, modify the test to select External Account (external transfer), enter the external destination account number (and confirm), submit the transfer, then verify the confirmation page displays a transaction ID and that an external_transfer_request record exists for the submitted destination account with transfer_status = success.
   > Limitation: None of the candidate tests explicitly perform and confirm an external transfer and then check the external_transfer_request record. 5.TRAFUN-001 already verifies a transaction ID on confirmation (useful for the 'transaction ID displayed' requirement) but targets an internal transfer rather than creating an external_transfer_request with the external destination account number. The other tests either cover validation failure (5.TRAFUN-006) or only UI input switching (5.TRAFUN-004), so they cannot confirm the required post-action record and status.

**8. [NAVIGATE]** Navigate to Account Statements
   > Navigate from Transfer Funds to Account Statements

**9. [POST-VERIFY] 11.ACCSTA-002** -- Generate statement using custom date range
   > Use the 'Generate statement using custom date range' test after performing the external transfer. Select the source account, enter a start and end date that include the transfer date, click 'Generate Statement', then inspect the generated transaction list to confirm a transaction row exists for the outgoing external transfer with the expected amount and reference.

**Notes:** PRE: Record baseline with 3.ACCOVE-003 → ACTION: Execute 5.TRAFUN-002 → POST: Verify with 3.ACCOVE-003, 5.TRAFUN-001, 11.ACCSTA-002 (compare against baseline)

---

### 6.PAYMEN-001: Submit valid payment and verify reference code and balance update

**Coverage:** PARTIAL Partial
**Modifies State:** bill_payment, account_balance

**1. Verify the Payments UI shows a payment confirmation and displays a payment reference code**

- **Status:** PARTIAL partial
- **Type:** -
- **Strategy:** After Only
- **Matched Test:** 6.PAYMEN-004 (Submit payment when amount equals available funds (boundary))
- **Confidence:** 65%
- **Execution Note:** This test exercises a successful payment submit on the Payments page and can serve as the basis for verification. It must be extended to assert that the post-submit confirmation area displays a success message and that a non-empty payment_reference code element is present/visible. Specifically, after the existing step 'Click "Pay"', add steps to locate the confirmation area, verify the success message text, and read/assert that the payment_reference field/value is present and not empty.
- **Reason:** The case runs on the correct Payments module and executes a successful payment, but its expected checks focus on account balance update rather than verifying the confirmation UI or the payment_reference code. As written it cannot, by itself (after_only), confirm the required visible payment_reference and success message.
- **Manual Step:** After clicking 'Pay', look at the confirmation area and verify: (1) a visible success message indicating payment completed, and (2) a payment reference code is displayed and non-empty (capture the code for records). If automating, add explicit assertions for the success text and that the payment_reference element exists and its text length > 0.

**2. Verify the source account balance is reduced by the payment amount**

- **Status:** FOUND found
- **Type:** -
- **Strategy:** Before/After
- **Matched Test:** 3.ACCOVE-003 (Footer displays the total balance across all accounts)
- **Confidence:** 86%
- **Before Action:** Record the source account's balance_display on Accounts Overview before clicking 'Pay'
- **After Action:** Confirm the source account's balance_display decreased by the exact payment amount
- **Execution Note:** Use this Accounts Overview test to read the 'Current Balance' value from each account row (including the source account). Run it BEFORE the payment to record the source account's balance_display, then run it AGAIN AFTER the payment and compare the recorded source account balance to confirm it decreased by the exact payment amount.

**3. Verify the payment transaction appears in Account Statements with payee details and reference code**

- **Status:** PARTIAL partial
- **Type:** -
- **Strategy:** After Only
- **Matched Test:** 11.ACCSTA-001 (Generate statement using month-and-year period)
- **Confidence:** 75%
- **Execution Note:** Use this test after the payment: select the same Account and Statement Period (month/year) and click 'Generate Statement' to display the statement transaction_list. Then locate/search the generated transaction_list for an entry that matches the payment's payee name, amount and payment reference code and assert a matching entry exists.
- **Reason:** This test operates on the correct module (Account Statements) and displays the retrieved transactions (so it can surface the transaction_list), but the documented expected result does not explicitly assert or verify the payee details and payment_reference. For an after_only verification it must confirm the specific transaction and fields; the current test must be extended to perform that assertion.
- **Manual Step:** After generating the statement for the appropriate account and period, inspect the statement's transaction_list and verify there is an entry where payee_name, amount, and payment_reference exactly match the expected values (record transaction id/date if present).

**Coverage Gaps:**
- The case runs on the correct Payments module and executes a successful payment, but its expected checks focus on account balance update rather than verifying the confirmation UI or the payment_reference code. As written it cannot, by itself (after_only), confirm the required visible payment_reference and success message.
- This test operates on the correct module (Account Statements) and displays the retrieved transactions (so it can surface the transaction_list), but the documented expected result does not explicitly assert or verify the payee details and payment_reference. For an after_only verification it must confirm the specific transaction and fields; the current test must be extended to perform that assertion.

#### Execution Plan

> **Strategy:** Run verification tests BEFORE and AFTER the action to compare values.

**1. [NAVIGATE]** Navigate to Accounts Overview
   > Navigate from Payments to Accounts Overview to record baseline data

**2. [PRE-VERIFY] 3.ACCOVE-003** -- Footer displays the total balance across all accounts
   > Run 3.ACCOVE-003 and RECORD the current values before the action

**3. [NAVIGATE]** Navigate to Payments
   > Return to Payments to execute the action

**4. [ACTION] 6.PAYMEN-001** -- Submit valid payment and verify reference code and balance update
   > Run 6.PAYMEN-001 — this is the state-changing action being verified

**5. [POST-VERIFY] 6.PAYMEN-004** -- Submit payment when amount equals available funds (boundary)
   > This test exercises a successful payment submit on the Payments page and can serve as the basis for verification. It must be extended to assert that the post-submit confirmation area displays a success message and that a non-empty payment_reference code element is present/visible. Specifically, after the existing step 'Click "Pay"', add steps to locate the confirmation area, verify the success message text, and read/assert that the payment_reference field/value is present and not empty.
   > Limitation: The case runs on the correct Payments module and executes a successful payment, but its expected checks focus on account balance update rather than verifying the confirmation UI or the payment_reference code. As written it cannot, by itself (after_only), confirm the required visible payment_reference and success message.

**6. [NAVIGATE]** Navigate to Accounts Overview
   > Navigate from Payments to Accounts Overview to verify the change

**7. [POST-VERIFY] 3.ACCOVE-003** -- Footer displays the total balance across all accounts
   > Run 3.ACCOVE-003 AGAIN and COMPARE with baseline values recorded in pre-verify

**8. [NAVIGATE]** Navigate to Account Statements
   > Navigate from Payments to Account Statements

**9. [POST-VERIFY] 11.ACCSTA-001** -- Generate statement using month-and-year period
   > Use this test after the payment: select the same Account and Statement Period (month/year) and click 'Generate Statement' to display the statement transaction_list. Then locate/search the generated transaction_list for an entry that matches the payment's payee name, amount and payment reference code and assert a matching entry exists.
   > Limitation: This test operates on the correct module (Account Statements) and displays the retrieved transactions (so it can surface the transaction_list), but the documented expected result does not explicitly assert or verify the payee details and payment_reference. For an after_only verification it must confirm the specific transaction and fields; the current test must be extended to perform that assertion.

**Notes:** PRE: Record baseline with 3.ACCOVE-003 → ACTION: Execute 6.PAYMEN-001 → POST: Verify with 6.PAYMEN-004, 3.ACCOVE-003, 11.ACCSTA-001 (compare against baseline)

---

### 7.REQLOA-001: Request a Personal loan with valid inputs

**Coverage:** PARTIAL Partial
**Modifies State:** loan_creation, collateral_hold, loan_status

**1. Verify the loan application result shows approval and the new loan details in the Request Loan module**

- **Status:** PARTIAL partial
- **Type:** -
- **Strategy:** After Only
- **Matched Test:** 7.REQLOA-002 (Request an Auto loan with valid inputs)
- **Confidence:** 70%
- **Execution Note:** Test exercises the Request Loan module and checks for an approval message and display of new loan account details (which matches the verification goal). To use this as the verification for the required Personal loan, change the Loan Type to Personal and run the test AFTER submitting the Personal loan request. Then confirm the UI shows the approval message and that the loan details (amount, interest rate, terms) are displayed. Additionally verify the loan_application_status field (in UI or API) equals 'approved'.
- **Reason:** The candidate operates on the correct module and verifies an approval message and loan details, but it is written for an Auto loan (not a Personal loan) and does not explicitly mention checking the loan_application_status field or named loan_terms fields. Therefore it cannot be used as-is for the Personal-loan after_only verification without small modifications.
- **Manual Step:** Submit a Personal loan request in the Request Loan module. After submission, open the created loan record or Request Loan results and confirm: (1) an approval message is displayed (e.g., 'Loan approved and created successfully!'), (2) loan_application_status shows 'approved', and (3) loan details are visible (loan amount, interest rate, term length). If any of these are not visible in the UI, query the backend/API for the new loan record to assert the same fields.

**2. Verify the newly created loan account appears in Accounts Overview as a loan-type account with appropriate open status/details**

- **Status:** PARTIAL partial
- **Type:** -
- **Strategy:** After Only
- **Matched Test:** 3.ACCOVE-002 (Accounts table displays expected columns in each row)
- **Confidence:** 60%
- **Execution Note:** This Accounts Overview test runs on the correct page and verifies that rows show Account Type and Account Status (Active). To serve as the after_only verification for a newly created loan, extend this test to assert that: (1) there exists a row with Account Type = 'Loan' (or 'Personal Loan'), and (2) the loan-specific details (loan amount and/or terms) are either displayed in the row (preferred) or accessible via a link/expand/action on the row. If the UI only provides a link, the test should click the account row/link and verify loan amount/terms on the resulting details pane/page.
- **Reason:** Matches the Accounts Overview module and inspects the account table columns (including Account Type and Account Status) but does not currently check for loan-specific details (loan amount/terms) or assert the account_type equals 'Loan/Personal'. As an after_only verification it must confirm the new loan entry and its loan details by itself, which the candidate does not currently do.
- **Manual Step:** Open Accounts Overview. Locate the newest account rows and find an entry with Account Type = 'Loan' or 'Personal'. Verify the account row shows/open link to loan-specific details and confirm the loan amount and terms (or open the account details page/panel to view them). Record account status (Open/Active) and any loan-specific fields.

**3. Verify a collateral hold was placed against the selected collateral account by checking the available balance change**

- **Status:** PARTIAL partial
- **Type:** -
- **Strategy:** Before/After
- **Matched Test:** 7.REQLOA-010 (Verify no actual balance debits occur after loan creation)
- **Confidence:** 60%
- **Before Action:** Record the collateral account's balance_display and any available/hold indicators on Accounts Overview before submitting the loan request
- **After Action:** Confirm the collateral account shows a deduction of the expected hold amount or a visible collateral_hold indicator and that available funds reflect the hold
- **Execution Note:** This test records the collateral account balance on the Request Loan page, but the verification requirement specifically needs the Accounts Overview page to be observed BEFORE and AFTER the loan action. To use this test for the required before_after verification, add explicit steps to navigate to Accounts Overview and record the collateral account's balance_display/available amount and any hold indicators before submitting the loan, then re-open Accounts Overview after loan creation to capture the same fields for comparison.
- **Reason:** Operates on the Request Loan module (not Accounts Overview). While it notes a displayed collateral account balance, it does not access/display the Accounts Overview available balance or any collateral_hold indicators as required by the verification scenario.
- **Manual Step:** Before running the loan submission: navigate to Accounts Overview, locate the collateral_account, record balance_display and available amount and note any hold indicators or references to collateral_hold. Submit the loan. After the loan is created: re-open Accounts Overview, re-check the collateral_account balance_display and available amount and any hold indicators. Compare before/after values to confirm the expected hold deduction or appearance of a collateral_hold indicator.

**Coverage Gaps:**
- The candidate operates on the correct module and verifies an approval message and loan details, but it is written for an Auto loan (not a Personal loan) and does not explicitly mention checking the loan_application_status field or named loan_terms fields. Therefore it cannot be used as-is for the Personal-loan after_only verification without small modifications.
- Matches the Accounts Overview module and inspects the account table columns (including Account Type and Account Status) but does not currently check for loan-specific details (loan amount/terms) or assert the account_type equals 'Loan/Personal'. As an after_only verification it must confirm the new loan entry and its loan details by itself, which the candidate does not currently do.
- Operates on the Request Loan module (not Accounts Overview). While it notes a displayed collateral account balance, it does not access/display the Accounts Overview available balance or any collateral_hold indicators as required by the verification scenario.

#### Execution Plan

> **Strategy:** Run verification tests BEFORE and AFTER the action to compare values.

**1. [PRE-VERIFY] 7.REQLOA-010** -- Verify no actual balance debits occur after loan creation
   > Run 7.REQLOA-010 and RECORD the current values before the action
   > Limitation: Operates on the Request Loan module (not Accounts Overview). While it notes a displayed collateral account balance, it does not access/display the Accounts Overview available balance or any collateral_hold indicators as required by the verification scenario.

**2. [ACTION] 7.REQLOA-001** -- Request a Personal loan with valid inputs
   > Run 7.REQLOA-001 — this is the state-changing action being verified

**3. [POST-VERIFY] 7.REQLOA-002** -- Request an Auto loan with valid inputs
   > Test exercises the Request Loan module and checks for an approval message and display of new loan account details (which matches the verification goal). To use this as the verification for the required Personal loan, change the Loan Type to Personal and run the test AFTER submitting the Personal loan request. Then confirm the UI shows the approval message and that the loan details (amount, interest rate, terms) are displayed. Additionally verify the loan_application_status field (in UI or API) equals 'approved'.
   > Limitation: The candidate operates on the correct module and verifies an approval message and loan details, but it is written for an Auto loan (not a Personal loan) and does not explicitly mention checking the loan_application_status field or named loan_terms fields. Therefore it cannot be used as-is for the Personal-loan after_only verification without small modifications.

**4. [NAVIGATE]** Navigate to Accounts Overview
   > Navigate from Request Loan to Accounts Overview

**5. [POST-VERIFY] 3.ACCOVE-002** -- Accounts table displays expected columns in each row
   > This Accounts Overview test runs on the correct page and verifies that rows show Account Type and Account Status (Active). To serve as the after_only verification for a newly created loan, extend this test to assert that: (1) there exists a row with Account Type = 'Loan' (or 'Personal Loan'), and (2) the loan-specific details (loan amount and/or terms) are either displayed in the row (preferred) or accessible via a link/expand/action on the row. If the UI only provides a link, the test should click the account row/link and verify loan amount/terms on the resulting details pane/page.
   > Limitation: Matches the Accounts Overview module and inspects the account table columns (including Account Type and Account Status) but does not currently check for loan-specific details (loan amount/terms) or assert the account_type equals 'Loan/Personal'. As an after_only verification it must confirm the new loan entry and its loan details by itself, which the candidate does not currently do.

**6. [POST-VERIFY] 7.REQLOA-010** -- Verify no actual balance debits occur after loan creation
   > Run 7.REQLOA-010 AGAIN and COMPARE with baseline values recorded in pre-verify
   > Limitation: Operates on the Request Loan module (not Accounts Overview). While it notes a displayed collateral account balance, it does not access/display the Accounts Overview available balance or any collateral_hold indicators as required by the verification scenario.

**Notes:** PRE: Record baseline with 7.REQLOA-010 → ACTION: Execute 7.REQLOA-001 → POST: Verify with 7.REQLOA-002, 3.ACCOVE-002, 7.REQLOA-010 (compare against baseline)

---

### 7.REQLOA-002: Request an Auto loan with valid inputs

**Coverage:** PARTIAL Partial
**Modifies State:** loan_creation, collateral_hold, loan_status

**1. Verify the Auto loan application shows approval and the new loan details in the Request Loan module**

- **Status:** PARTIAL partial
- **Type:** -
- **Strategy:** After Only
- **Matched Test:** 7.REQLOA-001 (Request a Personal loan with valid inputs)
- **Confidence:** 65%
- **Execution Note:** Use this test as the verification template but change Loan Type to 'Auto' and ensure the post-submit checks explicitly validate the approval message and the new loan account details (amount, interest rate, terms). Run only AFTER submitting the Auto loan request to confirm success.
- **Reason:** The test is on the correct module (Request Loan) and already checks for an approval message and display of new loan account details, but it targets a Personal loan rather than an Auto loan. It therefore does not exactly match the required loan type and must be adapted to verify an Auto loan's status and terms.
- **Manual Step:** After submitting the Auto loan request, open Request Loan and confirm: 1) an approval message is displayed (e.g., 'Loan approved and created successfully!'); 2) the new loan record is shown with correct loan amount, interest rate, and term; 3) the loan_application_status field equals 'approved' and loan_terms/details are visible.

**2. Verify the newly created auto loan account appears in Accounts Overview as a loan-type account with appropriate details**

- **Status:** PARTIAL partial
- **Type:** -
- **Strategy:** After Only
- **Matched Test:** 4.ONA-002 (Open a new Savings account with valid initial deposit)
- **Confidence:** 60%
- **Execution Note:** This test navigates to Accounts Overview and asserts the new account appears in the accounts listing (after account creation). To use it for the auto-loan verification, change the Open New Account flow to create an Auto/Loan account (or run the auto-loan creation action beforehand) and extend the check to assert the account's type/label is 'Loan' or 'Auto Loan' and that loan-specific details (principal, term, rate, payment schedule) are accessible from the listing.
- **Reason:** The candidate verifies that a newly opened account appears in Accounts Overview, so it exercises the correct page and listing behavior. However, it creates a Savings account (not an auto loan) and only asserts presence in the listing; it does not verify loan-type labeling or loan-specific details. Because the execution strategy is after_only, the test must itself confirm the auto loan entry and its loan details—this test would need modification to do that.
- **Manual Step:** After creating the auto loan, open Accounts Overview, locate the new entry in account_list, confirm the entry is labeled as a loan (e.g., 'Auto Loan' or 'Loan'), click or expand the entry to view details, and verify loan-specific fields such as principal, interest rate, term, monthly payment, and outstanding balance are present and correct.

**3. Verify a collateral hold was applied to the selected collateral account by checking balance/available funds before and after**

- **Status:** FOUND found
- **Type:** -
- **Strategy:** Before/After
- **Matched Test:** 7.REQLOA-010 (Verify no actual balance debits occur after loan creation)
- **Confidence:** 75%
- **Before Action:** Record the collateral account's balance_display and any existing hold indicators before submitting the loan request
- **After Action:** Confirm the collateral account shows the expected decrease in available funds or a new collateral_hold marker after loan creation
- **Execution Note:** Use 7.REQLOA-010 to record the collateral account's displayed balance before submitting the loan and again after loan approval. For this before_after verification, record the balance_display and available funds value shown by the Request Loan page (or Accounts Overview if available) on the BEFORE run, then re-run the same steps on the AFTER run to capture the post-approval values and compare. Augment the test to also read any visible collateral_hold indicator after approval.

**Coverage Gaps:**
- The test is on the correct module (Request Loan) and already checks for an approval message and display of new loan account details, but it targets a Personal loan rather than an Auto loan. It therefore does not exactly match the required loan type and must be adapted to verify an Auto loan's status and terms.
- The candidate verifies that a newly opened account appears in Accounts Overview, so it exercises the correct page and listing behavior. However, it creates a Savings account (not an auto loan) and only asserts presence in the listing; it does not verify loan-type labeling or loan-specific details. Because the execution strategy is after_only, the test must itself confirm the auto loan entry and its loan details—this test would need modification to do that.

#### Execution Plan

> **Strategy:** Run verification tests BEFORE and AFTER the action to compare values.

**1. [PRE-VERIFY] 7.REQLOA-010** -- Verify no actual balance debits occur after loan creation
   > Run 7.REQLOA-010 and RECORD the current values before the action

**2. [ACTION] 7.REQLOA-002** -- Request an Auto loan with valid inputs
   > Run 7.REQLOA-002 — this is the state-changing action being verified

**3. [POST-VERIFY] 7.REQLOA-001** -- Request a Personal loan with valid inputs
   > Use this test as the verification template but change Loan Type to 'Auto' and ensure the post-submit checks explicitly validate the approval message and the new loan account details (amount, interest rate, terms). Run only AFTER submitting the Auto loan request to confirm success.
   > Limitation: The test is on the correct module (Request Loan) and already checks for an approval message and display of new loan account details, but it targets a Personal loan rather than an Auto loan. It therefore does not exactly match the required loan type and must be adapted to verify an Auto loan's status and terms.

**4. [NAVIGATE]** Navigate to Open New Account
   > Navigate from Request Loan to Open New Account

**5. [POST-VERIFY] 4.ONA-002** -- Open a new Savings account with valid initial deposit
   > This test navigates to Accounts Overview and asserts the new account appears in the accounts listing (after account creation). To use it for the auto-loan verification, change the Open New Account flow to create an Auto/Loan account (or run the auto-loan creation action beforehand) and extend the check to assert the account's type/label is 'Loan' or 'Auto Loan' and that loan-specific details (principal, term, rate, payment schedule) are accessible from the listing.
   > Limitation: The candidate verifies that a newly opened account appears in Accounts Overview, so it exercises the correct page and listing behavior. However, it creates a Savings account (not an auto loan) and only asserts presence in the listing; it does not verify loan-type labeling or loan-specific details. Because the execution strategy is after_only, the test must itself confirm the auto loan entry and its loan details—this test would need modification to do that.

**6. [POST-VERIFY] 7.REQLOA-010** -- Verify no actual balance debits occur after loan creation
   > Run 7.REQLOA-010 AGAIN and COMPARE with baseline values recorded in pre-verify

**Notes:** PRE: Record baseline with 7.REQLOA-010 → ACTION: Execute 7.REQLOA-002 → POST: Verify with 7.REQLOA-001, 4.ONA-002, 7.REQLOA-010 (compare against baseline)

---

### 7.REQLOA-003: Request a Home loan with valid inputs

**Coverage:** PARTIAL Partial
**Modifies State:** loan_creation, collateral_hold, loan_status

**1. Verify the Home loan application shows approval and the new loan details in the Request Loan module**

- **Status:** PARTIAL partial
- **Type:** -
- **Strategy:** After Only
- **Matched Test:** 7.REQLOA-002 (Request an Auto loan with valid inputs)
- **Confidence:** 70%
- **Execution Note:** Use this Request Loan test flow but change Loan Type to 'Home'. After submitting, verify the UI shows the approval message and that the new loan account details (principal amount, interest rate, term length/period and any loan terms) are displayed. Also confirm the underlying loan_application_status is set to 'approved' for the Home loan record.
- **Reason:** The candidate operates in the correct module and already checks for an approval message and display of loan account details (which satisfies the after_only requirement). However, it targets an Auto loan rather than the required Home loan, so it doesn't exactly match the requested loan type. If adjusted to select Home, it would fully satisfy the verification.
- **Manual Step:** Submit a Home loan request in the Request Loan module (select Loan Type = Home, fill required fields, Submit). Then in Request Loan results/detail view: 1) Confirm an approval message like 'Loan approved and created successfully!' is shown. 2) Open the new loan record and verify loan_application_status = 'approved'. 3) Verify loan details are visible: loan amount, interest rate, term (months/years) and any loan_terms/conditions. 4) Record identifiers (loan account number) to tie the created loan to the Home application.

**2. Verify the newly created home loan account appears in Accounts Overview as a loan-type account with appropriate details**

- **Status:** PARTIAL partial
- **Type:** -
- **Strategy:** After Only
- **Matched Test:** 4.ONA-002 (Open a new Savings account with valid initial deposit)
- **Confidence:** 50%
- **Execution Note:** This test exercises opening a new account and verifies that the new account appears in Accounts Overview, so it covers the correct page and the act of checking the accounts listing. To use it for this requirement you would need to change the account type from Savings to a Home Loan (or otherwise adapt the test to create a loan-type account) and extend the expected checks to assert loan-type labeling and loan-specific detail fields are present and accessible.
- **Reason:** The candidate accesses Accounts Overview and checks that a newly opened account appears in the listing (good), but it opens a Savings account rather than a Home Loan and does not assert loan-type labeling or loan-specific details. Because execution_strategy is after_only, the verification must confirm the home loan entry and its loan details by itself — this test as written cannot do that.
- **Manual Step:** After creating the home loan, open the Accounts Overview page and locate the new entry. Confirm the entry is labeled as a loan/home loan and that loan details are accessible (account number, loan principal, interest rate, term/tenor, remaining balance and payment schedule). If automating, modify the test to create a Home Loan and add assertions for loan-type label and the specific loan detail fields in the accounts listing or account detail view.

**3. Verify a collateral hold was applied to the selected collateral account by checking balance/available funds before and after**

- **Status:** PARTIAL partial
- **Type:** -
- **Strategy:** Before/After
- **Matched Test:** 7.REQLOA-010 (Verify no actual balance debits occur after loan creation)
- **Confidence:** 65%
- **Before Action:** Record the collateral account's balance_display and any existing hold indicators before submitting the loan request
- **After Action:** Confirm the collateral account shows the expected decrease in available funds or a new collateral_hold marker after loan creation
- **Execution Note:** This test (Request Loan page) does display the collateral account balance, so it can be used to record baseline and post-action balances under a before_after strategy. However it is on the Request Loan module (not Accounts Overview) and does not explicitly capture available funds or any collateral_hold indicator. To use it as the verification test, modify or extend it to read the collateral account's balance_display and available funds and to detect any collateral_hold marker from the Accounts Overview page both BEFORE submitting the loan and AFTER approval.
- **Reason:** Closest candidate shows the collateral account balance but operates on the Request Loan page (not the required Accounts Overview) and does not explicitly capture available funds or a collateral_hold indicator. Because the before_after execution only needs to observe relevant data, showing the balance is helpful, but missing the available-funds field and hold indicator means it is not a full match.
- **Manual Step:** On Accounts Overview, record the collateral account's balance_display and available funds and note any collateral_hold indicator before submitting the home loan. After loan approval, reopen Accounts Overview and re-record balance_display, available funds, and hold indicator; compare values to confirm available balance decreased by the expected hold or that a new collateral_hold marker is present.

**Coverage Gaps:**
- The candidate operates in the correct module and already checks for an approval message and display of loan account details (which satisfies the after_only requirement). However, it targets an Auto loan rather than the required Home loan, so it doesn't exactly match the requested loan type. If adjusted to select Home, it would fully satisfy the verification.
- The candidate accesses Accounts Overview and checks that a newly opened account appears in the listing (good), but it opens a Savings account rather than a Home Loan and does not assert loan-type labeling or loan-specific details. Because execution_strategy is after_only, the verification must confirm the home loan entry and its loan details by itself — this test as written cannot do that.
- Closest candidate shows the collateral account balance but operates on the Request Loan page (not the required Accounts Overview) and does not explicitly capture available funds or a collateral_hold indicator. Because the before_after execution only needs to observe relevant data, showing the balance is helpful, but missing the available-funds field and hold indicator means it is not a full match.

#### Execution Plan

> **Strategy:** Run verification tests BEFORE and AFTER the action to compare values.

**1. [PRE-VERIFY] 7.REQLOA-010** -- Verify no actual balance debits occur after loan creation
   > Run 7.REQLOA-010 and RECORD the current values before the action
   > Limitation: Closest candidate shows the collateral account balance but operates on the Request Loan page (not the required Accounts Overview) and does not explicitly capture available funds or a collateral_hold indicator. Because the before_after execution only needs to observe relevant data, showing the balance is helpful, but missing the available-funds field and hold indicator means it is not a full match.

**2. [ACTION] 7.REQLOA-003** -- Request a Home loan with valid inputs
   > Run 7.REQLOA-003 — this is the state-changing action being verified

**3. [POST-VERIFY] 7.REQLOA-002** -- Request an Auto loan with valid inputs
   > Use this Request Loan test flow but change Loan Type to 'Home'. After submitting, verify the UI shows the approval message and that the new loan account details (principal amount, interest rate, term length/period and any loan terms) are displayed. Also confirm the underlying loan_application_status is set to 'approved' for the Home loan record.
   > Limitation: The candidate operates in the correct module and already checks for an approval message and display of loan account details (which satisfies the after_only requirement). However, it targets an Auto loan rather than the required Home loan, so it doesn't exactly match the requested loan type. If adjusted to select Home, it would fully satisfy the verification.

**4. [NAVIGATE]** Navigate to Open New Account
   > Navigate from Request Loan to Open New Account

**5. [POST-VERIFY] 4.ONA-002** -- Open a new Savings account with valid initial deposit
   > This test exercises opening a new account and verifies that the new account appears in Accounts Overview, so it covers the correct page and the act of checking the accounts listing. To use it for this requirement you would need to change the account type from Savings to a Home Loan (or otherwise adapt the test to create a loan-type account) and extend the expected checks to assert loan-type labeling and loan-specific detail fields are present and accessible.
   > Limitation: The candidate accesses Accounts Overview and checks that a newly opened account appears in the listing (good), but it opens a Savings account rather than a Home Loan and does not assert loan-type labeling or loan-specific details. Because execution_strategy is after_only, the verification must confirm the home loan entry and its loan details by itself — this test as written cannot do that.

**6. [POST-VERIFY] 7.REQLOA-010** -- Verify no actual balance debits occur after loan creation
   > Run 7.REQLOA-010 AGAIN and COMPARE with baseline values recorded in pre-verify
   > Limitation: Closest candidate shows the collateral account balance but operates on the Request Loan page (not the required Accounts Overview) and does not explicitly capture available funds or a collateral_hold indicator. Because the before_after execution only needs to observe relevant data, showing the balance is helpful, but missing the available-funds field and hold indicator means it is not a full match.

**Notes:** PRE: Record baseline with 7.REQLOA-010 → ACTION: Execute 7.REQLOA-003 → POST: Verify with 7.REQLOA-002, 4.ONA-002, 7.REQLOA-010 (compare against baseline)

---

### 7.REQLOA-010: Verify no actual balance debits occur after loan creation

**Coverage:** PARTIAL Partial
**Modifies State:** loan_creation, collateral_hold

**1. Verify the collateral account balance remains unchanged after loan creation (no actual debit)**

- **Status:** PARTIAL partial
- **Type:** -
- **Strategy:** Before/After
- **Matched Test:** 4.ONA-001 (Open a new Checking account with valid initial deposit)
- **Confidence:** 50%
- **Before Action:** Record the collateral account's balance_display and available funds on Accounts Overview before submitting the loan request
- **After Action:** Confirm the collateral account's balance_display and available funds are unchanged after the loan is created
- **Execution Note:** This test navigates to Accounts Overview (redirect after account creation) so it can be adapted to display the Accounts Overview. However it does not currently specify reading or recording the collateral account's balance_display or available funds. To use it for before_after verification, add explicit steps to open Accounts Overview and capture the collateral account's balance_display and available funds before the loan action, and repeat after the loan creation.
- **Reason:** The test is primarily an Open New Account scenario but includes a redirect to Accounts Overview; it does not explicitly access or record the specific account balance_display and available funds fields required for this verification.
- **Manual Step:** Before performing the loan action: 1) Navigate to Accounts Overview. 2) Locate the collateral account by account number/name. 3) Record 'balance_display' and 'available funds' values. After performing the loan action: 4) Re-open Accounts Overview, locate the same collateral account, and verify the recorded 'balance_display' and 'available funds' are unchanged.

**2. Verify the loan was created and the application status shows approved in Request Loan**

- **Status:** FOUND found
- **Type:** -
- **Strategy:** After Only
- **Matched Test:** 7.REQLOA-001 (Request a Personal loan with valid inputs)
- **Confidence:** 75%
- **Execution Note:** Use this test to verify the outcome after the action by checking the Request Loan module for the new loan record and confirming the displayed loan details and success message. Adapt the run to only perform the verification steps (navigate to Request Loan/listing or the applicant's loan history) and assert that loan_application_status equals 'Approved' and loan details are accessible. Do NOT re-run the 'Submit Loan Request' steps when using it purely as an after-only verification.

**Coverage Gaps:**
- The test is primarily an Open New Account scenario but includes a redirect to Accounts Overview; it does not explicitly access or record the specific account balance_display and available funds fields required for this verification.

#### Execution Plan

> **Strategy:** Run verification tests BEFORE and AFTER the action to compare values.

**1. [NAVIGATE]** Navigate to Open New Account
   > Navigate from Request Loan to Open New Account to record baseline data

**2. [PRE-VERIFY] 4.ONA-001** -- Open a new Checking account with valid initial deposit
   > Run 4.ONA-001 and RECORD the current values before the action
   > Limitation: The test is primarily an Open New Account scenario but includes a redirect to Accounts Overview; it does not explicitly access or record the specific account balance_display and available funds fields required for this verification.

**3. [NAVIGATE]** Navigate to Request Loan
   > Return to Request Loan to execute the action

**4. [ACTION] 7.REQLOA-010** -- Verify no actual balance debits occur after loan creation
   > Run 7.REQLOA-010 — this is the state-changing action being verified

**5. [NAVIGATE]** Navigate to Open New Account
   > Navigate from Request Loan to Open New Account to verify the change

**6. [POST-VERIFY] 4.ONA-001** -- Open a new Checking account with valid initial deposit
   > Run 4.ONA-001 AGAIN and COMPARE with baseline values recorded in pre-verify
   > Limitation: The test is primarily an Open New Account scenario but includes a redirect to Accounts Overview; it does not explicitly access or record the specific account balance_display and available funds fields required for this verification.

**7. [POST-VERIFY] 7.REQLOA-001** -- Request a Personal loan with valid inputs
   > Use this test to verify the outcome after the action by checking the Request Loan module for the new loan record and confirming the displayed loan details and success message. Adapt the run to only perform the verification steps (navigate to Request Loan/listing or the applicant's loan history) and assert that loan_application_status equals 'Approved' and loan details are accessible. Do NOT re-run the 'Submit Loan Request' steps when using it purely as an after-only verification.

**Notes:** PRE: Record baseline with 4.ONA-001 → ACTION: Execute 7.REQLOA-010 → POST: Verify with 4.ONA-001, 7.REQLOA-001 (compare against baseline)

---

### 8.UCI-001: Update profile with all valid contact fields

**Coverage:** PARTIAL Partial
**Modifies State:** user_profile_update, user_profile

**1. Verify the user's contact profile fields are updated and persisted**

- **Status:** PARTIAL partial
- **Type:** -
- **Strategy:** Before/After
- **Matched Test:** 8.UCI-005 (Submit with multiple fields failing format validation)
- **Confidence:** 64%
- **Before Action:** Record all visible contact_fields on the pre-filled profile form before making changes
- **After Action:** Re-open the profile form and confirm every contact field matches the new submitted values
- **Execution Note:** This test targets the Update Contact Info page and interacts with the contact fields (First Name, Last Name, Street Address, City, State, ZIP Code, Phone Number). To use it for a before_after verification run, remove or disable the steps that overwrite/submit the form; instead have the test simply open the profile form and read/record the visible values. The recorded values can then be compared by the before_after harness.
- **Reason:** Although the test operates on the correct module and does interact with the contact fields, as written it populates invalid formats and submits the form to verify validation errors. That submission would modify/interfere with the profile state and does not explicitly record the pre-filled field values needed for the before_after verification. Therefore it cannot be used as-is but could be adapted to serve as the observation step.
- **Manual Step:** Create/modify a verification test that: 1) Open the Update Contact Info/profile form for the target user; 2) Read and record the visible values for First Name, Last Name, Street Address, City, State, ZIP Code, and Phone Number (no edits or submits); 3) Return these values for comparison by the before_after harness. Repeat after the update action and compare recorded values.

**2. Verify the profile update confirmation message is displayed after submission**

- **Status:** PARTIAL partial
- **Type:** -
- **Strategy:** After Only
- **Matched Test:** 8.UCI-002 (Submit with all required fields empty)
- **Confidence:** 60%
- **Execution Note:** This test runs on the Update Contact Info page (correct module). To use it for verification you would need to modify its inputs to perform a successful update (provide all required fields with valid data) and then assert that a visible profile_update_status message like 'Profile updated successfully' appears and persists.
- **Reason:** All candidate tests operate on the correct module but they are negative/validation scenarios (empty or invalid fields) that expect validation errors, not a success confirmation message. Because the execution_strategy is after_only, the verification test must itself confirm the success message — none of the provided tests currently do that.
- **Manual Step:** Submit the Update Contact Info form with valid values for all required fields. After clicking 'Update Profile', verify that a visible confirmation message (e.g., 'Profile updated successfully') appears on the page and persists. Record the exact text and location of the profile_update_status element for automated assertion.

**Coverage Gaps:**
- Although the test operates on the correct module and does interact with the contact fields, as written it populates invalid formats and submits the form to verify validation errors. That submission would modify/interfere with the profile state and does not explicitly record the pre-filled field values needed for the before_after verification. Therefore it cannot be used as-is but could be adapted to serve as the observation step.
- All candidate tests operate on the correct module but they are negative/validation scenarios (empty or invalid fields) that expect validation errors, not a success confirmation message. Because the execution_strategy is after_only, the verification test must itself confirm the success message — none of the provided tests currently do that.

#### Execution Plan

> **Strategy:** Run verification tests BEFORE and AFTER the action to compare values.

**1. [PRE-VERIFY] 8.UCI-005** -- Submit with multiple fields failing format validation
   > Run 8.UCI-005 and RECORD the current values before the action
   > Limitation: Although the test operates on the correct module and does interact with the contact fields, as written it populates invalid formats and submits the form to verify validation errors. That submission would modify/interfere with the profile state and does not explicitly record the pre-filled field values needed for the before_after verification. Therefore it cannot be used as-is but could be adapted to serve as the observation step.

**2. [ACTION] 8.UCI-001** -- Update profile with all valid contact fields
   > Run 8.UCI-001 — this is the state-changing action being verified

**3. [POST-VERIFY] 8.UCI-005** -- Submit with multiple fields failing format validation
   > Run 8.UCI-005 AGAIN and COMPARE with baseline values recorded in pre-verify
   > Limitation: Although the test operates on the correct module and does interact with the contact fields, as written it populates invalid formats and submits the form to verify validation errors. That submission would modify/interfere with the profile state and does not explicitly record the pre-filled field values needed for the before_after verification. Therefore it cannot be used as-is but could be adapted to serve as the observation step.

**4. [POST-VERIFY] 8.UCI-002** -- Submit with all required fields empty
   > This test runs on the Update Contact Info page (correct module). To use it for verification you would need to modify its inputs to perform a successful update (provide all required fields with valid data) and then assert that a visible profile_update_status message like 'Profile updated successfully' appears and persists.
   > Limitation: All candidate tests operate on the correct module but they are negative/validation scenarios (empty or invalid fields) that expect validation errors, not a success confirmation message. Because the execution_strategy is after_only, the verification test must itself confirm the success message — none of the provided tests currently do that.

**Notes:** PRE: Record baseline with 8.UCI-005 → ACTION: Execute 8.UCI-001 → POST: Verify with 8.UCI-005, 8.UCI-002 (compare against baseline)

---

### 9.MANCAR-001: Request a new Debit card with valid linked account and complete shipping address

**Coverage:** PARTIAL Partial
**Modifies State:** card_request_creation

**1. Verify a new card request record was created and the UI displays the success message with tracking ID**

- **Status:** PARTIAL partial
- **Type:** -
- **Strategy:** After Only
- **Matched Test:** 9.MANCAR-002 (Request a new Credit card with valid linked account and complete shipping address)
- **Confidence:** 70%
- **Execution Note:** Use this test as the basis: it runs in Manage Cards and verifies the UI success notification with a tracking ID. To serve as the required after_only verification, modify/add steps to select Card Type = Debit (not Credit) and, after submission, open Manage Cards -> Requests/Request History and assert the most recent request entry fields (type and shipping address) match the expected values and that card_request_status reflects the new record.
- **Reason:** The candidate runs in the correct module and checks the success UI notification with tracking ID, but it requests a Credit card (requirement expects Debit) and does not verify the Requests/Request History entry or the saved shipping address/card_request_status. As written it cannot alone confirm the new record's type and address.
- **Manual Step:** After submitting the card request, open Manage Cards -> Requests/Request History and inspect the most recent entry: confirm type = Debit, shipping address matches the supplied address, and card_request_status indicates a created/requested state. Also verify the UI notification area shows 'Card request submitted successfully.' and includes a tracking ID.

**2. Verify the card request appears as a support/ticket entry so backend/support can track it**

- **Status:** MISSING not_found
- **Type:** -
- **Strategy:** After Only
- **Matched Test:** -
- **Confidence:** -
- **Reason:** None of the provided test cases both operate on the Support Center ticket listing/search page AND confirm a ticket exists referencing the card request. 13.SUPCEN-001 runs in Support Center and can show a created ticket ID for a sent message but does not search My Tickets or confirm a card-request ticket. 9.MANCAR-002 confirms a card request was submitted and shows a tracking ID in the Manage Cards UI but does not open the Support Center to verify the ticket record. 9.MANCAR-010 is irrelevant (negative case). Because the execution strategy is after_only, the verification must, by itself, confirm the ticket record in Support Center — no candidate performs that exact action.
- **Manual Step:** After submitting the card request, open Support Center -> My Tickets (or use Ticket Search). Enter the card request tracking ID (or filter by recent timestamp) and locate the corresponding ticket. Verify the ticket exists, that the ticket ID/tracking ID is present, and record the ticket status and any relevant details.

**Coverage Gaps:**
- The candidate runs in the correct module and checks the success UI notification with tracking ID, but it requests a Credit card (requirement expects Debit) and does not verify the Requests/Request History entry or the saved shipping address/card_request_status. As written it cannot alone confirm the new record's type and address.
- None of the provided test cases both operate on the Support Center ticket listing/search page AND confirm a ticket exists referencing the card request. 13.SUPCEN-001 runs in Support Center and can show a created ticket ID for a sent message but does not search My Tickets or confirm a card-request ticket. 9.MANCAR-002 confirms a card request was submitted and shows a tracking ID in the Manage Cards UI but does not open the Support Center to verify the ticket record. 9.MANCAR-010 is irrelevant (negative case). Because the execution strategy is after_only, the verification must, by itself, confirm the ticket record in Support Center — no candidate performs that exact action.

#### Execution Plan

**1. [ACTION] 9.MANCAR-001** -- Request a new Debit card with valid linked account and complete shipping address
   > Run 9.MANCAR-001 — this is the state-changing action being verified

**2. [POST-VERIFY] 9.MANCAR-002** -- Request a new Credit card with valid linked account and complete shipping address
   > Use this test as the basis: it runs in Manage Cards and verifies the UI success notification with a tracking ID. To serve as the required after_only verification, modify/add steps to select Card Type = Debit (not Credit) and, after submission, open Manage Cards -> Requests/Request History and assert the most recent request entry fields (type and shipping address) match the expected values and that card_request_status reflects the new record.
   > Limitation: The candidate runs in the correct module and checks the success UI notification with tracking ID, but it requests a Credit card (requirement expects Debit) and does not verify the Requests/Request History entry or the saved shipping address/card_request_status. As written it cannot alone confirm the new record's type and address.

**Notes:** Execute 9.MANCAR-001 → then verify with 9.MANCAR-002 → Manual verification needed for 1 item(s)

**Manual Verification Required:**
- Verify the card request appears as a support/ticket entry so backend/support can track it
  - Suggested: After submitting the card request, open Support Center -> My Tickets (or use Ticket Search). Enter the card request tracking ID (or filter by recent timestamp) and locate the corresponding ticket. Verify the ticket exists, that the ticket ID/tracking ID is present, and record the ticket status and any relevant details.

---

### 9.MANCAR-002: Request a new Credit card with valid linked account and complete shipping address

**Coverage:** PARTIAL Partial
**Modifies State:** card_request_creation

**1. Verify a new card request record was created and the UI displays the success message with tracking ID**

- **Status:** PARTIAL partial
- **Type:** -
- **Strategy:** After Only
- **Matched Test:** 9.MANCAR-001 (Request a new Debit card with valid linked account and complete shipping address)
- **Confidence:** 70%
- **Execution Note:** Use this test as the basis: it runs in the Manage Cards module and already verifies the UI success notification with a tracking ID. To serve as the after_only verification required here, modify the test to select Card Type = Credit (not Debit) and add a step after submission to open Manage Cards -> Requests/Request History and inspect the most recent request entry to verify the record's type is Credit and the shipping address matches the supplied address.
- **Reason:** The candidate operates on the correct module and verifies the UI success message with a tracking ID, but it requests a Debit card (requirement expects Credit) and does not explicitly check the Requests/Request History entry for the new record or verify the stored shipping address/type. Therefore it cannot by itself confirm the required post-action state.
- **Manual Step:** After performing the card request (select Card Type = Credit and submit with the intended shipping address), navigate to Manage Cards -> Requests/Request History. Confirm the top / most recent entry: a) request type = Credit; b) shipping address equals the supplied address; c) request status/card_request_status indicates creation; and also verify the UI notification area shows 'Card request submitted successfully.' with a tracking ID.

**2. Verify the card request appears as a support/ticket entry for tracking by support staff**

- **Status:** PARTIAL partial
- **Type:** -
- **Strategy:** After Only
- **Matched Test:** 13.SUPCEN-001 (Send message successfully with required fields (no attachment))
- **Confidence:** 65%
- **Execution Note:** This Support Center test displays a ticket ID after sending a message, which demonstrates the UI can show ticket IDs. However it is an outbound message creation flow (Send Message) rather than an explicit 'My Tickets' / 'Ticket Search' lookup of a card-request ticket. To use it for verification you would need to adapt it to: open Support Center -> My Tickets or Ticket Search and locate the ticket (match by tracking ID or card-request details) rather than sending a new message.
- **Reason:** Correct module (Support Center) and it does display a ticket ID on successful submission, but it does not perform the required lookup of an existing card-request ticket created earlier in the Manage Cards flow. Because execution_strategy is after_only, the verification test must itself confirm the card-request ticket exists in Support Center; 13.SUPCEN-001 as written confirms ticket creation for a message but does not verify the specific card-request ticket entry.
- **Manual Step:** After the card request action completes, open Support Center -> My Tickets (or Ticket Search). Enter the card request tracking ID (or search by request details such as account number, card type, or request date). Confirm a support ticket record exists with the matching tracking ID and that the ticket shows the request details and a visible ticket ID. Record the ticket ID and relevant fields (status, subject, description) to verify tracking by support staff.

**Coverage Gaps:**
- The candidate operates on the correct module and verifies the UI success message with a tracking ID, but it requests a Debit card (requirement expects Credit) and does not explicitly check the Requests/Request History entry for the new record or verify the stored shipping address/type. Therefore it cannot by itself confirm the required post-action state.
- Correct module (Support Center) and it does display a ticket ID on successful submission, but it does not perform the required lookup of an existing card-request ticket created earlier in the Manage Cards flow. Because execution_strategy is after_only, the verification test must itself confirm the card-request ticket exists in Support Center; 13.SUPCEN-001 as written confirms ticket creation for a message but does not verify the specific card-request ticket entry.

#### Execution Plan

**1. [ACTION] 9.MANCAR-002** -- Request a new Credit card with valid linked account and complete shipping address
   > Run 9.MANCAR-002 — this is the state-changing action being verified

**2. [POST-VERIFY] 9.MANCAR-001** -- Request a new Debit card with valid linked account and complete shipping address
   > Use this test as the basis: it runs in the Manage Cards module and already verifies the UI success notification with a tracking ID. To serve as the after_only verification required here, modify the test to select Card Type = Credit (not Debit) and add a step after submission to open Manage Cards -> Requests/Request History and inspect the most recent request entry to verify the record's type is Credit and the shipping address matches the supplied address.
   > Limitation: The candidate operates on the correct module and verifies the UI success message with a tracking ID, but it requests a Debit card (requirement expects Credit) and does not explicitly check the Requests/Request History entry for the new record or verify the stored shipping address/type. Therefore it cannot by itself confirm the required post-action state.

**3. [NAVIGATE]** Navigate to Support Center
   > Navigate from Manage Cards to Support Center

**4. [POST-VERIFY] 13.SUPCEN-001** -- Send message successfully with required fields (no attachment)
   > This Support Center test displays a ticket ID after sending a message, which demonstrates the UI can show ticket IDs. However it is an outbound message creation flow (Send Message) rather than an explicit 'My Tickets' / 'Ticket Search' lookup of a card-request ticket. To use it for verification you would need to adapt it to: open Support Center -> My Tickets or Ticket Search and locate the ticket (match by tracking ID or card-request details) rather than sending a new message.
   > Limitation: Correct module (Support Center) and it does display a ticket ID on successful submission, but it does not perform the required lookup of an existing card-request ticket created earlier in the Manage Cards flow. Because execution_strategy is after_only, the verification test must itself confirm the card-request ticket exists in Support Center; 13.SUPCEN-001 as written confirms ticket creation for a message but does not verify the specific card-request ticket entry.

**Notes:** Execute 9.MANCAR-002 → then verify with 9.MANCAR-001, 13.SUPCEN-001

---

### 9.MANCAR-003: Update spending limit with a valid amount

**Coverage:** FULL Full
**Modifies State:** card_control_update, spending_limit

**1. Verify the spending limit on the selected card was updated to the new numeric amount**

- **Status:** FOUND found
- **Type:** -
- **Strategy:** Before/After
- **Matched Test:** 9.MANCAR-012 (Reject non-numeric spending limit value)
- **Confidence:** 78%
- **Before Action:** Record the card's current spending limit value for the selected card before submitting the update
- **After Action:** Confirm the spending limit value now equals the new amount and differs from the recorded before value by the expected delta
- **Execution Note:** Use this test to open Manage Cards, select the existing card and access the 'New Spending Limit' / controls section to read and record the current spending_limit value. Run it once BEFORE the update to capture the baseline value and AGAIN AFTER the update to read the new value for comparison.

**2. Verify the UI shows a confirmation that controls were updated successfully**

- **Status:** FOUND found
- **Type:** -
- **Strategy:** After Only
- **Matched Test:** 9.MANCAR-007 (Update controls without adding a travel notice (travel notice optional))
- **Confidence:** 92%
- **Execution Note:** Use this test after performing the Update Controls action. It exercises the Manage Cards page, submits Update Controls, and explicitly expects the 'Card controls updated successfully.' notification and a successful update — suitable for after_only verification. Confirm the notification appears and the controls view shows the new spending limit.

#### Execution Plan

> **Strategy:** Run verification tests BEFORE and AFTER the action to compare values.

**1. [PRE-VERIFY] 9.MANCAR-012** -- Reject non-numeric spending limit value
   > Run 9.MANCAR-012 and RECORD the current values before the action

**2. [ACTION] 9.MANCAR-003** -- Update spending limit with a valid amount
   > Run 9.MANCAR-003 — this is the state-changing action being verified

**3. [POST-VERIFY] 9.MANCAR-012** -- Reject non-numeric spending limit value
   > Run 9.MANCAR-012 AGAIN and COMPARE with baseline values recorded in pre-verify

**4. [POST-VERIFY] 9.MANCAR-007** -- Update controls without adding a travel notice (travel notice optional)
   > Use this test after performing the Update Controls action. It exercises the Manage Cards page, submits Update Controls, and explicitly expects the 'Card controls updated successfully.' notification and a successful update — suitable for after_only verification. Confirm the notification appears and the controls view shows the new spending limit.

**Notes:** PRE: Record baseline with 9.MANCAR-012 → ACTION: Execute 9.MANCAR-003 → POST: Verify with 9.MANCAR-012, 9.MANCAR-007 (compare against baseline)

---

### 9.MANCAR-004: Freeze an active card by updating Card Status

**Coverage:** PARTIAL Partial
**Modifies State:** card_control_update, card_status

**1. Verify the selected card's status changed to Frozen and is displayed as such in the card detail**

- **Status:** PARTIAL partial
- **Type:** -
- **Strategy:** After Only
- **Matched Test:** 9.MANCAR-007 (Update controls without adding a travel notice (travel notice optional))
- **Confidence:** 60%
- **Execution Note:** This test runs on the correct Manage Cards page and selects an existing card and updates controls (including Card Status). However it only asserts the success message and does not explicitly verify the card's status badge/field. To use it for after_only verification, add a final step after Update Controls that re-opens/selects the same card and asserts the Card Status badge/field text equals 'Frozen'.
- **Reason:** All three candidates operate in the Manage Cards module and allow selecting a card and setting Card Status, but none include an explicit assertion that the card detail/status badge displays the new status. Because the execution_strategy is after_only, the test must confirm the outcome by itself; the candidate only confirms a success message, not the displayed card_status.
- **Manual Step:** After performing the update, open Manage Cards → select the same card → verify the status badge/field displays exactly 'Frozen'.

**2. Verify a confirmation is shown indicating controls were updated successfully**

- **Status:** FOUND found
- **Type:** -
- **Strategy:** After Only
- **Matched Test:** 9.MANCAR-007 (Update controls without adding a travel notice (travel notice optional))
- **Confidence:** 90%
- **Execution Note:** Run this test immediately after performing Update Controls. Observe the notification/confirmation area and assert that the exact text 'Card controls updated successfully.' is displayed.

**Coverage Gaps:**
- All three candidates operate in the Manage Cards module and allow selecting a card and setting Card Status, but none include an explicit assertion that the card detail/status badge displays the new status. Because the execution_strategy is after_only, the test must confirm the outcome by itself; the candidate only confirms a success message, not the displayed card_status.

#### Execution Plan

**1. [ACTION] 9.MANCAR-004** -- Freeze an active card by updating Card Status
   > Run 9.MANCAR-004 — this is the state-changing action being verified

**2. [POST-VERIFY] 9.MANCAR-007** -- Update controls without adding a travel notice (travel notice optional)
   > This test runs on the correct Manage Cards page and selects an existing card and updates controls (including Card Status). However it only asserts the success message and does not explicitly verify the card's status badge/field. To use it for after_only verification, add a final step after Update Controls that re-opens/selects the same card and asserts the Card Status badge/field text equals 'Frozen'.
   > Limitation: All three candidates operate in the Manage Cards module and allow selecting a card and setting Card Status, but none include an explicit assertion that the card detail/status badge displays the new status. Because the execution_strategy is after_only, the test must confirm the outcome by itself; the candidate only confirms a success message, not the displayed card_status.

**3. [POST-VERIFY] 9.MANCAR-007** -- Update controls without adding a travel notice (travel notice optional)
   > Run this test immediately after performing Update Controls. Observe the notification/confirmation area and assert that the exact text 'Card controls updated successfully.' is displayed.

**Notes:** Execute 9.MANCAR-004 → then verify with 9.MANCAR-007, 9.MANCAR-007

---

### 9.MANCAR-006: Add a travel notice with valid dates and destination

**Coverage:** PARTIAL Partial
**Modifies State:** card_control_update, card_controls

**1. Verify the travel notice (start date, end date, destination) is saved and visible in the card controls**

- **Status:** PARTIAL partial
- **Type:** -
- **Strategy:** After Only
- **Matched Test:** 9.MANCAR-013 (Reject travel notice with end date before start date)
- **Confidence:** 60%
- **Execution Note:** This test runs in the Manage Cards module and exercises the Travel Notice fields, so it is the closest candidate. However it verifies a negative validation (end date before start date) and expects the travel notice NOT to be saved. For after_only verification of a successfully saved travel notice you would need to modify this test to submit a valid travel notice (correct start/end dates and destination) and then inspect the Travel Notice section in the card controls to confirm the entry.
- **Reason:** None of the provided candidates confirm that a travel notice was saved and visible in the card controls after an update. 9.MANCAR-013 interacts with travel notice fields but asserts a validation failure (travel notice not saved). The other candidates (9.MANCAR-007, 9.MANCAR-003) leave travel notice empty and therefore do not verify a stored travel notice either.
- **Manual Step:** After performing the action that supposedly created the travel notice, open Manage Cards -> select the same card -> expand/view the Travel Notice section in the card controls. Verify there is a travel notice entry whose start date, end date, and destination exactly match the submitted values. (Also confirm the card_controls state reflects the entry.)

**2. Verify the UI shows a confirmation that controls were updated successfully after adding the travel notice**

- **Status:** PARTIAL partial
- **Type:** -
- **Strategy:** After Only
- **Matched Test:** 9.MANCAR-007 (Update controls without adding a travel notice (travel notice optional))
- **Confidence:** 72%
- **Execution Note:** This test runs on the correct Manage Cards page and already asserts the 'Card controls updated successfully.' confirmation. However it intentionally leaves Travel Notice fields empty, so it does not verify that a travel notice was added or is present in the controls. For after_only verification use, extend this test to populate a valid Travel Notice, submit, then assert both the confirmation message and that the travel notice appears in the card controls.
- **Reason:** Closest match because it verifies the success notification on the same page, but it does not add or check a travel notice. The requirement needs confirmation message plus presence of the travel notice, which this test does not cover.
- **Manual Step:** On Manage Cards select the card and fill Travel Notice (location, start date, end date) plus any other required fields; click 'Update Controls'. After submission, confirm the UI shows the exact notification 'Card controls updated successfully.' and verify the card controls section lists the newly added travel notice (correct dates/location).

**Coverage Gaps:**
- None of the provided candidates confirm that a travel notice was saved and visible in the card controls after an update. 9.MANCAR-013 interacts with travel notice fields but asserts a validation failure (travel notice not saved). The other candidates (9.MANCAR-007, 9.MANCAR-003) leave travel notice empty and therefore do not verify a stored travel notice either.
- Closest match because it verifies the success notification on the same page, but it does not add or check a travel notice. The requirement needs confirmation message plus presence of the travel notice, which this test does not cover.

#### Execution Plan

**1. [ACTION] 9.MANCAR-006** -- Add a travel notice with valid dates and destination
   > Run 9.MANCAR-006 — this is the state-changing action being verified

**2. [POST-VERIFY] 9.MANCAR-013** -- Reject travel notice with end date before start date
   > This test runs in the Manage Cards module and exercises the Travel Notice fields, so it is the closest candidate. However it verifies a negative validation (end date before start date) and expects the travel notice NOT to be saved. For after_only verification of a successfully saved travel notice you would need to modify this test to submit a valid travel notice (correct start/end dates and destination) and then inspect the Travel Notice section in the card controls to confirm the entry.
   > Limitation: None of the provided candidates confirm that a travel notice was saved and visible in the card controls after an update. 9.MANCAR-013 interacts with travel notice fields but asserts a validation failure (travel notice not saved). The other candidates (9.MANCAR-007, 9.MANCAR-003) leave travel notice empty and therefore do not verify a stored travel notice either.

**3. [POST-VERIFY] 9.MANCAR-007** -- Update controls without adding a travel notice (travel notice optional)
   > This test runs on the correct Manage Cards page and already asserts the 'Card controls updated successfully.' confirmation. However it intentionally leaves Travel Notice fields empty, so it does not verify that a travel notice was added or is present in the controls. For after_only verification use, extend this test to populate a valid Travel Notice, submit, then assert both the confirmation message and that the travel notice appears in the card controls.
   > Limitation: Closest match because it verifies the success notification on the same page, but it does not add or check a travel notice. The requirement needs confirmation message plus presence of the travel notice, which this test does not cover.

**Notes:** Execute 9.MANCAR-006 → then verify with 9.MANCAR-013, 9.MANCAR-007

---

### 9.MANCAR-007: Update controls without adding a travel notice (travel notice optional)

**Coverage:** PARTIAL Partial
**Modifies State:** card_control_update

**1. Verify Update Controls succeeds without creating a travel notice (no travel notice added)**

- **Status:** FOUND found
- **Type:** -
- **Strategy:** Before/After
- **Matched Test:** 9.MANCAR-003 (Update spending limit with a valid amount)
- **Confidence:** 75%
- **Before Action:** Record whether a travel notice exists and its details (or note 'none') for the selected card before submitting
- **After Action:** Confirm that after the update the travel notice existence/details are unchanged (still none or identical to before)
- **Execution Note:** Use this test to run the required before/after observations. Select the same existing card and open the Manage Cards controls (record the Travel Notice area contents — 'none' or full details). Execute the test (leave Travel Notice fields empty and click 'Update Controls'). Run the same test again after the action to re-open the controls and record the Travel Notice contents for comparison.

**2. Verify the UI displays a success confirmation that card controls were updated**

- **Status:** PARTIAL partial
- **Type:** -
- **Strategy:** After Only
- **Matched Test:** 9.MANCAR-003 (Update spending limit with a valid amount)
- **Confidence:** 68%
- **Execution Note:** Use this Manage Cards test as the base: it already submits Update Controls with Travel Notice left empty and verifies the success message and updated spending limit. To fully satisfy the after_only verification, add an explicit assertion after submission that (a) the notification/confirmation area contains exactly 'Card controls updated successfully.' and (b) the travel-notice entry is not present in the controls UI (e.g., travel notice list empty, or no travel notice row shown for the card).
- **Reason:** This test runs on the correct module and uses an empty Travel Notice (matches the scenario) and already checks for the success confirmation, but it does not currently assert that no travel notice entry was added. Because the execution_strategy is after_only, the test must explicitly confirm absence of a travel notice; as-written it only confirms the spending limit update.
- **Manual Step:** After clicking 'Update Controls', observe the notification area and confirm the text 'Card controls updated successfully.' is displayed. Then inspect the card controls/details to confirm there is no travel notice entry for the card (no travel notice row, dates, or destination present). If automating, add assertions that verify the notification text and that the travel notice element is absent or empty.

**Coverage Gaps:**
- This test runs on the correct module and uses an empty Travel Notice (matches the scenario) and already checks for the success confirmation, but it does not currently assert that no travel notice entry was added. Because the execution_strategy is after_only, the test must explicitly confirm absence of a travel notice; as-written it only confirms the spending limit update.

#### Execution Plan

> **Strategy:** Run verification tests BEFORE and AFTER the action to compare values.

**1. [PRE-VERIFY] 9.MANCAR-003** -- Update spending limit with a valid amount
   > Run 9.MANCAR-003 and RECORD the current values before the action

**2. [ACTION] 9.MANCAR-007** -- Update controls without adding a travel notice (travel notice optional)
   > Run 9.MANCAR-007 — this is the state-changing action being verified

**3. [POST-VERIFY] 9.MANCAR-003** -- Update spending limit with a valid amount
   > Run 9.MANCAR-003 AGAIN and COMPARE with baseline values recorded in pre-verify

**4. [POST-VERIFY] 9.MANCAR-003** -- Update spending limit with a valid amount
   > Use this Manage Cards test as the base: it already submits Update Controls with Travel Notice left empty and verifies the success message and updated spending limit. To fully satisfy the after_only verification, add an explicit assertion after submission that (a) the notification/confirmation area contains exactly 'Card controls updated successfully.' and (b) the travel-notice entry is not present in the controls UI (e.g., travel notice list empty, or no travel notice row shown for the card).
   > Limitation: This test runs on the correct module and uses an empty Travel Notice (matches the scenario) and already checks for the success confirmation, but it does not currently assert that no travel notice entry was added. Because the execution_strategy is after_only, the test must explicitly confirm absence of a travel notice; as-written it only confirms the spending limit update.

**Notes:** PRE: Record baseline with 9.MANCAR-003 → ACTION: Execute 9.MANCAR-007 → POST: Verify with 9.MANCAR-003, 9.MANCAR-003 (compare against baseline)

---

### 10.INVEST-001: Execute a Buy trade successfully and update holdings

**Coverage:** FULL Full
**Modifies State:** trade_execution, cash_balance, fund_holdings

**1. Verify the trade confirmation is shown with a success message and an order ID**

- **Status:** FOUND found
- **Type:** -
- **Strategy:** After Only
- **Matched Test:** 10.INVEST-002 (Execute a Sell trade successfully and update holdings)
- **Confidence:** 85%
- **Execution Note:** Run this test after executing the trade (change Action to Buy if the test currently performs Sell). Verify the confirmation area displays 'Trade executed successfully.' with a visible order ID and the trade details: fund symbol, quantity, executed price and executed time. This single after-only check confirms the trade_status via the UI confirmation.

**2. Verify the fund holdings increased by the purchased quantity in the portfolio snapshot**

- **Status:** FOUND found
- **Type:** -
- **Strategy:** Before/After
- **Matched Test:** 10.INVEST-007 (Portfolio snapshot displays current holdings and read-only values)
- **Confidence:** 90%
- **Before Action:** Record current holdings quantity for the fund in the portfolio snapshot before placing the buy order
- **After Action:** Confirm the holdings quantity equals the recorded before value plus the purchased quantity
- **Execution Note:** Use this test to open the Investments > Portfolio snapshot panel and read/display the current holdings for the selected fund (including the quantity). Run once BEFORE placing the buy to record the fund_holdings quantity, then run again AFTER the trade and compare the recorded before value + purchased quantity to the after value.

**3. Verify the funding account's cash balance decreased by the trade cash amount**

- **Status:** FOUND found
- **Type:** -
- **Strategy:** Before/After
- **Matched Test:** 3.ACCOVE-003 (Footer displays the total balance across all accounts)
- **Confidence:** 85%
- **Before Action:** Record the funding account's current balance shown on Accounts Overview before executing the trade
- **After Action:** Confirm the funding account balance decreased by the executed trade cash amount and matches expected post-trade balance
- **Execution Note:** Use this Accounts Overview test to read and record the 'Current Balance' value from the specific funding account row before the trade and again after the trade. Because execution_strategy is before_after, the test only needs to surface the account_balance (Current Balance) for the selected account; the pre/post comparison will be done externally to confirm the balance decreased by quantity * executed price.

#### Execution Plan

> **Strategy:** Run verification tests BEFORE and AFTER the action to compare values.

**1. [PRE-VERIFY] 10.INVEST-007** -- Portfolio snapshot displays current holdings and read-only values
   > Run 10.INVEST-007 and RECORD the current values before the action

**2. [NAVIGATE]** Navigate to Accounts Overview
   > Navigate from Investments to Accounts Overview to record baseline data

**3. [PRE-VERIFY] 3.ACCOVE-003** -- Footer displays the total balance across all accounts
   > Run 3.ACCOVE-003 and RECORD the current values before the action

**4. [NAVIGATE]** Navigate to Investments
   > Return to Investments to execute the action

**5. [ACTION] 10.INVEST-001** -- Execute a Buy trade successfully and update holdings
   > Run 10.INVEST-001 — this is the state-changing action being verified

**6. [POST-VERIFY] 10.INVEST-002** -- Execute a Sell trade successfully and update holdings
   > Run this test after executing the trade (change Action to Buy if the test currently performs Sell). Verify the confirmation area displays 'Trade executed successfully.' with a visible order ID and the trade details: fund symbol, quantity, executed price and executed time. This single after-only check confirms the trade_status via the UI confirmation.

**7. [POST-VERIFY] 10.INVEST-007** -- Portfolio snapshot displays current holdings and read-only values
   > Run 10.INVEST-007 AGAIN and COMPARE with baseline values recorded in pre-verify

**8. [NAVIGATE]** Navigate to Accounts Overview
   > Navigate from Investments to Accounts Overview to verify the change

**9. [POST-VERIFY] 3.ACCOVE-003** -- Footer displays the total balance across all accounts
   > Run 3.ACCOVE-003 AGAIN and COMPARE with baseline values recorded in pre-verify

**Notes:** PRE: Record baseline with 10.INVEST-007, 3.ACCOVE-003 → ACTION: Execute 10.INVEST-001 → POST: Verify with 10.INVEST-002, 10.INVEST-007, 3.ACCOVE-003 (compare against baseline)

---

### 10.INVEST-002: Execute a Sell trade successfully and update holdings

**Coverage:** PARTIAL Partial
**Modifies State:** trade_execution, cash_balance, fund_holdings

**1. Verify the sell trade confirmation is shown with a success message and an order ID**

- **Status:** PARTIAL partial
- **Type:** -
- **Strategy:** After Only
- **Matched Test:** 10.INVEST-001 (Execute a Buy trade successfully and update holdings)
- **Confidence:** 78%
- **Execution Note:** Test 10.INVEST-001 exercises the Investments confirmation area and verifies the success message and order details, but it uses Action = Buy. For after_only verification of a SELL trade, reuse this test but set Action to Sell (or parameterize the action). After executing the sell, confirm the confirmation area displays 'Trade executed successfully.', a visible order ID, and trade details (fund symbol, quantity, executed price/time). Also verify trade_status indicates execution.
- **Reason:** The test targets the correct module and checks the confirmation UI (success message and order details), which is exactly what must be observed after a trade. However, it specifically executes a Buy trade rather than a Sell; the requirement demands verifying a Sell trade confirmation, so the candidate does not fully match as-is.
- **Manual Step:** Manually execute a Sell trade in Investments with valid fund symbol, quantity, and funding account. After execution, inspect the trade confirmation/receipt area and confirm: 1) the message 'Trade executed successfully.' is shown, 2) an order ID is displayed, 3) trade details are present (fund symbol, quantity, executed price and time), and 4) trade_status reflects the executed state (e.g., 'Executed' or similar). If automating, modify 10.INVEST-001 to set Action = Sell and include assertions for order ID, trade details, and trade_status.

**2. Verify the fund holdings decreased by the sold quantity in the portfolio snapshot**

- **Status:** FOUND found
- **Type:** -
- **Strategy:** Before/After
- **Matched Test:** 10.INVEST-007 (Portfolio snapshot displays current holdings and read-only values)
- **Confidence:** 90%
- **Before Action:** Record current holdings quantity for the fund in the portfolio snapshot before placing the sell order
- **After Action:** Confirm the holdings quantity equals the recorded before value minus the sold quantity
- **Execution Note:** Run this test against the Investments > Portfolio snapshot panel both BEFORE and AFTER the sell. It displays the current fund holdings (including quantity), which is sufficient under the before_after strategy to record the baseline and later re-check the value.

**3. Verify proceeds from the sale increased the selected destination account's cash balance**

- **Status:** FOUND found
- **Type:** -
- **Strategy:** Before/After
- **Matched Test:** 3.ACCOVE-003 (Footer displays the total balance across all accounts)
- **Confidence:** 90%
- **Before Action:** Record the destination account's current balance on Accounts Overview before executing the sell
- **After Action:** Confirm the account balance increased by the expected proceeds amount and matches expected post-trade balance
- **Execution Note:** Run this Accounts Overview test before the sell to read and record the 'Current Balance' value for the destination account row, then run it again after the sell to obtain the post-trade balance. Compare the two recorded balances against the expected increase (quantity * executed price minus fees). If needed, adapt the test to target a specific account row (by account number) so it returns the numeric balance for that destination account.

**Coverage Gaps:**
- The test targets the correct module and checks the confirmation UI (success message and order details), which is exactly what must be observed after a trade. However, it specifically executes a Buy trade rather than a Sell; the requirement demands verifying a Sell trade confirmation, so the candidate does not fully match as-is.

#### Execution Plan

> **Strategy:** Run verification tests BEFORE and AFTER the action to compare values.

**1. [PRE-VERIFY] 10.INVEST-007** -- Portfolio snapshot displays current holdings and read-only values
   > Run 10.INVEST-007 and RECORD the current values before the action

**2. [NAVIGATE]** Navigate to Accounts Overview
   > Navigate from Investments to Accounts Overview to record baseline data

**3. [PRE-VERIFY] 3.ACCOVE-003** -- Footer displays the total balance across all accounts
   > Run 3.ACCOVE-003 and RECORD the current values before the action

**4. [NAVIGATE]** Navigate to Investments
   > Return to Investments to execute the action

**5. [ACTION] 10.INVEST-002** -- Execute a Sell trade successfully and update holdings
   > Run 10.INVEST-002 — this is the state-changing action being verified

**6. [POST-VERIFY] 10.INVEST-001** -- Execute a Buy trade successfully and update holdings
   > Test 10.INVEST-001 exercises the Investments confirmation area and verifies the success message and order details, but it uses Action = Buy. For after_only verification of a SELL trade, reuse this test but set Action to Sell (or parameterize the action). After executing the sell, confirm the confirmation area displays 'Trade executed successfully.', a visible order ID, and trade details (fund symbol, quantity, executed price/time). Also verify trade_status indicates execution.
   > Limitation: The test targets the correct module and checks the confirmation UI (success message and order details), which is exactly what must be observed after a trade. However, it specifically executes a Buy trade rather than a Sell; the requirement demands verifying a Sell trade confirmation, so the candidate does not fully match as-is.

**7. [POST-VERIFY] 10.INVEST-007** -- Portfolio snapshot displays current holdings and read-only values
   > Run 10.INVEST-007 AGAIN and COMPARE with baseline values recorded in pre-verify

**8. [NAVIGATE]** Navigate to Accounts Overview
   > Navigate from Investments to Accounts Overview to verify the change

**9. [POST-VERIFY] 3.ACCOVE-003** -- Footer displays the total balance across all accounts
   > Run 3.ACCOVE-003 AGAIN and COMPARE with baseline values recorded in pre-verify

**Notes:** PRE: Record baseline with 10.INVEST-007, 3.ACCOVE-003 → ACTION: Execute 10.INVEST-002 → POST: Verify with 10.INVEST-001, 10.INVEST-007, 3.ACCOVE-003 (compare against baseline)

---

### 10.INVEST-003: Create recurring investment plan with Weekly frequency

**Coverage:** PARTIAL Partial
**Modifies State:** trade_execution, fund_holdings

**1. Verify the recurring investment plan is created and confirmation message is shown**

- **Status:** PARTIAL partial
- **Type:** -
- **Strategy:** After Only
- **Matched Test:** 10.INVEST-004 (Create recurring investment plan with Monthly frequency)
- **Confidence:** 65%
- **Execution Note:** This test runs on the Investments module and verifies the confirmation message and that a recurring plan is created. To be used for the requested after_only verification it must be adjusted to: select Weekly frequency (instead of Monthly), and add post-creation verification steps that open the user's Recurring/Scheduled Plans list and assert a new active scheduled plan exists with the correct fund symbol, contribution amount, start date, funding account and trade_status (e.g., 'active').
- **Reason:** Although it verifies creation and the 'Plan created successfully.' message, it uses Monthly frequency (requirement needs Weekly) and does not include checks of the scheduled plans list or the trade_status. The other candidates are validation/error cases and do not verify successful creation.
- **Manual Step:** After creating the plan (set Frequency = Weekly): 1) Confirm confirmation area displays 'Plan created successfully.'; 2) Navigate to Investments → Recurring/Scheduled Plans; 3) Locate the new plan and verify: Frequency = Weekly, Fund Symbol = selected symbol, Contribution Amount = entered amount, Start Date = entered start date, Funding Account = selected account; 4) Verify the plan's trade_status is 'active' (or the expected active status value). If any automated test cannot check the scheduled list or trade_status, perform these verifications manually.

**2. Verify the new recurring plan appears in the portfolio/plan listing (plan stored for future executions)**

- **Status:** PARTIAL partial
- **Type:** -
- **Strategy:** After Only
- **Matched Test:** 10.INVEST-004 (Create recurring investment plan with Monthly frequency)
- **Confidence:** 60%
- **Execution Note:** This test runs in the Investments module and creates a recurring plan, but it only asserts a success message and uses Monthly frequency. To serve as the after-only verification, modify or extend it to: (1) select Weekly frequency when creating the plan (or create the plan via the prior action under test), then (2) navigate to Investments -> Recurring Plans (Scheduled Plans) and locate the plan by fund and start date, and (3) assert the listed plan shows frequency = Weekly, next run date matches the start date/schedule, and the correct funding account.
- **Reason:** Closest match is a create-recurring-plan test in the correct module, but it does not open the Recurring Plans listing or assert stored plan attributes. It also uses Monthly frequency in the test (mismatch with expected Weekly). As an after_only verification, the test must confirm the new record exists in the listing with the specified attributes; the candidate currently does not do that.
- **Manual Step:** After the plan creation action, open Investments -> Recurring Plans (Scheduled Plans), filter or search by the fund symbol and start date, and confirm the listed plan shows: frequency = Weekly, next run date matching the start date/schedule, and the correct funding account. If automating, add these verification steps to the test.

**Coverage Gaps:**
- Although it verifies creation and the 'Plan created successfully.' message, it uses Monthly frequency (requirement needs Weekly) and does not include checks of the scheduled plans list or the trade_status. The other candidates are validation/error cases and do not verify successful creation.
- Closest match is a create-recurring-plan test in the correct module, but it does not open the Recurring Plans listing or assert stored plan attributes. It also uses Monthly frequency in the test (mismatch with expected Weekly). As an after_only verification, the test must confirm the new record exists in the listing with the specified attributes; the candidate currently does not do that.

#### Execution Plan

**1. [ACTION] 10.INVEST-003** -- Create recurring investment plan with Weekly frequency
   > Run 10.INVEST-003 — this is the state-changing action being verified

**2. [POST-VERIFY] 10.INVEST-004** -- Create recurring investment plan with Monthly frequency
   > This test runs on the Investments module and verifies the confirmation message and that a recurring plan is created. To be used for the requested after_only verification it must be adjusted to: select Weekly frequency (instead of Monthly), and add post-creation verification steps that open the user's Recurring/Scheduled Plans list and assert a new active scheduled plan exists with the correct fund symbol, contribution amount, start date, funding account and trade_status (e.g., 'active').
   > Limitation: Although it verifies creation and the 'Plan created successfully.' message, it uses Monthly frequency (requirement needs Weekly) and does not include checks of the scheduled plans list or the trade_status. The other candidates are validation/error cases and do not verify successful creation.

**3. [POST-VERIFY] 10.INVEST-004** -- Create recurring investment plan with Monthly frequency
   > This test runs in the Investments module and creates a recurring plan, but it only asserts a success message and uses Monthly frequency. To serve as the after-only verification, modify or extend it to: (1) select Weekly frequency when creating the plan (or create the plan via the prior action under test), then (2) navigate to Investments -> Recurring Plans (Scheduled Plans) and locate the plan by fund and start date, and (3) assert the listed plan shows frequency = Weekly, next run date matches the start date/schedule, and the correct funding account.
   > Limitation: Closest match is a create-recurring-plan test in the correct module, but it does not open the Recurring Plans listing or assert stored plan attributes. It also uses Monthly frequency in the test (mismatch with expected Weekly). As an after_only verification, the test must confirm the new record exists in the listing with the specified attributes; the candidate currently does not do that.

**Notes:** Execute 10.INVEST-003 → then verify with 10.INVEST-004, 10.INVEST-004

---

### 10.INVEST-004: Create recurring investment plan with Monthly frequency

**Coverage:** PARTIAL Partial
**Modifies State:** trade_execution, fund_holdings

**1. Verify the recurring investment plan is created and confirmation message is shown**

- **Status:** PARTIAL partial
- **Type:** -
- **Strategy:** After Only
- **Matched Test:** 10.INVEST-003 (Create recurring investment plan with Weekly frequency)
- **Confidence:** 65%
- **Execution Note:** Use this test as the basis: it runs on the Investments page, creates a recurring plan and asserts the confirmation message. To meet the after_only verification requirements, extend the test to select Monthly frequency (instead of Weekly) and, after creation, navigate to the user's Recurring/Scheduled Plans list and assert a newly created active plan row exists with Monthly frequency, the chosen fund symbol, contribution amount, start date and funding account. Also assert the trade_status field/state for that plan is active.
- **Reason:** This candidate is on the correct module and already checks for the confirmation message and that the schedule is stored, but it uses Weekly frequency (requirement expects Monthly) and does not explicitly verify the presence and full details of the scheduled plan record or the plan's trade_status in the user's Recurring/Scheduled Plans list. Therefore it cannot fully confirm the after-only expected outcome without modification.
- **Manual Step:** After creating the plan, confirm the UI shows 'Plan created successfully.' Then go to Investments → Recurring/Scheduled Plans and verify there is an active plan entry with Frequency = Monthly, Fund Symbol = <selected symbol>, Contribution Amount = <amount>, Start Date = <date>, Funding Account = <account> and that the plan's trade_status (or status column) is 'active' (or equivalent).

**2. Verify the new recurring plan appears in the plans listing with the correct schedule**

- **Status:** PARTIAL partial
- **Type:** -
- **Strategy:** After Only
- **Matched Test:** 10.INVEST-003 (Create recurring investment plan with Weekly frequency)
- **Confidence:** 60%
- **Execution Note:** This test operates in the Investments module and exercises recurring plan creation, but it only verifies creation via a success message and uses Weekly frequency. To serve as the after_only verification, modify or extend it to: (1) create the plan with Frequency=Monthly and the intended Start Date, (2) after creation navigate to Investments -> Recurring Plans (Scheduled Plans), (3) locate the plan by Fund and Start Date, and (4) assert the listed Frequency is 'Monthly' and the Next Run Date matches the configured schedule.
- **Reason:** The candidate is on the correct module and concerns recurring plans, but it does not access the Recurring Plans listing nor assert the plan's frequency or next run date. As written it cannot, by itself, confirm the expected outcome required by an after_only verification.
- **Manual Step:** After the plan creation action completes, open Investments -> Recurring Plans (or Scheduled Plans). Filter or search by the Fund Symbol and Start Date used when creating the plan. Confirm a matching plan record exists. Verify the Frequency field equals 'Monthly' and that the Next Run Date shown corresponds to the start date and the monthly schedule (e.g., if Start Date = YYYY-MM-DD, next run should be the next monthly occurrence per system rules). Record screenshots of the listing row showing Fund, Start Date, Frequency, and Next Run Date.

**Coverage Gaps:**
- This candidate is on the correct module and already checks for the confirmation message and that the schedule is stored, but it uses Weekly frequency (requirement expects Monthly) and does not explicitly verify the presence and full details of the scheduled plan record or the plan's trade_status in the user's Recurring/Scheduled Plans list. Therefore it cannot fully confirm the after-only expected outcome without modification.
- The candidate is on the correct module and concerns recurring plans, but it does not access the Recurring Plans listing nor assert the plan's frequency or next run date. As written it cannot, by itself, confirm the expected outcome required by an after_only verification.

#### Execution Plan

**1. [ACTION] 10.INVEST-004** -- Create recurring investment plan with Monthly frequency
   > Run 10.INVEST-004 — this is the state-changing action being verified

**2. [POST-VERIFY] 10.INVEST-003** -- Create recurring investment plan with Weekly frequency
   > Use this test as the basis: it runs on the Investments page, creates a recurring plan and asserts the confirmation message. To meet the after_only verification requirements, extend the test to select Monthly frequency (instead of Weekly) and, after creation, navigate to the user's Recurring/Scheduled Plans list and assert a newly created active plan row exists with Monthly frequency, the chosen fund symbol, contribution amount, start date and funding account. Also assert the trade_status field/state for that plan is active.
   > Limitation: This candidate is on the correct module and already checks for the confirmation message and that the schedule is stored, but it uses Weekly frequency (requirement expects Monthly) and does not explicitly verify the presence and full details of the scheduled plan record or the plan's trade_status in the user's Recurring/Scheduled Plans list. Therefore it cannot fully confirm the after-only expected outcome without modification.

**3. [POST-VERIFY] 10.INVEST-003** -- Create recurring investment plan with Weekly frequency
   > This test operates in the Investments module and exercises recurring plan creation, but it only verifies creation via a success message and uses Weekly frequency. To serve as the after_only verification, modify or extend it to: (1) create the plan with Frequency=Monthly and the intended Start Date, (2) after creation navigate to Investments -> Recurring Plans (Scheduled Plans), (3) locate the plan by Fund and Start Date, and (4) assert the listed Frequency is 'Monthly' and the Next Run Date matches the configured schedule.
   > Limitation: The candidate is on the correct module and concerns recurring plans, but it does not access the Recurring Plans listing nor assert the plan's frequency or next run date. As written it cannot, by itself, confirm the expected outcome required by an after_only verification.

**Notes:** Execute 10.INVEST-004 → then verify with 10.INVEST-003, 10.INVEST-003

---

### 11.ACCSTA-001: Generate statement using month-and-year period

**Coverage:** PARTIAL Partial
**Modifies State:** statement_generation

**1. Verify a generated statement record exists for the selected account and month and that a success notification is shown**

- **Status:** PARTIAL partial
- **Type:** -
- **Strategy:** After Only
- **Matched Test:** 11.ACCSTA-002 (Generate statement using custom date range)
- **Confidence:** 75%
- **Execution Note:** Use this test as the basis: it already verifies the success notification and that the generated statement shows transactions for the requested period. To serve as the after_only verification, modify or extend the test to (1) choose the Month/Year statement period (instead of a custom date range) or record the selected month/year used, and (2) explicitly assert that the generated statement header displays the selected Account name and the chosen Month/Year along with the 'Statement generated successfully.' notification.
- **Reason:** This test runs in the correct module and already confirms the success message and returned statement data, but it targets a custom date range (not the Month/Year selection) and does not explicitly assert that the statement header lists the selected account and month/year. As written it cannot fully confirm the required header content.
- **Manual Step:** After generating the statement, visually confirm that 'Statement generated successfully.' is displayed and that the statement header contains the selected Account name and the chosen Month and Year. Alternatively, update the automated test to select a Month/Year period and add assertions that the header text matches the selected account and month/year.

**2. Verify the generated statement's transaction list contains only transactions from the selected month and that totals match the listed transactions**

- **Status:** PARTIAL partial
- **Type:** -
- **Strategy:** After Only
- **Matched Test:** 11.ACCSTA-002 (Generate statement using custom date range)
- **Confidence:** 72%
- **Execution Note:** Run this test to generate the statement for the chosen month/custom date range. After the statement is displayed, inspect the statement's transaction list and the displayed subtotal/total and compare them to the computed sum of the listed transactions to confirm correctness.
- **Reason:** This test operates in the correct module and displays the generated statement with the retrieved transactions for the selected date range, so it exposes the required transaction_list data. However, the test's existing expected outcome only asserts that transactions are shown and a success message is displayed; it does not validate that every transaction date falls within the selected month or that the displayed totals equal the sum of the listed transactions. Because the execution strategy is after_only, the verification test must confirm those outcomes by itself — which this candidate does not currently do.
- **Manual Step:** 1) Select the desired month (or enter the custom start and end dates) and the Account, then click 'Generate Statement'. 2) Verify the statement is generated and the transaction list is displayed. 3) For each transaction in the list, check the transaction date is >= first day and <= last day of the selected month. 4) Sum the transaction amounts shown in the list (apply same sign/credit-debit rules used by the system). 5) Compare the computed sum to the displayed subtotal/total on the statement; they must match. 6) If any date falls outside the month or totals differ, record a failure.

**Coverage Gaps:**
- This test runs in the correct module and already confirms the success message and returned statement data, but it targets a custom date range (not the Month/Year selection) and does not explicitly assert that the statement header lists the selected account and month/year. As written it cannot fully confirm the required header content.
- This test operates in the correct module and displays the generated statement with the retrieved transactions for the selected date range, so it exposes the required transaction_list data. However, the test's existing expected outcome only asserts that transactions are shown and a success message is displayed; it does not validate that every transaction date falls within the selected month or that the displayed totals equal the sum of the listed transactions. Because the execution strategy is after_only, the verification test must confirm those outcomes by itself — which this candidate does not currently do.

#### Execution Plan

**1. [ACTION] 11.ACCSTA-001** -- Generate statement using month-and-year period
   > Run 11.ACCSTA-001 — this is the state-changing action being verified

**2. [POST-VERIFY] 11.ACCSTA-002** -- Generate statement using custom date range
   > Use this test as the basis: it already verifies the success notification and that the generated statement shows transactions for the requested period. To serve as the after_only verification, modify or extend the test to (1) choose the Month/Year statement period (instead of a custom date range) or record the selected month/year used, and (2) explicitly assert that the generated statement header displays the selected Account name and the chosen Month/Year along with the 'Statement generated successfully.' notification.
   > Limitation: This test runs in the correct module and already confirms the success message and returned statement data, but it targets a custom date range (not the Month/Year selection) and does not explicitly assert that the statement header lists the selected account and month/year. As written it cannot fully confirm the required header content.

**3. [POST-VERIFY] 11.ACCSTA-002** -- Generate statement using custom date range
   > Run this test to generate the statement for the chosen month/custom date range. After the statement is displayed, inspect the statement's transaction list and the displayed subtotal/total and compare them to the computed sum of the listed transactions to confirm correctness.
   > Limitation: This test operates in the correct module and displays the generated statement with the retrieved transactions for the selected date range, so it exposes the required transaction_list data. However, the test's existing expected outcome only asserts that transactions are shown and a success message is displayed; it does not validate that every transaction date falls within the selected month or that the displayed totals equal the sum of the listed transactions. Because the execution strategy is after_only, the verification test must confirm those outcomes by itself — which this candidate does not currently do.

**Notes:** Execute 11.ACCSTA-001 → then verify with 11.ACCSTA-002, 11.ACCSTA-002

---

### 11.ACCSTA-002: Generate statement using custom date range

**Coverage:** PARTIAL Partial
**Modifies State:** statement_generation

**1. Verify a generated statement record exists for the specified custom date range and that a success notification is shown**

- **Status:** PARTIAL partial
- **Type:** -
- **Strategy:** After Only
- **Matched Test:** 11.ACCSTA-001 (Generate statement using month-and-year period)
- **Confidence:** 72%
- **Execution Note:** Use this test as the base: execute Generate Statement, confirm the 'Statement generated successfully.' notification and inspect the generated statement view. Augment the test to select a custom date range (start and end) instead of month-and-year and add explicit assertions that the statement header displays the selected account and the exact start and end dates (and/or that statement_data contains those fields).
- **Reason:** This test operates in the correct module and already checks for the success notification and generated statement content, but it uses a month-and-year period rather than a custom date range and does not explicitly assert that the statement header lists the selected account and the given start and end dates. Because the execution strategy is after_only, the verification must confirm the specific custom-date outcome and header contents — which this test does not fully cover.
- **Manual Step:** Select Statement Period as a custom date range (enter start date and end date). Select the Account. Click 'Generate Statement'. After generation, confirm the success notification 'Statement generated successfully.' is shown. On the Generate Statement result view, verify the statement header lists the selected account and shows the exact start and end dates entered. Optionally validate that the backend/statement_data record exists and contains the account and date-range fields matching the UI header.

**2. Verify the generated statement's transaction list contains only transactions within the specified date range and totals match the listed transactions**

- **Status:** PARTIAL partial
- **Type:** -
- **Strategy:** After Only
- **Matched Test:** 11.ACCSTA-001 (Generate statement using month-and-year period)
- **Confidence:** 70%
- **Execution Note:** This test runs on the Account Statements page and generates a statement for a specified month, which displays the retrieved transaction list. To serve as the after-only verification, extend the test to inspect the displayed statement details after generation: iterate the listed transactions and assert each transaction date is >= start date and <= end date; compute the sum of the listed transactions and assert it equals the displayed totals.
- **Reason:** The test operates in the correct module and displays the generated statement with transactions for the selected period, but it does not currently verify that every transaction date falls within the requested start/end dates nor that the displayed totals equal the computed sum. Therefore it cannot, as written, fully confirm the required outcome in an after-only run.
- **Manual Step:** After generating the statement, open the statement's transaction list and manually verify: (1) each transaction date is on or after the statement start date and on or before the end date; (2) add up the transaction amounts shown and confirm the total matches the statement's displayed totals.

**Coverage Gaps:**
- This test operates in the correct module and already checks for the success notification and generated statement content, but it uses a month-and-year period rather than a custom date range and does not explicitly assert that the statement header lists the selected account and the given start and end dates. Because the execution strategy is after_only, the verification must confirm the specific custom-date outcome and header contents — which this test does not fully cover.
- The test operates in the correct module and displays the generated statement with transactions for the selected period, but it does not currently verify that every transaction date falls within the requested start/end dates nor that the displayed totals equal the computed sum. Therefore it cannot, as written, fully confirm the required outcome in an after-only run.

#### Execution Plan

**1. [ACTION] 11.ACCSTA-002** -- Generate statement using custom date range
   > Run 11.ACCSTA-002 — this is the state-changing action being verified

**2. [POST-VERIFY] 11.ACCSTA-001** -- Generate statement using month-and-year period
   > Use this test as the base: execute Generate Statement, confirm the 'Statement generated successfully.' notification and inspect the generated statement view. Augment the test to select a custom date range (start and end) instead of month-and-year and add explicit assertions that the statement header displays the selected account and the exact start and end dates (and/or that statement_data contains those fields).
   > Limitation: This test operates in the correct module and already checks for the success notification and generated statement content, but it uses a month-and-year period rather than a custom date range and does not explicitly assert that the statement header lists the selected account and the given start and end dates. Because the execution strategy is after_only, the verification must confirm the specific custom-date outcome and header contents — which this test does not fully cover.

**3. [POST-VERIFY] 11.ACCSTA-001** -- Generate statement using month-and-year period
   > This test runs on the Account Statements page and generates a statement for a specified month, which displays the retrieved transaction list. To serve as the after-only verification, extend the test to inspect the displayed statement details after generation: iterate the listed transactions and assert each transaction date is >= start date and <= end date; compute the sum of the listed transactions and assert it equals the displayed totals.
   > Limitation: The test operates in the correct module and displays the generated statement with transactions for the selected period, but it does not currently verify that every transaction date falls within the requested start/end dates nor that the displayed totals equal the computed sum. Therefore it cannot, as written, fully confirm the required outcome in an after-only run.

**Notes:** Execute 11.ACCSTA-002 → then verify with 11.ACCSTA-001, 11.ACCSTA-001

---

### 11.ACCSTA-003: Save e-Statement preference with a valid email

**Coverage:** PARTIAL Partial
**Modifies State:** e_statement_preference

**1. Verify the e-Statement preference is saved and the UI persists the paperless checkbox and email after saving**

- **Status:** PARTIAL partial
- **Type:** -
- **Strategy:** After Only
- **Matched Test:** 11.ACCSTA-008 (Save preference with invalid email format)
- **Confidence:** 70%
- **Execution Note:** This test targets the correct module and the Save Preference action and interacts with the paperless checkbox and Email Address field, but it currently verifies the invalid-email negative path. To serve as the required after_only verification, modify the test to enter a valid email address, click 'Save Preference', assert the success message 'e-Statement preference updated.' is displayed, then reload/revisit the e-Statement preference panel and verify the paperless checkbox remains selected and the Email Address field shows the entered valid email.
- **Reason:** Though on the correct page and manipulating the relevant fields, the candidate test is written to validate an invalid-email failure case (expecting validation errors and that the preference is not saved). It does not confirm the successful save or persistence required by the after_only verification.
- **Manual Step:** After performing the save action with a valid email: 1) Confirm the UI shows 'e-Statement preference updated.' 2) Navigate away and return (or reload) the e-Statement preference panel. 3) Verify the paperless checkbox is still selected and the Email Address field displays the saved email.

**2. Verify the saved e-statement email is reflected in the user's contact/profile information**

- **Status:** PARTIAL partial
- **Type:** -
- **Strategy:** After Only
- **Matched Test:** 8.UCI-001 (Update profile with all valid contact fields)
- **Confidence:** 60%
- **Execution Note:** This test operates on the correct module and verifies that contact fields are refreshed after an update, but as written it does not include the email/e-statement email field. To use this test for the required after_only verification, add steps to (1) enter or confirm the e-statement email prior to saving (if needed), (2) save the e-statement preference or update profile, and (3) assert that the Contact Email (or profile email) field displays exactly the e-statement email value after save.
- **Reason:** The candidate runs on the Update Contact Info module and validates profile updates, but none of the provided test cases explicitly access or verify the email/contact email field. Because the verification must confirm the saved e-statement email after the action (after_only), the test must explicitly read and assert the email value; the current test does not.
- **Manual Step:** After saving the e-statement preference, open Update Contact Info, locate the Contact Email (or Email) field in the user's profile, and verify that the displayed email exactly matches the e-statement email that was entered and saved. If automating, add an assertion that profile.email == expected_estatement_email.

**Coverage Gaps:**
- Though on the correct page and manipulating the relevant fields, the candidate test is written to validate an invalid-email failure case (expecting validation errors and that the preference is not saved). It does not confirm the successful save or persistence required by the after_only verification.
- The candidate runs on the Update Contact Info module and validates profile updates, but none of the provided test cases explicitly access or verify the email/contact email field. Because the verification must confirm the saved e-statement email after the action (after_only), the test must explicitly read and assert the email value; the current test does not.

#### Execution Plan

**1. [ACTION] 11.ACCSTA-003** -- Save e-Statement preference with a valid email
   > Run 11.ACCSTA-003 — this is the state-changing action being verified

**2. [POST-VERIFY] 11.ACCSTA-008** -- Save preference with invalid email format
   > This test targets the correct module and the Save Preference action and interacts with the paperless checkbox and Email Address field, but it currently verifies the invalid-email negative path. To serve as the required after_only verification, modify the test to enter a valid email address, click 'Save Preference', assert the success message 'e-Statement preference updated.' is displayed, then reload/revisit the e-Statement preference panel and verify the paperless checkbox remains selected and the Email Address field shows the entered valid email.
   > Limitation: Though on the correct page and manipulating the relevant fields, the candidate test is written to validate an invalid-email failure case (expecting validation errors and that the preference is not saved). It does not confirm the successful save or persistence required by the after_only verification.

**3. [NAVIGATE]** Navigate to Update Contact Info
   > Navigate from Account Statements to Update Contact Info

**4. [POST-VERIFY] 8.UCI-001** -- Update profile with all valid contact fields
   > This test operates on the correct module and verifies that contact fields are refreshed after an update, but as written it does not include the email/e-statement email field. To use this test for the required after_only verification, add steps to (1) enter or confirm the e-statement email prior to saving (if needed), (2) save the e-statement preference or update profile, and (3) assert that the Contact Email (or profile email) field displays exactly the e-statement email value after save.
   > Limitation: The candidate runs on the Update Contact Info module and validates profile updates, but none of the provided test cases explicitly access or verify the email/contact email field. Because the verification must confirm the saved e-statement email after the action (after_only), the test must explicitly read and assert the email value; the current test does not.

**Notes:** Execute 11.ACCSTA-003 → then verify with 11.ACCSTA-008, 8.UCI-001

---

### 12.SECSET-001: Change password with valid current and strong matching new password

**Coverage:** FULL Full
**Modifies State:** credentials_update, password_change

**1. Verify the Security Settings UI shows a successful password change confirmation**

- **Status:** FOUND found
- **Type:** -
- **Strategy:** After Only
- **Matched Test:** 12.SECSET-006 (Change password using a minimally-compliant strong password)
- **Confidence:** 72%
- **Execution Note:** Execute this test after submitting Change Password. It performs a valid password change and its expected result asserts a successful password change; verify the change-password panel shows a clear success message (e.g., 'Password changed successfully.') and that no password validation/mismatch error messages are present.

**2. Verify authentication changed by confirming the old password no longer works and the new password can be used to sign in**

- **Status:** FOUND found
- **Type:** -
- **Strategy:** Before/After
- **Matched Test:** 1.LOGIN-008 (After changing password the old password no longer works)
- **Confidence:** 95%
- **Before Action:** Attempt to sign out (if signed in) and perform a login with the current (old) password to confirm it authenticates; attempt a login with the proposed new password and confirm it does NOT authenticate
- **After Action:** Sign out and attempt login with the old password (expect failure); then attempt login with the new password (expect success) and confirm session is established
- **Execution Note:** Use this test to perform the required before/after observations. For the BEFORE run: ensure the user is signed out, then perform only the login attempts (attempt login with the current/old password — expect success; attempt login with the candidate new password — expect failure) and record authentication_result and session_status. Do NOT perform the password-change steps during the BEFORE run. After the password-change action is executed by the plan, run the test AGAIN (AFTER run): sign out and perform the two login attempts (old password — expect failure; new password — expect success) and record authentication_result and session_status. Compare before/after recordings to verify the switch.

#### Execution Plan

> **Strategy:** Run verification tests BEFORE and AFTER the action to compare values.

**1. [NAVIGATE]** Navigate to Login
   > Navigate from Security Settings to Login to record baseline data

**2. [PRE-VERIFY] 1.LOGIN-008** -- After changing password the old password no longer works
   > Run 1.LOGIN-008 and RECORD the current values before the action

**3. [NAVIGATE]** Navigate to Security Settings
   > Return to Security Settings to execute the action

**4. [ACTION] 12.SECSET-001** -- Change password with valid current and strong matching new password
   > Run 12.SECSET-001 — this is the state-changing action being verified

**5. [POST-VERIFY] 12.SECSET-006** -- Change password using a minimally-compliant strong password
   > Execute this test after submitting Change Password. It performs a valid password change and its expected result asserts a successful password change; verify the change-password panel shows a clear success message (e.g., 'Password changed successfully.') and that no password validation/mismatch error messages are present.

**6. [NAVIGATE]** Navigate to Login
   > Navigate from Security Settings to Login to verify the change

**7. [POST-VERIFY] 1.LOGIN-008** -- After changing password the old password no longer works
   > Run 1.LOGIN-008 AGAIN and COMPARE with baseline values recorded in pre-verify

**Notes:** PRE: Record baseline with 1.LOGIN-008 → ACTION: Execute 12.SECSET-001 → POST: Verify with 12.SECSET-006, 1.LOGIN-008 (compare against baseline)

---

### 13.SUPCEN-001: Send message successfully with required fields (no attachment)

**Coverage:** PARTIAL Partial
**Modifies State:** support_ticket_creation

**1. Verify a support ticket is created and a success notification plus ticket ID are shown**

- **Status:** FOUND found
- **Type:** -
- **Strategy:** After Only
- **Matched Test:** 13.SUPCEN-002 (Send message successfully with a valid attachment)
- **Confidence:** 90%
- **Execution Note:** This test runs on the Support Center and explicitly expects the success notification 'Message sent successfully.' and a ticket ID to be shown in the confirmation view. For an after_only verification, run the observation portion of this test after the message has been sent (or run the full test which sends the message and then verifies). Capture the displayed ticket ID from the confirmation view and assert the success message text.

**2. Verify the created ticket appears in the user's support ticket listing with correct subject/category and initial status**

- **Status:** PARTIAL partial
- **Type:** -
- **Strategy:** After Only
- **Matched Test:** 13.SUPCEN-002 (Send message successfully with a valid attachment)
- **Confidence:** 62%
- **Execution Note:** This test runs in the correct module and creates a ticket (it verifies a success notification and that a ticket ID is shown). To serve as the required after_only verification it must be extended: after the ticket is created, navigate to the user's My Requests / Ticket listing, locate the ticket by the shown ticket ID or subject, and assert the ticket's subject, category and status (e.g., 'Open' or 'New').
- **Reason:** While 13.SUPCEN-002 creates the ticket and surfaces a ticket ID, it does NOT open the My Requests/ticket listing or inspect the ticket's subject, category and status. Because the execution_strategy is after_only, the verification test itself must confirm the ticket appears in the listing with correct fields; the candidate stops short of that.
- **Manual Step:** After the test shows the 'Message sent successfully.' notification and ticket ID, go to Support Center → My Requests (Ticket listing). Search or filter for the returned ticket ID or subject. Open the ticket row and verify: 1) Subject matches the submitted subject; 2) Category matches the selected category; 3) Status is the expected initial status (e.g., 'Open' or 'New'). Record pass/fail.

**Coverage Gaps:**
- While 13.SUPCEN-002 creates the ticket and surfaces a ticket ID, it does NOT open the My Requests/ticket listing or inspect the ticket's subject, category and status. Because the execution_strategy is after_only, the verification test itself must confirm the ticket appears in the listing with correct fields; the candidate stops short of that.

#### Execution Plan

**1. [ACTION] 13.SUPCEN-001** -- Send message successfully with required fields (no attachment)
   > Run 13.SUPCEN-001 — this is the state-changing action being verified

**2. [POST-VERIFY] 13.SUPCEN-002** -- Send message successfully with a valid attachment
   > This test runs on the Support Center and explicitly expects the success notification 'Message sent successfully.' and a ticket ID to be shown in the confirmation view. For an after_only verification, run the observation portion of this test after the message has been sent (or run the full test which sends the message and then verifies). Capture the displayed ticket ID from the confirmation view and assert the success message text.

**3. [POST-VERIFY] 13.SUPCEN-002** -- Send message successfully with a valid attachment
   > This test runs in the correct module and creates a ticket (it verifies a success notification and that a ticket ID is shown). To serve as the required after_only verification it must be extended: after the ticket is created, navigate to the user's My Requests / Ticket listing, locate the ticket by the shown ticket ID or subject, and assert the ticket's subject, category and status (e.g., 'Open' or 'New').
   > Limitation: While 13.SUPCEN-002 creates the ticket and surfaces a ticket ID, it does NOT open the My Requests/ticket listing or inspect the ticket's subject, category and status. Because the execution_strategy is after_only, the verification test itself must confirm the ticket appears in the listing with correct fields; the candidate stops short of that.

**Notes:** Execute 13.SUPCEN-001 → then verify with 13.SUPCEN-002, 13.SUPCEN-002

---

### 13.SUPCEN-002: Send message successfully with a valid attachment

**Coverage:** PARTIAL Partial
**Modifies State:** support_ticket_creation

**1. Verify a support ticket is created with attachment and a success notification plus ticket ID are shown**

- **Status:** PARTIAL partial
- **Type:** -
- **Strategy:** After Only
- **Matched Test:** 13.SUPCEN-001 (Send message successfully with required fields (no attachment))
- **Confidence:** 70%
- **Execution Note:** This test runs in the Support Center and verifies the success notification and that a ticket ID is shown (which satisfies the after_only requirement for confirming notification and ID). However, the test does not attach a file nor verify that the created ticket contains an attachment. To use as the verification, update the test steps to attach a supported file before clicking 'Send Message' and assert the same success notification and ticket ID are shown; or after the test captures the ticket ID, query/open the ticket details to assert the attachment is present.
- **Reason:** The candidate validates the success message and ticket ID but explicitly covers a message sent without an attachment. The requirement requires confirming creation with an attachment and verifying the attachment presence, which this test does not do.
- **Manual Step:** After the test shows the success notification and ticket ID, manually (or via an automated follow-up) open the created ticket using the shown ticket ID and verify the attachment is present in the ticket details. Alternatively, modify the test to attach a supported file before sending and assert the attachment is shown in the ticket confirmation/details.

**2. Verify the ticket detail shows the uploaded attachment with filename and a downloadable link**

- **Status:** PARTIAL partial
- **Type:** -
- **Strategy:** After Only
- **Matched Test:** 13.SUPCEN-001 (Send message successfully with required fields (no attachment))
- **Confidence:** 40%
- **Execution Note:** This test runs in the Support Center and creates a ticket (shows ticket ID). To use it for the required verification, augment or extend it so that the message includes an attachment and after send it opens the created ticket's detail page and inspects the attachments section for filename and download/view link.
- **Reason:** The test operates in the correct module and creates a ticket, but it explicitly has no attachment and does not open the ticket detail or check the attachments section. Because execution_strategy is after_only, the verification test must itself confirm the uploaded file is listed with a downloadable/view link — this test as written cannot do that.
- **Manual Step:** Open the created ticket's detail page, locate the attachments section, verify the uploaded file is listed with the correct filename, and click the download/view link to confirm the file is accessible. If automating, modify the test to attach a valid file when sending the message and add steps to open the ticket detail and assert the attachment name and presence of a download/view control.

**Coverage Gaps:**
- The candidate validates the success message and ticket ID but explicitly covers a message sent without an attachment. The requirement requires confirming creation with an attachment and verifying the attachment presence, which this test does not do.
- The test operates in the correct module and creates a ticket, but it explicitly has no attachment and does not open the ticket detail or check the attachments section. Because execution_strategy is after_only, the verification test must itself confirm the uploaded file is listed with a downloadable/view link — this test as written cannot do that.

#### Execution Plan

**1. [ACTION] 13.SUPCEN-002** -- Send message successfully with a valid attachment
   > Run 13.SUPCEN-002 — this is the state-changing action being verified

**2. [POST-VERIFY] 13.SUPCEN-001** -- Send message successfully with required fields (no attachment)
   > This test runs in the Support Center and verifies the success notification and that a ticket ID is shown (which satisfies the after_only requirement for confirming notification and ID). However, the test does not attach a file nor verify that the created ticket contains an attachment. To use as the verification, update the test steps to attach a supported file before clicking 'Send Message' and assert the same success notification and ticket ID are shown; or after the test captures the ticket ID, query/open the ticket details to assert the attachment is present.
   > Limitation: The candidate validates the success message and ticket ID but explicitly covers a message sent without an attachment. The requirement requires confirming creation with an attachment and verifying the attachment presence, which this test does not do.

**3. [POST-VERIFY] 13.SUPCEN-001** -- Send message successfully with required fields (no attachment)
   > This test runs in the Support Center and creates a ticket (shows ticket ID). To use it for the required verification, augment or extend it so that the message includes an attachment and after send it opens the created ticket's detail page and inspects the attachments section for filename and download/view link.
   > Limitation: The test operates in the correct module and creates a ticket, but it explicitly has no attachment and does not open the ticket detail or check the attachments section. Because execution_strategy is after_only, the verification test must itself confirm the uploaded file is listed with a downloadable/view link — this test as written cannot do that.

**Notes:** Execute 13.SUPCEN-002 → then verify with 13.SUPCEN-001, 13.SUPCEN-001

---

### 13.SUPCEN-003: Submit Request Callback with valid inputs

**Coverage:** PARTIAL Partial
**Modifies State:** callback_request_creation

**1. Verify the callback request is created and a success message is displayed with request details**

- **Status:** PARTIAL partial
- **Type:** -
- **Strategy:** After Only
- **Matched Test:** 13.SUPCEN-010 (Submit with Preferred Date set to the next business day (boundary))
- **Confidence:** 70%
- **Execution Note:** Use this test as the basis: it runs on the Support Center, submits a valid callback request and verifies the success message 'Callback request submitted.' Extend the test to, after submission, locate the created callback request (via the UI list/detail view, API, or DB) and assert the stored fields match the submitted Reason, Preferred Date, Preferred Time Window and Phone Number.
- **Reason:** This test operates on the correct module and confirms the success message, but it does not explicitly capture or verify the created callback request record or its details (reason, scheduled date/time window, phone number). Because execution_strategy is after_only, the test must itself confirm the record and field values; the candidate only partially meets that need.
- **Manual Step:** After clicking 'Request Callback' and observing the success message, navigate to the Support Center callback requests list or use the callback-requests API/DB query to find the newly created request (filter by the submitted phone number or timestamp). Verify the record exists and that its Reason, Scheduled Date, Time Window and Phone Number match the submitted values. Capture these details in the test evidence.

**2. Verify the system recorded/sent a confirmation for the callback request (confirmation flag or outbound confirmation recorded)**

- **Status:** PARTIAL partial
- **Type:** -
- **Strategy:** After Only
- **Matched Test:** 13.SUPCEN-010 (Submit with Preferred Date set to the next business day (boundary))
- **Confidence:** 65%
- **Execution Note:** This test submits a callback request in the Support Center and expects an email confirmation. To make it a full after_only verification, extend it after the submission step to: open the created callback request detail record (from the callbacks list or recent requests), and assert the presence of an outbound confirmation indicator, confirmation reference number, or an 'email confirmation sent' flag in the request record.
- **Reason:** The test operates in the correct module and exercises creating a callback request (and expects an email), but it does not include steps to open the callback request detail or verify a confirmation flag/reference in the request record — which is required for after_only verification.
- **Manual Step:** After running the callback submission test, manually open the newly created callback request detail in Support Center and verify one of: a confirmation flag is set, a confirmation/reference entry exists, or the record indicates an outbound confirmation email was queued/sent. If UI evidence is absent, check outbound email logs/queue for the confirmation message tied to the request.

**Coverage Gaps:**
- This test operates on the correct module and confirms the success message, but it does not explicitly capture or verify the created callback request record or its details (reason, scheduled date/time window, phone number). Because execution_strategy is after_only, the test must itself confirm the record and field values; the candidate only partially meets that need.
- The test operates in the correct module and exercises creating a callback request (and expects an email), but it does not include steps to open the callback request detail or verify a confirmation flag/reference in the request record — which is required for after_only verification.

#### Execution Plan

**1. [ACTION] 13.SUPCEN-003** -- Submit Request Callback with valid inputs
   > Run 13.SUPCEN-003 — this is the state-changing action being verified

**2. [POST-VERIFY] 13.SUPCEN-010** -- Submit with Preferred Date set to the next business day (boundary)
   > Use this test as the basis: it runs on the Support Center, submits a valid callback request and verifies the success message 'Callback request submitted.' Extend the test to, after submission, locate the created callback request (via the UI list/detail view, API, or DB) and assert the stored fields match the submitted Reason, Preferred Date, Preferred Time Window and Phone Number.
   > Limitation: This test operates on the correct module and confirms the success message, but it does not explicitly capture or verify the created callback request record or its details (reason, scheduled date/time window, phone number). Because execution_strategy is after_only, the test must itself confirm the record and field values; the candidate only partially meets that need.

**3. [POST-VERIFY] 13.SUPCEN-010** -- Submit with Preferred Date set to the next business day (boundary)
   > This test submits a callback request in the Support Center and expects an email confirmation. To make it a full after_only verification, extend it after the submission step to: open the created callback request detail record (from the callbacks list or recent requests), and assert the presence of an outbound confirmation indicator, confirmation reference number, or an 'email confirmation sent' flag in the request record.
   > Limitation: The test operates in the correct module and exercises creating a callback request (and expects an email), but it does not include steps to open the callback request detail or verify a confirmation flag/reference in the request record — which is required for after_only verification.

**Notes:** Execute 13.SUPCEN-003 → then verify with 13.SUPCEN-010, 13.SUPCEN-010

---

## Navigation Graph

![Navigation Graph](Output/Parabank/post-verified-gpt5mini/navigation_graph.png)

### Pages

| Module | URL | Auth Required | Test Cases |
|--------|-----|---------------|------------|
| Login | /login | No | 15 |
| Register | /register | No | 11 |
| Accounts Overview | /accounts | Yes | 7 |
| Open New Account | /open-account | Yes | 13 |
| Transfer Funds | /transfer-funds | Yes | 8 |
| Payments | /bill-pay | Yes | 4 |
| Request Loan | /request-loan | Yes | 14 |
| Update Contact Info | /update-contact-info | Yes | 5 |
| Manage Cards | /manage-cards | Yes | 15 |
| Investments | /investments | Yes | 16 |
| Account Statements | /account-statements | Yes | 8 |
| Security Settings | /security-settings | Yes | 6 |
| Support Center | /support-center | Yes | 10 |
