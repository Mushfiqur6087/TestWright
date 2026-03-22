# PHP Travels Functional Description

**Website URL:** https://phptravels.com/demo

**Navigation:** PHP Travels is a comprehensive travel booking platform. When visitors arrive, they land on the home page with a top navigation bar featuring links for **Home**, **Hotels**, **Flights**, **Tours**, **Cars**, **Visa**, **Offers**, **Blog**, and **Account / Login**. The home page displays a prominent search widget with tabs for Hotels, Flights, Tours, and Cars. The right side of the navigation bar shows a **currency selector**, a **language selector**, and a **Login / Signup** option. After successful authentication, the Login/Signup option is replaced by the user's name with a dropdown menu providing access to the dashboard and account management. The main navigation bar remains consistent across all pages, with additional contextual menus appearing based on the current section.

---

## 1. Home Page & Search

The home page features a prominent search widget with four tabs: **Hotels**, **Flights**, **Tours**, and **Cars**. Clicking a tab switches the visible search fields to those relevant for that service type.

**Hotels tab** fields: Destination or hotel name (text input with autocomplete), Check-in date (calendar picker), Check-out date (calendar picker), Number of rooms (numeric selector), and Guests per room (adults and children with age specification).

**Flights tab** fields: Trip type (radio buttons: One-way, Round-trip, Multi-city), Departure city (autocomplete), Arrival city (autocomplete), Departure date (calendar picker), Return date (calendar picker, enabled for round-trip only), Number of passengers (adults, children, infants), and Cabin class (dropdown: Economy, Premium Economy, Business, First).

**Tours tab** fields: Destination (autocomplete) and Travel dates (date range picker).

**Cars tab** fields: Pick-up location (autocomplete), Drop-off location (autocomplete, defaults to same as pick-up), Pick-up date and time (date/time picker), and Drop-off date and time (date/time picker).

The **Search** button validates that all required fields for the active tab are filled before submission. If required fields are empty, inline validation errors appear on the relevant fields and block the search. When all fields are valid and the user clicks Search, the system queries available options and redirects to the corresponding results listing page.

---

## 2. User Registration

The registration page is accessible via the **Signup** link in the top navigation bar or via the link on the login page. The registration form contains the following fields:

- **First Name** (required, text)
- **Last Name** (required, text)
- **Email** (required, must be valid email format and not already registered)
- **Password** (required)
- **Confirm Password** (required, must match Password)
- **Mobile Number** (required, includes a country code dropdown with flags)
- **Address** (optional, text)
- **Country** (optional, dropdown)
- **Terms and Conditions** checkbox (required)

On clicking the **"Sign Up"** button, the system validates all inputs: required field completeness, password match, valid email format, and uniqueness of the email address. If any validation fails, field-level error messages appear inline and the form remains editable. If validation passes, an account is created and the user is either automatically logged in and redirected to their dashboard, or prompted to verify their email address before gaining access.

---

## 3. User Login

The login page displays a form with the following elements: **Email** field, **Password** field, a **"Remember Me"** checkbox, a **"Forgot Password?"** link, a **"Login"** button, and a link to the registration page for new users. Social media login options (Google, Facebook) are displayed if enabled on the platform.

On clicking **"Login"**, the system submits credentials to the authentication server. If authentication succeeds, the user is redirected to their account dashboard, or to the page they were attempting to access before being prompted to log in. If credentials are invalid, an error message appears below the form fields; the password field is cleared and the email field retains its value for correction. The password field masks all input. After multiple consecutive failed attempts, CAPTCHA verification may be required before further login attempts are accepted.

---

## 4. Forgot Password

The Forgot Password page is accessed via the **"Forgot Password?"** link on the login page. The page presents a single **Email** field and a **"Reset Password"** button.

The user enters their registered email address and clicks **"Reset Password."** The system checks whether the email exists in the user database. If found, a password reset link is sent to that address and the page displays a confirmation message. The reset link expires after 24 hours. When the user clicks the reset link in their email, they are taken to a password reset page where they enter and confirm a new password. After a successful password change, the user is redirected to the login page with a success message. If the submitted email is not found, an error message is shown and the form remains editable.

---

## 5. Hotels Search & Listing

The hotels search form (accessible from the Hotels tab on the home page or via the **Hotels** link in the top navigation) contains: Destination or hotel name (autocomplete), Check-in date (calendar picker), Check-out date (calendar picker), Number of rooms (numeric selector), and Guests per room broken down into Adults and Children (with age specification for each child).

After clicking **Search**, required fields are validated. On success, the user is redirected to the hotels listing page.

Each hotel card on the listing page displays: hotel name, location, star rating, thumbnail image, starting price per night, amenity/facility icons, and a **"View Details"** or **"Book Now"** button.

The listing page includes a **left sidebar** with collapsible filter sections: Price range (slider), Star rating (checkboxes), Facilities/amenities (checkboxes), Hotel type (checkboxes), and Board basis (checkboxes). Filters update results dynamically as they are applied. A summary of active filters appears at the top of results with individual remove buttons and a **"Reset all"** control. Sorting options above the results grid allow ordering by: Price low to high, Price high to low, Star rating, and Guest rating. Pagination controls allow browsing additional result pages.

---

## 6. Hotel Details & Booking

Clicking a hotel card from the listing page opens the hotel details page, which displays:

- A **photo gallery** with multiple images
- Full written **description** of the property
- **Location map** (Google Maps integration)
- **Facilities and amenities** list
- **Room types and availability** section showing each room type (e.g., Standard, Deluxe, Suite) with price per night, maximum occupancy, included amenities, and a **"Select"** or **"Book Now"** button
- **Guest reviews and ratings** (aggregate score and individual reviews)
- **Hotel policies** including cancellation policy, check-in time, and check-out time

After selecting a room, the booking form displays: selected hotel and room type, check-in and check-out dates, number of guests, and a price breakdown (room rate, taxes, fees, total). The user fills in: **First Name**, **Last Name**, **Email**, **Phone Number**, and optional **Special Requests**. Clicking **"Confirm"** or **"Book Now"** requires the user to be logged in (unauthenticated users are redirected to the login page) and proceeds to the payment page.

---

## 7. Flights Search & Listing

The flights search form (accessible from the Flights tab on the home page or via the **Flights** link in the top navigation) contains: Trip type selector (One-way, Round-trip, Multi-city), Departure city (autocomplete), Arrival city (autocomplete), Departure date (calendar picker), Return date (calendar picker, active for round-trip only), Number of passengers — Adults, Children, Infants (numeric selectors), and Cabin class (dropdown: Economy, Premium Economy, Business, First).

After clicking **Search**, required fields are validated and the user is redirected to the flights listing page.

Each flight result displays: airline logo and name, departure and arrival times and airports, flight duration, number of stops (Non-stop, 1 stop, 2+ stops), price per passenger, and a **"Select"** or **"View Details"** button. Clicking **"View Details"** expands additional information including baggage allowance, fare rules, and seat availability.

The listing page left sidebar includes collapsible filters: Airlines (checkboxes), Number of stops (checkboxes), Departure time range (slider), Arrival time range (slider), and Price range (slider). Results update dynamically as filters are applied. Sorting options allow ordering by: Price, Duration, Departure time, and Arrival time.

---

## 8. Flight Booking

After selecting a flight from the listing page, the user is taken to the flight booking page, which displays a summary of the selected flight: itinerary, departure and arrival information, passenger count, cabin class, and a full fare breakdown (base fare, taxes, fees, and total per passenger and overall).

The booking form collects passenger information for each traveler: **Title** (dropdown: Mr, Mrs, Ms, Dr), **First Name**, **Last Name**, **Date of Birth**, **Passport Number** (required for international flights), and **Passport Expiry Date**. Contact information is collected for the lead passenger: **Email** and **Phone Number**. Optional fields include meal preferences and seat selection where available.

All required fields are validated including proper date formats and passport details. Users review the terms and conditions and click **"Continue"** or **"Proceed to Payment"** to advance to the payment page. Incomplete or invalid fields display inline errors and block progression.

---

## 9. Tours Search & Listing

The tours search form (accessible from the Tours tab on the home page or via the **Tours** link in the top navigation) contains: Destination (autocomplete), Travel dates (date range picker), Tour type (dropdown: Adventure, Cultural, Cruise, Wildlife, etc.), Duration (dropdown), and Budget range (price slider).

After clicking **Search**, required fields are validated and the user is redirected to the tours listing page.

Each tour card displays: tour image, tour name, destination, duration (e.g., 5 Days / 4 Nights), starting price per person, brief description, highlights, availability status, traveler rating, and a **"View Details"** button.

The listing page left sidebar includes collapsible filters: Destination, Tour type, Price range (slider), Duration, and Departure dates. Results update dynamically. Sorting options allow ordering by: Popularity, Price, Duration, and Rating.

---

## 10. Tour Details & Booking

Clicking a tour card opens the tour details page, which displays:

- A **slideshow** of tour images
- Full **day-by-day itinerary**
- **Inclusions and exclusions** (meals, accommodation, activities, transportation)
- **Departure dates and availability** calendar
- **Pricing per person** broken down by adult and child rates, with group-size considerations
- **Location map**
- **Guest reviews and ratings**
- **Terms and conditions**

The user selects a departure date from available options, specifies the number of travelers (Adults and Children with age), and clicks **"Book Now"** to proceed to the booking form. The booking form collects traveler names, contact details, special requirements, and displays the total cost breakdown (per-person rate multiplied by number of travelers, plus taxes and fees). After completing the form and agreeing to terms, the user proceeds to payment. Unauthenticated users are redirected to the login page before proceeding.

---

## 11. Cars Search & Listing

The car rental search form (accessible from the Cars tab on the home page or via the **Cars** link in the top navigation) contains: Pick-up location (autocomplete), Drop-off location (autocomplete, defaults to same as pick-up), Pick-up date and time (date/time picker), Drop-off date and time (date/time picker), and Driver age (numeric input).

After clicking **Search**, required fields are validated and the user is redirected to the cars listing page. Available vehicles are grouped by category (Economy, Compact, SUV, Luxury, Van).

Each car listing displays: vehicle image, make and model, transmission type (Automatic / Manual), fuel policy, seating capacity, luggage capacity, feature icons (AC, GPS, etc.), price per day, total rental cost for the selected period, and a **"Book Now"** or **"View Details"** button.

The listing page left sidebar includes collapsible filters: Car type (checkboxes), Transmission (checkboxes), Fuel policy (checkboxes), Rental company (checkboxes), and Price range (slider). Results update dynamically as filters are applied.

---

## 12. Car Booking

After selecting a vehicle from the listing page, the user is taken to the car booking page, which displays: selected vehicle details (make, model, category, features), rental period summary, pick-up and drop-off locations and times, and a full pricing breakdown (daily rate, number of rental days, taxes, insurance options, and additional fees).

The booking form collects driver information: **Full Name**, **Age**, **Driver's License Number**, **License Issue Country**, **Email**, and **Phone Number**. Optional add-ons include GPS, child seat, and additional driver. Users select an insurance option from the available plans. The page displays terms and conditions covering fuel policy, mileage limits, damage liability, and cancellation policy.

After reviewing all details and accepting the terms, the user clicks **"Confirm Booking"** and proceeds to payment. Incomplete or invalid fields display inline errors and block progression.

---

## 13. Visa Services

The Visa section is accessible via the **Visa** link in the top navigation. Users begin by selecting their **Nationality** (dropdown) and **Destination Country** (dropdown) to view visa requirements for that combination. The results display: visa type, processing time, required documents, and visa fees.

The visa application form collects personal information: **Full Name**, **Passport Number**, **Passport Expiry Date**, **Date of Birth**, **Nationality**, **Email**, and **Phone Number**. Travel details include: **Purpose of Visit** (dropdown), **Intended Travel Dates**, and **Duration of Stay**. A document upload section allows attaching required files such as passport copy, photographs, invitation letter, and supporting documents. After submission, users can track their visa application status through the bookings section of their account dashboard.

---

## 14. User Dashboard

After login, users are redirected to their account dashboard, which serves as the central control area for all account and booking activities. The dashboard is organized into the following sections:

- **My Bookings** — displays all past and upcoming bookings across Hotels, Flights, Tours, and Cars. Each booking card shows the booking reference number, service type, travel dates, booking status (Pending, Confirmed, Cancelled), and action buttons including **"View Details"**, **"Cancel"**, and **"Modify"** where the booking type and cancellation policy permit. Users can download booking confirmations, invoices, or vouchers from each booking record.
- **My Profile** — shows the user's personal information (name, email, phone, address, passport details) with an **"Edit"** button to update details.
- **Wallet / Credits** — displays available credit balance and a full transaction history of credits earned and used.
- **Wishlist** — shows hotels, tours, or flights the user has saved for later.
- **Reviews** — allows users to rate and review completed bookings by submitting star ratings and written feedback.
- **Settings** — provides controls for changing password, managing notification preferences, and selecting default currency and language.
- **Logout** — ends the session and redirects to the home page.

---

## 15. Booking Management

From the **My Bookings** section of the dashboard, or via confirmation links in booking emails, users can manage existing bookings. Each booking's detail view displays: confirmation number, full property or flight or tour information, traveler details, payment information, and current booking status.

**Modification:** Where the booking type and cancellation policy permit, a **"Modify"** button is available. The modification flow allows changing travel dates (subject to availability and applicable fees), adding special requests, or updating traveler information. Changes are validated against current availability before being confirmed.

**Cancellation:** Clicking **"Cancel"** opens a cancellation confirmation flow. The system displays the applicable refund amount based on the booking's cancellation policy and requires explicit user confirmation before processing. Once confirmed, the cancellation is processed and a refund is initiated to the original payment method. Users receive email notifications for all booking status changes including confirmation, modification, and cancellation.

---

## 16. Payment Processing

After completing booking details for any service type, the user is taken to the payment page, which displays a full booking summary: all selected services, price breakdown (base price, taxes, service fees, applicable discounts), and the total amount due.

The payment section offers the following methods: **Credit/Debit Card** (Visa, MasterCard, American Express), **PayPal**, **Bank Transfer**, and **Wallet / Credits** (if the user has an available balance). The credit/debit card form contains: **Cardholder Name**, **Card Number** (validated in real-time for format and card type), **Expiration Date**, and **CVV**. A checkbox allows users to save their payment method for future use.

The page displays security badges and SSL encryption indicators. After clicking **"Pay Now"** or **"Confirm Payment"**, the system processes the transaction. On success, the user is taken to a booking confirmation page showing the booking reference number, a booking summary, and options to download the invoice or voucher. An email confirmation is sent to the registered email address.

If payment fails, an error message appears describing the issue (e.g., "Card declined," "Insufficient funds"), and the user is offered the option to retry with the same or a different payment method without losing their booking details.

---

## 17. Currency & Language Selection

The top navigation bar includes two selector dropdowns on the right side: **Currency** and **Language**.

The **currency selector** displays a list of supported currencies with flag icons and currency codes (e.g., USD, EUR, GBP). Selecting a currency immediately updates all prices displayed across the entire site in real-time without losing the user's current search context. For authenticated users, the selected currency is saved to their profile. For unauthenticated users, the preference is stored in session/cookies and persists across pages.

The **language selector** displays supported languages (e.g., English, Arabic, Spanish, French). Selecting a language switches the entire site interface — including navigation labels, form labels, and content — to the chosen language. For authenticated users, the language preference is saved to their profile. For unauthenticated users, the preference is stored in session/cookies for the current browsing session.

---

## 18. Search & Filters

All listing pages (Hotels, Flights, Tours, Cars) include a **left sidebar** with collapsible filter sections and sorting controls above the results grid.

**Common filters across all listing types:** Price range (slider with minimum and maximum values) and Star or review ratings (checkboxes).

**Listing-specific filters:**
- **Hotels:** Facilities/amenities (checkboxes), Hotel type (checkboxes), Board basis (checkboxes), Location/area (checkboxes)
- **Flights:** Airlines (checkboxes), Number of stops (checkboxes), Departure time range (time slider), Arrival time range (time slider)
- **Tours:** Tour type (checkboxes), Duration (checkboxes), Departure dates
- **Cars:** Car type (checkboxes), Transmission (checkboxes), Fuel policy (checkboxes), Rental company (checkboxes)

As users select or adjust filters, results update dynamically without a full page refresh and the result count updates accordingly. Active filters are summarized at the top of the results area with individual **"×"** remove buttons and a **"Reset all filters"** control to clear all selections at once.

---

## 19. Reviews & Ratings

Reviews and ratings are displayed on hotel, tour, and car listing and detail pages. On listing pages, each item shows an aggregate rating score (e.g., 4.5 / 5) and total review count. On detail pages, a dedicated **Reviews** section displays individual guest reviews containing: overall rating, category-specific ratings (e.g., Cleanliness, Service, Location for hotels), reviewer name and country, review submission date, travel/stay date, written comments, and any guest-uploaded photos. Users can filter displayed reviews by rating, date, or traveler type.

Authenticated users who have completed a booking can submit their own review through the **Reviews** section of their dashboard or via a post-stay email prompt. The review submission form includes star rating selectors for overall experience and individual categories, and a text area for detailed written feedback.

---

## 20. Offers & Deals

The Offers page is accessible via the **Offers** link in the top navigation. The page displays promotional banners and featured deal cards, each showing: deal title, image, discount percentage or special rate, validity period, a **"Terms and Conditions"** link, and a **"Book Now"** button. Last-minute offers and seasonal packages are listed alongside standard promotions.

Users can filter displayed offers by: service type (Hotels, Flights, Packages), destination, and travel dates. Clicking **"Book Now"** on an offer either applies the promotional code automatically to the booking flow or redirects to a pre-filled search page with the discounted rates applied. A newsletter subscription field on the page allows users to submit their email address to receive future exclusive deals.

---

## Logout

The logout option is accessible from the user dropdown menu in the top navigation bar and from the account dashboard. Clicking **"Logout"** terminates the current user session, clears sensitive session data, and redirects the user to the home page. After logout, any attempt to access a protected page (such as the dashboard or booking management) redirects the user to the login page.