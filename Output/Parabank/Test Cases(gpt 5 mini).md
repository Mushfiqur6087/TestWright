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

## Navigation Graph

![Navigation Graph](Output/Parabank/navigation_graph.png)

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
