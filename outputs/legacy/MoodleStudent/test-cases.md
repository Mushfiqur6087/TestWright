# Moodlestudent

**Base URL:** 
**Generated:** 2026-04-27T04:49:19.239771

## Summary

| Metric | Count |
|--------|-------|
| **Total Tests** | 127 |

### By Type

| Type | Count |
|------|-------|
| Positive | 91 |
| Negative | 21 |
| Edge Case | 15 |

### By Priority

| Priority | Count |
|----------|-------|
| High | 75 |
| Medium | 42 |
| Low | 10 |

---

## Test Cases

### Login

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 1.LOGIN-001 | Login with valid credentials redirects to Dashboard | None | 1. Fill all required fields (Username, Password) with valid credentials<br>2. Click "Log in" button | User is redirected to the Dashboard. | High |
| 1.LOGIN-002 | Access as a guest grants unauthenticated browsing | None | 1. Click "Access as a guest" button | User is granted unauthenticated access and can browse site content without signing in. | High |
| 1.LOGIN-003 | Direct URL access while logged out redirects to login | User is not logged in | 1. In the browser address bar, navigate directly to a protected page such as Dashboard.<br>2. Observe whether the app allows access or changes the page. | The user is redirected to the login page instead of viewing the protected page. | High |
| 1.LOGIN-005 | View cookie usage information via Cookies notice | None | 1. Click "Cookies notice" button | Cookie usage information is displayed (for example, in a dialog or banner) explaining cookie usage. | Medium |
| 1.LOGIN-006 | Open Cookies notice then access as a guest | None | 1. Click "Cookies notice" button<br>2. Click "Access as a guest" button | Cookie information is displayed and the user is then granted unauthenticated access to browse the site without signing in. | Medium |
| 1.LOGIN-007 | Page refresh while logged in keeps user logged in | User is logged in on an authenticated page | 1. Ensure you are on an authenticated page (for example, Dashboard) while logged in.<br>2. Refresh the browser (reload the current page).<br>3. Verify the page re-renders and you remain on the authenticated page. | After refresh the user remains authenticated and is not redirected to the login page. | Medium |
| 1.LOGIN-008 | Already-logged-in user navigating to login URL is redirected to authenticated landing page | User is already logged in | 1. While authenticated, navigate to the login URL or open the login page.<br>2. Observe where the application navigates you next. | The user is redirected away from the login page to the authenticated landing page (e.g., Dashboard). | Medium |
| 1.LOGIN-011 | Cookies notice button displays cookie usage information | None | 1. Click the Cookies notice button | Cookie usage information is displayed. | Low |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 1.LOGIN-004 | Login attempt with invalid credentials shows inline error and clears password | None | 1. Fill all required fields (Username, Password) with invalid credentials<br>2. Click "Log in" button | Inline error message is displayed; password field is cleared; username remains populated for correction. | High |
| 1.LOGIN-009 | Submit with all required fields empty | None | 1. Leave all required fields empty<br>2. Click "Log in" button | Validation errors shown for all required fields. | Medium |

#### Edge Case Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 1.LOGIN-010 | Lost password? link is disabled on the login page | None | 1. Click the "Lost password?" link | The link is disabled and does not navigate to a recovery page. | Medium |

---

### Dashboard

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 2.DASHBO-001 | Enable Edit mode reveals reset/add controls and per-block UI | None | 1. Click the Edit mode toggle to enable edit mode | The "Reset page to default" button appears at the top right; the "+ Add a block" button appears below the Dashboard heading; each block displays a move icon and a three-dot menu. | High |
| 2.DASHBO-002 | "+ Add a block" opens the block types listing (Edit mode required) | Edit mode enabled | 1. Click the "+ Add a block" button | A page listing all available block types opens. | High |
| 2.DASHBO-003 | Three-dot menu exposes configure, move, and delete actions for a block | Edit mode enabled and at least one block present | 1. Click a block's three-dot menu | The three-dot menu lists configure, move, and delete actions for that block. | High |
| 2.DASHBO-004 | Move icon enables repositioning a block | Edit mode enabled and at least two blocks present | 1. Click and drag a block using its move icon to a different valid position<br>2. Release the block at the target position | The block is repositioned to the new location. | High |
| 2.DASHBO-005 | Disable Edit mode hides reset/add controls and per-block UI | Edit mode enabled | 1. Click the Edit mode toggle to disable edit mode | The "Reset page to default" button, the "+ Add a block" button, move icons, and three-dot menus are not visible. | High |
| 2.DASHBO-006 | Timeline displays upcoming activities across enrolled courses | User is on Dashboard and Timeline block is visible with upcoming activities in multiple enrolled courses. | 1. Locate the Timeline block on the Dashboard<br>2. Inspect the listed Timeline items and note their course labels | Timeline shows upcoming activities and deadlines from multiple enrolled courses. | High |
| 2.DASHBO-007 | Using time range dropdown updates displayed Timeline items | User is on Dashboard and Timeline block contains items across multiple time ranges. | 1. Open the time range dropdown<br>2. Select a different time range option | Timeline items update to display only activities within the selected time range. | High |
| 2.DASHBO-008 | Using sort order dropdown changes the sort order of Timeline items | User is on Dashboard and Timeline block shows at least two items with different dates or priorities. | 1. Open the sort order dropdown within the Timeline block<br>2. Select an alternate sort order option | Timeline items reorder according to the selected sort criterion. | High |
| 2.DASHBO-009 | Search field finds activities by name | User is on Dashboard and Timeline block contains an activity with a unique name. | 1. Enter the activity name into the Timeline search field<br>2. Trigger the search or apply the search filter | Search results include activities whose name matches the search query. | High |
| 2.DASHBO-010 | Search field finds activities by type | User is on Dashboard and Timeline block contains activities of the specified type. | 1. Enter the activity type into the Timeline search field<br>2. Trigger the search or apply the search filter | Search results include activities whose type matches the search query. | High |
| 2.DASHBO-011 | Create personal calendar entry via New event button | Calendar block is visible on the Dashboard | 1. Click "New event" in the Calendar block<br>2. Fill all required fields (event title, date/time, description or other required fields)<br>3. Click "Save" or "Create" to submit the event | Personal calendar entry is created and the event name appears inline on the corresponding date in the monthly view. | High |
| 2.DASHBO-012 | Monthly view shows current month and year heading | Calendar block is visible on the Dashboard | 1. Observe the Calendar block's monthly view heading | The Calendar shows the current month and year as a heading in the monthly view. | High |
| 2.DASHBO-013 | Navigate to next month using right arrow | Calendar block is visible on the page showing a monthly view | 1. Click the Calendar right arrow control | Monthly heading updates to the next month and year and event indicators for the newly visible month update accordingly. | High |
| 2.DASHBO-014 | Navigate to previous month using left arrow | Calendar block is visible on the page showing a monthly view | 1. Click the Calendar left arrow control | Monthly heading updates to the previous month and year and event indicators for the newly visible month update accordingly. | High |
| 2.DASHBO-015 | Calendar shows current month and year as monthly heading | Calendar block is visible on the page | 1. Observe the Calendar monthly heading | The Calendar monthly view displays the current month and year as the heading. | High |
| 2.DASHBO-016 | Current date is highlighted in the Calendar monthly view | Calendar block is visible and showing the current month | 1. Observe the Calendar monthly view | The cell corresponding to the current date is visually highlighted in the calendar. | High |
| 2.DASHBO-017 | Blocks show move icon and three-dot menu in Edit mode | Edit mode enabled | 1. Identify an existing block on the dashboard<br>2. Observe the block header area for the presence of a move icon and a three-dot menu | Each block displays both a move icon and a three-dot menu while Edit mode is enabled. | High |
| 2.DASHBO-018 | Three-dot menu exposes configure, move, and delete actions | Edit mode enabled | 1. Click the three-dot menu for a chosen block<br>2. Inspect the menu contents | The menu lists Configure, Move, and Delete actions for the block. | High |
| 2.DASHBO-019 | Move a block using move controls (triggerable from: move icon, three-dot menu 'Move' action) | Edit mode enabled and at least two blocks present on the dashboard | 1. Use either the block's move icon or open its three-dot menu and select the Move action<br>2. Reposition the block to a different location and complete the move action | The block's position changes to the new location and the dashboard reflects the updated block order. | High |
| 2.DASHBO-020 | Delete a block via three-dot menu | Edit mode enabled and the target block is present | 1. Click the three-dot menu for the target block<br>2. Click the Delete action and confirm the deletion in the confirmation dialog | The block is removed from the dashboard and no longer appears in the block list. | High |
| 2.DASHBO-022 | Dates with events display their names inline | Calendar block is visible and at least one event exists in the visible month | 1. Observe dates in the monthly view that have events | Dates that have events display the event names inline on their date cells. | Medium |
| 2.DASHBO-023 | Open Configure for a block via the three-dot menu | Edit mode enabled | 1. Click the three-dot menu for a chosen block<br>2. Click the Configure action in the menu | Block configuration panel or dialog opens allowing configuration of that block. | Medium |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 2.DASHBO-021 | Block-level controls unavailable when not in Edit mode | Edit mode disabled | 1. Locate an existing block on the dashboard<br>2. Attempt to find or interact with the move icon or the block's three-dot menu | The move icon and three-dot menu are not visible or are not actionable when Edit mode is disabled. | High |
| 2.DASHBO-024 | "+ Add a block" button not present when Edit mode is off | None | 1. Ensure Edit mode is disabled<br>2. Check for visibility of the "+ Add a block" button below the Dashboard heading | The "+ Add a block" button is not visible when Edit mode is off. | Medium |
| 2.DASHBO-025 | Block move icon and three-dot menu not visible when Edit mode is off | None | 1. Ensure Edit mode is disabled<br>2. Check a block for the presence of a move icon and a three-dot menu | Blocks do not display a move icon or a three-dot menu when Edit mode is off. | Medium |
| 2.DASHBO-026 | Selecting a time range with no matching items shows empty state | User is on Dashboard and no Timeline items exist within the target time range. | 1. Open the time range dropdown in the Timeline block<br>2. Select the time range that contains no items | An empty state is shown indicating no Timeline items match the selected range. | Medium |
| 2.DASHBO-027 | Submit with all required fields empty | Calendar block is visible on the Dashboard | 1. Leave all required fields empty in the New event form<br>2. Click "Save" or "Create" | Validation errors shown for all required fields. | Medium |

#### Edge Case Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 2.DASHBO-028 | Advance across year boundary using right arrow (month and year update) | Calendar block is visible and showing the last month of a year | 1. Click the Calendar right arrow control once | Monthly heading advances to the first month of the next year and event indicators for that month are shown as applicable. | Medium |
| 2.DASHBO-029 | Advance multiple months by repeatedly clicking the right arrow | Calendar block is visible on the page showing a monthly view | 1. Click the Calendar right arrow control multiple times to advance several months | Monthly heading advances one month per click (including year changes when applicable) and dates with events display their names inline for each newly visible month. | Low |

---

### My Courses

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 3.MYCOU-001 | Course card displays banner, clickable name, and category | My Courses page is open and contains at least one course card | 1. Locate a course card in the courses grid<br>2. Inspect the course card to verify it shows a banner image, the course name rendered as a clickable link, and the category name | The course card displays a banner image, the course name is a clickable link, and the category name is visible | High |
| 3.MYCOU-002 | Clicking the course name navigates to the course main page | My Courses page is open with at least one course card | 1. Click the course name link on a course card<br>2. Verify the course main page is displayed (course title and course-level navigation elements are visible) | User is taken to the course main page for that course | High |
| 3.MYCOU-003 | Star this course pins the course to the top of the list | My Courses page is open and contains multiple course cards with at least one course not already at the top | 1. Open the three-dot menu for a non-top course card<br>2. Click the "Star this course" action<br>3. Observe the course cards ordering in the grid | The selected course moves to the top of the courses grid (is pinned to the top) | High |
| 3.MYCOU-004 | Remove from view hides the course from the My Courses listing | My Courses page is open and contains the target course card | 1. Open the three-dot menu for the target course card<br>2. Click the "Remove from view" action<br>3. Verify the course no longer appears in the course grid | The course is hidden from the My Courses listing without changing enrollment | High |
| 3.MYCOU-005 | Controls above the course grid present and offer expected options | My Courses page is open | 1. Verify four controls appear above the course grid: a status dropdown, a search field, a sort dropdown, and a layout dropdown<br>2. Open the status dropdown and verify it lists the expected status options; open the layout dropdown and verify it lists the expected layout options | All four controls are present above the grid and the dropdowns expose the listed options | Medium |
| 3.MYCOU-006 | Three-dot menu lists course-level actions including Star and Remove | My Courses page is open and a course card is visible | 1. Open the three-dot menu for a course card<br>2. Verify the menu contains the actions for starring the course and removing the course from view | The three-dot menu displays the actions such as starring the course and removing it from view | Medium |

---

### Course Page

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 4.COUPAG-001 | Collapse all collapses every collapsible section | Course page open with multiple sections expanded | 1. Ensure at least two sections are expanded (use section chevrons to expand if needed)<br>2. Click the "Collapse all" link | All sections collapse simultaneously; section contents are hidden and chevrons indicate collapsed state. | High |
| 4.COUPAG-002 | Collapse all preserves course heading and navigation tab bar | Course page open with course name and navigation tab bar visible | 1. Click the "Collapse all" link | Course name remains as the page heading and the navigation tab bar remains displayed directly below the heading. | High |
| 4.COUPAG-003 | Activities and resources show type icon and clickable name within sections | Course page open with at least one section containing activities or resources | 1. Ensure a section containing activities/resources is expanded<br>2. Inspect the listed activities and resources | Each activity and resource displays a type icon and its name is presented as a clickable link. | High |
| 4.COUPAG-004 | Expand a collapsed section to reveal its activities and resources | Course page is open with at least one collapsed section containing activities | 1. Locate a collapsed section in the main content area<br>2. Click the section's collapsible chevron to expand it<br>3. Verify the activities and resources inside the section are visible | The section expands and its activities and resources are displayed. | High |
| 4.COUPAG-005 | Collapse an expanded section to hide its activities and resources | Course page is open with at least one expanded section containing activities | 1. Locate an expanded section in the main content area<br>2. Click the section's collapsible chevron to collapse it<br>3. Verify the activities and resources inside the section are hidden | The section collapses and its activities and resources are hidden. | High |
| 4.COUPAG-006 | Enable and disable Edit mode when user has edit permission | User is signed in with edit permissions and Course page is open. | 1. Click the "Edit mode" toggle/button to enable edit mode<br>2. Verify editing controls or edit UI are available on the Course page<br>3. Click the "Edit mode" toggle/button to disable edit mode<br>4. Verify editing controls are no longer available | Edit mode toggles on and off; availability of editing controls matches the toggle state. | High |
| 4.COUPAG-008 | Collapse all collapses sections while preserving Course Index sidebar and active item highlight | Course page open with the Course Index sidebar visible and an active item highlighted | 1. Click the "Collapse all" link | All sections collapse and the Course Index sidebar remains visible with the previously active item still highlighted. | Medium |
| 4.COUPAG-009 | Each activity and resource shows a type icon and has a clickable name when section is expanded | Course page is open with an expanded section containing activities/resources | 1. Ensure the target section is expanded<br>2. For each listed activity/resource in the section, verify a type icon is displayed and the name is clickable | All activities and resources display a type icon and have clickable names. | Medium |
| 4.COUPAG-010 | Course name is displayed as page heading with the navigation tab bar immediately following | Course page is open | 1. Observe the top of the course page<br>2. Verify the course name appears as the page heading and the navigation tab bar is displayed immediately after the heading | Course name appears as the page heading followed by the navigation tab bar. | Medium |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 4.COUPAG-007 | Prevent student from enabling Edit mode | User is signed in as a student and Course page is open. | 1. Click the "Edit mode" toggle/button on the Course page | Edit mode is not enabled; the student is prevented from activating edit controls (toggle stays off or a permission message is shown). | High |

#### Edge Case Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 4.COUPAG-011 | Only the clicked section toggles; other sections remain unchanged | Course page is open with at least two sections in different states (one expanded, one collapsed) | 1. Note the current expanded/collapsed state of two adjacent sections<br>2. Click the collapsible chevron of one section<br>3. Verify only the clicked section's state changes and the other section's state remains as before | Only the clicked section toggles; other sections are unaffected. | Medium |
| 4.COUPAG-012 | Clicking Collapse all when sections are already collapsed leaves state unchanged | Course page open with all sections already collapsed | 1. Click the "Collapse all" link | No visual change occurs; all sections remain collapsed. | Low |
| 4.COUPAG-013 | Toggling a section twice restores its original expanded/collapsed state | Course page is open with a section in a known expanded or collapsed state | 1. Note the current state of a section<br>2. Click the section's collapsible chevron to change its state<br>3. Click the same chevron again<br>4. Verify the section returns to its original state | After two toggles the section returns to its original state. | Low |

---

### Participants

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 5.PARTIC-001 | Apply a single filter condition to refine participants list | Participants page is open and participants are listed in the table. | 1. Select an attribute from the Select attribute dropdown and enter a matching value<br>2. Click "Apply filters" | Participants table shows only users matching the filter condition. | High |
| 5.PARTIC-002 | Apply multiple filter conditions with Any toggle enabled | Participants page is open and participants are listed in the table. | 1. Enable the "Any" toggle<br>2. Click "+ Add condition" and fill both condition rows (Select attribute dropdown and corresponding value for each)<br>3. Click "Apply filters" | Participants table is filtered according to the built conditions and the Any toggle setting. | High |
| 5.PARTIC-003 | Clear filters removes all active conditions and shows full participants list | Filter builder contains one or more active conditions | 1. Add multiple filter conditions using the Any toggle, Select attribute dropdown, and the "+ Add condition" link<br>2. Click the "Clear filters" button | All filter conditions are removed and the participants table displays all enrolled users. | High |
| 5.PARTIC-004 | Filter participants by First name initial | Participants page is open and the participants table is visible. | 1. Click the alphabetical button for First name for a chosen initial | Participants table shows only users whose first name begins with the chosen initial. | High |
| 5.PARTIC-005 | Filter participants by Last name initial | Participants page is open and the participants table is visible. | 1. Click the alphabetical button for Last name for a chosen initial | Participants table shows only users whose last name begins with the chosen initial. | High |
| 5.PARTIC-006 | Reset alphabetical filters via All (triggerable from: First name All, Last name All) | Participants page is open and a filtered view may be active. | 1. Click the "All" alphabetical button for First name or Last name | Participants table displays the full list of enrolled users (filter cleared). | High |
| 5.PARTIC-007 | Click a participant name opens their profile | Participants page is open and the participants table is visible. | 1. Click a participant's First or Last name link in the participants table | Participant profile page opens and displays that user's details. | High |
| 5.PARTIC-008 | Participants page initially lists all enrolled users | Participants page is open and no alphabetical filter is applied. | 1. Observe the participants table without applying any alphabetical filters | Participants table lists all users enrolled in the course. | High |
| 5.PARTIC-009 | Add multiple conditions using "+ Add condition" shows new condition row | Participants page is open and participants are listed in the table. | 1. Click "+ Add condition" | A new condition row appears containing a Select attribute dropdown and a value input control. | Medium |
| 5.PARTIC-010 | Clear filters button enabled when a filter condition exists | None | 1. Add a single filter condition using the Select attribute dropdown and the "+ Add condition" link<br>2. Observe the enabled/disabled state of the "Clear filters" button | The "Clear filters" button is enabled when at least one filter condition is present. | Medium |
| 5.PARTIC-014 | Toggle the Any control updates filter mode state | Participants page is open and participants are listed in the table. | 1. Toggle the "Any" control to change its state | The Any toggle reflects the new state and the filter mode UI updates accordingly. | Low |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 5.PARTIC-011 | Apply filters with all required fields empty | Participants page is open and participants are listed in the table. | 1. Leave all required filter fields empty<br>2. Click "Apply filters" | Validation errors shown for all required filter fields. | Medium |
| 5.PARTIC-012 | Apply filters with a condition value empty shows validation error | Participants page is open and participants are listed in the table. | 1. Click "+ Add condition"<br>2. Select an attribute from the Select attribute dropdown and leave the condition value empty<br>3. Click "Apply filters" | Validation error indicating the condition value is required is shown for the incomplete condition row. | Medium |

#### Edge Case Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 5.PARTIC-013 | Apply filters with no conditions added | Participants page is open and participants are listed in the table. | 1. Ensure no filter conditions are present<br>2. Click "Apply filters" | Participants table continues to list all enrolled users (no filtering applied). | Medium |
| 5.PARTIC-015 | Clear filters when no conditions present leaves participants list unchanged | Filter builder is empty (no active conditions) | 1. Ensure no filter conditions are present (no toggle selected and no conditions added)<br>2. Click the "Clear filters" button | Participants table remains showing all enrolled users and the filter builder stays empty. | Low |
| 5.PARTIC-016 | Select an initial with no matching participants shows empty results | Participants page is open and at least one alphabetical initial has no matching participants. | 1. Click the alphabetical button for First name for an initial that has no matching participants | Participants table displays no rows or an empty-state message indicating no matches. | Low |

---

### Grades

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 6.GRADES-001 | View own grades via User report | User is authenticated as a student and the User report (Grades page) is open | 1. Ensure the User report (Grades) is visible on the page<br>2. Inspect the Grade table and verify at least one grade item row is listed under the course header | Grades page displays the student's own grades for the course via a User report. | High |
| 6.GRADES-002 | Grade column shows earned value for a graded activity | User is authenticated as a student and the User report (Grades page) is open | 1. Locate a graded activity row in the Grade table<br>2. Verify the Grade cell for that activity displays an earned value (numeric or letter) rather than the placeholder | Earned value is shown in the Grade column for graded items. | High |
| 6.GRADES-003 | Course header collapsible expands to show indented graded activities | User is authenticated as a student and the User report (Grades page) is open | 1. Identify the course name shown as a collapsible header in the Grade table<br>2. Click the course header to expand it<br>3. Verify graded activities are visible and appear indented beneath the course header | Course name appears as a collapsible header with graded activities indented beneath. | High |
| 6.GRADES-004 | Grade table displays all expected columns | User is authenticated as a student and the User report (Grades page) is open | 1. Inspect the Grade table header row<br>2. Verify the columns: Grade item, Calculated weight, Grade, Range, Percentage, Feedback, and Contribution to course total are present | Grade table columns are displayed as specified in the Grade table layout. | High |
| 6.GRADES-005 | AGGREGATION Course total row shows cumulative course grade | User is authenticated as a student and the User report (Grades page) is open | 1. Scroll to the bottom of the Grade table<br>2. Verify the AGGREGATION Course total row is present and displays a cumulative grade value across weighted items | AGGREGATION Course total row displays the cumulative grade across all weighted items. | High |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 6.GRADES-006 | Prevent student from accessing the full gradebook | User is authenticated as a student and the User report (Grades page) is open | 1. Click any visible link or control labeled to open the full gradebook from the Grades page<br>2. Observe the response (page content, error message, or access restriction) | Student is prevented from accessing the full gradebook (access denied or full gradebook not displayed). | High |
| 6.GRADES-007 | Prevent student from viewing another student's grades | User is authenticated as a student and the User report (Grades page) is open | 1. Attempt to open a different user's grade view by clicking any student name or user-report link visible on the page<br>2. Observe whether grade details for another student are displayed or access is blocked | Student cannot view other students' grades; other students' grade details are not accessible. | High |

#### Edge Case Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 6.GRADES-008 | Ungraded activity displays placeholder "–" in Grade column | User is authenticated as a student and the User report (Grades page) is open | 1. Locate an activity known to be not yet graded in the Grade table<br>2. Verify the Grade cell for that activity displays "–" | Grade column shows "–" for activities that have not yet been graded. | Medium |

---

### Assignment

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 7.ASSIGN-001 | Submit assignment using online text editor | Assignment page is open and the submission form includes an online text editor. | 1. Click "Add submission"<br>2. Fill the online text editor with valid submission content<br>3. Click the submission form's submit button | Submission status changes to 'Submitted for grading'; the Submission status section shows the summary table rows for Submission status, Grading status, Time remaining, Last modified, and Submission comments; Last modified is updated and Grading status shows 'Not graded'. | High |
| 7.ASSIGN-002 | Submit assignment using file upload only | Assignment page is open and the submission form includes a file upload area. | 1. Click "Add submission"<br>2. Upload a valid file in the file upload area<br>3. Click the submission form's submit button | Submission status changes to 'Submitted for grading'; the Submission status section shows the summary table rows for Submission status, Grading status, Time remaining, Last modified, and Submission comments; Last modified is updated and Grading status shows 'Not graded'. | High |
| 7.ASSIGN-003 | Submit assignment using both online text and file upload | Assignment page is open and the submission form includes both an online text editor and a file upload area. | 1. Click "Add submission"<br>2. Fill the online text editor with valid submission content and upload a valid file<br>3. Click the submission form's submit button | Submission status changes to 'Submitted for grading'; the Submission status section shows the summary table rows for Submission status, Grading status, Time remaining, Last modified, and Submission comments; Last modified is updated and Grading status shows 'Not graded'. | High |
| 7.ASSIGN-004 | Edit an existing submission before the due date | Submission page is open, student has an existing submission, and due date has not passed. | 1. Click the "Edit submission" control on the submission page<br>2. Modify the online text editor content and/or attach files in the file upload area as applicable<br>3. Click "Save changes" or "Submit" | Submission updates are saved, Last modified updates, and Submission status shows the submission as updated. | High |
| 7.ASSIGN-005 | Edit submission after due date when teacher permits resubmission | Submission page is open, student has an existing submission, due date has passed, and teacher permits resubmission. | 1. Click the "Edit submission" control<br>2. Modify the online text editor content and/or attach files in the file upload area<br>3. Click "Save changes" or "Submit" | Submission updates are saved and Last modified updates reflecting the resubmission. | High |
| 7.ASSIGN-006 | View earned grade and written feedback after grading | Submission page is open and the student's submission has been graded. | 1. Locate the grading area on the submission page<br>2. Verify the earned grade is visible and the written feedback is displayed | Earned grade and written feedback appear on the submission page. | High |
| 7.ASSIGN-008 | Open submission form via Add submission | Assignment page is open and the "Add submission" control is visible. | 1. Click "Add submission"<br>2. Verify the submission form is displayed (online text editor and/or file upload area present as configured) | Submission form opens showing the configured online text editor and/or file upload area. | Medium |
| 7.ASSIGN-009 | Assignment page displays opened date, due date, and full description | Assignment page is open. | 1. Verify the Assignment page displays the Opened date, Due date, and full Description | Opened date, Due date, and full Description are visible on the Assignment page. | Medium |
| 7.ASSIGN-010 | Submission status summary table displays required rows | Assignment submission page is open. | 1. Locate the Submission status section on the page<br>2. Verify the summary table contains rows for Submission status, Grading status, Time remaining, Last modified, and Submission comments | Summary table lists Submission status, Grading status, Time remaining, Last modified, and Submission comments. | Medium |
| 7.ASSIGN-011 | Assignment page displays Opened date, Due date, and full Description | Assignment page is open. | 1. Locate the assignment metadata area on the page<br>2. Verify the Opened date, Due date, and the full Description are displayed | Assignment page shows Opened date, Due date, and full Description. | Medium |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 7.ASSIGN-007 | Prevent editing when due date has passed and teacher does not permit resubmission | Submission page is open, student has an existing submission, due date has passed, and teacher does not permit resubmission. | 1. Attempt to click the "Edit submission" control or locate edit inputs<br>2. Observe availability of edit controls and the submission form | Editing is not available: edit controls are absent or disabled and the submission cannot be modified. | High |
| 7.ASSIGN-012 | Submit with all required fields empty | Assignment page is open and the submission form is available. | 1. Click "Add submission"<br>2. Leave all required submission fields empty<br>3. Click the submission form's submit button | Submission is not accepted and Submission status remains 'No submissions have been made yet'. | Medium |
| 7.ASSIGN-013 | Submit with all required fields empty | Submission form is open and configured with at least one submission input. | 1. Leave all required submission fields empty<br>2. Click "Save changes" or "Submit" | Submission is not accepted: validation errors are shown or the submission remains in a no-submission state. | Medium |

#### Edge Case Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 7.ASSIGN-014 | Submission summary shows grading status options after submission | A valid submission has been made and the Assignment page is open. | 1. Verify the Submission status section's summary table displays the Grading status row<br>2. Observe the Grading status value shown in the summary table | Grading status displays either 'Not graded' or 'Graded' in the summary table. | Low |

---

### Activities

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 8.ACTIVI-001 | Assignments section displays expanded table with Name, Due date, and Submission status | Course page with activity sections visible. | 1. Observe the Assignments section header on the course page<br>2. Verify the section is expanded and displays a table with columns for Name (clickable link with parent section shown below), Due date, and Submission status | The Assignments section is expanded and the table shows columns for Name (clickable link with parent section shown below), Due date, and Submission status. | High |
| 8.ACTIVI-002 | Forums and Resources are collapsed by default and expand via arrow | Course page with activity sections visible. | 1. Confirm the Forums section and the Resources section are collapsed by default<br>2. Click the expand arrow for each collapsed section and verify each section expands to display its activities | Forums and Resources are collapsed initially and expand to show their activities when the arrow is clicked. | High |
| 8.ACTIVI-003 | Clicking an activity name navigates directly to that activity's page | Course page with at least one activity visible in an expanded section. | 1. Click any activity Name link within an expanded section<br>2. Verify the activity's page opens and displays the activity title corresponding to the clicked name | Clicking any activity name navigates directly to that activity's page. | High |
| 8.ACTIVI-004 | Additional activity types appear as distinct collapsible sections and expand | Course page containing additional activity types. | 1. Locate any additional activity type section on the page<br>2. Verify it appears as a collapsible section and click its arrow to expand<br>3. Confirm the section expands and its contained activities or resources become visible | Additional activity types appear as their own collapsible sections and expand to reveal their contents when the arrow is clicked. | Medium |

#### Edge Case Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 8.ACTIVI-005 | Collapse the Assignments section (expanded by default) hides the assignments table | Course page with the Assignments section visible and expanded. | 1. Confirm the Assignments section is expanded by default<br>2. Click the collapse arrow for the Assignments section<br>3. Verify the assignments table is no longer visible and the section displays a collapsed state | The Assignments table is hidden and the Assignments section shows a collapsed state after clicking the collapse arrow. | Medium |
| 8.ACTIVI-006 | Toggle expand/collapse repeatedly on Forums and Resources to verify stable behavior | Course page with Forums and Resources sections present. | 1. For each of the Forums and Resources sections, click the expand arrow to expand the section<br>2. Click the same arrow to collapse the section, then click again to expand once more<br>3. Verify the sections reliably toggle between expanded and collapsed states each time the arrow is clicked | Forums and Resources reliably toggle between expanded and collapsed states when their arrows are clicked repeatedly. | Low |

---

### Profile

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 9.PROFIL-001 | Profile header displays initials, full name, Message button, and optional description | Profile page is open | 1. Verify the circular initials icon is visible in the header area<br>2. Verify the user's full name and the "Message" button are visible<br>3. Verify the profile description is displayed when present (optional) | The header shows the initials icon, full name, Message button, and the profile description when provided. | High |
| 9.PROFIL-002 | User details card shows email, visibility note, timezone, and Edit profile link | Profile page is open | 1. Inspect the User details information card<br>2. Verify the email address, visibility note, timezone, and an "Edit profile" link are present | User details card lists email address, visibility note, timezone, and an "Edit profile" link. | High |
| 9.PROFIL-003 | Clicking Edit profile opens profile form with collapsible panels and all fields | Profile page is open | 1. Click "Edit profile" in the User details card<br>2. Verify the profile form opens and displays collapsible panels and fields (General, First name, Last name, Email address, Email visibility, MoodleNet profile ID, City/town, Country, Timezone, Description, User picture, Additional names, Interests, Optional fields) | Profile form opens with collapsible panels and all profile fields available for editing. | High |
| 9.PROFIL-004 | Edit profile: modify fields and save updates are reflected on the profile page | Profile page of the current student is open | 1. Click "Edit profile"<br>2. Modify editable fields (for example First name, Last name, Description, or upload a new user picture)<br>3. Click "Save" | Profile page reflects the updated values after saving. | High |
| 9.PROFIL-005 | Update profile with valid required fields | Profile form is open. | 1. Fill all required fields (First name, Last name, Email address and other required fields)<br>2. Click "Update profile" | Changes are saved and the profile page reflects the updated values. | High |
| 9.PROFIL-006 | Open profile form via Edit profile | User is viewing their Profile page. | 1. Click "Edit profile" | Profile form is displayed and ready for editing. | High |
| 9.PROFIL-007 | Cancel discards edits and returns to profile display | User is viewing their Profile page. | 1. Click "Edit profile"<br>2. Modify one or more editable fields in the profile form<br>3. Click "Cancel" | Profile form closes, changes are not saved, and the profile display shows the original values. | High |
| 9.PROFIL-010 | Collapsible panels expand and collapse in Edit profile form | Profile page is open and profile form is opened | 1. Click "Edit profile" to open the profile form<br>2. Expand a collapsible panel and verify its contained fields become visible<br>3. Collapse the same panel and verify the contained fields are hidden | Panels expand to reveal fields and collapse to hide them. | Medium |
| 9.PROFIL-011 | Open Edit profile form | User is viewing their own profile page. | 1. Click "Edit profile" | The profile form opens with editable fields. | Medium |
| 9.PROFIL-012 | Save profile leaving Description empty | Profile form is open. | 1. Fill all required fields (First name, Last name, Email address and other required fields), leave Description empty<br>2. Click "Update profile" | Profile is saved successfully and the Description remains empty. | Medium |
| 9.PROFIL-013 | Upload new user picture and save | Profile form is open. | 1. In the User picture section select a new picture to upload and optionally fill picture description<br>2. Fill all required fields if not already filled<br>3. Click "Update profile" | The user picture is updated to the newly uploaded image on the profile. | Medium |
| 9.PROFIL-014 | Change email visibility and persist setting | Profile form is open. | 1. Change the Email visibility setting<br>2. Fill all other required fields<br>3. Click "Update profile" | The updated Email visibility setting is saved and reflected on the profile. | Medium |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 9.PROFIL-008 | Edit option not available when viewing another student's profile | Profile page of another student is open | 1. Inspect the User details card on the other student's profile page<br>2. Verify the "Edit profile" link is not present or editing is not available | Student is unable to access edit functionality; the "Edit profile" link is not visible or editing is blocked. | High |
| 9.PROFIL-009 | Prevent student from editing another student's profile | User is viewing another student's profile page. | 1. Attempt to click "Edit profile" or initiate edit on the displayed profile | Editing is not permitted for this profile; user cannot make or save changes. | High |
| 9.PROFIL-015 | Submit with all required fields empty | Profile page is open | 1. Click "Edit profile"<br>2. Leave all required fields empty<br>3. Click "Save" | Validation errors shown for all required fields. | Medium |
| 9.PROFIL-016 | Submit with all required fields empty | Profile form is open. | 1. Leave all required fields empty<br>2. Click "Update profile" | Validation errors shown for all required fields. | Medium |
| 9.PROFIL-017 | Edit profile action not available when viewing another user's profile | User is viewing another user's Profile page. | 1. Check the profile page for the presence or availability of the "Edit profile" action | "Edit profile" action is not present or is disabled for the user. | Medium |

#### Edge Case Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 9.PROFIL-018 | Save succeeds when Description is left empty (description optional) | Profile page is open | 1. Click "Edit profile"<br>2. Fill other required fields leaving the Description field empty<br>3. Click "Save" | Profile is saved successfully and no description is displayed on the profile page. | Low |

---

### Logout

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 10.LOGOUT-001 | Log out ends session and returns to login page | User is authenticated and top navigation bar is visible | 1. Click the user's initials icon to open the user menu<br>2. Click the Log out option in the user menu | The current authenticated session is terminated and the page redirects to the login page | High |
| 10.LOGOUT-002 | Logout from user menu terminates session and shows login page | User is logged in | 1. Open the user menu by clicking the user's initials in the top navigation.<br>2. Click the Log out option in the user menu.<br>3. Verify the application displays the login page after logging out. | The session is terminated and the login page is displayed after using the Log out option. | High |
| 10.LOGOUT-003 | Protected routes inaccessible after logout | User has just logged out after an active session | 1. After completing logout, attempt to navigate to a protected page such as Dashboard or Course Page.<br>2. Observe whether the protected content loads or access is blocked. | Access to the protected route is denied and the user is redirected to the login page or shown an access denied state. | High |
| 10.LOGOUT-004 | Browser refresh after logout does not restore authenticated session | User has just logged out | 1. After logging out and seeing the login page, refresh the browser.<br>2. Verify whether any authenticated content reappears or the user remains on the login page. | Refreshing the browser does not restore the authenticated session; the user remains logged out and sees the login page. | High |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 10.LOGOUT-005 | Protected page access requires re-authentication after logout | User is authenticated and top navigation bar is visible | 1. Click the user's initials icon to open the user menu<br>2. Click the Log out option in the user menu<br>3. Click the Dashboard link in the top navigation | Navigation to the protected page is blocked and the user is prompted to log in (redirected to the login page) | High |

#### Edge Case Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 10.LOGOUT-006 | Browser Back does not restore authenticated session after logout | User is authenticated and top navigation bar is visible | 1. Click the user's initials icon to open the user menu<br>2. Click the Log out option in the user menu<br>3. Use the browser Back button<br>4. Attempt to click a protected link visible on the page (for example, My Courses or Dashboard) | User remains logged out; attempts to access protected content require login and redirect to the login page | Medium |

---

## Navigation Graph

![Navigation Graph](Output/MoodleStudent/navigation_graph.png)

### Pages

| Module | URL | Test Cases |
|--------|-----|------------|
| Login | /login | 11 |
| Dashboard | /dashboard | 29 |
| My Courses | /mycourses | 6 |
| Course Page | /course/{courseId} | 13 |
| Participants | /course/{courseId}/participants | 16 |
| Grades | /course/{courseId}/grades | 8 |
| Assignment | /course/{courseId}/assignment/{activityId} | 14 |
| Activities | /course/{courseId}/activities | 6 |
| Profile | /user/profile/{userId} | 18 |
| Logout | /logout | 6 |
