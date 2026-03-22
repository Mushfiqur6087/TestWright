# PHP Travels Functional Overview

**Website URL:** [https://phptravels.com/demo](https://phptravels.com/demo)

**Navigation:** PHP Travels is a comprehensive travel booking platform. When visitors arrive, they land on the home page with a top navigation bar featuring options for Home, Hotels, Flights, Tours, Cars, Visa, Offers, Blog, and Account/Login. The home page displays a prominent search widget that allows users to search for Hotels, Flights, Tours, or Cars through tabs. The right side of the navigation shows currency/language selectors and a Login/Signup option. After successful authentication, users can access their dashboard which displays booking history, profile settings, and account management options. The main navigation remains consistent across all pages, with additional contextual menus appearing based on the current section.

---

## 1. Home Page & Search
![Home Page](images/1_homepage_search.png)

The home page features a section with a prominent search widget that allows users to search for different travel services via tabs (Hotels, Flights, Tours, Cars). Each tab presents relevant search fields - for Hotels: destination/hotel name, check-in/check-out dates, number of guests and rooms; for Flights: departure/arrival cities, travel dates, number of travelers, and class type (Economy, Business, First); for Tours: destination and travel dates; for Cars: pick-up location, dates, and times. The search form validates required fields before allowing submission. When users enter search criteria and click Search, the system queries available options and redirects to results pages showing matching listings with filters and sorting options.

---

## 2. User Registration
![User Registration](images/2_registration.png)

The registration page is accessible via the Signup link in the navigation or login page. The registration form includes required fields: First Name, Last Name, Email, Password, Confirm Password, Mobile Number (with country code selector), and optional fields like Address and Country selection. All password fields must match, and email must be in valid format. The mobile number field includes a country code dropdown with flags. A checkbox for accepting terms and conditions is required. Upon clicking the Sign Up button, the system validates all inputs - checking for required fields, password match, email format, and unique email address. If validation passes, an account is created, and depending on configuration, the user may need to verify their email address or be automatically logged in and redirected to their dashboard.

---

## 3. User Login
![User Login](images/3_login.png)

The login page displays a form with Email and Password fields, a Remember Me checkbox, and a Forgot Password link. Users can also see options to login via social media accounts (Google, Facebook) if enabled. The Login button submits credentials to the authentication server. On successful authentication, users are redirected to their account dashboard or the page they were trying to access before login. If credentials are invalid, an error message appears below the form fields explaining the issue. The page also includes a link to the registration page for new users. Security features include password masking and optional CAPTCHA verification after multiple failed attempts.

---

## 4. Forgot Password
![Forgot Password](images/4_forgot_password.png)

Accessed via the login page, the Forgot Password page presents a simple form with a single Email field. Users enter their registered email address and click Submit or Reset Password button. The system checks if the email exists in the database. If found, a password reset link is sent to the provided email address with instructions and an expiration time (typically 24 hours). The user receives confirmation that the email has been sent. When users click the reset link in their email, they are taken to a password reset page where they enter and confirm their new password. After successful password change, users are redirected to the login page with a success message.

---

## 5. Hotels Search & Listing
![Hotels Search](images/5_hotels_search.png)
![Hotels Listing](images/5_hotels_listing.png)

The hotels search functionality allows users to enter destination (city or hotel name), check-in and check-out dates via a calendar picker, number of rooms, and guests per room (adults and children with age specification). Advanced search may include filters for star rating, price range, and amenities. After clicking Search, users are taken to the hotels listing page showing available properties matching their criteria. Each hotel card displays the hotel name, location, star rating, thumbnail image, starting price per night, facilities/amenities icons, and a View Details or Book Now button. The listing page includes filter options on the left sidebar (price range, star rating, facilities, hotel type, board basis) and sorting options (price low to high, price high to low, star rating, guest rating). Users can adjust filters dynamically to refine results, and pagination allows browsing multiple pages of results.

---

## 6. Hotel Details & Booking
![Hotel Details](images/6_hotel_details.png)
![Hotel Booking](images/6_hotel_booking.png)

When a user clicks on a hotel from the listing, they are taken to the hotel details page. This page displays comprehensive information including a photo gallery with multiple images, detailed description, location map (Google Maps integration), list of facilities and amenities, room types and availability, pricing for selected dates, guest reviews and ratings, and hotel policies (cancellation, check-in/check-out times). The room selection section shows different room types (Standard, Deluxe, Suite) with individual prices, max occupancy, amenities, and availability. Each room has a Select or Book Now button. After selecting a room, users proceed to the booking form where they confirm dates, number of guests, enter guest information (first name, last name, email, phone), special requests, and review the price breakdown (room rate, taxes, fees, total). Clicking Confirm or Book Now may require login and proceeds to payment.

---

## 7. Flights Search & Listing
![Flights Search](images/7_flights_search.png)
![Flights Listing](images/7_flights_listing.png)

The flights search form includes fields for trip type selection (one-way, round-trip, multi-city), departure and arrival cities (with autocomplete), departure date and return date (for round-trip), number of passengers (adults, children, infants), and cabin class (Economy, Premium Economy, Business, First). After submitting the search, users see a flights listing page with available options. Each flight result shows the airline logo and name, departure and arrival times, flight duration, number of stops (non-stop, 1 stop, 2+ stops), price per passenger, and a Select or View Details button. The listing includes filters for airlines, stops, departure/arrival times, and price range. Users can sort results by price, duration, departure time, or arrival time. Clicking on a flight shows additional details like baggage allowance, fare rules, and seat availability.

---

## 8. Flight Booking
![Flight Booking](images/8_flight_booking.png)

After selecting a flight from the listing page, users proceed to the flight booking page which displays a summary of selected flight details including itinerary, departure/arrival information, passenger count, and fare breakdown. The booking form collects passenger information for each traveler (title, first name, last name, date of birth, passport number if international, contact information for lead passenger). Users can add special requests, meal preferences, and seat selection if available. The form validates all required fields including proper date formats and passport information. After filling in details and reviewing terms and conditions, users proceed to payment by clicking Continue or Proceed to Payment.

---

## 9. Tours Search & Listing
![Tours Search](images/9_tours_search.png)
![Tours Listing](images/9_tours_listing.png)

The tours search section allows users to browse by destination, travel dates, tour type (adventure, cultural, cruise, wildlife, etc.), duration, and budget range. The tours listing page displays available tour packages with an attractive image, tour name, destination, duration (e.g., 5 Days / 4 Nights), starting price per person, brief description, highlights, and a View Details button. Sidebar filters enable users to narrow results by destination, tour type, price range, duration, and departure dates. Each tour card may also show availability status and ratings from previous travelers. Users can sort tours by popularity, price, duration, or rating.

---

## 10. Tour Details & Booking
![Tour Details](images/10_tour_details.png)
![Tour Booking](images/10_tour_booking.png)

The tour details page provides comprehensive information including a slideshow of tour images, detailed itinerary (day-by-day breakdown), inclusion and exclusions (meals, accommodation, activities, transportation), departure dates and availability, pricing per person (with group size considerations), location map, guest reviews, and terms and conditions. Users select a departure date from available options, specify number of travelers (adults and children with age), and click Book Now to proceed to the booking form. The booking form collects traveler information, contact details, special requirements, and displays the total cost breakdown. After completing the form and agreeing to terms, users proceed to payment.

---

## 11. Cars Search & Listing
![Cars Search](images/11_cars_search.png)
![Cars Listing](images/11_cars_listing.png)

The car rental search form includes fields for pick-up location (city or specific address), drop-off location (same or different), pick-up date and time, drop-off date and time, and driver age. After searching, users see available vehicles grouped by category (economy, compact, SUV, luxury, van). Each car listing shows the vehicle image, make and model, transmission type (automatic/manual), fuel policy, seating capacity, luggage capacity, features (AC, GPS, etc.), price per day and total rental cost, and a Book Now or View Details button. Filters on the sidebar allow narrowing by car type, transmission, fuel policy, rental company, and price. Users can compare multiple vehicles and view detailed specifications before booking.

---

## 12. Car Booking
![Car Booking](images/12_car_booking.png)

The car booking page displays the selected vehicle details, rental period summary, pick-up and drop-off locations and times, and pricing breakdown (daily rate, taxes, insurance options, additional fees). Users fill in driver information (name, age, license number, license issue country, contact details), select insurance and add-ons (GPS, child seat, additional driver), and provide payment information. The form includes terms and conditions regarding fuel policy, mileage limits, damage liability, and cancellation policy. After reviewing all details and accepting terms, users confirm the booking and proceed to payment.

---

## 13. Visa Services
![Visa Services](images/13_visa_services.png)

The Visa section allows users to check visa requirements and apply for visa services. Users select their nationality and destination country to see visa requirements, processing time, required documents, and visa fees. The visa application page includes a form for personal information (full name, passport details, date of birth, nationality, contact information), travel details (purpose of visit, intended travel dates, duration of stay), and document upload functionality for required paperwork (passport copy, photos, invitation letter, etc.). Users can track their visa application status through their account dashboard. This section may be informational or fully functional depending on the demo configuration.

---

## 14. User Dashboard
![User Dashboard](images/14_dashboard.png)

After login, users access their account dashboard which serves as the control center for managing all travel-related activities. The dashboard includes sections for: My Bookings (displaying all past and upcoming bookings for hotels, flights, tours, and cars with booking reference numbers, dates, status, and action buttons like View Details, Cancel, or Modify), My Profile (personal information, contact details, passport information, with Edit functionality), Wallet or Credits (available credits, transaction history), Wishlist (saved hotels, tours, or flights), Reviews (ability to rate and review completed bookings), Settings (password change, notification preferences, currency and language selection), and Logout option. Each booking card shows essential information and allows users to download booking confirmations, invoices, or vouchers.

---

## 15. Booking Management
![Booking Management](images/15_booking_management.png)

Within the dashboard or via email confirmation links, users can manage their bookings. For each booking, users can view complete details including confirmation numbers, property/flight/tour information, traveler details, payment information, and booking status (pending, confirmed, cancelled). Depending on the cancellation policy and booking type, users may see options to Modify or Cancel bookings. The modification process allows changing dates (subject to availability and fees), adding special requests, or updating traveler information. The cancellation flow shows applicable refund amounts based on cancellation policy, requires confirmation, and processes refunds according to payment method. Users receive email notifications for all booking activities.

---

## 16. Payment Processing
![Payment Processing](images/16_payment.png)

After completing booking details, users proceed to the payment page which displays a comprehensive booking summary including all selected services, price breakdown (base price, taxes, service fees, discounts), and total amount. The payment section offers multiple payment methods including credit/debit cards (Visa, MasterCard, American Express), PayPal, bank transfer, or wallet/credits if available. The credit card form includes fields for cardholder name, card number, expiration date, and CVV, all validated in real-time. Users may see options to save payment methods for future use. The page displays security badges and SSL encryption information. After successful payment processing, users receive a booking confirmation page with booking reference number, email confirmation, and options to download invoice or voucher. Failed payments show appropriate error messages and allow users to retry with different payment methods.

---

## 17. Currency & Language Selection
![Currency Language Selection](images/17_currency_language.png)

The top navigation includes dropdowns for currency and language selection. The currency selector shows common currencies (USD, EUR, GBP, etc.) with flags and codes. Selecting a currency updates all prices throughout the site in real-time without losing search context or cart items. Similarly, the language selector offers multiple languages (English, Arabic, Spanish, French, etc.) and switches the entire interface to the selected language. These preferences are saved in session/cookies and persist across pages. For authenticated users, these preferences may be saved to their profile.

---

## 18. Search & Filters
![Search Filters](images/18_filters.png)

All listing pages (hotels, flights, tours, cars) include robust filtering and sorting capabilities. The left sidebar contains collapsible filter sections for price range (with slider), ratings (star ratings for hotels, review scores), amenities/features (checkboxes for facilities), location/area (for hotels), departure times (for flights), duration (for tours), vehicle type (for cars), and more specific filters relevant to each category. As users select filters, results update dynamically without page refresh, showing the number of matching results. Users can clear individual filters or reset all filters at once. A summary of active filters appears at the top of results with quick remove options.

---

## 19. Reviews & Ratings
![Reviews Ratings](images/19_reviews_ratings.png)

Throughout the site, users can see reviews and ratings for hotels, tours, and cars. On listing pages, each item shows an aggregate rating (e.g., 4.5/5 stars) and number of reviews. On detail pages, a dedicated reviews section displays individual guest reviews with ratings (overall, and category-specific like cleanliness, service, location), reviewer name and country, review date, stay date, and detailed comments. Reviews may include photos uploaded by guests. Users can filter reviews by rating, date, or traveler type. Authenticated users who have completed bookings can submit their own reviews through their dashboard or via email prompts after their stay/trip. The review form includes rating sliders/stars for different aspects and a text area for detailed feedback.

---

## 20. Offers & Deals
![Offers Deals](images/20_offers_deals.png)

The Offers page showcases special deals, promotions, and packages. It displays promotional banners, featured deals with discount percentages or special rates, last-minute offers, and seasonal packages. Each offer card shows the deal title, attractive image, discount information, validity period, terms and conditions link, and a Book Now button. Users can filter offers by type (hotels, flights, packages), destination, or travel dates. Clicking on an offer applies the promotional code automatically or takes users to pre-filled search with discounted rates. Newsletter subscription options may be available to receive exclusive deals via email.

---

## Logout
The logout function is accessible from the user dropdown menu in the top navigation or from the dashboard. When clicked, the system terminates the user session, clears sensitive session data, and redirects the user to the home page or login page. A confirmation message may appear confirming successful logout. After logout, any attempt to access protected pages (like dashboard or bookings) redirects to the login page. The shopping cart or search criteria may be cleared depending on session configuration.
