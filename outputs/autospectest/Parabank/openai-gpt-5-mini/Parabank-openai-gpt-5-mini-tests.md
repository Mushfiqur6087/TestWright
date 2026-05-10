# Test Cases — Parabank

Generated: 2026-05-10T05:29:26.613076Z  
Model: openai/gpt-5-mini  

## Summary

| Modules | Total | Positive | Negative | Edge | High | Medium | Low |
|---------|-------|----------|----------|------|------|--------|-----|
| 13 | 46 | 46 | 0 | 0 | 26 | 19 | 1 |

## Login

Total: **2** (positive: 2, negative: 0, edge: 0)

### Positive Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| TC-001 | Successful sign in with valid credentials | User not signed in, Registered user exists with <valid email address or username> and <valid password> that meets password complexity requirements | 1. Navigate to the Login page<br>2. Enter <valid email address or username> in the Email/Username field<br>3. Enter <valid password> in the Password field<br>4. Click the Sign In button | flashes 'Signed in successfully.' and redirects to Accounts Overview page | high |
| TC-002 | Navigate to Forgot Password page via Forgot Password? link | User not signed in | 1. Navigate to the Login page<br>2. Click the Forgot Password? link | Navigates to Forgot Password page | low |

---

## Register

Total: **5** (positive: 5, negative: 0, edge: 0)

### Positive Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| TC-001 | Successful registration with all required fields completed | Registration page is open | 1. Enter <first name> in the First Name field<br>2. Enter <last name> in the Last Name field<br>3. Enter <street address> in the Street Address field<br>4. Enter <city> in the City field<br>5. Select <state> from the State dropdown<br>6. Enter <ZIP code in 5-digit format> in the ZIP Code field<br>7. Enter <phone number> in the Phone Number field<br>8. Enter <SSN> in the SSN field<br>9. Enter <valid email address> in the Username field<br>10. Enter <password> in the Password field<br>11. Enter <password> in the Confirm Password field<br>12. Click the Register button | Account created successfully — please sign in; redirects to login page | high |
| TC-002 | Phone number input is automatically formatted to (123) 456-7890 | Registration page is open | 1. Enter <phone number> in the Phone Number field<br>2. Move focus away from the Phone Number field | Phone Number field displays the input formatted as (123) 456-7890 (automatic formatting applied) | medium |
| TC-003 | SSN input is automatically formatted to 123-45-6789 | Registration page is open | 1. Enter <SSN> in the SSN field<br>2. Move focus away from the SSN field | SSN field displays the input formatted as 123-45-6789 (automatic formatting applied) | medium |
| TC-004 | ZIP Code field accepts 5+4 format (12345-6789) | Registration page is open | 1. Enter <ZIP code in 5+4 format> in the ZIP Code field<br>2. Move focus away from the ZIP Code field | ZIP Code field accepts and displays the entered 5+4 format (12345-6789) | medium |
| TC-005 | State dropdown allows selecting a US state | Registration page is open | 1. Click the State dropdown<br>2. Select <state> from the State dropdown | State dropdown shows <state> as selected | medium |

---

## Accounts Overview

Total: **2** (positive: 2, negative: 0, edge: 0)

### Positive Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| TC-001 | Accounts Overview displays welcome message, masked account numbers, status badges, ordered rows and total balance | User logged in, At least two customer accounts exist with differing <open date> and <current balance> values | 1. Navigate to the Accounts Overview page | The page displays a welcome message that includes <user name>. The accounts table is visible with columns: Account Number, Account Type, Current Balance, Account Status, and Open Date. Account Number values are masked and show only the last 4 digits (format: ****5001). Account Status shows an 'Active' badge for active accounts. Rows are ordered by Open Date ascending (earliest first). The table footer shows the label "Total Balance" and the displayed total equals the sum of the Current Balance values shown in the table. | high |
| TC-002 | Account Number rendered as clickable element but click action not implemented | User logged in, At least one customer account exists | 1. Navigate to the Accounts Overview page<br>2. Click the Account Number in the first row of the accounts table | The Account Number in the row is rendered as a clickable element (for example, link or button). Clicking the Account Number does not navigate away from the Accounts Overview page or open account details because the click action is not implemented; the Accounts Overview table remains visible. | medium |

---

## Open New Account

Total: **4** (positive: 4, negative: 0, edge: 0)

### Positive Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| TC-001 | Open Checking account with valid initial deposit and sufficient funding | Funding account <funding account with sufficient balance> exists | 1. Navigate to the Open New Account page<br>2. Select the Checking account type card<br>3. Enter <initial deposit amount meeting Checking minimum> in the Initial Deposit Amount field<br>4. Select <funding account with sufficient balance> from the Funding Source Account dropdown<br>5. Click the Open Account button | "Account opened successfully!" is displayed and the user is redirected to Accounts Overview | high |
| TC-002 | Open Savings account with valid initial deposit and sufficient funding | Funding account <funding account with sufficient balance> exists | 1. Navigate to the Open New Account page<br>2. Select the Savings account type card<br>3. Enter <initial deposit amount meeting Savings minimum> in the Initial Deposit Amount field<br>4. Select <funding account with sufficient balance> from the Funding Source Account dropdown<br>5. Click the Open Account button | "Account opened successfully!" is displayed and the user is redirected to Accounts Overview | high |
| TC-003 | Account type selection updates displayed minimum deposit requirement |  | 1. Navigate to the Open New Account page<br>2. Select the Checking account type card<br>3. Select the Savings account type card | The account type card display updates to show the minimum deposit requirement for the selected type (shows $25 for Checking and $100 for Savings) | medium |
| TC-004 | Open Account button becomes enabled when all required fields have valid values | Funding account <funding account with sufficient balance> exists | 1. Navigate to the Open New Account page<br>2. Select an account type<br>3. Enter <initial deposit amount meeting selected account type minimum> in the Initial Deposit Amount field<br>4. Select <funding account with sufficient balance> from the Funding Source Account dropdown | The Open Account button is enabled when Account Type is selected, Initial Deposit Amount is numeric and meets the selected type's minimum, and a funding account with sufficient balance is selected | medium |

---

## Transfer Funds

Total: **3** (positive: 3, negative: 0, edge: 0)

### Positive Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| TC-001 | Internal transfer (My ParaBank Account) happy path | User logged in, <source account> has sufficient funds for <transfer amount>, User has <internal destination account> in their accounts | 1. Navigate to the Transfer page<br>2. Select "My ParaBank Account" in the Transfer Type radio buttons<br>3. Click the Source Account dropdown<br>4. Select <source account> from the Source Account dropdown<br>5. Click the Internal Destination Account dropdown<br>6. Select <internal destination account> from the Internal Destination Account dropdown<br>7. Enter <transfer amount> in the Transfer Amount field<br>8. Click the Submit button | Transfer completed successfully. Returns transaction ID. A transaction ID is displayed on screen. | high |
| TC-002 | External transfer (External Account) happy path with matching account numbers | User logged in, <source account> has sufficient funds for <transfer amount> | 1. Navigate to the Transfer page<br>2. Select "External Account" in the Transfer Type radio buttons<br>3. Click the Source Account dropdown<br>4. Select <source account> from the Source Account dropdown<br>5. Enter <external account number> in the External Account Number field<br>6. Enter <external account number> in the External Account Number Confirmation field<br>7. Enter <transfer amount> in the Transfer Amount field<br>8. Click the Submit button | Transfer completed successfully. Returns transaction ID. A transaction ID is displayed on screen. | high |
| TC-003 | Source Account dropdown is filtered to Checking and Savings accounts | User logged in, User has multiple accounts including accounts of type Checking and Savings | 1. Navigate to the Transfer page<br>2. Click the Source Account dropdown | Source Account dropdown lists only accounts of type Checking or Savings | medium |

---

## Payments

Total: **2** (positive: 2, negative: 0, edge: 0)

### Positive Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| TC-001 | Submit payment with matching account numbers and sufficient funds | Source account with available funds >= <payment amount> | 1. Navigate to the Bill Payment page<br>2. Enter <payee name> in the Payee Name field<br>3. Enter <street address> in the Street Address field<br>4. Enter <city> in the City field<br>5. Enter <state> in the State field<br>6. Enter <zip code> in the ZIP Code field<br>7. Enter <phone number> in the Phone Number field<br>8. Enter <payee account number> in the Payee Account Number field<br>9. Enter <payee account number> in the Confirm Account Number field<br>10. Enter <payment amount> in the Payment Amount field<br>11. Select <source account> from the Source Account dropdown<br>12. Click the Pay button | Payment submitted successfully. Returns reference code and updates balances. A payment reference code is displayed to the user. Source account and payee balances are updated to reflect the deduction and credit of <payment amount> respectively. | high |
| TC-002 | Submit payment where source account funds equal the payment amount (boundary condition) | Source account with available funds equal to <payment amount> | 1. Navigate to the Bill Payment page<br>2. Enter <payee name> in the Payee Name field<br>3. Enter <street address> in the Street Address field<br>4. Enter <city> in the City field<br>5. Enter <state> in the State field<br>6. Enter <zip code> in the ZIP Code field<br>7. Enter <phone number> in the Phone Number field<br>8. Enter <payee account number> in the Payee Account Number field<br>9. Enter <payee account number> in the Confirm Account Number field<br>10. Enter <payment amount> in the Payment Amount field<br>11. Select <source account> from the Source Account dropdown<br>12. Click the Pay button | Payment submitted successfully. Returns reference code and updates balances. A payment reference code is displayed to the user. Source account balance is reduced by <payment amount> (resulting balance may be zero) and the payee's balance is increased by <payment amount>. | high |

---

## Request Loan

Total: **4** (positive: 4, negative: 0, edge: 0)

### Positive Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| TC-001 | Request Personal Loan without Collateral (happy path) | User logged in | 1. Navigate to the Request Loan page<br>2. Select Personal in the Loan Type radio group<br>3. Enter <valid personal loan amount within Personal range> in the Loan Amount field<br>4. Enter <valid down payment amount meeting minimum 10% requirement and less than Loan Amount> in the Down Payment Amount field<br>5. Ensure the Collateral Account dropdown is left unselected<br>6. Click the Request Loan button | Loan approved and created successfully! (no actual balance debits occur)  is displayed and the newly created loan is visible with <loan details> including Loan Type set to Personal and the entered Loan Amount and Down Payment | high |
| TC-002 | Request Auto Loan with Collateral meeting 20% requirement (happy path) | User logged in, <Collateral account with sufficient available funds and collateral value >= 20% of Loan Amount> exists | 1. Navigate to the Request Loan page<br>2. Select Auto in the Loan Type radio group<br>3. Enter <valid auto loan amount within Auto range> in the Loan Amount field<br>4. Enter <valid down payment amount meeting minimum 10% requirement and less than Loan Amount> in the Down Payment Amount field<br>5. Select <collateral account with sufficient available funds and collateral value >= 20% of Loan Amount> from the Collateral Account dropdown<br>6. Click the Request Loan button | Loan approved and created successfully! (no actual balance debits occur)  is displayed and the newly created loan is visible with <loan details> including Loan Type set to Auto and the selected Collateral Account shown | high |
| TC-003 | Request Home Loan without Collateral (happy path) | User logged in | 1. Navigate to the Request Loan page<br>2. Select Home in the Loan Type radio group<br>3. Enter <valid home loan amount within Home range> in the Loan Amount field<br>4. Enter <valid down payment amount meeting minimum 10% requirement and less than Loan Amount> in the Down Payment Amount field<br>5. Ensure the Collateral Account dropdown is left unselected<br>6. Click the Request Loan button | Loan approved and created successfully! (no actual balance debits occur)  is displayed and the newly created loan is visible with <loan details> including Loan Type set to Home and the entered Loan Amount and Down Payment | high |
| TC-004 | Request Home Loan with Collateral meeting 20% requirement (happy path) | User logged in, <Collateral account with sufficient available funds and collateral value >= 20% of Loan Amount> exists | 1. Navigate to the Request Loan page<br>2. Select Home in the Loan Type radio group<br>3. Enter <valid home loan amount within Home range> in the Loan Amount field<br>4. Enter <valid down payment amount meeting minimum 10% requirement and less than Loan Amount> in the Down Payment Amount field<br>5. Select <collateral account with sufficient available funds and collateral value >= 20% of Loan Amount> from the Collateral Account dropdown<br>6. Click the Request Loan button | Loan approved and created successfully! (no actual balance debits occur)  is displayed and the newly created loan is visible with <loan details> including Loan Type set to Home and the selected Collateral Account shown | high |

---

## Update Contact Info

Total: **5** (positive: 5, negative: 0, edge: 0)

### Positive Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| TC-001 | Update all profile fields with valid data and submit | User logged in, Customer profile page open with pre-filled data | 1. Navigate to the Customer Profile page<br>2. Enter <first name> in the First Name field<br>3. Enter <last name> in the Last Name field<br>4. Enter <street address> in the Street Address field<br>5. Enter <city> in the City field<br>6. Select <state> in the State field<br>7. Enter <zip code> in the ZIP Code field<br>8. Enter <phone number> in the Phone Number field<br>9. Click the Update Profile button | Profile updated successfully. Refreshes the data. The form displays the updated values for First Name, Last Name, Street Address, City, State, ZIP Code, and Phone Number and no inline error banner is shown. | high |
| TC-002 | Verify profile form is pre-filled with existing customer data | User logged in | 1. Navigate to the Customer Profile page | All fields (First Name, Last Name, Street Address, City, State, ZIP Code, Phone Number) are pre-filled with the customer's existing values. | medium |
| TC-003 | Submit profile without making changes (pre-filled values) and confirm success | User logged in, Customer profile page open with pre-filled data | 1. Navigate to the Customer Profile page<br>2. Click the Update Profile button | Profile updated successfully. Refreshes the data. The form remains populated with the existing customer values and no inline error banner is shown. | medium |
| TC-004 | Update address fields only and submit successfully | User logged in, Customer profile page open with pre-filled data | 1. Navigate to the Customer Profile page<br>2. Enter <street address> in the Street Address field<br>3. Enter <city> in the City field<br>4. Select <state> in the State field<br>5. Enter <zip code> in the ZIP Code field<br>6. Click the Update Profile button | Profile updated successfully. Refreshes the data. The form displays the updated Street Address, City, State, and ZIP Code values and no inline error banner is shown. | medium |
| TC-005 | Update phone number only and submit successfully | User logged in, Customer profile page open with pre-filled data | 1. Navigate to the Customer Profile page<br>2. Enter <phone number> in the Phone Number field<br>3. Click the Update Profile button | Profile updated successfully. Refreshes the data. The form displays the updated Phone Number and no inline error banner is shown. | medium |

---

## Manage Cards

Total: **4** (positive: 4, negative: 0, edge: 0)

### Positive Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| TC-001 | Submit Card Request with complete address and eligible account | An account in good standing exists | 1. Navigate to the Manage Cards page<br>2. Select <card type> from the Card Type dropdown<br>3. Select <account to link> from the Account to Link field<br>4. Enter <complete shipping address> in the Shipping Address field<br>5. Click the Request Card button | opens card-request ticket and shows 'Card request submitted successfully.' with tracking ID | high |
| TC-002 | Update spending limit within policy for an existing card | An existing card is available | 1. Navigate to the Manage Cards page<br>2. Select <existing card> from the Select Existing Card dropdown<br>3. Enter <new spending limit within policy> in the New Spending Limit field<br>4. Click the Update Controls button | Card controls updated successfully. | medium |
| TC-003 | Add a valid travel notice with start/end dates and destinations | An existing card is available | 1. Navigate to the Manage Cards page<br>2. Select <existing card> from the Select Existing Card dropdown<br>3. Enter <start date> in the Travel Notice Start Date field<br>4. Enter <end date> in the Travel Notice End Date field<br>5. Enter <destinations> in the Travel Notice Destinations field<br>6. Click the Update Controls button | Card controls updated successfully. No inline validation errors for Travel Notice; end date is on or after start date. | medium |
| TC-004 | Change card status and verify resulting status is applied | A card in <current status> status exists | 1. Navigate to the Manage Cards page<br>2. Select <existing card> from the Select Existing Card dropdown<br>3. Select <new status> from the Card Status dropdown<br>4. Click the Update Controls button | Card controls updated successfully. Card Status displays <new status>. | high |

---

## Investments

Total: **4** (positive: 4, negative: 0, edge: 0)

### Positive Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| TC-001 | Execute Buy trade successfully | <Fund Symbol exists>, <funding account with sufficient buying power> | 1. Navigate to the Investments page<br>2. In the Trade Funds form, select Buy from the Action dropdown<br>3. In the Trade Funds form, enter <Fund Symbol> in the Fund Symbol field<br>4. In the Trade Funds form, enter <Quantity> (greater than 0) in the Quantity field<br>5. In the Trade Funds form, select <Funding Account> from the Funding or Destination Account dropdown<br>6. Click the Execute Trade button | executes same-day trade; updates holdings; displays "Trade executed successfully." with order ID | high |
| TC-002 | Execute Sell trade successfully | <Fund Symbol exists>, <account with sufficient share balance of the specified Fund_Symbol> | 1. Navigate to the Investments page<br>2. In the Trade Funds form, select Sell from the Action dropdown<br>3. In the Trade Funds form, enter <Fund Symbol> in the Fund Symbol field<br>4. In the Trade Funds form, enter <Quantity> (greater than 0 and less than or equal to share balance) in the Quantity field<br>5. In the Trade Funds form, select <Destination Account> from the Funding or Destination Account dropdown<br>6. Click the Execute Trade button | executes same-day trade; updates holdings; displays "Trade executed successfully." with order ID | high |
| TC-003 | Create recurring investment plan successfully | <Fund Symbol exists>, <funding account with adequate balance for the first contribution> | 1. Navigate to the Investments page<br>2. In the Recurring Investment Plan form, enter <Fund Symbol> in the Fund Symbol field<br>3. In the Recurring Investment Plan form, enter <Contribution Amount> (meets minimum contribution) in the Contribution Amount field<br>4. In the Recurring Investment Plan form, select Monthly from the Frequency dropdown<br>5. In the Recurring Investment Plan form, enter <Start Date in the future> in the Start Date field<br>6. In the Recurring Investment Plan form, select <Funding Account> from the Funding Account dropdown<br>7. Click the Create Plan button | stores schedule; displays "Plan created successfully." | high |
| TC-004 | Investments workspace shows portfolio snapshot and both forms | <portfolio with holdings> | 1. Navigate to the Investments page<br>2. Verify the portfolio snapshot panel is visible<br>3. Verify the portfolio snapshot displays current fund holdings<br>4. Verify the portfolio snapshot displays market value<br>5. Verify the portfolio snapshot displays unrealised gain or loss<br>6. Verify the Trade Funds form is visible<br>7. Verify the Trade Funds form contains Action, Fund Symbol, Quantity, Funding or Destination Account fields and an Execute Trade button<br>8. Verify the Recurring Investment Plan form is visible<br>9. Verify the Recurring Investment Plan form contains Fund Symbol, Contribution Amount, Frequency, Start Date, Funding Account fields and a Create Plan button | Portfolio snapshot is visible and shows current fund holdings, market value, and unrealised gain or loss; Trade Funds form and Recurring Investment Plan form are visible with their respective fields and buttons | medium |

---

## Account Statements

Total: **5** (positive: 5, negative: 0, edge: 0)

### Positive Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| TC-001 | Generate statement using Custom Date Range | User on the Statements page | 1. Select "Custom Date Range" for the Statement Period<br>2. Enter <start date> in the Start Date field<br>3. Enter <end date> in the End Date field<br>4. Select <account> from the Account dropdown<br>5. Click the Generate Statement button | retrieves relevant transactions and displays "Statement generated successfully." | high |
| TC-002 | Generate statement using Month-and-Year selection | User on the Statements page | 1. Select "Month-and-Year" for the Statement Period<br>2. Select <account> from the Account dropdown<br>3. Click the Generate Statement button | retrieves relevant transactions and displays "Statement generated successfully." | high |
| TC-003 | Save e-Statement preference with paperless opt-in | User on the Statements page | 1. Click the Paperless_Opt_In checkbox to opt in to paperless statements<br>2. Enter <email address> in the Email Address field<br>3. Click the Save Preference button | displays "e-Statement preference updated." | high |
| TC-004 | Verify both forms are visible side by side on the Statements page | User on the Statements page | 1. Navigate to the Statements page<br>2. Observe that the Statement Period radio and the Generate Statement button are visible<br>3. Observe that the Account dropdown is visible<br>4. Observe that the Paperless_Opt_In checkbox, Email Address field, and Save Preference button are visible | Both forms are visible side by side: Statement Period, Account, Generate Statement; Paperless_Opt_In, Email Address, Save Preference are present. | medium |
| TC-005 | End-to-end: generate statement then update e-Statement preference | User on the Statements page | 1. Select "Custom Date Range" for the Statement Period<br>2. Enter <start date> in the Start Date field<br>3. Enter <end date> in the End Date field<br>4. Select <account> from the Account dropdown<br>5. Click the Generate Statement button<br>6. Click the Paperless_Opt_In checkbox to opt in to paperless statements<br>7. Enter <email address> in the Email Address field<br>8. Click the Save Preference button | retrieves relevant transactions and displays "Statement generated successfully." Then displays "e-Statement preference updated." | high |

---

## Security Settings

Total: **2** (positive: 2, negative: 0, edge: 0)

### Positive Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| TC-001 | Change password happy path | User logged in, User's current password is <current password> | 1. Navigate to the Security Settings page<br>2. Click the Toggle Panel control on the Change Password panel to expand it<br>3. Enter <current password> in the Current Password field<br>4. Enter <strong password> in the New Password field<br>5. Enter <strong password> in the Confirm New Password field<br>6. Click the Change Password button | Credentials are updated and the success message "Password changed successfully." is displayed. | high |
| TC-002 | Change Password panel expand and collapse | User logged in | 1. Navigate to the Security Settings page<br>2. Click the Toggle Panel control on the Change Password panel to expand it<br>3. Verify the Change Password form is visible and shows fields Current Password, New Password, Confirm New Password<br>4. Click the Toggle Panel control on the Change Password panel to collapse it<br>5. Verify the Change Password form is hidden | The Change Password panel expands to reveal the form with fields Current Password, New Password, Confirm New Password, and collapses to hide the form when toggled. | medium |

---

## Support Center

Total: **4** (positive: 4, negative: 0, edge: 0)

### Positive Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| TC-001 | Send secure message with subject, category, rich-text body and valid attachment | User logged in | 1. Navigate to the Support Center page<br>2. Enter <subject> in the Subject field<br>3. Select <Category> from the Category dropdown<br>4. Enter <message body> in the Message Body field<br>5. Upload <valid attachment file> to the Attachment field<br>6. Click the Send Message button | Message sent successfully. Returns ticket ID. | high |
| TC-002 | Request callback with preferred date at least next business day | User logged in | 1. Navigate to the Support Center page<br>2. Enter <preferred date at least next business day> in the Preferred Date field<br>3. Enter <preferred time window> in the Preferred Time Window field<br>4. Click the Request Callback button | Callback request submitted. Sends email confirmation. | high |
| TC-003 | Phone Number field is pre-filled from user profile in Schedule Callback form | User logged in | 1. Navigate to the Support Center page<br>2. Observe the Phone Number field in the Schedule Callback form | Phone Number field is pre-filled with <phone number from user profile>. | medium |
| TC-004 | Category dropdown displays all expected options | User logged in | 1. Navigate to the Support Center page<br>2. Open the Category dropdown in the Secure Message form | Category dropdown displays the options Account, Technical, Security, and Other. | medium |

---
