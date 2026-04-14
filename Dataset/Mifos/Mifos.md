# MIFOS Functional Description

---

## Navigation

Mifos is a comprehensive microfinance and core banking platform built on Apache Fineract. The application uses a Material Design layout with a persistent top navigation bar and a left icon-based sidebar. The top navigation bar displays the Mifos logo on the left and menu items for Institution, Accounting, Reports, Admin, Self Service, and Configuration Wizard, along with icons for global search, language selection, notifications, and user profile on the right. The Institution menu contains links to Clients, Groups, Centers, Accounting, Reports, Admin, and Self Service. The left sidebar contains icon-based shortcuts to commonly used sections including Clients, Groups, Centers, and Products; each icon navigates to the corresponding page in the main content area. Breadcrumbs appear at the top of the content area showing the navigation path. Entity listing pages display data in Material Design tables with search, filter, sort, and pagination controls. Detail pages display entity information in card layouts with action buttons for state transitions. Forms use Material Design input fields with inline validation.

---

## Login

The login page has two panels. The left panel displays a background image with the title "Mifos X." The right panel contains the authentication interface with the Mifos logo and a language selector. The login form contains a Tenant dropdown (defaults to "default"), Username, Password, and a Remember me checkbox. The Login button is enabled only after required fields are filled. A "Forgot Password?" link appears below the button. On submission, valid credentials redirect to the Dashboard. Invalid credentials show an error message; empty required fields show inline validation messages.

---

## Home Page

The Home page appears after successful login. The main content area displays a welcome card with the message "Welcome, mifos!" and a "Search Activity" input field for searching recent system activities. A "Dashboard" button provides quick access to the dashboard view. System version information for Mifos and Fineract is displayed at the bottom.

---

## Dashboard

The Dashboard is accessed from the "Dashboard" button on the Home page. A "Search Activity" field appears at the top. The main section displays a "Client Trends" chart visualizing client growth over time for the selected office, with legends for "New Clients" and "Closed Clients." Below the chart, two summary cards display "Amount Pending / Disbursed" and "Amount Collected" for the selected office, showing "No Data" if no information is available.

---

## Global Search

Global search is accessible from the search icon in the top toolbar from any page after login. Clicking the icon opens a search input field. As the user types, the system searches across Clients, Groups, Loans, and Savings accounts. Matching results appear in a dropdown grouped by entity type, each showing the entity name, identifier, and status. Selecting a result navigates to the corresponding detail page. If no matches are found, a "No results found" message is displayed. The search supports partial matching and is case-insensitive.

---

## Client Management

The Clients page displays a data table of all clients with columns for Name (clickable link), Account No., External ID, Status (Pending as yellow chip, Active as green chip, Closed as gray chip, Rejected as red chip, Withdrawn as orange chip), Office, and Staff. A search field allows searching by name, account number, external ID, or mobile number, and a filter bar supports filtering by status. Two buttons at the top-right provide "Import Client" (opens the Bulk Import page) and "Create Client." The Bulk Import page allows downloading a client Excel template, uploading a completed file, and displays an import history table with columns for Name, Import Time, End Time, Completed, Total Records, Success Count, Failure Count, and Download.

The Create Client form is a multi-step wizard. Step 1 (General Details) contains Office (required), Legal Form, First Name (required), Middle Name, Last Name (required), Date of Birth, Gender, Staff, Mobile Number, Email Address, Client Type, Client Classification, External ID (must be unique), Submitted On (required), Is Staff checkbox, Active checkbox, and Open Savings Account option. Step 2 covers Address Details. Step 3 covers Family Members. Step 4 covers Identifiers (Document Type and Document Key). Clicking "Submit" creates the client in Pending status.

The Client Detail page displays the client name, account number, status badge, activation date, and office. Action buttons change based on status: Pending offers Activate (requires Activation Date, which must not be before submission date), Edit, Reject (with reason), and Withdraw (with reason); Active offers Edit, Transfer Client (destination office required — same office is blocked), Close (closure reason required — cannot close with active accounts), Add Charge, New Loan, New Savings, and New Share Account; Closed offers Reactivate; Rejected and Withdrawn have no actions. Tabs on the detail page show General, Accounts (sub-tabs for Loans, Savings, Shares, Fixed Deposits, Recurring Deposits), Identifiers (Document Type and Key with add/remove — duplicates are prevented), Family Members, Notes, and Documents.

---

## Group Management

The Groups page displays a data table with columns for Group Name (clickable link), Account Number, Office, Status (Active, Pending, Closed as colored chips), and Staff. Buttons at the top-right allow importing groups or creating a new group. The Create Group form contains Name (required), Office (required), Staff, Submitted On (required), Active checkbox, External Id, and an Add Clients search-and-add interface to associate existing clients. Clicking "Submit" creates the group. The Bulk Import Groups page has a Groups Template panel (Office and Staff dropdowns with a Download button) and a Groups Upload panel (file picker and Upload button), with an import history table below.

The Group Detail page displays the group name, account number, status, office, and staff with action buttons for Activate, Edit, Close, Assign Staff, and Transfer Clients. Tabs show Members (list of client members with links to their profiles), Loan Accounts (group loans and GLIM — Group Linked Individual Micro-loans), Savings Accounts (group savings and GSIM accounts), Notes, and a Calendar/Meeting section for scheduling and recording group meetings. The Collection Sheet feature generates a sheet showing all group clients with loan repayment amounts due and savings deposit amounts for batch data entry.

---

## Center Management

Centers are higher-level organizational units that contain groups. The Centers page displays a data table with columns for Name (clickable link), Account #, External Id, Status, and Office Name. Buttons at the top-right provide "Import Center" and "Create Center." The Create Center form contains Name (required), Office (required), Staff, Active checkbox, External Id, Submitted On (required), and a Select and Add groups dropdown search. Clicking "Submit" creates the center. The Bulk Import Centers page follows the same template-download and file-upload pattern as Groups.

The Center Detail page displays the center name, status, office, and staff with action buttons for Activate, Edit, Close, and Assign Staff. Tabs show Groups (list of member groups with links), Loan Accounts, Savings Accounts, Notes, and a Calendar/Meeting section. The Collection Sheet feature generates a sheet showing all groups and their clients with loan repayment and savings deposit amounts for batch data entry.

---

## Loan Products

The Loan Products page displays a filter bar and a data table listing all loan products with columns for Name (clickable link), Short Name, Expiry Date, and Status. A "+ Create Loan Product" button opens a 6-step stepper wizard. Step 1 (Details) contains Product Name (required), Short Name (required), External Id, Fund, Include in Customer Loan Counter checkbox, Start Date, Close Date, and Description. Step 2 (Currency) contains currency selection with Decimal Places, Multiples of Rounding, and Principal Amount with Minimum, Default, and Maximum values. Step 3 (Settings) contains Amortization method (Equal Installments, Equal Principal Payments), Interest Method (Flat, Declining Balance), Interest Calculation Period (Daily, Same as repayment period), Repayment Strategy, Days in Year (360, 365, Actual), Days in Month (30, Actual), and numeric fields for grace periods and Arrears Tolerance. Step 4 (Terms) contains Number of Repayments with Minimum, Default, and Maximum; Repaid Every frequency with unit (Days, Weeks, Months); and Nominal Interest Rate with Minimum, Default, and Maximum. Step 5 (Charges) is a search-and-add interface for predefined charges. Step 6 (Accounting) contains a radio button for None, Cash-based, Accrual (periodic), or Accrual (upfront); selecting a non-None method reveals GL account dropdown mappings for Fund Source, Loan Portfolio, Interest on Loans, Income from Fees, Income from Penalties, Losses Written Off, and Overpayment Liability. All required fields show inline validation errors. Clicking an existing product name opens its detail view with an Edit option.

---

## Savings Products

The Savings Products page displays a filter bar and a data table with columns for Name (clickable link) and Short Name. A "+ Create Savings Product" button opens a stepper wizard. Step 1 (Details) contains Product Name (required), Short Name (required), Description, and External Id. Step 2 (Currency) contains Currency, Decimal Places, and Currency In Multiples Of. Step 3 (Terms) contains Nominal Annual Interest Rate, Interest Compounding Period (Daily, Monthly, Quarterly, Semi-Annual, Annually), Interest Posting Period (Monthly, Quarterly, Biannually, Annually), Interest Calculated Using (Daily Balance, Average Daily Balance), and Days in Year (360, 365, Actual). Step 4 (Settings) contains Minimum Opening Balance, Lock-in Period, Apply Withdrawal Fee for Transfers checkbox, Minimum Balance for Interest Calculation, Enforce Minimum Required Balance checkbox with Minimum Required Balance field, Is Overdraft Allowed checkbox with Maximum Overdraft Amount and Overdraft Interest Rate fields, Enable Withhold Tax checkbox with Tax Group dropdown, and Enable Dormancy Tracking checkbox with Days to Inactive, Days to Dormancy, and Days to Escheat fields. Step 5 (Charges) is a search-and-add interface for predefined charges. Step 6 (Accounting) contains a radio button for None or Cash-based; selecting Cash-based reveals GL account mappings for Savings Reference, Savings Control, Transfers in Suspense, Interest on Savings, Income from Fees, Income from Penalties, and Escheat Liability.

Fixed Deposit Products and Recurring Deposit Products follow the same stepper structure with additional steps. Fixed Deposit Products add a Pre-Closure step (Pre-Mature Closure Applicable checkbox, Pre-Closure Penal Interest, Pre-Closure Penal Interest On dropdown), a Deposit Term step (Minimum and Maximum Deposit Term with units, In Multiples Of, Minimum/Maximum/Default Deposit Amount), and an Interest Rate Chart step (tiered rates with Period From, Period To, Period Type, Interest Rate, and optional Amount Range slabs). Recurring Deposit Products additionally include Mandatory Recommended Deposit Amount, Is Mandatory Deposit checkbox, Allow Withdrawal checkbox, Adjust Advance Towards Future Payments checkbox, and Recurring Frequency with unit dropdown.

---

## Share Products

The Share Products page displays a data table with columns for Product Name (clickable link), Short Name, and Total Shares. A "+ Create Share Product" button opens a 7-step stepper wizard. Step 1 (Details) contains Product Name (required), Short Name (required), and Description (required). Step 2 (Currency) contains Currency, Decimal Places, and Currency In Multiples Of. Step 3 (Terms) contains Total Number of Shares (required), Shares to be Issued, Nominal/Unit Price (required), and Capital Value (auto-calculated). Step 4 (Settings) contains Allow Dividends for Inactive Clients checkbox, Minimum/Maximum/Nominal Shares per Client, Minimum Active Period Frequency, and Lock-in Period. Step 5 (Market Price) is a table where each row defines a From Date and Share Value; rows can be added or removed. Step 6 (Charges) is a search-and-add interface. Step 7 (Accounting) contains a radio button for None or Cash-based; selecting Cash-based reveals GL account mappings for Share Reference, Share Suspense, Equity in Shares, Income from Fees, and Share Equity. Clicking an existing product opens its detail view with Edit and Delete options.

---

## Charges

The Charges page displays a data table with columns for Name (clickable link), Charge Applies To, Is Penalty, Is Active, and Is Paid Derived. A "+ Create Charge" button opens the creation form containing Charge Name (required), Charge Applies To (Loan, Savings Account, Client, Shares — required), Currency (required), Charge Time Type (options vary by entity: for Loans includes Disbursement, Specified Due Date, Installment Fee, Overdue Fees, Tranche Disbursement; for Savings includes Specified Due Date, Savings Activation, Withdrawal Fee, Annual Fee, Monthly Fee, Overdraft Fee), Charge Calculation Type (Flat, Percentage of Amount, Percentage of Interest, Percentage of Total Outstanding), Amount (required), Is Penalty checkbox, Is Active checkbox, Tax Group dropdown, and Payment Mode (Regular, Account Transfer). Clicking "Submit" creates the charge definition. Clicking an existing charge opens its detail view with Edit and Delete options.

---

## Floating Rates

The Floating Rates page displays a data table with columns for Floating Rate Name (clickable link), Is Base Lending Rate, Is Active, and Created By. A "+ Create Floating Rate" button opens the creation form containing Floating Rate Name (required), Is Base Lending Rate checkbox (only one base rate can exist at a time), Is Active checkbox, and a Rate Periods table where each row has a From Date, Interest Rate (percentage), and Is Differential Rate checkbox (if checked, the rate is added to or subtracted from the base lending rate rather than used as an absolute value). Multiple rows can be added to define rate changes over time. When a loan product is linked to a floating rate, the loan's interest rate adjusts automatically based on the applicable rate period. The detail view shows the full rate history with an Edit option.

---

## Delinquency Management

The Delinquency pages cover two sub-pages: Delinquency Ranges and Delinquency Buckets. The Delinquency Ranges page displays a data table with columns for Classification (clickable link), Minimum Age Days, and Maximum Age Days. The Create Delinquency Range form contains Classification (required), Minimum Age Days (required), and Maximum Age Days (optional — if blank, applies to all days beyond the minimum). The Delinquency Buckets page displays a data table with columns for Bucket Name (clickable link) and associated ranges. The Create Delinquency Bucket form contains Bucket Name (required) and an interface for adding multiple delinquency ranges in sequence (e.g., 1–29 days = Range 1, 30–59 days = Range 2, 60+ days = Range 3). Delinquency buckets are linked to Loan Products; when a loan becomes overdue, the system automatically classifies it into the appropriate range based on days past due, which is used for portfolio-at-risk reporting, provisioning calculations, and collection workflow triggers.

---

## Loan Account

A new loan application is initiated from the Client Detail page. The Loan Application form is a multi-step wizard. Step 1 (Details) contains Product Name dropdown (selecting a product auto-populates default values), Loan Officer, Loan Purpose, Fund, Submitted On date, Expected Disbursement Date, Principal (bounded by product min/max), Number of Repayments, Repaid Every frequency and unit, Interest Rate (bounded by product min/max), and External ID. Step 2 (Terms) contains Repayment Strategy, Amortization, Interest Method, and Interest Calculation Period dropdowns (pre-filled from the product but adjustable), plus grace period fields. Step 3 (Charges) lists charges inherited from the product and includes an "Add Charge" button for additional charges. Step 4 (Collateral, optional) allows adding collateral items with Collateral Type, Value, and Description. Clicking "Submit" creates the loan in "Submitted and Pending Approval" status.

The Loan Detail page header displays the loan account number, product name, client name (clickable link), status badge, and loan balance. Status badges are color-coded: Submitted and Pending Approval (yellow), Approved (blue), Active (green), Closed (gray), Overpaid (purple), Written Off (red). Action buttons change based on status: Pending Approval offers Approve (dialog with Approved On Date, Approved Amount, Expected Disbursement Date, and Note), Reject, Withdraw, and Delete; Approved offers Disburse (form with Disbursed On Date, Transaction Amount, Payment Type — Cash, Check, Mobile Money, Bank Transfer — and payment detail fields; a "Disburse to Savings" option deposits directly into the client's linked savings account) and Undo Approval; Active offers Make Repayment (form with Transaction Date, Transaction Amount pre-filled with amount due, and Payment Type — partial repayments are applied per the configured repayment strategy; full settlement changes status to "Closed obligations met"), Waive Interest, Write Off, Close, Reschedule (form with Reschedule From Date, Reason, Adjusted Due Date, grace fields, Extra Terms, and New Interest Rate — creates a pending request requiring separate approval), Prepay Loan, Foreclosure, Charge Off, and Assign Loan Officer.

Tabs on the detail page show Summary (disbursement details, repayment schedule summary, total paid, total outstanding, total overdue, and charges summary), Repayment Schedule (table with Installment Number, Due Date, Principal Due, Interest Due, Fees Due, Penalties Due, Total Due, amounts paid, Total Outstanding, and status indicators), Transactions (table with Date, Type, Amount, Principal/Interest/Fees/Penalties portions, Outstanding Balance, and undo link), Charges (Charge Name, Amount, Due Date, Paid, Waived, Outstanding), Collateral, Notes, and Documents.

---

## Savings Account

A new savings account is created from the Client Detail page. The creation form contains Product Name dropdown (selecting a product auto-populates default values), Field Officer, Submitted On date, Nominal Annual Interest Rate, Interest Compounding Period, Interest Posting Period, Interest Calculated Using, Days in Year (all dropdowns, pre-filled from product), Minimum Opening Balance, Lock-in Period, Allow Overdraft checkbox, and a Charges section listing product charges with an option to add more. Clicking "Submit" creates the account in "Submitted and Pending Approval" status.

The Savings Account Detail page displays the account number, product name, client name, status badge, account balance, and available balance. Status badges include Submitted and Pending Approval, Approved, Active, Dormant, Closed, and Blocked. Action buttons change based on status: Pending offers Approve, Reject, and Withdraw Application; Approved offers Activate and Undo Approval; Active offers Deposit (form with Transaction Date, Transaction Amount, Payment Type — Cash, Check, Mobile Money — and payment detail fields; submitting credits the account), Withdraw (same form as Deposit — the system validates the withdrawal does not exceed available balance unless overdraft is enabled; if minimum balance is enforced and the withdrawal would breach it, an error is shown), Post Interest, Calculate Interest, Close, Block Account, Block Debit, and Block Credit. Tabs show Summary, Transactions (table of all deposits, withdrawals, and interest postings with Date, Type, Amount, and Running Balance), Charges, and Documents.

---

## Share Account

A new share account is created from the Client Detail page. The Share Account Application form contains Share Product dropdown (selecting a product auto-populates default values), Submitted On date, Requested Shares (bounded by product min/max per client), Application Date, Savings Account for Charges dropdown (lists the client's active savings accounts to debit fees from), External ID, and a Charges section. Clicking "Submit" creates the account in "Submitted and Pending Approval" status.

The Share Account Detail page displays the share account number, product name, client name, status badge, total approved shares, total pending shares, and unit price. Action buttons change based on status: Pending offers Approve (with Approved Shares and Approved Date) and Reject; Approved offers Activate and Undo Approval; Active offers Apply Additional Shares (purchase more shares), Redeem Shares (redemption amount is calculated as shares multiplied by current unit price and credited to the linked savings account), and Close. Tabs show Purchased Shares (table with Date, Type, Number of Shares, Unit Price, Amount, and Status), Dividends (posted dividend distributions with Date, Amount Per Share, and Total Amount), and Charges.

---

## Fixed & Recurring Deposit Accounts

Fixed Deposit and Recurring Deposit accounts are created from the Client Detail page. The FD Account creation form contains Fixed Deposit Product dropdown, Deposit Amount, Deposit Period (numeric and unit — Days, Months, Years), and Maturity Instructions (Transfer to Savings, Re-Invest, or Re-Invest Principal and Transfer Interest). The FD Account Detail page shows deposit amount, maturity date, maturity amount, interest rate, and status with action buttons for Approve, Activate, Premature Close, and Close on Maturity. The RD Account creation form contains Recurring Deposit Product dropdown, Mandatory Deposit Amount per installment, Deposit Period, Deposit Frequency (Daily, Weekly, Monthly, Quarterly, Yearly), and Expected First Deposit On date. The RD Account Detail page shows the deposit schedule, total deposits made, maturity details, interest rate, and status with action buttons for Approve, Activate, Deposit, Premature Close, and Close on Maturity. Both FD and RD detail pages include tabs for Summary, Transactions, and Charges. Interest rates are determined by the Interest Rate Chart configured on the product, with tiered rates based on deposit amount and term length.

---

## Accounting — Chart of Accounts

The Chart of Accounts page displays a hierarchical tree of all General Ledger accounts organized by type: Assets, Liabilities, Equity, Income, and Expenses. Each row shows GL Code, Account Name, Account Type (color-coded — Assets blue, Liabilities red, Equity green, Income purple, Expenses orange), Manual Entries Allowed indicator, Usage (Header or Detail), and Description. Header accounts serve as grouping parents; Detail accounts are used for actual journal postings. A "+ Create GL Account" button opens the creation form containing Account Type (required), Parent Account (dropdown listing header accounts of the same type), GL Code (required, must be unique — duplicates produce a validation error), Account Name (required), Account Usage (Header or Detail), Manual Entries Allowed checkbox, Description, and Tag dropdown. Clicking an account name opens its detail view with Edit and Delete options.

---

## Accounting — Journal Entries & Closures

The Journal Entries page displays a data table with columns for Entry ID, Office, Transaction Date, Created Date, Transaction ID, Type (Debit/Credit), GL Account, and Amount. A filter bar allows filtering by Office, GL Account, Date Range, Transaction ID, and Entry Type. A "+ Add Journal Entry" button opens the creation form containing Office (required), Currency (required), Reference Number, Transaction Date (required), Payment Type and payment detail fields, entry lines (each with a GL Account dropdown and Amount — an "Add Row" button adds additional lines), and Comments. A running total shows debit total, credit total, and difference; total debits must equal total credits or a validation error blocks submission.

The Closing Entries page displays a table with columns for Office, Closing Date, Created Date, and Comments. A "+ Create Closure" button opens the form with Office (required), Closing Date (required), and Comments. Creating a closure prevents journal entries from being posted for dates on or before the closing date, protecting completed accounting periods.

---

## Accounting Rules & Financial Activity Mappings

The Accounting Rules page displays a data table with columns for Rule Name (clickable link), Office, Debit Account(s), and Credit Account(s). A "+ Create Rule" button opens the creation form containing Office (dropdown — blank applies to all offices), Rule Name (required), Debit Tags/Debit Account (GL account dropdown or multi-select), Allow Multiple Debit Entries checkbox, Credit Tags/Credit Account, and Allow Multiple Credit Entries checkbox. Clicking a rule opens its detail view with Edit and Delete options.

The Financial Activity Mappings page displays a table mapping financial activities to GL accounts, where each row shows the Financial Activity (e.g., Asset Transfer, Liability Transfer, Cash at Mainvault, Cash at Teller, Opening Balances Transfer, Fund Source, Payable Dividends, Asset Fund Source, Overdraft Portfolio) and its mapped GL Account. A "+ Create Mapping" button opens the form with Financial Activity dropdown (listing unmapped activities) and GL Account dropdown. Each financial activity can only be mapped once; these mappings enable the system to automatically post accounting entries for internal transfers, teller operations, and other system-level financial activities.

---

## Provisioning

The Provisioning Criteria page displays a data table with columns for Criteria Name (clickable link) and Created Date. A "+ Create" button opens the creation form containing Criteria Name (required) and a Definitions table where each row specifies Loan Product, Category (STANDARD, SUB-STANDARD, DOUBTFUL, LOSS), Minimum Age (overdue days), Maximum Age (overdue days), Provisioning Percentage (percentage of outstanding principal), Liability Account (GL account dropdown), and Expense Account (GL account dropdown). Multiple rows can be added to cover different overdue ranges and product combinations.

The Provisioning Entries page lists all generated provisioning journal entries with columns for Entry Date, Journal Entry Created, Created By, and action buttons. A "+ Create Provisioning Entry" button generates new provisioning entries based on the current loan portfolio status and configured criteria; the system calculates the required provision amount for each loan category and creates the corresponding journal entries. Each entry can be reviewed (showing a detailed breakdown by loan product and category) or recreated.

---

## Offices

The Offices page displays a hierarchical table of all offices with columns for Office Name (clickable link), External ID, Parent Office, Opening Date, and hierarchy position. A "+ Create Office" button opens the creation form containing Office Name (required), Parent Office (required — Head Office is the root), Opened On Date (required), and External ID. The Office Detail page shows office information with an Edit option. Offices define the branch structure — clients, groups, staff, and accounting operations are all associated with specific offices.

---

## Employees

The Employees page displays a data table with columns for Name (clickable link), Office, Is Loan Officer indicator, and Status (Active, Inactive). A "+ Create Employee" button opens the creation form containing Office (required), First Name (required), Last Name (required), Is Loan Officer checkbox, Mobile Number, Is Active checkbox, Joining Date, and External ID. Staff members marked as Is Loan Officer appear in the Loan Officer dropdown when creating loans and can be assigned to clients, groups, and centers. The Staff Detail page shows employee information with an Edit option.

---

## Teller & Cashier Management

The Tellers page displays a data table with columns for Teller Name (clickable link), Office, Status (Active, Inactive), and Description. A "+ Create Teller" button opens the creation form containing Office (required), Teller Name (required), Description, Start Date (required), End Date, and Status (Active, Inactive). The Teller Detail page displays teller information with an Edit option and a Cashiers section listing all assignments with columns for Cashier Name, Start Date, End Date, Is Full Day, and Status. A "+ Allocate Cashier" button opens the allocation form with Staff (required), Start Date (required), End Date, Is Full Day checkbox, and Description. The Cashier Detail page shows Opening Balance and Cash In Hand, with actions for Allocate Cash (add cash from the vault) and Settle Cash (return cash to the vault — with Amount, Currency, and Transaction Date fields). A Cashier Transactions list shows all allocations, settlements, deposits, and withdrawals with columns for Date, Type, Amount, and Running Balance.

---

## Users & Roles

The Users page displays a data table with columns for Username (clickable link), First Name, Last Name, Email, Office, and Status. A "+ Create User" button opens the creation form containing Username (required, must be unique), First Name (required), Last Name (required), Email (required, validated for email format), Office (required), Staff dropdown (links the user to a staff record), Password (required, must meet password policy), Repeat Password (must match — shows a validation error if they differ), Roles (multi-select checkboxes), Override Password Expiry Policy checkbox, and Send Password to Email checkbox.

The Roles page displays all roles with Name and Description columns. A "+ Create Role" button opens a form with Role Name and Description. After creation, a permissions page displays a categorized matrix of all system permissions (User Management, Portfolio, Organization, Accounting, Reports, etc.) with checkboxes for each permission. Enabling or disabling permissions controls what menu items, pages, and actions the role can access.

---

## Reports

The Reports page lists available reports grouped by category: All, Clients, Loans, Savings, Funds, Accounting, and XBRL. Each row shows Name (clickable link), Type (Table, Pentaho, Chart), and Category. Clicking a report opens a parameters form with fields such as Office, Branch, Currency, Loan Product, Date Range, Loan Officer, and Fund dropdowns. A "Run Report" button generates the report as a data table with sorting and pagination. Output options include viewing on screen, exporting to Excel, CSV, or PDF. Common reports include Loans Awaiting Disbursal, Loans Pending Approval, Active Loans Summary, Active Loans Details, Obligation Met Loans Details, Portfolio at Risk, and Portfolio at Risk by Branch.

---

## Account Transfers & Standing Instructions

The Account Transfers form contains From Office, From Client, From Account Type (Savings Account, Loan Account), From Account, To Office, To Client, To Account Type, To Account, Transfer Amount (required), Transfer Date (required), and Description. If the transfer amount exceeds the available balance, an error is shown. Clicking "Submit" processes the transfer, debiting the source and crediting the destination.

The Standing Instructions page displays a data table with columns for Name, From Client, From Account, To Client, To Account, Amount, Validity (From/Till dates), and Status (Active, Disabled). A "+ Create Standing Instruction" button opens the creation form containing Name (required), From and To account fields, Transfer Type, Priority, Instruction Type (Fixed, Dues), Amount, Validity From and Till dates, Recurrence Type (Periodic, As Per Dues), Recurrence Frequency, and Recurrence Interval. Standing instructions can be enabled, disabled, or deleted from the listing.

---

## Tax Management

The Tax Components page displays a data table with columns for Name (clickable link), Percentage, Debit Account Type, Debit Account, Credit Account Type, Credit Account, and Start Date. A "+ Create Tax Component" button opens the creation form containing Name (required), Percentage (required), Debit Account Type (Asset, Liability, Equity, Income, Expense) and Debit Account (GL account), Credit Account Type and Credit Account (GL account), and Start Date (required).

The Tax Groups page displays a data table with columns for Name (clickable link) and associated components. A "+ Create Tax Group" button opens the form with Name (required) and a Tax Components section allowing multiple components to be added, each with a Start Date and End Date. Tax groups are referenced by Savings Products (Enable Withhold Tax checkbox with Tax Group dropdown) and Charge definitions; when a product has tax enabled, the system automatically applies the configured tax rate on interest income or fees and posts the corresponding journal entries to the mapped GL accounts.

---

## Organization Settings

The Organization section under the Admin menu provides access to several configuration pages. The Holidays page displays a table with columns for Name, Start Date, To Date, Status (Active, Pending), and Rescheduling Type. A "+ Create Holiday" button opens the form with Name (required), From Date (required), To Date (required), Repayments Rescheduled To date, Rescheduling Type dropdown, Description, and applicable Offices (multi-select). Holidays affect loan repayment schedules — installments falling on holidays are automatically rescheduled per the configured type.

The Working Days page allows configuring which days of the week are working days using checkboxes for Monday through Sunday, and a Repayment Rescheduling dropdown for handling repayments that fall on non-working days. The Currencies page allows selecting active currencies from a list, each showing Code, Name, and Decimal Places. The Funds page manages funding sources for loans with Fund Name and External ID columns and a Create Fund form. The Payment Types page lists all configured payment methods (Cash, Bank Transfer, Mobile Money, Check, Receipt) with columns for Name, Description, Is Cash Payment, and Position; a "+ Create" button adds new payment types that appear as dropdown options in all transaction forms. The Bulk Import page allows importing data for multiple entity types — Clients, Groups, Centers, Offices, Staff, Users, Loans, Savings, and more — each with a Download template button and an Upload interface.

---

## System Administration

The Manage Scheduler Jobs page displays a table of all batch jobs with columns for Job Name, Is Active (toggle), CRON Expression, Previous Run Status (Success/Failed with start/end times), Next Run Time, Currently Running indicator, and action buttons. Jobs include Apply Annual Fee, Add Accrual Transactions, Apply Penalty to Overdue Loans, Update Loan Summary, Post Interest for Savings, Transfer Fees, and Generate Loan Loss Provisioning. Each job can be toggled active/inactive and its CRON expression edited. A global Start/Stop scheduler toggle controls whether all scheduled jobs execute.

The Global Configuration page displays a table of system-wide feature flags with columns for Configuration Name, Enabled (toggle), Value, and Description. Key settings include maker-checker (4-eyes approval), reschedule-future-repayments, allow-transactions-on-non-workingday, reschedule-repayments-on-holidays, savings-interest-posting-current-period-end, financial-year-beginning-month, and meetings-mandatory-for-jlg-loans.

The Manage Codes page lists all code lists (Client Type, Gender, Address Type, Loan Purpose, etc.) with Name and Is System Defined columns. Clicking a code opens its values for adding, editing, reordering, and deactivating entries that populate dropdown options throughout the system.

The Manage Data Tables page lists custom data tables that extend core entities (m_client, m_group, m_loan, m_office, m_saving_account, m_product_loan, m_savings_product) with custom fields. The Create form includes Data Table Name, Application Table Name dropdown, Multi Row checkbox, and column definitions — each with Name, Type (string, number, boolean, decimal, date, datetime, text, dropdown), Length, Is Mandatory, and Is Unique checkboxes.

The Audit Trails page displays all system actions with columns for Action Name, Entity Name, Resource ID, Maker, Made On Date, Checker, Checked On Date, Processing Result (Pending, Approved, Rejected), Office Name, and Client/Loan/Savings details. Filters allow searching by Action Name, Entity Name, Resource ID, Maker ID, Checker ID, Office, and Date Range. When maker-checker is enabled, pending commands appear with Approve and Reject buttons.

---

## Logout

The logout function is accessible from the user profile icon in the top-right corner. Clicking the icon reveals a dropdown with Profile Settings and Log Out. Clicking "Log Out" terminates the authenticated session, clears the authentication token, and redirects to the login page. After logout, any attempt to navigate to an authenticated page redirects to the login page.