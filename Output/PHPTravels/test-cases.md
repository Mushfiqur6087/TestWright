# Phptravels

**Base URL:** 
**Generated:** 2026-04-20T18:34:19.329852

## Summary

| Metric | Count |
|--------|-------|
| **Total Tests** | 323 |

### By Type

| Type | Count |
|------|-------|
| Positive | 192 |
| Negative | 80 |
| Edge Case | 40 |
| Standard | 11 |

### By Priority

| Priority | Count |
|----------|-------|
| High | 171 |
| Medium | 134 |
| Low | 18 |

---

## Test Cases

### Home Page & Search

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 1.HP&S-001 | Search on Hotels tab with valid criteria redirects to hotel results | None | 1. Click the "Hotels" tab on the search widget<br>2. Fill all required fields on the Hotels tab (destination, check-in/check-out dates, number of rooms, guest count) with valid values<br>3. Click "Search" | User is redirected to the hotel results listing page. | High |
| 1.HP&S-002 | Perform a One-way flight search with valid data | Flights tab is active | 1. Select trip type "One-way"<br>2. Fill all required flight fields (departure city, arrival city, departure date, passenger counts, cabin class)<br>3. Click "Search" | User is redirected to the flight results listing page for the provided One-way criteria. | High |
| 1.HP&S-003 | Perform a Round-trip flight search with valid data | Flights tab is active | 1. Select trip type "Round-trip"<br>2. Fill all required flight fields (departure city, arrival city, departure and return dates, passenger counts, cabin class)<br>3. Click "Search" | User is redirected to the flight results listing page for the provided Round-trip criteria. | High |
| 1.HP&S-004 | Perform a Multi-city flight search with valid data | Flights tab is active | 1. Select trip type "Multi-city"<br>2. Fill all required fields for each flight segment (each segment's departure city, arrival city, and date), and fill passenger counts and cabin class once<br>3. Click "Search" | User is redirected to the flight results listing page showing results for the configured multi-city itinerary. | High |
| 1.HP&S-005 | Search on Tours tab with valid destination and travel date range redirects to results listing | None | 1. Click "Tours" tab<br>2. Fill all required fields (destination, travel date range) with valid values<br>3. Click "Search" | User is redirected to the tour results listing page. | High |
| 1.HP&S-006 | Search cars with valid pick-up and drop-off details | Home page is open | 1. Click the "Cars" tab<br>2. Fill all required fields (pick-up location, drop-off location, pick-up date and time, drop-off date and time)<br>3. Click "Search" | User is redirected to the car results listing page and search results are displayed. | High |
| 1.HP&S-007 | Hotels tab shows hotel-specific search fields when selected | None | 1. Click the "Hotels" tab on the search widget<br>2. Observe that destination, check-in/check-out dates, number of rooms, and guest count fields are visible | Hotel-specific search fields become visible for the Hotels tab. | Medium |
| 1.HP&S-008 | Flights tab displays flight-specific search fields | None | 1. Click the "Flights" tab in the search widget | Flight-specific fields (trip type, departure and arrival city, travel dates, passenger count, cabin class, Search button) are visible on the widget. | Medium |
| 1.HP&S-009 | Cabin class dropdown shows all cabin options | Flights tab is active | 1. Open the cabin class dropdown | Cabin class options include Economy, Premium Economy, Business, and First. | Medium |
| 1.HP&S-010 | Switch to Tours tab displays Tours search fields | None | 1. Click "Tours" tab | Search widget updates to show destination and travel date range fields for Tours. | Medium |
| 1.HP&S-011 | Switching to Cars tab displays car-specific search fields | Home page is open | 1. Click the "Cars" tab<br>2. Verify that pick-up location, drop-off location, pick-up date and time, and drop-off date and time fields are visible in the search widget | Car-specific search fields are visible for the Cars tab. | Medium |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 1.HP&S-012 | Submit with all required fields empty | None | 1. Click the "Hotels" tab on the search widget<br>2. Leave all required fields empty<br>3. Click "Search" | Validation errors shown for all required fields. | Medium |
| 1.HP&S-013 | Submit with all required fields empty | Flights tab is active | 1. Leave all required fields empty<br>2. Click "Search" | Validation errors shown for all required fields. | Medium |
| 1.HP&S-014 | Submit with all required fields empty | None | 1. Click "Tours" tab<br>2. Leave all required fields empty<br>3. Click "Search" | Validation errors shown for all required fields. | Medium |
| 1.HP&S-015 | Submit with all required fields empty | Home page is open | 1. Click the "Cars" tab<br>2. Leave all required fields empty<br>3. Click "Search" | Validation errors shown for all required fields. | Medium |
| 1.HP&S-016 | Inline errors appear for invalid car search inputs | Home page is open | 1. Click the "Cars" tab<br>2. Fill required fields with invalid data for car-specific fields (e.g., invalid location format or inconsistent date/time)<br>3. Click "Search" | Inline validation errors are displayed for the invalid fields in the Cars search form. | Medium |

---

### User Registration

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 2.USEREG-001 | Register new user with valid data | None | 1. Fill all required fields (First Name, Last Name, Email, Password, Confirm Password, Mobile Number, country code dropdown, Address, Country) with valid data<br>2. Check the Terms and Conditions checkbox<br>3. Click "Submit" | Account is created, user is automatically logged in and redirected to their dashboard, and the user is prompted to verify their email. | High |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 2.USEREG-002 | Submit with an email that already exists | An account exists using the email address to be entered. | 1. Fill all required fields using an email address already registered in the system<br>2. Check the Terms and Conditions checkbox<br>3. Click "Submit" | Inline validation error indicating the email is already in use and registration is blocked. | High |
| 2.USEREG-004 | Submit with all required fields empty | None | 1. Leave all required fields empty<br>2. Click "Submit" | Validation errors shown for all required fields. | Medium |
| 2.USEREG-005 | Submit with non-matching Password and Confirm Password | None | 1. Fill all required fields with valid values except enter a different value in Confirm Password<br>2. Check the Terms and Conditions checkbox<br>3. Click "Submit" | Inline validation error indicating Password and Confirm Password must match. | Medium |
| 2.USEREG-006 | Submit with invalid email format | None | 1. Fill all required fields with valid values except provide an invalid email format<br>2. Check the Terms and Conditions checkbox<br>3. Click "Submit" | Inline validation error indicating the email format is invalid. | Medium |

#### Edge Case Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 2.USEREG-003 | Registered user is prompted to verify email before full access | None | 1. Fill all required fields (First Name, Last Name, Email, Password, Confirm Password, Mobile Number, country code dropdown, Address, Country) with valid data<br>2. Check the Terms and Conditions checkbox<br>3. Click "Submit" | User is logged in and redirected to the dashboard but sees a prompt requiring email verification before gaining full access to protected features. | High |

---

### User Login

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 3.USELOG-001 | Login with valid credentials redirects to dashboard | None | 1. Fill all required fields (Email, Password) with valid credentials<br>2. Click "Login" | User is redirected to their dashboard after successful authentication. | High |
| 3.USELOG-002 | Login after attempting to access a protected page redirects back to that page | User attempted to access a protected page and was redirected to the login page | 1. Fill all required fields (Email, Password) with valid credentials<br>2. Click "Login" | User is redirected to the page they were previously trying to access. | High |
| 3.USELOG-010 | Social login options (Google, Facebook) are displayed when enabled | Social login options (Google and Facebook) are enabled in system settings | 1. Observe the login form area on the page<br>2. Verify that Google and Facebook social login options are displayed | Google and Facebook social login options are visible on the login page. | Medium |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 3.USELOG-003 | Login attempt with invalid credentials shows error and clears password | None | 1. Fill all required fields (Email, Password) with invalid credentials<br>2. Click "Login" | An error message is displayed indicating invalid credentials and the password field is cleared. | High |
| 3.USELOG-011 | Submit with all required fields empty | None | 1. Leave all required fields empty<br>2. Click "Login" | An error is shown indicating login failed and the password field is cleared. | Medium |

#### Edge Case Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 3.USELOG-004 | CAPTCHA is required after multiple consecutive failed login attempts | None | 1. Perform consecutive invalid login attempts by filling all required fields (Email, Password) with invalid credentials and clicking "Login" repeatedly<br>2. Observe the login form for additional verification elements | CAPTCHA verification is displayed and may be required for further login attempts. | High |

#### Standard Quality Patterns

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 3.USELOG-005 | Post-logout redirect to login when revisiting an authenticated page | Tester has a valid user account and can log in (use a normal user account). | 1. Log in with valid credentials on the Login page.<br>2. Navigate to a protected page (e.g., User Dashboard) and confirm authenticated content is visible.<br>3. Click Logout to end the session.<br>4. Attempt to navigate to the protected page again (use the same link or direct navigation). | After logout, navigating to the previously-open authenticated page redirects to the Login page (no authenticated content is shown). | High |
| 3.USELOG-006 | Browser back button after logout does not restore authenticated content | Tester has a valid user account and can log in. | 1. Log in with valid credentials and open a protected page (e.g., Booking Management).<br>2. Click Logout to end the session.<br>3. Use the browser Back button to return to the previously viewed page. | Using the Back button does not display cached authenticated content; the page either shows the login screen or a notice that the session has ended. | High |
| 3.USELOG-007 | Session expiry during form entry forces re-authentication or shows expiry notice | Tester has a valid user account and can log in; tester can fill a booking form. | 1. Log in with valid credentials and navigate to a protected form page (e.g., Flight Booking).<br>2. Begin filling the form but do not submit.<br>3. Simulate session expiry (wait beyond the application's session timeout or delete the session cookie) and then attempt to submit the form or interact further with the page. | On submission or further interaction after session expiry, the application either displays a session-expired notice and redirects to Login, or requires re-authentication before accepting the action; no data submission should proceed as an authenticated request. | High |
| 3.USELOG-008 | CAPTCHA or lockout enforced after repeated failed login attempts | Tester can reach the Login page. | 1. Open the Login page and enter a valid username with an incorrect password multiple times in a row (repeat failed attempts according to application policy, e.g., 3–5 attempts).<br>2. After the configured threshold, attempt another login. | After repeated failed attempts the application enforces additional protection (a CAPTCHA appears or further attempts are locked/blocked) and prevents unrestricted login attempts until the protection requirement is satisfied. | High |
| 3.USELOG-009 | After password change the old password no longer authenticates | Tester has a valid user account and knows the current password; tester can access the account settings page to change the password. | 1. Log in with the current password, navigate to the account settings or change-password page, and change the password to a new value.<br>2. Log out, then attempt to log in using the old password and verify the result; finally, log in with the new password to confirm it works. | Logging in with the old password fails after the change; logging in with the new password succeeds, confirming the old credentials were invalidated. | High |
| 3.USELOG-012 | Page refresh on authenticated page keeps the user logged in | Tester has a valid user account and can log in. | 1. Log in with valid credentials and open a protected page (e.g., User Dashboard).<br>2. Click the browser Refresh/Reload button.<br>3. Observe the page and any authenticated UI elements after reload. | After refresh, the user remains authenticated and protected content and user-specific UI remain visible (no redirect to login). | Medium |
| 3.USELOG-013 | Remember Me checked persists session after closing and reopening the browser | Tester has a valid user account and can access the Login page. | 1. Navigate to the Login page, enter valid credentials, check the 'Remember Me' checkbox, and submit to log in.<br>2. Close all browser windows completely, then reopen the browser and navigate back to the application without logging in again. | After reopening the browser, the tester remains authenticated (or is still able to access protected pages without re-entering credentials), indicating the session persisted when 'Remember Me' was checked. | Medium |
| 3.USELOG-014 | Remember Me unchecked does not persist session after closing and reopening the browser | Tester has a valid user account and can access the Login page. | 1. Navigate to the Login page, enter valid credentials, ensure 'Remember Me' is unchecked, and submit to log in.<br>2. Close all browser windows completely, then reopen the browser and navigate back to the application. | After reopening the browser, the user is not still authenticated and is presented the Login page (session did not persist when 'Remember Me' was unchecked). | Medium |
| 3.USELOG-015 | Expired password-reset link shows an appropriate error | Tester has access to an account email inbox to receive password reset links. | 1. On the Login page, use Forgot Password to request a reset for a valid account and capture the reset link from the received email.<br>2. Wait until the application's stated reset-link expiry period has passed, then open the captured reset link in the browser. | Opening an expired password-reset link shows a clear error message indicating the link has expired and prevents resetting the password using that link. | Medium |
| 3.USELOG-016 | Forgot password shows error for unregistered email (no silent success) | Tester can reach the Forgot Password form. | 1. Open the Forgot Password page, enter an email address that is not registered in the system, and submit the request.<br>2. Observe the response shown on the page. | The application displays a clear error or message indicating the email is not registered (not a silent success), so the tester understands the address is not in the system. | Medium |

---

### Forgot Password

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 4.FORPAS-001 | Send password reset link for existing account | None | 1. Fill all required fields (Email) with an email address that exists in the system<br>2. Click "Reset Password" button | Confirmation message is shown and a reset link is sent to the provided email address. | High |
| 4.FORPAS-002 | Reset password using valid reset link | User is on the password reset page via a valid, unexpired reset link | 1. Fill all required fields (New password, Confirm new password) with matching valid values<br>2. Click the submit action to save the new password | Password is changed, the user is redirected to the login page, and a success message is displayed. | High |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 4.FORPAS-004 | Submit with all required fields empty | None | 1. Leave all required fields empty<br>2. Click "Reset Password" button | Validation error is shown and the form remains editable. | Medium |
| 4.FORPAS-005 | Submit with non-existent email shows error and keeps form editable | None | 1. Fill all required fields (Email) with an address that is not registered in the system<br>2. Click "Reset Password" button | An error message is shown indicating the email was not found and the form remains editable. | Medium |
| 4.FORPAS-006 | Password and confirmation mismatch on reset page | User is on the password reset page via a valid reset link | 1. Fill New password with a valid value and Confirm new password with a different value<br>2. Click the submit action to save the new password | Validation error is shown indicating the passwords do not match and the form remains editable. | Medium |

#### Edge Case Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 4.FORPAS-003 | Attempt to use expired reset link shows expiration error | User is on the password reset page via a reset link older than 24 hours | 1. Fill all required fields (New password, Confirm new password) with matching valid values<br>2. Click the submit action to save the new password | An error is shown indicating the reset link has expired and the password is not changed. | High |

---

### Hotels Search & Listing

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 5.HS&L-001 | Submit hotels search form with valid criteria redirects to listing page and shows results | None | 1. Fill all required fields (Destination, Check-in date, Check-out date, Number of rooms, Adults, Children)<br>2. Click "Search" | User is redirected to the listing page showing matching hotels. | High |
| 5.HS&L-002 | Hotel card displays expected elements in search results | Search results listing page is open | 1. For a hotel card in the results, verify Hotel name, Location, Star rating, Thumbnail image, Starting price per night, Amenity icons, and a "Book Now" button are displayed | Each hotel card shows name, location, star rating, thumbnail image, starting price per night, amenity icons, and a Book Now button. | High |
| 5.HS&L-003 | Apply price range filter updates results and shows active filter summary | None | 1. Expand the price range filter in the left sidebar and set a price range<br>2. Observe the hotel listing and the active filters summary area | Hotel listing updates to reflect the selected price range and the active filters summary displays the selected price filter with an individual remove control and a Reset all control. | High |
| 5.HS&L-004 | Apply multiple filters (star rating, amenities, hotel type) and verify combined results | None | 1. Select a star rating in the star rating filter, choose one or more amenities, and pick a hotel type in the left sidebar<br>2. Observe the hotel listing and the active filters summary area | Hotel listing updates to show results that match all selected filters and the active filters summary lists each applied filter with individual remove buttons and a Reset all control. | High |
| 5.HS&L-005 | Filtered hotel card displays required details | At least one hotel remains visible after applying a filter | 1. Apply any filter in the left sidebar to narrow the listing<br>2. Inspect the first visible hotel card in the results | Each visible hotel card shows name, location, star rating, a thumbnail image, the starting price per night, amenity icons, and a Book Now button. | High |
| 5.HS&L-006 | Remove a single active filter and verify results update dynamically | Search results are displayed and at least one active filter is shown in the active filters summary. | 1. Click the individual remove button for one active filter in the active filters summary<br>2. Verify the removed filter is no longer displayed in the active filters summary<br>3. Verify the results list updates dynamically and each visible hotel card shows name, location, star rating, thumbnail image, starting price per night, amenity icons, and a Book Now button | Selected filter is removed from the summary; results refresh dynamically and hotel cards display the expected information. | High |
| 5.HS&L-007 | Remove one filter while other active filters remain and verify results reflect remaining filters | Search results are displayed and multiple active filters are shown in the active filters summary. | 1. Click the individual remove button for one active filter in the active filters summary<br>2. Verify that other active filters remain listed in the active filters summary<br>3. Verify the results list updates dynamically to reflect only the remaining active filters | Only the targeted filter is removed while other filters remain; results update dynamically to reflect the remaining filters. | High |
| 5.HS&L-008 | Remove the last active filter and verify the active filters summary is cleared and results update | Search results are displayed and exactly one active filter is shown in the active filters summary. | 1. Click the individual remove button for the single active filter in the active filters summary<br>2. Verify the active filters summary no longer shows any individual filters<br>3. Verify the results list updates dynamically to reflect the filter removal | Active filters summary is cleared of individual filters and results update dynamically to reflect the removed filter. | High |
| 5.HS&L-009 | Reset all clears all active filters and refreshes listing to unfiltered results | Search results are displayed | 1. Apply multiple filters (price range, star rating, facilities/amenities, hotel type, board basis)<br>2. Click the "Reset all" control | Listing refreshes dynamically to show unfiltered results, the active filters summary is cleared, and each hotel card displays name, location, star rating, thumbnail image, starting price per night, amenity icons, and a Book Now button. | High |
| 5.HS&L-010 | Sort results by price low to high and verify ascending prices | Hotel search results are visible on the page. | 1. Select the "Sort by price (low to high)" option from the sort control<br>2. Capture the starting prices shown on the visible hotel cards<br>3. Verify the captured starting prices are in ascending order | Hotel cards are reordered so starting prices appear from lowest to highest. | High |
| 5.HS&L-011 | Sort results by price high to low and verify descending prices | Hotel search results are visible on the page. | 1. Select the "Sort by price (high to low)" option from the sort control<br>2. Capture the starting prices shown on the visible hotel cards<br>3. Verify the captured starting prices are in descending order | Hotel cards are reordered so starting prices appear from highest to lowest. | High |
| 5.HS&L-012 | Sort results by star rating and verify hotels are ordered by rating | Hotel search results are visible on the page. | 1. Select the "Sort by star rating" option from the sort control<br>2. Capture the star ratings shown on the visible hotel cards<br>3. Verify the captured star ratings are ordered with higher-rated hotels before lower-rated hotels | Hotel cards are reordered so hotels with higher star ratings appear before those with lower star ratings. | High |
| 5.HS&L-013 | Sort results by guest rating and verify hotels are ordered by guest score | Hotel search results are visible on the page. | 1. Select the "Sort by guest rating" option from the sort control<br>2. Capture the guest ratings shown on the visible hotel cards<br>3. Verify the captured guest ratings are ordered with higher guest-rated hotels before lower-rated hotels | Hotel cards are reordered so hotels with higher guest ratings appear before those with lower guest ratings. | High |
| 5.HS&L-014 | Hotel card displays required elements in search results | Hotel search results are visible on the page. | 1. Inspect any visible hotel card<br>2. Verify the card shows the hotel name, location, star rating, thumbnail image, starting price per night, amenity icons, and a "Book Now" button | Each hotel card displays name, location, star rating, thumbnail image, starting price per night, amenity icons, and a Book Now button. | High |
| 5.HS&L-015 | Verify Reset all control remains visible when active filters persist after removing an individual filter | Search results are displayed and multiple active filters plus the Reset all control are visible in the active filters summary. | 1. Confirm the Reset all control is visible in the active filters summary<br>2. Click the individual remove button for one active filter<br>3. Verify the Reset all control remains visible while other active filters remain listed | Reset all control remains visible in the active filters summary as long as there are active filters. | Medium |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 5.HS&L-016 | Submit with all required fields empty | None | 1. Leave all required fields empty<br>2. Click "Search" | Validation errors shown for all required fields. | Medium |
| 5.HS&L-017 | Apply sort with no sort option selected | Hotel search results are visible on the page. | 1. Leave the sort control with no selection<br>2. Trigger the sort action or click the sort apply control | No reordering occurs; the listing remains unchanged or a prompt is shown indicating a sort option must be selected. | Medium |

#### Edge Case Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 5.HS&L-018 | Changing a filter control updates results immediately without explicit submit | None | 1. Change a filter control in the left sidebar (for example a checkbox, slider, or select)<br>2. Observe the hotel listing immediately after the change | The hotel listing refreshes dynamically to reflect the changed filter without requiring any submit action. | Medium |
| 5.HS&L-019 | Collapse then expand a filter group, select an option, and verify active summary updates | Left sidebar is visible | 1. Collapse a collapsible filter group in the left sidebar<br>2. Expand the same filter group and select an option<br>3. Observe the active filters summary and the hotel listing | The active filters summary updates to include the newly selected filter and the hotel listing updates to reflect the selection. | Low |
| 5.HS&L-020 | Edge: Remove an active price-range filter and verify results update dynamically | Search results are displayed and a price range filter is active and shown in the active filters summary. | 1. Click the individual remove button for the active price range filter in the active filters summary<br>2. Verify the price range filter is no longer shown in the active filters summary<br>3. Verify the results list updates to reflect the removal and hotel cards continue to display required information | Price range filter is removed from the summary and the results update dynamically to reflect the change. | Low |
| 5.HS&L-021 | Click Reset all when no filters are active | Search results are displayed with no active filters | 1. Verify no active filters are present in the active filters summary<br>2. Click the "Reset all" control | Listing remains unchanged and the active filters summary remains empty (no individual remove buttons displayed). | Low |

---

### Flights Search & Listing

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 7.FS&L-001 | Sort listing by price | Flight search results are displayed | 1. Click the "Sort by price" control on the results listing<br>2. Verify the listing is reordered by price such that the displayed results reflect price sorting (price per passenger in each result is in sorted order) | Results are reordered according to price and the displayed order reflects price-based sorting. | High |
| 7.FS&L-002 | Sort listing by total duration | Flight search results are displayed | 1. Click the "Sort by duration" control on the results listing<br>2. Verify the listing is reordered by total duration such that the displayed results reflect duration sorting (total duration in each result is in sorted order) | Results are reordered according to total duration and the displayed order reflects duration-based sorting. | High |
| 7.FS&L-003 | Sort listing by departure time | Flight search results are displayed | 1. Click the "Sort by departure time" control on the results listing<br>2. Verify the listing is reordered by departure time such that the displayed results reflect chronological departure-time sorting | Results are reordered according to departure time and the displayed order reflects departure-time sorting. | High |
| 7.FS&L-004 | Sort listing by arrival time | Flight search results are displayed | 1. Click the "Sort by arrival time" control on the results listing<br>2. Verify the listing is reordered by arrival time such that the displayed results reflect chronological arrival-time sorting | Results are reordered according to arrival time and the displayed order reflects arrival-time sorting. | High |
| 7.FS&L-005 | Each flight result shows required details and action | Flight search results are displayed | 1. For one or more visible results, inspect the result card/row on the listing<br>2. Verify each inspected result shows airline logo and name, departure and arrival times and airports, total duration, number of stops (Non-stop, 1 stop, 2+ stops), price per passenger, and a "Select" button | Each visible result displays the airline logo and name, departure and arrival times and airports, total duration, number of stops, price per passenger, and a Select button. | High |

---

### Flight Booking

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 8.FLIBOO-001 | Complete booking with all required passenger and lead contact details | Booking form is displayed with selected flight and passenger entries | 1. Fill all required fields for each traveler (Title, First name, Last name, Date of birth, Passport number, Passport expiry) and fill lead passenger contact fields (Email, Phone)<br>2. Click "Continue" | User proceeds to the payment page. | High |
| 8.FLIBOO-002 | Full itinerary summary shows passenger count and cabin class | Booking form is displayed with selected flight | 1. Verify Full itinerary summary is displayed, and verify Passenger count and Cabin class are displayed | Itinerary summary, passenger count, and cabin class are visible on the booking page. | High |
| 8.FLIBOO-003 | Fare breakdown displays base fare, taxes, fees, and totals | Booking form is displayed with price section visible | 1. Verify Fare breakdown displays Base fare, Taxes, Fees, Total per passenger, and Total overall | Fare breakdown shows base fare, taxes, fees, total per passenger, and overall total. | High |
| 8.FLIBOO-005 | Continue proceeds when optional meal and seat selection are left empty | Booking form is displayed with passenger sections visible | 1. Fill all required fields for each traveler (Title, First name, Last name, Date of birth, Passport number, Passport expiry) and fill lead passenger contact fields (Email, Phone); leave Meal preferences and Seat selection unselected<br>2. Click "Continue" | User proceeds to the payment page despite optional fields being empty. | Medium |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 8.FLIBOO-006 | Submit with all required fields empty | Booking form is displayed | 1. Leave all required fields empty<br>2. Click "Continue" | Validation errors shown for all required fields and progression to payment is blocked. | Medium |
| 8.FLIBOO-007 | Invalid lead passenger email format blocks progression | Booking form is displayed with passenger sections visible | 1. Fill all required fields for each traveler (Title, First name, Last name, Date of birth, Passport number, Passport expiry) and fill lead passenger Phone with a valid phone number; enter an invalid format in the lead passenger Email field<br>2. Click "Continue" | Inline validation error is displayed for the Email field and progression to payment is blocked. | Medium |

#### Standard Quality Patterns

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 8.FLIBOO-004 | Direct URL access to protected module while logged out redirects to login | Tester is logged out (no active session). | 1. Open a new browser window (not logged in).<br>2. Enter the direct URL for the Flight Booking page or paste the bookmarked URL for Flight Booking and press Enter. | Accessing the Flight Booking URL while logged out redirects the tester to the Login page before any protected content is shown. | High |

---

### Tours Search & Listing

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 9.TS&L-001 | Submit tours search form with all valid criteria | None | 1. Fill all required fields (destination, travel dates, tour type, duration, budget range) with valid values<br>2. Click "Search" on the tours search form | User is redirected to the listing page and matching tour cards are displayed. | High |
| 9.TS&L-002 | Submit tours search form with destination only | None | 1. Fill the destination field with a valid location, leave other search fields blank or at defaults<br>2. Click "Search" on the tours search form | User is redirected to the listing page and tour cards matching the destination are displayed. | High |
| 9.TS&L-003 | Search results show required tour card details | A listing page with search results is displayed | 1. Inspect visible tour cards on the listing page<br>2. Verify each card shows tour image, name, destination, duration, starting price per person, a brief description, availability status, and traveler rating | Each visible tour card displays the listed elements. | High |
| 9.TS&L-004 | Filter results by destination | Tours listing page is open | 1. Select a destination value in the destination filter<br>2. Click the "Apply Filters" control or wait for the listing to update<br>3. Verify each displayed tour card shows the selected destination and displays tour image, name, duration, starting price per person, a brief description, availability status, and traveler rating | Listing shows only tours for the selected destination and each card displays the expected tour information. | High |
| 9.TS&L-005 | Filter results by tour type | Tours listing page is open | 1. Select a tour type in the tour type filter<br>2. Click the "Apply Filters" control or wait for the listing to update<br>3. Verify all displayed tour cards correspond to the selected tour type and each card shows the expected tour information | Listing is narrowed to the chosen tour type and cards display required tour details. | High |
| 9.TS&L-006 | Filter results by price range | Tours listing page is open | 1. Adjust the price range filter to a specific minimum and maximum value<br>2. Click the "Apply Filters" control or wait for the listing to update<br>3. Verify each displayed tour's starting price per person falls within the selected price range and each card shows the expected tour information | Only tours with starting prices inside the selected range are displayed and cards include the expected fields. | High |
| 9.TS&L-007 | Combine multiple sidebar filters to narrow results | Tours listing page is open | 1. Select values for multiple filters (destination, tour type, price range, duration, and departure dates) in the sidebar<br>2. Click the "Apply Filters" control or wait for the listing to update<br>3. Verify each displayed tour meets all selected criteria and each card shows the expected tour information | Results are narrowed according to the combined filters and every card displays the required tour details. | High |
| 9.TS&L-008 | Listing card displays required tour information | Tours listing page is open and at least one tour is displayed | 1. Inspect a tour card in the listing<br>2. Verify the card shows tour image, name, destination, duration, starting price per person, a brief description, availability status, and traveler rating | Tour card displays all expected information fields. | High |
| 9.TS&L-009 | Sort results by popularity reorders listing and preserves card details | Listing page is displayed with multiple tour results. | 1. Capture the current sequence of visible tour names in the listing<br>2. Open the sort control and select "Sort by popularity"<br>3. Capture the new sequence of visible tour names | The visible sequence of tours changes to reflect ordering by popularity; each visible tour card shows tour image, name, destination, duration, starting price per person, a brief description, availability status, and traveler rating. | High |
| 9.TS&L-010 | Sort results by price reorders listings by starting price ascending | Listing page is open with multiple tour results visible. | 1. Open the sort control and select "Sort by price"<br>2. Observe the starting price per person on each displayed tour card | Tour results are ordered by starting price per person from lowest to highest. | High |
| 9.TS&L-011 | Sort results by duration reorders tour listing | Listing page displays multiple tour results with varying durations | 1. Select "Sort by duration" from the sort control on the listing page<br>2. Observe the duration values shown on consecutive tour cards | Tour results are reordered by duration so that durations appear in consistent ascending order across the listing | High |
| 9.TS&L-012 | Tour result card displays all required fields | Listing page displays at least one tour result card | 1. Inspect a visible tour result card<br>2. Verify it shows the tour image, name, destination, duration, starting price per person, a brief description, availability status, and traveler rating | Each inspected tour card displays image, name, destination, duration, starting price per person, brief description, availability status, and traveler rating | High |
| 9.TS&L-013 | Sort results by rating orders tours by traveler rating (descending) | Listing page displays multiple tours with traveler ratings. | 1. Select "Sort by rating" in the sort control on the listing page | The tour results reorder so that traveler rating values are in non-increasing order (each preceding rating is greater than or equal to the next). | High |
| 9.TS&L-014 | Sort results by rating while a sidebar filter is active | Listing page displays sidebar filters and multiple results. | 1. Apply a sidebar filter (for example: set a destination filter) and ensure filtered results are visible<br>2. Select "Sort by rating" in the sort control | Results remain filtered by the sidebar criteria and are ordered by traveler rating. | High |
| 9.TS&L-015 | Listing page includes expected sidebar filters | A listing page with search results is displayed | 1. Inspect the listing page sidebar<br>2. Verify sidebar filters include destination, tour type, price range, duration, and departure dates | All named sidebar filters are present and available for use. | Medium |
| 9.TS&L-016 | Listing page provides sorting options for results | A listing page with search results is displayed | 1. Locate the Sort by control on the listing page<br>2. Verify Sort by options include popularity, price, duration, and rating | Sort control offers popularity, price, duration, and rating options. | Medium |
| 9.TS&L-017 | Sidebar shows all expected filter controls | Tours listing page is open | 1. Observe the sidebar filter area on the listing page<br>2. Verify presence of destination filter, tour type filter, price range filter, duration filter, and departure dates filter | All five sidebar filters are visible and interactable. | Medium |
| 9.TS&L-018 | Filter results by duration | Tours listing page is open | 1. Select a duration range in the duration filter<br>2. Click the "Apply Filters" control or wait for the listing to update<br>3. Verify each displayed tour's duration matches the selected range and each card shows the expected tour information | Listing displays tours whose durations match the selected filter and cards show required tour details. | Medium |
| 9.TS&L-019 | Filter results by departure dates | Tours listing page is open | 1. Select a departure date range using the departure dates filter<br>2. Click the "Apply Filters" control or wait for the listing to update<br>3. Verify displayed tours have available departure dates within the selected range and each card shows the expected tour information | Only tours with departures in the selected date range are shown and cards display the expected fields. | Medium |
| 9.TS&L-020 | Sort control contains popularity, price, duration, and rating options | Listing page is displayed. | 1. Open the sort control/dropdown<br>2. Inspect the list of available sort options | Sort options include 'Sort by popularity', 'Sort by price', 'Sort by duration', and 'Sort by rating'. | Medium |
| 9.TS&L-021 | Applying popularity sort keeps sidebar filters visible and usable | Listing page is displayed with sidebar filters visible. | 1. Verify sidebar filters are visible<br>2. Select 'Sort by popularity' from the sort control<br>3. Attempt to interact with at least one sidebar filter | Sorting by popularity is applied and sidebar filters remain visible and are still selectable. | Medium |
| 9.TS&L-022 | Sort control includes price option | Listing page is open with multiple tour results visible. | 1. Open the sort control<br>2. Verify that "price" appears as an available sort option | "Price" is listed as a selectable sort option. | Medium |
| 9.TS&L-023 | Sorted results preserve complete tour card details | Listing page is open with multiple tour results visible. | 1. Select "Sort by price" from the sort control<br>2. Inspect several displayed tour cards for required fields (tour image, name, destination, duration, starting price per person, brief description, availability status, traveler rating) | Each inspected tour card displays all listed fields after sorting. | Medium |
| 9.TS&L-024 | Sort control includes duration as a sorting option | Listing page is visible | 1. Open the sort control on the listing page<br>2. Verify that the 'duration' option is present among the available sort choices | 'Duration' appears as one of the selectable sort options | Medium |
| 9.TS&L-025 | Sort by rating preserves display of required fields on each tour card | Listing page shows at least one tour result. | 1. Select "Sort by rating" in the sort control<br>2. Inspect one or more visible tour cards | Each inspected card shows tour image, name, destination, duration, starting price per person, a brief description, availability status, and traveler rating. | Medium |
| 9.TS&L-026 | Sort control offers rating option alongside other sort types | Listing page is open with the sort control visible. | 1. Open the sort control/dropdown on the listing page<br>2. Check the available sort options | Sort options include popularity, price, duration, and rating. | Medium |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 9.TS&L-027 | Submit with all required fields empty | None | 1. Leave all required fields empty<br>2. Click "Search" on the tours search form | Validation errors shown for all required fields and the user is not redirected to the listing page. | Medium |
| 9.TS&L-028 | Apply with all sidebar filters left unselected/cleared | Tours listing page is open | 1. Leave all sidebar filters unselected or cleared<br>2. Click the "Apply Filters" control or wait for the listing to update | Validation errors shown for all required filter fields. | Medium |
| 9.TS&L-029 | Sort by popularity option missing from sort control | Listing page is displayed. | 1. Open the sort control/dropdown<br>2. Attempt to locate and select the 'Sort by popularity' option | The 'Sort by popularity' option is not available and sorting by popularity cannot be applied. | Medium |

#### Edge Case Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 9.TS&L-030 | Sorting when only one tour result is visible is a no-op and card shows required fields | Listing page is displayed with only one tour result. | 1. Confirm there is exactly one visible tour card<br>2. Select 'Sort by popularity' from the sort control<br>3. Inspect the single tour card for required content | The listing remains with the single tour and the tour card shows tour image, name, destination, duration, starting price per person, a brief description, availability status, and traveler rating. | Low |
| 9.TS&L-031 | Select sort by duration with no result cards visible | Listing page currently shows zero tour result cards | 1. Confirm that no tour result cards are visible on the listing page<br>2. Select "Sort by duration" from the sort control | No errors occur and the page remains in an empty-state; UI indicates no results available | Low |
| 9.TS&L-032 | Sort by rating when some cards lack traveler rating | Listing page contains at least one tour card that does not display a traveler rating. | 1. Select "Sort by rating" in the sort control | Results update; cards that display traveler ratings are ordered by rating values and cards without ratings remain present (visible) after rated items. | Low |
| 9.TS&L-033 | Sort by rating with multiple tours having identical ratings maintains non-increasing rating order | Listing page contains multiple tours with identical traveler rating values. | 1. Select "Sort by rating" in the sort control | Visible results show traveler ratings in non-increasing order (ties allowed), ensuring no higher-rated item appears after a lower-rated item. | Low |

---

### Tour Details & Booking

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 10.TD&B-001 | Authenticated user selects departure date and books | User is authenticated and the tour details page is open | 1. Select an available departure date<br>2. Set the number of travelers (adults and children)<br>3. Verify pricing per person for adults and for children is visible<br>4. Click "Book Now" | Booking flow advances to the booking form with the selected date and traveler counts applied. | High |
| 10.TD&B-002 | Complete booking with valid traveler details and verify total cost breakdown | User is authenticated | 1. Fill all required booking fields (traveler names, contact details, special requirements) and ensure departure date and traveler counts are selected<br>2. Click "Confirm Booking" | Booking is confirmed and the booking review shows per-person pricing lines and the correct total cost breakdown based on the selected travelers. | High |
| 10.TD&B-005 | Tour details page shows available departure dates | None | 1. Observe the departure dates section on the tour details page<br>2. Verify at least one available departure date is displayed and selectable | Available departure dates are displayed and selectable on the tour details page. | Medium |
| 10.TD&B-006 | Tour details page shows per-person pricing for adults and children | None | 1. Observe the pricing section on the tour details page<br>2. Verify pricing per person for adults is displayed<br>3. Verify pricing per person for children is displayed | Per-person pricing for both adults and children is visible on the tour details page. | Medium |
| 10.TD&B-007 | Special requirements entered are shown on booking review | User is authenticated | 1. Fill all required booking fields including special requirements text<br>2. Click "Confirm Booking" | The booking review/confirmation displays the entered special requirements. | Medium |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 10.TD&B-003 | Unauthenticated user clicking Book Now is redirected to login | User is not authenticated and the tour details page is open | 1. Select an available departure date<br>2. Set the number of travelers (adults and children)<br>3. Click "Book Now" | The user is redirected to the login page before proceeding with booking. | High |
| 10.TD&B-004 | Unauthenticated user initiating booking is redirected to login | None | 1. Click "Book Now" on the tour details page | User is redirected to the login page before proceeding with booking. | High |
| 10.TD&B-008 | Submit with all required fields empty | None | 1. Leave all required fields empty<br>2. Click "Book Now" | Validation errors shown for all required fields. | Medium |
| 10.TD&B-009 | Submit with all required fields empty | None | 1. Leave all required fields empty<br>2. Click "Confirm Booking" | Validation errors shown for all required fields. | Medium |

#### Edge Case Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 10.TD&B-010 | Total cost breakdown shows separate per-person lines for adults and children | User is authenticated | 1. Select departure date and set number of adults and children<br>2. Fill traveler names and contact details<br>3. Observe the total cost breakdown section | Total cost breakdown lists per-person pricing for adults and children and shows a correctly summed total. | Medium |

---

### Cars Search & Listing

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 11.CS&L-001 | Submit car rental search form with valid criteria and view grouped listings | None | 1. Fill all required fields (pick-up location, drop-off location, pick-up date, drop-off date, pick-up time, drop-off time, driver age) with valid values<br>2. Click "Search" | User is redirected to the listing page; vehicles are grouped by category (Economy, Compact, SUV, Luxury, Van); sidebar filters (car type, transmission, fuel policy, rental company, price range) are visible; each listing shows vehicle image, make and model, transmission type, fuel policy, seating and luggage capacity, feature icons, price per day, total rental cost for the selected period, and a Book Now button. | High |
| 11.CS&L-002 | Apply a single sidebar filter (transmission) updates results dynamically and shows full listing details | Listing page is open with search results and a selected rental period. | 1. Select a transmission type in the sidebar filters<br>2. Wait for the listing results to update dynamically | Visible listings are filtered to the selected transmission; listings remain grouped by category and each visible listing shows vehicle image, make and model, transmission type, fuel policy, seating and luggage capacity, feature icons, price per day, total rental cost for the selected period, and a Book Now button. | High |
| 11.CS&L-003 | Apply multiple sidebar filters (car type, rental company, price range) and verify grouped filtered results | Listing page is open with search results and a selected rental period. | 1. Select one or more car type values in the sidebar filters, select one or more rental companies, and set a price range using the sidebar price control<br>2. Wait for the listing results to update dynamically | Visible listings reflect all selected filters; listings remain grouped by category and each listing displays the full vehicle details including price per day and total rental cost for the selected period. | High |
| 11.CS&L-004 | Book Now button is available on filtered listings and initiates booking action | Listing page is open with at least one visible listing after applying any filters. | 1. Apply a sidebar filter that yields at least one visible listing<br>2. Click the Book Now button on a visible listing | Clicking Book Now initiates the booking action for the selected vehicle (booking flow opens) and the selected listing includes a Book Now button. | High |
| 11.CS&L-005 | Clear applied sidebar filters restores original grouped results | Listing page is open with search results, and at least one sidebar filter can be applied. | 1. Apply one or more sidebar filters<br>2. Use the sidebar control to clear all applied filters | Listings return to the unfiltered state, grouped by category, showing vehicles across categories with full vehicle details. | Medium |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 11.CS&L-006 | Submit with all required fields empty | None | 1. Leave all required fields empty<br>2. Click "Search" | Validation errors shown for all required fields. | Medium |

#### Edge Case Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 11.CS&L-007 | Apply a combination of sidebar filters that yields no matches and verify empty-state handling | Listing page is open with search results and multiple filter options available. | 1. Select a combination of sidebar filters expected to produce no matching vehicles<br>2. Wait for the listing results to update dynamically | No vehicle listings are shown and the page displays a clear no-results message or suggestion indicating no matches for the selected filters. | Medium |
| 11.CS&L-008 | Apply price range at a boundary and verify prices and totals reflect selected range | Listing page is open with search results and a selected rental period. | 1. Set the sidebar price range control to a boundary value (minimum or maximum)<br>2. Wait for the listing results to update dynamically | Visible listings have price per day within the selected price range and the total rental cost reflects the selected rental period. | Low |

---

### Car Booking

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 12.CARBOO-001 | Confirm booking proceeds to payment when insurance selected and terms accepted | Selected vehicle and rental details pre-filled on the booking page. | 1. Fill all required booking fields (Driver full name, Age, License number, License issue country, Email, Phone number)<br>2. Select an insurance plan and review the terms<br>3. Check the boxes to accept the required terms (fuel policy, mileage limits, damage liability, cancellation)<br>4. Click "Confirm Booking" | Payment page or payment modal is displayed and booking proceeds to the payment stage. | High |
| 12.CARBOO-002 | Car booking page displays vehicle details, rental period, locations, times, and full pricing breakdown | Selected vehicle and rental details pre-filled on the booking page. | 1. Verify selected vehicle details and rental period are displayed<br>2. Verify pick-up and drop-off locations and pick-up/drop-off times are displayed<br>3. Verify pricing breakdown shows daily rate, number of rental days, taxes, insurance options, and additional fees | All listed booking details and the full pricing breakdown are visible on the page. | High |
| 12.CARBOO-005 | Selecting optional extras updates pricing breakdown | Pricing breakdown visible with base rate displayed. | 1. Select optional extras (GPS, Child seat, Additional driver)<br>2. Verify pricing breakdown updates to include fees for each selected extra and the total price reflects these additions | Pricing breakdown updates to include each selected optional extra and the booking total increases accordingly. | Medium |
| 12.CARBOO-006 | Selecting different insurance plans updates insurance line in pricing breakdown | Pricing breakdown and insurance options visible on the booking page. | 1. Select one insurance plan and verify the insurance line and total reflect that plan<br>2. Select an alternative insurance plan and verify the insurance line and total update to reflect the new selection | Insurance line and booking total update to reflect the chosen insurance plan each time. | Medium |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 12.CARBOO-003 | Attempt confirm without selecting an insurance plan | Selected vehicle and rental details pre-filled on the booking page. | 1. Fill all other required booking fields (Driver details and contact information), leave insurance plan unselected<br>2. Click "Confirm Booking" | Inline validation error indicating an insurance plan must be selected and progression is blocked. | High |
| 12.CARBOO-004 | Attempt confirm without accepting required terms | Selected vehicle and rental details pre-filled on the booking page. | 1. Fill all required booking fields and select an insurance plan, do not check the required terms acceptance boxes<br>2. Click "Confirm Booking" | Inline validation error indicating required terms must be accepted and progression is blocked. | High |
| 12.CARBOO-007 | Submit with all required fields empty | None | 1. Leave all required fields empty<br>2. Click "Confirm Booking" | Validation errors shown for all required fields and progression is blocked. | Medium |
| 12.CARBOO-008 | Submit with invalid email format shows inline error | Selected vehicle and rental details pre-filled on the booking page. | 1. Fill all required booking fields with valid data except enter an invalid email format<br>2. Click "Confirm Booking" | Inline validation error shown for the email field and progression is blocked. | Medium |

---

### Visa Services

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 13.VISSER-001 | View visa requirements for selected Nationality and Destination Country | None | 1. Select a Nationality and a Destination Country<br>2. Click "View Requirements" | Visa requirements are displayed for that nationality-destination combination, showing visa type, processing time, required documents, and fees. | High |
| 13.VISSER-002 | Submit visa application with valid data | User is on the Visa Application form page. | 1. Fill all required fields (Full name, Passport number, Passport expiry date, Date of birth, nationality, email, phone, purpose of visit, intended travel dates, duration of stay)<br>2. Click "Submit" | Submission is acknowledged and a success confirmation is displayed. | High |
| 13.VISSER-003 | Track submitted visa application status in dashboard bookings | A visa application has been submitted and user is on the bookings section of the dashboard. | 1. Locate the visa application entry in the bookings list<br>2. Open the application's status/details | After submission, application status can be tracked through the bookings section of the dashboard. | High |
| 13.VISSER-004 | Upload all required visa documents and submit | Document upload section is visible | 1. Attach files for all required document types (Passport Copy, Photographs, Invitation Letter, Supporting Documents) in the Document upload section<br>2. Click "Submit" or "Save" to complete the upload | All files are uploaded successfully and each required document shows a successful upload status or confirmation message. | High |
| 13.VISSER-005 | Nationality and Destination Country dropdowns show selectable options | None | 1. Open the Nationality dropdown and verify options are listed<br>2. Open the Destination Country dropdown and verify options are listed | Both dropdowns list countries and allow selection. | Medium |
| 13.VISSER-006 | Attach each required document individually and verify it appears in the list | Document upload section is visible | 1. Attach a Passport Copy file and verify it appears in the uploaded files list<br>2. Attach a Photographs file and verify it appears in the uploaded files list<br>3. Attach an Invitation Letter file and attach at least one Supporting Document file, verify all appear in the uploaded files list | Each attached document appears in the uploaded files list with the correct document type indicated. | Medium |
| 13.VISSER-007 | Upload multiple supporting documents and verify all are retained | Document upload section is visible | 1. Attach multiple Supporting Document files using the supporting documents upload control<br>2. Click "Submit"<br>3. Verify each supporting document is listed under uploaded supporting documents | All uploaded supporting documents are listed, retained after submission, and available for download or preview. | Medium |
| 13.VISSER-009 | Required documents list displays expected document types | Document upload section is visible | 1. View the required documents area in the Document upload section<br>2. Verify the list includes Passport Copy, Photographs, Invitation Letter, and Supporting Documents as required items | The required documents list enumerates Passport Copy, Photographs, Invitation Letter, and Supporting Documents. | Low |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 13.VISSER-008 | Submit with all required fields empty | None | 1. Leave all required fields empty<br>2. Click "View Requirements" | Validation errors shown for all required fields or user is prompted to select nationality and destination. | Medium |

#### Edge Case Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 13.VISSER-010 | View visa requirements when Nationality equals Destination Country | None | 1. Select the same country in both Nationality and Destination Country fields<br>2. Click "View Requirements" | Visa requirements are displayed for that nationality-destination combination, showing visa type, processing time, required documents, and fees. | Low |

---

### User Dashboard

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 14.USEDAS-001 | Open booking details shows full booking information and available actions | User is logged in and My Bookings list is visible with a booking eligible for cancellation or modification | 1. Click "View Details" for an upcoming booking that is eligible for cancellation or modification<br>2. Verify the details view displays booking reference, service type, travel dates, status, and available action buttons (Cancel, Modify) as permitted | Details view shows the full booking information and the available action buttons reflect cancellation/modification permissions. | High |
| 14.USEDAS-002 | My Bookings displays past and upcoming bookings with required columns and View Details action | User is logged in and My Bookings list is visible with both past and upcoming bookings across service types | 1. Inspect the My Bookings list<br>2. Verify each visible booking row displays booking reference, service type, travel dates, a status value, and a "View Details" action button | My Bookings lists past and upcoming bookings across Hotels, Flights, Tours, and Cars with booking reference, service type, travel dates, status, and a "View Details" action for each booking. | High |
| 14.USEDAS-003 | Cancel a permitted booking from My Bookings and verify status update | A booking exists in My Bookings for which cancellation is permitted. | 1. Click "Cancel" on the booking's row in My Bookings<br>2. Confirm cancellation in the confirmation dialog | Booking status changes to "Cancelled" and the booking row's available action buttons update accordingly. | High |
| 14.USEDAS-004 | My Bookings displays booking reference, service type, travel dates, status, and action buttons | User has at least one past or upcoming booking in My Bookings. | 1. Locate a booking row in My Bookings<br>2. Verify booking reference, service type, travel dates, and status are displayed and that action buttons for View Details, Cancel, and Modify appear where permitted | My Bookings lists bookings with booking reference, service type, travel dates, status, and action buttons for View Details, Cancel, and Modify where the booking type and cancellation policy permit. | High |
| 14.USEDAS-005 | My Bookings displays booking reference, service type, travel dates, status, and action buttons | User is authenticated and My Bookings page is visible | 1. Inspect the My Bookings listing rows on the page<br>2. Verify each row displays booking reference, service type, travel dates, status, and action buttons for View Details, Cancel, and Modify where applicable | My Bookings lists past and upcoming bookings with booking reference, service type, travel dates, status, and the appropriate action buttons shown where permitted. | High |
| 14.USEDAS-006 | Modify an existing booking when modification is permitted | An upcoming booking exists and modification is permitted by its cancellation policy | 1. On My Bookings, locate the booking row that shows an enabled Modify button and click Modify<br>2. Fill all required modification fields (for example: new travel dates, passenger details) and click Save/Confirm<br>3. Verify the booking details page and the My Bookings listing reflect the updated values | Booking is updated successfully and the changes are persisted and displayed in My Bookings. | High |
| 14.USEDAS-007 | My Bookings displays expected columns and action buttons | User is authenticated and My Bookings page is open. | 1. Observe the bookings list on the My Bookings page<br>2. Verify each booking row displays booking reference, service type, travel dates, and status<br>3. Verify action buttons are present on each row where applicable: View Details, Cancel, Modify, and Download Confirmation | Every booking row displays booking reference, service type, travel dates, status, and the described action buttons where applicable. | High |
| 14.USEDAS-008 | Download booking confirmation for a confirmed booking | User is authenticated, My Bookings page is open, and at least one booking exists with status Confirmed. | 1. Locate a booking row with status 'Confirmed' on the My Bookings page<br>2. Click the 'Download Confirmation' action for that booking row<br>3. Verify the confirmation file download is initiated or a download dialog is presented | Booking confirmation file is downloaded successfully or a download dialog is presented allowing the file to be saved. | High |
| 14.USEDAS-009 | Download invoice from My Bookings listing (triggerable for: past bookings, upcoming bookings, Hotels, Flights, Tours, Cars) | User is authenticated and My Bookings page is open with at least one booking that has an invoice available. | 1. Locate a booking row that has a downloadable invoice in the My Bookings listing<br>2. Click the "Download Invoice" action/button for that booking | Invoice file is downloaded or the invoice PDF opens for the selected booking. | High |
| 14.USEDAS-010 | Download invoice from Booking Details page | Booking detail page is open for a booking that has an invoice available. | 1. On the booking detail page, click the "Download Invoice" button | Invoice file is downloaded or the invoice PDF opens for the booking shown on the detail page. | High |
| 14.USEDAS-011 | My Bookings displays booking reference, service type, travel dates, status, and action buttons | User is authenticated and My Bookings page is open. | 1. Observe the bookings list on the My Bookings page and inspect a booking row | Each booking row shows booking reference, service type, travel dates, status (Pending, Confirmed, Cancelled), and appropriate action buttons for View Details, Cancel, and Modify where permitted. | High |
| 14.USEDAS-012 | Download voucher for a booking from My Bookings | User is logged in and My Bookings page is open with at least one booking that has a downloadable voucher | 1. Locate the booking row for a booking that has a voucher available<br>2. Click the "Download Vouchers" action for that booking<br>3. Verify the voucher file download starts or the voucher opens in a new tab/window | Voucher file is downloaded or displayed successfully. | High |
| 14.USEDAS-013 | Submit rating and review for a completed booking | User is logged in and at least one completed booking is visible in My Bookings. | 1. Locate a completed booking in the past bookings list on the My Bookings page<br>2. Click the booking's "Review" or "Write Review" action<br>3. Fill all required fields (Rating, Review text)<br>4. Click "Submit Review" | Review is saved; the rating and review text appear on the booking detail and in the user's Reviews list. | High |
| 14.USEDAS-014 | Review action visibility restricted to completed bookings | User is logged in and has both completed and upcoming bookings visible in My Bookings. | 1. Observe the action items for a completed booking and for an upcoming booking in the My Bookings list<br>2. Verify presence or absence of the "Review" / "Write Review" action for each booking | The "Review" action is present for completed bookings and is not available (or is disabled) for upcoming bookings. | High |
| 14.USEDAS-015 | Change password with valid current and matching new password | User is authenticated and Settings page is open | 1. Fill all required fields (Current password, New password, Confirm new password) with valid values<br>2. Click Save | Password update confirmation is displayed and no validation errors are shown. | High |
| 14.USEDAS-016 | Update notification preferences and save changes | User is on Settings > Notification Preferences section of the Dashboard | 1. Modify notification preference controls (enable or disable desired notification channels)<br>2. Click the "Save" (or "Update") button in the Notification Preferences section | A success confirmation is shown and the notification preference UI reflects the updated selections. | High |
| 14.USEDAS-017 | Notification preference changes persist after page refresh | User is on Settings > Notification Preferences section of the Dashboard | 1. Modify notification preference controls (enable or disable desired notification channels)<br>2. Click the "Save" (or "Update") button in the Notification Preferences section<br>3. Refresh the Settings page | Notification preferences retain the saved selections after the page refresh. | High |
| 14.USEDAS-018 | Update default currency successfully | User is authenticated and Settings page is open | 1. Select a different option from the Default Currency dropdown<br>2. Click "Save" or "Save Changes" | Default currency is updated and the change is reflected in the user's dashboard pricing display. | High |
| 14.USEDAS-019 | Default currency persists after page refresh | User is authenticated and Settings page is open | 1. Select a different option from the Default Currency dropdown<br>2. Click "Save" or "Save Changes"<br>3. Refresh the Settings page | Previously selected default currency remains selected after the page refresh. | High |
| 14.USEDAS-020 | Change display language to a different option | User is authenticated and Settings page is open. | 1. Select a different language from the Language control in Settings<br>2. Click "Save" or "Update" | Display language updates immediately and the Language control shows the newly selected language. | High |
| 14.USEDAS-021 | Logout from dashboard signs out the user and updates navigation | User is logged in and dashboard is open | 1. Open the account/user dropdown from the top navigation<br>2. Click "Logout" | User is signed out; navigation bar shows Login/Signup instead of the user's name and dashboard-specific content is no longer accessible. | High |
| 14.USEDAS-025 | Cancel button visible for bookings where cancellation is permitted | A booking exists in My Bookings for which cancellation is permitted. | 1. Locate the booking's row in My Bookings<br>2. Verify the "Cancel" action button is present for that booking | The "Cancel" button is displayed for bookings when the booking type and cancellation policy permit cancellation. | Medium |
| 14.USEDAS-026 | My Bookings lists past and upcoming bookings and allows downloading confirmations for both | User is authenticated and My Bookings page is open with both past and upcoming bookings present. | 1. Identify at least one past booking and one upcoming booking in the bookings list<br>2. Verify travel dates and status are correctly displayed for each identified booking<br>3. For each identified booking, click the 'Download Confirmation' action and verify the download is initiated | Past and upcoming bookings are listed with correct dates and statuses, and confirmations can be downloaded for both. | Medium |
| 14.USEDAS-027 | My Bookings displays expected booking fields and action buttons including download | User is logged in and My Bookings page is open with one or more bookings | 1. Inspect the bookings list<br>2. Verify each visible booking row shows booking reference, service type, travel dates, and status<br>3. Verify action buttons for a booking row include "View Details" and a "Download Vouchers" action where applicable | Bookings listing displays the listed fields and the download action is present for bookings that support it. | Medium |
| 14.USEDAS-028 | Settings page shows controls for password, notifications, currency and language | User is authenticated and Settings page is open | 1. Verify presence of controls for changing password<br>2. Verify presence of controls for notification preferences<br>3. Verify presence of controls for default currency and language | Settings displays controls for changing password, notification preferences, and default currency and language. | Medium |
| 14.USEDAS-029 | Notification preferences controls visible in Settings | User is on Settings > Notification Preferences section of the Dashboard | 1. Observe the notification preferences area<br>2. Verify notification preference controls are displayed (toggles/checkboxes or channel selectors) on the page | Notification preference controls are visible and available for interaction. | Medium |
| 14.USEDAS-030 | Change default currency and language together | User is authenticated and Settings page is open | 1. Modify the Default Currency dropdown and the Language selector to valid options<br>2. Click "Save" or "Save Changes" | Both default currency and language are saved and reflected in the user's dashboard settings. | Medium |
| 14.USEDAS-031 | Language control lists available language options | User is authenticated and Settings page is open. | 1. Click the Language control to open the language options list<br>2. Observe the available language options shown in the list | A list of available language options is displayed in the Language control. | Medium |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 14.USEDAS-022 | Cancellation action not available when booking type or policy disallow it | A booking exists in My Bookings for which cancellation is not permitted by its type or cancellation policy. | 1. Locate the booking's row in My Bookings<br>2. Verify the "Cancel" action is not present or is disabled for that booking | Cancellation action is not available for bookings whose type or cancellation policy disallow cancellation. | High |
| 14.USEDAS-023 | Attempt to submit a review for an upcoming booking | User is logged in and at least one upcoming booking is visible in My Bookings. | 1. Locate an upcoming booking in the My Bookings list and attempt to open its "Review" action<br>2. If a review form appears, fill all required fields<br>3. Click "Submit Review" | Submission is prevented and an error or informational message indicates reviews are only allowed for completed bookings. | High |
| 14.USEDAS-032 | Modify unavailable when booking type or cancellation policy prohibit modifications (applies to past bookings and cancelled bookings) | A booking exists that is not eligible for modification (past booking, cancelled booking, or a booking type governed by a non-modifiable policy) and My Bookings page is visible | 1. On My Bookings, locate a booking known to be non-modifiable (past, cancelled, or policy-prohibited)<br>2. Verify the Modify action/button is not present or is disabled, or that attempting to invoke Modify displays a blocking message | The Modify action is not available or is blocked for bookings that are not permitted to be modified. | Medium |
| 14.USEDAS-033 | Download vouchers action unavailable when booking type or policy does not permit actions | User is logged in and My Bookings page is open with at least one booking whose type or cancellation policy restricts actions | 1. Locate a booking row for which actions are restricted by type or policy<br>2. Check for the presence or enabled state of the "Download Vouchers" action for that booking | "Download Vouchers" action is not present or is disabled for bookings where actions are not permitted. | Medium |
| 14.USEDAS-034 | Submit with all required fields empty | User is logged in and a completed booking's review form is available. | 1. Click the completed booking's "Review" or "Write Review" action<br>2. Leave all required fields empty<br>3. Click "Submit Review" | Validation errors shown for all required fields. | Medium |
| 14.USEDAS-035 | Submit with all required fields empty | User is authenticated and Settings page is open | 1. Leave all required fields empty<br>2. Click Save | Validation errors shown for all required fields. | Medium |
| 14.USEDAS-036 | Change password with non-matching new password and confirmation | User is authenticated and Settings page is open | 1. Fill all other required fields, set New password and Confirm new password to different values<br>2. Click Save | Validation error indicating the new password and confirmation do not match. | Medium |
| 14.USEDAS-037 | Change password with incorrect current password | User is authenticated and Settings page is open | 1. Fill all required fields, provide an incorrect Current password and valid New password and Confirm new password<br>2. Click Save | Validation error indicating the current password is incorrect and the password is not changed. | Medium |
| 14.USEDAS-038 | Submit with all required fields empty | User is on Settings > Notification Preferences section of the Dashboard | 1. Leave all required fields empty<br>2. Click "Save" | Validation errors shown for all required required fields. | Medium |
| 14.USEDAS-039 | Submit with all required fields empty | User is authenticated and Settings page is open | 1. Leave all required fields empty<br>2. Click "Save" or "Save Changes" | Validation errors shown for all required required fields. | Medium |
| 14.USEDAS-040 | Submit with all required fields empty | User is authenticated and Settings page is open. | 1. Leave all required fields empty<br>2. Click "Save" or "Update" | Validation errors shown for all required fields. | Medium |

#### Edge Case Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 14.USEDAS-024 | After logout, attempting to access dashboard requires authentication | User is logged in and dashboard is open | 1. Open the account/user dropdown and click "Logout"<br>2. Click the "Dashboard" link or another authenticated navigation link in the header | Access is denied or the site prompts for authentication so the user must log in again. | High |
| 14.USEDAS-041 | Detail view hides Cancel and Modify when cancellation policy does not permit them | User is logged in and My Bookings contains a booking where cancellation or modification is prohibited by policy | 1. Click "View Details" for the booking that is not eligible for cancellation or modification<br>2. Verify the Cancel and Modify buttons are not present on the details view | Cancel and Modify actions are not offered for bookings when the booking type or cancellation policy does not permit them. | Medium |
| 14.USEDAS-042 | Cancelled booking details show status Cancelled and do not offer Cancel/Modify actions | User is logged in and My Bookings contains a booking with status Cancelled | 1. Click "View Details" for a booking whose status is Cancelled<br>2. Verify the details view displays the status as Cancelled and that Cancel and Modify action buttons are not available | Details view displays status as Cancelled and Cancel/Modify actions are not available for cancelled bookings. | Medium |
| 14.USEDAS-043 | Using browser Back after logout does not restore authenticated session | User is logged in and dashboard is open | 1. Open the account/user dropdown and click "Logout"<br>2. Use the browser Back action | Previously viewed dashboard content is not restored and the user remains logged out (authentication required). | Medium |
| 14.USEDAS-044 | Attempt to cancel an already cancelled booking | A booking exists in My Bookings with status "Cancelled". | 1. Locate the cancelled booking's row in My Bookings<br>2. Verify the "Cancel" action is not available for the cancelled booking | No cancellation action is available for bookings already marked as "Cancelled". | Low |
| 14.USEDAS-045 | Download voucher for a past booking | User is logged in and My Bookings page is open with at least one past booking that may have a voucher | 1. Locate a booking row categorized as a past booking<br>2. Click the "Download Vouchers" action for that past booking<br>3. Verify the voucher file download starts or the voucher opens | Voucher for the past booking is downloaded or displayed successfully. | Low |
| 14.USEDAS-046 | Save settings without changing the currently selected language | User is authenticated and Settings page is open with a language already selected. | 1. Ensure the current language is selected in the Language control<br>2. Click "Save" or "Update" | Settings save succeeds, no error is shown, and the displayed language remains unchanged. | Low |

---

### Booking Management

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 15.BOOMAN-001 | Booking detail displays all key booking information | A booking exists and its detail page is open. | 1. On the booking detail page, observe the displayed information | Confirmation number, full service information, traveler details, payment information, and current booking status are shown. | High |
| 15.BOOMAN-002 | Modify travel dates successfully when new dates are available and fees accepted | Booking exists, modification is permitted by policy, and the desired new dates are available. | 1. Click "Modify"<br>2. Fill all required fields in the modification form (new travel dates and accept applicable fees; optionally add special requests)<br>3. Click "Confirm" or "Save Changes" | Booking travel dates are updated on the detail page, applicable fee is reflected in payment information, and booking status updates accordingly. | High |
| 15.BOOMAN-003 | Add special requests to a permitted booking via Modify | A booking exists where modifications are permitted and its detail page is open. | 1. Click "Modify"<br>2. Fill special requests with a valid request description<br>3. Click "Save" or "Confirm" to apply changes | Special requests are saved and displayed on the booking detail, and a booking modification notification is sent. | High |
| 15.BOOMAN-004 | Update existing special requests via Modify | A booking exists with existing special requests and modifications permitted, and its detail page is open. | 1. Click "Modify"<br>2. Modify the special requests field to a different valid description<br>3. Click "Save" or "Confirm" | Updated special requests are displayed on the booking detail, and a booking modification notification is sent. | High |
| 15.BOOMAN-005 | Booking detail displays confirmation, service, traveler, payment, and status | A booking exists and its detail page is open. | 1. Verify the booking detail shows the confirmation number, full service information, traveler details, payment information, and current booking status | All listed booking details are visible and correctly populated. | High |
| 15.BOOMAN-006 | Update traveler information via Modify when permitted | Booking detail page is open and the Modify button is available | 1. Click "Modify"<br>2. Fill all required traveler fields with valid new details (e.g., name, document number, contact information)<br>3. Click "Save" or "Confirm Changes" | Traveler details on the booking detail view reflect the updates and the booking shows the updated traveler information. | High |
| 15.BOOMAN-007 | Booking detail displays confirmation number, traveler details, payment info, and current status | Booking detail page is open | 1. Verify confirmation number, full service information, traveler details, payment information, and current booking status are displayed on the page | All listed booking detail elements are visible and populated. | High |
| 15.BOOMAN-008 | Cancel booking and initiate refund to the original payment method | An existing booking in a cancellable status and its detail page is open. | 1. Click "Cancel" on the booking detail page<br>2. In the cancellation confirmation flow verify the applicable refund amount and that the original payment method is referenced<br>3. Explicitly confirm the cancellation | Booking status changes to "Cancelled", a refund is initiated to the original payment method, and an email notification is sent for the cancellation. | High |
| 15.BOOMAN-009 | Cancelled booking shows refund transaction referencing original payment method in payment information | An existing booking and its detail page is open. | 1. Click "Cancel" on the booking detail page<br>2. Explicitly confirm the cancellation<br>3. In the payment information section verify a refund transaction is listed referencing the original payment method | A refund transaction appears in the payment information and references the original payment method. | High |
| 15.BOOMAN-012 | Booking detail displays confirmation number, service, traveler, payment and status | An existing booking and its detail page is open. | 1. On the booking detail page verify the confirmation number is visible<br>2. Verify full service information, traveler details, payment information, and current booking status are displayed | All listed booking details (confirmation number, service info, traveler details, payment information, current booking status) are visible on the detail page. | Medium |
| 15.BOOMAN-013 | Cancellation updates booking status and available actions | An existing booking in a cancellable status and its detail page is open. | 1. Click "Cancel" on the booking detail page<br>2. Explicitly confirm the cancellation<br>3. Verify the booking's current status updates and the Cancel action is no longer available | Booking status is updated to "Cancelled" and the Cancel action is removed from available actions. | Medium |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 15.BOOMAN-010 | Attempt to change to unavailable travel dates is rejected | Booking exists and modification is permitted for the booking. | 1. Click "Modify"<br>2. Fill the modification form with new travel dates that are not available<br>3. Click "Confirm" | System displays an unavailability message and the booking travel dates remain unchanged. | High |
| 15.BOOMAN-014 | Modify blocked when booking type or cancellation policy does not permit changes | A booking exists whose booking type or cancellation policy does not permit modification. | 1. Attempt to click "Modify" or verify the "Modify" button is not visible/enabled on the detail page<br>2. If a blocking message appears, observe the message text | System prevents modification: the Modify button is not available or a clear message indicates modification is not permitted. | Medium |
| 15.BOOMAN-015 | Submit with all required fields empty | Modify form is open on the booking detail page and modification is permitted. | 1. Leave all required fields empty<br>2. Click "Confirm" or "Save Changes" | Validation errors shown for all required fields. | Medium |
| 15.BOOMAN-016 | Prevent modifying special requests when Modify is not permitted | A booking exists where modifications are not permitted and its detail page is open. | 1. Observe whether the "Modify" button is present and enabled<br>2. If an enabled "Modify" button exists, attempt to click it and change the special requests; otherwise attempt to edit special requests through the UI | The UI prevents modification (no enabled Modify button or a clear message indicating modification is not allowed) and no changes are saved. | Medium |
| 15.BOOMAN-017 | Submit with all required traveler fields empty | Modify dialog is open for the booking | 1. Leave all required traveler fields empty<br>2. Click "Save" or "Confirm Changes" | Validation errors shown for all required traveler fields. | Medium |
| 15.BOOMAN-018 | Modify action unavailable when booking type or cancellation policy disallow changes | Booking detail page is open for a booking whose type or cancellation policy does not permit modifications | 1. Verify the "Modify" button is not visible or is disabled on the booking detail page | No modification dialog can be opened and traveler information cannot be changed via Modify. | Medium |
| 15.BOOMAN-019 | Submit with all required fields empty | An existing booking and its cancellation confirmation flow is open. | 1. Leave all required fields in the cancellation confirmation flow empty<br>2. Click "Confirm Cancellation" | Validation errors shown for all required fields. | Medium |
| 15.BOOMAN-020 | Close cancellation confirmation without explicit confirmation does not process cancellation | An existing booking and its detail page is open. | 1. Click "Cancel" on the booking detail page<br>2. Close the cancellation confirmation flow without explicitly confirming | Booking status remains unchanged and no refund is initiated. | Medium |

#### Edge Case Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 15.BOOMAN-011 | Modification of traveler information triggers modification email notification | Booking detail page is open and the Modify button is available | 1. Click "Modify"<br>2. Modify one or more traveler fields with valid new details<br>3. Click "Save" or "Confirm Changes" | A modification email notification is sent for the booking change. | High |
| 15.BOOMAN-021 | Modification triggers email notification for the status change | Booking exists and modification is permitted. | 1. Click "Modify"<br>2. Fill all required fields in the modification form (new travel dates)<br>3. Click "Confirm" or "Save Changes" | Booking status changes and an email notification for the modification is sent. | Medium |
| 15.BOOMAN-022 | Cancellation when applicable refund amount is zero is processed and notifies user | A booking whose calculated refund amount is zero and its detail page is open. | 1. Click "Cancel" on the booking detail page<br>2. Verify the cancellation confirmation flow shows the applicable refund amount as zero<br>3. Explicitly confirm the cancellation | Booking status changes to "Cancelled", a refund of zero is recorded/initiated to the original payment method as applicable, and an email notification is sent for the cancellation. | Low |

---

### Payment Processing

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 16.PAYPRO-001 | Successful payment with Visa card leads to booking confirmation | User is on the payment page with the full booking summary displayed | 1. Select the Credit/Debit Card payment method and choose Visa<br>2. Fill all required card fields (cardholder name, card number, expiration date, CVV)<br>3. Click "Pay" | User is taken to a booking confirmation page with a reference number; options to download the invoice and voucher are available; a confirmation email is sent | High |
| 16.PAYPRO-002 | Successful payment with MasterCard leads to booking confirmation | User is on the payment page with the full booking summary displayed | 1. Select the Credit/Debit Card payment method and choose MasterCard<br>2. Fill all required card fields (cardholder name, card number, expiration date, CVV)<br>3. Click "Pay" | User is taken to a booking confirmation page with a reference number; options to download the invoice and voucher are available; a confirmation email is sent | High |
| 16.PAYPRO-003 | Successful payment with American Express leads to booking confirmation | User is on the payment page with the full booking summary displayed | 1. Select the Credit/Debit Card payment method and choose American Express<br>2. Fill all required card fields (cardholder name, card number, expiration date, CVV)<br>3. Click "Pay" | User is taken to a booking confirmation page with a reference number; options to download the invoice and voucher are available; a confirmation email is sent | High |
| 16.PAYPRO-004 | Payment page displays booking summary and security indicators | User is on the payment page | 1. Observe the booking summary area<br>2. Verify the price breakdown shows base price, taxes, service fees, applicable discounts, and total<br>3. Verify security badges and SSL encryption indicators are visible on the page | Full booking summary with base price, taxes, service fees, applicable discounts, and total is displayed and security badges/SSL indicators are visible | High |
| 16.PAYPRO-005 | Payment page displays booking summary with price breakdown and security indicators | User is on the payment page with a prepared booking | 1. Verify full booking summary and price breakdown (base price, taxes, service fees, applicable discounts, total) is visible on the payment page<br>2. Verify security badges and SSL encryption indicators are displayed on the payment page | Booking summary and price breakdown are displayed and security indicators are visible. | High |
| 16.PAYPRO-006 | Complete booking using PayPal and reach confirmation with reference, downloads, and email | User is on the payment page with a prepared booking | 1. Click "Pay with PayPal" and complete the PayPal authorization<br>2. On return to the site, verify the booking confirmation page shows a reference number and options to download the invoice and voucher | User is taken to a booking confirmation page with a reference number; invoice and voucher download options are available and a confirmation email is sent. | High |
| 16.PAYPRO-007 | Payment page shows full booking summary, price breakdown, and security indicators | None | 1. Select the "Bank Transfer" payment method on the payment page<br>2. Observe the booking summary area and verify it displays base price, taxes, service fees, applicable discounts, and total<br>3. Observe that security badges and SSL encryption indicators are displayed on the page | The payment page shows a complete price breakdown (base price, taxes, service fees, discounts, total) and visible security badges/SSL indicators. | High |
| 16.PAYPRO-008 | Complete booking using Bank Transfer and receive booking confirmation | Valid booking is in the payment page with user's email available | 1. Select the "Bank Transfer" payment method<br>2. Follow the bank transfer instructions or upload transfer receipt and click the page's action to submit transfer details<br>3. Confirm submission and observe the resulting page | User is taken to a booking confirmation page with a reference number; options to download the invoice or voucher are available and a confirmation email is sent. | High |
| 16.PAYPRO-009 | Pay with Wallet/Credits succeeds when wallet balance covers total | User is authenticated and payment page is open; wallet balance is sufficient to cover the booking total. | 1. Select "Wallet/Credits" as the payment method and choose to apply wallet/credits for the payment<br>2. Confirm the amount to use from wallet/credits if prompted<br>3. Click the primary "Pay" / "Confirm Payment" button | User is taken to the booking confirmation page with a reference number; options to download the invoice and voucher are available and a confirmation email is sent. | High |
| 16.PAYPRO-010 | Payment page displays full booking summary with price breakdown | Payment page is open for a prepared booking. | 1. Observe the booking summary area<br>2. Verify the price breakdown shows base price, taxes, service fees, applicable discounts, and total | Full booking summary and complete price breakdown (base price, taxes, service fees, applicable discounts, total) are displayed. | High |
| 16.PAYPRO-011 | Retry payment succeeds and displays booking confirmation with downloads and email | Payment attempt has failed and the payment page shows the error message. | 1. Confirm the page displays a full booking summary with a price breakdown (base price, taxes, service fees, applicable discounts, total)<br>2. Click "Retry Payment"<br>3. Fill valid payment details and click "Pay" | User is taken to a booking confirmation page with a reference number; options to download the invoice or voucher are available and a confirmation email is sent. | High |
| 16.PAYPRO-012 | Payment page shows full booking summary with price breakdown | User is on the payment page. | 1. Confirm the booking summary section is visible on the page<br>2. Verify the price breakdown displays base price, taxes, service fees, applicable discounts, and total | The page displays a full booking summary with a price breakdown including base price, taxes, service fees, applicable discounts, and total. | High |
| 16.PAYPRO-024 | Pay and save card for future use completes booking | User is on the payment page with the full booking summary displayed and is signed in | 1. Select the Credit/Debit Card payment method<br>2. Fill all required card fields (cardholder name, card number, expiration date, CVV) and enable the option to save the card for future use<br>3. Click "Pay" | Booking confirmation page is displayed with a reference number and download options available; payment completes successfully | Medium |
| 16.PAYPRO-025 | Download invoice and voucher are available on the confirmation page | User is on the booking confirmation page after a successful payment | 1. Observe the confirmation page actions<br>2. Click the link/button to download the invoice<br>3. Click the link/button to download the voucher | Invoice and voucher download actions are available and initiate the respective downloads | Medium |
| 16.PAYPRO-026 | Download invoice and voucher from booking confirmation page | Booking confirmation page is open | 1. Click "Download Invoice"<br>2. Click "Download Voucher" | Invoice and voucher downloads are initiated. | Medium |
| 16.PAYPRO-027 | Download invoice and voucher from booking confirmation | Booking confirmation page is open for a completed booking | 1. Click the "Download Invoice" action on the booking confirmation page<br>2. Click the "Download Voucher" action on the booking confirmation page | Invoice and voucher downloads are initiated or files are downloaded/available for the user. | Medium |
| 16.PAYPRO-028 | Security badges and SSL encryption indicators are visible on payment page | Payment page is open. | 1. Inspect the payment page header/footer and payment sections<br>2. Verify security badges and SSL encryption indicators are present and visible | Security badges and SSL encryption indicators are displayed on the payment page. | Medium |
| 16.PAYPRO-029 | Download invoice and voucher from booking confirmation after wallet payment | User is on the booking confirmation page after a successful payment. | 1. Click the "Download Invoice" control on the confirmation page<br>2. Click the "Download Voucher" control on the confirmation page | Invoice and voucher download actions are triggered (files downloadable) and download links are available on the confirmation page. | Medium |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 16.PAYPRO-013 | Payment failure shows descriptive error for card decline | User is on the payment page with the card payment form visible | 1. Fill all required card fields with a card that results in a declined payment response<br>2. Click "Pay" | An error message describing the issue (e.g., "Card declined") is displayed and the booking details remain available for retry | High |
| 16.PAYPRO-014 | Payment failure shows descriptive error for insufficient funds | User is on the payment page with the card payment form visible | 1. Fill all required card fields with a card that results in an insufficient funds response<br>2. Click "Pay" | An error message describing the issue (e.g., "Insufficient funds") is displayed and the booking details remain available for retry | High |
| 16.PAYPRO-015 | Payment failure displays descriptive error message (Card declined) and allows retry | User is on the payment page with a prepared booking | 1. Click "Pay with PayPal" and complete PayPal authorization that results in a denial reflecting a card-related decline<br>2. Verify the payment page displays a descriptive error message and the booking details remain visible | A descriptive error message is shown and the user can retry without losing booking details. | High |
| 16.PAYPRO-016 | Payment failure displays descriptive error message (Insufficient funds) and allows retry | User is on the payment page with a prepared booking | 1. Click "Pay with PayPal" and complete PayPal authorization that results in an insufficient-funds outcome<br>2. Verify the payment page displays a descriptive error message and the booking details remain visible | A descriptive error message is shown and the user can retry without losing booking details. | High |
| 16.PAYPRO-017 | Retry after payment failure preserves booking details and allows reattempt | User experienced a payment failure and is on the payment page | 1. Observe the error message after the failed payment attempt<br>2. Verify the full booking summary and price breakdown remain displayed and unchanged<br>3. Click "Pay with PayPal" to attempt payment again | User can retry payment and booking details remain intact. | High |
| 16.PAYPRO-018 | Bank Transfer payment failure shows descriptive error and allows retry without losing booking details | Booking payment is ready and Bank Transfer is selected | 1. Submit Bank Transfer details that simulate or return a failed payment state<br>2. Observe the error message shown and use the retry action on the payment page<br>3. Verify the booking summary and price breakdown remain visible and unchanged after the failure | A descriptive error message is shown (e.g., 'Card declined', 'Insufficient funds') and the user can retry without losing their booking details. | High |
| 16.PAYPRO-019 | Attempt wallet payment with insufficient wallet balance shows error and allows retry | User is authenticated and payment page is open; wallet balance is less than the booking total. | 1. Select "Wallet/Credits" as the payment method and apply wallet/credits to cover the total<br>2. Click the primary "Pay" / "Confirm Payment" button and observe the response | Payment fails with an error message describing the issue (e.g., insufficient funds) and the user is offered options to retry or choose an alternative payment without losing booking details. | High |
| 16.PAYPRO-020 | After a failed wallet payment, user can retry with an alternative payment without losing booking details | Payment page is open and a prior wallet payment attempt has failed and returned to the payment page. | 1. Observe that booking summary and previously entered booking details remain displayed<br>2. Select an alternative supported payment method and fill required fields for that method, then click the primary "Pay" / "Confirm Payment" button | Alternative payment can be submitted successfully and booking details were retained after the failed wallet attempt. | High |
| 16.PAYPRO-021 | Retry payment fails and displays descriptive error message | Payment attempt has failed and the payment page shows the error message. | 1. Confirm the booking summary is visible<br>2. Click "Retry Payment"<br>3. Fill payment details that will be declined and click "Pay" | An error message describing the issue is shown (for example, card declined or insufficient funds) and the booking details remain visible so the user can attempt payment again. | High |
| 16.PAYPRO-022 | Failed retry preserves booking details for subsequent attempts | Payment attempt has failed and the payment page shows the error message. | 1. Confirm the booking summary and price breakdown are visible<br>2. Click "Retry Payment", submit payment details that fail, and observe the error<br>3. Verify the booking summary and all pricing details remain displayed after the failure | Booking details are retained on the payment page and the user can retry payment without losing their booking details. | High |
| 16.PAYPRO-030 | Submit with all required fields empty | User is on the payment page with the card payment form visible | 1. Leave all required fields empty<br>2. Click "Pay" | Validation errors shown for all required card fields. | Medium |
| 16.PAYPRO-031 | Submit with all required fields empty | User is on the payment page | 1. Leave all required fields empty<br>2. Click "Pay with PayPal" | Validation errors shown for all required fields. | Medium |
| 16.PAYPRO-032 | Submit with all required fields empty | None | 1. Leave all required fields related to Bank Transfer empty<br>2. Click the payment page's "Submit" or "Confirm Payment" action | Validation errors are shown for all required fields and submission is prevented. | Medium |
| 16.PAYPRO-033 | Submit with all required fields empty | Payment page is open. | 1. Leave all required payment fields and options empty or unselected<br>2. Click the primary "Pay" / "Confirm Payment" button | Validation errors shown for all required fields and payment is not processed. | Medium |

#### Edge Case Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 16.PAYPRO-023 | After a failed card payment the user can retry without losing booking details | User is on the payment page with the full booking summary displayed | 1. Fill card fields with a card that causes payment to fail and click "Pay"<br>2. After the error appears, verify the booking summary and price breakdown remain visible, then fill card fields with a valid card and click "Pay" | User is able to retry payment and proceed to booking confirmation without losing booking details | High |
| 16.PAYPRO-034 | Bank Transfer confirmation occurs only after reconciliation | Bank Transfer payment details submitted on the payment page | 1. Submit Bank Transfer transfer details or indicate payment has been made<br>2. Observe the immediate page response and status message on the payment page indicating next steps | The booking is not immediately shown as confirmed on the site; final booking confirmation occurs only after reconciliation as part of the successful Bank Transfer flow. | Medium |
| 16.PAYPRO-035 | Wallet balance equal to booking total processes successfully (boundary) | User is authenticated and payment page is open; wallet balance equals the booking total exactly. | 1. Select "Wallet/Credits" as the payment method and apply wallet/credits for the full amount<br>2. Click the primary "Pay" / "Confirm Payment" button | Payment succeeds and the user is taken to the booking confirmation page with a reference number. | Medium |
| 16.PAYPRO-036 | Wallet balance slightly below total triggers insufficient funds error (boundary) | User is authenticated and payment page is open; wallet balance is just below the booking total. | 1. Select "Wallet/Credits" as the payment method and attempt to apply wallet/credits for the total<br>2. Click the primary "Pay" / "Confirm Payment" button | Payment fails with an error indicating insufficient funds and the user can retry or choose another payment method without losing booking details. | Medium |
| 16.PAYPRO-037 | Consecutive retries: initial failure followed by successful payment resulting in confirmation | Payment attempt has failed and the payment page shows the error message. | 1. Click "Retry Payment", submit payment details that fail and observe the error<br>2. Click "Retry Payment" again, submit valid payment details and click "Pay" | After the final successful payment the user is taken to a booking confirmation page with a reference number and download options; intermediate failures displayed their respective error messages. | Medium |

---

### Currency & Language Selection

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 17.C&LS-001 | Change currency updates displayed prices in real-time and preserves search context | User has an active search context (search results or filters applied) on the current page. | 1. Click the Currency selector in the top navigation and choose a different currency<br>2. Observe all visible price elements on the current page | All displayed prices update to the selected currency in real-time and the current search context (filters, selected item) remains unchanged. | High |
| 17.C&LS-002 | Authenticated user's selected currency persists across page reload | User is authenticated and on a page with the Currency selector visible. | 1. Click the Currency selector and choose a different currency<br>2. Refresh the current page | The selected currency remains active after reload and displayed prices continue to show the selected currency (preference saved to profile). | High |
| 17.C&LS-003 | Unauthenticated user's selected currency persists across page reload within session | User is unauthenticated (guest) and on a page with the Currency selector visible. | 1. Click the Currency selector and choose a different currency<br>2. Refresh the current page | The selected currency remains active after reload during the browsing session and displayed prices continue to show the selected currency (preference stored in session/cookies for the session). | High |
| 17.C&LS-004 | Authenticated user's currency and language preferences persist after reload | User is authenticated and on a page with both Currency and Language selectors visible. | 1. Select a different currency from the Currency selector and select a different language from the Language selector<br>2. Refresh the current page | Both the selected currency and language remain active after reload and displayed content and prices reflect the chosen preferences (preferences saved to profile). | High |
| 17.C&LS-005 | Switch site interface to English via language selector | None | 1. Select English from the Language selector | Navigation labels, form labels, and page content switch to English. | High |
| 17.C&LS-006 | Switch site interface to Spanish via language selector | None | 1. Select Spanish from the Language selector | Navigation labels, form labels, and page content switch to Spanish. | High |
| 17.C&LS-007 | Switch site interface to French via language selector | None | 1. Select French from the Language selector | Navigation labels, form labels, and page content switch to French. | High |
| 17.C&LS-008 | Switch site interface to Arabic via language selector | None | 1. Select Arabic from the Language selector | Navigation labels, form labels, and page content switch to Arabic. | High |
| 17.C&LS-009 | Authenticated user's language preference is saved to profile | User is authenticated | 1. Select a language from the Language selector<br>2. Open the user account dropdown and view the profile or preferences summary | Selected language appears in the user's profile/preferences indicating it was saved to the profile. | High |
| 17.C&LS-011 | Unauthenticated user's language preference stored in session/cookies and persists during session | User is not authenticated | 1. Select a language from the Language selector<br>2. Refresh the page<br>3. Inspect session/cookies for a language preference value | Site remains in the chosen language after refresh and a session/cookie contains the chosen language preference. | Medium |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 17.C&LS-012 | Unauthenticated currency preference cleared when session cookies are removed | User is unauthenticated (guest) and on a page with the Currency selector visible. | 1. Click the Currency selector and choose a different currency<br>2. Clear the site's session/cookies for the browser and refresh the current page | The site no longer retains the previously selected currency and displayed prices revert to the default currency. | Medium |
| 17.C&LS-013 | Language selector must switch entire interface — negative case when content remains untranslated | None | 1. Select a language from the Language selector<br>2. Observe whether navigation labels and form labels update while main page content remains in the prior language | If main page content remains in the prior language while navigation or forms changed, the behavior is incorrect (partial translation). | Medium |
| 17.C&LS-014 | Authenticated user's selected language is not saved to profile (negative verification) | User is authenticated | 1. Select a language from the Language selector<br>2. Open the user account dropdown and view the profile or preferences summary | Selected language does not appear in the user's profile/preferences indicating the profile save failed. | Medium |

#### Edge Case Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 17.C&LS-010 | All visible price elements update in real-time when currency is changed (results, summary, banners) | User is on a page where multiple price elements are visible (search results list, booking summary, promotional banners). | 1. Click the Currency selector and choose a different currency<br>2. Observe each price element on the current page for immediate update to the chosen currency without refreshing | Every visible price element on the page updates to the selected currency in real-time with no loss of other page state. | High |
| 17.C&LS-015 | Currency change preserves complex search context (filters and selected item) | User has a complex search context (multiple filters applied and a result item selected/expanded) on the current page. | 1. Click the Currency selector and choose a different currency<br>2. Verify that filters, selected/expanded item, and other search state remain as before while observing price displays | The search context remains unchanged and all displayed prices update to the chosen currency in real-time. | Medium |
| 17.C&LS-016 | Unauthenticated language preference does not persist after session end | User is not authenticated | 1. Select a language from the Language selector<br>2. Clear session and cookies for the site and refresh the page | Site interface reverts to the default language; unauthenticated preference is not retained across sessions. | Medium |

---

### Search & Filters

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 18.S&F-001 | Apply a single filter updates results, count, and shows active filter | Search results page with initial results visible | 1. Select a single filter in the left sidebar (for example: star rating, facility, or hotel type)<br>2. Observe the results grid and result count | Results grid updates dynamically to show only items matching the selected filter; result count updates and the selected filter appears in the active filters summary with an individual remove button. | High |
| 18.S&F-002 | Apply multiple filters across collapsible sections updates results and summary | Search results page with initial results visible | 1. Open relevant collapsible filter sections as needed<br>2. Select multiple filters across different sections (e.g., location, amenities, board basis) in the left sidebar | Results grid and result count update dynamically to reflect the combined filters; all selected filters appear in the active filters summary at the top. | High |
| 18.S&F-003 | Adjust price range slider updates results and shows price filter in summary | Search results page with initial results visible and price range slider present | 1. Move the price range slider to narrow the allowed price span<br>2. Observe the results grid and active filters summary | Results grid updates dynamically to include only items within the selected price range; result count updates and a price-range entry appears in the active filters summary. | High |
| 18.S&F-004 | Remove an individual active filter updates results and count | Search results page with at least one active filter shown in the active filters summary | 1. Click the individual remove button for one active filter in the active filters summary | The removed filter disappears from the active filters summary and the results grid and result count update dynamically to reflect the remaining active filters. | High |
| 18.S&F-005 | Reset all filters clears filters and returns results to unfiltered state | Search results page with multiple active filters applied | 1. Click the "Reset all filters" control | All active filters are cleared from the summary, the results grid updates dynamically to the unfiltered result set, and the result count updates accordingly. | High |
| 18.S&F-006 | Remove a single active filter updates results and result count | Search results are displayed with at least one active filter | 1. Click the individual remove button for a specific active filter in the active-filters summary<br>2. Wait for the results grid and result count to refresh | The removed filter is no longer shown in the active filters summary, the results grid refreshes to reflect the change, and the result count updates accordingly. | High |
| 18.S&F-007 | Remove one filter among multiple active filters retains other active filters and updates results | Search results are displayed with multiple active filters | 1. Click the individual remove button for one specific active filter in the active-filters summary<br>2. Wait for the results grid and result count to refresh | Only the selected filter is removed from the summary, other active filters remain, and the results grid and result count update to reflect the change. | High |
| 18.S&F-008 | Remove the last active filter clears the active-filters summary and refreshes unfiltered results | Search results are displayed with a single active filter | 1. Click the individual remove button for the active filter in the active-filters summary<br>2. Wait for the results grid and result count to refresh | The active filters summary is no longer displayed, the results refresh to the unfiltered set, and the result count updates accordingly. | High |
| 18.S&F-009 | Reset all filters clears applied filters and restores unfiltered listing | Search results have multiple active filters | 1. Apply multiple filters (price range slider, star rating, facilities/amenities, location/area)<br>2. Click Reset all filters control | All active filters are cleared, active filters summary is empty, and the results grid and result count reflect the unfiltered listing. | High |
| 18.S&F-011 | Change sorting while a filter is active retains filter and updates ordering | Search results page with initial results visible | 1. Apply a filter from the left sidebar<br>2. Change the sorting control to a different sort option | Result ordering updates according to the selected sorting option while the active filter remains applied and the result count remains consistent with the active filter set. | Medium |
| 18.S&F-012 | Active filters summary displays each active filter with individual remove buttons | Search results page with at least one filter applied | 1. Apply multiple filters from the left sidebar<br>2. View the active filters summary at the top | Each active filter is summarized at the top and shows an individual remove button for that filter. | Medium |
| 18.S&F-013 | Reset control is visible and enabled when filters can be applied | Search results listing is displayed | 1. Inspect the filter area and active filters summary<br>2. Confirm Reset all filters control is visible and enabled | Reset all filters control is displayed and enabled when filters are available. | Medium |
| 18.S&F-014 | Reset restores filter widgets to default states | Search results have modified widget filters | 1. Adjust widget filters (move price range slider, select star/review ratings, check facility/amenity boxes, select hotel type or board basis)<br>2. Click Reset all filters control | All widget controls return to their default/unselected states and the results and result count update to the unfiltered state. | Medium |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 18.S&F-015 | Attempting to remove a non-active filter is not possible (no remove button present) | Search results are displayed and the specific filter to be tested is not currently active | 1. Inspect the active-filters summary for the specific filter<br>2. Attempt to interact with an individual remove button for that non-active filter in the active-filters summary | No individual remove button is present for the non-active filter and no changes occur to filters, results, or result count. | Medium |

#### Edge Case Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 18.S&F-010 | Reset updates the result count accordingly after clearing filters | Search results have filters applied such that the result count differs from the unfiltered listing | 1. Apply filters that change the result count (e.g., price range, stop counts, departure date)<br>2. Click Reset all filters control | Result count updates to reflect the unfiltered listing and the results update dynamically after reset. | High |
| 18.S&F-016 | Apply combination of filters that yields no matching results shows zero count and empty results | Search results page with initial results visible | 1. Apply a combination of filters that are unlikely to match any item (across multiple filter sections)<br>2. Observe the results grid and result count | Results grid shows no items and the result count displays zero; the active filters remain summarized at the top. | Medium |
| 18.S&F-017 | Removing a restrictive filter from a zero-results search refreshes results and updates count | Search results display zero results with one or more active filters | 1. Click the individual remove button for a restrictive active filter in the active-filters summary<br>2. Wait for the results grid and result count to refresh | Results update dynamically after the filter is removed and the result count updates accordingly, potentially showing additional results. | Low |
| 18.S&F-018 | Click Reset when no filters are active produces no change and no errors | Search results listing with no filters active | 1. Ensure no filters are active and the active filters summary is empty<br>2. Click Reset all filters control | No change occurs to the results or UI and no error is shown; Reset control remains available. | Low |

---

### Reviews & Ratings

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 19.R&R-001 | Submit a review through the dashboard (without photos) | Authenticated user with a completed booking and dashboard open. | 1. Fill all required fields in the dashboard review form (overall star rating, category-specific ratings, stay date, written feedback)<br>2. Click "Submit" | Review is submitted and success confirmation is shown; the review appears in the item's Reviews section showing overall rating, category-specific ratings, reviewer name and country, review date, stay date, and written comments; the listing's aggregate rating score and total review count reflect the new review. | High |
| 19.R&R-002 | Submit a review through the dashboard including guest-uploaded photos | Authenticated user with a completed booking and dashboard open. | 1. Fill all required fields in the dashboard review form (overall star rating, category-specific ratings, stay date, written feedback) and attach one or more guest photos<br>2. Click "Submit" | Review is submitted and success confirmation is shown; the review appears in the item's Reviews section including the guest-uploaded photos alongside overall rating, category-specific ratings, reviewer name and country, review date, stay date, and written comments; listing aggregate rating and total review count update accordingly. | High |
| 19.R&R-003 | Listing shows aggregate rating score and total review count for the item | Listing page open and the item is visible in the results. | 1. Locate the item's listing entry on the listing page<br>2. Inspect the aggregate rating and review count elements for that item | The listing entry displays an aggregate rating score and a total review count for the item. | High |
| 19.R&R-004 | Submit review via post-stay email prompt (authenticated completed booking) | User is authenticated, has a completed booking, and is on the post-stay review submission page. | 1. Fill all required fields (Overall rating, category-specific ratings, written feedback) and optionally attach photos<br>2. Click "Submit" | Review is saved and a submission confirmation is shown; the review will appear in the item's Reviews section and contribute to the aggregate rating and total review count. | High |
| 19.R&R-005 | Submitted review displays on detail page with ratings, reviewer info, dates, comments, and photos | A review was submitted for the item and the item's detail page is open. | 1. Open the Reviews section on the item detail page<br>2. Locate the submitted review and inspect displayed fields (overall rating, category-specific ratings, reviewer name and country, review date, stay date, written comments, guest-uploaded photos) | Individual review shows overall rating, each category rating, reviewer name and country, review date, stay date, written comments, and any guest-uploaded photos. | High |
| 19.R&R-006 | Listing page reflects updated aggregate rating and total review count after review submission | A new review was submitted for the item. | 1. View the item's listing card or row<br>2. Inspect the displayed aggregate rating score and total review count for the item | The aggregate rating score and total review count reflect the newly submitted review. | High |
| 19.R&R-007 | Filter reviews by overall rating | Detail page Reviews section is visible and contains reviews with varying overall ratings | 1. Select a desired overall rating in the 'Filter by rating' control<br>2. Click the 'Apply Filters' button | Only individual reviews with the selected overall rating are displayed; each visible review shows its overall rating and reviewer details. | High |
| 19.R&R-008 | Filter reviews by review date range | Detail page Reviews section is visible and contains reviews with differing review dates | 1. Set a start and end date in the 'Filter by date' controls<br>2. Click the 'Apply Filters' button | Only individual reviews whose review date falls within the selected date range are displayed; each visible review shows its review date and stay date. | High |
| 19.R&R-009 | Filter reviews by traveler type | Detail page Reviews section is visible and contains reviews from multiple traveler types | 1. Select a traveler type in the 'Filter by traveler type' control<br>2. Click the 'Apply Filters' button | Only individual reviews matching the selected traveler type are displayed; reviewer country and other review details remain visible for each result. | High |
| 19.R&R-010 | Apply multiple filters together (rating, date, traveler type) | Detail page Reviews section is visible and contains reviews that vary by rating, date, and traveler type | 1. Select a rating, set a date range, and choose a traveler type in the respective filter controls<br>2. Click the 'Apply Filters' button | Only individual reviews that satisfy all selected filter criteria are displayed. | High |
| 19.R&R-013 | Reviews section displays individual review details on the item detail page | Item detail page with at least one review open. | 1. Click the "Reviews" tab or scroll to the Reviews section<br>2. Locate an individual review entry | The individual review entry displays overall rating, category-specific ratings (e.g., Cleanliness, Service, Location), reviewer name and country, review date, stay date, written comments, and any guest-uploaded photos. | Medium |
| 19.R&R-014 | Include guest-uploaded photos when submitting a review via post-stay email prompt | User is authenticated, has a completed booking, and is on the post-stay review submission page. | 1. Attach one or more photos using the review photo upload control<br>2. Fill all other required fields (Overall rating, category-specific ratings, written feedback)<br>3. Click "Submit" | Review is saved and the guest-uploaded photos appear with the review on the detail page. | Medium |
| 19.R&R-015 | Individual review displays expected fields | Detail page Reviews section is visible with at least one individual review | 1. Inspect an individual review in the Reviews section | The review displays overall rating, category-specific ratings, reviewer name and country, review date, stay date, written comments, and any guest-uploaded photos. | Medium |
| 19.R&R-016 | Reviews section is present on detail page | Detail page is open | 1. Locate the Reviews section on the detail page | Detail page includes a dedicated Reviews section. | Medium |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 19.R&R-011 | Attempt to submit a review without having completed a booking | Authenticated user without a completed booking and dashboard open. | 1. Fill all required fields in the dashboard review form (overall star rating, category-specific ratings, stay date, written feedback)<br>2. Click "Submit" | Submission is rejected and an error or notice indicates the user is not allowed to submit a review because they have not completed a booking. | High |
| 19.R&R-012 | Attempt to submit review via post-stay link while unauthenticated | User is not authenticated and is on the post-stay review submission page. | 1. Fill all required fields on the review form<br>2. Click "Submit" | Submission is blocked and the user is prompted to sign in or shown an authentication-required error; the review is not accepted. | High |
| 19.R&R-017 | Submit with all required fields empty | Authenticated user with a completed booking and dashboard open. | 1. Leave all required fields in the dashboard review form empty<br>2. Click "Submit" | Validation errors are shown for all required review fields. | Medium |
| 19.R&R-018 | Submit with all required fields empty | User is authenticated, has a completed booking, and is on the post-stay review submission page. | 1. Leave all required fields empty<br>2. Click "Submit" | Validation errors shown for all required fields. | Medium |
| 19.R&R-019 | Apply filters with all filter fields empty | Detail page Reviews section is visible | 1. Leave all filter fields empty<br>2. Click the 'Apply Filters' button | Validation errors shown for all required filter fields or no filtering is applied. | Medium |

#### Edge Case Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 19.R&R-020 | Apply filters that match no reviews | Detail page Reviews section is visible | 1. Set filter criteria that do not match any existing reviews (e.g., combination of rating, date range, and traveler type)<br>2. Click the 'Apply Filters' button | No individual reviews are displayed and a 'no reviews found' or equivalent message is shown. | Low |

---

### Offers & Deals

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 20.O&D-001 | Filter offers by service type, destination, and travel dates | Offers page is open | 1. Select a service type (Hotels, Flights, Packages)<br>2. Enter a destination<br>3. Select travel start and end dates<br>4. Click the filter/apply button | Promotional banners and featured deal cards update to reflect the selected service type, destination, and travel dates. | High |
| 20.O&D-002 | Featured deal cards display required elements | Offers page is open with at least one featured deal | 1. Inspect a featured deal card | Deal card shows deal title, image, discount percentage or special rate, validity period, a Terms and Conditions link, and a Book Now button. | High |
| 20.O&D-003 | Subscribe to newsletter with a valid email | None | 1. Fill the newsletter subscription field with a valid email address<br>2. Click the newsletter subscription submit button | Subscription success confirmation is displayed indicating the user will receive future exclusive deals. | High |
| 20.O&D-004 | Apply promotional code via Book Now (triggerable from: featured card, banner) | Offers page is open with at least one active promotional offer. | 1. Click any Book Now entry point for an active offer (featured deal card or promotional banner)<br>2. Fill all required booking fields<br>3. Click Confirm Booking | The promotional code is applied and the discounted rate is reflected in the booking total. | High |
| 20.O&D-005 | Redirect to pre-filled search with discounted rates via Book Now (triggerable from: featured card, banner) | Offers page is open with at least one active promotional offer that redirects to search. | 1. Click Book Now on an offer that redirects to a search<br>2. On the search form, verify destination and travel dates are pre-filled from the offer<br>3. Select a search result, fill all required booking fields, and click Confirm Booking | User is redirected to a pre-filled search and the discounted rates are shown and applied to the booking. | High |
| 20.O&D-006 | Last-minute offers and seasonal packages are listed alongside standard promotions | Offers page is open | 1. Scan the offers listings area for sections or labels related to last-minute offers and seasonal packages | Last-minute offers and seasonal packages appear in the listings alongside standard promotions. | Medium |
| 20.O&D-007 | Filter offers by service type only | Offers page is open | 1. Select a service type (Hotels, Flights, Packages) and leave destination and travel dates empty<br>2. Click the filter/apply button | Displayed promotional banners and deal cards update to reflect the selected service type. | Medium |
| 20.O&D-008 | Offers page displays promotional banners and featured deal cards with required elements | Offers page is open with at least one featured deal displayed. | 1. On the Offers page, verify promotional banners and featured deal cards are visible<br>2. For a featured deal card, verify it shows deal title, image, discount or special rate, validity period, Terms and Conditions link, and a Book Now button | Offers page displays promotional banners and featured deal cards with the required elements. | Medium |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 20.O&D-009 | Submit with all required fields empty | Offers page is open | 1. Leave all required filter fields empty<br>2. Click the filter/apply button | Validation errors shown for all required fields. | Medium |
| 20.O&D-010 | Submit with all required fields empty | None | 1. Leave all required fields empty<br>2. Click the newsletter subscription submit button | Validation error shown for the email field indicating it is required. | Medium |
| 20.O&D-011 | Submit with invalid email format in newsletter field | None | 1. Fill the newsletter subscription field with an invalid email format<br>2. Click the newsletter subscription submit button | Validation error shown indicating the email format is invalid. | Medium |
| 20.O&D-012 | Book Now does not apply promotional code to booking flow | Offers page is open with at least one active promotional offer. | 1. Click Book Now for an active offer<br>2. Fill all required booking fields<br>3. Click Confirm Booking | Promotional code is not applied and booking total does not reflect the discounted rate. | Medium |
| 20.O&D-013 | Book Now does not redirect to a pre-filled search with discounted rates | Offers page is open with at least one active promotional offer that normally redirects to search. | 1. Click Book Now on an offer that is expected to redirect<br>2. Observe the search form and results after the click | User is not redirected to a pre-filled search and discounted rates are not applied or visible. | Medium |

#### Edge Case Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 20.O&D-014 | Apply filters that return no matching offers | Offers page is open | 1. Select a service type and destination and travel dates that do not match any active offers<br>2. Click the filter/apply button | UI indicates no offers are available for the selected criteria and the offers listing is empty or shows a no-results message. | Medium |

---

### Logout

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 21.LOGOUT-001 | Logout terminates session, clears sensitive session data, and redirects to home | User is authenticated and account dropdown is visible | 1. Open the account dropdown and click "Logout"<br>2. Verify the application redirects to the home page and the account menu shows unauthenticated options (e.g., Login/Signup) | User session is terminated, sensitive session-related UI is cleared and replaced by unauthenticated options, and the home page is displayed. | High |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 21.LOGOUT-002 | Attempt to access a protected page after logout redirects to the login page | User is authenticated and a protected page is accessible | 1. Open the account dropdown and click "Logout"<br>2. Attempt to access a protected page (for example, by entering its URL or clicking its protected link) | The application redirects to the login page and does not display the protected content. | High |
| 21.LOGOUT-003 | Logout clears client-side sensitive session data (cookies/storage) after sign out | User is authenticated and account dropdown is visible | 1. Open the account dropdown and click "Logout"<br>2. Inspect client-side session storage and authentication cookies for presence of user-specific tokens or sensitive session values | No user tokens or sensitive session values remain in cookies or client-side storage after logout. | Medium |

#### Edge Case Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 21.LOGOUT-004 | Browser Back after logout does not restore protected content and redirects to login | User is authenticated and currently viewing a protected page | 1. Open the account dropdown and click "Logout"<br>2. Use the browser Back button to attempt to return to the previously viewed protected page<br>3. Observe the page displayed after navigating back | Back navigation does not restore authenticated protected content; the user is redirected to the login page instead. | Low |

---

## Navigation Graph

![Navigation Graph](Output/PHPTravels/navigation_graph.png)

### Pages

| Module | URL | Test Cases |
|--------|-----|------------|
| Home Page & Search | / | 16 |
| User Registration | /register | 6 |
| User Login | /login | 16 |
| Forgot Password | /forgot-password | 6 |
| Hotels Search & Listing | /hotels | 21 |
| Hotel Details & Booking | /hotels/{id} | 0 |
| Flights Search & Listing | /flights | 5 |
| Flight Booking | /flights/{id}/book | 7 |
| Tours Search & Listing | /tours | 33 |
| Tour Details & Booking | /tours/{id}/book | 10 |
| Cars Search & Listing | /cars | 8 |
| Car Booking | /cars/{id}/book | 8 |
| Visa Services | /visa | 10 |
| User Dashboard | /dashboard | 46 |
| Booking Management | /account/bookings | 22 |
| Payment Processing | /checkout | 37 |
| Currency & Language Selection | /settings/locale | 16 |
| Search & Filters | /search | 18 |
| Reviews & Ratings | /reviews | 20 |
| Offers & Deals | /offers | 14 |
| Logout | /logout | 4 |
