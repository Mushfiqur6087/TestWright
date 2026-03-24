# Parabank

**Base URL:** 
**Generated:** 2026-03-23T21:41:44.163365

## Summary

| Metric | Count |
|--------|-------|
| **Total Tests** | 151 |

### By Type

| Type | Count |
|------|-------|
| Positive | 36 |
| Negative | 98 |
| Edge Case | 17 |

### By Priority

| Priority | Count |
|----------|-------|
| High | 112 |
| Medium | 21 |
| Low | 18 |

---

## Test Cases

### login

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 1.LOGIN-001 | Login with valid email and password | None | 1. Enter a valid email address in the Email/Username field<br>2. Enter a valid password in the Password field<br>3. Click on the Sign In button | Show 'Signed in successfully.' and redirect to the Accounts Overview page | High |
| 1.LOGIN-002 | Login with valid username and password | None | 1. Enter a valid username in the Email/Username field<br>2. Enter a valid password in the Password field<br>3. Click on the Sign In button | Show 'Signed in successfully.' and redirect to the Accounts Overview page | High |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 1.LOGIN-003 | Email/Username field empty | None | 1. Leave the Email/Username field empty<br>2. Enter a valid password in the Password field<br>3. Click on the Sign In button | Show 'Incorrect email or password. Please try again,' and clear the password field | High |
| 1.LOGIN-004 | Password field empty | None | 1. Enter a valid email address in the Email/Username field<br>2. Leave the Password field empty<br>3. Click on the Sign In button | Show 'Incorrect email or password. Please try again,' and clear the password field | High |
| 1.LOGIN-005 | Invalid email format | None | 1. Enter an invalid email format in the Email/Username field<br>2. Enter a valid password in the Password field<br>3. Click on the Sign In button | Show 'Incorrect email or password. Please try again,' and clear the password field | Medium |
| 1.LOGIN-006 | Password too short | None | 1. Enter a valid email address in the Email/Username field<br>2. Enter a password shorter than 8 characters in the Password field<br>3. Click on the Sign In button | Show 'Incorrect email or password. Please try again,' and clear the password field | Medium |
| 1.LOGIN-007 | Password missing uppercase letter | None | 1. Enter a valid email address in the Email/Username field<br>2. Enter a password without an uppercase letter in the Password field<br>3. Click on the Sign In button | Show 'Incorrect email or password. Please try again,' and clear the password field | Medium |
| 1.LOGIN-008 | Password missing lowercase letter | None | 1. Enter a valid email address in the Email/Username field<br>2. Enter a password without a lowercase letter in the Password field<br>3. Click on the Sign In button | Show 'Incorrect email or password. Please try again,' and clear the password field | Medium |
| 1.LOGIN-009 | Password missing number | None | 1. Enter a valid email address in the Email/Username field<br>2. Enter a password without a number in the Password field<br>3. Click on the Sign In button | Show 'Incorrect email or password. Please try again,' and clear the password field | Medium |
| 1.LOGIN-010 | Password missing special character | None | 1. Enter a valid email address in the Email/Username field<br>2. Enter a password without a special character in the Password field<br>3. Click on the Sign In button | Show 'Incorrect email or password. Please try again,' and clear the password field | Medium |

---

### register

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 2.REGIST-001 | Successful account registration with valid inputs | None | 1. Enter valid first name<br>2. Enter valid last name<br>3. Enter valid street address<br>4. Enter valid city<br>5. Select valid state<br>6. Enter valid ZIP code<br>7. Enter valid phone number<br>8. Enter valid social security number<br>9. Enter valid username in email format<br>10. Enter valid password<br>11. Enter same password in confirm password field<br>12. Click on register button | Account created successfully — please sign in | High |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 2.REGIST-002 | First Name field empty | None | 1. Leave first name field empty<br>2. Enter valid last name<br>3. Enter valid street address<br>4. Enter valid city<br>5. Select valid state<br>6. Enter valid ZIP code<br>7. Enter valid phone number<br>8. Enter valid social security number<br>9. Enter valid username in email format<br>10. Enter valid password<br>11. Enter same password in confirm password field<br>12. Click on register button | Error message displayed for first name field | High |
| 2.REGIST-003 | Last Name field empty | None | 1. Enter valid first name<br>2. Leave last name field empty<br>3. Enter valid street address<br>4. Enter valid city<br>5. Select valid state<br>6. Enter valid ZIP code<br>7. Enter valid phone number<br>8. Enter valid social security number<br>9. Enter valid username in email format<br>10. Enter valid password<br>11. Enter same password in confirm password field<br>12. Click on register button | Error message displayed for last name field | High |
| 2.REGIST-004 | Street Address field empty | None | 1. Enter valid first name<br>2. Enter valid last name<br>3. Leave street address field empty<br>4. Enter valid city<br>5. Select valid state<br>6. Enter valid ZIP code<br>7. Enter valid phone number<br>8. Enter valid social security number<br>9. Enter valid username in email format<br>10. Enter valid password<br>11. Enter same password in confirm password field<br>12. Click on register button | Error message displayed for street address field | High |
| 2.REGIST-005 | City field empty | None | 1. Enter valid first name<br>2. Enter valid last name<br>3. Enter valid street address<br>4. Leave city field empty<br>5. Select valid state<br>6. Enter valid ZIP code<br>7. Enter valid phone number<br>8. Enter valid social security number<br>9. Enter valid username in email format<br>10. Enter valid password<br>11. Enter same password in confirm password field<br>12. Click on register button | Error message displayed for city field | High |
| 2.REGIST-006 | State field empty | None | 1. Enter valid first name<br>2. Enter valid last name<br>3. Enter valid street address<br>4. Enter valid city<br>5. Leave state field empty<br>6. Enter valid ZIP code<br>7. Enter valid phone number<br>8. Enter valid social security number<br>9. Enter valid username in email format<br>10. Enter valid password<br>11. Enter same password in confirm password field<br>12. Click on register button | Error message displayed for state field | High |
| 2.REGIST-007 | ZIP Code field empty | None | 1. Enter valid first name<br>2. Enter valid last name<br>3. Enter valid street address<br>4. Enter valid city<br>5. Select valid state<br>6. Leave ZIP code field empty<br>7. Enter valid phone number<br>8. Enter valid social security number<br>9. Enter valid username in email format<br>10. Enter valid password<br>11. Enter same password in confirm password field<br>12. Click on register button | Error message displayed for ZIP code field | High |
| 2.REGIST-008 | Phone Number field empty | None | 1. Enter valid first name<br>2. Enter valid last name<br>3. Enter valid street address<br>4. Enter valid city<br>5. Select valid state<br>6. Enter valid ZIP code<br>7. Leave phone number field empty<br>8. Enter valid social security number<br>9. Enter valid username in email format<br>10. Enter valid password<br>11. Enter same password in confirm password field<br>12. Click on register button | Error message displayed for phone number field | High |
| 2.REGIST-009 | Social Security Number field empty | None | 1. Enter valid first name<br>2. Enter valid last name<br>3. Enter valid street address<br>4. Enter valid city<br>5. Select valid state<br>6. Enter valid ZIP code<br>7. Enter valid phone number<br>8. Leave social security number field empty<br>9. Enter valid username in email format<br>10. Enter valid password<br>11. Enter same password in confirm password field<br>12. Click on register button | Error message displayed for social security number field | High |
| 2.REGIST-010 | Username field empty | None | 1. Enter valid first name<br>2. Enter valid last name<br>3. Enter valid street address<br>4. Enter valid city<br>5. Select valid state<br>6. Enter valid ZIP code<br>7. Enter valid phone number<br>8. Enter valid social security number<br>9. Leave username field empty<br>10. Enter valid password<br>11. Enter same password in confirm password field<br>12. Click on register button | Error message displayed for username field | High |
| 2.REGIST-011 | Password field empty | None | 1. Enter valid first name<br>2. Enter valid last name<br>3. Enter valid street address<br>4. Enter valid city<br>5. Select valid state<br>6. Enter valid ZIP code<br>7. Enter valid phone number<br>8. Enter valid social security number<br>9. Enter valid username in email format<br>10. Leave password field empty<br>11. Enter same password in confirm password field<br>12. Click on register button | Error message displayed for password field | High |
| 2.REGIST-012 | Confirm Password field empty | None | 1. Enter valid first name<br>2. Enter valid last name<br>3. Enter valid street address<br>4. Enter valid city<br>5. Select valid state<br>6. Enter valid ZIP code<br>7. Enter valid phone number<br>8. Enter valid social security number<br>9. Enter valid username in email format<br>10. Enter valid password<br>11. Leave confirm password field empty<br>12. Click on register button | Error message displayed for confirm password field | High |
| 2.REGIST-013 | Password and Confirm Password mismatch | None | 1. Enter valid first name<br>2. Enter valid last name<br>3. Enter valid street address<br>4. Enter valid city<br>5. Select valid state<br>6. Enter valid ZIP code<br>7. Enter valid phone number<br>8. Enter valid social security number<br>9. Enter valid username in email format<br>10. Enter valid password<br>11. Enter different password in confirm password field<br>12. Click on register button | Error message displayed for password mismatch | High |
| 2.REGIST-014 | Username not in valid email format | None | 1. Enter valid first name<br>2. Enter valid last name<br>3. Enter valid street address<br>4. Enter valid city<br>5. Select valid state<br>6. Enter valid ZIP code<br>7. Enter valid phone number<br>8. Enter valid social security number<br>9. Enter invalid username format<br>10. Enter valid password<br>11. Enter same password in confirm password field<br>12. Click on register button | Error message displayed for invalid username format | High |
| 2.REGIST-015 | Phone Number not in valid format | None | 1. Enter valid first name<br>2. Enter valid last name<br>3. Enter valid street address<br>4. Enter valid city<br>5. Select valid state<br>6. Enter valid ZIP code<br>7. Enter invalid phone number format<br>8. Enter valid social security number<br>9. Enter valid username in email format<br>10. Enter valid password<br>11. Enter same password in confirm password field<br>12. Click on register button | Error message displayed for invalid phone number format | High |
| 2.REGIST-016 | ZIP Code not in valid format | None | 1. Enter valid first name<br>2. Enter valid last name<br>3. Enter valid street address<br>4. Enter valid city<br>5. Select valid state<br>6. Enter invalid ZIP code format<br>7. Enter valid phone number<br>8. Enter valid social security number<br>9. Enter valid username in email format<br>10. Enter valid password<br>11. Enter same password in confirm password field<br>12. Click on register button | Error message displayed for invalid ZIP code format | High |
| 2.REGIST-017 | Social Security Number not in valid format | None | 1. Enter valid first name<br>2. Enter valid last name<br>3. Enter valid street address<br>4. Enter valid city<br>5. Select valid state<br>6. Enter valid ZIP code<br>7. Enter valid phone number<br>8. Enter invalid social security number format<br>9. Enter valid username in email format<br>10. Enter valid password<br>11. Enter same password in confirm password field<br>12. Click on register button | Error message displayed for invalid social security number format | High |
| 2.REGIST-018 | Password shorter than 8 characters | None | 1. Enter valid first name<br>2. Enter valid last name<br>3. Enter valid street address<br>4. Enter valid city<br>5. Select valid state<br>6. Enter valid ZIP code<br>7. Enter valid phone number<br>8. Enter valid social security number<br>9. Enter valid username in email format<br>10. Enter short password<br>11. Enter same short password in confirm password field<br>12. Click on register button | Error message displayed for password length requirement | High |

#### Edge Case Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 2.REGIST-019 | Maximum length for first name | None | 1. Enter maximum length first name<br>2. Enter valid last name<br>3. Enter valid street address<br>4. Enter valid city<br>5. Select valid state<br>6. Enter valid ZIP code<br>7. Enter valid phone number<br>8. Enter valid social security number<br>9. Enter valid username in email format<br>10. Enter valid password<br>11. Enter same password in confirm password field<br>12. Click on register button | Account created successfully — please sign in | Low |
| 2.REGIST-020 | Maximum length for last name | None | 1. Enter valid first name<br>2. Enter maximum length last name<br>3. Enter valid street address<br>4. Enter valid city<br>5. Select valid state<br>6. Enter valid ZIP code<br>7. Enter valid phone number<br>8. Enter valid social security number<br>9. Enter valid username in email format<br>10. Enter valid password<br>11. Enter same password in confirm password field<br>12. Click on register button | Account created successfully — please sign in | Low |

---

### accounts_overview

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 3.ACCOUN-001 | Welcome message displays user's name | User is logged in | 1. Locate the welcome message element<br>2. Verify the welcome message contains the user's name | Welcome message displays the user's name correctly | High |
| 3.ACCOUN-002 | Customer accounts table displays correctly | User is logged in | 1. Locate the customer accounts table<br>2. Verify the table is displayed<br>3. Verify the table contains rows for each account | Customer accounts table is displayed with all account rows | High |
| 3.ACCOUN-003 | Account numbers are masked for security | User is logged in and has accounts | 1. Locate the account number elements in the table<br>2. Verify each account number displays as **** followed by the last 4 digits | Account numbers are masked correctly | High |
| 3.ACCOUN-004 | Accounts are ordered by creation date (earliest first) | User is logged in and has multiple accounts | 1. Locate the account creation date elements<br>2. Verify the accounts are ordered from earliest to latest | Accounts are displayed in the correct order by creation date | High |
| 3.ACCOUN-005 | Total balance footer displays correctly | User is logged in and has accounts | 1. Locate the total balance footer<br>2. Verify the total balance matches the sum of current balances of all accounts | Total balance footer displays the correct total balance | High |

---

### open_new_account

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 4.OPEN_N-001 | Open Checking Account with Valid Initial Deposit | None | 1. Select 'Checking' as account type<br>2. Enter a valid numeric initial deposit amount above $25<br>3. Select a valid funding source account<br>4. Click on 'Open Account' button | Account opened successfully! | High |
| 4.OPEN_N-002 | Open Savings Account with Valid Initial Deposit | None | 1. Select 'Savings' as account type<br>2. Enter a valid numeric initial deposit amount above $100<br>3. Select a valid funding source account<br>4. Click on 'Open Account' button | Account opened successfully! | High |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 4.OPEN_N-003 | Initial Deposit Amount Field Empty | None | 1. Select 'Checking' as account type<br>2. Leave initial deposit amount field empty<br>3. Select a valid funding source account<br>4. Click on 'Open Account' button | Real-time validation error displayed for initial deposit amount | High |
| 4.OPEN_N-004 | Funding Source Account Field Empty | None | 1. Select 'Checking' as account type<br>2. Enter a valid numeric initial deposit amount above $25<br>3. Leave funding source account field empty<br>4. Click on 'Open Account' button | Real-time validation error displayed for funding source account | High |
| 4.OPEN_N-005 | Initial Deposit Amount Below Minimum for Checking | None | 1. Select 'Checking' as account type<br>2. Enter a numeric initial deposit amount of $20<br>3. Select a valid funding source account<br>4. Click on 'Open Account' button | Real-time validation error displayed for initial deposit amount | High |
| 4.OPEN_N-006 | Initial Deposit Amount Below Minimum for Savings | None | 1. Select 'Savings' as account type<br>2. Enter a numeric initial deposit amount of $50<br>3. Select a valid funding source account<br>4. Click on 'Open Account' button | Real-time validation error displayed for initial deposit amount | High |
| 4.OPEN_N-007 | Insufficient Balance in Funding Source Account | None | 1. Select 'Checking' as account type<br>2. Enter a valid numeric initial deposit amount above $25<br>3. Select a funding source account with insufficient balance<br>4. Click on 'Open Account' button | Real-time validation error displayed for insufficient balance | High |

#### Edge Case Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 4.OPEN_N-008 | Open Checking Account with Exact Minimum Initial Deposit | None | 1. Select 'Checking' as account type<br>2. Enter a numeric initial deposit amount of $25<br>3. Select a valid funding source account<br>4. Click on 'Open Account' button | Account opened successfully! | Low |
| 4.OPEN_N-009 | Open Savings Account with Exact Minimum Initial Deposit | None | 1. Select 'Savings' as account type<br>2. Enter a numeric initial deposit amount of $100<br>3. Select a valid funding source account<br>4. Click on 'Open Account' button | Account opened successfully! | Low |
| 4.OPEN_N-010 | Open Checking Account with Just Below Minimum Initial Deposit | None | 1. Select 'Checking' as account type<br>2. Enter a numeric initial deposit amount of $24.99<br>3. Select a valid funding source account<br>4. Click on 'Open Account' button | Real-time validation error displayed for initial deposit amount | Low |
| 4.OPEN_N-011 | Open Savings Account with Just Below Minimum Initial Deposit | None | 1. Select 'Savings' as account type<br>2. Enter a numeric initial deposit amount of $99.99<br>3. Select a valid funding source account<br>4. Click on 'Open Account' button | Real-time validation error displayed for initial deposit amount | Low |

---

### transfer_funds

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 5.TRANSF-001 | Transfer funds successfully from My ParaBank Account | User has sufficient funds in their Checking account | 1. Select 'My ParaBank Account' as the transfer type<br>2. Enter a valid transfer amount<br>3. Select a Checking account as the source account<br>4. Click the Submit button | Transfer completed successfully with a transaction ID | High |
| 5.TRANSF-002 | Transfer funds successfully from Savings Account | User has sufficient funds in their Savings account | 1. Select 'My ParaBank Account' as the transfer type<br>2. Enter a valid transfer amount<br>3. Select a Savings account as the source account<br>4. Click the Submit button | Transfer completed successfully with a transaction ID | High |
| 5.TRANSF-003 | Transfer funds successfully to an External Account | User has sufficient funds in their Checking account | 1. Select 'External Account' as the transfer type<br>2. Enter a valid transfer amount<br>3. Select a Checking account as the source account<br>4. Enter a valid account number for external transfer<br>5. Confirm the account number matches<br>6. Click the Submit button | Transfer completed successfully with a transaction ID | High |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 5.TRANSF-004 | Transfer Amount field empty | None | 1. Select 'My ParaBank Account' as the transfer type<br>2. Leave the transfer amount field empty<br>3. Select a Checking account as the source account<br>4. Click the Submit button | Error shown indicating Transfer Amount is required | High |
| 5.TRANSF-005 | Source Account field empty | None | 1. Select 'My ParaBank Account' as the transfer type<br>2. Enter a valid transfer amount<br>3. Leave the source account field empty<br>4. Click the Submit button | Error shown indicating Source Account is required | High |
| 5.TRANSF-006 | Insufficient funds for transfer | User has insufficient funds in their Checking account | 1. Select 'My ParaBank Account' as the transfer type<br>2. Enter a valid transfer amount greater than available balance<br>3. Select a Checking account as the source account<br>4. Click the Submit button | Error shown indicating insufficient funds | High |
| 5.TRANSF-007 | Account number mismatch for external transfer | User has sufficient funds in their Checking account | 1. Select 'External Account' as the transfer type<br>2. Enter a valid transfer amount<br>3. Select a Checking account as the source account<br>4. Enter a valid account number for external transfer<br>5. Enter a different account number in the confirm field<br>6. Click the Submit button | Error shown indicating account numbers do not match | High |

#### Edge Case Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 5.TRANSF-008 | Transfer Amount at exact boundary value | User has sufficient funds in their Checking account | 1. Select 'My ParaBank Account' as the transfer type<br>2. Enter an exact boundary transfer amount<br>3. Select a Checking account as the source account<br>4. Click the Submit button | Transfer completed successfully with a transaction ID | Low |
| 5.TRANSF-009 | Transfer Amount just below boundary value | User has sufficient funds in their Checking account | 1. Select 'My ParaBank Account' as the transfer type<br>2. Enter a transfer amount just below the boundary<br>3. Select a Checking account as the source account<br>4. Click the Submit button | Transfer completed successfully with a transaction ID | Low |

---

### payments

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 6.PAYMEN-001 | Submit payment with valid inputs | None | 1. Enter valid Payee Name<br>2. Enter valid Street Address<br>3. Enter valid City<br>4. Select valid State<br>5. Enter valid ZIP Code<br>6. Enter valid Phone Number<br>7. Enter valid Payee Account Number<br>8. Enter matching Confirm Account Number<br>9. Enter valid Payment Amount<br>10. Click Pay button | Payment submitted successfully with a reference code and balances updated | High |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 6.PAYMEN-002 | Payee Name field empty | None | 1. Leave Payee Name field empty<br>2. Enter valid Street Address<br>3. Enter valid City<br>4. Select valid State<br>5. Enter valid ZIP Code<br>6. Enter valid Phone Number<br>7. Enter valid Payee Account Number<br>8. Enter matching Confirm Account Number<br>9. Enter valid Payment Amount<br>10. Click Pay button | Error displayed inline for Payee Name field | High |
| 6.PAYMEN-003 | Street Address field empty | None | 1. Enter valid Payee Name<br>2. Leave Street Address field empty<br>3. Enter valid City<br>4. Select valid State<br>5. Enter valid ZIP Code<br>6. Enter valid Phone Number<br>7. Enter valid Payee Account Number<br>8. Enter matching Confirm Account Number<br>9. Enter valid Payment Amount<br>10. Click Pay button | Error displayed inline for Street Address field | High |
| 6.PAYMEN-004 | City field empty | None | 1. Enter valid Payee Name<br>2. Enter valid Street Address<br>3. Leave City field empty<br>4. Select valid State<br>5. Enter valid ZIP Code<br>6. Enter valid Phone Number<br>7. Enter valid Payee Account Number<br>8. Enter matching Confirm Account Number<br>9. Enter valid Payment Amount<br>10. Click Pay button | Error displayed inline for City field | High |
| 6.PAYMEN-005 | State field empty | None | 1. Enter valid Payee Name<br>2. Enter valid Street Address<br>3. Enter valid City<br>4. Leave State field empty<br>5. Enter valid ZIP Code<br>6. Enter valid Phone Number<br>7. Enter valid Payee Account Number<br>8. Enter matching Confirm Account Number<br>9. Enter valid Payment Amount<br>10. Click Pay button | Error displayed inline for State field | High |
| 6.PAYMEN-006 | ZIP Code field empty | None | 1. Enter valid Payee Name<br>2. Enter valid Street Address<br>3. Enter valid City<br>4. Select valid State<br>5. Leave ZIP Code field empty<br>6. Enter valid Phone Number<br>7. Enter valid Payee Account Number<br>8. Enter matching Confirm Account Number<br>9. Enter valid Payment Amount<br>10. Click Pay button | Error displayed inline for ZIP Code field | High |
| 6.PAYMEN-007 | Phone Number field empty | None | 1. Enter valid Payee Name<br>2. Enter valid Street Address<br>3. Enter valid City<br>4. Select valid State<br>5. Enter valid ZIP Code<br>6. Leave Phone Number field empty<br>7. Enter valid Payee Account Number<br>8. Enter matching Confirm Account Number<br>9. Enter valid Payment Amount<br>10. Click Pay button | Error displayed inline for Phone Number field | High |
| 6.PAYMEN-008 | Payee Account Number field empty | None | 1. Enter valid Payee Name<br>2. Enter valid Street Address<br>3. Enter valid City<br>4. Select valid State<br>5. Enter valid ZIP Code<br>6. Enter valid Phone Number<br>7. Leave Payee Account Number field empty<br>8. Enter matching Confirm Account Number<br>9. Enter valid Payment Amount<br>10. Click Pay button | Error displayed inline for Payee Account Number field | High |
| 6.PAYMEN-009 | Confirm Account Number field empty | None | 1. Enter valid Payee Name<br>2. Enter valid Street Address<br>3. Enter valid City<br>4. Select valid State<br>5. Enter valid ZIP Code<br>6. Enter valid Phone Number<br>7. Enter valid Payee Account Number<br>8. Leave Confirm Account Number field empty<br>9. Enter valid Payment Amount<br>10. Click Pay button | Error displayed inline for Confirm Account Number field | High |
| 6.PAYMEN-010 | Payment Amount field empty | None | 1. Enter valid Payee Name<br>2. Enter valid Street Address<br>3. Enter valid City<br>4. Select valid State<br>5. Enter valid ZIP Code<br>6. Enter valid Phone Number<br>7. Enter valid Payee Account Number<br>8. Enter matching Confirm Account Number<br>9. Leave Payment Amount field empty<br>10. Click Pay button | Error displayed inline for Payment Amount field | High |
| 6.PAYMEN-011 | Account number mismatch | None | 1. Enter valid Payee Name<br>2. Enter valid Street Address<br>3. Enter valid City<br>4. Select valid State<br>5. Enter valid ZIP Code<br>6. Enter valid Phone Number<br>7. Enter valid Payee Account Number<br>8. Enter non-matching Confirm Account Number<br>9. Enter valid Payment Amount<br>10. Click Pay button | Error displayed inline for account number mismatch | High |
| 6.PAYMEN-012 | Insufficient funds for payment | None | 1. Enter valid Payee Name<br>2. Enter valid Street Address<br>3. Enter valid City<br>4. Select valid State<br>5. Enter valid ZIP Code<br>6. Enter valid Phone Number<br>7. Enter valid Payee Account Number<br>8. Enter matching Confirm Account Number<br>9. Enter Payment Amount exceeding available funds<br>10. Click Pay button | Error displayed inline for insufficient funds | High |

#### Edge Case Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 6.PAYMEN-013 | Submit payment with maximum Payment Amount | None | 1. Enter valid Payee Name<br>2. Enter valid Street Address<br>3. Enter valid City<br>4. Select valid State<br>5. Enter valid ZIP Code<br>6. Enter valid Phone Number<br>7. Enter valid Payee Account Number<br>8. Enter matching Confirm Account Number<br>9. Enter maximum valid Payment Amount<br>10. Click Pay button | Payment submitted successfully with a reference code and balances updated | Low |
| 6.PAYMEN-014 | Submit payment with Payment Amount just below maximum | None | 1. Enter valid Payee Name<br>2. Enter valid Street Address<br>3. Enter valid City<br>4. Select valid State<br>5. Enter valid ZIP Code<br>6. Enter valid Phone Number<br>7. Enter valid Payee Account Number<br>8. Enter matching Confirm Account Number<br>9. Enter Payment Amount just below maximum<br>10. Click Pay button | Payment submitted successfully with a reference code and balances updated | Low |

---

### request_loan

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 7.REQUES-001 | Successful loan request with valid inputs | None | 1. Enter a valid Loan Amount within the type-specific range<br>2. Enter a valid Down Payment Amount less than the Loan Amount<br>3. Select a valid Collateral Account with sufficient funds<br>4. Select a loan type card | Loan approved and created successfully! | High |
| 7.REQUES-009 | Display of loan type cards | None | 1. Verify that Personal loan type card is displayed<br>2. Verify that Auto loan type card is displayed<br>3. Verify that Home loan type card is displayed | All loan type cards are displayed correctly | Medium |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 7.REQUES-002 | Loan Amount field empty | None | 1. Leave the Loan Amount field empty<br>2. Enter a valid Down Payment Amount<br>3. Select a valid Collateral Account<br>4. Select a loan type card | Error message indicating Loan Amount is required | High |
| 7.REQUES-003 | Down Payment Amount field empty | None | 1. Enter a valid Loan Amount<br>2. Leave the Down Payment Amount field empty<br>3. Select a valid Collateral Account<br>4. Select a loan type card | Error message indicating Down Payment Amount is required | High |
| 7.REQUES-004 | Collateral Account not selected | None | 1. Enter a valid Loan Amount<br>2. Enter a valid Down Payment Amount<br>3. Leave the Collateral Account unselected<br>4. Select a loan type card | Error message indicating Collateral Account must be selected | High |
| 7.REQUES-005 | Loan Amount exceeds type-specific range | None | 1. Enter an invalid Loan Amount exceeding the maximum limit<br>2. Enter a valid Down Payment Amount<br>3. Select a valid Collateral Account<br>4. Select a loan type card | Error message indicating Loan Amount exceeds the allowed range | High |
| 7.REQUES-006 | Down Payment Amount greater than Loan Amount | None | 1. Enter a valid Loan Amount<br>2. Enter a Down Payment Amount greater than the Loan Amount<br>3. Select a valid Collateral Account<br>4. Select a loan type card | Error message indicating Down Payment Amount must be less than Loan Amount | High |
| 7.REQUES-007 | Insufficient collateral funds | None | 1. Enter a valid Loan Amount<br>2. Enter a valid Down Payment Amount<br>3. Select a valid Collateral Account with insufficient funds<br>4. Select a loan type card | Error message indicating insufficient collateral funds | High |
| 7.REQUES-008 | Collateral value less than 20% | None | 1. Enter a valid Loan Amount<br>2. Enter a valid Down Payment Amount<br>3. Select a valid Collateral Account with less than 20% value<br>4. Select a loan type card | Error message indicating collateral value must be at least 20% | High |

---

### update_contact_info

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 8.UPDATE-001 | Update profile with valid contact information | None | 1. Enter a valid first name<br>2. Enter a valid last name<br>3. Enter a valid street address<br>4. Enter a valid city<br>5. Select a valid state<br>6. Enter a valid ZIP code<br>7. Enter a valid phone number<br>8. Click on the Update Profile button | Profile updated successfully | High |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 8.UPDATE-002 | First Name field empty | None | 1. Leave the first name field empty<br>2. Enter a valid last name<br>3. Enter a valid street address<br>4. Enter a valid city<br>5. Select a valid state<br>6. Enter a valid ZIP code<br>7. Enter a valid phone number<br>8. Click on the Update Profile button | First Name field is highlighted as required | High |
| 8.UPDATE-003 | Last Name field empty | None | 1. Enter a valid first name<br>2. Leave the last name field empty<br>3. Enter a valid street address<br>4. Enter a valid city<br>5. Select a valid state<br>6. Enter a valid ZIP code<br>7. Enter a valid phone number<br>8. Click on the Update Profile button | Last Name field is highlighted as required | High |
| 8.UPDATE-004 | Street Address field empty | None | 1. Enter a valid first name<br>2. Enter a valid last name<br>3. Leave the street address field empty<br>4. Enter a valid city<br>5. Select a valid state<br>6. Enter a valid ZIP code<br>7. Enter a valid phone number<br>8. Click on the Update Profile button | Street Address field is highlighted as required | High |
| 8.UPDATE-005 | City field empty | None | 1. Enter a valid first name<br>2. Enter a valid last name<br>3. Enter a valid street address<br>4. Leave the city field empty<br>5. Select a valid state<br>6. Enter a valid ZIP code<br>7. Enter a valid phone number<br>8. Click on the Update Profile button | City field is highlighted as required | High |
| 8.UPDATE-006 | State field empty | None | 1. Enter a valid first name<br>2. Enter a valid last name<br>3. Enter a valid street address<br>4. Enter a valid city<br>5. Leave the state field empty<br>6. Enter a valid ZIP code<br>7. Enter a valid phone number<br>8. Click on the Update Profile button | State field is highlighted as required | High |
| 8.UPDATE-007 | ZIP Code field empty | None | 1. Enter a valid first name<br>2. Enter a valid last name<br>3. Enter a valid street address<br>4. Enter a valid city<br>5. Select a valid state<br>6. Leave the ZIP Code field empty<br>7. Enter a valid phone number<br>8. Click on the Update Profile button | ZIP Code field is highlighted as required | High |
| 8.UPDATE-008 | Phone Number field empty | None | 1. Enter a valid first name<br>2. Enter a valid last name<br>3. Enter a valid street address<br>4. Enter a valid city<br>5. Select a valid state<br>6. Enter a valid ZIP code<br>7. Leave the phone number field empty<br>8. Click on the Update Profile button | Phone Number field is highlighted as required | High |
| 8.UPDATE-009 | Invalid format for ZIP Code | None | 1. Enter a valid first name<br>2. Enter a valid last name<br>3. Enter a valid street address<br>4. Enter a valid city<br>5. Select a valid state<br>6. Enter an invalid ZIP Code format<br>7. Enter a valid phone number<br>8. Click on the Update Profile button | ZIP Code field is highlighted for invalid format | Medium |
| 8.UPDATE-010 | Invalid format for Phone Number | None | 1. Enter a valid first name<br>2. Enter a valid last name<br>3. Enter a valid street address<br>4. Enter a valid city<br>5. Select a valid state<br>6. Enter a valid ZIP Code<br>7. Enter an invalid Phone Number format<br>8. Click on the Update Profile button | Phone Number field is highlighted for invalid format | Medium |

#### Edge Case Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 8.UPDATE-011 | Update profile with maximum length values | None | 1. Enter a valid first name with maximum length<br>2. Enter a valid last name with maximum length<br>3. Enter a valid street address with maximum length<br>4. Enter a valid city with maximum length<br>5. Select a valid state<br>6. Enter a valid ZIP Code<br>7. Enter a valid phone number<br>8. Click on the Update Profile button | Profile updated successfully | Low |

---

### manage_cards

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 9.MANAGE-001 | Request card with valid shipping address | None | 1. Select a card type from the available options<br>2. Select an account to link from the available accounts<br>3. Enter a valid shipping address<br>4. Click on the Request Card button | Card request submitted successfully with a tracking ID | High |
| 9.MANAGE-002 | Update card controls with valid spending limit | Card is selected | 1. Enter a valid new spending limit<br>2. Select a valid travel notice<br>3. Select a valid card status<br>4. Click on Update Controls button | Card controls updated successfully | High |
| 9.MANAGE-003 | Verify card controls updated state after successful update | Card controls updated successfully | 1. Check the displayed new spending limit<br>2. Check the displayed travel notice<br>3. Check the displayed card status | Displayed values match the updated card controls | High |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 9.MANAGE-004 | Shipping address field empty | None | 1. Select a card type from the available options<br>2. Select an account to link from the available accounts<br>3. Leave the shipping address field empty<br>4. Click on the Request Card button | Error message displayed indicating that shipping address is required | High |
| 9.MANAGE-005 | Update card controls with empty spending limit | Card is selected | 1. Leave the new spending limit field empty<br>2. Select a valid travel notice<br>3. Select a valid card status<br>4. Click on Update Controls button | Validation error displayed for spending limit field | High |
| 9.MANAGE-006 | Update card controls with empty travel notice | Card is selected | 1. Enter a valid new spending limit<br>2. Leave the travel notice field empty<br>3. Select a valid card status<br>4. Click on Update Controls button | Validation error displayed for travel notice field | High |
| 9.MANAGE-007 | Update card controls with empty card status | Card is selected | 1. Enter a valid new spending limit<br>2. Select a valid travel notice<br>3. Leave the card status field empty<br>4. Click on Update Controls button | Validation error displayed for card status field | High |
| 9.MANAGE-008 | Update card controls with invalid spending limit | Card is selected | 1. Enter an invalid new spending limit<br>2. Select a valid travel notice<br>3. Select a valid card status<br>4. Click on Update Controls button | Validation error displayed for spending limit field | High |
| 9.MANAGE-009 | Update card controls with invalid date range for travel notice | Card is selected | 1. Enter a valid new spending limit<br>2. Enter an invalid travel notice date range<br>3. Select a valid card status<br>4. Click on Update Controls button | Validation error displayed for travel notice date range | High |
| 9.MANAGE-010 | Update card controls with invalid card status transition | Card is selected | 1. Enter a valid new spending limit<br>2. Select a valid travel notice<br>3. Select an invalid card status transition<br>4. Click on Update Controls button | Validation error displayed for card status transition | High |

#### Edge Case Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 9.MANAGE-011 | Update card controls with maximum spending limit | Card is selected | 1. Enter the maximum valid spending limit<br>2. Select a valid travel notice<br>3. Select a valid card status<br>4. Click on Update Controls button | Card controls updated successfully | Low |
| 9.MANAGE-012 | Update card controls with spending limit just below maximum | Card is selected | 1. Enter a spending limit just below the maximum valid limit<br>2. Select a valid travel notice<br>3. Select a valid card status<br>4. Click on Update Controls button | Card controls updated successfully | Low |

---

### investments

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 10.INVEST-001 | Execute trade with valid parameters | User has sufficient buying power | 1. Select 'Buy' from the Action dropdown<br>2. Enter a valid Fund Symbol in the Fund Symbol field<br>3. Enter a valid Quantity greater than zero in the Quantity field<br>4. Select a valid Funding or Destination Account from the dropdown<br>5. Click the Execute Trade button | Trade executed successfully with an order ID displayed | High |
| 10.INVEST-002 | Create recurring investment plan with valid inputs | None | 1. Enter a valid fund symbol in the fund symbol field<br>2. Enter a valid contribution amount that meets the minimum requirement<br>3. Select a valid frequency from the frequency dropdown<br>4. Select a future date in the start date field<br>5. Select a funding account with adequate balance<br>6. Click the Create Plan button | Recurring investment plan is created successfully | High |
| 10.INVEST-014 | Verify Fund Symbol autocomplete functionality | User is on the Execute Trade page | 1. Select 'Buy' from the Action dropdown<br>2. Start typing a valid Fund Symbol in the Fund Symbol field<br>3. Observe the autocomplete suggestions | Autocomplete suggestions for valid Fund Symbols are displayed | Medium |
| 10.INVEST-015 | Verify dropdown options for Funding or Destination Account | User is on the Execute Trade page | 1. Select 'Buy' from the Action dropdown<br>2. Click on the Funding or Destination Account dropdown<br>3. Observe the available account options | Dropdown displays a list of valid Funding or Destination Accounts | Medium |
| 10.INVEST-016 | Verify fields are displayed correctly | None | 1. Check that the fund symbol field is present<br>2. Check that the contribution amount field is present<br>3. Check that the frequency dropdown is present<br>4. Check that the start date field is present<br>5. Check that the funding account field is present<br>6. Check that the Create Plan button is present | All fields and button are displayed correctly on the page | Medium |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 10.INVEST-003 | Fund Symbol field empty | User is on the Execute Trade page | 1. Select 'Buy' from the Action dropdown<br>2. Leave the Fund Symbol field empty<br>3. Enter a valid Quantity greater than zero in the Quantity field<br>4. Select a valid Funding or Destination Account from the dropdown<br>5. Click the Execute Trade button | Validation error appears indicating the Fund Symbol is required | High |
| 10.INVEST-004 | Quantity field empty | User is on the Execute Trade page | 1. Select 'Buy' from the Action dropdown<br>2. Enter a valid Fund Symbol in the Fund Symbol field<br>3. Leave the Quantity field empty<br>4. Select a valid Funding or Destination Account from the dropdown<br>5. Click the Execute Trade button | Validation error appears indicating the Quantity is required | High |
| 10.INVEST-005 | Quantity less than or equal to zero | User is on the Execute Trade page | 1. Select 'Buy' from the Action dropdown<br>2. Enter a valid Fund Symbol in the Fund Symbol field<br>3. Enter a Quantity of zero in the Quantity field<br>4. Select a valid Funding or Destination Account from the dropdown<br>5. Click the Execute Trade button | Validation error appears indicating Quantity must be greater than zero | High |
| 10.INVEST-006 | Insufficient buying power | User has insufficient buying power | 1. Select 'Buy' from the Action dropdown<br>2. Enter a valid Fund Symbol in the Fund Symbol field<br>3. Enter a valid Quantity greater than zero in the Quantity field<br>4. Select a valid Funding or Destination Account from the dropdown<br>5. Click the Execute Trade button | Validation error appears indicating insufficient buying power | High |
| 10.INVEST-007 | Contribution amount field empty | None | 1. Enter a valid fund symbol in the fund symbol field<br>2. Leave the contribution amount field empty<br>3. Select a valid frequency from the frequency dropdown<br>4. Select a future date in the start date field<br>5. Select a funding account with adequate balance<br>6. Click the Create Plan button | Inline validation message appears for contribution amount field | High |
| 10.INVEST-008 | Frequency field empty | None | 1. Enter a valid fund symbol in the fund symbol field<br>2. Enter a valid contribution amount that meets the minimum requirement<br>3. Leave the frequency field empty<br>4. Select a future date in the start date field<br>5. Select a funding account with adequate balance<br>6. Click the Create Plan button | Inline validation message appears for frequency field | High |
| 10.INVEST-009 | Start date field empty | None | 1. Enter a valid fund symbol in the fund symbol field<br>2. Enter a valid contribution amount that meets the minimum requirement<br>3. Select a valid frequency from the frequency dropdown<br>4. Leave the start date field empty<br>5. Select a funding account with adequate balance<br>6. Click the Create Plan button | Inline validation message appears for start date field | High |
| 10.INVEST-010 | Funding account field empty | None | 1. Enter a valid fund symbol in the fund symbol field<br>2. Enter a valid contribution amount that meets the minimum requirement<br>3. Select a valid frequency from the frequency dropdown<br>4. Select a future date in the start date field<br>5. Leave the funding account field empty<br>6. Click the Create Plan button | Inline validation message appears for funding account field | High |
| 10.INVEST-011 | Start date is not in the future | None | 1. Enter a valid fund symbol in the fund symbol field<br>2. Enter a valid contribution amount that meets the minimum requirement<br>3. Select a valid frequency from the frequency dropdown<br>4. Select a date in the start date field that is today or in the past<br>5. Select a funding account with adequate balance<br>6. Click the Create Plan button | Inline validation message appears for start date field | High |
| 10.INVEST-012 | Contribution amount below minimum requirement | None | 1. Enter a valid fund symbol in the fund symbol field<br>2. Enter a contribution amount that is below the minimum requirement<br>3. Select a valid frequency from the frequency dropdown<br>4. Select a future date in the start date field<br>5. Select a funding account with adequate balance<br>6. Click the Create Plan button | Inline validation message appears for contribution amount field | High |
| 10.INVEST-013 | Funding account does not have adequate balance | None | 1. Enter a valid fund symbol in the fund symbol field<br>2. Enter a valid contribution amount that meets the minimum requirement<br>3. Select a valid frequency from the frequency dropdown<br>4. Select a future date in the start date field<br>5. Select a funding account that does not have adequate balance<br>6. Click the Create Plan button | Inline validation message appears for funding account balance | High |

#### Edge Case Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 10.INVEST-017 | Execute trade with maximum Quantity | User has sufficient buying power | 1. Select 'Buy' from the Action dropdown<br>2. Enter a valid Fund Symbol in the Fund Symbol field<br>3. Enter the maximum valid Quantity in the Quantity field<br>4. Select a valid Funding or Destination Account from the dropdown<br>5. Click the Execute Trade button | Trade executed successfully with an order ID displayed | Low |
| 10.INVEST-018 | Execute trade with Quantity just below minimum | User has sufficient buying power | 1. Select 'Buy' from the Action dropdown<br>2. Enter a valid Fund Symbol in the Fund Symbol field<br>3. Enter a Quantity of just below the minimum valid amount in the Quantity field<br>4. Select a valid Funding or Destination Account from the dropdown<br>5. Click the Execute Trade button | Validation error appears indicating Quantity must be greater than zero | Low |

---

### account_statements

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 11.ACCOUN-001 | Generate statement with valid period and account | None | 1. Select a valid statement period from the dropdown<br>2. Select a valid account from the account list<br>3. Click on the Generate Statement button | Statement generated successfully | High |
| 11.ACCOUN-002 | Verify statement generation button is displayed | None | 1. Check if the Generate Statement button is visible on the page | Generate Statement button is displayed | High |
| 11.ACCOUN-003 | Verify statement period dropdown is displayed | None | 1. Check if the statement period dropdown is visible on the page | Statement period dropdown is displayed | High |
| 11.ACCOUN-004 | Verify account selection dropdown is displayed | None | 1. Check if the account selection dropdown is visible on the page | Account selection dropdown is displayed | High |
| 11.ACCOUN-005 | Opt into paperless statements and save valid email preference | None | 1. Check the checkbox to opt into paperless statements<br>2. Enter a valid email address<br>3. Click the Save Preference button | e-Statement preference updated successfully | High |
| 11.ACCOUN-009 | Opt into paperless statements without checking the checkbox | None | 1. Leave the checkbox for paperless statements unchecked<br>2. Enter a valid email address<br>3. Click the Save Preference button | e-Statement preference updated successfully without opting into paperless statements | Medium |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 11.ACCOUN-006 | Generate statement with empty statement period | None | 1. Leave the statement period field empty<br>2. Select a valid account from the account list<br>3. Click on the Generate Statement button | Unable to generate statement — please try again later | High |
| 11.ACCOUN-007 | Generate statement with empty account selection | None | 1. Select a valid statement period from the dropdown<br>2. Leave the account selection empty<br>3. Click on the Generate Statement button | Unable to generate statement — please try again later | High |
| 11.ACCOUN-008 | Email field empty | None | 1. Check the checkbox to opt into paperless statements<br>2. Leave the email address field empty<br>3. Click the Save Preference button | Email field highlighted with guidance on failure | High |
| 11.ACCOUN-010 | Generate statement with invalid statement period | None | 1. Enter an invalid statement period<br>2. Select a valid account from the account list<br>3. Click on the Generate Statement button | Unable to generate statement — please try again later | Medium |
| 11.ACCOUN-011 | Generate statement with future statement period | None | 1. Select a future date as the statement period<br>2. Select a valid account from the account list<br>3. Click on the Generate Statement button | Unable to generate statement — please try again later | Medium |

---

### security_settings

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 12.SECURI-001 | Change password successfully with valid inputs | User is logged in and on the security settings page | 1. Enter a valid current password<br>2. Enter a valid new password that meets strong-password policy<br>3. Confirm the new password by entering it again<br>4. Click on the Change Password button | Password changed successfully message is displayed | High |
| 12.SECURI-007 | Verify fields are displayed correctly on the page | User is on the security settings page | 1. Check if Current Password field is displayed<br>2. Check if New Password field is displayed<br>3. Check if Confirm New Password field is displayed<br>4. Check if Change Password button is displayed | All fields and the Change Password button are displayed correctly | Low |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 12.SECURI-002 | Current Password field empty | User is on the security settings page | 1. Leave the Current Password field empty<br>2. Enter a valid new password that meets strong-password policy<br>3. Confirm the new password by entering it again<br>4. Click on the Change Password button | Validation error highlights the Current Password field | High |
| 12.SECURI-003 | New Password field empty | User is on the security settings page | 1. Enter a valid current password<br>2. Leave the New Password field empty<br>3. Confirm the new password by entering it again<br>4. Click on the Change Password button | Validation error highlights the New Password field | High |
| 12.SECURI-004 | Confirm New Password field empty | User is on the security settings page | 1. Enter a valid current password<br>2. Enter a valid new password that meets strong-password policy<br>3. Leave the Confirm New Password field empty<br>4. Click on the Change Password button | Validation error highlights the Confirm New Password field | High |
| 12.SECURI-005 | New Password and Confirm New Password do not match | User is on the security settings page | 1. Enter a valid current password<br>2. Enter a valid new password that meets strong-password policy<br>3. Enter a different password in the Confirm New Password field<br>4. Click on the Change Password button | Validation error indicates that New Password and Confirm New Password do not match | High |
| 12.SECURI-006 | New Password does not meet strong-password policy | User is on the security settings page | 1. Enter a valid current password<br>2. Enter a new password that does not meet strong-password policy<br>3. Confirm the new password by entering it again<br>4. Click on the Change Password button | Validation error indicates the New Password does not meet strong-password policy | Medium |

---

### support_center

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 13.SUPPOR-001 | Send secure message with valid subject and message body | None | 1. Enter a valid subject<br>2. Select a category<br>3. Enter a valid message body<br>4. Click the Send Message button | Shows 'Message sent successfully.' with a ticket ID | High |
| 13.SUPPOR-002 | Send secure message with valid subject, category, and message body but no attachment | None | 1. Enter a valid subject<br>2. Select a category<br>3. Enter a valid message body<br>4. Leave the attachment field empty<br>5. Click the Send Message button | Shows 'Message sent successfully.' with a ticket ID | High |
| 13.SUPPOR-003 | Request callback with valid inputs | None | 1. Enter a valid reason for the call<br>2. Select a preferred date that is at least the next business day<br>3. Select a preferred time window<br>4. Enter a valid phone number<br>5. Click the Request Callback button | Callback request submitted. | High |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 13.SUPPOR-004 | Subject field empty | None | 1. Leave the subject field empty<br>2. Select a category<br>3. Enter a valid message body<br>4. Click the Send Message button | Displays inline guidance indicating the subject is required | High |
| 13.SUPPOR-005 | Message body field empty | None | 1. Enter a valid subject<br>2. Select a category<br>3. Leave the message body field empty<br>4. Click the Send Message button | Displays inline guidance indicating the message body is required | High |
| 13.SUPPOR-006 | Preferred Date field empty | None | 1. Enter a valid reason for the call<br>2. Leave the preferred date field empty<br>3. Select a preferred time window<br>4. Enter a valid phone number<br>5. Click the Request Callback button | Shows validation error for Preferred Date field. | High |
| 13.SUPPOR-007 | Phone Number field empty | None | 1. Enter a valid reason for the call<br>2. Select a preferred date that is at least the next business day<br>3. Select a preferred time window<br>4. Leave the phone number field empty<br>5. Click the Request Callback button | Shows validation error for Phone Number field. | High |
| 13.SUPPOR-008 | Attachment type invalid | None | 1. Enter a valid subject<br>2. Select a category<br>3. Enter a valid message body<br>4. Attach an invalid file type<br>5. Click the Send Message button | Displays inline guidance indicating the attachment type is invalid | Medium |
| 13.SUPPOR-009 | Subject exceeds maximum length | None | 1. Enter a subject that exceeds the maximum length<br>2. Select a category<br>3. Enter a valid message body<br>4. Click the Send Message button | Displays inline guidance indicating the subject length must be checked | Medium |
| 13.SUPPOR-010 | Message body exceeds maximum length | None | 1. Enter a valid subject<br>2. Select a category<br>3. Enter a message body that exceeds the maximum length<br>4. Click the Send Message button | Displays inline guidance indicating the message body length must be checked | Medium |
| 13.SUPPOR-011 | Invalid Phone Number format | None | 1. Enter a valid reason for the call<br>2. Select a preferred date that is at least the next business day<br>3. Select a preferred time window<br>4. Enter an invalid phone number format<br>5. Click the Request Callback button | Shows validation error for Phone Number format. | Medium |
| 13.SUPPOR-012 | Preferred Date set to today | None | 1. Enter a valid reason for the call<br>2. Select today's date as preferred date<br>3. Select a preferred time window<br>4. Enter a valid phone number<br>5. Click the Request Callback button | Shows validation error for Preferred Date must be at least the next business day. | Medium |

#### Edge Case Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 13.SUPPOR-013 | Request callback with maximum length reason for call | None | 1. Enter a reason for the call that is at maximum allowed length<br>2. Select a preferred date that is at least the next business day<br>3. Select a preferred time window<br>4. Enter a valid phone number<br>5. Click the Request Callback button | Callback request submitted. | Low |
| 13.SUPPOR-014 | Request callback with just below maximum length reason for call | None | 1. Enter a reason for the call that is just below maximum allowed length<br>2. Select a preferred date that is at least the next business day<br>3. Select a preferred time window<br>4. Enter a valid phone number<br>5. Click the Request Callback button | Callback request submitted. | Low |

---

## Navigation Graph

### Pages

| Module | URL | Auth Required | Test Cases |
|--------|-----|---------------|------------|
| login | /login | No | 10 |
| register | /register | No | 20 |
| accounts_overview | /accounts-overview | Yes | 5 |
| open_new_account | /open-new-account | Yes | 11 |
| transfer_funds | /transfer-funds | Yes | 9 |
| payments | /bill-pay | Yes | 14 |
| request_loan | /request-loan | No | 9 |
| update_contact_info | /update-contact-info | Yes | 11 |
| manage_cards | /manage-cards | Yes | 12 |
| investments | /investments | Yes | 18 |
| account_statements | /account-statements | No | 11 |
| security_settings | /security-settings | Yes | 7 |
| support_center | /support-center | No | 14 |
