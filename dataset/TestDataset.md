# MIFOS Functional Description

---

## Navigation

Mifos is a comprehensive microfinance and core banking platform built on Apache Fineract. The application uses a Material Design layout with a persistent top navigation bar and a left icon-based sidebar. The top navigation bar displays the Mifos logo on the left and menu items for Institution, Accounting, Reports, Admin, Self Service, and Configuration Wizard, along with icons for global search, language selection, notifications, and user profile on the right. The Institution menu contains links to Clients, Groups, Centers, Accounting, Reports, Admin, and Self Service. The left sidebar contains icon-based shortcuts to commonly used sections including Clients, Groups, Centers, and Products; each icon navigates to the corresponding page in the main content area. Breadcrumbs appear at the top of the content area showing the navigation path. Entity listing pages display data in Material Design tables with search, filter, sort, and pagination controls. Detail pages display entity information in card layouts with action buttons for state transitions. Forms use Material Design input fields with inline validation.

---


## Client Management

The Clients page displays a data table of all clients with columns for Name (clickable link), Account No., External ID, Status (Pending as yellow chip, Active as green chip, Closed as gray chip, Rejected as red chip, Withdrawn as orange chip), Office, and Staff. A search field allows searching by name, account number, external ID, or mobile number, and a filter bar supports filtering by status. Two buttons at the top-right provide "Import Client" (opens the Bulk Import page) and "Create Client." The Bulk Import page allows downloading a client Excel template, uploading a completed file, and displays an import history table with columns for Name, Import Time, End Time, Completed, Total Records, Success Count, Failure Count, and Download.

The Create Client form is a multi-step wizard. Step 1 (General Details) contains Office (required), Legal Form, First Name (required), Middle Name, Last Name (required), Date of Birth, Gender, Staff, Mobile Number, Email Address, Client Type, Client Classification, External ID (must be unique), Submitted On (required), Is Staff checkbox, Active checkbox, and Open Savings Account option. Step 2 covers Address Details. Step 3 covers Family Members. Step 4 covers Identifiers (Document Type and Document Key). Clicking "Submit" creates the client in Pending status.

The Client Detail page displays the client name, account number, status badge, activation date, and office. Action buttons change based on status: Pending offers Activate (requires Activation Date, which must not be before submission date), Edit, Reject (with reason), and Withdraw (with reason); Active offers Edit, Transfer Client (destination office required — same office is blocked), Close (closure reason required — cannot close with active accounts), Add Charge, New Loan, New Savings, and New Share Account; Closed offers Reactivate; Rejected and Withdrawn have no actions. Tabs on the detail page show General, Accounts (sub-tabs for Loans, Savings, Shares, Fixed Deposits, Recurring Deposits), Identifiers (Document Type and Key with add/remove — duplicates are prevented), Family Members, Notes, and Documents.

---