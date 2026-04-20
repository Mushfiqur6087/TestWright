# Phptravels — Verifications

**Base URL:** 
**Generated:** 2026-04-20T19:08:30.965513
**Source test cases:** Output/PHPTravels/test-cases.json
**Source spec files:**
- Dataset/PHPTravels/PHPTravels.md

## Coverage Summary

| Coverage | Count |
|----------|-------|
| Verifiable | 13 |
| Manual only | 13 |
| Not coverable | 0 |
| **Total records** | **26** |

### Breakdown by verification type

| Type | Count |
|------|-------|
| same_actor_navigation | 13 |
| cross_actor | 0 |
| unobservable_by_design | 0 |
| out_of_band | 13 |

---

## Verifications

### Module 13

#### 13.VISSER-007

- **Type:** `same_actor_navigation`
- **Coverage:** `verifiable`

**Pre-check**
- navigate_to: Visa Services
- observe:
  - Uploaded supporting documents list does not contain entries for the test files to be attached (e.g., passport copy, photograph, invitation letter, additional supporting documents)

**Test case context**
- title: Upload multiple supporting documents and verify all are retained
- workflow: Attach required files such as passport copy, photographs, invitation letter, and supporting documents
- execution_page: Visa Services -> Booking Management
- test_steps:
  - Attach multiple Supporting Document files using the supporting documents upload control
  - Click "Submit"
  - Verify each supporting document is listed under uploaded supporting documents
- expected_result: All uploaded supporting documents are listed, retained after submission, and available for download or preview.

**Post-check**
- navigate_to: Booking Management
- observe:
  - Presence of uploaded supporting document entry for passport copy (uploaded test file)
  - Presence of uploaded supporting document entry for photograph (uploaded test file)
  - Presence of uploaded supporting document entry for invitation letter (uploaded test file)
  - Presence of any additional supporting document entries uploaded in the test
  - Download or preview control available for each uploaded document entry
- expected_change: Each previously-absent uploaded document (passport copy, photograph, invitation letter, and any additional supporting documents uploaded during the test) appears in the application's document list after submission and remains present in Booking Management; each document entry provides a working download or preview action that returns the correct file.

---

### Module 14

#### 14.USEDAS-008

- **Type:** `out_of_band`
- **Coverage:** `manual_only`
- **Coverage note:** The booking confirmation file is delivered to the user's device via the browser download flow (outside the web UI). The application cannot assert that the file was saved to the user's filesystem or that the browser download dialog was presented. Verification requires access to the user's browser download dialog, the downloaded file in the filesystem, or a network capture of the PDF response (e.g., configured browser automation).

- trigger_action: On User Dashboard → My Bookings, locate a booking row with status 'Confirmed' and click the 'Download Confirmation' action for that booking row.
- channel: file_download
- recipient: authenticated user's browser / client device
- expected_content:
  - Unique booking reference number (must match reference shown in User Dashboard)
  - Service type and provider (e.g., Hotel name or Flight itinerary)
  - Lead passenger / guest full name
  - Travel dates (check-in/check-out or flight dates)
  - Total amount paid and currency
  - Booking status marked as 'Confirmed'
  - Cancellation policy summary and contact information
- in_app_partial_check:
  - navigate_to: User Dashboard
  - observe: Booking row with status 'Confirmed' showing a 'Download Confirmation' action; booking reference visible in the row (reference used to match the downloaded file)
- verification_method: Manual: Trigger the download and confirm the browser download dialog appears or check the browser's Downloads list; open the downloaded file (PDF) and verify each expected_content item and that the booking reference matches the dashboard. Automated option (if available): run browser automation configured to auto-save downloads to a known folder or capture the HTTP response for the confirmation PDF and validate its contents.

#### 14.USEDAS-009

- **Type:** `out_of_band`
- **Coverage:** `manual_only`
- **Coverage note:** Invoice delivery is an external file download (PDF) saved to the user's device or opened by the browser. This side effect cannot be fully confirmed by navigating within the PHPTravels UI; it requires access to the test machine's download folder or a browser automation harness that captures downloads.

- trigger_action: Click the 'Download Invoice' button for the selected booking row in the My Bookings listing
- channel: file_download
- recipient: authenticated user's browser / local filesystem
- expected_content:
  - PDF file (Content-Type: application/pdf)
  - Booking reference number that matches the selected booking
  - Service type and provider (e.g., Hotel/Flight/Tour/Car)
  - Passenger/guest name
  - Travel dates
  - Itemized charges and total amount charged
  - Invoice date and billing details (payer information)
- in_app_partial_check:
  - navigate_to: User Dashboard
  - observe: In My Bookings listing, the 'Download Invoice' action/button is present for the booking row and is clickable; clicking the control initiates a browser download (download prompt or automatic save) or opens the PDF in a new tab.
- verification_method: Manual verification: confirm a PDF file is saved to the test machine's download directory (or opened in the browser) within 2 minutes of clicking. Open the PDF and verify all expected_content items are present. Automated option: run browser test with controlled download directory and assert a new PDF file appears and its contents (text-extract) include the expected items.

#### 14.USEDAS-010

- **Type:** `out_of_band`
- **Coverage:** `manual_only`
- **Coverage note:** The primary effect is a file download / PDF open in the user's browser which cannot be fully observed from within the application UI or by a standard in-app automated check. Verifying the downloaded file requires access to the browser download artifact or interception of the HTTP response (download stream) which is outside the app UI.

- trigger_action: On the Booking Details page, click the 'Download Invoice' button for the booking with an available invoice.
- channel: file_download
- recipient: authenticated user's browser (download folder or PDF viewer)
- expected_content:
  - Invoice number / reference matching the booking
  - Booking reference number
  - Guest / lead passenger name
  - Service provider name (hotel/flight/car/etc.) and address
  - Travel/check-in and check-out dates (or flight dates)
  - Invoice issue date
  - Line-item price breakdown (room rate, taxes, fees) and total amount
  - Company billing details (if applicable) and VAT/tax identifiers
- in_app_partial_check:
  - navigate_to: Booking Management
  - observe: Booking detail shows 'Invoice available' indicator and the invoice reference number (if displayed) or a downloadable invoice link/button
- verification_method: Manual: Confirm the browser initiates a download or opens a PDF within the browser when 'Download Invoice' is clicked. Locate the downloaded file in the browser's Downloads folder or opened PDF viewer and verify the PDF contains all expected_content items. Alternatively, use a test harness capable of intercepting the HTTP response for the invoice endpoint to save the PDF and validate its contents programmatically.

#### 14.USEDAS-012

- **Type:** `out_of_band`
- **Coverage:** `manual_only`
- **Coverage note:** Voucher file download is an external browser action (file saved to the user's device or opened in a new tab). This cannot be fully observed from within the PHPTravels UI. Verification requires access to the test browser's downloads (or a headless browser configured to capture downloads) or a network capture/proxy that records the voucher response.

- trigger_action: On My Bookings, click the 'Download Vouchers' action for the selected booking
- channel: file_download
- recipient: authenticated user's browser (current session) / user's device
- expected_content:
  - PDF voucher file containing the booking reference number
  - Service name (hotel/flight/tour/car) and provider details
  - Guest/lead passenger name
  - Travel dates (check-in/check-out or travel date)
  - Booking reference and booking date
  - Price/total amount charged and tax/fee breakdown
  - Voucher terms and cancellation policy or instructions
- in_app_partial_check:
  - navigate_to: User Dashboard
  - observe: Booking row contains 'Download Vouchers' action; any immediate UI indicator (toast or ephemeral message) stating 'Download started' or a new tab was opened
- verification_method: Confirm manually by checking the browser's Downloads list or the opened tab displays the voucher PDF. Alternatively, use a headless browser configured to capture downloads or a network proxy (e.g., BrowserMob, mitmproxy) to capture the voucher file response and validate the PDF contains the expected_content.

#### 14.USEDAS-013

- **Type:** `same_actor_navigation`
- **Coverage:** `verifiable`

**Pre-check**
- navigate_to: User Dashboard
- observe:
  - Selected completed booking entry in My Bookings shows no existing review (no star rating or review text visible in its booking detail)
  - User's Reviews list does not contain an entry for the selected booking reference

**Test case context**
- title: Submit rating and review for a completed booking
- workflow: Rating and reviewing completed bookings
- execution_page: User Dashboard -> Reviews & Ratings
- test_steps:
  - Locate a completed booking in the past bookings list on the My Bookings page
  - Click the booking's "Review" or "Write Review" action
  - Fill all required fields (Rating, Review text)
  - Click "Submit Review"
- expected_result: Review is saved; the rating and review text appear on the booking detail and in the user's Reviews list.

**Post-check**
- navigate_to: Reviews & Ratings
- observe:
  - Review entry for the booking showing submitted star rating and review text
  - Booking detail displays the submitted star rating and review text
- expected_change: A new review entry appears in Reviews & Ratings containing the submitted star rating and review text associated with the completed booking; the booking's detail view now displays the submitted rating and review text.

#### 14.USEDAS-017

- **Type:** `same_actor_navigation`
- **Coverage:** `verifiable`

**Pre-check**
- navigate_to: User Dashboard
- observe:
  - state of the notification preference controls to be modified (e.g., Email notifications toggle, SMS notifications toggle, Push notifications toggle)

**Test case context**
- title: Notification preference changes persist after page refresh
- workflow: Change notification preferences
- execution_page: User Dashboard
- test_steps:
  - Modify notification preference controls (enable or disable desired notification channels)
  - Click the "Save" (or "Update") button in the Notification Preferences section
  - Refresh the Settings page
- expected_result: Notification preferences retain the saved selections after the page refresh.

**Post-check**
- navigate_to: User Dashboard
- observe:
  - state of the notification preference controls that were modified (e.g., Email notifications toggle, SMS notifications toggle, Push notifications toggle)
- expected_change: After saving and refreshing the Settings page, the state of each modified notification preference control equals the value recorded in pre_check (each toggle shows the same enabled/disabled state that was selected before saving).

#### 14.USEDAS-026

- **Type:** `out_of_band`
- **Coverage:** `manual_only`
- **Coverage note:** Confirmation file download is an external browser/OS-side effect (file saved to disk or served over HTTP) and cannot be fully confirmed by inspecting the PHPTravels UI DOM alone. Verifying the actual file arrival and its contents requires access to the test browser's download directory or network/proxy capture or a manual inspection of the downloaded file.

- trigger_action: On User Dashboard -> My Bookings, for each identified past and upcoming booking, click the 'Download Confirmation' action.
- channel: file_download
- recipient: authenticated user's browser / download directory
- expected_content:
  - Unique booking reference number
  - Lead passenger / booking holder name
  - Service type and provider (Hotel/Flight/Tour/Car) and identifying details (hotel name or flight itinerary)
  - Travel dates (check-in/check-out or departure/arrival) matching the booking
  - Booking status (Confirmed / Pending / Cancelled)
  - Total amount paid and currency
  - Issuer information (booking site name and contact or booking agent details)
- in_app_partial_check:
  - navigate_to: User Dashboard
  - observe: Presence of past and upcoming bookings rows with visible booking reference, travel dates, status, and an enabled 'Download Confirmation' action/button for each identified booking
- verification_method: Use browser automation configured with a dedicated download directory (or intercept network response) to click the download action and confirm a file appears within a short timeout. Open the downloaded PDF/ document and validate it contains all expected_content items. Alternatively, manually perform the download and inspect the saved file or check captured HTTP response headers (Content-Disposition, Content-Type) and response body for the confirmation document.

---

### Module 15

#### 15.BOOMAN-003

- **Type:** `out_of_band`
- **Coverage:** `manual_only`
- **Coverage note:** Booking modification notifications are sent via email and cannot be observed within the PHPTravels UI. Verification requires access to a test inbox or email logs (e.g., Mailtrap, Mailhog, or SMTP logs).

- trigger_action: Click 'Modify' on an existing permitted booking, enter a valid Special Requests description, and click 'Save' or 'Confirm' to apply changes
- channel: email
- recipient: lead passenger / booking contact email associated with the booking
- expected_content:
  - Modification notification subject indicating booking was modified
  - Unique booking reference number
  - Summary of changes including the updated Special Requests text
  - Modification timestamp and/or 'Last modified' indicator
  - Contact or support information and sender identity (e.g., noreply@ domain)
- in_app_partial_check:
  - navigate_to: Booking Management
  - observe: Booking detail shows Special Requests field updated to the entered text and a modification timestamp or 'Last modified' note
- verification_method: Access the test inbox (Mailtrap, Mailhog, or equivalent) for the booking contact email within 2 minutes of saving changes. Confirm an email was delivered and contains all expected_content items and that the Special Requests text and timestamp match the Booking Management detail view.

#### 15.BOOMAN-004

- **Type:** `out_of_band`
- **Coverage:** `manual_only`
- **Coverage note:** Booking modification notification is sent via email and cannot be observed within the application UI. Requires access to a test inbox (Mailtrap/Mailhog) or email server logs to confirm delivery and content.

- trigger_action: On the open booking detail in Booking Management, click 'Modify', change the Special Requests field to a different valid description, and click 'Save'/'Confirm' to submit the modification.
- channel: email
- recipient: lead passenger email address on the booking
- expected_content:
  - Email subject indicating booking modification (e.g., 'Your booking has been modified')
  - Booking reference number
  - Identification of the modified field(s) (Special Requests) and the updated special requests text matching the new description
  - Modification date and time
  - Link to the booking detail page or instructions to view the updated booking in the user's dashboard
- in_app_partial_check:
  - navigate_to: Booking Management
  - observe: Special Requests field on the booking detail displays the updated description
- verification_method: Access the test inbox (Mailtrap, Mailhog, or equivalent) for the lead passenger email address or review email delivery logs. Confirm the modification email arrives within 2 minutes and contains all expected_content items, and that the Special Requests text in the email matches the updated text shown in Booking Management.

#### 15.BOOMAN-008

- **Type:** `same_actor_navigation`
- **Coverage:** `verifiable`
- **Coverage note:** Only the in-app booking status and the creation of a refund transaction in the booking's payment history can be verified. Email notification delivery and final settlement of the refund by the external payment processor cannot be observed within the application UI and require access to the test inbox and payment gateway logs.

**Pre-check**
- navigate_to: Booking Management
- observe:
  - booking status for the booking currently open (e.g., 'Confirmed' or 'Pending')
  - booking payment history: absence of any refund transaction for this booking
  - original payment method as shown in booking payment details (e.g., masked card, PayPal identifier, or bank reference)

**Test case context**
- title: Cancel booking and initiate refund to the original payment method
- workflow: cancellation is processed and a refund is initiated to the original payment method (after explicit confirmation)
- execution_page: Booking Management
- test_steps:
  - Click "Cancel" on the booking detail page
  - In the cancellation confirmation flow verify the applicable refund amount and that the original payment method is referenced
  - Explicitly confirm the cancellation
- expected_result: Booking status changes to "Cancelled", a refund is initiated to the original payment method, and an email notification is sent for the cancellation.

**Post-check**
- navigate_to: Booking Management
- observe:
  - booking status for the booking
  - booking payment history entry for refund including refund amount and referenced payment method
  - booking row status in the Booking Management list
- expected_change: Booking status changes from the pre_check observed value to 'Cancelled'; a new refund transaction appears in the booking's payment history with an amount equal to the applicable refund amount shown during cancellation and the payment method referencing the original payment method; the booking is marked 'Cancelled' in the Booking Management list.

---

### Module 16

#### 16.PAYPRO-002

- **Type:** `out_of_band`
- **Coverage:** `manual_only`
- **Coverage note:** Confirmation email is sent to the user's external email inbox and cannot be observed within the application UI. Verifying email delivery and content requires access to a test inbox (Mailtrap/Mailhog) or email server/logs.

- trigger_action: Complete payment by selecting Credit/Debit Card → MasterCard, entering valid card details (cardholder name, card number, expiration date, CVV), and clicking 'Pay'.
- channel: email
- recipient: lead passenger email address entered on the booking/payment form
- expected_content:
  - Booking confirmation subject line referencing confirmation/booking
  - Unique booking reference number (must match reference shown on confirmation page)
  - Service type and provider name (e.g., Hotel name or Flight itinerary)
  - Travel dates (check-in/check-out or flight dates)
  - Total amount charged and currency
  - Invoice as attachment or download link
  - Voucher as attachment or download link
  - Cancellation policy summary or link
  - Support/contact information
- in_app_partial_check:
  - navigate_to: Booking Management
  - observe: Booking reference number and options to download invoice and voucher visible on the booking details page (reference must match the one received by email)
- verification_method: Inspect test inbox (Mailtrap/Mailhog) or email server logs. Confirm an email is delivered to the recipient within 2 minutes of payment and that the message contains all expected_content items. Verify the booking reference in the email matches the reference shown in the application Booking Management page.

#### 16.PAYPRO-003

- **Type:** `same_actor_navigation`
- **Coverage:** `verifiable`

**Pre-check**
- navigate_to: Payment Processing
- observe:
  - booking summary details (service type and name, travel dates)
  - booking total amount shown on the page

**Test case context**
- title: Successful payment with American Express leads to booking confirmation
- workflow: Pay with Credit/Debit Card
- execution_page: Payment Processing -> Booking Management
- test_steps:
  - Select the Credit/Debit Card payment method and choose American Express
  - Fill all required card fields (cardholder name, card number, expiration date, CVV)
  - Click "Pay"
- expected_result: User is taken to a booking confirmation page with a reference number; options to download the invoice and voucher are available; a confirmation email is sent

**Post-check**
- navigate_to: Booking Management
- observe:
  - booking reference number (most recent booking)
  - booking status
  - Download Invoice button
  - Download Voucher button
  - booking total amount displayed in booking details
- expected_change: A new booking entry appears in Booking Management with a non-empty booking reference number and booking status 'Confirmed'; 'Download Invoice' and 'Download Voucher' buttons are present; the booking total amount shown in the booking details equals the booking total amount observed on the Payment Processing page; booking details (service, dates) match the pre-check booking summary.

#### 16.PAYPRO-006

- **Type:** `out_of_band`
- **Coverage:** `manual_only`
- **Coverage note:** Confirmation email is sent to the customer's email address outside the PHPTravels UI and cannot be observed from within the application. Verifying email delivery and content requires access to the recipient mailbox or an email-testing tool (e.g., Mailtrap, Mailhog) or email logs.

- trigger_action: Complete PayPal checkout flow and return to the site (Pay with PayPal authorization and payment completion).
- channel: email
- recipient: email address entered in the booking lead passenger form
- expected_content:
  - Unique booking reference number
  - Booking confirmation subject line (e.g., 'Booking Confirmation' or containing the reference)
  - Invoice (PDF or link) that includes booking reference and total amount charged
  - Voucher (PDF or link) for the booked service
  - Booked service details (hotel/flight/car/tour name, dates, traveler name(s))
  - Payment method indicated as PayPal
  - Booking date/time
- in_app_partial_check:
  - navigate_to: Booking Management
  - observe: Confirmation page/reference displayed and visible links/buttons to download invoice and voucher (reference number shown on page should match reference in the email).
- verification_method: Check the lead passenger's test inbox (Mailtrap, Mailhog, or real inbox) within 5 minutes of booking. Confirm an email arrives with subject containing 'Booking Confirmation' or the booking reference. Verify the email body includes all expected_content items and that invoice and voucher attachments or links are present and download correctly. Confirm the booking reference in the email matches the reference displayed in-app.

#### 16.PAYPRO-008

- **Type:** `out_of_band`
- **Coverage:** `manual_only`
- **Coverage note:** Confirmation email is sent outside the application UI and cannot be observed from within PHPTravels. Verification requires access to the recipient inbox or email delivery tooling (Mailtrap/Mailhog/test inbox) or email server logs.

- trigger_action: On Payment Processing page, select 'Bank Transfer', follow bank transfer instructions or upload transfer receipt, then submit transfer details to complete booking
- channel: email
- recipient: lead passenger email address entered on the payment page
- expected_content:
  - Booking confirmation subject line indicating successful booking
  - Unique booking reference number
  - Service type and booked item (e.g., hotel name or flight itinerary) matching the booking
  - Check-in and check-out dates or travel dates as applicable
  - Total amount charged or payment status indicating bank transfer pending/received
  - Downloadable invoice and/or voucher link or attachment
  - Bank transfer receipt acknowledgement or instructions reference (if applicable)
  - Cancellation policy summary and contact/support information
- in_app_partial_check:
  - navigate_to: Booking Management
  - observe: Booking reference number displayed on confirmation/booking detail page and Download Invoice/Voucher buttons present — reference should match the one in the email
- verification_method: Access the test inbox (Mailtrap, Mailhog, or equivalent) for the lead passenger email or check email server delivery logs. Confirm the confirmation email is received within 5 minutes of submission, verify the presence of all expected_content items, and ensure the booking reference in the email matches the in-app confirmation.

#### 16.PAYPRO-009

- **Type:** `out_of_band`
- **Coverage:** `manual_only`
- **Coverage note:** Booking confirmation email is sent to an external inbox and cannot be observed within the PHPTravels UI. Requires access to the test inbox (Mailtrap/Mailhog) or the user's email account or email logs to verify delivery and content.

- trigger_action: Complete payment using Wallet/Credits on the Payment Processing page when wallet balance is sufficient to cover the booking total
- channel: email
- recipient: email address entered as lead passenger (authenticated user's email if prefilled)
- expected_content:
  - Booking confirmation subject containing the booking reference number
  - Unique booking reference number
  - Booking details (service type, hotel/flight/tour/car name, travel dates)
  - Total amount charged and price breakdown
  - Links or attachments to download the invoice
  - Links or attachments to download the voucher/confirmation
  - Cancellation policy summary and contact/support information
- in_app_partial_check:
  - navigate_to: Booking Management
  - observe: Booking reference number displayed on the confirmation/booking details page and visible 'Download Invoice' and 'Download Voucher' options
- verification_method: Check the test inbox (Mailtrap, Mailhog, or equivalent) for the recipient address. Confirm email arrives within 2 minutes of payment. Verify the email subject contains the booking reference, the body includes all expected_content items, and invoice/voucher links or attachments are present and match the reference shown in the in-app booking details.

#### 16.PAYPRO-011

- **Type:** `same_actor_navigation`
- **Coverage:** `verifiable`
- **Coverage note:** Confirmation email delivery cannot be observed from within the application UI; email delivery must be verified using a test inbox (Mailtrap/Mailhog) or email logs.

**Pre-check**
- navigate_to: Payment Processing
- observe:
  - full booking summary including base price
  - taxes amount
  - service fees amount
  - applicable discounts amount
  - total amount payable

**Test case context**
- title: Retry payment succeeds and displays booking confirmation with downloads and email
- workflow: Retry payment
- execution_page: Payment Processing -> Booking Management
- test_steps:
  - Confirm the page displays a full booking summary with a price breakdown (base price, taxes, service fees, applicable discounts, total)
  - Click "Retry Payment"
  - Fill valid payment details and click "Pay"
- expected_result: User is taken to a booking confirmation page with a reference number; options to download the invoice or voucher are available and a confirmation email is sent.

**Post-check**
- navigate_to: Booking Management
- observe:
  - booking reference number displayed on confirmation/booking page
  - invoice download link/button
  - voucher download link/button
  - booking price breakdown (base price, taxes, fees, discounts, total) as shown on booking record
- expected_change: User is redirected to a booking confirmation view in Booking Management showing a new booking with a visible reference number; invoice and voucher download options are present and accessible; the booking's price breakdown matches the pre-check payment summary. (Confirmation email is expected to have been sent to the user's email — see coverage_note for verification method.)

#### 16.PAYPRO-024

- **Type:** `same_actor_navigation`
- **Coverage:** `verifiable`

**Pre-check**
- navigate_to: Payment Processing
- observe:
  - count of saved cards for the signed-in user
  - list of saved cards showing cardholder name and last four digits

**Test case context**
- title: Pay and save card for future use completes booking
- workflow: Pay with Credit/Debit Card
- execution_page: Payment Processing
- test_steps:
  - Select the Credit/Debit Card payment method
  - Fill all required card fields (cardholder name, card number, expiration date, CVV) and enable the option to save the card for future use
  - Click "Pay"
- expected_result: Booking confirmation page is displayed with a reference number and download options available; payment completes successfully

**Post-check**
- navigate_to: Payment Processing
- observe:
  - count of saved cards for the signed-in user
  - list of saved cards showing cardholder name and last four digits
- expected_change: Saved cards count increases by 1 compared to pre-check; a new saved card appears in the list with the cardholder name and the same last four digits as the card used during payment.

#### 16.PAYPRO-027

- **Type:** `out_of_band`
- **Coverage:** `manual_only`
- **Coverage note:** Invoice and voucher files are downloaded to the user's device (outside the application UI). This cannot be confirmed solely by in-app checks; requires access to the browser download folder or a download-interception tool (e.g., Selenium configured download directory or a proxy) to validate the files and their contents.

- trigger_action: Click 'Download Invoice' and 'Download Voucher' actions on the booking confirmation page after completing payment via Bank Transfer
- channel: file_download
- recipient: end-user's browser / download directory
- expected_content:
  - Invoice PDF contains booking reference number
  - Invoice PDF shows billed amount, taxes/fees, and payment method 'Bank Transfer'
  - Invoice PDF includes billing/lead passenger name and contact details
  - Voucher PDF contains service/hotel name, check-in and check-out dates (or service dates), guest name, and booking reference number
  - Both files are valid, well-formed PDF files and are downloadable
- in_app_partial_check:
  - navigate_to: Payment Processing
  - observe: Booking confirmation reference number displayed and 'Download Invoice' and 'Download Voucher' action buttons present on the confirmation page
- verification_method: Manual or automated: verify presence of downloaded files in the test browser's configured download directory or capture them via a network proxy. Open PDFs to confirm expected_content items are present. Automation requires configuring the browser profile to auto-download to a known folder and validating file existence and contents programmatically.

---

### Module 17

#### 17.C&LS-002

- **Type:** `same_actor_navigation`
- **Coverage:** `verifiable`

**Pre-check**
- navigate_to: Hotels Search & Listing
- observe:
  - selected currency displayed in header currency selector (currency code)
  - price displayed on the first hotel card (currency symbol and numeric amount)

**Test case context**
- title: Authenticated user's selected currency persists across page reload
- workflow: The currency selector updates all prices displayed across the site in real-time without losing the user's current search context
- execution_page: Hotels Search & Listing
- test_steps:
  - Click the Currency selector and choose a different currency
  - Refresh the current page
- expected_result: The selected currency remains active after reload and displayed prices continue to show the selected currency (preference saved to profile).

**Post-check**
- navigate_to: Hotels Search & Listing
- observe:
  - selected currency displayed in header currency selector (currency code)
  - price displayed on the first hotel card (currency symbol and numeric amount)
- expected_change: After page reload, the selected currency shown in the header currency selector matches the value recorded in pre_check; prices on the page continue to display using that same currency code/symbol (i.e., currency unit unchanged from pre_check).

---

### Module 19

#### 19.R&R-001

- **Type:** `same_actor_navigation`
- **Coverage:** `verifiable`

**Pre-check**
- navigate_to: Hotel Details & Booking
- observe:
  - aggregate rating score for the item being reviewed
  - total review count for the item being reviewed
  - absence of a review entry by the current user matching the intended stay date and review text

**Test case context**
- title: Submit a review through the dashboard (without photos)
- workflow: Submit a review through the dashboard
- execution_page: Hotel Details & Booking
- test_steps:
  - Fill all required fields in the dashboard review form (overall star rating, category-specific ratings, stay date, written feedback)
  - Click "Submit"
- expected_result: Review is submitted and success confirmation is shown; the review appears in the item's Reviews section showing overall rating, category-specific ratings, reviewer name and country, review date, stay date, and written comments; the listing's aggregate rating score and total review count reflect the new review.

**Post-check**
- navigate_to: Hotel Details & Booking
- observe:
  - new review entry in the Reviews section matching reviewer name and country, overall star rating, category-specific ratings, stay date, review date, and written comments
  - aggregate rating score for the item being reviewed
  - total review count for the item being reviewed
- expected_change: Total review count increased by 1 compared to pre_check; a new review entry appears in the Reviews section showing the submitted overall star rating, category-specific ratings, reviewer name and country, review date matching the submission date, stay date as submitted, and the written comments; aggregate rating updated from the pre_check value to reflect inclusion of the newly submitted overall rating.

#### 19.R&R-002

- **Type:** `same_actor_navigation`
- **Coverage:** `verifiable`

**Pre-check**
- navigate_to: Hotel Details & Booking
- observe:
  - aggregate rating value displayed in the Reviews section for the booked property (numeric)
  - total review count displayed in the Reviews section (numeric)
  - absence of a review matching the test submission data (reviewer name used in test, stay date used in test, and written feedback text)

**Test case context**
- title: Submit a review through the dashboard including guest-uploaded photos
- workflow: Submit a review through the dashboard
- execution_page: Hotel Details & Booking
- test_steps:
  - Fill all required fields in the dashboard review form (overall star rating, category-specific ratings, stay date, written feedback) and attach one or more guest photos
  - Click "Submit"
- expected_result: Review is submitted and success confirmation is shown; the review appears in the item's Reviews section including the guest-uploaded photos alongside overall rating, category-specific ratings, reviewer name and country, review date, stay date, and written comments; listing aggregate rating and total review count update accordingly.

**Post-check**
- navigate_to: Hotel Details & Booking
- observe:
  - presence of a review entry matching the submitted data: reviewer name, reviewer country, stay date, written comments, overall star rating, category-specific ratings
  - guest-uploaded photos displayed inline with the new review entry
  - total review count displayed in the Reviews section (numeric)
  - aggregate rating value displayed in the Reviews section (numeric)
- expected_change: A new review matching the submitted data appears in the property's Reviews section with guest-uploaded photos visible inline; total review count increases by 1 compared to pre_check; aggregate rating is recalculated to include the new overall star rating (agent should compute expected new aggregate from pre_check aggregate and pre_check count plus the submitted rating).

#### 19.R&R-004

- **Type:** `same_actor_navigation`
- **Coverage:** `verifiable`

**Pre-check**
- navigate_to: Hotel Details & Booking
- observe:
  - current aggregate rating for the hotel (numeric value)
  - current total review count for the hotel (integer)
  - absence of a review matching the submitted review text and submitted overall rating

**Test case context**
- title: Submit review via post-stay email prompt (authenticated completed booking)
- workflow: Submit a review via a post-stay email prompt
- execution_page: Hotel Details & Booking
- test_steps:
  - Fill all required fields (Overall rating, category-specific ratings, written feedback) and optionally attach photos
  - Click "Submit"
- expected_result: Review is saved and a submission confirmation is shown; the review will appear in the item's Reviews section and contribute to the aggregate rating and total review count.

**Post-check**
- navigate_to: Hotel Details & Booking
- observe:
  - aggregate rating for the hotel (numeric value)
  - total review count for the hotel (integer)
  - presence of a review in the Reviews section matching the submitted overall rating, category-specific ratings, written feedback, and any attached photos
- expected_change: Total review count increased by 1 compared to pre_check.total review count; a new review appears in the Reviews section matching the submitted overall rating, category ratings, written feedback, and any attached photos; aggregate rating updated to include the new review (i.e. new aggregate = (pre_check.aggregate_rating * pre_check.total_review_count + submitted_overall_rating) / (pre_check.total_review_count + 1)).

#### 19.R&R-006

- **Type:** `same_actor_navigation`
- **Coverage:** `verifiable`

**Pre-check**
- navigate_to: Hotels Search & Listing
- observe:
  - aggregate rating score for the item
  - total review count for the item

**Test case context**
- title: Listing page reflects updated aggregate rating and total review count after review submission
- workflow: Submit a review via a post-stay email prompt
- execution_page: Hotels Search & Listing
- test_steps:
  - View the item's listing card or row
  - Inspect the displayed aggregate rating score and total review count for the item
- expected_result: The aggregate rating score and total review count reflect the newly submitted review.

**Post-check**
- navigate_to: Hotels Search & Listing
- observe:
  - aggregate rating score for the item
  - total review count for the item
- expected_change: Total review count increased by 1 compared to pre_check; aggregate rating score updated to the recalculated average that includes the new review (compare post-check value to pre_check value to confirm the change—if the new review's rating differs from the pre_check average, the aggregate rating should change accordingly).

#### 19.R&R-014

- **Type:** `same_actor_navigation`
- **Coverage:** `verifiable`

**Pre-check**
- navigate_to: Hotel Details & Booking
- observe:
  - current review count displayed in Reviews section
  - absence of a review by the current user for the stay date in the Reviews section

**Test case context**
- title: Include guest-uploaded photos when submitting a review via post-stay email prompt
- workflow: Submit a review via a post-stay email prompt
- execution_page: Hotel Details & Booking
- test_steps:
  - Attach one or more photos using the review photo upload control
  - Fill all other required fields (Overall rating, category-specific ratings, written feedback)
  - Click "Submit"
- expected_result: Review is saved and the guest-uploaded photos appear with the review on the detail page.

**Post-check**
- navigate_to: Hotel Details & Booking
- observe:
  - new review entry by the current user in the Reviews section
  - photo thumbnails displayed with the new review corresponding to each uploaded image
- expected_change: Review count increased by 1 compared to pre_check; a new review by the current user appears in the Reviews section showing the submitted overall and category ratings and written feedback; guest-uploaded photo thumbnails are displayed with the new review (one thumbnail per uploaded photo).

---

### Module 4

#### 4.FORPAS-001

- **Type:** `out_of_band`
- **Coverage:** `manual_only`
- **Coverage note:** Password reset delivery occurs via email outside the application UI and cannot be observed by an automated in-app agent. Requires access to a test inbox (Mailtrap, Mailhog, or equivalent) or email/server logs to confirm delivery and content. Enabling email capture in the test environment would allow automated verification.

- trigger_action: Submit Forgot Password form by entering an existing account email and clicking the 'Reset Password' button
- channel: email
- recipient: email address entered in the Forgot Password form (existing account email)
- expected_content:
  - Email subject indicating a password reset or reset password request
  - A unique password reset link or token
  - Clear instructions to click the link and enter a new password
  - Expiry information stating the reset link is valid for 24 hours
  - Reference to the account or masked email/username
- in_app_partial_check:
  - navigate_to: Forgot Password
  - observe: Confirmation message displayed indicating a reset link has been sent to the provided email address
- verification_method: Access the test inbox (Mailtrap, Mailhog, or equivalent) for the recipient address within 2 minutes of submitting the form. Confirm the email arrives, verify subject, presence of the reset link and instructions, and that the link target is a password reset page. If inbox tooling is unavailable, verify delivery and content via application email logs.

---
