# Mifos Banking System Test Cases

**Website URL:** <http://localhost:4200>
**Test Suite Version:** 2.0 (Revised — optimised for generated-set coverage)

## Test Credentials

| Field | Value |
|-------|-------|
| Tenant | default |
| Username | mifos |
| Password | password |

---

## Table of Contents

1. [Login](#1-login)
2. [Home](#2-home)
3. [Dashboard](#3-dashboard)
4. [Global Search](#4-global-search)
5. [Client Management](#5-client-management)
6. [Group Management](#6-group-management)
7. [Center Management](#7-center-management)
8. [Loan Products](#8-loan-products)
9. [Savings Products](#9-savings-products)
10. [Charges](#10-charges)
11. [Loan Account](#11-loan-account)
12. [Savings Account](#12-savings-account)
13. [Accounting - Chart of Accounts](#13-accounting---chart-of-accounts)
14. [Accounting - Journal Entries](#14-accounting---journal-entries)
15. [Users & Roles](#15-users--roles)
16. [Offices](#16-offices)
17. [Employees](#17-employees)
18. [Reports](#18-reports)
19. [Organization Settings](#19-organization-settings)
20. [Share Products](#20-share-products)
21. [Floating Rates](#21-floating-rates)
22. [Delinquency Management](#22-delinquency-management)
23. [Share Account](#23-share-account)
24. [Fixed & Recurring Deposit Accounts](#24-fixed--recurring-deposit-accounts)
25. [Accounting - Closures](#25-accounting---closures)
26. [Accounting Rules & Financial Activity Mappings](#26-accounting-rules--financial-activity-mappings)
27. [Provisioning](#27-provisioning)
28. [Teller & Cashier Management](#28-teller--cashier-management)
29. [Account Transfers & Standing Instructions](#29-account-transfers--standing-instructions)
30. [Tax Management](#30-tax-management)
31. [System Administration](#31-system-administration)
32. [Logout](#32-logout)

---

## 1. Login

### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MF-LOGIN-001 | Valid login with correct credentials | Mifos instance running | 1. Navigate to login page<br>2. Enter "default" as Tenant<br>3. Enter "mifos" as Username<br>4. Enter "password" as Password<br>5. Click "Login" | User is redirected to Home page, toolbar shows username | High |
| MF-LOGIN-002 | Login page elements displayed | None | 1. Navigate to login page | Tenant Identifier field, Username field, Password field, and Login button are visible with application branding | Medium |

### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MF-LOGIN-005 | Invalid username | None | 1. Enter valid tenant<br>2. Enter invalid username<br>3. Enter any password<br>4. Click "Login" | Error message for invalid authentication is displayed | High |
| MF-LOGIN-006 | Invalid password | None | 1. Enter valid tenant<br>2. Enter "mifos" as username<br>3. Enter incorrect password<br>4. Click "Login" | Error message displayed, user remains on login page | High |
| MF-LOGIN-007 | Empty username | None | 1. Enter valid tenant<br>2. Leave username empty<br>3. Enter password<br>4. Click "Login" | Inline validation error shown for username | High |
| MF-LOGIN-008 | Empty password | None | 1. Enter valid tenant<br>2. Enter username<br>3. Leave password empty<br>4. Click "Login" | Inline validation error shown for password | High |
| MF-LOGIN-009 | Both fields empty | None | 1. Leave Username and Password empty<br>2. Click "Login" | Validation errors shown for all mandatory fields | Medium |

### Boundary Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MF-LOGIN-015 | Login using Enter key | None | 1. Enter valid Tenant, Username, and Password<br>2. Press Enter in Password field | Login is submitted and user is redirected on success | Medium |
| MF-LOGIN-017 | Direct access to login page after authenticated session | User already logged in | 1. Login successfully<br>2. Navigate again to login URL | User is redirected to Home page or active session is preserved | Medium |

### Additional Coverage Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MF-LOGIN-020 | Session persists on page refresh after successful login | User logged in | 1. Login successfully<br>2. Refresh browser tab | User remains authenticated and current page reloads successfully | High |
| MF-LOGIN-021 | Direct navigation to login page while authenticated | User already logged in | 1. Enter login page URL manually | User is redirected to Home page or duplicate login form usage is prevented | Medium |
| MF-LOGIN-022 | Logout invalidates session token for subsequent protected requests | User logged in | 1. Login successfully<br>2. Logout<br>3. Navigate to protected route or call protected API | Request is rejected and user is returned to login page | High |

---

## 2. Home

### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MF-HOME-001 | User lands on Home page after successful login | Valid user credentials | 1. Login with valid tenant, username, and password | Home page is displayed as the first authenticated page | High |
| MF-HOME-002 | Home page widgets and navigation tiles load successfully | User logged in | 1. Login<br>2. Observe Home page | Home page loads without blank state or route error and shows configured landing content/cards/navigation elements | High |
| MF-HOME-003 | Top toolbar is visible on Home page | User logged in | 1. Login<br>2. Observe top header area | Toolbar displays application header, global search access, profile/user menu, and other permitted header actions | High |
| MF-HOME-005 | Home page route is accessible directly after authentication | User logged in | 1. Login<br>2. Enter Home route URL directly | Home page opens successfully without redirect loop | Medium |
| MF-HOME-006 | Home page navigation to Dashboard | User logged in, user has dashboard permission | 1. Open Home page<br>2. Click Dashboard navigation entry | Dashboard page opens successfully | High |

---

## 3. Dashboard

### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MF-DASH-001 | Dashboard loads from Home page | User logged in | 1. Login with valid credentials<br>2. From Home page click Dashboard | Dashboard page displayed with summary cards for total clients, active loans, pending approvals, portfolio at risk | High |
| MF-DASH-002 | Summary cards display metrics | User logged in, data exists | 1. Navigate to Dashboard | Summary cards show correct counts for clients, loans, approvals | High |

### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MF-DASH-005 | Dashboard with no data | Fresh instance, no clients/loans | 1. Login and open Dashboard from Home | Dashboard shows zero counts or empty state appropriately | Medium |
| MF-DASH-006 | Dashboard refresh after transaction | User logged in, data exists | 1. View dashboard metrics<br>2. Create a client or post a repayment<br>3. Refresh dashboard | Summary metrics reflect latest committed data | Medium |
| MF-DASH-007 | Navigate from dashboard quick links | User logged in | 1. Click each quick action on Dashboard | Each action opens the corresponding create or transaction page | Medium |

---

## 4. Global Search

### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MF-SEARCH-001 | Global search bar visible in toolbar | User logged in | 1. Observe top toolbar/header | Search input is visible and accessible from authenticated pages | High |
| MF-SEARCH-002 | Search active client by name | Active client exists | 1. Enter full or partial client name in global search<br>2. Submit search | Matching client appears in results with link to client detail page | High |
| MF-SEARCH-003 | Search loan account by account number | Loan account exists | 1. Enter exact loan account number<br>2. Submit | Matching loan account appears in results and opens loan detail page when selected | High |
| MF-SEARCH-004 | Search savings account by account number | Savings account exists | 1. Enter exact savings account number<br>2. Submit | Matching savings account appears in results and opens savings detail page when selected | High |

### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MF-SEARCH-009 | Search non-existent term | User logged in | 1. Enter random string not mapped to any entity<br>2. Submit | "No results found" or equivalent empty-state message displayed | Medium |
| MF-SEARCH-010 | Empty search submission | User logged in | 1. Leave search input empty<br>2. Submit | Search is not executed or empty-state guidance is shown without error | Low |

### Boundary Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MF-SEARCH-013 | Partial prefix match | Multiple entities with similar prefixes exist | 1. Enter partial prefix of entity name | Relevant matching results are returned according to supported search behavior | Medium |
| MF-SEARCH-014 | Exact account number match preferred over loose text match | Entity with exact account number and similar text entities exist | 1. Search exact account number | Exact account result appears clearly and opens correct detail page | Medium |

### Additional Coverage Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MF-SEARCH-016 | Search result click navigates to correct entity detail page | Searchable entity exists | 1. Run search<br>2. Click matching result | Correct entity profile/account page opens | High |
| MF-SEARCH-017 | Search supports case-insensitive text matching | Searchable entity exists | 1. Search using different case variation | Matching entity is returned regardless of letter case | Medium |
| MF-SEARCH-018 | Search results update correctly across entity types for same term | Client/group/center with similar names exist | 1. Search shared term | Results include all authorized matching entity types without duplication | Medium |

---

## 5. Client Management

### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MF-CLIENT-001 | View clients list | User logged in | 1. Click "Clients" in sidebar | Client list page displays table with columns: Name, Account No., External ID, Status, Office, Staff | High |
| MF-CLIENT-002 | Create new client successfully | At least one office exists | 1. Click "+" on Clients page<br>2. Select Office<br>3. Enter First Name and Last Name<br>4. Set Submitted On date<br>5. Click "Submit" | New client created and appears in client list with Pending status | High |
| MF-CLIENT-003 | Activate pending client | Client in Pending status | 1. Open client detail page<br>2. Click "Activate"<br>3. Set Activation Date<br>4. Submit | Client status changes to "Active" (green chip) | High |
| MF-CLIENT-004 | Client detail page elements | Active client exists | 1. Click client name in list | Header shows full name, account number, status badge, activation date, office. Tabs: General, Accounts, Identifiers, Family Members, Notes, Documents | High |
| MF-CLIENT-005 | Filter clients by status | Multiple clients exist | 1. Use filter bar to select status "Active" | Only active clients displayed in table | Medium |
| MF-CLIENT-006 | Search clients by name | Multiple clients exist | 1. Type name in search bar on Clients page | Table filters to matching clients | Medium |
| MF-CLIENT-007 | Transfer client | Active client exists, multiple offices | 1. Open client detail<br>2. Click "Transfer Client"<br>3. Select destination office<br>4. Submit | Client transferred to new office | Medium |
| MF-CLIENT-008 | Close client | Active client, no active accounts | 1. Open client detail<br>2. Click "Close"<br>3. Provide closure reason<br>4. Submit | Client status changes to "Closed" (gray chip) | Medium |
| MF-CLIENT-009 | Add client identifier | Active client exists | 1. Go to Identifiers tab<br>2. Add Document Type (National ID), Document Key<br>3. Submit | Identifier added and visible in list | Medium |
| MF-CLIENT-010 | Add client note | Active client exists | 1. Go to Notes tab<br>2. Click "Add Note"<br>3. Enter note text<br>4. Submit | Note appears in chronological list | Low |
| MF-CLIENT-011 | Pagination on clients list | Many clients exist | 1. View Clients page<br>2. Navigate pages | Pagination controls work correctly, showing total count and page navigation | Medium |

### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MF-CLIENT-012 | Create client without Office | None | 1. Open Create Client form<br>2. Fill name fields but leave Office empty<br>3. Submit | Validation error "Office is required" | High |
| MF-CLIENT-013 | Create client without First Name | None | 1. Open Create Client form<br>2. Leave First Name empty<br>3. Fill other required fields<br>4. Submit | Validation error "First name is required" | High |
| MF-CLIENT-014 | Create client without Last Name | None | 1. Open Create Client form<br>2. Leave Last Name empty<br>3. Fill other required fields<br>4. Submit | Validation error "Last name is required" | High |
| MF-CLIENT-015 | Close client with active accounts | Client has active loan/savings | 1. Try to close client | Error: cannot close client with active accounts | High |
| MF-CLIENT-016 | Edit client profile details | Active client exists | 1. Open client detail<br>2. Click Edit<br>3. Update fields such as mobile number or external ID<br>4. Submit | Updated values are saved and displayed on client profile | Medium |
| MF-CLIENT-017 | Add family member to client | Active client exists | 1. Open Family Members tab<br>2. Click Add<br>3. Enter relationship and basic details<br>4. Submit | Family member is added to the list | Medium |
| MF-CLIENT-018 | Upload client document | Active client exists | 1. Open Documents tab<br>2. Upload a valid file with description<br>3. Submit | Document is uploaded and listed under client documents | Medium |
| MF-CLIENT-019 | Search clients by account number | Multiple clients exist | 1. Enter client account number in list search | Matching client row is returned | Medium |
| MF-CLIENT-020 | Activate client with activation date before submission date | Pending client exists | 1. Open Activate dialog<br>2. Enter date earlier than Submitted On date<br>3. Submit | Validation error or business rule prevents activation | High |
| MF-CLIENT-021 | Duplicate identifier for same client document type | Active client with identifier exists | 1. Add another identifier with same document type and key where uniqueness is enforced<br>2. Submit | Validation or server error prevents duplicate identifier | Medium |
| MF-CLIENT-022 | Transfer client to same office | Active client exists | 1. Click Transfer Client<br>2. Select current office<br>3. Submit | Validation blocks no-op transfer or system handles without duplicate history | Low |
| MF-CLIENT-023 | Close client without closure reason | Active client with no active accounts | 1. Click Close<br>2. Leave reason empty<br>3. Submit | Validation error shown for closure reason | High |

### Additional Coverage Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MF-CLIENT-024 | Reject pending client | Pending client exists | 1. Open client detail<br>2. Click Reject<br>3. Enter rejection date/reason<br>4. Submit | Client status changes to Rejected and no activation actions remain available | High |
| MF-CLIENT-025 | Withdraw pending client application | Pending client exists | 1. Open client detail<br>2. Click Withdraw<br>3. Enter withdrawal reason/date<br>4. Submit | Client status changes to Withdrawn | Medium |
| MF-CLIENT-026 | Reactivate closed client when business rules allow | Closed client exists and reactivation allowed | 1. Open client detail<br>2. Click Reactivate<br>3. Submit | Client returns to Active state with audit history preserved | Medium |
| MF-CLIENT-027 | Assign staff to client | Active client and staff record exist | 1. Edit client<br>2. Select staff member<br>3. Submit | Staff assignment is saved and shown on client profile/list | Medium |
| MF-CLIENT-028 | Client charges tab supports add charge action | Active client exists and charge definition exists | 1. Open client detail<br>2. Add charge<br>3. Submit | Charge appears under client-related charges and is available for collection workflow | Medium |
| MF-CLIENT-029 | Duplicate client creation with same external ID | External ID uniqueness enforced | 1. Create client with already-used external ID<br>2. Submit | Validation or server-side error prevents duplicate external ID | High |

---

## 6. Group Management

### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MF-GROUP-001 | View groups list | User logged in | 1. Navigate to Groups page | Groups list loads with group name, account number, office, staff, and status | High |
| MF-GROUP-002 | Create group successfully | Office exists | 1. Click Create Group<br>2. Select office<br>3. Enter group name<br>4. Set submitted date<br>5. Submit | Group is created in pending status | High |
| MF-GROUP-003 | Activate group | Pending group exists | 1. Open group detail<br>2. Click Activate<br>3. Set activation date<br>4. Submit | Group status changes to Active | High |
| MF-GROUP-004 | View group details | Group exists | 1. Open a group record | Group profile displays general details, members, accounts, notes, and actions | High |
| MF-GROUP-005 | Add client members to group | Active group and active clients exist | 1. Open group<br>2. Add members<br>3. Select eligible clients<br>4. Submit | Selected clients become group members | High |
| MF-GROUP-006 | Assign staff to group | Group and staff exist | 1. Edit group<br>2. Select staff member<br>3. Submit | Staff assignment is saved | Medium |
| MF-GROUP-007 | Transfer group to another office | Active group and destination office exist | 1. Open group<br>2. Click Transfer<br>3. Select office<br>4. Submit | Group office is updated successfully | Medium |
| MF-GROUP-008 | Close group | Group has no blocking active constraints | 1. Open active group<br>2. Click Close<br>3. Provide closure details<br>4. Submit | Group status changes to Closed | Medium |

### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MF-GROUP-009 | Create group without office | None | 1. Open Create Group form<br>2. Leave office empty<br>3. Enter other fields<br>4. Submit | Validation error is shown for office | High |
| MF-GROUP-010 | Create group without group name | None | 1. Open Create Group form<br>2. Leave group name empty<br>3. Submit | Validation error is shown for group name | High |
| MF-GROUP-011 | Activate group with invalid activation date | Pending group exists | 1. Activate group<br>2. Enter date before submission date<br>3. Submit | Validation or business rule prevents activation | High |
| MF-GROUP-012 | Add ineligible client to group | Client not eligible due to status/office constraints | 1. Add member to group<br>2. Select ineligible client | Selection is blocked or submission fails with proper message | Medium |
| MF-GROUP-013 | Close group with active dependent accounts blocking closure | Group has active dependent accounts | 1. Attempt close action | Closure is prevented with business-rule error | High |

### Additional Coverage Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MF-GROUP-014 | Search groups by name | Groups exist | 1. Search on Groups page using partial name | Matching groups are returned | Medium |
| MF-GROUP-015 | Remove member from group | Active group with members exists | 1. Open group members tab<br>2. Remove member<br>3. Submit | Member is removed according to business rules | Medium |
| MF-GROUP-016 | Reject pending group application | Pending group exists | 1. Open group<br>2. Click Reject<br>3. Submit | Group status changes to Rejected | Medium |
| MF-GROUP-017 | Withdraw pending group application | Pending group exists | 1. Open group<br>2. Click Withdraw<br>3. Submit | Group status changes to Withdrawn | Medium |
| MF-GROUP-018 | Group notes can be added and displayed chronologically | Group exists | 1. Add note to group | Note is persisted and displayed in notes section | Low |

---

## 7. Center Management

### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MF-CENTER-001 | View centers list | User logged in | 1. Navigate to Centers page | Centers list loads with center information | High |
| MF-CENTER-002 | Create center successfully | Office exists | 1. Click Create Center<br>2. Select office<br>3. Enter center name<br>4. Set submission data<br>5. Submit | Center is created in pending state | High |
| MF-CENTER-003 | Activate center | Pending center exists | 1. Open center detail<br>2. Click Activate<br>3. Enter activation date<br>4. Submit | Center becomes Active | High |
| MF-CENTER-004 | View center detail | Center exists | 1. Open center | Center profile shows details, groups, staff, and actions | High |
| MF-CENTER-005 | Add groups to center | Active center and eligible groups exist | 1. Open center<br>2. Add groups<br>3. Select groups<br>4. Submit | Groups are associated with the center | Medium |
| MF-CENTER-006 | Assign staff to center | Center and staff exist | 1. Edit center<br>2. Select staff<br>3. Submit | Staff assignment is saved | Medium |
| MF-CENTER-007 | Transfer center | Active center and destination office exist | 1. Open center<br>2. Click Transfer<br>3. Select destination office<br>4. Submit | Center is transferred successfully | Medium |
| MF-CENTER-008 | Close center | Center eligible for closure | 1. Open center<br>2. Click Close<br>3. Submit with closure details | Center status changes to Closed | Medium |

### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MF-CENTER-009 | Create center without office | None | 1. Leave office empty in create form<br>2. Submit | Validation error shown for office | High |
| MF-CENTER-010 | Create center without center name | None | 1. Leave name empty<br>2. Submit | Validation error shown for center name | High |
| MF-CENTER-011 | Activate center using date before submission date | Pending center exists | 1. Enter invalid activation date<br>2. Submit | Activation is prevented | High |
| MF-CENTER-012 | Add ineligible group to center | Group does not meet eligibility rules | 1. Add group to center<br>2. Select ineligible group | Operation is blocked or fails with proper message | Medium |
| MF-CENTER-013 | Close center with active dependencies | Center has active linked entities blocking closure | 1. Attempt closure | Closure is rejected by business rule | High |

### Additional Coverage Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MF-CENTER-014 | Search centers by name | Centers exist | 1. Search centers page | Matching centers are listed | Medium |
| MF-CENTER-015 | Reject pending center application | Pending center exists | 1. Open center<br>2. Reject application | Center status changes to Rejected | Medium |
| MF-CENTER-016 | Withdraw pending center application | Pending center exists | 1. Open center<br>2. Withdraw application | Center status changes to Withdrawn | Medium |
| MF-CENTER-017 | Remove group from center | Active center with linked groups exists | 1. Open center<br>2. Remove linked group<br>3. Submit | Group is removed according to business rules | Medium |
| MF-CENTER-018 | Add center notes | Center exists | 1. Open notes section<br>2. Add note | Note is saved and displayed | Low |

---

## 8. Loan Products

### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MF-LPROD-001 | View loan products list | User logged in with permission | 1. Navigate to Loan Products | Loan products list displays available products and status | High |
| MF-LPROD-002 | Create loan product successfully | Required accounting setup exists | 1. Click Create Loan Product<br>2. Fill mandatory details including name, short name, fund, currency, principal, interest, repayment settings, accounting mappings<br>3. Submit | Loan product is created and visible in list | High |
| MF-LPROD-003 | View loan product detail | Loan product exists | 1. Open product record | Product detail shows terms, charges, accounting, and configuration tabs/sections | High |
| MF-LPROD-004 | Edit loan product | Loan product exists and is editable | 1. Open product<br>2. Click Edit<br>3. Update editable fields<br>4. Submit | Product updates are saved successfully | High |
| MF-LPROD-005 | Create declining balance loan product | Required accounting setup exists | 1. Create product with declining balance interest method | Product saves with correct calculation configuration | High |
| MF-LPROD-006 | Create flat interest loan product | Required accounting setup exists | 1. Create product with flat interest method | Product saves with flat interest configuration | High |
| MF-LPROD-007 | Configure loan product charges | Charge definitions exist | 1. Add charges while creating/editing product | Product stores configured charges correctly | Medium |
| MF-LPROD-008 | Configure accounting mappings for loan product | GL accounts exist | 1. Define asset, income, expense, liability mappings<br>2. Submit | Product accounting configuration is saved | High |

### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MF-LPROD-011 | Create product without product name | None | 1. Leave product name empty<br>2. Fill other fields<br>3. Submit | Validation error shown for product name | High |
| MF-LPROD-012 | Create product without short name | None | 1. Leave short name empty<br>2. Submit | Validation error shown for short name | High |
| MF-LPROD-013 | Create product with principal min greater than principal max | None | 1. Enter invalid min/max principal range<br>2. Submit | Validation error prevents save | High |
| MF-LPROD-014 | Create product with interest rate min greater than max | None | 1. Enter invalid interest rate range<br>2. Submit | Validation error prevents save | High |
| MF-LPROD-015 | Create product with missing mandatory accounting mappings when accounting is enabled | GL accounts incomplete | 1. Select accounting rule requiring mappings<br>2. Omit mandatory GL values<br>3. Submit | Validation error shown and save blocked | High |
| MF-LPROD-017 | Invalid repayment frequency values | None | 1. Enter zero or invalid repayment frequency<br>2. Submit | Validation blocks invalid repayment setup | High |

---

## 9. Savings Products

### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MF-SPROD-001 | View savings products list | User logged in with permission | 1. Navigate to Savings Products | Savings product list displays configured products and status | High |
| MF-SPROD-002 | Create savings product successfully | Required accounting setup exists | 1. Click Create Savings Product<br>2. Fill mandatory product details, interest settings, withdrawal rules, accounting mappings<br>3. Submit | Savings product is created successfully | High |
| MF-SPROD-003 | View savings product details | Savings product exists | 1. Open product | Product details show terms, interest settings, fees/charges, and accounting mappings | High |
| MF-SPROD-004 | Edit savings product | Savings product exists | 1. Open product<br>2. Click Edit<br>3. Update allowed fields<br>4. Submit | Changes are saved successfully | High |
| MF-SPROD-005 | Configure interest-bearing savings product | Required setup exists | 1. Create product with interest calculation and posting rules | Product stores interest settings correctly | High |
| MF-SPROD-006 | Configure overdraft-enabled savings product | Feature supported | 1. Enable overdraft settings during product creation<br>2. Save | Product is created with overdraft rules | Medium |
| MF-SPROD-007 | Configure withdrawal fee or charge on savings product | Charges exist | 1. Link charge(s) to product<br>2. Save | Product stores linked charge configuration | Medium |
| MF-SPROD-008 | Configure accounting mappings for savings product | GL accounts exist | 1. Set liability, expense, income, and overdraft-related mappings<br>2. Submit | Accounting setup is saved successfully | High |
| MF-SPROD-009 | Create zero-interest savings product | Required setup exists | 1. Create product with no interest | Product is saved successfully with non-interest-bearing behavior | Medium |

### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MF-SPROD-010 | Create product without name | None | 1. Leave product name empty<br>2. Submit | Validation error shown for product name | High |
| MF-SPROD-011 | Create product without short name | None | 1. Leave short name empty<br>2. Submit | Validation error shown for short name | High |
| MF-SPROD-012 | Create product with minimum balance greater than allowed threshold or conflicting limits | None | 1. Enter invalid balance rule combination<br>2. Submit | Validation error prevents save | High |
| MF-SPROD-013 | Create product with missing accounting mappings when accounting rule requires them | GL mappings incomplete | 1. Select accounting option requiring mappings<br>2. Omit mandatory fields<br>3. Submit | Validation blocks save | High |
| MF-SPROD-014 | Duplicate savings product short name | Existing short name exists | 1. Create another product with same short name | Validation or server error prevents duplicate | Medium |
| MF-SPROD-015 | Invalid interest rate configuration | None | 1. Enter invalid rate/frequency combination<br>2. Submit | Validation error shown | High |

---

## 10. Charges

### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MF-CHARGE-001 | View charges list | User logged in with permission | 1. Navigate to Charges | Charges list displays configured charge definitions | High |
| MF-CHARGE-002 | Create flat charge successfully | None | 1. Click Create Charge<br>2. Enter name, currency, flat amount, applicable time/type and target entity<br>3. Submit | Charge is created successfully | High |
| MF-CHARGE-003 | Create percentage-based charge successfully | None | 1. Create charge with percentage amount and valid basis | Charge is created successfully with percentage configuration | High |
| MF-CHARGE-004 | Edit charge definition | Existing charge exists and is editable | 1. Open charge<br>2. Click Edit<br>3. Update allowed fields<br>4. Submit | Updated values are saved | High |
| MF-CHARGE-005 | Create loan disbursement charge | Loan charge applicability supported | 1. Create charge applicable to loans at disbursement | Charge is available for relevant loan product/account workflows | High |
| MF-CHARGE-006 | Create savings withdrawal charge | Savings applicability supported | 1. Create charge applicable to savings withdrawals | Charge can be linked to savings products/accounts | Medium |
| MF-CHARGE-007 | Create client-level charge | Client charges supported | 1. Create charge applicable to clients | Charge is available for client charge assignment | Medium |
| MF-CHARGE-008 | View charge details | Charge exists | 1. Open charge record | Detail page shows amount, type, applicability, and timing | Medium |

### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MF-CHARGE-009 | Create charge without name | None | 1. Leave name empty<br>2. Submit | Validation error shown for charge name | High |
| MF-CHARGE-010 | Create charge without amount or percentage | None | 1. Omit required amount field<br>2. Submit | Validation error prevents save | High |
| MF-CHARGE-011 | Create percentage charge above supported limit | None | 1. Enter invalid percentage value<br>2. Submit | Validation error shown | High |
| MF-CHARGE-012 | Create charge with incompatible applicability/time combination | None | 1. Choose invalid target entity and event timing combination<br>2. Submit | Validation or business rule prevents save | Medium |

### Additional Coverage Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MF-CHARGE-014 | Inactivate charge definition | Charge exists and can be disabled | 1. Open charge<br>2. Disable or inactivate | Charge is unavailable for future assignments while historical usage remains intact | Medium |
| MF-CHARGE-015 | Charge linked to product appears during account lifecycle | Product linked to charge exists | 1. Create account from linked product<br>2. Trigger relevant event | Charge is assessed according to configuration | High |
| MF-CHARGE-016 | Charge collected from account updates accounting and balance correctly | Charge applied to active account | 1. Collect due charge | Charge balance reduces and transaction entries are posted correctly | High |
| MF-CHARGE-017 | Waive charge from applicable account | Applied charge exists | 1. Open charge on account<br>2. Waive charge | Charge outstanding amount is reduced according to waived amount | Medium |

---

## 11. Loan Account

### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MF-LOAN-001 | Create new loan application for client | Active client and loan product exist | 1. Open client profile<br>2. Click New Loan<br>3. Select product<br>4. Enter principal, term, interest, disbursement/submission data<br>5. Submit | Loan account is created in Submitted and Pending Approval state | High |
| MF-LOAN-002 | Approve loan application | Pending approval loan exists | 1. Open loan account<br>2. Click Approve<br>3. Enter approval details<br>4. Submit | Loan moves to Approved state | High |
| MF-LOAN-003 | Disburse approved loan | Approved loan exists | 1. Open approved loan<br>2. Click Disburse<br>3. Enter disbursement date and amount<br>4. Submit | Loan becomes Active and disbursement transaction is recorded | High |
| MF-LOAN-004 | View repayment schedule | Loan exists | 1. Open loan account | Repayment schedule is displayed with installments, principal, interest, fees, and balances | High |
| MF-LOAN-005 | Make repayment | Active loan with amount due exists | 1. Open loan<br>2. Click Repayment<br>3. Enter transaction date and amount<br>4. Submit | Repayment is posted and outstanding balances are updated | High |
| MF-LOAN-006 | Undo repayment or reverse transaction where supported | Loan repayment exists and user has permission | 1. Open repayment transaction<br>2. Reverse or undo | Transaction is reversed according to business rules and balances are recalculated | Medium |
| MF-LOAN-007 | View loan transactions | Loan with transactions exists | 1. Open loan transactions tab/section | Full transaction history is displayed | High |
| MF-LOAN-008 | Add loan charge | Loan exists and charge definition exists | 1. Open loan<br>2. Add charge<br>3. Submit | Charge is added to the loan account | Medium |
| MF-LOAN-009 | Waive loan charge | Loan charge exists | 1. Open loan charge<br>2. Waive charge | Charge amount is reduced appropriately | Medium |
| MF-LOAN-010 | Reschedule loan where supported | Loan eligible for rescheduling | 1. Open loan<br>2. Start reschedule workflow<br>3. Submit new schedule details | Loan repayment schedule is updated after approval/process completion | Medium |
| MF-LOAN-011 | Multi-disbursement loan additional tranche disbursement | Active multi-disbursement loan exists | 1. Open loan<br>2. Disburse next tranche<br>3. Submit | Additional disbursement is recorded and schedule/balance updated | Medium |
| MF-LOAN-012 | Foreclosure or close loan as closed obligations met | Active loan eligible for closure | 1. Open loan<br>2. Complete closure action | Loan reaches appropriate closed status | High |
| MF-LOAN-013 | Loan write-off | Delinquent loan eligible for write-off | 1. Open loan<br>2. Click Write Off<br>3. Enter date<br>4. Submit | Loan status changes to written-off and accounting entries are posted | High |

### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MF-LOAN-014 | Submit loan without mandatory product | Active client exists | 1. Start loan application<br>2. Omit product selection<br>3. Submit | Validation error shown | High |
| MF-LOAN-015 | Approve loan with approval date before submission date | Pending loan exists | 1. Approve loan with invalid date<br>2. Submit | Validation or business rule prevents approval | High |
| MF-LOAN-016 | Disburse loan with date before approval date | Approved loan exists | 1. Disburse using invalid date | Validation prevents disbursement | High |
| MF-LOAN-017 | Repayment amount invalid or negative | Active loan exists | 1. Enter zero or negative repayment amount<br>2. Submit | Validation error shown | High |
| MF-LOAN-018 | Repayment on non-active loan | Loan not in active state | 1. Attempt repayment | Action is blocked | High |
| MF-LOAN-019 | Disbursement amount above approved amount when not allowed | Approved loan exists | 1. Enter excessive disbursement amount<br>2. Submit | Business rule prevents invalid disbursement | High |
| MF-LOAN-021 | Add invalid charge to loan | Inapplicable charge selected | 1. Add incompatible charge<br>2. Submit | Validation or business rule prevents assignment | Medium |

### Additional Coverage Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MF-LOAN-022 | Reject loan application | Pending approval loan exists | 1. Open loan<br>2. Reject application<br>3. Submit | Loan status changes to Rejected | High |
| MF-LOAN-023 | Withdraw loan application before approval | Submitted loan exists | 1. Open loan<br>2. Withdraw application<br>3. Submit | Loan status changes to Withdrawn by client/officer as supported | Medium |
| MF-LOAN-024 | Undo approval of loan where supported | Approved loan not yet disbursed | 1. Open approved loan<br>2. Undo approval | Loan returns to prior workflow state | Medium |
| MF-LOAN-025 | Apply payment allocation rules correctly for mixed due amounts | Active loan with principal, interest, fees, penalties due | 1. Make repayment | Amount is allocated according to configured repayment strategy | High |
| MF-LOAN-026 | Post penalty on overdue installment | Active delinquent loan and penalty charge exist | 1. Add penalty or allow scheduled assessment | Penalty transaction is created correctly | Medium |
| MF-LOAN-027 | Loan schedule recalculates after transaction reversal | Loan with repayment reversal exists | 1. Reverse repayment | Outstanding balances and schedule-derived figures are recalculated consistently | High |
| MF-LOAN-028 | Overpayment handling on loan | Loan allows overpayment or prepayment | 1. Make repayment above due amount | Excess amount is handled according to business rules without corruption | Medium |
| MF-LOAN-029 | Loan notes and documents can be added | Loan exists | 1. Add note or upload document | Supporting artifacts are stored and visible on loan profile | Low |
| MF-LOAN-030 | Loan guarantor or collateral tab accessible where feature is enabled | Feature enabled and loan exists | 1. Open relevant tab | Guarantor/collateral workflows are available and functional | Low |

---

## 12. Savings Account

### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MF-SAV-001 | Create savings account for client | Active client and savings product exist | 1. Open client profile<br>2. Click New Savings Account<br>3. Select product<br>4. Fill required fields<br>5. Submit | Savings account is created in submitted/pending state | High |
| MF-SAV-002 | Approve savings account | Pending savings account exists | 1. Open account<br>2. Click Approve<br>3. Submit | Savings account moves to approved state | High |
| MF-SAV-003 | Activate savings account | Approved savings account exists | 1. Open account<br>2. Click Activate<br>3. Enter activation date<br>4. Submit | Savings account becomes Active | High |
| MF-SAV-004 | Deposit into active savings account | Active savings account exists | 1. Open account<br>2. Click Deposit<br>3. Enter amount and date<br>4. Submit | Deposit transaction is posted and balance increases | High |
| MF-SAV-005 | Withdraw from active savings account | Active savings account with sufficient balance or allowed overdraft exists | 1. Open account<br>2. Click Withdraw<br>3. Enter amount and date<br>4. Submit | Withdrawal transaction is posted and balance decreases | High |
| MF-SAV-006 | View savings transactions | Savings account with transactions exists | 1. Open transactions section | Transaction history is displayed correctly | High |
| MF-SAV-007 | Post interest to savings account | Interest-bearing savings account exists and posting is due | 1. Run posting event or inspect posted account | Interest posting appears correctly in transactions/balance | Medium |
| MF-SAV-008 | Add charge to savings account | Active account and charge exist | 1. Open account<br>2. Add charge<br>3. Submit | Charge is added to the savings account | Medium |
| MF-SAV-009 | Close savings account | Active savings account eligible for closure | 1. Open account<br>2. Click Close<br>3. Submit closure details | Account status changes to Closed | High |
| MF-SAV-010 | Reactivate or reopen eligible savings account where supported | Closed account and business rule allow | 1. Open account<br>2. Use reactivation action | Account returns to active workflow as supported | Low |

### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MF-SAV-011 | Create savings account without product | Active client exists | 1. Start application<br>2. Omit product<br>3. Submit | Validation error shown | High |
| MF-SAV-012 | Activate with invalid date sequence | Approved account exists | 1. Activate using date before submission/approval | Validation prevents activation | High |
| MF-SAV-013 | Withdraw more than available balance when overdraft not allowed | Active account exists | 1. Attempt excessive withdrawal | Transaction is blocked with appropriate message | High |
| MF-SAV-014 | Deposit negative or zero amount | Active account exists | 1. Enter invalid deposit amount<br>2. Submit | Validation error shown | High |
| MF-SAV-015 | Withdraw on non-active account | Account not active | 1. Attempt withdrawal | Action is blocked | High |
| MF-SAV-016 | Close savings account with blocked pending conditions | Account has holds or constraints | 1. Attempt closure | Business rule prevents closure | Medium |

### Additional Coverage Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MF-SAV-017 | Reject savings account application | Pending account exists | 1. Open account<br>2. Reject application<br>3. Submit | Account status changes to Rejected | Medium |
| MF-SAV-018 | Undo approval of savings account before activation where supported | Approved account exists | 1. Open approved account<br>2. Undo approval | Account returns to previous state | Low |
| MF-SAV-019 | Waive savings account charge | Charge exists on account | 1. Open charge<br>2. Waive | Outstanding charge is reduced correctly | Medium |
| MF-SAV-020 | Overdraft-enabled account allows negative balance within configured limit | Active overdraft-enabled account exists | 1. Withdraw amount exceeding current positive balance but within overdraft limit | Withdrawal succeeds and resulting balance respects configured overdraft rules | Medium |
| MF-SAV-021 | Savings notes and documents can be maintained | Savings account exists | 1. Add note/upload document | Records are saved and visible | Low |
| MF-SAV-022 | Interest recalculation after backdated transaction is handled correctly | Interest-bearing account with backdated txn support | 1. Post backdated transaction<br>2. Trigger recalculation/posting | Interest outcomes remain consistent with product rules | Medium |

---

## 13. Accounting - Chart of Accounts

### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MF-COA-001 | View chart of accounts | User with accounting permission | 1. Navigate to Chart of Accounts | GL accounts tree/list is displayed grouped by account type | High |
| MF-COA-002 | Create header account | Accounting access available | 1. Create new GL account as header<br>2. Submit | Header account is created successfully | High |
| MF-COA-003 | Create non-header account | Parent/header account exists where needed | 1. Create new GL account with type, usage, classification<br>2. Submit | GL account is created and visible in chart | High |
| MF-COA-004 | Edit GL account | Editable GL account exists | 1. Open GL account<br>2. Edit details<br>3. Submit | Changes are saved successfully | High |
| MF-COA-005 | Disable or close GL account | Eligible account exists | 1. Open account<br>2. Disable/close | Account status changes and account is unavailable for future use as configured | Medium |
| MF-COA-006 | View GL account usage details | GL account exists | 1. Open GL account detail | Details show account classification, usage type, and relationships | Medium |

### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MF-COA-007 | Create GL account without name | None | 1. Leave name empty<br>2. Submit | Validation error shown | High |
| MF-COA-008 | Create GL account without account type | None | 1. Omit account type/classification<br>2. Submit | Validation error shown | High |
| MF-COA-009 | Duplicate GL account code | Existing code exists | 1. Create another GL account using same code | Validation or server-side uniqueness error occurs | High |
| MF-COA-010 | Disable GL account that is constrained by business rules | Account linked or protected | 1. Attempt disable/close action | Operation is blocked with correct error message | Medium |

### Additional Coverage Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MF-COA-011 | Manual entries allowed only for accounts with correct usage type | GL account exists | 1. Attempt journal entry on restricted and allowed accounts | Only accounts eligible for manual posting can be used | High |

---

## 14. Accounting - Journal Entries

### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MF-JRN-001 | View journal entries list | User with accounting permission | 1. Navigate to Journal Entries | Journal entries list is displayed with date, office, transaction ID, debit, and credit data | High |
| MF-JRN-002 | Create manual journal entry | Eligible GL accounts exist | 1. Click Create Journal Entry<br>2. Select office/date<br>3. Add balanced debit and credit rows<br>4. Submit | Journal entry is posted successfully | High |
| MF-JRN-003 | Reverse manual journal entry where supported | Existing reversible entry exists | 1. Open journal entry<br>2. Reverse it | Reversal entry is created and reflected in list | High |
| MF-JRN-004 | Filter journal entries by date range | Journal entries exist | 1. Apply date filter | Only entries within date range are displayed | Medium |
| MF-JRN-005 | Filter journal entries by office or transaction ID | Journal entries exist | 1. Apply office/ID filter | Matching entries are displayed | Medium |

### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MF-JRN-006 | Submit unbalanced journal entry | Eligible GL accounts exist | 1. Add debit and credit rows with unequal totals<br>2. Submit | Validation prevents posting | High |
| MF-JRN-007 | Submit journal entry without mandatory office/date | None | 1. Omit required fields<br>2. Submit | Validation error shown | High |
| MF-JRN-008 | Use restricted GL account for manual entry | Restricted account exists | 1. Add account not allowed for manual posting<br>2. Submit | Validation or business rule prevents save | High |
| MF-JRN-009 | Reverse already reversed entry | Reversed entry exists | 1. Attempt second reversal | Operation is blocked | Medium |

### Additional Coverage Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MF-JRN-010 | View journal entry detail drill-down | Entry exists | 1. Open entry detail | Entry lines and metadata are shown accurately | Medium |
| MF-JRN-011 | Backdated journal entry follows accounting closure rules | Closure exists for period | 1. Attempt manual entry in closed period | Operation is blocked if closure rules disallow posting | High |

---

## 15. Users & Roles

### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MF-USER-001 | View users list | Admin user logged in | 1. Navigate to Users | Users list displays username, office, roles, and status | High |
| MF-USER-002 | Create new user successfully | Office and role exist | 1. Click Create User<br>2. Enter username, first name, last name, email if applicable, office, roles, and password<br>3. Submit | User is created successfully and appears in users list | High |
| MF-USER-003 | View user details | User exists | 1. Open user record | User profile displays office, assigned roles, status, and metadata | High |
| MF-USER-004 | Edit user details | Editable user exists | 1. Open user<br>2. Click Edit<br>3. Update allowed fields<br>4. Submit | User details are updated successfully | High |
| MF-USER-005 | Assign additional role to user | User and role exist | 1. Edit user roles<br>2. Add role<br>3. Submit | New role is assigned successfully | High |
| MF-USER-006 | Remove role from user | User with multiple roles exists | 1. Edit user roles<br>2. Remove role<br>3. Submit | Role is removed successfully according to business rules | Medium |
| MF-USER-007 | Disable user | Active user exists | 1. Open user<br>2. Disable/inactivate user | User becomes inactive and cannot authenticate | High |
| MF-USER-008 | Re-enable disabled user | Disabled user exists | 1. Open disabled user<br>2. Enable user | User is restored to active status | Medium |
| MF-USER-009 | View roles list | Admin user logged in | 1. Navigate to Roles | Roles list loads with role names and status | High |
| MF-USER-010 | Create role successfully | Admin permissions available | 1. Click Create Role<br>2. Enter role name and permissions<br>3. Submit | Role is created successfully | High |
| MF-USER-011 | Edit role permissions | Existing role exists | 1. Open role<br>2. Update permission mappings<br>3. Submit | Role permissions are updated successfully | High |

### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MF-USER-013 | Create user without username | None | 1. Leave username empty<br>2. Submit | Validation error shown for username | High |
| MF-USER-014 | Create user without office | None | 1. Omit office selection<br>2. Submit | Validation error shown for office | High |
| MF-USER-015 | Create user without password | None | 1. Leave password blank<br>2. Submit | Validation error shown | High |
| MF-USER-016 | Duplicate username | Existing username exists | 1. Create user using existing username | Validation or server-side uniqueness error occurs | High |
| MF-USER-018 | Disable own currently logged-in user account | Admin logged in as target user | 1. Attempt to disable own account | System blocks or handles safely according to business rules | Medium |

### Additional Coverage Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MF-USER-019 | Password reset for existing user | User exists | 1. Open user<br>2. Reset password<br>3. Submit | User password is updated and old password becomes invalid | High |
| MF-USER-021 | Maker-checker permissions assigned through roles | Maker-checker enabled | 1. Assign maker/checker permissions to role<br>2. Perform relevant workflow | User can create or approve actions according to permission set | Medium |

---

## 16. Offices

### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MF-OFFICE-001 | View offices list | User with organization permission | 1. Navigate to Offices | Offices hierarchy/list is displayed | High |
| MF-OFFICE-002 | Create office successfully | Parent office exists if required | 1. Click Create Office<br>2. Enter office name, parent office, opening date<br>3. Submit | Office is created successfully | High |
| MF-OFFICE-003 | Edit office details | Office exists | 1. Open office<br>2. Edit details<br>3. Submit | Office details are updated successfully | High |
| MF-OFFICE-004 | View office hierarchy | Multiple parent-child offices exist | 1. Open Offices page | Parent-child structure is displayed correctly | Medium |
| MF-OFFICE-005 | Close office | Office eligible for closure | 1. Open office<br>2. Close office with closure date and reason | Office status changes to closed/inactive according to rules | Medium |

### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MF-OFFICE-006 | Create office without name | None | 1. Leave office name blank<br>2. Submit | Validation error shown | High |
| MF-OFFICE-007 | Create office without opening date | None | 1. Omit opening date<br>2. Submit | Validation error shown | High |
| MF-OFFICE-008 | Create office with invalid parent hierarchy | Existing office hierarchy exists | 1. Set invalid parent causing cyclic hierarchy if possible<br>2. Submit | Validation or business rule prevents save | High |
| MF-OFFICE-009 | Close office with active dependencies blocking closure | Office has active clients/users or dependent entities | 1. Attempt to close office | Operation is blocked with correct error | High |

### Additional Coverage Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MF-OFFICE-010 | Transfer dependent entities before office closure | Source and destination offices exist | 1. Move required dependencies<br>2. Close office | Closure succeeds only after dependencies are handled | Medium |
| MF-OFFICE-011 | Search/filter offices list | Multiple offices exist | 1. Search for office by name | Matching office is returned | Low |

---

## 17. Employees

### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MF-EMP-001 | View employees list | User with organization permission | 1. Navigate to Employees | Employees list is displayed with office and status | High |
| MF-EMP-002 | Create employee successfully | Office exists | 1. Click Create Employee<br>2. Enter first name, last name, office, joining date<br>3. Submit | Employee is created successfully | High |
| MF-EMP-003 | Edit employee details | Employee exists | 1. Open employee<br>2. Edit allowed fields<br>3. Submit | Employee updates are saved | High |
| MF-EMP-004 | View employee profile | Employee exists | 1. Open employee record | Employee detail page shows linked office and personal details | Medium |
| MF-EMP-005 | Assign employee to office correctly | Offices and employee exist | 1. Create or edit employee with office assignment | Office linkage is saved successfully | Medium |

### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MF-EMP-006 | Create employee without first name | None | 1. Leave first name blank<br>2. Submit | Validation error shown | High |
| MF-EMP-007 | Create employee without office | None | 1. Omit office<br>2. Submit | Validation error shown | High |

---

## 18. Reports

### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MF-REPORT-001 | View reports list | User with reporting permission | 1. Navigate to Reports | Reports page displays available report definitions/categories | High |
| MF-REPORT-002 | Run report with valid parameters | Parameterized report exists | 1. Open report<br>2. Enter required parameters<br>3. Run | Report output is generated successfully | High |
| MF-REPORT-003 | Run report without parameters when not required | Non-parameterized report exists | 1. Open report<br>2. Run report | Report output is generated | Medium |
| MF-REPORT-004 | Export report where supported | Generated report exists | 1. Run report<br>2. Export to available format | Export file is generated successfully | Medium |
| MF-REPORT-005 | View report data with large result set pagination or scrolling | Report with large dataset exists | 1. Run report | Results remain readable and usable | Medium |

### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MF-REPORT-006 | Run parameterized report without mandatory parameters | Parameterized report exists | 1. Open report<br>2. Leave required parameter blank<br>3. Run | Validation error shown | High |
| MF-REPORT-007 | Run report with invalid date range | Date-parameter report exists | 1. Provide invalid date range<br>2. Run | Validation or backend error handled gracefully | Medium |

### Additional Coverage Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MF-REPORT-009 | Search/filter reports catalog | Multiple reports exist | 1. Search report name | Matching reports displayed | Low |
| MF-REPORT-010 | Scheduled or background report definition visibility where supported | Feature available | 1. Open reports admin/settings | Available scheduled/report metadata is displayed correctly | Low |
| MF-REPORT-011 | Report output reflects latest committed transactions | Report depends on recent transaction | 1. Post transaction<br>2. Run report | Report includes latest data after commit | High |

---

## 19. Organization Settings

### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MF-ORG-001 | View organization settings modules | User with admin permission | 1. Navigate to Organization settings area | Available configuration pages are displayed | High |
| MF-ORG-002 | Configure working days | Organization settings accessible | 1. Open Working Days<br>2. Set business days and repayment reschedule rule<br>3. Save | Working day settings are saved successfully | High |
| MF-ORG-003 | Configure holidays | Organization settings accessible | 1. Open Holidays<br>2. Create holiday with office/date details<br>3. Save | Holiday is created and visible in list | High |
| MF-ORG-004 | Configure currency settings | Settings accessible | 1. Open currency/configuration module<br>2. Update allowed settings<br>3. Save | Currency-related settings are saved | Medium |
| MF-ORG-005 | Manage code values/code tables | Code management accessible | 1. Open codes module<br>2. Add or edit code value<br>3. Save | Code values are updated successfully | High |
| MF-ORG-006 | Manage payment types | Payment types accessible | 1. Open payment types<br>2. Create or edit payment type<br>3. Save | Payment type changes are saved | Medium |
| MF-ORG-007 | Configure fund definitions | Fund configuration accessible | 1. Open funds<br>2. Create/edit fund<br>3. Save | Fund definition is saved | Medium |
| MF-ORG-008 | Configure account number format | Feature accessible | 1. Open account number preferences<br>2. Update format/rules<br>3. Save | Account number format configuration is saved | Medium |

### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MF-ORG-010 | Create holiday with invalid date range | Settings accessible | 1. Enter invalid holiday period<br>2. Save | Validation error shown | High |
| MF-ORG-011 | Configure working days with invalid combination | Settings accessible | 1. Choose inconsistent rule combination<br>2. Save | Validation or business rule prevents save | Medium |
| MF-ORG-012 | Duplicate code value where uniqueness is required | Existing code value exists | 1. Add duplicate code value | Validation or server-side error occurs | Medium |

### Additional Coverage Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MF-ORG-014 | Account numbering changes apply to newly created entities only as designed | Account number format updated | 1. Change format<br>2. Create new client/account | New records follow updated numbering rule without corrupting existing numbers | Medium |
| MF-ORG-015 | Holiday affects repayment or transaction scheduling rules correctly | Holiday configured and relevant product/account exists | 1. Attempt transaction or schedule generation on holiday | Behavior follows configured holiday handling rule | High |
| MF-ORG-016 | Code value change appears in dependent dropdowns | Code table linked to entity form | 1. Add/edit code value<br>2. Open dependent form | Updated value appears correctly in UI | Medium |
| MF-ORG-017 | Payment type in transaction form reflects configured values | Payment types configured | 1. Open repayment/deposit form | Payment type dropdown matches organization settings | Medium |

---

## 20. Share Products

### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MF-SHPROD-001 | View share products list | Share module enabled | 1. Navigate to Share Products | Share products list displays configured products | High |
| MF-SHPROD-002 | Create share product successfully | Required setup exists | 1. Click Create Share Product<br>2. Fill mandatory fields including product name, short name, currency, total shares, nominal price, market price, accounting mappings if applicable<br>3. Submit | Share product is created successfully | High |
| MF-SHPROD-003 | View share product detail | Share product exists | 1. Open product | Product detail displays pricing, share limits, and settings | High |
| MF-SHPROD-004 | Edit share product | Share product exists | 1. Open product<br>2. Edit allowed fields<br>3. Submit | Product changes are saved successfully | High |
| MF-SHPROD-005 | Configure dividend settings on share product | Dividend feature enabled | 1. Create or edit product with dividend settings | Product retains dividend configuration | Medium |
| MF-SHPROD-006 | Configure share purchase limits | Share product exists | 1. Set minimum/maximum share purchase limits<br>2. Save | Limits are saved successfully | Medium |

### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MF-SHPROD-007 | Create share product without mandatory name | None | 1. Leave product name empty<br>2. Submit | Validation error shown | High |
| MF-SHPROD-008 | Create share product with invalid share limits | None | 1. Set min shares greater than max shares<br>2. Submit | Validation error prevents save | High |
| MF-SHPROD-009 | Missing accounting mappings when accounting rule requires them | GL accounts incomplete | 1. Configure accounting-requiring product without mandatory mappings<br>2. Submit | Validation blocks save | High |

### Additional Coverage Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MF-SHPROD-010 | Inactivate share product for future use | Product exists | 1. Disable/inactivate product | Product is unavailable for new share accounts | Medium |
| MF-SHPROD-011 | Dividend configuration is available only when feature is enabled | Feature toggles exist | 1. Inspect share product form under different configurations | Dividend settings behave according to feature availability | Low |
| MF-SHPROD-012 | Share product pricing updates affect new purchase behavior according to rules | Product exists | 1. Change allowed pricing field<br>2. Create new share purchase | New transactions use updated configuration as designed | Medium |

---

## 21. Floating Rates

### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MF-FRATE-001 | View floating rates list | Floating rate feature enabled | 1. Navigate to Floating Rates | Existing floating rates and periods are displayed | High |
| MF-FRATE-002 | Create floating rate successfully | Feature enabled | 1. Click Create Floating Rate<br>2. Enter name and required details<br>3. Submit | Floating rate is created successfully | High |
| MF-FRATE-003 | Add floating rate period | Floating rate exists | 1. Open floating rate<br>2. Add new period with effective date and rate<br>3. Submit | New floating rate period is saved | High |
| MF-FRATE-004 | View floating rate history | Floating rate with multiple periods exists | 1. Open floating rate details | Historical effective periods and rates are shown correctly | Medium |
| MF-FRATE-005 | Edit floating rate metadata | Floating rate exists | 1. Open floating rate<br>2. Edit metadata<br>3. Submit | Changes are saved successfully | Medium |

### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MF-FRATE-006 | Create floating rate without mandatory name | None | 1. Leave required name field empty<br>2. Submit | Validation error shown | High |
| MF-FRATE-007 | Add rate period with overlapping effective date range | Floating rate exists | 1. Add period overlapping existing effective period<br>2. Submit | Validation or business rule prevents save | High |
| MF-FRATE-008 | Add rate period with invalid rate value | Floating rate exists | 1. Enter invalid or out-of-range rate<br>2. Submit | Validation error shown | Medium |

### Additional Coverage Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MF-FRATE-009 | Loan product linked to floating rate uses latest applicable period | Linked loan product exists | 1. Configure product with floating rate<br>2. Create/inspect loan | Linked rate is resolved according to effective date rules | High |
| MF-FRATE-010 | Future-dated floating rate period does not affect current calculations before effective date | Floating rate has future-dated period | 1. Add future period<br>2. Inspect current-linked calculations | Current calculations remain unchanged until effective date | High |
| MF-FRATE-011 | Floating rate history remains immutable for already effective periods where business rules restrict edits | Existing period history exists | 1. Attempt restricted update to historical period | System blocks invalid modification or handles according to rules | Medium |

---

## 22. Delinquency Management

### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MF-DELINQ-001 | View delinquency buckets or ranges | Delinquency feature enabled | 1. Navigate to Delinquency configuration | Delinquency ranges/buckets are displayed | High |
| MF-DELINQ-002 | Create delinquency bucket successfully | Feature enabled | 1. Click Create Delinquency Bucket<br>2. Enter name and age/range details<br>3. Submit | Delinquency bucket is created successfully | High |
| MF-DELINQ-003 | Edit delinquency bucket | Existing bucket exists | 1. Open bucket<br>2. Edit values<br>3. Submit | Changes are saved successfully | Medium |
| MF-DELINQ-004 | View delinquent loans grouped by bucket | Delinquent loans exist | 1. Open delinquency view/report | Loans are categorized into correct delinquency ranges | High |
| MF-DELINQ-005 | Configure delinquency classification linked to loan product where supported | Loan product exists | 1. Open product delinquency settings<br>2. Link classification<br>3. Save | Product stores delinquency configuration | Medium |

### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MF-DELINQ-006 | Create bucket with overlapping ranges | Existing bucket ranges exist | 1. Create new overlapping range<br>2. Submit | Validation prevents overlapping configuration | High |
| MF-DELINQ-007 | Create bucket with invalid min/max range | None | 1. Enter invalid boundaries<br>2. Submit | Validation error shown | High |
| MF-DELINQ-008 | Delete or disable bucket in active use where restricted | Bucket linked to active configuration | 1. Attempt delete/disable | Business rule blocks unsafe change | Medium |

### Additional Coverage Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MF-DELINQ-009 | Delinquency categorization updates after repayment | Delinquent loan exists | 1. Post repayment reducing overdue days/amount<br>2. Refresh delinquency view | Loan bucket changes according to updated delinquency state | High |
| MF-DELINQ-010 | Write-off or closure removes loan from active delinquency population as expected | Written-off/closed loan exists | 1. Change loan status appropriately<br>2. Reopen delinquency report | Loan no longer appears in active delinquency bucket population unless designed otherwise | High |

---

## 23. Share Account

### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MF-SHARE-001 | Create share account for client | Active client and share product exist | 1. Open client profile<br>2. Create new share account<br>3. Select product and submit required values | Share account is created successfully | High |
| MF-SHARE-002 | Approve share account application | Pending share account exists | 1. Open share account<br>2. Approve application | Share account moves to approved state | High |
| MF-SHARE-003 | Activate share account | Approved share account exists | 1. Open account<br>2. Activate | Share account becomes active | High |
| MF-SHARE-004 | Purchase shares | Active share account exists | 1. Open share account<br>2. Purchase shares with quantity/date<br>3. Submit | Purchase transaction is posted and holdings increase | High |
| MF-SHARE-005 | Redeem shares | Active share account with sufficient holdings exists | 1. Open share account<br>2. Redeem shares<br>3. Submit | Redemption transaction is posted and holdings decrease | High |
| MF-SHARE-006 | View share transactions | Share account with activity exists | 1. Open transactions section | Purchase/redemption/dividend history is displayed | Medium |
| MF-SHARE-007 | Post dividend to eligible share account | Dividend-capable share product/account exists | 1. Trigger or post dividend action | Dividend transaction is recorded correctly | Medium |
| MF-SHARE-008 | Close share account | Eligible account exists | 1. Open account<br>2. Close with required details | Share account status changes to closed | Medium |

### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MF-SHARE-009 | Purchase shares below minimum allowed quantity | Active share account exists | 1. Attempt purchase below minimum threshold | Validation or business rule blocks transaction | High |
| MF-SHARE-010 | Redeem more shares than held | Active share account exists | 1. Attempt redemption exceeding holdings | Transaction is blocked | High |
| MF-SHARE-011 | Purchase or redeem on non-active share account | Account not active | 1. Attempt transaction | Action is blocked | High |
| MF-SHARE-012 | Activate share account with invalid date order | Approved share account exists | 1. Activate with invalid date | Validation prevents activation | Medium |

### Additional Coverage Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MF-SHARE-013 | Reject share account application | Pending share account exists | 1. Open account<br>2. Reject | Account status changes to Rejected | Medium |
| MF-SHARE-014 | Share balance and nominal/market value display updates after transactions | Share account exists | 1. Purchase or redeem shares<br>2. Reopen summary | Summary values reflect updated holdings and valuation inputs | Medium |
| MF-SHARE-015 | Dividend posting respects eligible holdings and effective rules | Dividend run configured | 1. Post dividend | Dividend amount aligns with eligible share holdings/rules | Medium |

---

## 24. Fixed & Recurring Deposit Accounts

### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MF-DEP-001 | Create fixed deposit product successfully | Required accounting and configuration setup exists | 1. Navigate to deposit products<br>2. Create fixed deposit product with mandatory details<br>3. Submit | Fixed deposit product is created successfully | High |
| MF-DEP-002 | Create recurring deposit product successfully | Required setup exists | 1. Create recurring deposit product with mandatory details<br>2. Submit | Recurring deposit product is created successfully | High |
| MF-DEP-003 | Open fixed deposit account for client | Active client and fixed deposit product exist | 1. Open client profile<br>2. Create fixed deposit account<br>3. Fill required values<br>4. Submit | Fixed deposit account is created successfully | High |
| MF-DEP-004 | Open recurring deposit account for client | Active client and recurring deposit product exist | 1. Create recurring deposit account from client profile | Recurring deposit account is created successfully | High |
| MF-DEP-005 | Approve deposit account | Pending deposit account exists | 1. Open deposit account<br>2. Approve | Account moves to approved state | High |
| MF-DEP-006 | Activate deposit account | Approved deposit account exists | 1. Open account<br>2. Activate with required date | Account becomes active | High |
| MF-DEP-007 | Premature close fixed deposit account | Eligible fixed deposit account exists | 1. Open account<br>2. Initiate premature closure<br>3. Submit | Account closes with premature closure handling applied | Medium |
| MF-DEP-008 | Mature and close fixed deposit account | Matured fixed deposit account exists | 1. Open matured account<br>2. Close on maturity | Maturity proceeds are handled correctly and account closes | High |
| MF-DEP-009 | Post installment to recurring deposit account | Active RD account exists | 1. Open RD account<br>2. Post deposit installment | Installment transaction is recorded correctly | High |
| MF-DEP-010 | View deposit account transactions and maturity details | Deposit account exists | 1. Open account | Transactions, interest accruals, and maturity information display correctly | Medium |

### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MF-DEP-011 | Create deposit product without mandatory name | None | 1. Leave name empty<br>2. Submit | Validation error shown | High |
| MF-DEP-012 | Create fixed deposit with invalid tenure configuration | None | 1. Enter invalid tenure values<br>2. Submit | Validation prevents save | High |
| MF-DEP-013 | Open deposit account without product | Active client exists | 1. Start account creation<br>2. Omit product<br>3. Submit | Validation error shown | High |
| MF-DEP-014 | Activate deposit account with invalid date sequence | Approved account exists | 1. Use invalid activation date<br>2. Submit | Validation prevents activation | High |
| MF-DEP-015 | Post RD installment with invalid amount | Active RD exists | 1. Enter invalid installment amount<br>2. Submit | Validation error shown | High |
| MF-DEP-016 | Premature closure on ineligible account | Deposit account not eligible | 1. Attempt premature closure | Business rule blocks action | Medium |

### Additional Coverage Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MF-DEP-017 | Reject deposit account application | Pending deposit account exists | 1. Open account<br>2. Reject | Account status changes to Rejected | Medium |
| MF-DEP-018 | Interest posting or accrual updates deposit account balances correctly | Active deposit account exists | 1. Trigger interest accrual/posting | Balances and maturity details update correctly | High |
| MF-DEP-019 | Maturity instructions transfer proceeds according to configured option | Matured account with instructions exists | 1. Process maturity | Proceeds are paid out, transferred, or renewed according to configuration | High |
| MF-DEP-020 | Recurring deposit missed installment behavior follows product rules | Active RD with missed schedule exists | 1. Skip installment and inspect account | Penalties or status outcomes follow configured rules | Medium |

---

## 25. Accounting - Closures

### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MF-CLOSE-001 | View accounting closures list | Accounting admin logged in | 1. Navigate to Accounting Closures | Existing closures are displayed by office/date | High |
| MF-CLOSE-002 | Create accounting closure successfully | No conflicting closure for same scope/date | 1. Click Create Closure<br>2. Select office and closing date<br>3. Submit | Closure is created successfully | High |
| MF-CLOSE-003 | View closure details | Closure exists | 1. Open closure | Closure details display office/date metadata | Medium |

### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MF-CLOSE-004 | Create duplicate closure for same office/date constraints | Closure exists | 1. Attempt duplicate closure | Validation or business rule prevents duplicate | High |
| MF-CLOSE-005 | Create closure without required office/date | None | 1. Omit mandatory fields<br>2. Submit | Validation error shown | High |
| MF-CLOSE-006 | Backdated transaction after closure is blocked | Closure exists for relevant period | 1. Attempt transaction/manual journal entry in closed period | System blocks posting according to closure rules | High |

### Additional Coverage Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MF-CLOSE-007 | Closure impacts all relevant accounting transactions for scoped office | Closure exists and transactions attempted | 1. Try various posting workflows after closure | Restricted transactions are blocked consistently | High |
| MF-CLOSE-008 | Closure list can be filtered or sorted where supported | Multiple closures exist | 1. Use available list controls | Expected closures are shown | Low |

---

## 26. Accounting Rules & Financial Activity Mappings

### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MF-FAM-001 | View financial activity mappings | Accounting configuration accessible | 1. Navigate to Financial Activity Mappings | Existing mappings are displayed | High |
| MF-FAM-002 | Create or update financial activity to GL mapping | GL accounts exist | 1. Open financial activity<br>2. Assign GL account mapping<br>3. Save | Mapping is saved successfully | High |
| MF-FAM-003 | View accounting rules configuration | Accounting settings accessible | 1. Navigate to accounting rules/settings | Configured rules are displayed correctly | Medium |
| MF-FAM-004 | Edit accounting rule setting | Editable accounting setting exists | 1. Update rule value<br>2. Save | Rule change is persisted | Medium |

### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MF-FAM-005 | Save mapping without required GL account | Financial activity selected | 1. Leave required account empty<br>2. Save | Validation error shown | High |
| MF-FAM-006 | Map financial activity to invalid or incompatible GL account | GL account incompatible | 1. Select invalid account type<br>2. Save | Validation or business rule blocks save | High |

### Additional Coverage Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MF-FAM-008 | Product/account posting uses configured financial activity mapping | Mapping exists and relevant txn occurs | 1. Perform linked transaction | Journal entries use configured mapped GL account | High |
| MF-FAM-009 | Updating mapping affects future transactions without corrupting historical entries | Existing transactions and mapping exist | 1. Change mapping<br>2. Post new transaction | Historical entries remain unchanged and new entries use updated mapping | High |
| MF-FAM-010 | Accounting rules visible state matches enabled features | Different features enabled/disabled | 1. Review accounting settings | Only relevant rules are displayed and editable | Low |

---

## 27. Provisioning

### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MF-PROV-001 | View provisioning criteria | Provisioning feature enabled | 1. Navigate to Provisioning | Provisioning criteria and history are displayed | High |
| MF-PROV-002 | Create provisioning criteria | Feature enabled | 1. Create criteria with delinquency ranges and percentages<br>2. Save | Criteria are saved successfully | High |
| MF-PROV-003 | Generate provisioning entries | Criteria and eligible loans exist | 1. Run provisioning process | Provisioning entries/report are generated successfully | High |
| MF-PROV-004 | View provisioning history | Provisioning runs exist | 1. Open provisioning history | Past generated entries are displayed | Medium |

### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MF-PROV-005 | Create provisioning criteria with overlapping delinquency ranges | Criteria ranges exist | 1. Enter overlapping ranges<br>2. Save | Validation prevents overlapping setup | High |
| MF-PROV-006 | Create criteria with invalid percentage | None | 1. Enter invalid percentage value<br>2. Save | Validation error shown | High |
| MF-PROV-007 | Run provisioning without required setup | No valid criteria exists | 1. Attempt generate process | Process is blocked with proper error | Medium |

### Additional Coverage Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MF-PROV-008 | Provisioning output reflects latest delinquency positions | Delinquent loans exist | 1. Change delinquency state via repayment or aging<br>2. Re-run provisioning | Output reflects current delinquency categories | High |
| MF-PROV-009 | Generated provisioning creates expected accounting impact where configured | Accounting integration enabled | 1. Run provisioning | Related accounting entries are created correctly | High |

---

## 28. Teller & Cashier Management

### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MF-TELLER-001 | View tellers list | Teller feature enabled and user has permission | 1. Navigate to Tellers | Teller list is displayed with office and status details | High |
| MF-TELLER-002 | Create teller successfully | Office and required setup exist | 1. Click Create Teller<br>2. Enter teller details including office and cash limits if required<br>3. Submit | Teller is created successfully | High |
| MF-TELLER-003 | View cashier assignments | Tellers and users exist | 1. Navigate to Cashiers or teller detail page | Cashier assignments are displayed correctly | High |
| MF-TELLER-004 | Assign cashier to teller | Teller and eligible user exist | 1. Open teller<br>2. Assign cashier/user with start and end time if required<br>3. Submit | Cashier assignment is saved successfully | High |
| MF-TELLER-005 | Allocate cash to cashier | Active teller and cashier assignment exist | 1. Open cashier allocation workflow<br>2. Enter amount<br>3. Submit | Cash allocation transaction is recorded successfully | High |
| MF-TELLER-006 | Settle cashier balance | Active cashier with transactions exists | 1. Open settle or close cashier workflow<br>2. Submit settlement | Cashier is settled and balances are reconciled according to rules | High |
| MF-TELLER-007 | View cashier transactions | Cashier transaction history exists | 1. Open cashier transactions/history | Allocation, settlement, and cash transactions are displayed | Medium |
| MF-TELLER-008 | Close or deactivate teller | Teller eligible for closure | 1. Open teller<br>2. Deactivate or close | Teller status is updated successfully | Medium |

### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MF-TELLER-009 | Create teller without mandatory office | None | 1. Omit office while creating teller<br>2. Submit | Validation error shown | High |
| MF-TELLER-010 | Assign cashier with invalid overlapping schedule | Existing assignment exists | 1. Create overlapping cashier assignment for same user/teller if restricted<br>2. Submit | Validation or business rule prevents overlap | High |
| MF-TELLER-011 | Allocate negative or zero cash amount | Active cashier exists | 1. Enter invalid amount<br>2. Submit | Validation error shown | High |
| MF-TELLER-012 | Settle cashier with inconsistent cash balance | Cashier imbalance exists | 1. Attempt settlement without resolving discrepancy if required | Process is blocked or discrepancy is surfaced correctly | High |

### Additional Coverage Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MF-TELLER-014 | Cash allocation impacts cashier available balance immediately | Active cashier exists | 1. Allocate cash<br>2. Refresh cashier detail | Available cash/balance reflects allocation | High |
| MF-TELLER-015 | Settlement closes cashier session for further transactions where required | Cashier settled | 1. Settle cashier<br>2. Attempt additional cashier action | Further cashier activity is blocked or requires new assignment/session | Medium |
| MF-TELLER-016 | Teller and cashier list filters work | Multiple tellers/cashiers exist | 1. Search/filter by office or status | Matching records are displayed | Low |
| MF-TELLER-017 | Cashier transaction audit trail shows maker/checker metadata where enabled | Maker-checker enabled | 1. Perform teller workflow | Audit details are recorded correctly | Medium |

---

## 29. Account Transfers & Standing Instructions

### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MF-TRF-001 | Transfer funds between eligible own accounts | Client has eligible source and destination accounts | 1. Open transfer workflow<br>2. Select source and destination accounts<br>3. Enter amount/date<br>4. Submit | Transfer is completed and reflected in both accounts | High |
| MF-TRF-002 | Transfer from savings to loan repayment | Active savings and loan accounts exist | 1. Select savings as source and loan as destination<br>2. Submit transfer | Savings is debited and loan repayment transaction is posted | High |
| MF-TRF-003 | Transfer between client accounts across supported account types | Eligible account types exist | 1. Perform supported transfer | Transfer succeeds according to supported combinations | Medium |
| MF-TRF-004 | Create standing instruction successfully | Eligible source/destination accounts exist | 1. Navigate to Standing Instructions<br>2. Create instruction with frequency, amount/rule, start date, source, and destination<br>3. Submit | Standing instruction is created successfully | High |
| MF-TRF-005 | Execute due standing instruction | Active standing instruction exists and due date reached | 1. Trigger scheduled execution or inspect executed run | Transfer posts successfully according to standing instruction | High |
| MF-TRF-006 | View standing instructions list | Standing instructions exist | 1. Navigate to Standing Instructions | Standing instruction list displays status and rule details | Medium |
| MF-TRF-007 | Disable or delete standing instruction | Existing standing instruction exists | 1. Open instruction<br>2. Disable/delete | Instruction status changes accordingly and future execution stops | Medium |

### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MF-TRF-008 | Transfer amount exceeds allowed source balance | Eligible accounts exist but insufficient funds | 1. Enter excessive transfer amount<br>2. Submit | Transfer is blocked with proper validation or business-rule message | High |
| MF-TRF-009 | Transfer between unsupported account types | Unsupported combination selected | 1. Attempt unsupported transfer | Action is blocked | High |
| MF-TRF-010 | Create standing instruction with invalid schedule | Eligible accounts exist | 1. Enter invalid start/end date or frequency combination<br>2. Submit | Validation error shown | High |
| MF-TRF-011 | Standing instruction execution fails when source account has insufficient balance | Active standing instruction exists | 1. Allow due execution with insufficient funds | Execution fails gracefully and failure status/history is recorded | High |

### Additional Coverage Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MF-TRF-013 | Transfer transaction appears in both source and destination histories | Successful transfer exists | 1. Open both accounts | Matching debit/credit entries are visible | High |
| MF-TRF-014 | Standing instruction can be paused and resumed where supported | Instruction exists | 1. Pause instruction<br>2. Resume instruction | Execution behavior follows updated status | Medium |
| MF-TRF-015 | Duplicate standing instruction detection where business rules restrict duplicates | Same instruction already exists | 1. Attempt duplicate creation | Validation or business rule prevents duplicate | Low |

---

## 30. Tax Management

### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MF-TAX-001 | View tax components list | Tax feature enabled | 1. Navigate to tax management | Tax components and groups are displayed | High |
| MF-TAX-002 | Create tax component successfully | Tax feature enabled | 1. Create tax component with name and percentage/value<br>2. Submit | Tax component is created successfully | High |
| MF-TAX-003 | Create tax group successfully | Tax components exist | 1. Create tax group and add components<br>2. Submit | Tax group is created successfully | High |
| MF-TAX-004 | Link tax group to applicable charge/product where supported | Charges/products and tax config exist | 1. Edit applicable configuration<br>2. Assign tax group<br>3. Save | Tax configuration is saved successfully | Medium |
| MF-TAX-005 | View tax configuration details | Tax components/groups exist | 1. Open tax component/group | Details display correct rates and applicability | Medium |

### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MF-TAX-006 | Create tax component without mandatory fields | None | 1. Omit required fields<br>2. Submit | Validation error shown | High |
| MF-TAX-007 | Create tax component with invalid rate | None | 1. Enter invalid tax rate<br>2. Submit | Validation error shown | High |
| MF-TAX-008 | Create tax group without components where at least one is required | None | 1. Leave group empty<br>2. Submit | Validation or business rule prevents save | Medium |

### Additional Coverage Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MF-TAX-010 | Tax is applied correctly on configured charge transaction | Tax-linked charge exists | 1. Trigger charge transaction | Tax amount is computed and posted according to configuration | High |
| MF-TAX-011 | Updating tax rate affects future transactions only | Tax component already used historically | 1. Update tax rate<br>2. Trigger new transaction | Historical transactions remain unchanged and new transactions use updated rate | High |
| MF-TAX-012 | Tax breakdown is visible in transaction details where supported | Tax-applied transaction exists | 1. Open transaction detail | Tax component breakdown is shown correctly | Medium |

---

## 31. System Administration

### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MF-SYS-001 | View system administration modules | Admin user logged in | 1. Navigate to system administration area | Available admin modules are displayed | High |
| MF-SYS-002 | Manage data tables | Data table feature enabled | 1. Navigate to Data Tables<br>2. View existing tables | Data tables list is displayed correctly | Medium |
| MF-SYS-003 | Create or register data table where supported | Data table feature enabled | 1. Create/register new data table configuration<br>2. Save | Data table is created successfully | Medium |
| MF-SYS-004 | Manage hooks/webhooks configuration | Hook feature enabled | 1. Open hooks configuration<br>2. Create or edit hook endpoint/settings<br>3. Save | Hook configuration is saved successfully | Medium |
| MF-SYS-005 | View scheduler jobs | Scheduler feature enabled | 1. Navigate to Scheduler Jobs | Jobs list and status are displayed | High |
| MF-SYS-006 | Run a schedulable job manually where supported | Eligible job exists | 1. Trigger manual execution | Job execution starts/completes successfully | Medium |
| MF-SYS-007 | Manage password preferences or security settings | Security settings accessible | 1. Open password/security preferences<br>2. Update policy settings<br>3. Save | Security preferences are saved successfully | High |
| MF-SYS-008 | Manage external services or configurations where supported | Feature enabled | 1. Open external service configuration<br>2. View/edit supported settings | Changes are saved successfully | Low |
| MF-SYS-009 | Manage maker-checker settings | Maker-checker feature accessible | 1. Open maker-checker settings<br>2. Enable or configure | Configuration is saved successfully | High |
| MF-SYS-010 | View audit or application logs where supported | Feature enabled | 1. Navigate to log/audit section | Available logs/audit metadata are displayed | Low |

### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MF-SYS-012 | Save invalid hook endpoint configuration | Hook feature enabled | 1. Enter invalid endpoint/config values<br>2. Save | Validation or connectivity error is shown | Medium |
| MF-SYS-014 | Set invalid password policy values | Security settings accessible | 1. Enter invalid values such as unsupported lengths or combinations<br>2. Save | Validation error shown | High |

### Additional Coverage Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MF-SYS-015 | Scheduler job execution updates last-run status correctly | Schedulable job exists | 1. Run job<br>2. Refresh job list | Last run metadata and status reflect execution outcome | Medium |
| MF-SYS-016 | Maker-checker workflow holds pending action until checker approval | Maker-checker enabled and applicable action exists | 1. Perform maker action<br>2. Inspect pending approvals | Action remains pending until checker approves | High |
| MF-SYS-017 | Checker approval completes pending maker action | Pending maker-checker action exists | 1. Login as checker<br>2. Approve action | Underlying business operation completes successfully | High |
| MF-SYS-018 | Checker rejection cancels pending maker action | Pending maker-checker action exists | 1. Reject pending action | Pending action is not executed and status updates accordingly | High |
| MF-SYS-019 | Hook invocation occurs on configured business event | Valid hook configured | 1. Trigger linked event such as client creation or repayment | Hook is invoked according to event configuration | Medium |
| MF-SYS-020 | Password policy update affects subsequent user password operations | Password policy modified | 1. Update security policy<br>2. Create/reset password using new values | System enforces updated policy on future operations | High |

---

## 32. Logout

### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MF-LOGOUT-001 | Logout from user menu | User logged in | 1. Open user/profile menu<br>2. Click Logout | User session is terminated and login page is displayed | High |
| MF-LOGOUT-002 | Protected routes inaccessible after logout | User logged out after active session | 1. Logout<br>2. Attempt to navigate to protected route | User is redirected to login page or access is denied | High |
| MF-LOGOUT-003 | Browser refresh after logout does not restore authenticated session | User has logged out | 1. Logout<br>2. Refresh page | User remains logged out | High |

### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MF-LOGOUT-004 | Browser back after logout does not reopen active authenticated page | User logged out | 1. Logout<br>2. Press browser back | Previously visited protected page is not usable without re-authentication | High |
| MF-LOGOUT-005 | Expired session behaves consistently with explicit logout | Session timeout configured or token invalidated | 1. Allow session to expire<br>2. Perform action | User is redirected to login or prompted to re-authenticate | High |

### Additional Coverage Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| MF-LOGOUT-006 | Logout clears user-specific UI state | User logged in and navigation state exists | 1. Logout<br>2. Login as different user | New user does not inherit previous user's UI state in unauthorized ways | Medium |
| MF-LOGOUT-007 | Logout from any module behaves consistently | User logged in on non-home route | 1. Logout from multiple pages/modules | Logout always invalidates session and returns to login page | Medium |

---

## Test Summary

| Module | Total Tests | High Priority | Medium Priority | Low Priority |
|--------|-------------|---------------|-----------------|--------------|
| Login | 12 | 7 | 5 | 0 |
| Home | 5 | 4 | 1 | 0 |
| Dashboard | 5 | 2 | 3 | 0 |
| Global Search | 11 | 5 | 5 | 1 |
| Client Management | 29 | 12 | 15 | 2 |
| Group Management | 18 | 9 | 8 | 1 |
| Center Management | 18 | 8 | 9 | 1 |
| Loan Products | 14 | 13 | 1 | 0 |
| Savings Products | 15 | 11 | 4 | 0 |
| Charges | 16 | 10 | 6 | 0 |
| Loan Account | 29 | 17 | 10 | 2 |
| Savings Account | 22 | 12 | 7 | 3 |
| Accounting - Chart of Accounts | 11 | 8 | 3 | 0 |
| Accounting - Journal Entries | 11 | 7 | 4 | 0 |
| Users & Roles | 18 | 14 | 4 | 0 |
| Offices | 11 | 7 | 3 | 1 |
| Employees | 7 | 5 | 2 | 0 |
| Reports | 10 | 4 | 4 | 2 |
| Organization Settings | 15 | 6 | 9 | 0 |
| Share Products | 12 | 7 | 4 | 1 |
| Floating Rates | 11 | 7 | 4 | 0 |
| Delinquency Management | 10 | 7 | 3 | 0 |
| Share Account | 15 | 8 | 7 | 0 |
| Fixed & Recurring Deposit Accounts | 20 | 15 | 5 | 0 |
| Accounting - Closures | 8 | 6 | 1 | 1 |
| Accounting Rules & Financial Activity Mappings | 9 | 6 | 2 | 1 |
| Provisioning | 9 | 7 | 2 | 0 |
| Teller & Cashier Management | 16 | 11 | 4 | 1 |
| Account Transfers & Standing Instructions | 14 | 9 | 4 | 1 |
| Tax Management | 11 | 7 | 4 | 0 |
| System Administration | 18 | 9 | 7 | 2 |
| Logout | 7 | 5 | 2 | 0 |
| **TOTAL** | **437** | **265** | **152** | **20** |