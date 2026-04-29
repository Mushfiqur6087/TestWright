# Parabank

**Base URL:** 
**Generated:** 2026-04-29T11:28:19.015157

## Summary

| Metric | Count |
|--------|-------|
| **Total Tests** | 139 |

### By Type

| Type | Count |
|------|-------|
| Positive | 58 |
| Negative | 64 |
| Edge Case | 17 |

### By Priority

| Priority | Count |
|----------|-------|
| High | 66 |
| Medium | 68 |
| Low | 5 |

---

## Test Cases

### Login

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 1.LOGIN-001 | Successful sign in using username | None | 1. Fill all required fields (Email/Username with a registered username, Password with the corresponding valid password)<br>2. Click "Sign In" | User sees "Signed in successfully." and is redirected to the Accounts Overview page. | High |
| 1.LOGIN-002 | Protected routes inaccessible after logout | User has just logged out after an active session | 1. After logging out, attempt to navigate to a protected page (for example, Transfer Funds) by entering its direct URL.<br>2. Observe the application's response to the navigation attempt.<br>3. Verify access to the protected page is denied or the user is redirected to the login page. | Attempts to access protected routes after logout result in redirection to the login page or an access-denied response. | High |
| 1.LOGIN-003 | Direct URL access while logged out redirects to login | User is not logged in | 1. Open a browser and enter the direct URL for a protected page (for example, the Accounts Overview page).<br>2. Observe the browser navigation after the request completes.<br>3. Verify the login page is displayed and the login form (Email/Username and Password fields) is present. | The user is redirected to the login page and presented with the login form instead of the protected content. | High |
| 1.LOGIN-004 | Open forgot password flow via "Forgot Password?" link | User is on the login page. | 1. Verify the "Forgot Password?" link is visible and enabled on the login page<br>2. Click the "Forgot Password?" link | Reset-password workflow is initiated and a reset form or instructions are displayed. | High |
| 1.LOGIN-005 | Logout from user menu terminates session and shows login page | User is logged in | 1. While logged in, open the user/profile menu and click the Log Out option.<br>2. Wait for the application to complete the logout action and navigate.<br>3. Verify the login page is displayed and authenticated UI elements (account lists, balances, protected navigation) are no longer visible. | The session is terminated and the login page is displayed instead of authenticated content. | High |
| 1.LOGIN-006 | Browser refresh after logout does not restore authenticated session | User has just logged out | 1. After completing logout and confirming the login page is displayed, click the browser refresh/reload button.<br>2. Wait for the page to finish reloading.<br>3. Verify no authenticated content reappears and the user remains on the login page. | Refreshing the browser after logout does not restore the authenticated session and no protected content is shown. | High |
| 1.LOGIN-008 | Page refresh while logged in keeps user logged in | User is logged in on an authenticated page | 1. While authenticated and viewing a protected page (for example, Accounts Overview), click the browser refresh/reload button.<br>2. Wait for the page to finish reloading.<br>3. Verify the user remains authenticated and the protected page re-renders without redirecting to the login page. | After refresh the user remains logged in and the protected page content is displayed (no redirect to login). | Medium |
| 1.LOGIN-009 | Already-logged-in user navigating to login URL is redirected to authenticated landing page | User is already logged in | 1. With an active authenticated session, navigate to the application's login URL.<br>2. Observe the resulting navigation behavior.<br>3. Verify the user is redirected away from the login page to the authenticated landing page (for example, Accounts Overview) and the login form is not shown. | The application redirects the already-authenticated user away from the login page to the authenticated landing page. | Medium |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 1.LOGIN-007 | Attempt login with incorrect credentials | None | 1. Fill Email/Username with a registered identifier and Password with an incorrect password<br>2. Click "Sign In" | Error message 'Incorrect email or password. Please try again,' is shown, the password field is cleared, and the user may attempt to sign in again. | High |
| 1.LOGIN-010 | Submit with all required fields empty | None | 1. Leave all required fields empty<br>2. Click "Sign In" | Validation errors shown for all required fields. | Medium |
| 1.LOGIN-011 | Attempt sign in with password not meeting complexity requirements | None | 1. Fill all required fields (Email/Username with a registered identifier, Password that does not meet the specified complexity)<br>2. Click "Sign In" | Authentication fails showing "Incorrect email or password. Please try again," and the password field is cleared. | Medium |

#### Edge Case Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 1.LOGIN-012 | Login with password at minimum length that meets complexity | None | 1. Fill Email/Username with a registered identifier and Password with a value exactly at the minimum required length that satisfies uppercase, lowercase, number, and special character rules<br>2. Click "Sign In" | Flash message 'Signed in successfully.' is shown and the user is redirected to the Accounts Overview page. | Medium |

---

### Register

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 2.REGIST-001 | Auto-format SSN while typing | None | 1. Focus the Social Security Number field<br>2. Type a continuous sequence of numeric digits into the SSN field<br>3. Observe the field content as digits are entered | Field content updates incrementally to match the 123-45-6789 pattern as the user types. | High |
| 2.REGIST-002 | Register with all valid inputs | None | 1. Fill all required fields (First Name, Last Name, Street Address, City, State, ZIP Code, Phone Number, Social Security Number, Username, Password, Confirm Password) with valid values<br>2. Click "Register" | Success message "Account created successfully — please sign in" is displayed and the page redirects to the login page | High |
| 2.REGIST-003 | Auto-format phone number on blur | None | 1. Fill Phone Number with a valid ten-digit numeric string (no formatting)<br>2. Move focus out of the Phone Number field | Phone Number is displayed in the (123) 456-7890 format. | High |
| 2.REGIST-004 | Auto-format phone number when pasted | None | 1. Paste an unformatted or variably formatted ten-digit phone number into the Phone Number field | Phone Number is normalized and displayed in the (123) 456-7890 format. | High |
| 2.REGIST-005 | Auto-format phone number while typing | None | 1. Type a valid ten-digit phone number digit-by-digit into the Phone Number field | Phone Number updates incrementally and ends up in the (123) 456-7890 format. | High |
| 2.REGIST-006 | Successful registration shows success message and redirects to login | None | 1. Fill all required registration fields with valid values<br>2. Click "Register" | The message "Account created successfully — please sign in" is displayed and the user is redirected to the login page. | High |
| 2.REGIST-011 | Accept 5-digit ZIP Code during registration | None | 1. Fill all required fields with valid values including a valid 5-digit ZIP Code<br>2. Click "Register" | Registration proceeds without ZIP Code format errors and success message is shown | Medium |
| 2.REGIST-012 | Phone number auto-formats on input during registration | None | 1. Fill all required fields with valid values except Phone Number; enter unformatted numeric digits into Phone Number field<br>2. Move focus out of the Phone Number field | Phone Number is automatically formatted to (123) 456-7890 in the Phone Number field | Medium |
| 2.REGIST-013 | Social Security Number auto-formats on input during registration | None | 1. Fill all required fields with valid values except Social Security Number; enter unformatted numeric digits into Social Security Number field<br>2. Move focus out of the Social Security Number field | Social Security Number is automatically formatted to 123-45-6789 in the SSN field | Medium |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 2.REGIST-007 | Submit with Password field empty | Registration page is open. | 1. Fill all other required fields with valid values, leave Password empty<br>2. Click "Register" | Validation error indicating Password is required. | High |
| 2.REGIST-008 | Submit with invalid Username format | Registration page is open. | 1. Fill all required fields with valid values, enter an invalid email format into Username<br>2. Click "Register" | Validation error indicating Username must be a valid email format. | High |
| 2.REGIST-009 | Submit with non-matching Confirm Password | Registration page is open. | 1. Fill all required fields with valid values, enter a valid Password and enter a different value in Confirm Password<br>2. Click "Register" | Validation error indicating Confirm Password must match the Password field. | High |
| 2.REGIST-010 | Submit with Password shorter than required length | Registration page is open. | 1. Fill all required fields with valid values, enter a Password shorter than the minimum length and set Confirm Password to the same short value<br>2. Click "Register" | Validation error indicating Password must meet minimum length requirement. | High |
| 2.REGIST-014 | Submit with City field empty | Registration page is open. | 1. Fill all other required fields with valid values, leave City empty<br>2. Click "Register" | Validation error indicating City is required. | Medium |
| 2.REGIST-015 | Submit with State not selected | Registration page is open. | 1. Fill all other required fields with valid values, leave State unselected<br>2. Click "Register" | Validation error indicating State is required. | Medium |
| 2.REGIST-016 | Submit with ZIP Code field empty | Registration page is open. | 1. Fill all other required fields with valid values, leave ZIP Code empty<br>2. Click "Register" | Validation error indicating ZIP Code is required. | Medium |
| 2.REGIST-017 | Submit with Last Name field empty | Registration page is open. | 1. Fill all other required fields with valid values, leave Last Name empty<br>2. Click "Register" | Validation error indicating Last Name is required. | Medium |
| 2.REGIST-018 | Submit with Phone Number field empty | Registration page is open. | 1. Fill all other required fields with valid values, leave Phone Number empty<br>2. Click "Register" | Validation error indicating Phone Number is required. | Medium |
| 2.REGIST-019 | Submit with improperly formatted SSN | None | 1. Fill all other required fields with valid values, set Social Security Number to an incorrectly formatted value<br>2. Click "Register" | Field-level validation error shown indicating SSN format is invalid. | Medium |
| 2.REGIST-020 | Submit with all required fields empty | None | 1. Leave all required fields empty<br>2. Click "Register" | Validation errors shown for all required fields. | Medium |
| 2.REGIST-021 | Submit with Street Address field empty | Registration page is open. | 1. Fill all other required fields with valid values, leave Street Address empty<br>2. Click "Register" | Validation error indicating Street Address is required. | Medium |
| 2.REGIST-022 | Submit with improperly formatted Phone Number | None | 1. Fill all other required fields with valid values, set Phone Number to an incorrectly formatted value<br>2. Click "Register" | Field-level validation error shown indicating Phone Number format is invalid. | Medium |
| 2.REGIST-023 | Submit with Social Security Number field empty | Registration page is open. | 1. Fill all other required fields with valid values, leave Social Security Number empty<br>2. Click "Register" | Validation error indicating Social Security Number is required. | Medium |

#### Edge Case Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 2.REGIST-024 | Partial SSN (fewer than nine digits) does not produce complete formatting on blur | None | 1. Enter fewer than nine digits into the Social Security Number field<br>2. Move focus away from the Social Security Number field | No complete 123-45-6789 formatting is applied; the field does not show the full formatted pattern. | Medium |

---

### Accounts Overview

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 3.ACCOVE-001 | Dashboard shows welcome message with user's name | User is logged in and Accounts Overview dashboard is displayed | 1. Locate the welcome message area on the dashboard<br>2. Verify the welcome message contains the logged-in user's name | Welcome message displays the user's name. | High |
| 3.ACCOVE-002 | Footer displays total balance across all accounts | User is logged in and Accounts Overview dashboard is displayed with multiple accounts | 1. Locate the footer row of the accounts table<br>2. Verify the footer total equals the sum of the Current Balance values from all visible account rows | Footer row displays the correct total balance across all accounts. | High |
| 3.ACCOVE-003 | Accounts table displays required columns in each row | User is logged in and Accounts Overview dashboard is displayed | 1. Inspect the accounts table rows<br>2. Verify each row displays Account Number (clickable element), Account Type, Current Balance, Account Status (Active badge), and Open Date | Every account row shows Account Number, Account Type, Current Balance, Account Status (Active badge), and Open Date. | High |
| 3.ACCOVE-004 | Accounts are ordered by creation date (earliest first) | User is logged in and Accounts Overview dashboard is displayed with multiple accounts | 1. Inspect the Open Date values for the accounts table rows<br>2. Verify the rows are ordered by Open Date with the earliest date appearing first | Table rows are ordered by account creation date (earliest first). | High |
| 3.ACCOVE-006 | Active accounts display an Active status badge | User is logged in and Accounts Overview dashboard is displayed with at least one active account | 1. Inspect the Account Status column for each account row<br>2. Verify active accounts show an Active badge in the status column | Active accounts show an Active badge in the Account Status column. | Medium |

#### Edge Case Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 3.ACCOVE-005 | Account numbers are masked showing only last four digits | User is logged in and Accounts Overview dashboard is displayed | 1. Inspect the Account Number cells in the accounts table<br>2. Verify each displayed account number uses masking and shows only the last four digits with preceding mask characters | Account numbers are displayed in masked format, revealing only the last four digits. | High |
| 3.ACCOVE-007 | Clicking Account Number does not navigate (clickable not implemented yet) | User is logged in and Accounts Overview dashboard is displayed | 1. Click an Account Number entry in the accounts table<br>2. Observe whether the dashboard remains visible and no account detail navigation occurs | Clicking the Account Number does not navigate away from the dashboard (feature not implemented). | Medium |

---

### Open New Account

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 4.ONA-001 | Open new Savings account with valid deposit and sufficient funding | User is authenticated and on the Open New Account page | 1. Select the Savings account type card<br>2. Fill Initial Deposit Amount with a valid numeric amount meeting the Savings minimum<br>3. Select a funding source account with sufficient balance<br>4. Click "Open Account" | Account opened successfully and user is redirected to the accounts overview. | High |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 4.ONA-002 | Submit with all required fields empty | User is authenticated and on the Open New Account page | 1. Leave all required fields empty<br>2. Click "Open Account" | Validation errors shown for all required fields. | Medium |
| 4.ONA-003 | Submit without selecting account type | User is authenticated and on the Open New Account page | 1. Leave account type unselected, fill other required fields with valid values<br>2. Click "Open Account" | Validation error indicating account type must be selected is shown. | Medium |
| 4.ONA-004 | Enter non-numeric Initial Deposit Amount | User is authenticated and on the Open New Account page | 1. Select an account type, fill Initial Deposit Amount with a non-numeric value, select a funding source with sufficient balance<br>2. Click "Open Account" | Validation error indicating the Initial Deposit Amount must be numeric is shown. | Medium |
| 4.ONA-005 | Initial Deposit below minimum for Checking | User is authenticated and on the Open New Account page | 1. Select the Checking account type card<br>2. Fill Initial Deposit Amount with a numeric amount below the Checking minimum, select a funding source with sufficient balance<br>3. Click "Open Account" | Validation error indicating the Initial Deposit Amount does not meet the required minimum is shown. | Medium |
| 4.ONA-006 | Attempt to open account when funding source has insufficient balance | User is authenticated and on the Open New Account page | 1. Select an account type, fill Initial Deposit Amount with a valid numeric amount meeting the selected account minimum<br>2. Select a funding source account that does not have sufficient balance<br>3. Click "Open Account" | Validation error indicating the funding source account lacks sufficient balance is shown. | Medium |

#### Edge Case Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 4.ONA-007 | Real-time validation displays error for non-numeric deposit input | User is authenticated and on the Open New Account page | 1. Select an account type<br>2. Enter a non-numeric value into the Initial Deposit Amount field and observe the field without submitting | A real-time validation error is displayed for the Initial Deposit Amount field without submitting the form. | Low |

---

### Transfer Funds

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 5.TRAFUN-001 | Complete an external transfer successfully | User is on the Transfer Funds page and has a Checking or Savings account with sufficient funds. | 1. Select the "External Account" transfer type<br>2. Select a source account from the Source Account dropdown<br>3. Fill all required fields (External account number, Confirm account number, Transfer Amount) with valid matching values and an amount within the available balance<br>4. Click "Submit" | Transfer completed successfully. A transaction ID is displayed. | High |
| 5.TRAFUN-002 | Transfer funds between own accounts with valid amount | User is authenticated and Transfer Funds form is open. | 1. Select Transfer type "My ParaBank Account"<br>2. Fill all required fields (Source Account: a Checking or Savings account, Destination Account: another own account, Transfer Amount: valid amount within available funds)<br>3. Click "Transfer" | "Transfer completed successfully." message is shown and a transaction ID is displayed. | High |
| 5.TRAFUN-003 | Source Account dropdown shows only Checking and Savings accounts | User is authenticated and Transfer Funds form is open. | 1. Click the Source Account dropdown<br>2. Observe the list of accounts shown | Only Checking and Savings accounts appear in the Source Account dropdown. | High |
| 5.TRAFUN-005 | Destination options update when transfer type changes | User is authenticated and Transfer Funds page is open | 1. Select transfer type "My ParaBank Account" and observe the Destination input/list<br>2. Select transfer type "External Account" and observe the Destination input/list | Destination options change based on the selected transfer type | Medium |
| 5.TRAFUN-006 | Source Account dropdown shows only Checking and Savings | User is authenticated and the Transfer Funds page is open. | 1. Select the "External Account" transfer type<br>2. Open the Source Account dropdown | Source Account dropdown lists only Checking and Savings account options. | Medium |
| 5.TRAFUN-007 | Destination options update when External Account selected | User is authenticated and the Transfer Funds page is open. | 1. Select the "External Account" transfer type<br>2. Observe the destination options/fields on the page | Destination options update to reflect external transfers and account number entry fields are visible. | Medium |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 5.TRAFUN-004 | Transfer fails when insufficient funds are available | User is authenticated and Transfer Funds form is open. | 1. Select Transfer type "My ParaBank Account"<br>2. Fill all required fields (Source Account: account with insufficient balance, Destination Account: another own account, Transfer Amount: amount greater than available balance)<br>3. Click "Transfer" | A contextual error is displayed indicating the transfer cannot proceed due to insufficient funds. | High |
| 5.TRAFUN-008 | Submit with all required fields empty | User is authenticated and Transfer Funds page is open | 1. Leave all required fields empty<br>2. Click "Transfer" | Validation errors shown for all required fields. | Medium |
| 5.TRAFUN-009 | Submit with all required fields empty | User is authenticated and the Transfer Funds page is open. | 1. Select the "External Account" transfer type<br>2. Leave all required fields empty<br>3. Click "Submit" | Validation errors shown for all required fields. | Medium |
| 5.TRAFUN-010 | Submit with mismatched external account numbers | User is on the Transfer Funds page, has a Checking or Savings account, and has selected External Account transfer type. | 1. Select the "External Account" transfer type<br>2. Fill all required fields with valid values, enter a different value in Confirm account number than in External account number<br>3. Click "Submit" | Validation error 'Account numbers do not match.' is displayed. | Medium |
| 5.TRAFUN-011 | Reject transfer with invalid transfer amount format | User is authenticated and the Transfer Funds page is open. | 1. Select the "External Account" transfer type<br>2. Fill all required fields (choose a Source Account, enter matching Account number and Confirm account number, enter an invalid Transfer Amount format)<br>3. Click "Submit" | Validation error shown for the Transfer Amount field. | Medium |

#### Edge Case Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 5.TRAFUN-012 | Reject transfer with zero or negative amount | User is authenticated and Transfer Funds form is open. | 1. Select Transfer type "My ParaBank Account"<br>2. Fill all required fields (Source Account, Destination Account, Transfer Amount: zero or a negative value)<br>3. Click "Transfer" | Validation error shown indicating the transfer amount is invalid. | Medium |

---

### Payments

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 6.PAYMEN-001 | Submit payment with valid details | User is logged in and on the Submit Payment page. | 1. Fill all required fields (Payee Name, Street Address, City, State, ZIP Code, Phone Number, Payee Account Number, Confirm Account Number, Payment Amount, Source Account) with valid and matching values<br>2. Click "Pay" | Success message "Payment submitted successfully." with a reference code is displayed; the payment is executed and account balances are updated. | High |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 6.PAYMEN-002 | Submit with non-matching account numbers | User is logged in and on the Submit Payment page. | 1. Fill all required fields with valid data, enter a Payee Account Number and a different Confirm Account Number<br>2. Click "Pay" | Inline error indicating account numbers do not match is displayed and the form remains editable. | High |
| 6.PAYMEN-003 | Submit with all required fields empty | User is logged in and on the Submit Payment page. | 1. Leave all required fields empty<br>2. Click "Pay" | Validation errors shown for all required fields and the form remains editable. | Medium |

#### Edge Case Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 6.PAYMEN-004 | Submit payment equal to available funds (boundary funds check) | User is logged in and on the Submit Payment page. | 1. Fill all required fields with valid and matching account details and a Payment Amount equal to the available balance of the selected Source Account<br>2. Click "Pay" | Payment submitted successfully with a reference code and the Source Account balance is updated accordingly (reduced by the payment amount). | Medium |

---

### Request Loan

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 7.REQLOA-001 | Auto loan accepts amount at maximum boundary | Request Loan form is visible | 1. Select the Auto loan type card<br>2. Fill all required fields (Loan Amount set to exactly the maximum allowed for the selected loan type)<br>3. Click "Submit" | Loan Amount is accepted and no validation error is shown for the selected loan type | High |
| 7.REQLOA-002 | Home loan accepts amount at minimum boundary | Request Loan form is visible | 1. Select the Home loan type card<br>2. Fill all required fields (Loan Amount set to exactly the minimum allowed for the selected loan type)<br>3. Click "Submit" | Loan Amount is accepted and no validation error is shown for the selected loan type | High |
| 7.REQLOA-003 | Request loan successfully when credit approves | Credit engine approves the application. | 1. Select the desired loan type card (Personal/Auto/Home)<br>2. Fill all required fields (Loan Amount within type-specific range, Down Payment meeting minimum percentage and less than Loan Amount, select Collateral Account with sufficient funds)<br>3. Click "Run Credit Simulation" and confirm approval is displayed<br>4. Click "Submit" to create the loan | Loan approved and created successfully! with the new loan account details displayed. | High |
| 7.REQLOA-004 | Request loan with valid inputs resulting in approval | None | 1. Select the desired loan type card<br>2. Fill all required fields (Loan Amount within the loan type range, Down Payment meeting minimum and less than loan amount)<br>3. Select a Collateral Account with sufficient available funds<br>4. Click "Run Credit Simulation", then when simulation shows approval click "Submit" | When the credit simulation returns approval, the page shows "Loan approved and created successfully!" and the new loan account details are displayed. | High |
| 7.REQLOA-005 | Submit loan request with valid down payment and collateral | User is on the Request Loan page | 1. Fill all required fields (Loan Amount, Down Payment Amount less than Loan Amount and meeting the minimum percentage)<br>2. Select a Collateral Account from the dropdown that has sufficient funds and a collateral value meeting the required percentage<br>3. Click "Request Loan" | Loan request is submitted for credit evaluation and a confirmation is shown. | High |
| 7.REQLOA-006 | Request loan and display approval with created loan details | User is authenticated and the Request Loan form is visible. | 1. Fill all required fields (Loan Amount, Down Payment Amount, Collateral Account, Interest Rate)<br>2. Click "Request Loan" or the form's submit control | "Loan approved and created successfully!" is displayed and the created loan account details are shown on the confirmation. | High |
| 7.REQLOA-007 | Request Personal loan with a valid amount within allowed range | Request Loan form is visible | 1. Select the Personal loan type card<br>2. Fill all required fields (Loan Amount with a valid value within the Personal loan range)<br>3. Click "Submit" | Loan Amount is accepted and no validation error is shown for the selected loan type | High |
| 7.REQLOA-008 | Approve loan shows success message and created loan account details | A loan request is in "Pending Approval" status and approval action is available on the page. | 1. Click "Approve"<br>2. Confirm approval in the approval dialog | The confirmation displays the exact message "Loan approved and created successfully!" and the created loan account details (account number, loan amount, interest rate, down payment, collateral reference) are shown in the approval confirmation. | High |
| 7.REQLOA-009 | Request loan with valid inputs resulting in denial displays reasons | None | 1. Select the desired loan type card<br>2. Fill all required fields (Loan Amount within the loan type range, Down Payment meeting minimum and less than loan amount)<br>3. Select a Collateral Account<br>4. Click "Run Credit Simulation" | When the credit simulation returns denial, denial reasons are displayed such as "Insufficient credit history" or "Inadequate collateral value". | High |
| 7.REQLOA-010 | Simulate credit approval with valid inputs results in loan creation | None | 1. Fill all required fields (Loan Amount, Down Payment Amount, Collateral Account) with valid values ensuring down payment meets the minimum<br>2. Click "Simulate Credit Approval" | "Loan approved and created successfully!" message is displayed and the newly created loan account details are shown; account balances remain unchanged (no actual balance debits occur). | High |
| 7.REQLOA-011 | Display 'Inadequate collateral value' when collateral validation fails | None | 1. Fill all required fields with values expected to pass credit but fail collateral validation and select the collateral account with insufficient value<br>2. Click "Apply" | Loan application is denied and a specific denial reason 'Inadequate collateral value' is displayed. | High |
| 7.REQLOA-017 | Display multiple denial reasons when more than one check fails | None | 1. Fill all required fields with values that would concurrently fail multiple validations (for example, credit eligibility and collateral value)<br>2. Click "Apply" | Loan application is denied and all applicable denial reasons are displayed as a list (e.g., credit and collateral reasons). | Medium |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 7.REQLOA-012 | Reject when Down Payment equals or exceeds Loan Amount | Request Loan form is open. | 1. Fill Down Payment Amount equal to or greater than the Loan Amount and fill other required fields (Loan Amount, select Collateral Account)<br>2. Click "Submit" | Validation error stating the down payment must be less than the loan amount and submission is blocked. | High |
| 7.REQLOA-013 | Request loan denied due to inadequate collateral value | None | 1. Select the desired loan type card<br>2. Fill all required fields (Loan Amount within range, Down Payment meeting minimum and less than Loan Amount, select Collateral Account with insufficient funds relative to required collateral)<br>3. Click "Run Credit Simulation" and then "Submit" | Application is denied with a reason indicating inadequate collateral value. | High |
| 7.REQLOA-014 | Display denial reasons when credit engine denies application | Credit engine denies the application. | 1. Select the desired loan type card<br>2. Fill all required fields with valid values<br>3. Click "Run Credit Simulation" and observe denial<br>4. Click "Submit" or confirm denial outcome | Application is denied and the UI displays specific denial reasons. | High |
| 7.REQLOA-015 | Engine denies loan showing 'Inadequate collateral value' reason | None | 1. Fill all required fields (Loan Amount, Down Payment Amount, Collateral Account) with values where selected collateral value is insufficient<br>2. Click "Simulate Credit Approval" | Loan is denied and the denial reason 'Inadequate collateral value' is displayed. | High |
| 7.REQLOA-016 | Engine denies loan showing 'Insufficient credit history' reason | None | 1. Fill all required fields (Loan Amount, Down Payment Amount, Collateral Account) with values that would trigger a credit-history based denial<br>2. Click "Simulate Credit Approval" | Loan is denied and the denial reason 'Insufficient credit history' is displayed. | High |
| 7.REQLOA-018 | Submit with all required fields empty | None | 1. Leave all required fields empty on the Request Loan form<br>2. Click "Submit" or "Request Loan" | Validation errors shown for all required fields. | Medium |

#### Edge Case Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 7.REQLOA-019 | Loan amount at minimum boundary is accepted | None | 1. Select the desired loan type card<br>2. Fill Loan Amount equal to the type-specific minimum and fill other required fields with valid values<br>3. Click "Run Credit Simulation" | System accepts the minimum loan amount and proceeds to credit simulation or next step. | Medium |
| 7.REQLOA-020 | Confirmation shows exact approval message text | User is authenticated and the Request Loan form is visible. | 1. Fill all required fields (Loan Amount, Down Payment Amount, Collateral Account, Interest Rate)<br>2. Click "Request Loan"<br>3. Verify the on-screen confirmation message text exactly matches the expected approval phrase | The confirmation message exactly matches "Loan approved and created successfully!" | Medium |
| 7.REQLOA-021 | Auto loan rejected when amount is just below minimum | Request Loan form is visible | 1. Select the Auto loan type card<br>2. Fill all required fields (Loan Amount with an amount just below the minimum allowed for the selected loan type)<br>3. Click "Submit" | Validation error shown indicating the Loan Amount is outside the allowed range for the selected loan type. | Medium |
| 7.REQLOA-022 | Denial displays reason and does not debit account balances | None | 1. Fill all required fields with values expected to trigger a denial (credit or collateral)<br>2. Click "Apply" | Loan is denied with a specific denial reason displayed and no account balances are debited as part of the denial process. | Medium |
| 7.REQLOA-023 | Approving a loan does not debit account balances in the mock system | A loan request is in "Pending Approval" status and a collateral account with a visible balance is shown on the same page. | 1. Record the displayed balance for the collateral account on the page<br>2. Click "Approve" and confirm the approval<br>3. Verify the success message is displayed and that the recorded collateral account balance remains unchanged | Success message displayed and the collateral account balance remains the same as before approval; created loan account details are shown. | Medium |
| 7.REQLOA-024 | Loan creation does not debit any account balances in mock system | User is authenticated and account balances for involved accounts are visible on the Request Loan page. | 1. Note the displayed balances for the collateral/source accounts involved<br>2. Fill all required fields (Loan Amount, Down Payment Amount, Collateral Account, Interest Rate)<br>3. Click "Request Loan"<br>4. Verify the displayed balances for those accounts remain unchanged after approval | No account balances are debited as a result of loan creation; balances remain the same as before submission. | Low |
| 7.REQLOA-025 | Verify simulated approval rate approximates configured probability | None | 1. Repeat: Fill required fields (Loan Amount, Down Payment Amount, Collateral Account) with valid values and click "Simulate Credit Approval" across many iterations, recording approval outcomes<br>2. Calculate the percentage of approvals and verify it falls close to the configured probability | Observed approval percentage is approximately 80% within an acceptable tolerance. | Low |
| 7.REQLOA-026 | When credit engine simulation denies, a specific denial reason is shown | None | 1. Fill all required fields with values that would ordinarily meet validations<br>2. Click "Apply" | If the credit engine simulation results in a denial, a specific denial reason (for example, insufficient credit history) is displayed to the user. | Low |

---

### Update Contact Info

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 8.UCI-001 | Updated profile persists after page refresh | User is authenticated and Update Contact Info form is visible | 1. Modify a contact field (e.g., Phone Number) with a valid value<br>2. Click "Update Profile"<br>3. Reload the form/page | The updated value remains visible and the form shows the refreshed data after reload. | High |
| 8.UCI-002 | Update profile with valid contact information | User is authenticated and Update Contact Info form is visible | 1. Modify one or more fields (First Name, Last Name, Street Address, City, State, ZIP Code, Phone Number) with valid values<br>2. Click "Update Profile" | Profile updated successfully and the form displays the refreshed updated data. | High |
| 8.UCI-003 | Form displays pre-filled contact information | User is authenticated and Update Contact Info form is visible | 1. Verify form fields (First Name, Last Name, Street Address, City, State, ZIP Code, Phone Number) are pre-filled with the user's current contact information | Editable form is pre-filled with the user's contact information. | Medium |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 8.UCI-004 | Submit with all required fields empty | User is authenticated and Update Contact Info form is visible | 1. Clear all required fields (First Name, Last Name, Street Address, City, State, ZIP Code, Phone Number)<br>2. Click "Update Profile" | Validation errors shown for all required fields and the profile is not updated. | Medium |
| 8.UCI-005 | Update with invalid ZIP Code format shows inline errors | User is authenticated and Update Contact Info form is visible | 1. Fill all required fields with valid values except enter an invalid ZIP Code format<br>2. Click "Update Profile" | ZIP Code field is highlighted, an inline error banner is displayed, and the profile is not updated. | Medium |
| 8.UCI-006 | Update with invalid phone number format shows inline errors | User is authenticated and Update Contact Info form is visible | 1. Fill all required fields with valid values except enter an invalid phone number format<br>2. Click "Update Profile" | Phone field is highlighted, an inline error banner is displayed, and the profile is not updated. | Medium |

---

### Manage Cards

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 9.MANCAR-001 | Request Debit card successfully | User is logged in and Manage Cards page is open with an eligible account in good standing. | 1. Select Card Type as Debit<br>2. Fill all required fields (Account to Link: select an eligible account, Shipping Address: enter a complete address)<br>3. Click "Request Card" | A card-request ticket is opened and "Card request submitted successfully." message with a tracking ID is displayed. | High |
| 9.MANCAR-002 | Freeze an active card (valid status transition) | An existing card is in "Active" status and selectable. | 1. Select the existing active card<br>2. Fill all required fields (Card Status set to Frozen, optionally update New Spending Limit or leave unchanged)<br>3. Click "Update Controls" | Displays "Card controls updated successfully." and the card status changes to Frozen on the card details. | High |
| 9.MANCAR-003 | Submit valid card request using Credit card type | User is logged in and Manage Cards page is open | 1. Select Card Type as Credit, select a valid Account to Link, and fill a complete Shipping Address<br>2. Click "Request Card" | A card-request ticket is opened and the page shows "Card request submitted successfully." with a tracking ID. | High |
| 9.MANCAR-004 | Update card controls with valid limit, travel notice, and status | An existing card is available and selectable. | 1. Select an existing card<br>2. Fill all required fields (New Spending Limit with a valid amount within policy, Travel Notice with valid start and end dates and destinations, Card Status with an allowed value)<br>3. Click "Update Controls" | Displays "Card controls updated successfully." and the card's spending limit, travel notice, and status reflect the updated values. | High |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 9.MANCAR-005 | Submit when selected account is not in good standing | User is logged in and Manage Cards page is open | 1. Select a valid Card Type, select an Account to Link that is not in good standing, and fill a complete Shipping Address<br>2. Click "Request Card" | Submission is rejected with an error indicating the selected account is not eligible for a card request. | High |
| 9.MANCAR-006 | Reject spending limit above policy | An existing card is available and selectable. | 1. Select an existing card<br>2. Fill all required fields (New Spending Limit set above the allowed policy limit, Card Status with an allowed value)<br>3. Click "Update Controls" | Inline validation error shown for the spending limit and the form remains editable. | Medium |
| 9.MANCAR-007 | Submit with all required fields empty | User is logged in and Manage Cards page is open | 1. Leave all required fields empty<br>2. Click "Request Card" | Validation errors shown for all required fields. | Medium |
| 9.MANCAR-008 | Submit with incomplete shipping address | User is logged in and Manage Cards page is open. | 1. Select a valid Card Type and an eligible Account to Link<br>2. Enter an incomplete Shipping Address (missing required address parts)<br>3. Click "Request Card" | Validation error indicating the address is incomplete and the request is not submitted. | Medium |
| 9.MANCAR-009 | Reject disallowed card-status transition | An existing card is in a status that does not allow the attempted transition and is selectable. | 1. Select the existing card in the disallowed initial status<br>2. Fill all required fields (Card Status set to the disallowed target status, other required fields as needed)<br>3. Click "Update Controls" | Inline validation error shown indicating the status transition is not allowed and the form remains editable. | Medium |
| 9.MANCAR-010 | Reject travel notice with invalid date range | An existing card is available and selectable. | 1. Select an existing card<br>2. Fill all required fields (Travel Notice with an end date earlier than the start date, and other required fields as needed)<br>3. Click "Update Controls" | Inline validation error shown for the travel notice date range and the form remains editable. | Medium |

---

### Investments

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 10.INVEST-001 | Execute a same-day buy trade with valid inputs | User has sufficient buying power and the selected symbol exists. | 1. Fill all required fields (Action = Buy, Fund Symbol selected via autocomplete, Quantity with a positive integer, Funding Account selected)<br>2. Click "Execute Trade" | Trade executed successfully message with an order ID is displayed, the trade is processed same-day and holdings are updated. | High |
| 10.INVEST-002 | Create new investment plan with Weekly frequency | User is authenticated and on the Create Plan page | 1. Fill all required fields (Fund Symbol, Contribution Amount, Frequency set to Weekly, Start Date in the future, Funding Account with adequate balance)<br>2. Click "Create Plan" | Plan created successfully and the new schedule is stored and visible. | High |
| 10.INVEST-008 | Portfolio snapshot displays read-only holdings and values | None | 1. Verify the portfolio snapshot panel is visible<br>2. Confirm the panel shows current fund holdings, market value, and unrealised gain or loss and that the fields are not editable | The portfolio snapshot is read-only and displays current fund holdings, market value, and unrealised gain or loss. | Medium |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 10.INVEST-003 | Attempt buy with insufficient buying power | None | 1. Fill all required fields for a Buy (select Fund Symbol, set Quantity that requires more funds than available in the selected Funding Account, select Funding Account)<br>2. Click "Execute Trade" | Inline validation error indicating insufficient buying power and the trade is not executed. | High |
| 10.INVEST-004 | Attempt sell with insufficient share balance | None | 1. Fill all required fields for a Sell (select Fund Symbol, set Quantity greater than current share balance, select Destination Account)<br>2. Click "Execute Trade" | Inline validation error indicating insufficient share balance and the trade is not executed. | High |
| 10.INVEST-005 | Reject plan when Contribution is below minimum | None | 1. Fill all required fields with Contribution Amount less than the minimum<br>2. Click "Create Plan" | Validation error indicating the contribution does not meet the minimum and Contribution Amount field is highlighted. | High |
| 10.INVEST-006 | Reject plan when Start Date is not in the future | None | 1. Fill all required fields with Start Date set to today or a past date<br>2. Click "Create Plan" | Validation error "Start date must be in the future" shown and Start Date field highlighted. | High |
| 10.INVEST-007 | Reject plan when Funding Account has inadequate balance | Funding account balance is less than the contribution amount | 1. Fill all required fields selecting a Funding Account with insufficient balance<br>2. Click "Create Plan" | Validation error indicating insufficient funds and Funding Account field highlighted. | High |
| 10.INVEST-009 | Submit with Funding Account empty | None | 1. Fill all other required fields, leave Funding Account empty<br>2. Click "Create Plan" | Validation error indicating Funding Account is required. | Medium |
| 10.INVEST-010 | Submit with Contribution Amount empty | None | 1. Fill all other required fields, leave Contribution Amount empty<br>2. Click "Create Plan" | Validation error indicating Contribution Amount is required. | Medium |
| 10.INVEST-011 | Submit with all required fields empty | None | 1. Leave all required fields empty<br>2. Click "Execute Trade" | Validation errors shown inline for all required fields. | Medium |
| 10.INVEST-012 | Attempt trade with non-existent symbol | None | 1. Fill all required fields (select an invalid/non-existent Fund Symbol via the autocomplete, set Action and Quantity, select Funding/Destination Account)<br>2. Click "Execute Trade" | Inline validation error indicating the symbol is not recognized and the trade is not executed. | Medium |
| 10.INVEST-013 | Attempt trade with zero or negative quantity | None | 1. Fill all required fields (Action and Fund Symbol selected, set Quantity to zero or a negative value, select Funding/Destination Account)<br>2. Click "Execute Trade" | Inline validation error indicating quantity must be greater than zero and the trade is not executed. | Medium |

#### Edge Case Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 10.INVEST-014 | Contribution equals minimum creates plan (boundary) | Funding account has sufficient balance and minimum contribution is defined | 1. Fill all required fields with Contribution Amount equal to the minimum and other values valid<br>2. Click "Create Plan" | Plan is created and confirmation message "Plan created successfully." is displayed. | Medium |
| 10.INVEST-015 | Execute trade with minimum allowable quantity (boundary case) | User has at least one share or sufficient buying power as appropriate. | 1. Fill all required fields (Action, Fund Symbol via autocomplete, set Quantity to the minimum allowed value, select Funding/Destination Account)<br>2. Click "Execute Trade" | Trade executes successfully, confirmation with order ID is displayed, and holdings update reflects the trade. | Low |

---

### Account Statements

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 11.ACCSTA-001 | Generate statement for a selected month-and-year | User is logged in and on the Account Statements page. | 1. Select a month-and-year in the Statement Period control<br>2. Select an account from the Account dropdown<br>3. Click "Generate Statement" | Statement generated successfully and transactions for the selected month are displayed or available for download. | High |
| 11.ACCSTA-002 | Generate statement for a valid custom date range | User is logged in and on the Account Statements page. | 1. Select custom Statement Period and enter a valid start date and end date<br>2. Select an account from the Account dropdown<br>3. Click "Generate Statement" | Statement generated successfully and transactions for the selected date range are displayed or available for download. | High |
| 11.ACCSTA-003 | Enable paperless statements with a valid email address | User is signed in and the Account Statements page is open. | 1. Check the paperless statements opt-in checkbox and fill a valid email address in the Email Address field<br>2. Click "Save Preference" | e-Statement preference updated and confirmation displayed; the preference is reflected in the UI (checkbox remains checked and the email is saved). | High |
| 11.ACCSTA-004 | Update existing e-statement email address and save preference | User is signed in, the Account Statements page is open, and paperless statements are already enabled. | 1. Modify the Email Address field with a different valid email address<br>2. Click "Save Preference" | e-Statement preference updated to the new email and confirmation displayed. | High |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 11.ACCSTA-005 | Submit with all required fields empty | User is logged in and on the Account Statements page. | 1. Leave all required fields empty<br>2. Click "Generate Statement" | Validation errors shown for required fields and statement is not generated. | Medium |
| 11.ACCSTA-006 | Save Preference with invalid email format | User is signed in and the Account Statements page is open. | 1. Check the paperless statements opt-in checkbox and fill the Email Address field with an invalid email format<br>2. Click "Save Preference" | Email field is highlighted with guidance indicating invalid email and the preference is not saved. | Medium |
| 11.ACCSTA-007 | Save Preference with all required fields empty | User is signed in and the Account Statements page is open. | 1. Leave all required fields empty<br>2. Click "Save Preference" | Validation errors shown; the email field is highlighted with guidance and the preference is not saved. | Medium |
| 11.ACCSTA-008 | Display error when statement generation fails on server | User is logged in and on the Account Statements page. | 1. Select a valid Statement Period (month-or custom range) and an account<br>2. Click "Generate Statement" | An error message is displayed indicating the statement could not be generated and advising to try again later. | Medium |

---

### Security Settings

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 12.SECSET-001 | Attempt change with incorrect current password | User is signed in and Change Password panel is open. | 1. Fill all required fields (Current Password: incorrect value, New Password: valid strong password, Confirm New Password: same strong password)<br>2. Click "Change Password" button | Error indicating current password verification failed and the Current Password field is highlighted. | High |
| 12.SECSET-002 | Submit with all required fields empty | User is authenticated and Change Password panel is open. | 1. Leave all required fields empty<br>2. Click "Change Password" | Validation errors shown for all required fields. | Medium |

---

### Support Center

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 13.SUPCEN-001 | Submit valid callback request | User is signed in and the Request Callback form is open. | 1. Fill all required fields (select Reason for Call, set Preferred Date to a valid next-business-day-or-later date, select Preferred Time Window, ensure Phone Number contains a valid phone number)<br>2. Click "Request Callback" | Confirmation message "Callback request submitted." is displayed and an email confirmation is sent for the callback request. | High |
| 13.SUPCEN-002 | Send message with a valid attachment | Support Center 'Send Message' form is open. | 1. Fill all required fields (Subject with valid length, Category, Message Body)<br>2. Attach a supported file type<br>3. Click "Send Message" | Displays "Message sent successfully." and shows a ticket ID. | High |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 13.SUPCEN-003 | Submit with Message Body empty | Support Center 'Send Message' form is open. | 1. Fill all other required fields (Subject with valid length, Category), leave Message Body empty<br>2. Click "Send Message" | Inline validation error indicating Message Body is required. | Medium |
| 13.SUPCEN-004 | Submit with all required fields empty | User is signed in and the Request Callback form is open. | 1. Clear the Phone Number field so it is empty<br>2. Leave all required fields empty<br>3. Click "Request Callback" | Validation errors shown for all required fields. | Medium |
| 13.SUPCEN-005 | Request callback with invalid phone number format | Request Callback form is open | 1. Fill all required fields with an invalid format in Phone Number<br>2. Click "Request Callback" | Inline validation error indicating the phone number format is invalid. | Medium |
| 13.SUPCEN-006 | Request callback with Preferred Date before next business day | Request Callback form is open | 1. Fill all required fields with valid values, set Preferred Date to a date earlier than the next business day<br>2. Click "Request Callback" | Inline validation error indicating Preferred Date must be moved to the next business day or later. | Medium |

---

## Navigation Graph

![Navigation Graph](outputs/autospectest/Parabank/openai-gpt-5-mini/navigation_graph.png)

### Pages

| Module | URL | Test Cases |
|--------|-----|------------|
| Login | /login | 12 |
| Register | /register | 24 |
| Accounts Overview | /accounts | 7 |
| Open New Account | /accounts/new | 7 |
| Transfer Funds | /transfer | 12 |
| Payments | /payments | 4 |
| Request Loan | /loans/request | 26 |
| Update Contact Info | /profile/contact | 6 |
| Manage Cards | /cards | 10 |
| Investments | /investments | 15 |
| Account Statements | /statements | 8 |
| Security Settings | /settings/security | 2 |
| Support Center | /support | 6 |
