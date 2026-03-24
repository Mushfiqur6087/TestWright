# My Website (ParaBank Clone) Test Cases

**Application Type:** React/TypeScript Banking Application
**Test Suite Version:** 1.0

---

## Table of Contents
1. [Login](#1-login)
2. [Registration](#2-registration)
3. [Accounts Overview](#3-accounts-overview)
4. [Open New Account](#4-open-new-account)
5. [Transfer Funds](#5-transfer-funds)
6. [Bill Pay](#6-bill-pay)
7. [Request Loan](#7-request-loan)
8. [Update Contact Info](#8-update-contact-info)
9. [Manage Cards](#9-manage-cards)
10. [Investments](#10-investments)
11. [Account Statements](#11-account-statements)
12. [Security Settings](#12-security-settings)
13. [Support Center](#13-support-center)

---

## Test Credentials

| Field | Value |
|-------|-------|
| Email | admin@parabank.com |
| Username | admin |
| Password | Admin123!@# |

### Mock Account Data

| Account | Type | Balance | Status |
|---------|------|---------|--------|
| ****5001 | Checking | $5,847.52 | Active |
| ****5002 | Savings | $25,678.90 | Active |
| ****5003 | Credit Card | -$1,534.67 | Active |
| ****5004 | Loan | -$45,000.00 | Active |

---

## 1. Login

### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MW-LOGIN-001 | Valid login with email | Registered user exists | 1. Navigate to login page<br>2. Enter valid email (admin@parabank.com)<br>3. Enter valid password (Admin123!@#)<br>4. Click "Sign In" | Flash message "Signed in successfully." displayed, redirected to Accounts Overview | High |
| MW-LOGIN-002 | Valid login with username | Registered user exists | 1. Enter username instead of email<br>2. Enter valid password<br>3. Click "Sign In" | User logged in successfully | High |
| MW-LOGIN-003 | Login page elements | None | 1. Navigate to login page | Email/Username field, Password field, Sign In button, Register link, Forgot Password? link visible | Medium |

### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MW-LOGIN-004 | Invalid email format | None | 1. Enter invalid email format (no @)<br>2. Try to submit | Validation error: invalid email format | High |
| MW-LOGIN-005 | Incorrect password | Registered user exists | 1. Enter valid email<br>2. Enter incorrect password<br>3. Click "Sign In" | Error: "Incorrect email or password. Please try again.", password field cleared | High |
| MW-LOGIN-006 | Unregistered email | None | 1. Enter non-existent email<br>2. Enter any password<br>3. Click "Sign In" | Error message displayed | High |
| MW-LOGIN-007 | Empty email | None | 1. Leave email empty<br>2. Enter password<br>3. Click "Sign In" | Validation error for email field | High |
| MW-LOGIN-008 | Empty password | None | 1. Enter email<br>2. Leave password empty<br>3. Click "Sign In" | Validation error for password field | High |
| MW-LOGIN-009 | Password less than 8 chars | None | 1. Enter valid email<br>2. Enter password < 8 characters<br>3. Click "Sign In" | Validation error: password must be at least 8 characters | High |
| MW-LOGIN-010 | Password without uppercase | None | 1. Enter password without uppercase letter | Validation error: password must contain uppercase | Medium |
| MW-LOGIN-011 | Password without lowercase | None | 1. Enter password without lowercase letter | Validation error: password must contain lowercase | Medium |
| MW-LOGIN-012 | Password without number | None | 1. Enter password without number | Validation error: password must contain number | Medium |
| MW-LOGIN-013 | Password without special char | None | 1. Enter password without special character | Validation error: password must contain special character | Medium |

### UI/UX Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MW-LOGIN-014 | Password masking | None | 1. Enter text in password field | Characters are masked | High |
| MW-LOGIN-015 | Success flash message | Valid login | 1. Login successfully | "Signed in successfully." message displayed briefly | Medium |
| MW-LOGIN-016 | Password cleared on error | Invalid login attempt | 1. Submit invalid credentials | Password field cleared, email remains | Medium |

---

## 2. Registration

### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MW-REG-001 | Successful registration | None | 1. Navigate to Register page<br>2. Fill all fields with valid data<br>3. Click "Register" | "Account created successfully — please sign in." message, redirected to login | High |
| MW-REG-002 | All form fields displayed | None | 1. Navigate to Register | Fields: First Name, Last Name, Street Address, City, State (dropdown), ZIP Code, Phone Number, SSN, Username (email), Password, Confirm Password | Medium |
| MW-REG-003 | State dropdown | None | 1. Click State dropdown | All US states displayed | Medium |
| MW-REG-004 | Phone auto-formatting | None | 1. Enter phone digits: 5551234567 | Auto-formatted to (555) 123-4567 | High |
| MW-REG-005 | SSN auto-formatting | None | 1. Enter SSN digits: 123456789 | Auto-formatted to 123-45-6789 | High |

### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MW-REG-006 | First Name empty | None | 1. Leave First Name empty<br>2. Fill other fields<br>3. Submit | Validation error on First Name | High |
| MW-REG-007 | Last Name empty | None | 1. Leave Last Name empty<br>2. Submit | Validation error on Last Name | High |
| MW-REG-008 | Street Address empty | None | 1. Leave Street Address empty<br>2. Submit | Validation error on Street Address | High |
| MW-REG-009 | City empty | None | 1. Leave City empty<br>2. Submit | Validation error on City | High |
| MW-REG-010 | State not selected | None | 1. Don't select State<br>2. Submit | Validation error on State | High |
| MW-REG-011 | ZIP Code empty | None | 1. Leave ZIP Code empty<br>2. Submit | Validation error on ZIP Code | High |
| MW-REG-012 | Invalid ZIP format | None | 1. Enter ZIP: 1234 (4 digits)<br>2. Submit | Validation error: must be 5 digits or 5+4 format | High |
| MW-REG-013 | Valid 5+4 ZIP | None | 1. Enter ZIP: 12345-6789<br>2. Submit | Accepted | Medium |
| MW-REG-014 | Phone Number empty | None | 1. Leave Phone empty<br>2. Submit | Validation error on Phone | High |
| MW-REG-015 | Invalid Phone format | None | 1. Enter partial phone: 555123<br>2. Submit | Validation error: must be (123) 456-7890 format | High |
| MW-REG-016 | SSN empty | None | 1. Leave SSN empty<br>2. Submit | Validation error on SSN | High |
| MW-REG-017 | Invalid SSN format | None | 1. Enter partial SSN: 12345<br>2. Submit | Validation error: must be 123-45-6789 format | High |
| MW-REG-018 | Username not email format | None | 1. Enter username without @ symbol<br>2. Submit | Validation error: must be valid email format | High |
| MW-REG-019 | Password less than 8 chars | None | 1. Enter password < 8 characters<br>2. Submit | Validation error on password | High |
| MW-REG-020 | Password mismatch | None | 1. Enter different values for Password and Confirm Password<br>2. Submit | Validation error: passwords must match | High |
| MW-REG-021 | Confirm Password empty | None | 1. Leave Confirm Password empty<br>2. Submit | Validation error on Confirm Password | High |
| MW-REG-022 | All fields empty | None | 1. Submit empty form | Field-level errors displayed for all required fields | Medium |

### Boundary Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MW-REG-023 | Minimum valid inputs | None | 1. Enter minimum valid data for all fields<br>2. Submit | Registration succeeds | Medium |
| MW-REG-024 | Maximum length inputs | None | 1. Enter very long strings<br>2. Submit | System handles gracefully | Low |

---

## 3. Accounts Overview

### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MW-AO-001 | Welcome message displayed | User logged in | 1. View Accounts Overview | "Welcome, [First Name]" message displayed | High |
| MW-AO-002 | All accounts listed | User logged in | 1. View accounts table | All accounts shown: Account Number, Type, Balance, Status, Open Date | High |
| MW-AO-003 | Account number masking | User logged in | 1. View account numbers | Only last 4 digits shown (****5001) | High |
| MW-AO-004 | Total balance calculation | User logged in | 1. View total row | Total = sum of all account balances | High |
| MW-AO-005 | Accounts ordered by date | User logged in | 1. View accounts table | Ordered by Open Date (earliest first) | Medium |
| MW-AO-006 | Active status badge | User logged in | 1. View Status column | "Active" badge displayed for active accounts | Medium |

### UI/UX Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MW-AO-007 | Table column headers | User logged in | 1. View table | Headers: Account Number, Account Type, Current Balance, Account Status, Open Date | Medium |
| MW-AO-008 | Currency formatting | User logged in | 1. View balances | Formatted as $X,XXX.XX with proper comma separation | Medium |
| MW-AO-009 | Negative balance display | User has loan/credit | 1. View loan/credit account | Negative balance shown correctly (e.g., -$1,534.67) | Medium |
| MW-AO-010 | Navigation menu highlight | User logged in | 1. View left menu | "Accounts Overview" highlighted | Low |

---

## 4. Open New Account

### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MW-ONA-001 | Open Checking account | User logged in, sufficient funds | 1. Navigate to Open New Account<br>2. Select Checking card<br>3. Enter deposit >= $25<br>4. Select funding account<br>5. Click "Open Account" | "Account opened successfully!" message, redirect to overview | High |
| MW-ONA-002 | Open Savings account | User logged in, sufficient funds | 1. Select Savings card<br>2. Enter deposit >= $100<br>3. Select funding account<br>4. Click "Open Account" | Account opened successfully | High |
| MW-ONA-003 | Interactive account type cards | User logged in | 1. View account type selection | Cards show features and minimum deposit requirements | Medium |
| MW-ONA-004 | Real-time validation | User logged in | 1. Enter invalid deposit amount | Immediate validation error displayed | High |

### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MW-ONA-005 | No account type selected | User logged in | 1. Don't select account type<br>2. Try to submit | Validation error: account type required | High |
| MW-ONA-006 | Checking deposit < $25 | User logged in | 1. Select Checking<br>2. Enter $20<br>3. Submit | Validation error: minimum $25 required | High |
| MW-ONA-007 | Savings deposit < $100 | User logged in | 1. Select Savings<br>2. Enter $50<br>3. Submit | Validation error: minimum $100 required | High |
| MW-ONA-008 | Non-numeric deposit | User logged in | 1. Enter "abc" as deposit<br>2. Submit | Validation error: must be numeric | High |
| MW-ONA-009 | Insufficient funding balance | User logged in | 1. Enter deposit > funding account balance<br>2. Submit | Validation error: insufficient funds in funding account | High |
| MW-ONA-010 | No funding account selected | User logged in | 1. Don't select funding account<br>2. Submit | Validation error: funding account required | High |

### Boundary Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MW-ONA-011 | Exact minimum Checking ($25) | User logged in | 1. Select Checking<br>2. Enter exactly $25<br>3. Submit | Account opens successfully | Medium |
| MW-ONA-012 | Exact minimum Savings ($100) | User logged in | 1. Select Savings<br>2. Enter exactly $100<br>3. Submit | Account opens successfully | Medium |
| MW-ONA-013 | Just below minimum | User logged in | 1. Select Checking<br>2. Enter $24.99 | Validation error | Medium |

---

## 5. Transfer Funds

### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MW-TF-001 | Internal transfer | User logged in, multiple accounts | 1. Select "My ParaBank Account"<br>2. Enter amount<br>3. Select source account<br>4. Select destination account<br>5. Submit | "Transfer completed successfully." with transaction ID | High |
| MW-TF-002 | External transfer | User logged in | 1. Select "External Account"<br>2. Enter amount<br>3. Select source account<br>4. Enter and confirm external account number<br>5. Submit | "Transfer completed successfully." with transaction ID | High |
| MW-TF-003 | Source account filter | User logged in | 1. View source dropdown | Only Checking and Savings accounts shown | High |
| MW-TF-004 | Transfer type toggle | User logged in | 1. Select Internal<br>2. Select External | Destination options change appropriately | Medium |

### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MW-TF-005 | Empty amount | User logged in | 1. Leave amount empty<br>2. Submit | Validation error | High |
| MW-TF-006 | Zero amount | User logged in | 1. Enter $0<br>2. Submit | Validation error | High |
| MW-TF-007 | Negative amount | User logged in | 1. Enter -$100<br>2. Submit | Validation error | High |
| MW-TF-008 | Insufficient funds | User logged in | 1. Enter amount > source balance<br>2. Submit | Error: "Insufficient funds" | High |
| MW-TF-009 | Same source and destination | User logged in | 1. Select same account for source and destination<br>2. Submit | Error or prevented | High |
| MW-TF-010 | External account mismatch | User logged in | 1. Select External<br>2. Enter different account numbers<br>3. Submit | Error: "Account numbers do not match" | High |
| MW-TF-011 | No source selected | User logged in | 1. Don't select source account<br>2. Submit | Validation error | High |
| MW-TF-012 | No destination selected | Internal transfer | 1. Don't select destination<br>2. Submit | Validation error | High |

### Boundary Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MW-TF-013 | Transfer exact balance | User logged in | 1. Enter exact source balance<br>2. Submit | Transfer succeeds, source balance = $0 | Medium |
| MW-TF-014 | Minimum transfer ($0.01) | User logged in | 1. Enter $0.01<br>2. Submit | Transfer succeeds or minimum amount error | Low |

---

## 6. Bill Pay

### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MW-BP-001 | Successful bill payment | User logged in, sufficient funds | 1. Fill all fields: Payee Name, Address, City, State, ZIP, Phone, Account Number, Confirm Account, Amount<br>2. Select source account<br>3. Click "Pay" | "Payment submitted successfully." with reference code | High |
| MW-BP-002 | Quick select payee | User logged in | 1. Select from quick payees (Electric Company, Gas Utility, Internet Provider) | Payee fields auto-populated | High |
| MW-BP-003 | Balance updated | MW-BP-001 completed | 1. View Accounts Overview | Source account balance reduced | High |

### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MW-BP-004 | Payee Name empty | User logged in | 1. Leave Payee Name empty<br>2. Submit | Validation error | High |
| MW-BP-005 | Street Address empty | User logged in | 1. Leave Address empty<br>2. Submit | Validation error | High |
| MW-BP-006 | City empty | User logged in | 1. Leave City empty<br>2. Submit | Validation error | High |
| MW-BP-007 | State empty | User logged in | 1. Leave State empty<br>2. Submit | Validation error | High |
| MW-BP-008 | ZIP Code empty | User logged in | 1. Leave ZIP empty<br>2. Submit | Validation error | High |
| MW-BP-009 | Phone empty | User logged in | 1. Leave Phone empty<br>2. Submit | Validation error | High |
| MW-BP-010 | Account Number empty | User logged in | 1. Leave Account Number empty<br>2. Submit | Validation error | High |
| MW-BP-011 | Confirm Account empty | User logged in | 1. Leave Confirm Account empty<br>2. Submit | Validation error | High |
| MW-BP-012 | Account numbers mismatch | User logged in | 1. Enter different account numbers<br>2. Submit | Error: "Account numbers do not match" | High |
| MW-BP-013 | Amount empty | User logged in | 1. Leave Amount empty<br>2. Submit | Validation error | High |
| MW-BP-014 | Insufficient funds | User logged in | 1. Enter amount > source balance<br>2. Submit | Error: "Insufficient funds" | High |
| MW-BP-015 | No source account | User logged in | 1. Don't select source<br>2. Submit | Validation error | High |

---

## 7. Request Loan

### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MW-RL-001 | Personal loan approved | User logged in, sufficient collateral | 1. Select Personal Loan card<br>2. Enter amount $1,000-$50,000<br>3. Enter down payment (>= 10% of loan)<br>4. Select collateral account<br>5. Click submit | "Loan approved and created successfully!" with account details | High |
| MW-RL-002 | Auto loan approved | User logged in, sufficient collateral | 1. Select Auto Loan<br>2. Enter amount $5,000-$75,000<br>3. Enter down payment<br>4. Select collateral<br>5. Submit | Loan approved | High |
| MW-RL-003 | Home loan approved | User logged in, sufficient collateral | 1. Select Home Loan<br>2. Enter amount $50,000-$500,000<br>3. Enter down payment<br>4. Select collateral<br>5. Submit | Loan approved | High |
| MW-RL-004 | Loan type cards | User logged in | 1. View loan selection | Cards show: Personal (7.5% APR), Auto (4.5% APR), Home (3.5% APR) with ranges | Medium |

### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MW-RL-005 | Personal loan below minimum | User logged in | 1. Select Personal<br>2. Enter $500 (below $1,000 min)<br>3. Submit | Validation error: minimum $1,000 | High |
| MW-RL-006 | Personal loan above maximum | User logged in | 1. Select Personal<br>2. Enter $60,000 (above $50,000 max)<br>3. Submit | Validation error: maximum $50,000 | High |
| MW-RL-007 | Auto loan below minimum | User logged in | 1. Select Auto<br>2. Enter $3,000<br>3. Submit | Validation error: minimum $5,000 | High |
| MW-RL-008 | Auto loan above maximum | User logged in | 1. Select Auto<br>2. Enter $80,000<br>3. Submit | Validation error: maximum $75,000 | High |
| MW-RL-009 | Home loan below minimum | User logged in | 1. Select Home<br>2. Enter $40,000<br>3. Submit | Validation error: minimum $50,000 | High |
| MW-RL-010 | Home loan above maximum | User logged in | 1. Select Home<br>2. Enter $600,000<br>3. Submit | Validation error: maximum $500,000 | High |
| MW-RL-011 | Down payment >= loan | User logged in | 1. Enter down payment equal to or greater than loan amount<br>2. Submit | Validation error: down payment must be less than loan | High |
| MW-RL-012 | Insufficient collateral (< 20%) | User logged in | 1. Enter loan where collateral account < 20% of loan<br>2. Submit | Denial: "Inadequate collateral value" | High |
| MW-RL-013 | Down payment < 10% | User logged in | 1. Enter down payment < 10% of loan<br>2. Submit | Denial or validation error | High |
| MW-RL-014 | No loan type selected | User logged in | 1. Don't select loan type<br>2. Submit | Validation error | High |
| MW-RL-015 | No collateral account | User logged in | 1. Don't select collateral<br>2. Submit | Validation error | High |

### Boundary Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MW-RL-016 | Exact minimum Personal ($1,000) | User logged in | 1. Enter exactly $1,000<br>2. Valid down payment<br>3. Submit | Loan processed | Medium |
| MW-RL-017 | Exact maximum Personal ($50,000) | User logged in | 1. Enter exactly $50,000<br>2. Valid down payment<br>3. Submit | Loan processed | Medium |
| MW-RL-018 | Exactly 10% down payment | User logged in | 1. Enter loan amount<br>2. Enter exactly 10% as down payment<br>3. Submit | Loan processed | Medium |

---

## 8. Update Contact Info

### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MW-UCI-001 | Pre-populated form | User logged in | 1. Navigate to Update Contact Info | All fields pre-filled with current user data | High |
| MW-UCI-002 | Successful update | User logged in | 1. Modify any field<br>2. Click "Update Profile" | "Profile updated successfully." message, data refreshed | High |
| MW-UCI-003 | Update First Name | User logged in | 1. Change First Name<br>2. Submit | Updated successfully | Medium |
| MW-UCI-004 | Update Last Name | User logged in | 1. Change Last Name<br>2. Submit | Updated successfully | Medium |
| MW-UCI-005 | Update Address | User logged in | 1. Change Street Address<br>2. Submit | Updated successfully | Medium |
| MW-UCI-006 | Update City | User logged in | 1. Change City<br>2. Submit | Updated successfully | Medium |
| MW-UCI-007 | Update State | User logged in | 1. Change State<br>2. Submit | Updated successfully | Medium |
| MW-UCI-008 | Update ZIP Code | User logged in | 1. Change ZIP Code<br>2. Submit | Updated successfully | Medium |
| MW-UCI-009 | Update Phone | User logged in | 1. Change Phone Number<br>2. Submit | Updated successfully | Medium |

### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MW-UCI-010 | First Name empty | User logged in | 1. Clear First Name<br>2. Submit | Validation error, error banner displayed | High |
| MW-UCI-011 | Last Name empty | User logged in | 1. Clear Last Name<br>2. Submit | Validation error | High |
| MW-UCI-012 | Address empty | User logged in | 1. Clear Street Address<br>2. Submit | Validation error | High |
| MW-UCI-013 | City empty | User logged in | 1. Clear City<br>2. Submit | Validation error | High |
| MW-UCI-014 | State empty | User logged in | 1. Clear State<br>2. Submit | Validation error | High |
| MW-UCI-015 | ZIP Code empty | User logged in | 1. Clear ZIP Code<br>2. Submit | Validation error | High |
| MW-UCI-016 | Phone empty | User logged in | 1. Clear Phone Number<br>2. Submit | Validation error | High |
| MW-UCI-017 | Invalid ZIP format | User logged in | 1. Enter invalid ZIP<br>2. Submit | Validation error | High |
| MW-UCI-018 | Invalid Phone format | User logged in | 1. Enter invalid phone<br>2. Submit | Validation error | High |

---

## 9. Manage Cards

### Card Request Form Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MW-MC-001 | Request Debit card | User logged in | 1. Select Card Type: Debit<br>2. Select account to link<br>3. Enter complete shipping address<br>4. Click "Request Card" | "Card request submitted successfully." with tracking ID | High |
| MW-MC-002 | Request Credit card | User logged in | 1. Select Card Type: Credit<br>2. Select account<br>3. Enter address<br>4. Submit | Card request submitted | High |
| MW-MC-003 | Incomplete address | User logged in | 1. Leave shipping address incomplete<br>2. Submit | Validation error: address required | High |
| MW-MC-004 | No account selected | User logged in | 1. Don't select account to link<br>2. Submit | Validation error | High |

### Card Controls Form Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MW-MC-005 | Update spending limit | Existing card | 1. Select existing card<br>2. Enter new spending limit<br>3. Click "Update Controls" | "Card controls updated successfully." | High |
| MW-MC-006 | Add travel notice | Existing card | 1. Select card<br>2. Enter travel dates and destination<br>3. Submit | Controls updated | Medium |
| MW-MC-007 | Freeze card | Existing card, Active | 1. Select card<br>2. Change status to Frozen<br>3. Submit | Card frozen successfully | High |
| MW-MC-008 | Unfreeze card | Existing card, Frozen | 1. Select frozen card<br>2. Change status to Active<br>3. Submit | Card activated | High |
| MW-MC-009 | Invalid spending limit | Existing card | 1. Enter limit above policy maximum<br>2. Submit | Validation error displayed inline | High |
| MW-MC-010 | Invalid date range | Existing card | 1. Enter end date before start date<br>2. Submit | Validation error | Medium |

---

## 10. Investments

### Portfolio Snapshot Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MW-INV-001 | View portfolio snapshot | User logged in | 1. Navigate to Investments | Read-only panel shows fund holdings, market value, unrealized gain/loss | High |

### Trade Funds Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MW-INV-002 | Buy funds | User logged in, sufficient funds | 1. Select Action: Buy<br>2. Enter/select Fund Symbol<br>3. Enter Quantity > 0<br>4. Select Funding Account<br>5. Click "Execute Trade" | "Trade executed successfully." with order ID | High |
| MW-INV-003 | Sell funds | User logged in, has shares | 1. Select Action: Sell<br>2. Enter Fund Symbol<br>3. Enter Quantity <= shares owned<br>4. Select Destination Account<br>5. Submit | Trade executed successfully | High |
| MW-INV-004 | Fund symbol autocomplete | User logged in | 1. Start typing fund symbol | Autocomplete suggestions appear | Medium |
| MW-INV-005 | Invalid fund symbol | User logged in | 1. Enter non-existent symbol<br>2. Submit | Validation error: symbol not found | High |
| MW-INV-006 | Zero quantity | User logged in | 1. Enter 0 as quantity<br>2. Submit | Validation error: quantity must be > 0 | High |
| MW-INV-007 | Insufficient buying power | User logged in | 1. Try to buy more than account allows<br>2. Submit | Validation error: insufficient funds | High |
| MW-INV-008 | Sell more than owned | User logged in | 1. Try to sell more shares than owned<br>2. Submit | Validation error: insufficient shares | High |

### Recurring Investment Plan Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MW-INV-009 | Create weekly plan | User logged in | 1. Enter Fund Symbol<br>2. Enter Contribution Amount<br>3. Select Frequency: Weekly<br>4. Enter future Start Date<br>5. Select Funding Account<br>6. Click "Create Plan" | "Plan created successfully." | High |
| MW-INV-010 | Create monthly plan | User logged in | 1. Enter all fields<br>2. Select Monthly<br>3. Submit | Plan created | High |
| MW-INV-011 | Past start date | User logged in | 1. Enter start date in the past<br>2. Submit | Validation error: "Start date must be in the future" | High |
| MW-INV-012 | Below minimum contribution | User logged in | 1. Enter contribution below minimum<br>2. Submit | Validation error | High |
| MW-INV-013 | Insufficient funding balance | User logged in | 1. Select account with low balance<br>2. Submit | Validation error: inadequate balance | High |

---

## 11. Account Statements

### Generate Statement Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MW-AS-001 | Generate monthly statement | User logged in | 1. Select month-and-year period<br>2. Select account<br>3. Click "Generate Statement" | "Statement generated successfully." | High |
| MW-AS-002 | Generate custom date range | User logged in | 1. Select custom date range<br>2. Enter start and end dates<br>3. Select account<br>4. Submit | Statement generated | High |
| MW-AS-003 | Invalid date range | User logged in | 1. Enter end date before start date<br>2. Submit | Validation error | High |
| MW-AS-004 | No account selected | User logged in | 1. Don't select account<br>2. Submit | Validation error | High |
| MW-AS-005 | Generation failure | User logged in | 1. Trigger generation error (server issue) | "Unable to generate statement — please try again later." | Medium |

### E-Statement Preference Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MW-AS-006 | Opt-in to paperless | User logged in | 1. Check paperless checkbox<br>2. Enter email<br>3. Click "Save Preference" | "e-Statement preference updated." | High |
| MW-AS-007 | Opt-out of paperless | Previously opted-in | 1. Uncheck paperless checkbox<br>2. Submit | Preference updated | High |
| MW-AS-008 | Invalid email | User logged in | 1. Enter invalid email<br>2. Submit | Validation error, email field highlighted | High |
| MW-AS-009 | Empty email with opt-in | User logged in | 1. Check paperless<br>2. Leave email empty<br>3. Submit | Validation error | High |

---

## 12. Security Settings

### Change Password Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MW-SS-001 | Successful password change | User logged in | 1. Enter current password<br>2. Enter new password meeting requirements<br>3. Confirm new password<br>4. Click "Change Password" | "Password changed successfully." | High |
| MW-SS-002 | Incorrect current password | User logged in | 1. Enter wrong current password<br>2. Enter new password<br>3. Submit | Validation error: current password incorrect | High |
| MW-SS-003 | New password too short | User logged in | 1. Enter correct current<br>2. Enter new password < 8 chars<br>3. Submit | Validation error: password policy | High |
| MW-SS-004 | New password missing uppercase | User logged in | 1. Enter new password without uppercase<br>2. Submit | Validation error | High |
| MW-SS-005 | New password missing lowercase | User logged in | 1. Enter new password without lowercase<br>2. Submit | Validation error | High |
| MW-SS-006 | New password missing number | User logged in | 1. Enter new password without number<br>2. Submit | Validation error | High |
| MW-SS-007 | New password missing special char | User logged in | 1. Enter new password without special char<br>2. Submit | Validation error | High |
| MW-SS-008 | Passwords don't match | User logged in | 1. Enter different values for new and confirm<br>2. Submit | Validation error: passwords must match | High |
| MW-SS-009 | Collapsible panel | User logged in | 1. Click panel header | Panel collapses/expands | Low |

---

## 13. Support Center

### Secure Message Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MW-SC-001 | Send message successfully | User logged in | 1. Enter Subject<br>2. Select Category<br>3. Enter Message Body<br>4. Click "Send Message" | "Message sent successfully." with ticket ID | High |
| MW-SC-002 | Send with attachment | User logged in | 1. Fill required fields<br>2. Attach valid file<br>3. Submit | Message sent with attachment | Medium |
| MW-SC-003 | Empty subject | User logged in | 1. Leave Subject empty<br>2. Submit | Validation error | High |
| MW-SC-004 | Empty message body | User logged in | 1. Leave Message Body empty<br>2. Submit | Validation error | High |
| MW-SC-005 | Invalid attachment type | User logged in | 1. Attach invalid file type<br>2. Submit | Validation error | Medium |
| MW-SC-006 | Category dropdown | User logged in | 1. Click Category dropdown | Options: Account, Technical, Security, Other | Medium |

### Schedule Callback Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MW-SC-007 | Schedule callback | User logged in | 1. Select Reason for Call<br>2. Select Preferred Date (next business day+)<br>3. Select Time Window<br>4. Verify/edit Phone Number<br>5. Click "Request Callback" | "Callback request submitted." | High |
| MW-SC-008 | Phone pre-filled | User logged in | 1. View callback form | Phone number pre-filled from profile | Medium |
| MW-SC-009 | Date too soon | User logged in | 1. Select today's date or next non-business day<br>2. Submit | Validation error: date must be next business day or later | High |
| MW-SC-010 | Invalid phone format | User logged in | 1. Enter invalid phone<br>2. Submit | Validation error | High |
| MW-SC-011 | Email confirmation | MW-SC-007 completed | Check email | Confirmation email received | Medium |

---

## End-to-End Test Scenarios

### E2E-001: New User Registration and Account Opening
| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Navigate to registration page | Registration form displayed |
| 2 | Fill all fields with valid data | Fields accept input with auto-formatting |
| 3 | Submit registration | "Account created successfully" message |
| 4 | Login with new credentials | Redirected to Accounts Overview |
| 5 | Navigate to Open New Account | Form displayed |
| 6 | Open new Checking account | Account created, appears in overview |

### E2E-002: Complete Transfer Flow
| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Login as admin@parabank.com | Dashboard displayed |
| 2 | Note balances of two accounts | Balances recorded |
| 3 | Navigate to Transfer Funds | Transfer form displayed |
| 4 | Transfer $500 from Checking to Savings | "Transfer completed successfully." |
| 5 | View Accounts Overview | Checking reduced by $500, Savings increased by $500 |

### E2E-003: Bill Payment Flow
| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Login | Dashboard displayed |
| 2 | Navigate to Bill Pay | Payment form displayed |
| 3 | Select Electric Company from quick payees | Fields auto-populated |
| 4 | Enter payment amount $150 | Amount entered |
| 5 | Select source account | Account selected |
| 6 | Submit payment | "Payment submitted successfully." with reference code |
| 7 | Verify balance | Source account reduced by $150 |

### E2E-004: Loan Application Flow
| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Login | Dashboard displayed |
| 2 | Navigate to Request Loan | Loan form displayed |
| 3 | Select Personal Loan | Card selected, amount range shown |
| 4 | Enter $10,000 loan amount | Amount entered |
| 5 | Enter $1,500 down payment (15%) | Down payment entered |
| 6 | Select collateral account with > $2,000 | Account selected |
| 7 | Submit application | "Loan approved and created successfully!" |
| 8 | View Accounts Overview | New loan account visible |

---

## Test Summary

| Module | Total Tests | High Priority | Medium Priority | Low Priority |
|--------|-------------|---------------|-----------------|--------------|
| Login | 16 | 11 | 5 | 0 |
| Registration | 24 | 17 | 5 | 2 |
| Accounts Overview | 10 | 4 | 5 | 1 |
| Open New Account | 13 | 10 | 3 | 0 |
| Transfer Funds | 14 | 12 | 1 | 1 |
| Bill Pay | 15 | 14 | 1 | 0 |
| Request Loan | 18 | 15 | 3 | 0 |
| Update Contact Info | 18 | 14 | 4 | 0 |
| Manage Cards | 10 | 7 | 3 | 0 |
| Investments | 13 | 10 | 3 | 0 |
| Account Statements | 9 | 6 | 3 | 0 |
| Security Settings | 9 | 8 | 0 | 1 |
| Support Center | 11 | 6 | 5 | 0 |
| **TOTAL** | **180** | **134** | **41** | **5** |
