# PHP Travels Functional Description

## Navigation
PHP Travels is a comprehensive travel booking platform. When visitors arrive, they land on the home page with a top navigation bar featuring options for Home, Hotels, Flights, Tours, Cars, Visa, Offers, Blog, and Account/Login. The home page displays a prominent search widget that allows users to search for Hotels, Flights, Tours, or Cars through tabs. The right side of the navigation shows currency/language selectors and a Login/Signup option. After successful authentication, users can access their dashboard which displays booking history, profile settings, and account management options. The main navigation remains consistent across all pages, with additional contextual menus appearing based on the current section.

---

## Home Page & Search

The home page features a prominent search widget with four tabs: Hotels, Flights, Tours, and Cars. Clicking a tab switches the visible search fields for that service type. The Hotels tab collects destination, check-in/check-out dates, number of rooms, and guest count (adults and children). The Flights tab collects trip type (One-way, Round-trip, or Multi-city), departure and arrival city, travel dates, passenger count (adults, children, infants), and cabin class (Economy, Premium Economy, Business, or First). The Tours tab collects destination and a travel date range. The Cars tab collects pick-up and drop-off location, pick-up and drop-off date and time. The Search button validates that all required fields for the active tab are filled; inline errors appear on invalid fields. On success, the user is redirected to the corresponding results listing page.

---

## User Registration

The registration form collects First Name, Last Name, Email, Password, Confirm Password, Mobile Number (with country code dropdown), Address, Country, and a Terms and Conditions checkbox. On submission, the system validates required fields, password match, valid email format, and email uniqueness. Field-level errors appear inline on failure. On success, an account is created and the user is either automatically logged in and redirected to their dashboard, or prompted to verify their email before gaining access.

---

## User Login

The login page contains an Email field, Password field, Remember Me checkbox, Forgot Password? link, and a Login button. Social login options (Google, Facebook) are displayed if enabled. On submission, valid credentials redirect the user to their dashboard or the page they were previously trying to access. Invalid credentials show an error message and clear the password field. After multiple consecutive failed attempts, CAPTCHA verification may be required.

---

## Forgot Password

The page presents an Email field and a Reset Password button. If the email exists in the system, a reset link is sent to that address and a confirmation message is shown. The reset link expires after 24 hours. Clicking the link takes the user to a password reset page where they enter and confirm a new password; after a successful change, they are redirected to the login page with a success message. If the email is not found, an error is shown and the form remains editable.

---

## Hotels Search & Listing

The hotels search form collects destination, check-in/check-out dates, number of rooms, and guest count (adults and children). On success, users are redirected to the listing page, where each hotel card shows name, location, star rating, thumbnail image, starting price per night, amenity icons, and a Book Now button. A left sidebar provides collapsible filters for price range, star rating, facilities/amenities, hotel type, and board basis. Filters update results dynamically, with active filters summarized at the top with individual remove buttons and a Reset all control. Results can be sorted by price (low to high or high to low), star rating, or guest rating.

---

## Hotel Details & Booking

The hotel details page displays a photo gallery, full property description, location map, room types with pricing and maximum occupancy, guest reviews and aggregate rating, and hotel policies including cancellation policy and check-in/check-out times. After selecting a room, a booking form shows the selected hotel and room type, stay dates, guest count, and a price breakdown (room rate, taxes, fees, and total). The user provides First Name, Last Name, Email, Phone Number, and optional Special Requests. Clicking Book Now requires the user to be logged in and proceeds to the payment page.

---

## Flights Search & Listing

The flights search form collects trip type (One-way, Round-trip, Multi-city), departure and arrival city, travel dates, passenger count (adults, children, infants), and cabin class (Economy, Premium Economy, Business, First). On success, users are redirected to the listing page, where each result shows airline logo and name, departure and arrival times and airports, total duration, number of stops (Non-stop, 1 stop, 2+ stops), price per passenger, and a Select button. Expanding a result shows baggage allowance, fare rules, and seat availability. Sidebar filters include airlines, number of stops, departure and arrival time ranges, and price range. Results can be sorted by price, duration, departure time, or arrival time.

---

## Flight Booking

The flight booking page displays a full itinerary summary, passenger count, cabin class, and a fare breakdown (base fare, taxes, fees, and total per passenger and overall). The booking form collects title (Mr, Mrs, Ms, Dr), first name, last name, date of birth, passport number, and passport expiry for each traveler, plus email and phone for the lead passenger. Optional fields include meal preferences and seat selection. All required fields are validated; incomplete or invalid fields display inline errors and block progression. The user clicks Continue to proceed to the payment page.

---

## Tours Search & Listing

The tours search form collects destination, travel dates, tour type (Adventure, Cultural, Cruise, Wildlife, etc.), duration, and budget range. On success, users are redirected to the listing page, where each card shows tour image, name, destination, duration, starting price per person, a brief description, availability status, and traveler rating. Sidebar filters include destination, tour type, price range, duration, and departure dates. Results can be sorted by popularity, price, duration, or rating.

---

## Tour Details & Booking

The tour details page displays a slideshow of images, a full day-by-day itinerary, inclusions and exclusions (meals, accommodation, activities, transportation), available departure dates, pricing per person for adults and children, location map, guest reviews, and terms and conditions. The user selects a departure date, specifies the number of travelers (adults and children), and clicks Book Now. The booking form collects traveler names, contact details, and special requirements, and displays the total cost breakdown. Unauthenticated users are redirected to the login page before proceeding.

---

## Cars Search & Listing

The car rental search form collects pick-up and drop-off location, pick-up and drop-off date and time, and driver age. On success, users are redirected to the listing page, where vehicles are grouped by category (Economy, Compact, SUV, Luxury, Van). Each listing shows vehicle image, make and model, transmission type (Automatic/Manual), fuel policy, seating and luggage capacity, feature icons (AC, GPS, etc.), price per day, total rental cost for the selected period, and a Book Now button. Sidebar filters include car type, transmission, fuel policy, rental company, and price range. Filters update results dynamically.

---

## Car Booking

The car booking page displays selected vehicle details, rental period, pick-up and drop-off locations and times, and a full pricing breakdown including daily rate, number of rental days, taxes, insurance options, and additional fees. The booking form collects driver full name, age, license number, license issue country, email, and phone number. Optional add-ons include GPS, child seat, and additional driver. Users select an insurance plan and review terms covering fuel policy, mileage limits, damage liability, and cancellation. After accepting terms, the user clicks Confirm Booking to proceed to payment. Invalid fields display inline errors and block progression.

---

## Visa Services

Users select their Nationality and Destination Country to view visa requirements for that combination, including visa type, processing time, required documents, and fees. The visa application form collects personal information (full name, passport number, passport expiry date, date of birth, nationality, email, phone) and travel details (purpose of visit, intended travel dates, duration of stay). A document upload section allows attaching required files such as passport copy, photographs, invitation letter, and supporting documents. After submission, application status can be tracked through the bookings section of the dashboard.

---

## User Dashboard

The dashboard is organized into the following sections. My Bookings displays all past and upcoming bookings across Hotels, Flights, Tours, and Cars, with booking reference, service type, travel dates, status (Pending, Confirmed, Cancelled), and action buttons for View Details, Cancel, and Modify where the booking type and cancellation policy permit; users can also download confirmations, invoices, or vouchers. My Profile shows personal information with an Edit button. Wallet/Credits shows available credit balance and full transaction history. Wishlist shows saved hotels, tours, or flights. Reviews allows rating and reviewing completed bookings. Settings provides controls for changing password, notification preferences, and default currency and language. Logout ends the session.

---

## Booking Management

Each booking's detail view shows confirmation number, full service information, traveler details, payment information, and current booking status. Where the booking type and cancellation policy permit, a Modify button allows changing travel dates (subject to availability and applicable fees), adding special requests, or updating traveler information. Clicking Cancel opens a cancellation confirmation flow showing the applicable refund amount; the user must explicitly confirm before the cancellation is processed and a refund is initiated to the original payment method. Email notifications are sent for all status changes including confirmation, modification, and cancellation.

---

## Payment Processing

The payment page displays a full booking summary with a price breakdown (base price, taxes, service fees, applicable discounts, and total). Supported payment methods include Credit/Debit Card (Visa, MasterCard, American Express), PayPal, Bank Transfer, and Wallet/Credits. The card form collects cardholder name, card number, expiration date, and CVV, with an option to save the card for future use. Security badges and SSL encryption indicators are displayed on the page. On success, the user is taken to a booking confirmation page with a reference number and options to download the invoice or voucher; a confirmation email is sent. If payment fails, an error message describes the issue (e.g., "Card declined," "Insufficient funds") and the user can retry without losing their booking details.

---

## Currency & Language Selection

The currency selector updates all prices displayed across the site in real-time without losing the user's current search context. The language selector switches the entire site interface — including navigation labels, form labels, and content — to the chosen language (e.g., English, Arabic, Spanish, French). For authenticated users, both preferences are saved to their profile; for unauthenticated users, preferences are stored in session/cookies for the current browsing session.

---

## Search & Filters

All listing pages include a left sidebar with collapsible filter sections and sorting controls above the results grid. Common filters across all listing types include price range (slider) and star or review ratings. Listing-specific filters are available for Hotels (facilities/amenities, hotel type, board basis, location/area), Flights (airlines, number of stops, departure and arrival time ranges), Tours (tour type, duration, departure dates), and Cars (car type, transmission, fuel policy, rental company). Results update dynamically as filters are adjusted, with the result count updating accordingly. Active filters are summarized at the top with individual remove buttons and a Reset all filters control.

---

## Reviews & Ratings

Listing pages show an aggregate rating score and total review count for each item. Detail pages include a dedicated Reviews section with individual reviews showing overall rating, category-specific ratings (e.g., Cleanliness, Service, Location for hotels), reviewer name and country, review date, stay date, written comments, and any guest-uploaded photos. Users can filter reviews by rating, date, or traveler type. Authenticated users who have completed a booking can submit a review through the dashboard or via a post-stay email prompt, providing star ratings for overall experience and individual categories, plus written feedback.

---

## Offers & Deals

The Offers page displays promotional banners and featured deal cards, each showing deal title, image, discount percentage or special rate, validity period, a Terms and Conditions link, and a Book Now button. Last-minute offers and seasonal packages are listed alongside standard promotions. Users can filter offers by service type (Hotels, Flights, Packages), destination, and travel dates. Clicking Book Now either applies the promotional code automatically to the booking flow or redirects to a pre-filled search with the discounted rates applied. A newsletter subscription field allows users to submit their email to receive future exclusive deals.

---

## Logout

Clicking Logout terminates the current session, clears sensitive session data, and redirects the user to the home page. Attempts to access protected pages after logout redirect to the login page.