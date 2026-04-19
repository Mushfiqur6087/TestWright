# Parabank

**Base URL:** 
**Generated:** 2026-04-20T02:04:48.618542

## Summary

| Metric | Count |
|--------|-------|
| **Total Tests** | 146 |

### By Type

| Type | Count |
|------|-------|
| Positive | 43 |
| Negative | 83 |
| Edge Case | 12 |
| Standard | 8 |

### By Priority

| Priority | Count |
|----------|-------|
| High | 46 |
| Medium | 91 |
| Low | 9 |

---

## Test Cases

### Login

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 1.LOGIN-001 | Sign in with registered email | User exists with registered email and password. | 1. Fill all required fields (Email/Username with registered email, Password with valid password)<br>2. Click "Sign In" | The system flashes "Signed in successfully." and redirects the user to the Accounts Overview page. | High |
| 1.LOGIN-002 | Sign in with registered username | User exists with registered username and password. | 1. Fill all required fields (Email/Username with registered username, Password with valid password)<br>2. Click "Sign In" | The system flashes "Signed in successfully." and redirects the user to the Accounts Overview page. | High |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 1.LOGIN-003 | Sign in with incorrect credentials clears password and shows error | An active registered user exists. | 1. Fill all required fields (Email/Username with registered email, Password with incorrect password)<br>2. Click "Sign In" | The system shows the authentication error message, clears the password field, and allows another attempt. | High |
| 1.LOGIN-009 | Submit with all required fields empty | None | 1. Leave all required fields empty<br>2. Click "Sign In" | Validation errors shown for all required fields. | Medium |
| 1.LOGIN-010 | Sign in with invalid email format | None | 1. Fill all required fields (Email/Username with an invalid email format, Password with valid password)<br>2. Click "Sign In" | Validation error indicating the email format is invalid and sign-in is not attempted. | Medium |
| 1.LOGIN-011 | Sign in with password shorter than minimum length | User exists with registered email. | 1. Fill all required fields (Email/Username with registered email, Password shorter than the required length)<br>2. Click "Sign In" | Validation error indicating the password does not meet the required length/complexity and sign-in is not performed. | Medium |

#### Edge Case Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 1.LOGIN-004 | Sign in with password exactly at minimum required length and complexity | User exists with a password that exactly satisfies the minimum complexity and length requirements. | 1. Fill all required fields (Email/Username with registered email, Password that exactly meets the minimum length and complexity)<br>2. Click "Sign In" | Authentication succeeds: the system flashes "Signed in successfully." and redirects the user to the Accounts Overview page. | High |

#### Standard Quality Patterns

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 1.LOGIN-005 | Post-logout redirect to login when revisiting an authenticated page | A valid user account exists and tester can log in; tester knows the URL of a protected page (e.g., Accounts Overview). | 1. Log in with a valid user account.<br>2. Navigate to a protected page (e.g., Accounts Overview) and note the URL.<br>3. Click the application's Logout control.<br>4. In the browser address bar, paste the previously noted protected-page URL and press Enter. | The app redirects to the login page (or shows the login form) instead of displaying the protected content. | High |
| 1.LOGIN-006 | Browser back button after logout does not restore authenticated content | A valid user account exists and tester can log in; tester is using a standard desktop or mobile browser. | 1. Log in with a valid user account and navigate to a protected page (e.g., Transfer Funds).<br>2. Click the application's Logout control to end the session.<br>3. Use the browser Back button to attempt to return to the protected page. | The protected page is not restored; the browser either shows the login page or an unauthenticated notice and no cached sensitive data is visible. | High |
| 1.LOGIN-007 | Session expiry during form entry forces re-authentication or shows expiry notice | A valid user account exists and tester can log in; tester can start filling a multi-step form on a protected page (e.g., Transfer Funds). | 1. Log in with a valid user account and navigate to a form on a protected page (e.g., Transfer Funds).<br>2. Begin filling the form, then simulate session expiry by either waiting the configured timeout or using developer tools to delete/expire the session cookie/token.<br>3. Attempt to submit the form after the session has been expired. | The application prevents the submission and either displays a session-expired message prompting re-login or redirects the user to the login page before accepting the submission. | High |
| 1.LOGIN-008 | After changing password, the old password no longer authenticates | A valid user account exists and tester knows current credentials; password-change feature accessible from an authenticated session. | 1. Log in with the current credentials and navigate to the Change Password page.<br>2. Change the password to a new value and confirm success, then log out.<br>3. Attempt to log in using the old password, then attempt to log in using the new password. | Login with the old password is rejected and shows an authentication error; login with the new password succeeds. | High |
| 1.LOGIN-012 | Page refresh on an authenticated page preserves login state | A valid user account exists and tester can log in. | 1. Log in with a valid user account and navigate to a protected page (e.g., Account Statements).<br>2. Click the browser's Reload/Refresh button or press F5.<br>3. Verify the page reload completes. | The user remains authenticated after the refresh and the protected content is visible without being redirected to login. | Medium |
| 1.LOGIN-013 | Password reset link shows error when used after its expiration | Password reset functionality is enabled; tester can request and obtain reset links (via email/logs/test inbox). | 1. On the login page, initiate a password reset for a valid account and obtain the reset link from the test inbox or email logs.<br>2. Wait until the stated expiration period has passed (or manipulate the token to simulate an expired timestamp), then open the reset link in the browser. | The application rejects the expired reset link and displays a clear error message indicating the link has expired and prompting to request a new reset. | Medium |
| 1.LOGIN-014 | Forgot-password shows clear error for an unregistered email | Password reset page is accessible from the login screen. | 1. From the login page, click 'Forgot Password' (or equivalent) to open the password reset form.<br>2. Enter an email address that is not registered in the system and submit the reset request. | The application returns a clear, user-visible error indicating the email is not associated with an account (not a silent success), or presents a message explaining the address is unrecognized and guidance to proceed. | Medium |

---

### Register

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 2.REGIST-001 | Register with all valid required fields | None | 1. Fill all required fields with valid values (First Name, Last Name, Street Address, City, State, ZIP Code in allowed format, Phone Number, Social Security Number, Username as a valid email, Password meeting length requirement, Confirm Password matching Password)<br>2. Click "Register" | Account created successfully message shown and user is redirected to the login page. | High |
| 2.REGIST-002 | Phone number auto-formats on entry | None | 1. Fill all other required fields with valid values<br>2. Enter phone number as digits only into Phone Number field and move focus out of the field | Phone Number is automatically formatted to (123) 456-7890 on the form. | Medium |
| 2.REGIST-003 | SSN auto-formats on entry | None | 1. Fill all other required fields with valid values<br>2. Enter SSN as digits only into Social Security Number field and move focus out of the field | SSN is automatically formatted to 123-45-6789 on the form. | Medium |
| 2.REGIST-004 | Register using 5+4 ZIP code format | None | 1. Fill all required fields with valid values using a ZIP Code in 5+4 format<br>2. Click "Register" | Account created successfully message shown and user is redirected to the login page. | Medium |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 2.REGIST-005 | Submit with all required fields empty | None | 1. Leave all required fields empty<br>2. Click "Register" | Validation errors shown for all required fields. | Medium |
| 2.REGIST-006 | Submit with First Name empty | None | 1. Fill all other required fields with valid values, leave First Name empty<br>2. Click "Register" | Validation error indicating First Name is required. | Medium |
| 2.REGIST-007 | Submit with Last Name empty | None | 1. Fill all other required fields with valid values, leave Last Name empty<br>2. Click "Register" | Validation error indicating Last Name is required. | Medium |
| 2.REGIST-008 | Submit with Street Address empty | None | 1. Fill all other required fields with valid values, leave Street Address empty<br>2. Click "Register" | Validation error indicating Street Address is required. | Medium |
| 2.REGIST-009 | Submit with City empty | None | 1. Fill all other required fields with valid values, leave City empty<br>2. Click "Register" | Validation error indicating City is required. | Medium |
| 2.REGIST-010 | Submit with State empty | None | 1. Fill all other required fields with valid values, leave State unselected<br>2. Click "Register" | Validation error indicating State is required. | Medium |
| 2.REGIST-011 | Submit with ZIP Code empty | None | 1. Fill all other required fields with valid values, leave ZIP Code empty<br>2. Click "Register" | Validation error indicating ZIP Code is required. | Medium |
| 2.REGIST-012 | Submit with Phone Number empty | None | 1. Fill all other required fields with valid values, leave Phone Number empty<br>2. Click "Register" | Validation error indicating Phone Number is required. | Medium |
| 2.REGIST-013 | Submit with Social Security Number empty | None | 1. Fill all other required fields with valid values, leave Social Security Number empty<br>2. Click "Register" | Validation error indicating Social Security Number is required. | Medium |
| 2.REGIST-014 | Submit with Username empty | None | 1. Fill all other required fields with valid values, leave Username empty<br>2. Click "Register" | Validation error indicating Username is required. | Medium |
| 2.REGIST-015 | Submit with Password empty | None | 1. Fill all other required fields with valid values, leave Password empty<br>2. Click "Register" | Validation error indicating Password is required. | Medium |
| 2.REGIST-016 | Submit with Confirm Password empty | None | 1. Fill all other required fields with valid values, leave Confirm Password empty<br>2. Click "Register" | Validation error indicating Confirm Password is required. | Medium |
| 2.REGIST-017 | Register with invalid email format for Username | None | 1. Fill all required fields with valid values except enter an invalid email format into Username<br>2. Click "Register" | Validation error indicating Username must be a valid email format. | Medium |
| 2.REGIST-018 | Register with invalid phone number format | None | 1. Fill all required fields with valid values except enter a phone value that does not conform to the expected digits/format<br>2. Click "Register" | Validation error indicating Phone Number must follow the required format. | Medium |
| 2.REGIST-019 | Register with invalid ZIP Code format | None | 1. Fill all required fields with valid values except enter a ZIP Code that is not 5 digits or 5+4 format<br>2. Click "Register" | Validation error indicating ZIP Code must use the accepted format. | Medium |
| 2.REGIST-020 | Register with invalid SSN format | None | 1. Fill all required fields with valid values except enter an SSN that does not conform to required digits/format<br>2. Click "Register" | Validation error indicating SSN must follow the required format. | Medium |
| 2.REGIST-021 | Register with password shorter than minimum length | None | 1. Fill all required fields with valid values except enter a Password shorter than the minimum length and set Confirm Password to the same short value<br>2. Click "Register" | Validation error indicating Password must meet the minimum length requirement. | Medium |
| 2.REGIST-022 | Register with mismatched Password and Confirm Password | None | 1. Fill all required fields with valid values but enter a different value in Confirm Password than in Password<br>2. Click "Register" | Validation error indicating Confirm Password must match Password. | Medium |

#### Edge Case Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 2.REGIST-023 | Register with Password at minimum length boundary | None | 1. Fill all required fields with valid values using a Password that is exactly the minimum allowed length and set Confirm Password to match<br>2. Click "Register" | Account created successfully and user is redirected to the login page. | Low |

---

### Accounts Overview

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 3.ACCOVE-001 | Accounts overview displays welcome message and account listing | User is logged in and Accounts Overview (dashboard) is open. | 1. Verify the welcome message displays the user's name<br>2. Verify the accounts table is present and each row shows Account Number, Account Type, Current Balance, Account Status (Active badge), and Open Date | Welcome message shows the user's name and the accounts table displays the listed columns for each account. | High |
| 3.ACCOVE-002 | Footer displays total balance equal to sum of account balances | User is logged in and Accounts Overview (dashboard) is open. | 1. Read the Current Balance value from each account row and compute their sum<br>2. Compare the computed sum to the total balance displayed in the table footer row | Footer row displays a total balance equal to the sum of all Current Balance values shown in the rows. | High |
| 3.ACCOVE-003 | Rows are ordered by account creation date (earliest first) | User is logged in and Accounts Overview (dashboard) is open. | 1. Collect the Open Date value from each account row in displayed order<br>2. Verify the sequence of Open Date values is ordered earliest first | Account rows are displayed in ascending order by Open Date (earliest account first). | High |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 3.ACCOVE-006 | Clicking an Account Number has no implemented detail navigation | User is logged in and Accounts Overview (dashboard) is open. | 1. Click the Account Number link in a visible account row<br>2. Observe the page behavior after the click | Clicking the Account Number does not navigate to an account detail page (no detail view is opened) or a not-implemented indication is shown. | Medium |

#### Edge Case Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 3.ACCOVE-004 | Account numbers are displayed masked showing only last four digits | User is logged in and Accounts Overview (dashboard) is open. | 1. Inspect the Account Number field in multiple account rows<br>2. Verify each displayed account number shows only the last four digits and preceding characters are masked | Each account number on the dashboard is masked, revealing only the last four digits. | High |

#### Standard Quality Patterns

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 3.ACCOVE-005 | Direct URL access while logged out redirects to login (Accounts Overview) | Tester is logged out (fresh browser session) and knows the Accounts Overview entry URL. | 1. Ensure you are logged out (clear cookies or open a private window).<br>2. Enter the Accounts Overview page URL directly in the browser address bar and press Enter. | The app redirects to the login page (or displays the login form) instead of showing the Accounts Overview content. | High |

---

### Open New Account

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 4.ONA-001 | Open a new Checking account with a valid initial deposit | A funding source account has sufficient balance. | 1. Select the Checking account type card<br>2. Fill all required fields (Initial Deposit Amount with an amount equal to or above the Checking minimum, Funding Source Account selecting an account with sufficient balance)<br>3. Click "Open Account" | Success shows "Account opened successfully!" and Success redirects to accounts overview; the new Checking account appears in the accounts listing. | High |
| 4.ONA-002 | Open a new Savings account with a valid initial deposit | A funding source account has sufficient balance. | 1. Select the Savings account type card<br>2. Fill all required fields (Initial Deposit Amount with an amount equal to or above the Savings minimum, Funding Source Account selecting an account with sufficient balance)<br>3. Click "Open Account" | Success shows "Account opened successfully!" and Success redirects to accounts overview; the new Savings account appears in the accounts listing. | High |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 4.ONA-003 | Submit with all required fields empty | None | 1. Leave all required fields empty<br>2. Click "Open Account" | Validation errors shown for all required fields. | Medium |
| 4.ONA-004 | Submit with Account Type not selected | None | 1. Fill all other required fields with valid values, leave Account Type unselected<br>2. Click "Open Account" | Validation error indicating the account type is required and the account is not opened. | Medium |
| 4.ONA-005 | Enter non-numeric Initial Deposit Amount | A funding source account has sufficient balance. | 1. Fill all other required fields with valid values<br>2. Enter a non-numeric value into the Initial Deposit Amount field<br>3. Attempt to click "Open Account" | Real-time validation error indicating the deposit must be numeric is shown and submission is blocked. | Medium |
| 4.ONA-006 | Reject initial deposit below the Checking minimum | A funding source account has sufficient balance. | 1. Select the Checking account type card<br>2. Fill all other required fields with valid values and enter an amount below the Checking minimum in Initial Deposit Amount<br>3. Click "Open Account" | Validation error indicating the initial deposit does not meet the required minimum is shown and the account is not opened. | Medium |
| 4.ONA-007 | Reject initial deposit below the Savings minimum | A funding source account has sufficient balance. | 1. Select the Savings account type card<br>2. Fill all other required fields with valid values and enter an amount below the Savings minimum in Initial Deposit Amount<br>3. Click "Open Account" | Validation error indicating the initial deposit does not meet the required minimum is shown and the account is not opened. | Medium |
| 4.ONA-008 | Reject open request when funding source has insufficient balance | A funding source account has insufficient balance. | 1. Select an account type card<br>2. Fill all required fields with a valid initial deposit amount greater than the funding account balance and select the insufficient funding source<br>3. Click "Open Account" | Validation error indicating the funding source does not have sufficient balance is shown and the account is not opened. | Medium |

#### Edge Case Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 4.ONA-009 | Open Checking account with initial deposit exactly at the minimum | A funding source account has sufficient balance. | 1. Select the Checking account type card<br>2. Fill all required fields (Initial Deposit Amount equal to the Checking minimum, Funding Source Account selecting an account with sufficient balance)<br>3. Click "Open Account" | Success shows "Account opened successfully!" and Success redirects to accounts overview; the new Checking account appears in the accounts listing. | Low |
| 4.ONA-010 | Open Savings account with initial deposit exactly at the minimum | A funding source account has sufficient balance. | 1. Select the Savings account type card<br>2. Fill all required fields (Initial Deposit Amount equal to the Savings minimum, Funding Source Account selecting an account with sufficient balance)<br>3. Click "Open Account" | Success shows "Account opened successfully!" and Success redirects to accounts overview; the new Savings account appears in the accounts listing. | Low |

---

### Transfer Funds

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 5.TRAFUN-001 | Perform internal transfer between own accounts successfully | User is logged in and Transfer Funds page is open. | 1. Select the 'My ParaBank Account' transfer type radio button<br>2. Fill all required fields (choose Source Account, choose Destination Account from user's own accounts, enter a valid Transfer Amount within available balance)<br>3. Click 'Transfer' | Displays "Transfer completed successfully." and a transaction ID. | High |
| 5.TRAFUN-002 | Perform external transfer with valid account numbers and sufficient funds | User is logged in and has at least one Checking or Savings account with sufficient balance | 1. Select the radio option for 'External Account' transfer type<br>2. Fill all required fields (Source Account: select a Checking or Savings account, Transfer Amount: enter an amount within available balance, External Account Number: enter valid account number, Confirm Account Number: enter the same account number)<br>3. Click 'Submit' or 'Transfer' | 'Transfer completed successfully.' message is shown and a transaction ID is displayed | High |
| 5.TRAFUN-005 | Destination options update when transfer type toggled | User is logged in and Transfer Funds page is open. | 1. Select the 'My ParaBank Account' transfer type radio button<br>2. Verify destination options allow selecting from the user's own accounts<br>3. Select the 'External Account' transfer type radio button<br>4. Verify destination input changes to accept external account details | Destination options change based on transfer type. | Medium |
| 5.TRAFUN-006 | Source Account dropdown shows only Checking and Savings accounts | User has multiple accounts of different types. | 1. Open the Source Account dropdown<br>2. Verify only Checking and Savings accounts are listed as selectable options | Source Account dropdown is filtered to Checking and Savings accounts only. | Medium |
| 5.TRAFUN-007 | Destination options update when switching to External Account transfer type | User is logged in | 1. Select the radio option for 'External Account' transfer type<br>2. Observe that destination inputs update to show external-specific options (External Account Number and Confirm Account Number fields) | Destination options change based on transfer type and external account fields are displayed | Medium |
| 5.TRAFUN-008 | Source Account dropdown shows only Checking and Savings accounts | User is logged in and has multiple account types | 1. Open the Source Account dropdown<br>2. Verify the listed options | Source Account dropdown filtered to Checking and Savings accounts only | Medium |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 5.TRAFUN-003 | Transfer fails when source account has insufficient funds | User is logged in and Transfer Funds page is open and the selected source account balance is less than the intended transfer amount. | 1. Select the source account with insufficient balance and select a valid destination account<br>2. Enter a Transfer Amount greater than the source account's available balance<br>3. Click 'Transfer' | Contextual error indicating insufficient funds is displayed and the transfer is not processed. | High |
| 5.TRAFUN-004 | Fail transfer when external account numbers do not match | User is logged in and has at least one Checking or Savings account | 1. Select 'External Account' transfer type<br>2. Fill all other required fields correctly (Source Account, Transfer Amount), enter an external account number and a different Confirm Account Number<br>3. Click 'Submit' or 'Transfer' | Error 'Account numbers do not match.' is displayed and the transfer is not processed. | High |
| 5.TRAFUN-009 | Submit transfer with all required fields empty | User is logged in and Transfer Funds page is open. | 1. Leave all required fields empty<br>2. Click 'Transfer' | Validation errors shown for all required fields. | Medium |
| 5.TRAFUN-010 | Transfer fails with invalid amount format | User is logged in and Transfer Funds page is open. | 1. Fill all required fields, entering a non-numeric or improperly formatted value into the Transfer Amount field<br>2. Click 'Transfer' | Validation error indicating invalid transfer amount format is displayed. | Medium |
| 5.TRAFUN-011 | Submit with all required fields empty | User is logged in | 1. Leave all required fields empty<br>2. Click 'Submit' or 'Transfer' | Validation errors shown for all required fields. | Medium |
| 5.TRAFUN-012 | Submit with Confirm Account Number empty for external transfer | User is logged in | 1. Select 'External Account' transfer type<br>2. Fill all other required fields, leave Confirm Account Number empty<br>3. Click 'Submit' or 'Transfer' | Validation error indicating account number confirmation is required and the transfer is not processed. | Medium |

---

### Payments

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 6.PAYMEN-001 | Submit payment with valid details and sufficient funds | Source account has sufficient available funds. | 1. Fill all required fields (Payee Name, Street Address, City, State, ZIP Code, Phone Number, Payee Account Number, Confirm Account Number, Payment Amount, Source Account) ensuring Payee Account Number and Confirm Account Number match and Payment Amount is within available funds<br>2. Click "Pay" | Payment submitted successfully with a reference code and the source account balance is updated. | High |
| 6.PAYMEN-002 | Form remains editable after validation errors and allows retry | None | 1. Fill all required fields with an input that triggers a validation error (for example, mismatched account numbers)<br>2. Click "Pay"<br>3. Correct the invalid field(s) so all validations pass, then click "Pay" again | Validation error displayed after the first attempt, the form remains editable, and after correction the payment submits successfully with a reference code and balances update. | Medium |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 6.PAYMEN-003 | Submit with all required fields empty | None | 1. Leave all required fields empty<br>2. Click "Pay" | Validation errors shown for all required fields and errors displayed inline. | Medium |
| 6.PAYMEN-004 | Submit payment with mismatched account numbers | None | 1. Fill all required fields, set Payee Account Number and Confirm Account Number to different values<br>2. Click "Pay" | Inline error shown stating the account numbers do not match and the form remains editable. | Medium |

#### Edge Case Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 6.PAYMEN-005 | Submit payment equal to available funds (boundary case) | Source account available funds equal the Payment Amount. | 1. Fill all required fields with Payment Amount equal to the source account's available funds and matching account numbers<br>2. Click "Pay" | Payment submitted successfully with a reference code and the source account balance becomes zero. | Low |

---

### Request Loan

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 7.REQLOA-001 | Request Personal loan successfully (approved by credit engine) | User is authenticated and Request Loan page is open. | 1. Click the "Personal" loan type card<br>2. Fill all required fields (Loan Amount within Personal range, Down Payment meeting minimum percentage and less than Loan Amount, select Collateral Account with sufficient funds)<br>3. Click "Apply" | Displays "Loan approved and created successfully!" and shows new loan account details. | High |
| 7.REQLOA-002 | Request Auto loan successfully (approved by credit engine) | User is authenticated and Request Loan page is open. | 1. Click the "Auto" loan type card<br>2. Fill all required fields (Loan Amount within Auto range, Down Payment meeting minimum percentage and less than Loan Amount, select Collateral Account with sufficient funds)<br>3. Click "Apply" | Displays "Loan approved and created successfully!" and shows new loan account details. | High |
| 7.REQLOA-003 | Request Home loan successfully (approved by credit engine) | User is authenticated and Request Loan page is open. | 1. Click the "Home" loan type card<br>2. Fill all required fields (Loan Amount within Home range, Down Payment meeting minimum percentage and less than Loan Amount, select Collateral Account with sufficient funds)<br>3. Click "Apply" | Displays "Loan approved and created successfully!" and shows new loan account details. | High |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 7.REQLOA-004 | Loan denied by credit engine shows insufficient credit history reason | User is authenticated and Request Loan page is open. | 1. Select a loan type card<br>2. Fill all required fields (Loan Amount within allowed range, Down Payment meeting minimum percentage and less than Loan Amount, select Collateral Account with sufficient funds) and submit in a way that triggers credit engine denial<br>3. Click "Apply" | Application is denied and the denial reason "Insufficient credit history" is displayed. | High |
| 7.REQLOA-005 | Submit with all required fields empty | User is authenticated and Request Loan page is open. | 1. Leave all required fields empty<br>2. Click "Apply" | Validation errors shown for all required fields. | Medium |
| 7.REQLOA-006 | Reject when Loan Amount is below minimum for selected loan type | User is authenticated and Request Loan page is open. | 1. Select any loan type card<br>2. Fill all required fields (Loan Amount set below the allowed minimum for the selected loan type, valid Down Payment less than Loan Amount, select Collateral Account with sufficient funds)<br>3. Click "Apply" | Validation error indicating the loan amount is outside the allowed range for the selected loan type. | Medium |
| 7.REQLOA-007 | Reject when Loan Amount exceeds maximum for selected loan type | User is authenticated and Request Loan page is open. | 1. Select any loan type card<br>2. Fill all required fields (Loan Amount set above the allowed maximum for the selected loan type, valid Down Payment less than Loan Amount, select Collateral Account with sufficient funds)<br>3. Click "Apply" | Validation error indicating the loan amount is outside the allowed range for the selected loan type. | Medium |
| 7.REQLOA-008 | Reject when Down Payment is equal to or greater than Loan Amount | User is authenticated and Request Loan page is open. | 1. Select a loan type card<br>2. Fill all required fields (Loan Amount set, Down Payment set equal to or greater than Loan Amount, select Collateral Account with sufficient funds)<br>3. Click "Apply" | Validation error indicating the Down Payment must be less than the Loan Amount. | Medium |
| 7.REQLOA-009 | Reject when Down Payment is below 10% minimum requirement | User is authenticated and Request Loan page is open. | 1. Select a loan type card<br>2. Fill all required fields (Loan Amount set within allowed range, Down Payment set below the 10% minimum, select Collateral Account with sufficient funds)<br>3. Click "Apply" | Validation error indicating the Down Payment does not meet the minimum percentage requirement. | Medium |
| 7.REQLOA-010 | Reject when collateral funds are insufficient relative to required collateral value | User is authenticated and Request Loan page is open. | 1. Select a loan type card<br>2. Fill all required fields (Loan Amount set within allowed range, Down Payment meeting minimum percentage and less than Loan Amount, select Collateral Account with funds insufficient to meet collateral requirement)<br>3. Click "Apply" | Application is rejected or shows a validation/denial message such as "Inadequate collateral value." | Medium |

#### Edge Case Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 7.REQLOA-011 | Accept loan amount at minimum boundary (triggerable for: Personal, Auto, Home) | User is authenticated and Request Loan page is open. | 1. Select a loan type card<br>2. Fill all required fields in the form (Loan Amount set to the minimum allowed for the selected loan type, Down Payment meeting minimum percentage and less than Loan Amount, select Collateral Account with sufficient funds)<br>3. Click "Apply" | Loan proceeds and, if approved by credit engine, displays "Loan approved and created successfully!" with account details. | Medium |
| 7.REQLOA-012 | Accept Down Payment exactly at 10% minimum requirement | User is authenticated and Request Loan page is open. | 1. Select a loan type card<br>2. Fill all required fields (Loan Amount set within allowed range, Down Payment set to exactly the 10% minimum, select Collateral Account with sufficient funds)<br>3. Click "Apply" | Loan proceeds to credit evaluation; if approved, displays "Loan approved and created successfully!" with account details. | Medium |

---

### Update Contact Info

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 8.UCI-001 | Form displays pre-filled contact information | User is signed in and Update Contact Info page is open | 1. Observe the values in all form fields (First Name, Last Name, Street Address, City, State, ZIP Code, Phone Number) | All listed fields are populated with the user's existing contact information. | High |
| 8.UCI-002 | Update profile with valid changes and save | User is signed in and Update Contact Info page is open | 1. Modify one or more contact fields with valid values (First Name, Last Name, Street Address, City, State, ZIP Code, Phone Number)<br>2. Click "Update Profile" | "Profile updated successfully." is displayed and the form refreshes to show the updated contact information. | High |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 8.UCI-003 | Submit with all required fields empty | User is signed in and Update Contact Info page is open | 1. Clear all required fields (First Name, Last Name, Street Address, City, State, ZIP Code, Phone Number)<br>2. Click "Update Profile" | Validation errors shown for all required fields; invalid fields are highlighted and an inline error banner is displayed. | Medium |
| 8.UCI-004 | Submit with invalid ZIP Code format | User is signed in and Update Contact Info page is open | 1. Fill all required fields with valid values except enter an invalid format for ZIP Code<br>2. Click "Update Profile" | Validation error shown for the ZIP Code field, the field is highlighted and an inline error banner is displayed. | Medium |
| 8.UCI-005 | Submit with invalid Phone Number format | User is signed in and Update Contact Info page is open | 1. Fill all required fields with valid values except enter an invalid format for Phone Number<br>2. Click "Update Profile" | Validation error shown for the Phone Number field, the field is highlighted and an inline error banner is displayed. | Medium |

---

### Manage Cards

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 9.MANCAR-001 | Request a Debit card with valid account and complete shipping address | User is signed in and the Request Card page is open. | 1. Select Card Type as Debit<br>2. Select an account that is in good standing to link<br>3. Fill a complete shipping address<br>4. Click "Request Card" | A card-request ticket is created and the UI shows "Card request submitted successfully." with a tracking ID. | High |
| 9.MANCAR-002 | Request a Credit card with valid account and complete shipping address | User is signed in and the Request Card page is open. | 1. Select Card Type as Credit<br>2. Select an account that is in good standing to link<br>3. Fill a complete shipping address<br>4. Click "Request Card" | A card-request ticket is created and the UI shows "Card request submitted successfully." with a tracking ID. | High |
| 9.MANCAR-003 | Update card controls with valid limit, travel notice, and allowed status change | Manage Cards Update Controls page is open and at least one card exists. | 1. Select an existing card<br>2. Fill all required fields (New Spending Limit with a valid amount within policy, Travel Notice with valid dates and destinations, Card Status to an allowed new value)<br>3. Click "Update Controls" | The message "Card controls updated successfully." is displayed and the card's spending limit, travel notice, and status reflect the submitted changes. | High |
| 9.MANCAR-004 | Update only the spending limit with a valid amount | Manage Cards Update Controls page is open and at least one card exists. | 1. Select an existing card<br>2. Fill New Spending Limit with a valid amount within policy<br>3. Click "Update Controls" | The message "Card controls updated successfully." is displayed and the card's spending limit is updated. | High |
| 9.MANCAR-005 | Change card status to a valid new status | Manage Cards Update Controls page is open and at least one card exists. | 1. Select an existing card<br>2. Set Card Status to a valid target status (e.g., change to Frozen if allowed for that card)<br>3. Click "Update Controls" | The message "Card controls updated successfully." is displayed and the card's status is updated accordingly. | High |
| 9.MANCAR-006 | Add a travel notice with destination only (dates optional) | Manage Cards Update Controls page is open and at least one card exists. | 1. Select an existing card<br>2. Fill Travel Notice with destination(s) only, leaving dates blank<br>3. Click "Update Controls" | The message "Card controls updated successfully." is displayed and the travel notice destination is recorded for the card. | Medium |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 9.MANCAR-007 | Submit with all required fields empty | User is signed in and the Request Card page is open. | 1. Leave all required fields empty<br>2. Click "Request Card" | Validation errors shown for all required fields. | Medium |
| 9.MANCAR-008 | Submit with Account to Link empty | User is signed in and the Request Card page is open. | 1. Select a Card Type and fill a complete shipping address, leave Account to Link empty<br>2. Click "Request Card" | Validation error indicating an account must be selected or the request is rejected due to missing account selection. | Medium |
| 9.MANCAR-009 | Submit with Shipping Address empty | User is signed in and the Request Card page is open. | 1. Select a Card Type and select a valid account in good standing, leave Shipping Address empty<br>2. Click "Request Card" | Validation error indicating the shipping address is required. | Medium |
| 9.MANCAR-010 | Submit with incomplete shipping address | User is signed in and the Request Card page is open. | 1. Select a Card Type and select a valid account in good standing<br>2. Fill a shipping address that is missing required components<br>3. Click "Request Card" | Validation error indicating the shipping address is incomplete and the request is not submitted. | Medium |
| 9.MANCAR-011 | Submit using an account that is not in good standing | User is signed in and the Request Card page is open. | 1. Select a Card Type and select an account that is flagged as not in good standing<br>2. Fill a complete shipping address<br>3. Click "Request Card" | Request is rejected with an error indicating the selected account cannot be used due to its standing. | Medium |
| 9.MANCAR-012 | Submit with all required fields empty | Manage Cards Update Controls page is open. | 1. Leave all required fields empty<br>2. Click "Update Controls" | Validation errors shown for all required fields and the form remains editable. | Medium |
| 9.MANCAR-013 | Attempt to set a spending limit above policy | Manage Cards Update Controls page is open and at least one card exists. | 1. Select an existing card<br>2. Fill New Spending Limit with an amount above the allowed policy<br>3. Click "Update Controls" | An inline validation error indicates the spending limit exceeds policy and the form remains editable. | Medium |
| 9.MANCAR-014 | Enter a travel notice with an invalid date range (end date before start date) | Manage Cards Update Controls page is open and at least one card exists. | 1. Select an existing card<br>2. Fill Travel Notice with a start date and an end date where the end date is before the start date<br>3. Click "Update Controls" | An inline validation error indicates the date range is invalid and the form remains editable. | Medium |
| 9.MANCAR-015 | Attempt a disallowed card-status transition | Manage Cards Update Controls page is open and a card exists whose current status prohibits the chosen new status. | 1. Select the card whose current status disallows the chosen transition<br>2. Set Card Status to the disallowed target status<br>3. Click "Update Controls" | An inline validation error indicates the status transition is not allowed and the form remains editable. | Medium |

#### Edge Case Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 9.MANCAR-016 | Set spending limit exactly at the policy maximum | Manage Cards Update Controls page is open and at least one card exists. | 1. Select an existing card<br>2. Fill New Spending Limit with an amount equal to the policy maximum<br>3. Click "Update Controls" | The message "Card controls updated successfully." is displayed and the card's spending limit is updated to the policy maximum. | Low |
| 9.MANCAR-017 | Add a single-day travel notice (start date equals end date) | Manage Cards Update Controls page is open and at least one card exists. | 1. Select an existing card<br>2. Fill Travel Notice with start date and end date set to the same valid day and provide destination(s)<br>3. Click "Update Controls" | Either the travel notice is accepted and "Card controls updated successfully." is displayed or an inline validation error explains the date range issue, with the form remaining editable. | Low |

---

### Investments

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 10.INVEST-001 | Execute same-day Buy trade successfully | User has sufficient buying power and the fund symbol exists. | 1. Fill all required fields (Action = Buy, Fund Symbol with a valid existing symbol, Quantity with a positive number, select Funding Account)<br>2. Click "Execute Trade" | Trade executed successfully with a same-day order; holdings and portfolio snapshot update and a confirmation displays "Trade executed successfully." with an order ID. | High |
| 10.INVEST-002 | Execute same-day Sell trade successfully | User holds sufficient shares of the specified fund and the fund symbol exists. | 1. Fill all required fields (Action = Sell, Fund Symbol with a valid existing symbol, Quantity less than or equal to held shares, select Destination Account)<br>2. Click "Execute Trade" | Trade executed successfully with a same-day order; holdings and portfolio snapshot update and a confirmation displays "Trade executed successfully." with an order ID. | High |
| 10.INVEST-003 | Create recurring investment plan with Weekly frequency | User is on the Create Recurring Investment Plan page | 1. Fill all required fields (Fund Symbol, Contribution Amount, Frequency set to Weekly, Start Date in the future, Funding Account with adequate balance)<br>2. Click "Create Plan" | Schedule is stored and confirmation message "Plan created successfully." is displayed. | High |
| 10.INVEST-004 | Create recurring investment plan with Monthly frequency | User is on the Create Recurring Investment Plan page | 1. Fill all required fields (Fund Symbol, Contribution Amount, Frequency set to Monthly, Start Date in the future, Funding Account with adequate balance)<br>2. Click "Create Plan" | Schedule is stored and confirmation message "Plan created successfully." is displayed. | High |
| 10.INVEST-007 | Portfolio snapshot is read-only and displays holdings details | Portfolio snapshot is visible on the Execute Trade page. | 1. Observe the portfolio snapshot area | Portfolio snapshot is read-only and shows current fund holdings, market value, and unrealised gain or loss. | Medium |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 10.INVEST-005 | Reject Buy when insufficient buying power | User does not have sufficient buying power for the requested purchase. | 1. Fill all required fields (Action = Buy, Fund Symbol with a valid existing symbol, Quantity that exceeds buying power, select Funding Account)<br>2. Click "Execute Trade" | Inline error indicating insufficient buying power and the trade is not executed. | High |
| 10.INVEST-006 | Reject Sell when requested quantity exceeds share balance | User does not hold sufficient shares of the specified fund. | 1. Fill all required fields (Action = Sell, Fund Symbol with a valid existing symbol, Quantity greater than current share balance, select Destination Account)<br>2. Click "Execute Trade" | Inline error indicating insufficient share balance and the trade is not executed. | High |
| 10.INVEST-008 | Submit with all required fields empty | None | 1. Leave all required fields empty<br>2. Click "Execute Trade" | Validation errors shown for all required fields (inline). | Medium |
| 10.INVEST-009 | Reject trade when Fund Symbol does not exist | All other required fields are filled with valid values. | 1. Fill all required fields (Action, Quantity, Funding/Destination Account) and enter a non-existent Fund Symbol<br>2. Click "Execute Trade" | Inline validation error indicating the fund symbol is invalid or not found; trade is not executed. | Medium |
| 10.INVEST-010 | Reject trade when Quantity is zero or negative | All other required fields are filled with valid values. | 1. Fill all required fields (Action, Fund Symbol, Funding/Destination Account) and set Quantity to zero or a negative value<br>2. Click "Execute Trade" | Inline validation error indicating quantity must be greater than zero and trade is not executed. | Medium |
| 10.INVEST-011 | Submit with all required fields empty | User is on the Create Recurring Investment Plan page | 1. Leave all required fields empty<br>2. Click "Create Plan" | Validation errors shown for all required fields. | Medium |
| 10.INVEST-012 | Submit with Start Date field empty | User is on the Create Recurring Investment Plan page | 1. Fill all other required fields with valid values, leave Start Date empty<br>2. Click "Create Plan" | Validation error indicating the Start Date is required and highlighted. | Medium |
| 10.INVEST-013 | Submit with Contribution Amount field empty | User is on the Create Recurring Investment Plan page | 1. Fill all other required fields with valid values, leave Contribution Amount empty<br>2. Click "Create Plan" | Validation error indicating the Contribution Amount is required and highlighted. | Medium |
| 10.INVEST-014 | Submit with Funding Account field empty | User is on the Create Recurring Investment Plan page | 1. Fill all other required fields with valid values, leave Funding Account empty<br>2. Click "Create Plan" | Validation error indicating the Funding Account is required and highlighted. | Medium |
| 10.INVEST-015 | Reject plan when Start Date is not in the future | User is on the Create Recurring Investment Plan page | 1. Fill all required fields with valid values, set Start Date to a past date<br>2. Click "Create Plan" | Validation error shown for Start Date (for example, "Start date must be in the future") and field is highlighted. | Medium |
| 10.INVEST-016 | Reject plan when Contribution Amount is below minimum | User is on the Create Recurring Investment Plan page | 1. Fill all required fields with valid values, set Contribution Amount below the minimum<br>2. Click "Create Plan" | Validation error indicating the Contribution Amount does not meet the minimum and the field is highlighted. | Medium |
| 10.INVEST-017 | Reject plan when Funding Account has inadequate balance | User is on the Create Recurring Investment Plan page | 1. Fill all required fields with valid values, select a Funding Account with insufficient balance<br>2. Click "Create Plan" | Validation error indicating the Funding Account has insufficient balance and the field is highlighted. | Medium |

#### Edge Case Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 10.INVEST-018 | Reject plan when Start Date is today (not a future date) | User is on the Create Recurring Investment Plan page | 1. Fill all required fields with valid values, set Start Date to today's date<br>2. Click "Create Plan" | Validation error shown indicating Start Date must be in the future and the field is highlighted. | Low |

---

### Account Statements

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 11.ACCSTA-001 | Generate statement for a selected account using month-and-year period | User is signed in and on the Account Statements page. | 1. Select 'Statement Period' using the month-and-year option and choose a valid month and year<br>2. Select an account from the 'Account' dropdown<br>3. Click "Generate Statement" | Statement generated successfully and the transactions for the selected month are retrieved and displayed. | High |
| 11.ACCSTA-002 | Generate statement using a custom date range | User is signed in and on the Account Statements page. | 1. Choose the custom date range option and fill both start and end dates within a valid interval<br>2. Select an account from the 'Account' dropdown<br>3. Click "Generate Statement" | Statement generated successfully and transactions within the selected date range are retrieved and displayed. | High |
| 11.ACCSTA-003 | Enable paperless statements with valid email | User is signed in and the Account Statements page is open. | 1. Check the paperless statements opt-in checkbox and fill a valid email address in the Email Address field<br>2. Click "Save Preference" | e-Statement preference updated. | High |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 11.ACCSTA-004 | Submit with all required fields empty | User is signed in and on the Account Statements page. | 1. Leave all required fields empty<br>2. Click "Generate Statement" | Validation errors shown for required fields and statement is not generated. | Medium |
| 11.ACCSTA-005 | Fail to generate statement when end date is before start date | User is signed in and on the Account Statements page. | 1. Choose the custom date range option and set the end date earlier than the start date<br>2. Select an account from the 'Account' dropdown<br>3. Click "Generate Statement" | Validation error shown indicating an invalid date range and statement is not generated. | Medium |
| 11.ACCSTA-006 | Handle system failure during statement generation | User is signed in and on the Account Statements page. | 1. Select a valid statement period (month-or custom range) and an account from the 'Account' dropdown<br>2. Click "Generate Statement" | User is shown an error message and the statement is not produced. | Medium |
| 11.ACCSTA-007 | Save preference with all required fields empty | User is signed in and the Account Statements page is open. | 1. Leave all required fields empty<br>2. Click "Save Preference" | Validation errors shown for all required fields. | Medium |
| 11.ACCSTA-008 | Save preference with Email Address empty while opting into paperless | User is signed in and the Account Statements page is open. | 1. Check the paperless statements opt-in checkbox, leave Email Address empty<br>2. Click "Save Preference" | Email field highlighted with guidance and preference not saved. | Medium |
| 11.ACCSTA-009 | Save preference with invalid email format | User is signed in and the Account Statements page is open. | 1. Check the paperless statements opt-in checkbox and fill an invalid email address in the Email Address field<br>2. Click "Save Preference" | Email field highlighted with guidance and preference not saved. | Medium |

---

### Security Settings

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 12.SECSET-001 | Change password with valid current password and strong matching new password | User is logged in and Security Settings panel is open | 1. Expand the Change Password collapsible panel if it is collapsed<br>2. Fill all required fields (Current Password, New Password, Confirm New Password) using the valid current password and a strong matching new password<br>3. Click "Change Password" | Password changed successfully and credentials are updated. | High |
| 12.SECSET-006 | Expand collapsible panel reveals Change Password form fields | User is logged in and Security Settings panel is open | 1. Ensure the Change Password collapsible panel is collapsed<br>2. Expand the Change Password collapsible panel<br>3. Verify the form displays Current Password, New Password, Confirm New Password, and the "Change Password" button | Change Password form fields and button are visible when the collapsible panel is expanded. | Low |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 12.SECSET-002 | Change password fails with incorrect current password | User is logged in and Security Settings panel is open | 1. Fill all required fields (Current Password, New Password, Confirm New Password) with an incorrect current password and a valid strong matching new password<br>2. Click "Change Password" | Change is rejected and an error indicates the current password is incorrect. | High |
| 12.SECSET-003 | Submit with all required fields empty | User is logged in and Security Settings panel is open | 1. Leave all required fields empty<br>2. Click "Change Password" | Validation errors shown for all required fields and the relevant fields are highlighted. | Medium |
| 12.SECSET-004 | Change password fails when New Password and Confirm New Password do not match | User is logged in and Security Settings panel is open | 1. Fill all required fields (Current Password, New Password, Confirm New Password) with a valid current password and non-matching new and confirm values<br>2. Click "Change Password" | Validation error shown indicating the new password and confirmation must match and the mismatch fields are highlighted. | Medium |
| 12.SECSET-005 | Change password fails when new password violates strong-password policy | User is logged in and Security Settings panel is open | 1. Fill all required fields (Current Password, New Password, Confirm New Password) with a valid current password and a weak new password entered in both New and Confirm fields<br>2. Click "Change Password" | Validation error shown indicating the new password does not meet the strong-password requirements and the New Password field is highlighted. | Medium |

---

### Support Center

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 13.SUPCEN-001 | Send a support message with valid subject, category, message body, and attachment | User is signed in and on the Support Center Send Message page. | 1. Fill all fields (valid Subject, select a Category, valid Message Body, attach a file of an allowed type)<br>2. Click "Send Message" | “Message sent successfully.” is displayed and a ticket ID is shown. | High |
| 13.SUPCEN-002 | Send a support message without attachment (attachment optional) | User is signed in and on the Support Center Send Message page. | 1. Fill all required fields (valid Subject, select a Category, valid Message Body), leave Attachment empty<br>2. Click "Send Message" | “Message sent successfully.” is displayed and a ticket ID is shown. | High |
| 13.SUPCEN-003 | Schedule a callback with valid inputs | User is on the Support Center Request Callback form. | 1. Fill all required fields (select Reason for Call, enter Preferred Date at least next business day, select Preferred Time Window, confirm or edit Phone Number) with valid values<br>2. Click "Request Callback" | The page shows "Callback request submitted." and a confirmation email is sent. | High |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 13.SUPCEN-004 | Submit with all required fields empty | User is signed in and on the Support Center Send Message page. | 1. Leave all required fields empty<br>2. Click "Send Message" | Validation errors shown for all required fields and inline guidance is displayed. | Medium |
| 13.SUPCEN-005 | Submit with invalid subject length | User is signed in and on the Support Center Send Message page. | 1. Fill all other required fields (select a Category, valid Message Body), enter a Subject with invalid length<br>2. Click "Send Message" | Inline validation guidance indicating the subject length is invalid is shown. | Medium |
| 13.SUPCEN-006 | Attach an unsupported file type and attempt to send | User is signed in and on the Support Center Send Message page. | 1. Fill all required fields (valid Subject, select a Category, valid Message Body), attach a file of an unsupported type<br>2. Click "Send Message" | Inline guidance indicating the attachment type is not allowed is shown and message is not sent. | Medium |
| 13.SUPCEN-007 | Submit with all required fields empty | User is on the Support Center Request Callback form. | 1. Leave all required fields empty<br>2. Click "Request Callback" | Validation errors shown for all required fields. | Medium |
| 13.SUPCEN-008 | Reject callback request for date earlier than next business day | User is on the Support Center Request Callback form. | 1. Fill all required fields with a Preferred Date that is before the next business day and other fields valid<br>2. Click "Request Callback" | Submission is blocked and an inline validation error indicates the preferred date is invalid. | Medium |

#### Edge Case Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 13.SUPCEN-009 | Accept callback scheduled for the next business day boundary | User is on the Support Center Request Callback form. | 1. Fill all required fields with Preferred Date equal to the next business day and other fields valid<br>2. Click "Request Callback" | The page shows "Callback request submitted." and a confirmation email is sent. | Low |

---

## Navigation Graph

![Navigation Graph](Output/Parabank/navigation_graph.png)

### Pages

| Module | URL | Auth Required | Test Cases |
|--------|-----|---------------|------------|
| Login | /login | No | 14 |
| Register | /register | No | 23 |
| Accounts Overview | /accounts | Yes | 6 |
| Open New Account | /open-account | Yes | 10 |
| Transfer Funds | /transfer-funds | Yes | 12 |
| Payments | /bill-pay | Yes | 5 |
| Request Loan | /request-loan | Yes | 12 |
| Update Contact Info | /update-contact-info | Yes | 5 |
| Manage Cards | /manage-cards | Yes | 17 |
| Investments | /investments | Yes | 18 |
| Account Statements | /statements | Yes | 9 |
| Security Settings | /security-settings | Yes | 6 |
| Support Center | /support | Yes | 9 |
