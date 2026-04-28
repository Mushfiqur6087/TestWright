# Moodleteacher

**Base URL:** 
**Generated:** 2026-04-27T04:37:50.026622

## Summary

| Metric | Count |
|--------|-------|
| **Total Tests** | 244 |

### By Type

| Type | Count |
|------|-------|
| Positive | 175 |
| Negative | 37 |
| Edge Case | 32 |

### By Priority

| Priority | Count |
|----------|-------|
| High | 122 |
| Medium | 97 |
| Low | 25 |

---

## Test Cases

### Login

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 1.LOGIN-001 | Login with valid credentials redirects to Dashboard | None | 1. Fill all required fields (Username, Password) with valid credentials for a teacher account<br>2. Click "Log in" button | User is redirected to the Dashboard. | High |
| 1.LOGIN-002 | Access as a guest offers unauthenticated browsing | None | 1. Click "Access as a guest" button | Unauthenticated browsing is offered (guest access to course content is provided). | High |
| 1.LOGIN-003 | Direct URL access while logged out redirects to login | User is not logged in | 1. In a new browser session, enter the URL of a protected page (for example, the Dashboard) in the address bar and press Enter.<br>2. Observe the page that loads and inspect the UI for the presence of the login form or login page content. | The browser redirects to the login page and the protected page content is not accessible without authentication. | High |
| 1.LOGIN-004 | Cookies notice button displays cookie usage information | None | 1. Click the "Cookies notice" button | Cookie usage information is displayed to the user. | Medium |
| 1.LOGIN-005 | Page refresh while logged in keeps user logged in | User is logged in on an authenticated page | 1. While authenticated on an authenticated page (for example, Dashboard), click the browser refresh/reload button or press the refresh key.<br>2. Confirm the page reloads and user-specific UI elements (such as the user initials in the top navigation and access to the user menu) remain visible and no redirect to the login page occurs. | After the refresh the user remains authenticated, the page re-renders, and no redirect to the login page happens. | Medium |
| 1.LOGIN-006 | Already-logged-in user navigating to login URL is redirected to authenticated landing page | User is already logged in | 1. While signed in, navigate to the site's login page URL (enter the login page address in the address bar and press Enter).<br>2. Verify the application redirects away from the login page to the authenticated landing page (for example, Dashboard) and the login form is not shown. | The already-authenticated user is redirected away from the login page to an authenticated landing page and does not see the login form. | Medium |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 1.LOGIN-007 | Submit with all required fields empty | None | 1. Leave all required fields empty<br>2. Click "Log in" button | Validation errors shown for all required fields. | Medium |
| 1.LOGIN-008 | Invalid credentials show inline error, clear password, and retain username | None | 1. Fill all required fields (Username with an invalid username, Password with an invalid password)<br>2. Click "Log in" button | An inline error message is shown; the password field is cleared; the username remains populated for correction. | Medium |
| 1.LOGIN-009 | Lost password? link is disabled on test site | None | 1. Inspect the "Lost password?" link<br>2. Attempt to activate or click the "Lost password?" link | The "Lost password?" link is disabled and cannot be used on this site. | Low |

---

### Dashboard

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 2.DASHBO-001 | Timeline aggregates upcoming teaching actions across enrolled courses | User is on the Dashboard and multiple upcoming teaching actions exist across different enrolled courses | 1. Select a time range from the Time Range dropdown that includes upcoming items<br>2. Observe the Timeline block contents | Timeline displays upcoming teaching actions aggregated from the user's enrolled courses. | High |
| 2.DASHBO-002 | Change sort order to reorganize timeline items | Timeline shows multiple upcoming items in the selected time range | 1. Select a time range that includes multiple upcoming items<br>2. Select a different option from the Sort Order dropdown | Timeline items reorder to reflect the selected sort order. | High |
| 2.DASHBO-003 | Search narrows timeline to matching upcoming actions | At least one upcoming teaching action matches the intended search term | 1. Enter a search term matching an upcoming action in the Search field and trigger the search | Timeline shows only upcoming actions that match the search term. | High |
| 2.DASHBO-004 | Create a new calendar event via New event and verify it appears in monthly view | User is logged in and Dashboard page with Calendar block is visible | 1. Click the "New event" button in the Dashboard Calendar block<br>2. Fill all required fields (Event title, Date, Time, and any required visibility/course selection)<br>3. Click "Save" or "Create" in the event dialog | The event is created and its name appears inline on the correct date in the Calendar block's monthly view; the calendar still shows the current month and year heading | High |
| 2.DASHBO-005 | Filter calendar by a single course | Calendar block is visible on the Dashboard | 1. Click the "All courses" dropdown<br>2. Select a specific course from the dropdown | Calendar updates to show only events belonging to the selected course and dates with events display their names inline. | High |
| 2.DASHBO-006 | Show events for all courses using the All courses option | Calendar block is visible on the Dashboard | 1. Click the "All courses" dropdown<br>2. Select the "All courses" option | Calendar displays events from all courses and dates with events display their names inline. | High |
| 2.DASHBO-007 | Switching course selection updates displayed calendar events | Calendar block is visible on the Dashboard | 1. Click the "All courses" dropdown and select one course<br>2. Open the "All courses" dropdown again and select a different course | Calendar refreshes after each selection so the events shown correspond to the currently selected course and dates with events show their names inline. | High |
| 2.DASHBO-008 | Calendar shows current month and year heading and highlights current date on load | Dashboard page is open and Calendar block is visible | 1. Observe the Calendar block monthly view heading<br>2. Observe the calendar grid for the current date cell | The monthly view heading shows the current month and year and the current date cell is highlighted | High |
| 2.DASHBO-009 | Navigate to next month using the right arrow | Dashboard page is open and Calendar block is visible | 1. Click the right arrow in the Calendar block<br>2. Observe the monthly view heading | The monthly view advances and the heading updates to the next month and year | High |
| 2.DASHBO-010 | Navigate to previous month using the left arrow | Dashboard page is open and Calendar block is visible | 1. Click the left arrow in the Calendar block<br>2. Observe the monthly view heading | The monthly view moves to the previous month and the heading updates to the previous month and year | High |
| 2.DASHBO-011 | Navigate multiple months forward and back using left/right arrows | Dashboard page is open and Calendar block is visible | 1. Click the right arrow twice in the Calendar block<br>2. Observe the monthly view heading has advanced by two months<br>3. Click the left arrow twice in the Calendar block<br>4. Observe the monthly view heading has returned to the original month | Repeated arrow clicks navigate the monthly view forward and back by the expected number of months and the heading updates accordingly | High |
| 2.DASHBO-012 | Calendar monthly view displays current month and year heading | User is logged in and Dashboard page with Calendar block is visible | 1. Switch the Calendar block to monthly view if not already selected<br>2. Observe the Calendar block header | The Calendar block shows the current month and year as a heading | Medium |
| 2.DASHBO-013 | Calendar block shows monthly view with current month and year heading | Calendar block is visible on the Dashboard | 1. Inspect the Calendar block header in the monthly view | Calendar shows a monthly view and the header displays the current month and year. | Medium |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 2.DASHBO-014 | Selecting a time range with no items shows empty state | No upcoming teaching actions exist within the chosen time interval | 1. Select a time range from the Time Range dropdown that contains no upcoming items | The Timeline block displays the empty-state message or UI indicating no items. | Medium |
| 2.DASHBO-015 | Search term that yields no matches displays empty state | No upcoming teaching actions match the entered search term | 1. Enter a search term that matches no upcoming actions in the Search field and trigger the search | The Timeline block displays the empty-state message or UI indicating no items. | Medium |
| 2.DASHBO-016 | Submit new event with all required fields empty | User is logged in and Dashboard page with Calendar block is visible | 1. Click the "New event" button in the Dashboard Calendar block<br>2. Leave all required fields empty and click "Save" or "Create" in the event dialog | Validation errors shown for all required fields and no calendar entry is created | Medium |

#### Edge Case Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 2.DASHBO-017 | Current date not highlighted when viewing a different month | Dashboard page is open and Calendar block is visible showing the current month | 1. Click the right arrow in the Calendar block to move away from the current month<br>2. Observe the calendar grid for the original current date cell | The current date cell is not highlighted when the monthly view is not the current month | Medium |
| 2.DASHBO-018 | Combined time range and search producing no items shows empty state | No upcoming items satisfy both the selected time range and the entered search term | 1. Select a time range from the Time Range dropdown<br>2. Enter a search term in the Search field that together with the selected time range matches no items and trigger the search | The Timeline block displays the empty-state message or UI indicating no items. | Low |
| 2.DASHBO-019 | Selecting a course with no calendar events results in no inline event names displayed | Calendar block is visible on the Dashboard and at least one enrolled course has no calendar events | 1. Click the "All courses" dropdown<br>2. Select a course that has no calendar events | Monthly calendar displays with no dates showing event names (no inline event entries visible for the selected course). | Low |

---

### Dashboard — Edit Mode

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 3.D—EM-001 | Enable Edit mode shows Reset and Add a block controls | Dashboard page is open and Edit mode is disabled | 1. Click the "Edit mode" toggle | The "Reset page to default" button appears at the top right and the "+ Add a block" button appears below the Dashboard heading. | High |
| 3.D—EM-002 | Open Add a block page lists all available block types | Dashboard page is open and Edit mode is enabled | 1. Click the "+ Add a block" button | Add a block page opens and lists all available block types: Comments, Course overview, Latest announcements, Latest badges, Learning plans, Logged in user, Mentees, Online users, Private files, Random glossary entry, Recently accessed courses, Starred courses, Tags, Text, and Upcoming events. | High |
| 3.D—EM-003 | Cancel on Add a block returns to Dashboard without adding a block | Add a block page is open | 1. Click the "Cancel" link at the bottom of the Add a block page | User returns to the Dashboard and no new block is added. | High |
| 3.D—EM-004 | In Edit mode each existing block shows move icon and three-dot options | Dashboard page is open with at least one block and Edit mode is enabled | 1. For an existing block, verify the move icon and the three-dot options menu are visible | Each existing block displays a move icon and a three-dot options menu. | High |
| 3.D—EM-005 | Three-dot options menu provides configure, move, and delete actions | Dashboard page is open with at least one block and Edit mode is enabled | 1. Click the three-dot options menu on an existing block | The options menu lists configure, move, and delete actions. | High |
| 3.D—EM-006 | Reset page to default reverts persisted dashboard layout changes | Edit mode is toggled on and the user has previously made persisted dashboard layout changes | 1. Click "Reset page to default"<br>2. Verify the dashboard layout matches the module default and previously persisted layout changes are removed | Dashboard layout is restored to the module default and user-specific layout changes are undone. | High |
| 3.D—EM-007 | Layout changes persist per user after exiting Edit mode | Edit mode is toggled on | 1. Make a dashboard layout change in Edit mode (for example move or add a block)<br>2. Toggle Edit mode off<br>3. Verify the layout change remains visible on the dashboard | The dashboard retains the layout change after exiting Edit mode, demonstrating persistence per user. | High |
| 3.D—EM-008 | Move a block using three-dot options menu and persist position | Edit mode is enabled and at least two block locations are available | 1. Click the block's three-dot options menu<br>2. Click the "Move" option<br>3. Use the move controls to place the block in a different valid location and confirm the move<br>4. Reload the current page | Block appears in the new location and the position persists after reload. | High |
| 3.D—EM-009 | Delete a block via three-dot options menu and persist removal | Edit mode is enabled and the target block is present | 1. Click the block's three-dot options menu<br>2. Click the "Delete" option<br>3. Confirm deletion in the confirmation dialog<br>4. Reload the current page | Block is removed and the removal persists after reload. | High |
| 3.D—EM-010 | Move a block using the move icon in Edit mode | Edit mode is enabled and the target block is visible | 1. Use the block's move icon to reposition it to a different valid location on the page<br>2. Confirm the block appears in the new location | Block is relocated to the selected position immediately. | High |
| 3.D—EM-011 | Moved block persists after page refresh (per-user persistence) | Edit mode is enabled and the target block is visible | 1. Use the block's move icon to reposition it to a different valid location<br>2. Refresh the page<br>3. Verify the block remains in the new location | Block remains in the new position after page refresh. | High |
| 3.D—EM-012 | Reset page to default reverts moved block to original position | Edit mode is enabled and the target block has been moved | 1. Click "Reset page to default"<br>2. Confirm the page layout reverts to default and the block returns to its original position | Layout is fully reverted to default and the moved block returns to its original position. | High |
| 3.D—EM-014 | Edit mode shows Reset page to default and Add a block controls | None | 1. Toggle Edit mode on<br>2. Verify the "Reset page to default" button appears at the top right and the "+ Add a block" button appears below the Dashboard heading | Both the "Reset page to default" and "+ Add a block" controls are visible when Edit mode is on. | Medium |
| 3.D—EM-015 | Open block configuration via three-dot options menu in Edit mode | Edit mode is enabled and a block is visible | 1. Click the block's three-dot options menu<br>2. Click the "Configure" option | Block configuration panel or dialog is displayed allowing edits. | Medium |
| 3.D—EM-016 | Block displays move icon and three-dot menu contains configure, move, delete in Edit mode | Edit mode is enabled and the block is visible | 1. Verify the block shows a visible move icon<br>2. Open the block's three-dot options menu and verify it lists configure, move, and delete actions | Move icon is visible and the options menu lists configure, move, and delete. | Medium |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 3.D—EM-017 | Attempt to open Add a block when Edit mode is disabled | Dashboard page is open with Edit mode disabled | 1. Verify the "+ Add a block" button is not present below the Dashboard heading | The "+ Add a block" button is not available when Edit mode is disabled. | Medium |
| 3.D—EM-018 | Reset action unavailable when Edit mode is not enabled | Edit mode is toggled off | 1. Verify the "Reset page to default" button is not present on the page | The "Reset page to default" control is not visible and cannot be invoked when Edit mode is off. | Medium |
| 3.D—EM-019 | Three-dot options menu not available when Edit mode is disabled | Edit mode is disabled and a block is visible | 1. Observe the action area of a visible block for the move icon and three-dot options menu<br>2. Attempt to open the three-dot options menu if present | Move icon and three-dot options menu are not present or do not open; block-level configure/move/delete actions are not accessible. | Medium |
| 3.D—EM-020 | Move icon not present when Edit mode is disabled | Edit mode is disabled | 1. Ensure Edit mode is not enabled<br>2. Verify no move icon is displayed on any block | Move icons are not displayed on blocks and the move action is unavailable. | Medium |

#### Edge Case Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 3.D—EM-013 | Multiple block-level layout changes via three-dot menu persist per user | Edit mode is enabled and multiple blocks are visible | 1. Use the first block's three-dot options menu to move it to a different valid location and confirm the move<br>2. Use a second block's three-dot options menu to delete that block and confirm deletion<br>3. Reload the current page | All layout changes made via the three-dot options menu are persisted for the user (moved block remains in new location and deleted block remains absent). | High |
| 3.D—EM-021 | Disable Edit mode hides Reset/Add controls and editing handles | Dashboard page is open with Edit mode enabled and blocks visible | 1. Click the "Edit mode" toggle to disable Edit mode | The "Reset page to default" button and the "+ Add a block" button are no longer visible and move icons and three-dot options menus are hidden on blocks. | Medium |
| 3.D—EM-022 | Reset page to default when no layout changes made leaves dashboard unchanged | Edit mode is toggled on and no dashboard layout changes have been made | 1. Click "Reset page to default"<br>2. Verify the dashboard layout remains equivalent to the module default and no errors are shown | Reset completes successfully and the dashboard remains at the module default with no errors. | Low |
| 3.D—EM-023 | Multiple block moves reverted by Reset page to default | Edit mode is enabled and multiple blocks are visible | 1. Use move icons to reposition multiple blocks to different locations<br>2. Click "Reset page to default"<br>3. Verify the page layout and all moved blocks return to default positions | Reset page to default fully reverts the layout changes and all blocks return to their default positions. | Low |

---

### My Courses

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 4.MYCOU-001 | Star a course from the three-dot menu pins it to the top | Teacher is logged in and My Courses page is open with multiple course cards visible | 1. Open the three-dot menu on a specific course card<br>2. Click "Star this course"<br>3. Verify the selected course card appears as the first card in the My Courses list | The selected course is pinned to the top of the My Courses list. | High |
| 4.MYCOU-002 | Remove a course from view via the three-dot menu hides it from My Courses | Teacher is logged in and My Courses page is open with the target course card visible | 1. Open the three-dot menu on the target course card<br>2. Click "Remove from view"<br>3. Verify the course card no longer appears in the My Courses list | The selected course is hidden from the My Courses page without affecting enrollment. | High |
| 4.MYCOU-003 | My Courses displays all courses the teacher has access to as visual cards | Teacher is logged in and My Courses page is open | 1. Observe the course listing area on the My Courses page<br>2. Verify each course the teacher has access to is represented as a visual card (banner, name, category) | The My Courses page displays all courses the teacher has access to as visual cards. | High |
| 4.MYCOU-004 | Controls above course grid are present | None | 1. On the My Courses page, observe the controls above the course grid<br>2. Verify the status dropdown, search field, sort dropdown, and layout dropdown are visible | Status dropdown, search field, sort dropdown, and layout dropdown are present above the course grid. | High |
| 4.MYCOU-005 | Filter courses using status dropdown: All | Teacher has multiple courses across different statuses (In progress, Future, Past, Starred, Hidden). | 1. Open the status dropdown and select the 'All' option<br>2. Verify the displayed course cards include courses from all statuses and each card shows a banner image, a clickable course name, and the category name | Course grid displays all courses the teacher has access to; each card shows banner image, clickable course name, and category name. | High |
| 4.MYCOU-006 | Filter courses using status dropdown: In progress | Teacher has at least one course in 'In progress' status. | 1. Open the status dropdown and select the 'In progress' option<br>2. Verify only courses in 'In progress' status are shown and each displayed card shows a banner image, a clickable course name, and the category name | Course grid shows only 'In progress' courses; each card displays banner image, clickable course name, and category name. | High |
| 4.MYCOU-007 | Filter courses using status dropdown: Future | Teacher has at least one course in 'Future' status. | 1. Open the status dropdown and select the 'Future' option<br>2. Verify only courses in 'Future' status are shown and each displayed card shows a banner image, a clickable course name, and the category name | Course grid shows only 'Future' courses; each card displays banner image, clickable course name, and category name. | High |
| 4.MYCOU-008 | Filter courses using status dropdown: Past | Teacher has at least one course in 'Past' status. | 1. Open the status dropdown and select the 'Past' option<br>2. Verify only courses in 'Past' status are shown and each displayed card shows a banner image, a clickable course name, and the category name | Course grid shows only 'Past' courses; each card displays banner image, clickable course name, and category name. | High |
| 4.MYCOU-009 | Filter courses using status dropdown: Starred | Teacher has at least one starred course. | 1. Open the status dropdown and select the 'Starred' option<br>2. Verify only starred courses are shown and each displayed card shows a banner image, a clickable course name, and the category name | Course grid shows only starred courses; each card displays banner image, clickable course name, and category name. | High |
| 4.MYCOU-010 | Filter courses using status dropdown: Hidden | Teacher has at least one hidden course. | 1. Open the status dropdown and select the 'Hidden' option<br>2. Verify only hidden courses are shown and each displayed card shows a banner image, a clickable course name, and the category name | Course grid shows only hidden courses; each card displays banner image, clickable course name, and category name. | High |
| 4.MYCOU-011 | Search returns matching course cards | My Courses page is open | 1. Fill the search field with a term that matches a course name or category<br>2. Trigger the search action (press Enter or click search) | Grid displays only course cards that match the search term; each displayed card shows the course banner image, the course name as a clickable link, and the category name | High |
| 4.MYCOU-012 | Search with empty input shows all teacher-accessible courses | My Courses page is open | 1. Clear or leave the search field empty<br>2. Trigger the search action (press Enter or click search) | The My Courses page displays all courses the teacher has access to as visual cards | High |
| 4.MYCOU-013 | Sort courses using the sort dropdown updates course ordering | My Courses page is open and multiple course cards are visible | 1. Select a sort option different from the current selection from the sort dropdown<br>2. Wait for the course grid to refresh<br>3. Verify the order of visible course cards has changed to reflect the selected sort criterion | Course cards reorder according to the selected sort criterion | High |
| 4.MYCOU-014 | Default Card layout shows courses as visual cards with banner, name link, and category | User is on the My Courses page as a teacher | 1. Ensure the layout dropdown is set to Card<br>2. Verify the My Courses page displays courses as visual cards and each course card shows the course banner image, course name as a clickable link, and the category name | All teacher-accessible courses are displayed as cards and each card includes a banner image, clickable course name, and category name | High |
| 4.MYCOU-015 | Switch to List layout displays courses in list view while preserving course name link and category | User is on the My Courses page as a teacher | 1. Open the layout dropdown and select List<br>2. Verify the course listing updates to list view and each listed item shows the course name as a clickable link and the category name | Course list view is displayed and course name links and category names remain visible for each course | High |
| 4.MYCOU-016 | Switch to Summary layout displays courses in summary view while preserving course name link and category | User is on the My Courses page as a teacher | 1. Open the layout dropdown and select Summary<br>2. Verify the course listing updates to summary view and each item shows the course name as a clickable link and the category name | Course summary view is displayed and course name links and category names remain visible for each course | High |
| 4.MYCOU-017 | Clicking a course name navigates to that course's main page (triggerable from: Card, List, Summary) | User is on the My Courses page as a teacher and at least one course is listed | 1. Click a course name link from the current layout<br>2. Verify the application opens the clicked course's main page | Clicking the course name navigates to the course's main page | High |
| 4.MYCOU-018 | Three-dot menu lists Star this course and Remove from view options | Teacher is logged in and My Courses page is open with at least one course card visible | 1. Open the three-dot menu on a course card<br>2. Verify the menu contains the "Star this course" option and the "Remove from view" option | The three-dot menu presents both "Star this course" and "Remove from view" actions. | Medium |
| 4.MYCOU-019 | Course card displays banner image, clickable name, and category name | Teacher is logged in and My Courses page is open with at least one course card visible | 1. Inspect a course card<br>2. Verify it shows a course banner image, the course name as a clickable link, and the category name | Each course card displays a banner image, the course name as a clickable link, and the category name. | Medium |
| 4.MYCOU-020 | Search field present among four controls above the grid | My Courses page is open | 1. Verify the four controls appear above the grid: status dropdown, search field, sort dropdown, and layout dropdown | All four controls are present and visible above the courses grid | Medium |
| 4.MYCOU-021 | Sort dropdown control is present among the page controls above the grid | My Courses page is open | 1. Verify four controls appear above the grid: status dropdown, search field, sort dropdown, and layout dropdown | Status dropdown, search field, sort dropdown, and layout dropdown are visible above the course grid | Medium |
| 4.MYCOU-022 | Course card displays banner, clickable course name, and category | My Courses page is open and at least one course card is visible | 1. Inspect a visible course card and verify the banner image is present, the course name is a clickable link, and the category name is shown | Course card shows the banner image, course name as a clickable link, and the category name | Medium |
| 4.MYCOU-023 | Layout dropdown contains Card, List, Summary options | User is on the My Courses page as a teacher | 1. Verify four controls appear above the grid (status dropdown, search field, sort dropdown, layout dropdown)<br>2. Open the layout dropdown | Layout dropdown lists the options Card, List, and Summary | Medium |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 4.MYCOU-024 | Sorting when the teacher has no accessible courses results in no course cards shown | My Courses page is open and the teacher has no accessible courses | 1. Select any option from the sort dropdown<br>2. Verify the page shows no course cards and no sorting errors are displayed | No course cards are shown and the page handles sorting without error | Medium |

#### Edge Case Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 4.MYCOU-025 | Star an already pinned course does not create duplicate entries and remains at top | Teacher is logged in and My Courses page is open with the course already pinned to the top | 1. Open the three-dot menu on the already-pinned course card<br>2. Click "Star this course"<br>3. Verify the course remains the first card in the My Courses list and no duplicate card is created | Re-starring an already pinned course does not duplicate the course card and the course stays pinned to the top. | Medium |
| 4.MYCOU-026 | Selecting the currently active sort option leaves course ordering unchanged | My Courses page is open with multiple course cards visible | 1. Record the current order of visible course cards<br>2. Select the same (currently active) option from the sort dropdown<br>3. Verify the order of course cards remains the same | The order of course cards remains unchanged after re-selecting the active sort option | Low |

---

### Course Page

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 5.COUPAG-001 | Collapse all collapses every section and hides their contents | Course page displays multiple expanded sections with visible contents. | 1. Click the "Collapse all" link<br>2. Verify every section's content becomes hidden and each section chevron reflects the collapsed state | All sections are collapsed, their contents are hidden, and chevrons show the collapsed state. | High |
| 5.COUPAG-002 | Expand a collapsed section reveals its activities and resources | Course page is open and the target section is collapsed and contains activities/resources. | 1. Click the target section's collapsible chevron | The section expands and the activities/resources are visible, each showing a type icon and a clickable name. | High |
| 5.COUPAG-003 | Collapse an expanded section hides its activities and resources | Course page is open and the target section is expanded and its activities/resources are visible. | 1. Click the target section's collapsible chevron | The section collapses and the activities/resources are hidden from view. | High |
| 5.COUPAG-004 | Clicking a section's chevron toggles only that section (other sections unchanged) | Course page is open with at least two sections in different expanded/collapsed states. | 1. Click the collapsible chevron for the target section | Only the target section changes state (expanded ↔ collapsed); other sections retain their previous state. | High |
| 5.COUPAG-005 | Collapse all link is visible at the top right of the Course page | Course page is open with sections displayed. | 1. Locate the "Collapse all" link at the top right of the sections area<br>2. Verify the link is visible and enabled | The "Collapse all" link is visible and enabled. | Medium |
| 5.COUPAG-006 | Course sections display a collapsible chevron and section name | Course page displays multiple sections in the main content area. | 1. For each visible section, inspect the section header<br>2. Verify a collapsible chevron is present and the section name text is displayed | Each section header shows a collapsible chevron and its section name. | Medium |

#### Edge Case Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 5.COUPAG-007 | Collapse all collapses all sections when some are already collapsed | Course page has at least one expanded section and at least one collapsed section. | 1. Click the "Collapse all" link<br>2. Verify every section is now collapsed and section contents are hidden | All sections become collapsed and their contents are hidden. | Medium |
| 5.COUPAG-008 | Collapse all leaves sections collapsed when they are already collapsed | Course page has all sections already collapsed. | 1. Click the "Collapse all" link<br>2. Verify sections remain collapsed and no errors or unexpected UI changes occur | Sections remain collapsed and the UI remains stable with no errors. | Low |
| 5.COUPAG-009 | Toggle a section twice returns it to the original state | Course page is open and the target section is in a known collapsed or expanded state. | 1. Click the target section's collapsible chevron<br>2. Click the same section's collapsible chevron again | After two consecutive clicks the section returns to its original state (collapsed if originally collapsed, expanded if originally expanded). | Low |

---

### Course Edit Mode and Activity Chooser

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 6.CEMAC-001 | Enable Edit mode shows authoring interface and inline controls | Course page is open and user has authoring permissions | 1. Click the "Edit mode" toggle to enable Edit mode<br>2. Observe the course page content area | Course page turns into an authoring interface and inline authoring controls appear on sections and activities. | High |
| 6.CEMAC-002 | Disable Edit mode hides authoring controls and returns to normal view | Edit mode is currently enabled on the Course page | 1. Click the "Edit mode" toggle to disable Edit mode<br>2. Observe the course page content area | Inline and authoring controls are removed and the course page returns to non-authoring view. | High |
| 6.CEMAC-003 | Inline edit icon performs quick renaming for a section or activity | Edit mode is enabled and at least one section or activity is visible | 1. Click the inline edit icon for a section or activity<br>2. Change the title to a valid new title and save the change | The section or activity title is updated to the new value and the change is reflected on the page. | High |
| 6.CEMAC-004 | Bulk actions toolbar appears when multiple activities are selected | Edit mode is enabled and multiple activities are visible | 1. Select multiple activities using the row selection controls<br>2. Observe the page for the bulk actions toolbar | Bulk actions toolbar appears allowing batch operations on the selected activities. | High |
| 6.CEMAC-005 | '+ Add an activity or resource' opens the Activity Chooser modal | Edit mode is enabled and a section bottom is visible | 1. Click the "+ Add an activity or resource" button at the bottom of a section<br>2. Observe the resulting UI | The Activity Chooser modal opens. | High |
| 6.CEMAC-006 | Inline controls visible on section and activity rows in Edit mode | Course Edit mode is active and the course page with sections is open. | 1. Locate a section row and an activity row on the page<br>2. Verify each row displays inline controls (edit icon, section-level three-dot menu, and + Add a subsection where applicable) | Each section and activity row displays the inline controls. | High |
| 6.CEMAC-007 | Quick rename a section using the edit icon | Course Edit mode is active and the target section row is visible. | 1. Click the section's edit icon<br>2. Enter a new section title and confirm/save the change | Section title is updated to the new value. | High |
| 6.CEMAC-008 | Duplicate a section via the section-level three-dot menu | Course Edit mode is active and the target section row is visible. | 1. Click the section-level three-dot menu on the target section<br>2. Click the Duplicate option and confirm if a confirmation appears | A duplicate of the section is created and appears in the section list or Course Index. | High |
| 6.CEMAC-009 | Delete a section via the section-level three-dot menu | Course Edit mode is active and the target section row is visible. | 1. Click the section-level three-dot menu on the target section<br>2. Click the Delete option and confirm deletion in the confirmation dialog | The section is removed and no longer appears in the section list. | High |
| 6.CEMAC-010 | Move a section to a new position via the section-level three-dot menu | Course Edit mode is active and the target section row is visible. | 1. Click the section-level three-dot menu on the target section<br>2. Click the Move option, select the new position, and confirm the move | The section order updates and the section appears in the selected new position. | High |
| 6.CEMAC-011 | Add a subsection and nest it under the parent section | Course Edit mode is active and the + Add a subsection control is visible on a section. | 1. Click the + Add a subsection control on the parent section<br>2. Fill required fields (subsection title and any required details) and click Save/Add | The new subsection appears nested under the parent section in the Course Index. | High |
| 6.CEMAC-012 | Inline controls visible on activity rows in Edit mode | Course page is open and Edit mode is enabled | 1. Locate an activity row on the course page<br>2. Inspect the activity row for inline controls (three-dot menu and edit icon) | Inline controls (three-dot menu and edit icon) are visible on the activity row | High |
| 6.CEMAC-013 | Quick rename an activity using the inline edit icon | Course page is open and Edit mode is enabled | 1. Click the inline edit icon on an activity row<br>2. Fill the inline title field with a new valid title and confirm the change | Activity title is updated in the activity row | High |
| 6.CEMAC-014 | Open activity settings via activity-level three-dot menu | Course page is open and Edit mode is enabled | 1. Click the activity-level three-dot menu on an activity row<br>2. Click the "Edit settings" action in the menu | The activity settings form or page for that activity is displayed | High |
| 6.CEMAC-015 | Move an activity to a different section via three-dot menu | Course page is open and Edit mode is enabled | 1. Click the activity-level three-dot menu on an activity row<br>2. Select the "Move" action, choose a target section, and confirm the move | Activity appears under the selected target section in the course listing | High |
| 6.CEMAC-016 | Duplicate an activity via activity-level three-dot menu | Course page is open and Edit mode is enabled | 1. Click the activity-level three-dot menu on an activity row<br>2. Click the "Duplicate" action and confirm duplication | A duplicate of the activity appears in the course activity listing | High |
| 6.CEMAC-017 | Delete an activity using the activity-level three-dot menu | Course page is open and Edit mode is enabled | 1. Click the activity-level three-dot menu on an activity row<br>2. Click the "Delete" action and confirm deletion in the confirmation dialog | Activity is removed and no longer appears in the course activity listing | High |
| 6.CEMAC-018 | Perform a bulk operation on multiple selected activities | Edit mode is enabled on the course page and multiple activities are visible | 1. Select multiple activities using the inline selection controls on their rows<br>2. Click a bulk action in the bulk actions toolbar<br>3. Complete any confirmation or secondary inputs and confirm the bulk action | The chosen bulk operation is applied to all selected activities and the changes are reflected in the course listing and Course Index. | High |
| 6.CEMAC-019 | Move multiple selected activities to another section using bulk actions | Edit mode is enabled on the course page and at least two course sections exist | 1. Select multiple activities using the inline selection controls (can be from one or more source sections)<br>2. Click the 'Move' bulk action in the bulk actions toolbar, choose a destination section, and confirm the move | All selected activities are relocated to the chosen destination section and the Course Index updates to reflect the new hierarchy. | High |
| 6.CEMAC-020 | Open Activity Chooser and verify UI elements | None | 1. Click "+ Add an activity or resource"<br>2. Verify the Activity Chooser modal contains a category filter bar (All, Activities, Resources, Recommended), a search field, and a grid of activity/resource tiles | Activity Chooser modal opens and displays the filter bar, search field, and a grid including tiles such as Assignment, Forum, Quiz, File, Page, Lesson, SCORM, URL, Workshop; each tile shows a star/favorite toggle. | High |
| 6.CEMAC-021 | Select an activity via category filter and open its creation form | None | 1. Click "+ Add an activity or resource"<br>2. Click the category filter 'Activities' and select an activity tile from the grid<br>3. Click "Add" | The selected activity's creation form opens. | High |
| 6.CEMAC-022 | Search for an activity and open its creation form | None | 1. Click "+ Add an activity or resource"<br>2. Enter a matching term in the Activity Chooser search field and select the matching activity tile from the results<br>3. Click "Add" | The selected activity's creation form opens. | High |
| 6.CEMAC-023 | Section-level three-dot menu lists expected actions | Edit mode is enabled and a section row is visible | 1. Click the section-level three-dot menu for a section<br>2. Inspect the list of menu options | Menu lists the actions: edit, duplicate, hide, delete, and move. | Medium |
| 6.CEMAC-024 | Activity-level three-dot menu lists expected actions | Edit mode is enabled and at least one activity row is visible | 1. Click the activity-level three-dot menu for an activity<br>2. Inspect the list of menu options | Menu lists the actions: edit settings, move, duplicate, hide, set access restrictions, and delete. | Medium |
| 6.CEMAC-025 | '+ Add a subsection' control creates a nested subsection | Edit mode is enabled and a section is visible | 1. Click the "+ Add a subsection" control for a section<br>2. Fill any required subsection fields and confirm creation | A new subsection is created and displayed nested under the parent section. | Medium |
| 6.CEMAC-026 | Section-level three-dot menu lists edit, duplicate, hide, delete, move | Course Edit mode is active and a section row's three-dot menu is visible. | 1. Click the section-level three-dot menu on a section row<br>2. Verify the menu contains the options: edit, duplicate, hide, delete, move | The three-dot menu lists edit, duplicate, hide, delete, and move. | Medium |
| 6.CEMAC-027 | Hide a section via the section-level three-dot menu | Course Edit mode is active and the target section row is visible. | 1. Click the section-level three-dot menu on the target section<br>2. Click the Hide option | The section is marked as hidden (visually indicated) in the edit view. | Medium |
| 6.CEMAC-028 | Activity-level three-dot menu lists expected actions | Course page is open and Edit mode is enabled | 1. Click the activity-level three-dot menu for an activity row<br>2. Verify the menu lists the expected action items | Menu contains the actions: edit settings, move, duplicate, hide, set access restrictions, and delete | Medium |
| 6.CEMAC-029 | Hide an activity using the activity-level three-dot menu | Course page is open and Edit mode is enabled | 1. Click the activity-level three-dot menu on an activity row<br>2. Click the "Hide" action and confirm the hide operation | Activity is marked or displayed as hidden in the course activity listing | Medium |
| 6.CEMAC-030 | Set access restrictions for an activity via three-dot menu | Course page is open and Edit mode is enabled | 1. Click the activity-level three-dot menu on an activity row<br>2. Select "Set access restrictions", configure at least one restriction, and save | Access restriction configuration is saved and the activity shows the applied restriction state | Medium |
| 6.CEMAC-031 | Bulk actions toolbar appears after selecting multiple activities | Edit mode is enabled on the course page and multiple activities are visible | 1. Select multiple activities using the inline selection controls on their rows<br>2. Observe the bulk actions toolbar area | Bulk actions toolbar becomes visible and presents available batch operations. | Medium |
| 6.CEMAC-032 | Inline controls appear on section and activity rows in Edit mode | Edit mode is enabled on the course page | 1. Inspect the section rows on the course page<br>2. Inspect the activity rows on the course page and verify inline controls are present on each row | Each section and activity row displays inline controls for editing and selection. | Medium |
| 6.CEMAC-033 | Favorite a tile then select it and click Add to open creation form | None | 1. Click "+ Add an activity or resource"<br>2. Toggle the star/favorite on an activity/resource tile, then select that same tile<br>3. Click "Add" | The selected favorited activity's creation form opens. | Medium |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 6.CEMAC-034 | Activity Chooser modal opens only when using '+ Add an activity or resource' in Edit mode | Edit mode is disabled and the Course page is visible | 1. Attempt to locate or click a "+ Add an activity or resource" button at the bottom of a section<br>2. If the control is present, attempt to click it and observe the UI | The "+ Add an activity or resource" control is not available or, if not available, the Activity Chooser does not open. | Medium |
| 6.CEMAC-035 | Add a subsection with all required fields empty | Course Edit mode is active and the + Add a subsection control is visible on a section. | 1. Click the + Add a subsection control on the parent section<br>2. Leave all required fields empty<br>3. Click Save/Add | Validation errors shown for all required fields. | Medium |
| 6.CEMAC-036 | Attempt to select an action not listed in the activity three-dot menu | Course page is open and Edit mode is enabled | 1. Click the activity-level three-dot menu on an activity row<br>2. Search the menu for an action that is not part of the expected set | The unlisted action is not present in the menu | Medium |
| 6.CEMAC-037 | Attempt bulk action with no activities selected | Edit mode is enabled on the course page | 1. Ensure no activities are selected<br>2. Attempt to open or invoke the bulk actions toolbar or a bulk action | Bulk actions cannot be performed: the bulk actions toolbar does not appear or its actions are disabled when nothing is selected. | Medium |
| 6.CEMAC-038 | Submit with all required fields empty | None | 1. Leave all required selections empty (do not select any activity/resource tile)<br>2. Click "Add" | Validation errors shown for all required selections and the activity creation form does not open. | Medium |

#### Edge Case Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 6.CEMAC-039 | Toggling Edit mode repeatedly remains consistent with last toggle state | Course page is open and user has authoring permissions | 1. Toggle Edit mode on and off repeatedly in quick succession using the Edit mode control<br>2. After the final toggle, observe whether inline authoring controls are present or absent | UI remains stable and the course page reflects the expected authoring interface state corresponding to the final toggle position. | Low |
| 6.CEMAC-040 | Attempt quick rename with an empty title using the inline edit icon | Course page is open and Edit mode is enabled | 1. Click the inline edit icon on an activity row<br>2. Clear the inline title field and attempt to confirm/save the empty title | Rename is blocked or a validation error is displayed preventing empty activity title | Low |
| 6.CEMAC-041 | Selecting a single activity does not enable batch-only bulk operations | Edit mode is enabled on the course page and at least one activity is visible | 1. Select a single activity using the inline selection control on its row<br>2. Observe whether the bulk actions toolbar appears or whether batch-only actions are enabled | Bulk actions toolbar remains unavailable or batch-only actions are disabled when only one activity is selected. | Low |

---

### Assignment Creation

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 7.ASSCRE-001 | Create assignment and return to course with required fields | None | 1. Fill all required fields (Assignment name)<br>2. Click "Save and return to course" | The assignment is created and the instructor is redirected to the course page; the new assignment appears in the course listing. | High |
| 7.ASSCRE-002 | Create assignment with File submissions enabled and file constraints configured | None | 1. Fill all required fields (Assignment name)<br>2. Enable File submissions and fill additional controls (maximum number of uploaded files, maximum submission size, accepted file types)<br>3. Click "Save and return to course" | The assignment is created with file submission settings saved and the instructor is redirected to the course page; the assignment summary reflects file submission configuration. | High |
| 7.ASSCRE-003 | Create assignment and open its page (Save and display) | None | 1. Fill all required fields (Assignment name) and any desired optional fields (Description, Additional files, submission settings, grading settings)<br>2. Click "Save and display" | The assignment is created and the new assignment's page opens; the assignment appears in the course and the Course Index highlights the newly active item. | High |
| 7.ASSCRE-004 | Cancel discards unsaved assignment changes and closes the creation form | Assignment creation form is open | 1. Fill all editable fields in the assignment creation form with valid values (Title, Description, Due date, attachments/settings as applicable)<br>2. Click "Cancel" | Assignment creation form is closed and none of the entered changes are saved; no new assignment is created in the course. | High |
| 7.ASSCRE-006 | Enable File submissions reveals file constraint controls | Assignment creation form is open | 1. Fill all required fields (Assignment name)<br>2. Enable File submissions | Controls for maximum number of uploaded files, maximum submission size, and accepted file types become visible. | Medium |
| 7.ASSCRE-007 | Save and return with all submission date toggles disabled | None | 1. Fill all required fields (Assignment name)<br>2. Ensure Allow submissions from, Due date, and Cut-off date Enable toggles are disabled<br>3. Click "Save and return to course" | The assignment is created and the instructor is redirected to the course page; the saved assignment shows no enabled submission dates. | Medium |
| 7.ASSCRE-008 | '+ Add restriction' opens restriction-type picker | Assignment creation form is open | 1. Click the "+ Add restriction" button | A restriction-type picker dialog or panel opens. | Medium |
| 7.ASSCRE-009 | Enabling File submissions reveals file submission controls | None | 1. In Submission types, check "File submissions"<br>2. Verify additional controls for maximum number of uploaded files, maximum submission size, and accepted file types are visible<br>3. Fill those file submission controls with valid values | File-specific controls become visible when File submissions is enabled and accept input. | Medium |
| 7.ASSCRE-013 | Collapsible panels expand and collapse | Assignment creation form is open | 1. Identify a collapsible panel on the form<br>2. Collapse the panel, then expand the panel | The panel collapses and expands as expected, showing and hiding its fields. | Low |
| 7.ASSCRE-014 | Form panels collapse and expand | None | 1. Collapse a collapsible panel in the assignment form<br>2. Expand the same collapsible panel | Panels collapse and expand as expected, showing and hiding their contained fields. | Low |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 7.ASSCRE-005 | Submit with Assignment name empty | None | 1. Fill all other required fields, leave Assignment name empty<br>2. Click "Save and return to course" | Validation error indicating the Assignment name is required. | High |
| 7.ASSCRE-010 | Submit with all required fields empty | None | 1. Leave all required fields empty<br>2. Click "Save and return to course" | Validation errors shown for all required fields. | Medium |
| 7.ASSCRE-011 | Submit with all required fields empty | None | 1. Leave all required fields empty<br>2. Click "Save and display" | Validation errors shown for all required fields. | Medium |

#### Edge Case Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 7.ASSCRE-012 | Reopening the creation form after Cancel shows no previously entered data | Assignment creation form is open | 1. Fill all editable fields in the assignment creation form with valid values<br>2. Click "Cancel"<br>3. Click the control to open the assignment creation form again | Creation form opens with fields in their default/empty state and previous edits are not retained. | Medium |
| 7.ASSCRE-015 | Disabled date toggles exclude date from enforcement | None | 1. Fill all required fields (Assignment name), ensure the Due date toggle is disabled and the Due date date/time picker is empty<br>2. Click "Save and display" | Assignment is created successfully and the new assignment's page shows no enforced due date. | Low |

---

### Course Settings

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 8.COUSET-001 | Save and display persists valid course settings and returns to course page | Course settings form is open | 1. Fill all required fields (Course full name, Course short name, Course category) and other optional settings (visibility, start date, end date toggle and date if desired, Course ID number, Course summary, Course image, Course format, appearance settings, language, news items, activity dates, completion conditions display, Maximum upload size, Completion tracking, group mode and grouping, Tags)<br>2. Click "Save and display" | The configuration is persisted and the user is returned to the course page; the course page displays the saved values (including format, visibility, summary and image). | High |
| 8.COUSET-002 | Selecting a course format exposes layout controls and the selection is saved | Course settings form is open | 1. Select a Course format that has layout controls, adjust the layout controls as appropriate, and fill all required fields (Course full name, Course short name, Course category)<br>2. Click "Save and display" | Chosen Course format and its layout control settings are persisted and the course page reflects the selected format and layout. | High |
| 8.COUSET-003 | Cancel discards unsaved edits and preserves existing settings | Course Settings form is open and populated with current settings. | 1. Modify multiple editable fields in the Course Settings form<br>2. Click "Cancel" | Changes are not persisted and the course settings remain unchanged. | High |
| 8.COUSET-004 | Cancel button is visible and enabled on Course Settings form | Course Settings form is open. | 1. Verify the 'Cancel' button is visible on the Course Settings form<br>2. Verify the 'Cancel' button is enabled and can be clicked | 'Cancel' button is present and clickable. | Medium |
| 8.COUSET-008 | Cancel with no changes returns without altering settings | Course Settings form is open and populated with current settings. | 1. Leave all fields as-is on the Course Settings form<br>2. Click "Cancel" | No changes are made and the original course settings remain unchanged. | Low |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 8.COUSET-005 | Submit with all required fields empty | Course settings form is open | 1. Leave all required fields empty<br>2. Click "Save and display" | Validation errors shown for all required fields. | Medium |
| 8.COUSET-006 | Format-specific validation produces inline error when format controls are invalid or missing | Course settings form is open | 1. Fill all general required fields (Course full name, Course short name, Course category), select a Course format that requires additional layout input, leave the format-specific layout control empty or set an invalid layout option<br>2. Click "Save and display" | An inline validation error is shown for the format-specific control and the settings are not saved. | Medium |

#### Edge Case Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 8.COUSET-007 | Enable end date toggle persists end date when enabled and remains unset when disabled | Course settings form is open | 1. Enable the Course end date toggle and set a valid end date, fill all required fields (Course full name, Course short name, Course category)<br>2. Click "Save and display" | The course end date and its enabled state are persisted and the course page reflects the enabled end date; if the toggle is disabled the end date is not applied. | Medium |

---

### Participants Management

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 9.PARMAN-001 | Filter participants by enrollment scope | Participants page is open and participants list is visible | 1. Select an enrollment context from the enrolled-users scope dropdown<br>2. Click Apply filters | Participants list updates to show only users in the selected enrollment context | High |
| 9.PARMAN-002 | Filter participants by attribute condition | Participants page is open and participants list is visible | 1. Set Select attribute dropdown to a chosen attribute and configure its matching value via the + Add condition link<br>2. Click Apply filters | Participants list shows users matching the configured attribute condition | High |
| 9.PARMAN-003 | Filter participants by enrollment scope and attribute condition | Participants page is open and participants list is visible | 1. Select an enrollment context from the enrolled-users scope dropdown<br>2. Add and configure an attribute condition using Select attribute and + Add condition<br>3. Click Apply filters | Participants list shows users matching both the selected enrollment scope and the attribute condition | High |
| 9.PARMAN-004 | Clear filters resets all filter controls and listing | Participants page is open and participants list is visible | 1. Apply an enrollment scope filter and an alphabetical filter<br>2. Click Clear filters | All filter controls are cleared and the full participants list is displayed | High |
| 9.PARMAN-005 | Open Enrol users dialog and verify fields present | Participants management page is open | 1. Click the "Enrol users" button<br>2. Observe the enrollment dialog and its contained controls | Enrollment dialog is displayed and contains a user search field, a Role dropdown, and an optional Enrollment duration control. | High |
| 9.PARMAN-006 | Enrol a user using required fields only (no enrollment duration) | Participants management page is open | 1. Click the "Enrol users" button<br>2. Fill all required fields (locate and select the user in the user search field, choose a role from the Role dropdown)<br>3. Click the enrollment confirm button | User is added to the course with the selected role and appears in the participants list. | High |
| 9.PARMAN-007 | Enrol a user with an enrollment duration specified | Participants management page is open | 1. Click the "Enrol users" button<br>2. Fill all required fields (locate and select the user in the user search field, choose a role from the Role dropdown) and set the Enrollment duration control to a valid duration<br>3. Click the enrollment confirm button | User is added to the course with the selected role and the enrollment shows the specified duration in the participants listing or enrollment details. | High |
| 9.PARMAN-008 | View participant profile via row three-dot action menu | Participants list is visible with participant rows | 1. Click the three-dot action menu on a participant's row<br>2. Click the "View profile" option | Participant's profile view opens and displays the participant's details. | High |
| 9.PARMAN-009 | View participant profile via First/Last name link | Participants list is visible with participant rows | 1. Click the participant's First or Last name link in the row | Participant's profile view opens and displays the participant's details. | High |
| 9.PARMAN-010 | Edit a participant's role via row three-dot action menu | Participants list is visible with participant rows and user has permission to edit roles | 1. Click the three-dot action menu on a participant's row<br>2. Click the "Edit role" option<br>3. Modify the role selection and click "Save" or "Confirm" | Participant's role is updated and the change is reflected in the participants listing or profile. | High |
| 9.PARMAN-011 | Send a message to a participant via row three-dot action menu | Participants list is visible with participant rows and messaging is available | 1. Click the three-dot action menu on a participant's row<br>2. Click the "Send a message" option<br>3. Fill the message content and click "Send" | Message is sent; confirmation is shown and the message appears in the messaging history or drawer. | High |
| 9.PARMAN-012 | Apply a bulk action to multiple selected participants | Participant list with multiple participants and row checkboxes is visible | 1. Select multiple participants using their row checkboxes<br>2. Open the "With selected users…" dropdown and choose a bulk action<br>3. Confirm the bulk action if a confirmation appears | The chosen bulk action is applied to all selected participants and the UI shows a success message or the participant listing reflects the changes. | High |
| 9.PARMAN-013 | Filter participants by First name initial | Participants page is open and participants list is visible | 1. Click a letter button in the First name alphabetical filter<br>2. Click Apply filters | Participants list is reduced to users whose first name starts with the selected letter | Medium |
| 9.PARMAN-014 | Filter participants by Last name initial | Participants page is open and participants list is visible | 1. Click a letter button in the Last name alphabetical filter<br>2. Click Apply filters | Participants list is reduced to users whose last name starts with the selected letter | Medium |
| 9.PARMAN-015 | Filter participants by combined First and Last name initials | Participants page is open and participants list is visible | 1. Click a letter button in the First name alphabetical filter<br>2. Click a letter button in the Last name alphabetical filter<br>3. Click Apply filters | Participants list shows users whose first and last names match the selected initials | Medium |
| 9.PARMAN-016 | Three-dot action menu composition lists expected options | Participants list is visible with participant rows | 1. Click the three-dot action menu on any participant row<br>2. Verify the menu lists the options for viewing profile, editing role, and sending a message | The three-dot action menu contains options to view profile, edit role, and send a message. | Medium |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 9.PARMAN-017 | Submit enrollment with all required fields empty | Participants management page is open | 1. Leave all required fields empty<br>2. Click the enrollment confirm button | Validation errors shown for all required fields. | Medium |
| 9.PARMAN-018 | Attempt action when a row's three-dot menu is missing an expected option | Participants list is visible with participant rows | 1. Click the three-dot action menu on a participant's row<br>2. If an expected option (view profile / edit role / send a message) is not present, attempt the same action via the participant's name link where applicable | When an expected menu option is missing the action cannot be performed via the menu; the participant name link still opens the profile when used as a fallback. | Medium |
| 9.PARMAN-019 | Attempt to apply a bulk action with no participants selected | Participant list is visible | 1. Ensure no participant checkboxes are checked<br>2. Open the "With selected users…" dropdown and choose a bulk action<br>3. Confirm the bulk action if a confirmation appears | The system prevents the action or shows an error/notification indicating that no participants were selected. | Medium |

#### Edge Case Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 9.PARMAN-020 | Verify bulk action applies only to checked participants | Participant list with at least three participants and row checkboxes is visible | 1. Select two participants using their row checkboxes and leave at least one participant unchecked<br>2. Open the "With selected users…" dropdown and choose a bulk action<br>3. Confirm the bulk action if a confirmation appears | The bulk action is applied only to the checked participants; unchecked participants remain unaffected. | Medium |
| 9.PARMAN-021 | Selecting All in First name alphabetical filter shows unfiltered results | Participants page is open and participants list is visible | 1. Click the All button in the First name alphabetical filter<br>2. Click Apply filters | Participants list is displayed without first-name initial filtering | Low |
| 9.PARMAN-022 | Applying an enrollment scope that has no enrolled users displays empty results | Participants page is open and participants list is visible | 1. Select an enrollment context expected to have no enrolled users from the enrolled-users scope dropdown<br>2. Click Apply filters | Participants list shows no results and the page displays the empty-state for participants | Low |
| 9.PARMAN-023 | Three-dot action menu is present on each participant row | Participants list is visible with multiple participant rows | 1. For multiple participant rows, click the three-dot action menu on each row<br>2. Observe whether the menu opens and displays options for each row | A three-dot action menu is present and opens for each participant row, displaying the expected options. | Low |

---

### Assignment — Teacher View

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 10.A—TV-001 | Assignment metadata displays opened date, due date, description, and attachments | Assignment page (teacher view) is open | 1. Observe the Assignment page metadata area<br>2. Verify Opened date and Due date are displayed and the full Description is visible including any attached files<br>3. Click an attached file listed in the Description | Opened date, Due date and full Description are visible and attached files open or download when clicked | High |
| 10.A—TV-002 | Grade button opens the grading interface for individual students | Assignment page (teacher view) is open | 1. Locate the Grade button in the assignment header or actions area<br>2. Click the Grade button | The grading interface for individual students opens | High |
| 10.A—TV-003 | Grading summary panel shows expected read-only metrics | Assignment page (teacher view) is open | 1. Locate the Grading summary panel on the Assignment page<br>2. Observe that the panel displays Number of participants, Number of submissions, Needs grading, Visibility, and Time remaining | The Grading summary panel displays all listed metrics | Medium |
| 10.A—TV-004 | Tab bar provides navigation to Assignment, Settings, Submissions, Advanced grading, and More | Assignment page (teacher view) is open and the Grading summary panel is visible | 1. Locate the tab bar below the Grading summary panel<br>2. Click each named tab (Assignment, Settings, Submissions, Advanced grading, More) and observe the resulting panel or content area | Each tab opens its corresponding content area; tabs for Assignment, Settings, Submissions, Advanced grading, and More are present and functional | Medium |
| 10.A—TV-005 | Breadcrumbs show full navigation path with clickable segments | An activity detail (Assignment) page is open | 1. Observe the breadcrumbs at the top of the activity page showing the navigation path from the course<br>2. Click a breadcrumb segment | Breadcrumbs display the full navigation path and clicking a segment navigates to the corresponding page | Medium |
| 10.A—TV-006 | Course Index sidebar expand/collapse, active highlight, and close behavior | Course page containing the Assignment is open and the Course Index sidebar is visible | 1. Use a section's expand/collapse arrow in the Course Index sidebar to expand and collapse its child items<br>2. Observe that the currently active item is highlighted in the tree<br>3. Click the sidebar close button (X) | Sections expand and collapse as expected, the active item is highlighted, and clicking the close button hides the Course Index sidebar | Medium |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 10.A—TV-007 | Attempting to modify grading summary metrics is not permitted | Assignment page (teacher view) is open and the Grading summary panel is visible | 1. Attempt to edit or change the displayed value for each metric in the Grading summary panel (Number of participants, Number of submissions, Needs grading, Visibility, Time remaining)<br>2. Attempt to save or persist any change to those metrics | The metrics cannot be edited or changed; values remain unchanged and no save is possible | Medium |

---

### Assignment Submissions

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 11.ASSSUB-001 | Filter submissions by student name | Submissions table is visible and contains multiple student records. | 1. Enter a student's name or partial name in the search control<br>2. Click the "Apply filters" control or press Enter | Table rows are narrowed to show only submissions whose student name matches the search; non-matching rows are hidden. | High |
| 11.ASSSUB-002 | Filter submissions by submission status | Submissions table is visible and contains records with different submission statuses. | 1. Select a submission status from the submission status dropdown<br>2. Click the "Apply filters" control | Table shows only submissions with the selected submission status; other rows are hidden. | High |
| 11.ASSSUB-003 | Filter submissions by grading status | Submissions table is visible and contains records with different grading statuses. | 1. Select a grading status from the grading status dropdown<br>2. Click the "Apply filters" control | Table shows only submissions with the selected grading status; other rows are hidden. | High |
| 11.ASSSUB-004 | Filter submissions using combined student name, submission status, and grading status | Submissions table is visible and contains records covering multiple students, submission statuses, and grading statuses. | 1. Enter a student's name or partial name in the search control and select a submission status and a grading status<br>2. Click the "Apply filters" control | Table is narrowed to rows that match all provided criteria (student name AND submission status AND grading status). | High |
| 11.ASSSUB-005 | Enable Quick grading mode enables inline grade editing in submissions table | Submissions view is open and at least one student submission row is visible. | 1. Click the "Quick grading" toggle/control to enable Quick grading mode<br>2. Observe the submissions table and interact with a grade cell | Grade cells in the submissions table become inline-editable inputs, allowing direct grade entry. | High |
| 11.ASSSUB-006 | Enable Quick grading and enter a Final grade inline | Teacher is viewing the assignment submissions table and at least one student submission row is visible | 1. Enable Quick grading mode<br>2. Click the Final grade cell for a student, enter a valid grade, and commit the change (press Enter or click outside the cell) | The entered grade appears in the Final grade column for that student and is retained in the table after editing | High |
| 11.ASSSUB-007 | Edit an existing Final grade inline while Quick grading enabled | Teacher is viewing the assignment submissions table with Quick grading enabled and a submission has an existing Final grade | 1. Click the existing Final grade cell for that student, modify the grade value, and commit the change | The Final grade column updates to show the modified grade for that student | High |
| 11.ASSSUB-008 | Open grading workflow from a submission row's action menu and verify student mapping | Submissions table displays at least one student submission row. | 1. Click the action menu for a chosen student's submission row<br>2. Select the option to open the grading workflow from the action menu<br>3. Verify the grading workflow header shows the same student name as the selected submission row and the student's submission is displayed | Grading workflow opens for the selected student and displays that student's submission and identity. | High |
| 11.ASSSUB-010 | Student name and initials icon open the student's profile | Submissions table is visible with at least one student row containing a name and initials icon. | 1. Click the student's name or initials icon in a table row | The student's profile opens (profile page or profile modal) for the selected student. | Medium |
| 11.ASSSUB-011 | Submissions table displays expected submission and grading status values | Submissions table is visible and contains records with varied statuses. | 1. Observe the submission status and grading status columns in the submissions table | Submission status column displays values such as 'Submitted for grading', 'No submission', 'Draft — not submitted'; Grading status column displays 'Graded' and 'Not graded'. | Medium |
| 11.ASSSUB-012 | Disable Quick grading mode returns submissions table to non-editable state | Quick grading mode is currently enabled and the submissions table is visible. | 1. Click the "Quick grading" toggle/control to disable Quick grading mode<br>2. Observe the submissions table and attempt to interact with a grade cell | Grade cells are no longer inline-editable and display read-only values. | Medium |
| 11.ASSSUB-013 | Final grade column is visible in the submissions table | Teacher is viewing the assignment submissions table | 1. Verify that the Final grade column header is present in the submissions table | The Final grade column header and corresponding cells are visible for each submission row | Medium |
| 11.ASSSUB-014 | Student identity column displays name and initials icon in submissions table | Submissions table is visible with at least one submission row. | 1. Inspect the student identity column for a sample submission row<br>2. Verify the row displays the student's name and an initials icon | Student name and initials icon are shown in the student identity column. | Medium |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 11.ASSSUB-009 | Action menu opens grading workflow for a different student (incorrect mapping) | At least two student submission rows are visible. | 1. Note the student name shown in a target submission row<br>2. Click that row's action menu and select the option to open the grading workflow<br>3. Observe the student name shown in the opened grading workflow header | The grading workflow opens but shows a different student than the selected submission row (incorrect mapping). | High |
| 11.ASSSUB-015 | Apply filters with all filter fields empty | Submissions table is visible and contains multiple records. | 1. Leave all search and filter controls empty or unselected<br>2. Click the "Apply filters" control | No narrowing occurs; the submissions table remains unfiltered and all submission records remain visible. | Medium |
| 11.ASSSUB-016 | Inline grade entry is not available when Quick grading mode is not enabled | Teacher is viewing the assignment submissions table with Quick grading disabled | 1. Attempt to activate inline editing by clicking the Final grade cell for a student | Inline edit control does not appear and the Final grade cell remains read-only | Medium |
| 11.ASSSUB-018 | Enable Quick grading mode when no submission records are present | Submissions view is open and shows no student submission rows. | 1. Click the "Quick grading" toggle/control to enable Quick grading mode<br>2. Observe the submissions table area for inline grade inputs | No inline grade inputs appear because there are no submission records to edit. | Low |

#### Edge Case Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 11.ASSSUB-017 | Open grading workflow from action menu when student identity displays only initials icon | Submissions table includes at least one row where the student identity displays an initials icon alongside or instead of the full name. | 1. Identify a submission row that shows the student's initials icon in the identity column<br>2. Click that row's action menu and select the option to open the grading workflow<br>3. Verify the grading workflow opens and the student identity in the workflow corresponds to the selected row | Grading workflow opens for the student represented by the initials icon and shows the corresponding student identity. | Medium |
| 11.ASSSUB-019 | No results displayed when filters match no submissions | Submissions table is visible and contains multiple records. | 1. Enter a search string and/or select submission and grading status combinations that match no records<br>2. Click the "Apply filters" control | The table shows a 'no results' message or an empty result set indicating no matching submissions. | Low |
| 11.ASSSUB-020 | Toggle Quick grading mode on, off, and on preserves inline editability | Submissions view is open and at least one student submission row is visible. | 1. Click the "Quick grading" toggle to enable Quick grading mode<br>2. Click the "Quick grading" toggle to disable Quick grading mode<br>3. Click the "Quick grading" toggle to enable Quick grading mode again | After re-enabling, grade cells are inline-editable again and behave as before. | Low |
| 11.ASSSUB-021 | Disabling Quick grading removes inline edit controls | Teacher is viewing the assignment submissions table with Quick grading enabled | 1. Disable Quick grading mode<br>2. Attempt to edit a Final grade cell for a student | Final grade cells are no longer editable and inline edit controls are not available | Low |

---

### Gradebook — Grader Report

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 12.G—GR-001 | Narrow grade rows by student name using User search | Gradebook Grader report page is open and the grade table with enrolled students and activities is visible. | 1. Enter a student name or partial name into the User search control<br>2. Click the control to apply the search/filter | Grade table rows are filtered to show only students matching the search; the table still displays activities as columns. | High |
| 12.G—GR-002 | Narrow grade rows by selecting a group using the group filter control | Gradebook Grader report page is open and the grade table with enrolled students and activities is visible. | 1. Select a group from the group filter control<br>2. Click the control to apply the filters | Grade table rows are filtered to show only students in the selected group and the table displays activities as columns. | High |
| 12.G—GR-003 | Open per-column action menu and open Edit grade settings dialog | Grader Report is open and the grade table is populated with activities and enrolled students. | 1. Click the per-column action menu on any activity column header<br>2. Click "Edit grade settings" in the menu | The Edit grade settings dialog opens for the selected activity column. | High |
| 12.G—GR-004 | Edit an activity's grade settings via per-column action menu and save | Grader Report is open and the grade table is populated with activities and enrolled students. | 1. Click the per-column action menu on an activity column header<br>2. Click "Edit grade settings"<br>3. Modify one or more editable fields in the grade settings form<br>4. Click "Save" | The grade settings are saved and the activity column reflects the updated settings. | High |
| 12.G—GR-005 | Grade table displays activities as columns and enrolled students as rows | Grader Report is open and the grade table is populated with activities and enrolled students. | 1. Locate the grade table on the page<br>2. Inspect the table headers and rows to identify their mapping | Each column header corresponds to an activity and each row corresponds to an enrolled student. | High |
| 12.G—GR-006 | Edit a single student's grade via per-cell three-dot menu | Grader report page is open and user has teacher permissions. | 1. Open the per-cell three-dot menu for a specific student and activity grade cell<br>2. Click the "Edit" action, change the grade value and any optional comment, then click "Save" | The targeted grade cell updates to the new value, the change persists in the grade table, and no other cells are modified. | High |
| 12.G—GR-007 | Enable Edit mode and save a valid grade edit updates grade and class average | Grader report is open with at least one activity and an enrolled student | 1. Click "Edit mode" to enable inline editing<br>2. Edit one or more grade cells with values within the configured grade range<br>3. Click "Save changes" | Edits are applied to the grade table and the overall average row updates to reflect the new class averages. | High |
| 12.G—GR-009 | Per-column action menu is available on each activity column header | Grader Report is open and the grade table is populated with multiple activity columns. | 1. For several activity column headers, click the per-column action menu on each header<br>2. Observe whether the menu opens for each clicked header | The per-column action menu opens for each activity column header clicked. | Medium |
| 12.G—GR-010 | Grade table displays activities as columns and enrolled students as rows | Grader report page is open. | 1. Inspect the grade table header and body on the grader report page | The grade table displays activities as columns and enrolled students as rows. | Medium |
| 12.G—GR-011 | Grade table displays activities as columns, students as rows, and shows overall average row | Grader report is open with at least one activity and enrolled students | 1. Observe the grade table on the page | The grade table displays activities as columns, enrolled students as rows, and an overall average row is shown at the bottom. | Medium |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 12.G—GR-008 | Entering an out-of-range grade flags the cell and blocks saving | Grader report is open with a known configured grade range | 1. Click "Edit mode" to enable inline editing<br>2. Enter a value outside the configured grade range into a grade cell<br>3. Click "Save changes" | The out-of-range cell is flagged inline and the save action is blocked; edits are not applied. | High |
| 12.G—GR-012 | Apply filters with all search and filter fields empty | Gradebook Grader report page is open and the grade table with enrolled students and activities is visible. | 1. Leave the User search and group filter controls empty or cleared<br>2. Click the control to apply the filters | Validation errors shown for all required fields. | Medium |
| 12.G—GR-013 | Attempt to save Edit grade settings with all required fields empty | Grader Report is open and the grade table is populated with activities and enrolled students. | 1. Click the per-column action menu on an activity column header<br>2. Click "Edit grade settings"<br>3. Leave all required fields in the edit form empty<br>4. Click "Save" | Validation errors are shown for required fields and the changes are not saved. | Medium |
| 12.G—GR-014 | Attempt to save an empty grade via per-cell edit | Grader report page is open and user has teacher permissions. | 1. Open the per-cell three-dot menu for a specific grade cell<br>2. Click "Edit", clear the grade input so it is empty, then click "Save" | Save is rejected and a validation error is shown; the original grade remains unchanged. | Medium |
| 12.G—GR-015 | Out-of-range grade shows inline validation flag on blur | Grader report is open with a known configured grade range | 1. Click "Edit mode" to enable inline editing<br>2. Enter a value outside the configured grade range into a grade cell and move focus away from the cell | The edited cell displays an inline validation flag or message indicating the value is outside the configured range. | Medium |

#### Edge Case Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 12.G—GR-016 | Save changes is blocked when multiple edits include at least one out-of-range value | Grader report is open and Edit mode is enabled | 1. Edit multiple grade cells with valid values and at least one cell with a value outside the configured grade range<br>2. Click "Save changes" | Save is prevented, no edits are applied, and the out-of-range cell(s) are flagged inline. | Medium |

---

### Profile

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 13.PROFIL-001 | Profile header displays initials, full name, Message button and description (when present) | Profile description is present for the teacher. | 1. On the Profile page, observe the header area containing the teacher identity<br>2. Verify the circular initials icon, the full name text, and the Message button are visible<br>3. Verify the profile description text is visible in the header area | Header shows the circular initials icon, full name, Message button, and the profile description. | High |
| 13.PROFIL-002 | User details card shows email, visibility note, timezone, and Edit profile link | None | 1. Locate the User details information card on the Profile page<br>2. Verify the email address, visibility note, timezone, and an Edit profile link are present in the card | User details card displays email address, visibility note, timezone, and an Edit profile link. | High |
| 13.PROFIL-003 | Edit profile updates are saved and reflected on Profile page | User has permission to edit the profile. | 1. Click the Edit profile link<br>2. Modify one or more editable profile fields (for example name, description or timezone)<br>3. Click Save<br>4. Verify the Profile page reflects the updated values | Profile page shows the saved updates and the modified fields reflect the new values. | High |
| 13.PROFIL-004 | Login activity shows First and Last access with exact dates and relative time indicators | None | 1. Locate the Login activity section on the Profile page<br>2. Verify the First access entry shows an exact date and a relative time indicator<br>3. Verify the Last access entry shows an exact date and a relative time indicator | Login activity displays First and Last access with exact dates and relative time indicators. | High |
| 13.PROFIL-005 | Privacy and policies card contains Data retention summary link | None | 1. Locate the Privacy and policies card on the Profile page<br>2. Click the Data retention summary link and verify the Data retention summary is displayed | Data retention summary is displayed after clicking the Data retention summary link. | Medium |
| 13.PROFIL-006 | Course details card lists links to associated course profiles and opens a course profile | Teacher is associated with at least one course. | 1. Locate the Course details card on the Profile page<br>2. Verify links to associated course profiles are listed in the card<br>3. Click one associated course profile link and verify the corresponding course profile content is displayed | Course details card lists links to associated course profiles and clicking a link opens the respective course profile. | Medium |
| 13.PROFIL-007 | Miscellaneous card links navigate to respective content lists (Blog entries, Forum posts, Forum discussions, Learning plans) | None | 1. Locate the Miscellaneous card on the Profile page and verify links for Blog entries, Forum posts, Forum discussions, and Learning plans are present<br>2. Click each link and verify the corresponding content list or page is displayed for that link | Each Miscellaneous link navigates to and displays its respective content list or page. | Medium |
| 13.PROFIL-008 | Reports card contains Browser sessions and Grades overview links that open respective reports | None | 1. Locate the Reports card on the Profile page and verify Browser sessions and Grades overview links are present<br>2. Click the Browser sessions link and verify the browser sessions report is displayed, then click the Grades overview link and verify the grades overview is displayed | Browser sessions and Grades overview links open the corresponding report pages or views. | Medium |

#### Edge Case Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 13.PROFIL-009 | Profile page displays core header elements when description is absent | Profile description is not set for the teacher. | 1. On the Profile page, observe the header area containing the teacher identity<br>2. Verify the circular initials icon, the full name text, and the Message button are visible and no profile description is shown | Profile page displays the circular initials icon, full name, and Message button while no profile description is present. | Low |

---

### Profile Edit

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 14.PROEDI-001 | Update profile with valid field changes and file upload | User is on the Edit profile page | 1. Fill all required fields (First name, Last name, Email address) and modify other editable fields (City/town, Country, Timezone, Description)<br>2. Upload a valid image file in the New picture upload area and fill the Picture description field<br>3. Click "Update profile" | Profile page refreshes and displays the updated field values and the newly uploaded user picture. | High |
| 14.PROEDI-002 | Update profile using drag-and-drop picture upload | User is on the Edit profile page | 1. Fill all required fields (First name, Last name, Email address) and other necessary fields<br>2. Drag-and-drop a valid image file into the New picture upload area<br>3. Click "Update profile" | Profile page refreshes and the dragged-and-dropped picture is shown as the user picture. | High |
| 14.PROEDI-003 | Cancel discards edited text fields and returns to profile view | Profile Edit form is open. | 1. Fill editable text fields with new values (First name, Last name, Email address, City/town, Country, Timezone)<br>2. Modify the Description field with plain text<br>3. Click "Cancel" | Edit form closes and profile view displays the original text values (no edits were saved). | High |
| 14.PROEDI-005 | Edit optional name formats, interests, and site-defined custom fields and save | User is on the Edit profile page | 1. Fill all required fields (First name, Last name, Email address)<br>2. Fill Additional names optional fields, add one or more Interests tags, and complete any site-defined fields under Optional fields<br>3. Click "Update profile" | Profile page refreshes and the updated additional names, interests, and custom optional fields are displayed. | Medium |
| 14.PROEDI-006 | User picture area shows the current picture on the Edit profile page | User is on the Edit profile page | 1. Observe the User picture area on the Edit profile page | User picture area displays the current picture. | Medium |
| 14.PROEDI-011 | Expand all collapsible sections to reveal all profile fields | User is on the Edit profile page | 1. Click the "Expand all" link<br>2. Verify collapsible sections (General, Optional, Additional names) are expanded and fields are visible | All collapsible sections are expanded and their fields are visible. | Low |
| 14.PROEDI-012 | Click Cancel with no changes returns to profile view unchanged | Profile Edit form is open with no unsaved changes. | 1. Click "Cancel" | Edit form closes and profile view remains unchanged. | Low |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 14.PROEDI-007 | Submit with all required fields empty | User is on the Edit profile page | 1. Leave all required fields empty<br>2. Click "Update profile" | Validation errors shown for all required fields. | Medium |
| 14.PROEDI-008 | Attempt to save with an invalid picture upload | User is on the Edit profile page | 1. Fill all required fields (First name, Last name, Email address) with valid values<br>2. Attempt to upload an invalid picture file that violates upload constraints in the New picture upload area<br>3. Click "Update profile" | Upload validation error is shown and the profile is not saved. | Medium |

#### Edge Case Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 14.PROEDI-004 | Cancel after uploading a new user picture discards the uploaded image | Profile Edit form is open and a current user picture is displayed. | 1. Use the New picture upload area to upload a valid image file (drag-and-drop or file select)<br>2. Click "Cancel" | Edit form closes and profile view continues to display the original user picture (the uploaded image was not saved). | High |
| 14.PROEDI-009 | Cancel discards rich-text Description formatting and content changes | Profile Edit form is open and Description has existing content. | 1. Edit the Description rich text editor with formatted content (apply bold/italic and add new text)<br>2. Click "Cancel" | Edit form closes and profile view displays the original Description content and formatting (no new content or formatting saved). | Medium |
| 14.PROEDI-010 | Cancel discards added Interests tags | Profile Edit form is open and Interests field exists. | 1. Add one or more tags to the Interests field<br>2. Click "Cancel" | Edit form closes and profile view shows the original Interests tags (new tags were not saved). | Medium |

---

### Logout

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 15.LOGOUT-001 | Log out terminates session and redirects to login page | User is authenticated and on any protected page | 1. Click the user's initials in the top navigation to open the user menu<br>2. Click "Log out" | The user session is terminated and the application redirects to the login page. | High |
| 15.LOGOUT-002 | Logout from user menu terminates session and shows login page | User is logged in | 1. Click the user initials circular icon in the top navigation to open the user menu.<br>2. Click the Log out option in the user menu.<br>3. Observe the resulting page to confirm the session ended and the login page is displayed. | The session is terminated and the application displays the login page; authenticated content is no longer accessible without signing in again. | High |
| 15.LOGOUT-003 | Protected routes inaccessible after logout | User has just logged out after an active session | 1. After completing logout, attempt to navigate directly to a protected page (for example, Course Page or Dashboard) by entering its URL or clicking a saved link.<br>2. Verify the application prevents access to the protected content by redirecting to the login page or otherwise denying access. | Attempting to access a protected route after logout results in a redirect to the login page or an access denial; protected content is not shown. | High |
| 15.LOGOUT-004 | Browser refresh after logout does not restore authenticated session | User has just logged out | 1. Immediately after logging out, refresh the browser (reload the current page).<br>2. Confirm that the page remains on the login screen and no authenticated or user-specific content reappears. | Refreshing the browser after logout does not restore the authenticated session; the user remains logged out and only the login page or unauthenticated content is visible. | High |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 15.LOGOUT-005 | Accessing a protected page after logout requires re-authentication | User is authenticated and a protected page is open | 1. Click the user's initials in the top navigation to open the user menu<br>2. Click "Log out"<br>3. Use the browser Back button or attempt to load a protected page URL | The login page is shown and access to the protected page is denied until the user re-authenticates. | High |

#### Edge Case Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 15.LOGOUT-006 | Logout in one tab prevents access to protected pages in other open tabs | User is authenticated with the application open in multiple browser tabs | 1. In one tab, click the user's initials in the top navigation to open the user menu and click "Log out"<br>2. Switch to another open tab with a protected page and attempt to interact with or refresh the page | The other tab requires the user to re-authenticate before accessing protected content. | Medium |

---

## Navigation Graph

![Navigation Graph](Output/MoodleTeacher/navigation_graph.png)

### Pages

| Module | URL | Test Cases |
|--------|-----|------------|
| Login | /login | 9 |
| Dashboard | /my | 19 |
| Dashboard — Edit Mode | /my?edit=1 | 23 |
| My Courses | /my/courses | 26 |
| Course Page | /course/view.php | 9 |
| Course Edit Mode and Activity Chooser | /course/edit.php | 41 |
| Assignment Creation | /mod/assign/edit.php | 15 |
| Course Settings | /course/settings.php | 8 |
| Participants Management | /user/index.php | 23 |
| Assignment — Teacher View | /mod/assign/view.php | 7 |
| Assignment Submissions | /mod/assign/submissions.php | 21 |
| Gradebook — Grader Report | /grade/report/grader/index.php | 16 |
| Profile | /user/profile.php | 9 |
| Profile Edit | /user/edit.php | 12 |
| Logout | /login/logout.php | 6 |
