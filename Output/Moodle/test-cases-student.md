# Moodlestudent

**Base URL:** 
**Generated:** 2026-04-20T20:50:45.722331

## Summary

| Metric | Count |
|--------|-------|
| **Total Tests** | 152 |

### By Type

| Type | Count |
|------|-------|
| Positive | 103 |
| Negative | 25 |
| Edge Case | 24 |
| Standard | 0 |

### By Priority

| Priority | Count |
|----------|-------|
| High | 84 |
| Medium | 56 |
| Low | 12 |

---

## Test Cases

### Login

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 1.LOGIN-001 | Login with valid credentials | None | 1. Fill all required fields (Username, Password) with valid credentials<br>2. Click "Log in" | Valid credentials redirect the student to the Dashboard. | High |
| 1.LOGIN-002 | Access as a guest offers unauthenticated browsing | None | 1. Click "Access as a guest" | Access as a guest offers unauthenticated browsing. | Medium |
| 1.LOGIN-008 | Cookies notice displays cookie usage information | None | 1. Verify Cookies notice is visible and contains cookie usage information<br>2. If a dismiss control is present, optionally dismiss the notice | Cookies notice provides cookie usage information. | Low |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 1.LOGIN-003 | Submit with all required fields empty | None | 1. Leave all required fields empty<br>2. Click "Log in" | Inline error message is shown; password field is cleared; username retained for correction. | Medium |
| 1.LOGIN-004 | Submit with Username field empty | None | 1. Fill all other required fields, leave Username empty<br>2. Click "Log in" | Validation error indicating Username is required; password field is cleared. | Medium |
| 1.LOGIN-005 | Submit with Password field empty | None | 1. Fill all other required fields, leave Password empty<br>2. Click "Log in" | Validation error indicating Password is required; password field is cleared; username retained for correction. | Medium |
| 1.LOGIN-006 | Login with invalid credentials | None | 1. Fill all required fields (Username with existing account identifier, Password with incorrect value)<br>2. Click "Log in" | Inline error message is shown; password field is cleared; username retained for correction. | Medium |

#### Edge Case Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 1.LOGIN-007 | Lost password? link is disabled on test site | None | 1. Verify the "Lost password?" link is present and attempt to activate it (click it to confirm no navigation) | The "Lost password?" link is disabled on the test site and does not navigate. | Medium |

---

### Dashboard

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 2.DASHBO-001 | Update Timeline when a time range is selected | Timeline block is visible on the Dashboard and the user is enrolled in at least one course | 1. Select a time range from the time range dropdown<br>2. Observe the Timeline block update | Timeline displays activities and deadlines that fall within the selected time range. | High |
| 2.DASHBO-002 | Timeline aggregates activities across all enrolled courses for selected time range | User is enrolled in multiple courses and at least one enrolled course has upcoming activities within the selected time range | 1. Select a time range from the time range dropdown<br>2. Verify the Timeline lists activities from each enrolled course that have items in the selected range | Timeline shows upcoming activities and deadlines from all enrolled courses that fall within the selected time range. | High |
| 2.DASHBO-003 | Timeline updates when switching between different time ranges | Timeline block is visible and there are activities present in at least one selectable time range | 1. Select a first time range from the time range dropdown and note the displayed Timeline items<br>2. Select a different time range from the time range dropdown<br>3. Observe the Timeline block update to reflect the newly selected range | Timeline updates to show activities corresponding to the newly selected time range (or shows the empty state if none exist). | High |
| 2.DASHBO-004 | Change sort order updates Timeline order | User is on Dashboard with Timeline block visible and multiple upcoming items present. | 1. Open the sort order dropdown in the Timeline block<br>2. Select a different sort order option<br>3. Verify the Timeline items are reordered according to the selected sort order | Timeline items reorder to reflect the chosen sort order. | High |
| 2.DASHBO-005 | Changing sort order preserves activities from all enrolled courses in Timeline | User is on Dashboard with Timeline block visible and multiple upcoming items from different courses present. | 1. Open the sort order dropdown in the Timeline block<br>2. Select a different sort order option<br>3. Verify Timeline still lists upcoming activities and deadlines from multiple enrolled courses | Timeline remains populated with upcoming activities and deadlines across the user's enrolled courses and is ordered per the selected sort. | High |
| 2.DASHBO-006 | Search activities by name returns matching Timeline items | User is on Dashboard with the Timeline block visible and containing activities. | 1. Fill the search field with an activity name query<br>2. Click the Search button or press Enter | Timeline displays activities whose name matches the query. | High |
| 2.DASHBO-007 | Search activities by type returns matching Timeline items | User is on Dashboard with the Timeline block visible and containing activities of various types. | 1. Fill the search field with an activity type value<br>2. Click the Search button or press Enter | Timeline displays activities that match the specified type. | High |
| 2.DASHBO-008 | Filter calendar events by a specific course | Calendar block is visible in monthly view | 1. Select a specific course from the "All courses" dropdown | Calendar updates to show only events belonging to the selected course; the calendar heading shows the current month and year; dates with events display their names inline; the current date is highlighted. | High |
| 2.DASHBO-009 | Show events from all courses using the All courses option | Calendar block is visible in monthly view | 1. Select the "All courses" option from the "All courses" dropdown | Calendar displays events from all courses; the calendar heading shows the current month and year; dates with events display their names inline; the current date is highlighted. | High |
| 2.DASHBO-010 | Create a personal calendar entry via New event | User is signed in and Dashboard is visible. | 1. Click the Calendar block's "New event" button<br>2. Fill all required fields in the event form (event title and date, plus optional time if applicable)<br>3. Click the event form's Save/Submit button | A personal calendar entry is created and appears on its date in the Calendar block's monthly view. | High |
| 2.DASHBO-011 | Dates with events display their names inline in monthly view | A personal calendar event exists in the current month. | 1. Ensure the Calendar block shows the monthly view for the current month<br>2. Locate the date cell for the existing event and observe its contents | The event's name is displayed inline on the corresponding date in the monthly calendar view. | High |
| 2.DASHBO-012 | Calendar shows monthly view with current month and year heading | Dashboard is visible. | 1. Observe the Calendar block header | Calendar displays a monthly view with the current month and year as the heading. | High |
| 2.DASHBO-013 | Calendar displays current month and highlights current date | Dashboard page is open and the Calendar block is visible | 1. Observe the Calendar block heading<br>2. Observe the highlighted date for today in the calendar grid<br>3. Observe date cells that contain events and their inline event names | Calendar shows the current month and year in the heading, the current date is highlighted, and dates with events display their names inline. | High |
| 2.DASHBO-014 | Navigate to next month using right arrow | Dashboard page is open and the Calendar block is visible | 1. Click the Calendar block right arrow<br>2. Verify the month and year heading advances by one month<br>3. Verify the calendar grid updates and dates with events for the displayed month show their names inline | Calendar updates to the next month/year and displays the appropriate dates and inline event names for that month. | High |
| 2.DASHBO-015 | Navigate to previous month using left arrow | Dashboard page is open and the Calendar block is visible | 1. Click the Calendar block left arrow<br>2. Verify the month and year heading moves back by one month<br>3. Verify the calendar grid updates and dates with events for the displayed month show their names inline | Calendar updates to the previous month/year and displays the appropriate dates and inline event names for that month. | High |
| 2.DASHBO-016 | Toggle Edit mode on shows Reset page to default button | None | 1. Click the Edit mode toggle to turn editing on | A "Reset page to default" button appears at the top right of the page. | High |
| 2.DASHBO-017 | Toggle Edit mode on shows + Add a block and opens block types listing | None | 1. Click the Edit mode toggle to turn editing on<br>2. Click the "+ Add a block" button below the Dashboard heading | A page or panel listing all available block types is displayed. | High |
| 2.DASHBO-018 | Add a block via + Add a block listing | Dashboard is in Edit mode | 1. Click the "+ Add a block" button<br>2. Select a block type from the listing and confirm adding the block | The selected block is added to the Dashboard and appears on the page. | High |
| 2.DASHBO-019 | In Edit mode each block shows move icon and three-dot menu | Dashboard contains at least one existing block | 1. Click the Edit mode toggle to turn editing on | Each existing block shows a move icon and a three-dot menu for block actions. | High |
| 2.DASHBO-020 | Configure an existing block via three-dot menu | Dashboard contains at least one existing block and is in Edit mode | 1. For an existing block, click its three-dot menu<br>2. Click the "Configure" action in the menu | The block configuration interface (dialog or settings panel) opens for that block. | High |
| 2.DASHBO-021 | Delete an existing block via three-dot menu | Dashboard contains at least one existing block and is in Edit mode | 1. For an existing block, click its three-dot menu<br>2. Click the "Delete" action and confirm the deletion if prompted | The block is removed from the Dashboard and no longer appears on the page. | High |
| 2.DASHBO-022 | Move an existing block using the move icon | Dashboard contains at least two blocks and is in Edit mode | 1. Click and drag the move icon of a block to a different position on the page<br>2. Release to place the block in the new position | The block's position on the Dashboard updates to the new location. | High |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 2.DASHBO-023 | Timeline does not update after changing sort order (regression negative) | User is on Dashboard with Timeline block visible and multiple upcoming items present. | 1. Open the sort order dropdown in the Timeline block<br>2. Select a different sort order option<br>3. Observe whether the Timeline order changes | Timeline order fails to update and items remain in the previous order. | Medium |
| 2.DASHBO-024 | Submit with all required fields empty | User is on Dashboard with the Timeline block visible. | 1. Leave the search field empty<br>2. Click the Search button | Validation errors shown for all required fields. | Medium |
| 2.DASHBO-025 | Per-block edit controls are not visible when Edit mode is off | Edit mode is off | 1. Observe an existing block on the Dashboard | The block does not show a move icon or a three-dot menu for configure, move, or delete actions. | Medium |

#### Edge Case Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 2.DASHBO-026 | Selecting a time range with no activities shows the empty state | No activities exist within the selected time range across all enrolled courses | 1. Select a time range from the time range dropdown that contains no upcoming activities<br>2. Observe the Timeline block | The Timeline block displays its empty state indicating no activities in the selected range. | Medium |
| 2.DASHBO-027 | Search with non-matching query shows no results in Timeline | User is on Dashboard with the Timeline block visible and populated with activities. | 1. Fill the search field with a query that does not match any activity name or type<br>2. Click the Search button or press Enter | Timeline shows an empty results state indicating no activities found. | Medium |
| 2.DASHBO-028 | Filter to a course that has no events | A course with no calendar events exists | 1. Select the course that has no events from the "All courses" dropdown | Month view shows no event names for any dates (no events displayed); the calendar heading shows the current month and year; the current date remains highlighted. | Medium |
| 2.DASHBO-029 | Multiple personal events on the same date display their names inline | User is signed in and Dashboard is visible. | 1. Click the Calendar block's "New event" button; fill all required fields to create an event on a chosen date; click the event form's Save/Submit button<br>2. Repeat to create a second personal event on the same chosen date<br>3. Observe the date cell for that date in the monthly view | Both event names are displayed inline on that date in the monthly calendar view. | Medium |
| 2.DASHBO-030 | Navigate across year boundary using right arrow | Dashboard page is open and the Calendar block is visible | 1. If the month/year heading shows December, click the Calendar block right arrow once; otherwise click the Calendar block right arrow repeatedly until the heading shows January of the following year<br>2. Verify the month and year heading reflects the year transition<br>3. Verify the calendar grid updates and dates with events for the displayed month show their names inline | Month/year heading correctly transitions across the year boundary (December→January) and the calendar displays the dates and inline event names for the new month. | Medium |
| 2.DASHBO-031 | Current date is not highlighted when viewing a different month | Dashboard page is open and the Calendar block is visible | 1. Click the Calendar block left or right arrow to change the displayed month to one that is not the current month<br>2. Observe whether the calendar highlights the current date<br>3. Observe that dates with events for the displayed month show their names inline | When a month other than the current month is displayed, the current date is not highlighted and the calendar shows inline event names for the displayed month. | Medium |
| 2.DASHBO-032 | Change sort order when Timeline has a single upcoming item | User is on Dashboard with Timeline block visible and only one upcoming item present. | 1. Open the sort order dropdown in the Timeline block<br>2. Select any sort order option | Timeline remains unchanged with the single upcoming item still displayed. | Low |

---

### My Courses

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 3.MYCOU-001 | Star a course via the course card's three-dot menu pins it to the top | At least two courses are visible in the My Courses listing | 1. Open the three-dot menu on a non-starred course card<br>2. Click "Star this course" | The selected course is pinned and appears at the top of the My Courses list. | High |
| 3.MYCOU-002 | Filtering by Status = Starred shows pinned courses at the top | At least one course is already starred | 1. Open the status dropdown above the course grid and select "Starred" | The list is filtered to starred courses and the pinned course appears at the top of the filtered results. | High |
| 3.MYCOU-003 | Remove a course from view via course card menu and verify it appears under Hidden | My Courses page is open and the target course card is visible | 1. Open the course card's three-dot menu for the target course and click "Remove from view"<br>2. Set the status dropdown to "Hidden"<br>3. Verify the target course appears in the grid and that its course card shows a banner image, the course name as a clickable link, and the category name | The course is hidden from the default listing and appears under the Hidden status with the expected course card elements. | High |
| 3.MYCOU-004 | Course card displays banner image, clickable course name, and category name | At least one course card is visible in the course grid | 1. Inspect a course card in the course grid | The course card shows the course banner image, the course name as a clickable link, and the category name. | Medium |
| 3.MYCOU-005 | My Courses shows status dropdown, search field, sort dropdown, and layout dropdown above grid | The My Courses listing is visible | 1. Inspect the controls area above the course grid | Four controls are present above the grid: a status dropdown, a search field, a sort dropdown, and a layout dropdown. | Medium |
| 3.MYCOU-006 | Course card displays banner image, clickable course name, and category name | My Courses page is open and at least one course card is visible | 1. Inspect a course card in the grid<br>2. Verify the card shows a course banner image, the course name rendered as a clickable link, and the category name | Each course card displays the banner image, the course name as a clickable link, and the category name. | Medium |
| 3.MYCOU-007 | My Courses shows status dropdown, search field, sort dropdown, and layout dropdown above the grid | My Courses page is open | 1. Locate the controls above the course grid<br>2. Verify presence of the status dropdown, the search field, the sort dropdown, and the layout dropdown | All four controls (status dropdown, search field, sort dropdown, layout dropdown) are present above the course grid. | Medium |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 3.MYCOU-008 | Removed course is not visible in non-Hidden status listings | My Courses page is open and the target course card is visible | 1. Open the course card's three-dot menu for the target course and click "Remove from view"<br>2. Set the status dropdown to a non-Hidden option (e.g., "All" or "In progress")<br>3. Verify the target course is not visible in the grid for the selected non-Hidden status | The removed course does not appear in non-Hidden status listings. | Medium |

#### Edge Case Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 3.MYCOU-009 | Starring a second course pins the newly starred course above the previously starred course | At least two courses exist and one course is already starred | 1. Open the three-dot menu on a different non-starred course card<br>2. Click "Star this course" | The newly starred course is pinned to the top of the My Courses list, appearing above the previously starred course. | Medium |
| 3.MYCOU-010 | Status dropdown contains the expected options | The My Courses listing is visible | 1. Open the status dropdown and inspect the list of available options | The dropdown includes the options: All, In progress, Future, Past, Starred, and Hidden. | Medium |

---

### Course Page

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 4.COUPAG-001 | Collapse all collapses every section at once | Course page with multiple sections expanded and their contents visible | 1. Click the "Collapse all" link at the top right of the Course page<br>2. Verify every section's content area (activities and resources) is hidden | All sections are collapsed and their contents are not visible. | High |
| 4.COUPAG-002 | Collapsed sections hide activities and resources including type icons and names | Course page with sections containing activities and resources | 1. Click the "Collapse all" link at the top right<br>2. For each section, verify activity/resource rows are not visible and that type icons and clickable names are not displayed or interactable | Activities and resources (including their type icons and clickable names) are hidden and not interactable after collapsing. | High |
| 4.COUPAG-003 | Toggle a section collapsed then expanded using its chevron | Course page is open and the section contains at least one activity or resource. | 1. Click the section's collapsible chevron to collapse the section<br>2. Verify the section's activities and resources are hidden<br>3. Click the same section's collapsible chevron to expand the section<br>4. Verify the section's activities and resources are visible with type icons and clickable names | Section collapses to hide its activities and re-expands to show activities with type icons and clickable names. | High |
| 4.COUPAG-004 | Collapse one section without affecting other sections' expanded state | Course page is open with at least two sections visible and both expanded. | 1. Click the collapsible chevron for one section<br>2. Verify the clicked section's activities are hidden<br>3. Verify other section(s) remain in their previous visible/expanded state | Only the targeted section is collapsed; other sections retain their prior state. | High |
| 4.COUPAG-007 | Collapse all sets every section's collapsible chevron to collapsed state | Course page with multiple expanded sections that show a collapsible chevron per section | 1. Click the "Collapse all" link at the top right<br>2. Verify each section's collapsible chevron updates to indicate the collapsed state | All section chevrons show the collapsed indicator after using "Collapse all". | Medium |
| 4.COUPAG-008 | Collapse all preserves the currently highlighted active item in the Course Index | Course page with at least one section expanded and a currently active item highlighted in the Course Index sidebar | 1. Note the currently highlighted item in the Course Index sidebar<br>2. Click the "Collapse all" link at the top right<br>3. Verify the same item in the Course Index remains highlighted | The previously highlighted active item remains highlighted after collapsing all sections. | Medium |
| 4.COUPAG-009 | Each section displays a collapsible chevron and section name in the main content area | Course page is open with course sections listed. | 1. Observe the main content area<br>2. Verify each section shows a collapsible chevron adjacent to its section name | The main content area lists sections, each with a collapsible chevron and section name. | Medium |
| 4.COUPAG-010 | Expanded section lists activities and resources with type icon and clickable name | Course page is open and the target section is expanded. | 1. If the section is collapsed, click its collapsible chevron to expand<br>2. Verify each activity/resource in the section shows a type icon and a clickable name | Within the expanded section, activities and resources are listed with a type icon and a clickable name. | Medium |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 4.COUPAG-005 | Student cannot enable Edit mode on course pages | Logged in as a student on a Course page | 1. Attempt to enable Edit mode by clicking any Edit/Turn editing on control if present on the page<br>2. Observe whether Edit mode becomes enabled or the control/action is blocked | Edit mode is not enabled for the student (control absent or action not permitted). | High |
| 4.COUPAG-006 | Students cannot enable Edit mode on course pages | Course page is open as a student user. | 1. Attempt to click an 'Enable edit mode' control if it is present<br>2. Verify that edit mode is not enabled (control absent, disabled, or clicking has no effect) | Student user cannot enable Edit mode; the page remains in view-only mode. | High |

#### Edge Case Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 4.COUPAG-011 | Clicking Collapse all when all sections are already collapsed maintains collapsed state without errors | Course page where all collapsible sections are already collapsed | 1. Click the "Collapse all" link at the top right<br>2. Verify all sections remain collapsed and no error or unexpected UI change occurs | Sections remain collapsed and no error is shown after clicking "Collapse all." | Low |

---

### Participants

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 5.PARTIC-001 | Apply a single filter condition and verify filtered results | Participants page is open with enrolled users present | 1. Use the Select attribute dropdown to add a single filter condition (choose an attribute and set a value that matches at least one participant)<br>2. Click "Apply filters" | Participants list updates to show only participants matching the condition and the table columns remain visible. | High |
| 5.PARTIC-002 | Apply multiple filter conditions using + Add condition and verify combined filtering | Participants page is open with enrolled users present | 1. Use the Select attribute dropdown to add a first filter condition and click "+ Add condition" to add a second condition (set values that together match at least one participant)<br>2. Click "Apply filters" | Participants list updates to show only participants matching the combined conditions. | High |
| 5.PARTIC-003 | Clear filters removes a single active condition and restores full participants list | Participants page has an active filter applied | 1. Ensure a single filter condition is active (via any toggle, attribute dropdown, or condition)<br>2. Click "Clear filters" | All filter conditions are removed and the participants table shows all enrolled users; table displays expected columns. | High |
| 5.PARTIC-004 | Clear filters removes multiple active conditions and restores full participants list | Participants page has multiple active filter conditions | 1. Ensure multiple filter conditions are active (using toggles, attribute dropdown and added conditions)<br>2. Click "Clear filters" | All filter conditions are removed and the participants table shows all enrolled users; table displays expected columns. | High |
| 5.PARTIC-005 | Participants table displays expected columns after clearing filters | Participants page has active filters | 1. Click "Clear filters"<br>2. Verify the participants table contains columns for checkbox, First/Last name, Roles, Groups, and Last access to course | Participants table shows the listed columns and rows reflect the unfiltered set of enrolled users. | High |
| 5.PARTIC-006 | Filter participants by a chosen first-name initial | Participants page is open and contains participants with varied first-name initials. | 1. Click the First name alphabetical filter button for a chosen letter | Participants list shows only users whose first name starts with the chosen letter. | High |
| 5.PARTIC-007 | Show full participants list using the First name 'All' filter | Participants page is open and multiple participants are enrolled. | 1. Click the First name 'All' alphabetical filter button | Participants table displays all enrolled users without initial-based filtering. | High |
| 5.PARTIC-008 | Clicking a participant name opens their profile | Participants page is open and at least one participant is listed. | 1. Click a participant's First or Last name link in the participants table | The selected participant's profile page opens. | High |
| 5.PARTIC-009 | Filter participants by selected Last name initial | Participants page is open and at least one participant has a last name starting with a visible letter | 1. Click a letter button (A–Z) in the Last name alphabetical filter<br>2. Observe the participants list | Participants list is filtered to show only users whose last name begins with the selected letter | High |
| 5.PARTIC-010 | Selecting 'All' in Last name filter displays all enrolled participants | Participants page is open | 1. Click the 'All' button in the Last name alphabetical filter<br>2. Observe the participants list | Participants list shows all users enrolled in the course | High |
| 5.PARTIC-011 | Clicking a participant name opens their profile from the Participants list | Participants page is open and at least one participant row is visible | 1. Click any participant's First or Last name link in the participants table<br>2. Observe the resulting view | The participant's profile is opened (profile view is displayed) | High |
| 5.PARTIC-012 | Toggle sort by First name (ascending then descending) | Participants page is open and participants listing is visible | 1. Click the "First name" column header to sort the participants by first name<br>2. Verify the participants list is ordered by first name in ascending order<br>3. Click the "First name" column header again to reverse the sort<br>4. Verify the participants list is ordered by first name in descending order | Participants are sorted by first name in ascending order after first click and in descending order after the second click. | High |
| 5.PARTIC-013 | Toggle sort by Last name (ascending then descending) | Participants page is open and participants listing is visible | 1. Click the "Last name" column header to sort the participants by last name<br>2. Verify the participants list is ordered by last name in ascending order<br>3. Click the "Last name" column header again to reverse the sort<br>4. Verify the participants list is ordered by last name in descending order | Participants are sorted by last name in ascending order after first click and in descending order after the second click. | High |
| 5.PARTIC-014 | Open a participant's profile by clicking their name link | Participants page is open and participants listing is visible | 1. Click any participant's First/Last name link in the participants table<br>2. Observe that the participant's profile page opens | Clicking a participant name opens that participant's profile. | High |
| 5.PARTIC-015 | Participants table displays required columns | Participants page is open and participants listing is visible | 1. Inspect the participants table header | Table contains columns for checkbox, First/Last name, Roles, Groups, and Last access to course. | High |
| 5.PARTIC-016 | Participants table displays expected columns | Participants page is open with enrolled users present | 1. Ensure the participants table is visible on the page<br>2. Verify the table shows columns for checkbox, First/Last name, Roles, Groups, and Last access to course | Participants table displays the listed columns. | Medium |
| 5.PARTIC-017 | First name alphabetical filter group contains All and A–Z buttons | Participants page is open. | 1. Verify the First name alphabetical filter group displays 'All' and buttons for letters A–Z | The First name filter shows the 'All' option and buttons for letters A–Z. | Medium |
| 5.PARTIC-018 | Participants table displays expected columns | Participants page is open. | 1. Verify the participants table contains columns for checkbox, First/Last name, Roles, Groups, and Last access to course | Participants table shows the checkbox, First/Last name, Roles, Groups, and Last access to course columns. | Medium |
| 5.PARTIC-019 | Last name alphabetical filter contains All and A–Z buttons | Participants page is open | 1. Locate the Last name alphabetical filter controls on the Participants page<br>2. Verify there is an 'All' button and buttons for letters A through Z in the Last name filter area | The Last name alphabetical filter shows 'All' and buttons for A–Z | Medium |
| 5.PARTIC-020 | Participants table displays expected columns including Last access to course | Participants page is open | 1. Inspect the participants table header<br>2. Verify the table contains columns for checkbox, First/Last name, Roles, Groups, and Last access to course | Participants table shows the checkbox, First/Last name, Roles, Groups, and Last access to course columns | Medium |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 5.PARTIC-021 | Apply filters with all filter inputs empty | Participants page is open | 1. Leave all filter controls empty<br>2. Click "Apply filters" | Validation errors shown for all required filter fields or no filters are applied and the full participants list remains visible. | Medium |

#### Edge Case Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 5.PARTIC-022 | First name filter applies to given names, not family names | Participants page is open and there exists a participant whose last name starts with the chosen letter but whose first name does not. | 1. Click the First name alphabetical filter button for the chosen letter | Participants whose last name but not first name start with the letter are not shown; filtering targets first names only. | Medium |
| 5.PARTIC-023 | Sorted names remain clickable and open profile after sorting | Participants page is open and participants listing is visible | 1. Click the "First name" column header to sort the participants<br>2. Click any participant's First/Last name link from the sorted list<br>3. Observe that the participant's profile page opens | After sorting, participant names remain links and clicking a name opens the participant's profile. | Medium |
| 5.PARTIC-024 | Apply filters that match no participants | Participants page is open with enrolled users present | 1. Use the Select attribute dropdown to add a filter condition with a value that matches no enrolled user<br>2. Click "Apply filters" | Participants table shows no rows and an appropriate 'no results' or empty-state message is displayed. | Low |
| 5.PARTIC-025 | Click Clear filters when no filters are active | Participants page with no active filters | 1. Ensure no filter conditions are active<br>2. Click "Clear filters" | No error occurs; participants list continues to show all enrolled users and table state remains unchanged. | Low |
| 5.PARTIC-026 | Clear filters when course has no enrolled users | Course has no enrolled users | 1. Ensure any active filters are cleared or click "Clear filters"<br>2. Observe the participants table | Participants table remains empty (no rows) and table columns remain visible; no errors are shown. | Low |
| 5.PARTIC-027 | Filter by a letter with no matching first names shows no results | Participants page is open and no participant has a first name starting with the chosen letter. | 1. Click the First name alphabetical filter button for a letter that no participant's first name starts with | Participants list shows no rows or a clear 'no participants' message for the selected initial. | Low |

---

### Grades

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 6.GRADES-001 | Display student's grades via the User report including course header and AGGREGATION row | User report for the course is displayed for a student | 1. Confirm course name appears as a collapsible header in the User report<br>2. Click the course header to expand it<br>3. Observe that graded activities are listed indented beneath the header with columns Grade, Range, Percentage, Feedback, Contribution, and Calculated weight<br>4. Scroll to the bottom of the report and confirm an AGGREGATION Course total row is present | The User report shows the course header, indented graded activities with the listed columns, and an AGGREGATION Course total row. | High |
| 6.GRADES-002 | Verify graded activity shows earned grade and percentage | User report contains at least one graded activity | 1. Locate a graded activity row in the User report<br>2. Verify the Grade column shows an earned numeric value and the Percentage column shows a corresponding percentage | Graded activity displays an earned numeric grade and the corresponding percentage. | High |
| 6.GRADES-003 | User report identifies the current student and displays only their grades | User report for the course is displayed for a student | 1. Locate the user identification area or header in the User report<br>2. Verify the report corresponds to the current student and that grade rows correspond to that single user only | The User report is labeled for the current student and shows only that student's grades. | High |
| 6.GRADES-005 | Collapse and expand course header hides and reveals graded activities | User report for the course is displayed with at least one activity listed | 1. Click the course header to collapse it<br>2. Verify that graded activities are hidden from the list<br>3. Click the course header to expand it<br>4. Verify that graded activities are visible again and the currently active item is highlighted | Collapsing hides activities; expanding reveals them and the active item is highlighted. | Medium |
| 6.GRADES-006 | Display contribution to course total and calculated weight per activity | User report lists activities that have weight and contribution data | 1. Locate an activity row that includes weight/contribution information<br>2. Verify Calculated weight and Contribution to course total columns are present and show values for that activity | Each activity row shows Calculated weight and Contribution to course total values where applicable. | Medium |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 6.GRADES-004 | Prevent student from viewing other students' grades or the full gradebook | User report for the course is displayed for a student | 1. Attempt to switch the report view to a full gradebook or select a different user from any available user selector on the page<br>2. Observe whether other students' grades or a full gradebook view are presented | The UI prevents access to other students' grades or the full gradebook (no other students' grades are shown and access is denied or unavailable). | High |

#### Edge Case Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 6.GRADES-007 | Display dash for ungraded activities in Grade column | User report contains at least one ungraded activity | 1. Locate an ungraded activity row in the User report<br>2. Verify the Grade column displays "–" for that activity | The Grade column shows "–" for ungraded activities. | Medium |

---

### Assignment

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 7.ASSIGN-001 | Open submission form via Add submission | Assignment page is open and the assignment is accepting submissions | 1. Click "Add submission"<br>2. Observe the submission form area | Submission form opens and shows the configured input methods (online text editor and/or file upload area). | High |
| 7.ASSIGN-002 | Add submission using online text editor | Submission form includes an online text editor | 1. Click "Add submission"<br>2. Fill the online text editor with valid submission content<br>3. Click the submission form's "Submit" button | Submission status updates to "Submitted for grading" and the submission summary table reflects the submission (Last modified updated). | High |
| 7.ASSIGN-003 | Add submission using file upload area | Submission form includes a file upload area | 1. Click "Add submission"<br>2. Upload a valid file using the file upload area<br>3. Click the submission form's "Submit" button | Submission status updates to "Submitted for grading" and the submission summary table reflects the submission (Last modified updated). | High |
| 7.ASSIGN-004 | Add submission using both online text editor and file upload | Submission form includes both an online text editor and a file upload area | 1. Click "Add submission"<br>2. Fill the online text editor and upload a valid file<br>3. Click the submission form's "Submit" button | Submission status updates to "Submitted for grading" and the submission summary table reflects both text and uploaded file in the submission details. | High |
| 7.ASSIGN-005 | Edit submission before due date when resubmission permitted | A submission exists, the due date has not passed, and the teacher permits resubmission | 1. Click the submission's "Edit" or "Edit submission" action<br>2. Modify the submission content or uploaded file as needed<br>3. Click the submission form's "Submit" button | Submission is updated and the summary table's Last modified value reflects the update. | High |
| 7.ASSIGN-006 | View submitted work and submission metadata | Student has submitted the assignment and is viewing the Assignment page. | 1. Verify the Opened date, Due date and full Description are displayed on the page<br>2. Verify the Submission status section shows a summary table with rows for Submission status, Grading status, Time remaining, Last modified, and Submission comments<br>3. Click "View submission" and verify the submitted content (files or text) is visible | Submission content and all submission metadata are visible in the summary table and the full description and dates are displayed. | High |
| 7.ASSIGN-007 | View graded assignment shows earned grade and written feedback | The assignment has been graded for the student and the student is viewing the Assignment page. | 1. Verify the Grading status row reflects a graded state<br>2. Verify the earned grade and written feedback are displayed on the page | Grading status indicates graded and the earned grade plus written feedback are visible on the Assignment page. | High |
| 7.ASSIGN-008 | Open edit submission when resubmission permitted and before due date | Student has submitted the assignment, the due date has not passed, and the teacher permits resubmission. | 1. Click the "Edit submission" button in the Submission status section<br>2. Verify the submission editor/form opens and existing submission content is editable | Submission editor opens and the student can modify their submission. | High |
| 7.ASSIGN-009 | Submission status displays 'Submitted for grading' after submission | Student has submitted the assignment and is viewing the Assignment page. | 1. Verify the Submission status row shows 'Submitted for grading' in the summary table<br>2. Verify Time remaining and Last modified values are present alongside the status | Submission status reads 'Submitted for grading' and Time remaining and Last modified metadata are displayed. | High |
| 7.ASSIGN-010 | Edit and submit an online text-only submission | Assignment configured with online text editor; student has an existing submission; due date not passed; teacher permits resubmission. | 1. Click "Edit submission"<br>2. Fill the online text editor with updated submission text<br>3. Click "Save changes" or "Submit" | Submission is saved; Submission status shows 'Submitted for grading' and Last modified is updated. | High |
| 7.ASSIGN-011 | Edit and submit a file-only submission | Assignment configured with file upload area only; student has an existing submission; due date not passed; teacher permits resubmission. | 1. Click "Edit submission"<br>2. Attach a new file in the file upload area and remove or replace existing files as needed<br>3. Click "Save changes" or "Submit" | File upload is saved; Submission status shows 'Submitted for grading' and Last modified is updated. | High |
| 7.ASSIGN-012 | Edit and submit when both online text and file upload are enabled (update both) | Assignment configured with both online text editor and file upload; student has an existing submission; due date not passed; teacher permits resubmission. | 1. Click "Edit submission"<br>2. Update the online text editor and attach or replace files in the file upload area<br>3. Click "Save changes" or "Submit" | Both text and file changes are saved; Submission status shows 'Submitted for grading' and Last modified is updated. | High |
| 7.ASSIGN-016 | Submission status section displays expected summary rows | Assignment page is open | 1. Locate the Submission status section<br>2. Inspect the summary table rows | The Submission status section shows a summary table with rows for Submission status, Grading status, Time remaining, Last modified, and Submission comments. | Medium |
| 7.ASSIGN-017 | Initial state shows no submissions message | Assignment page is open and no submission has been made | 1. Locate the Submission status section<br>2. Read the Submission status text | Submission status displays "No submissions have been made yet". | Medium |
| 7.ASSIGN-018 | View assignment with no submission made | Student has not made a submission for the assignment and is viewing the Assignment page. | 1. Verify the Submission status section summary table is present<br>2. Verify the Submission status row displays 'No submissions have been made yet' and no submitted content is shown | The summary table is shown and Submission status reads 'No submissions have been made yet', with no submission content available. | Medium |
| 7.ASSIGN-019 | Breadcrumbs show full navigation path and each segment is clickable | Student is viewing the assignment activity page. | 1. Verify breadcrumbs at the top show the full navigation path from the course to the activity with each segment rendered as a link<br>2. Click a breadcrumb segment and verify it navigates to the corresponding page | Breadcrumb segments are links representing the full path and clicking a segment navigates to the corresponding page. | Medium |
| 7.ASSIGN-020 | Course Index sidebar shows hierarchical tree, highlights active item, and can be closed | Student is viewing a course page with the Course Index sidebar open. | 1. Verify the Course Index sidebar presents a hierarchical tree with expand/collapse arrows for sections<br>2. Click a section's expand arrow and verify activities become visible and the current activity is highlighted<br>3. Click the sidebar close button (X) and verify the sidebar is hidden | The Course Index expands/collapses sections, the active item is highlighted, and the close button hides the sidebar. | Medium |
| 7.ASSIGN-021 | Edit only the online text when both editor and file upload are present | Assignment configured with both online text editor and file upload; student has an existing submission; due date not passed; teacher permits resubmission. | 1. Click "Edit submission"<br>2. Modify the online text editor content without changing files<br>3. Click "Save changes" or "Submit" | Text changes are saved; existing uploaded files remain unchanged; Last modified is updated. | Medium |
| 7.ASSIGN-022 | Submission status section shows expected summary rows | Assignment page open with Submission status section visible. | 1. Locate the Submission status section and view the summary table | Summary table contains rows for Submission status, Grading status, Time remaining, Last modified, and Submission comments. | Medium |
| 7.ASSIGN-023 | Assignment page displays Opened date, Due date, and Description | Assignment page is open. | 1. Locate the assignment header and description area on the page | The Opened date, Due date, and full Description are displayed. | Medium |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 7.ASSIGN-013 | Attempt to edit submission when due date passed or resubmission not permitted | Student has submitted the assignment and the due date has passed or the teacher does not permit resubmission. | 1. Click the "Edit submission" button on the Assignment page<br>2. Observe whether the edit action is prevented or an explanatory message is shown | Edit action is not allowed and an appropriate message indicating resubmission is not permitted is displayed. | High |
| 7.ASSIGN-014 | Attempt to edit submission after due date has passed | Assignment due date has passed. | 1. Click "Edit submission" | Edit controls are not available and a message indicates editing is not permitted after the due date. | High |
| 7.ASSIGN-015 | Attempt to edit submission when teacher does not permit resubmission | Teacher has disabled resubmission for the assignment and due date has not passed. | 1. Click "Edit submission" | Edit controls are not available and a message indicates resubmission is not permitted by the teacher. | High |
| 7.ASSIGN-024 | Submit with all required fields empty | Submission form is open | 1. Leave the online text editor and file upload area empty<br>2. Click the submission form's "Submit" button | Validation errors shown for required submission inputs and the submission is not accepted. | Medium |
| 7.ASSIGN-025 | Submit with all required fields empty | Assignment form includes at least an online text editor or a file upload area. | 1. Leave all required fields empty<br>2. Click "Save changes" or "Submit" | Validation errors shown for required submission inputs. | Medium |
| 7.ASSIGN-027 | Attempt to edit submission after due date when resubmission not permitted | A submission exists and the assignment due date has passed | 1. Attempt to click the submission's "Edit" or "Edit submission" action<br>2. Observe the result or any messages preventing editing | Editing is not allowed (no edit form opens or an explanatory message is shown). | Low |

#### Edge Case Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 7.ASSIGN-026 | View submission when not yet graded shows 'Not graded' and no feedback | Student has submitted the assignment but it has not been graded. | 1. Verify the Grading status row displays the not-graded state<br>2. Verify that earned grade and written feedback are not present on the page | Grading status shows the not-graded state and there is no earned grade or written feedback displayed. | Medium |

---

### Activities

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 8.ACTIVI-001 | Forums section is collapsed by default in Course Index sidebar | Course page is open and Course Index sidebar is visible | 1. Observe the Forums section in the Course Index sidebar<br>2. Verify the Forums section is in collapsed state and the expand arrow is visible | Forums section is collapsed by default and shows an expand arrow | High |
| 8.ACTIVI-002 | Expand Forums section via arrow reveals forum activities grouped under Forums | Forums section is visible and collapsed | 1. Click the Forums section expand arrow<br>2. Verify forum activities are displayed under the Forums header and appear grouped by type | Forums section expands and forum activities are shown grouped under Forums | High |
| 8.ACTIVI-003 | Expand Resources section via its arrow | Course Index sidebar is visible and Resources section is collapsed | 1. Click the Resources section's expand arrow<br>2. Observe the Resources section's content area | Resources section expands and its contained resource items become visible. | High |
| 8.ACTIVI-004 | Expanded Resources shows resource items grouped by type | Course Index sidebar is visible and Resources section is collapsed | 1. Click the Resources section's expand arrow<br>2. Inspect the list of items displayed under the expanded Resources section | Resource items are displayed and grouped by resource type under the Resources section. | High |
| 8.ACTIVI-005 | Expand an additional activity type collapsible section to reveal its activities | Course page is open and shows additional activity type collapsible sections in the Course Index sidebar | 1. Click the expand arrow for an additional activity type collapsible section<br>2. Observe the content area under that section | The section expands and the activities of that type are displayed grouped under the section. | High |
| 8.ACTIVI-006 | Collapse an expanded additional activity type collapsible section to hide its activities | Course page is open and the target additional activity type collapsible section is expanded | 1. Click the collapse arrow for the expanded additional activity type collapsible section<br>2. Observe the content area under that section | The section collapses and the activities of that type are hidden. | High |
| 8.ACTIVI-007 | Expanding a section reveals the currently active item and preserves its highlight | Course page is open and the currently active activity is located inside a collapsed additional activity type section | 1. Click the expand arrow for the additional activity type collapsible section that contains the active activity<br>2. Observe the list of activities within the expanded section | The active activity becomes visible and remains highlighted in the list after expansion. | High |
| 8.ACTIVI-009 | Collapse Forums section via arrow hides forum activities | Forums section is expanded | 1. Click the Forums section expand arrow<br>2. Verify forum activities are hidden and the section returns to collapsed state | Forums section collapses and forum activities are hidden | Medium |
| 8.ACTIVI-010 | Expand multiple additional activity type sections independently | Course page is open with at least two additional activity type collapsible sections present | 1. Click the expand arrow for one additional activity type collapsible section<br>2. Click the expand arrow for a different additional activity type collapsible section | Both sections are expanded simultaneously and each displays the activities for its respective type. | Medium |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 8.ACTIVI-011 | Expand arrow missing or non-responsive for Forums section | Forums section is visible | 1. Check for presence of the Forums section expand arrow<br>2. Click the Forums section expand arrow if present | Forum activities remain hidden after clicking the arrow (no expand behavior) | Medium |
| 8.ACTIVI-012 | Clicking Resources header outside the arrow does not expand the section | Course Index sidebar is visible and Resources section is collapsed | 1. Click the Resources section header area excluding the expand arrow<br>2. Verify whether the Resources section expands or remains collapsed | Resources section remains collapsed; expansion occurs only via the arrow control. | Medium |

#### Edge Case Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 8.ACTIVI-008 | Resources section is collapsed by default | Course Index sidebar is visible | 1. Observe the Resources section without interacting with the page | Resources section appears collapsed and its child items are hidden by default. | High |
| 8.ACTIVI-013 | Expanded Forums section displays a consolidated overview of forum activities grouped by type | Course page is open and the course contains multiple forum activities | 1. Click the Forums section expand arrow<br>2. Verify the expanded view lists all forum activities and they are grouped under the Forums heading | A consolidated overview of every activity in the course is displayed, grouped by type | Low |
| 8.ACTIVI-014 | Repeatedly toggling an additional activity type section preserves the consolidated grouping | Course page is open and the target additional activity type collapsible section is present | 1. Click the expand arrow for the additional activity type collapsible section<br>2. Click the collapse arrow for the same section<br>3. Click the expand arrow for the same section again | The activities reappear and remain grouped by type as before; the consolidated overview is preserved after repeated toggles. | Low |

---

### Profile

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 9.PROFIL-001 | Open Edit profile form shows collapsible panels and expected fields | User is on their Profile page | 1. Click "Edit profile" link<br>2. Click each collapsible panel header (General, User picture, Additional names, Interests, Optional fields) to expand them | The profile form is displayed; each named panel expands to reveal its fields including First name, Last name, Email address, Email visibility dropdown, MoodleNet profile ID, City/town, Country dropdown, Timezone dropdown, Description, current user picture, new picture upload and picture description, Additional names, Interests, and the Update profile and Cancel controls. | High |
| 9.PROFIL-002 | Profile header displays initials icon, full name, Message button, and optional description | User is on their Profile page | 1. Locate the student's circular initials icon, full name, and "Message" button in the profile header<br>2. Observe the profile description area for presence or absence | Profile header shows the circular initials icon, full name, a "Message" button, and the profile description area which may be empty or contain text. | High |
| 9.PROFIL-003 | Update profile with valid required fields | Profile form is open | 1. Fill all required fields with valid data (First name, Last name, Email address, Country, Timezone, and any other required fields)<br>2. Click "Update profile" | Profile saved and updated values displayed on the profile page. | High |
| 9.PROFIL-004 | Cancel discards edited profile field values | Profile form is open for the current user | 1. Fill editable profile fields (First name, Last name, City/town, Description, Interests) with new values<br>2. Click "Cancel" | Profile form closes and the profile displays the original values; none of the edits were saved. | High |
| 9.PROFIL-005 | Cancel discards a newly selected user picture | Profile form is open for the current user and a current picture is displayed | 1. Change user picture by selecting a new picture file and enter a picture description<br>2. Click "Cancel" | Profile form closes and the displayed user picture remains the previous/current picture; the new upload is not saved. | High |
| 9.PROFIL-009 | Save profile with Description left empty (Description optional) | Profile form is open | 1. Fill all required fields with valid data and leave the Description field empty<br>2. Click "Update profile" | Profile saved successfully and Description remains empty on the profile page. | Medium |
| 9.PROFIL-010 | Replace user picture and save profile | Profile form is open | 1. Upload a new user picture and fill all required fields<br>2. Click "Update profile" | New picture is saved and displayed as the current picture on the profile page. | Medium |
| 9.PROFIL-011 | Cancel discards changes to optional profile fields only | Profile form is open for the current user | 1. Modify only optional fields (Additional names, Interests, Description)<br>2. Click "Cancel" | Profile form closes and optional fields remain unchanged on the profile; no optional-field edits are saved. | Medium |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 9.PROFIL-006 | Prevent a student from editing another student's profile | User is on another student's Profile page | 1. Attempt to click the "Edit profile" link on the other student's Profile page | The Edit profile form is not accessible; editing controls are not available and the user cannot modify the profile. | High |
| 9.PROFIL-007 | Attempt to update another user's profile is blocked | Profile form for another user is open | 1. Modify one or more editable fields<br>2. Click "Update profile" | Changes are not saved and the system prevents the update (authorization error or redirect). | High |
| 9.PROFIL-008 | Edit control not available for another user's profile (students) | Viewing a profile belonging to another user while signed in as a student | 1. Inspect the profile page for the presence of an "Edit profile" control or button | The "Edit profile" control is not present or is disabled for the student viewing another user's profile. | High |
| 9.PROFIL-012 | Submit with all required fields empty | Profile form is open | 1. Leave all required fields empty<br>2. Click "Update profile" | Validation errors shown for all required fields. | Medium |

#### Edge Case Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 9.PROFIL-013 | Open Edit profile when Description is empty | User is on their Profile page with an empty profile description | 1. Click "Edit profile" link<br>2. Open the General panel and inspect the Description field | The profile form opens normally and the Description field may be empty without error or blocking the form. | Low |
| 9.PROFIL-014 | Cancel with no changes closes form without affecting profile | Profile form is open for the current user | 1. Click "Cancel" without modifying any fields<br>2. Verify the profile display after the form closes | Form closes and the profile data remains unchanged. | Low |

---

### Logout

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 10.LOGOUT-001 | Log out terminates the current session and redirects to login page | User is authenticated and the user menu is visible | 1. Open the user menu via the user's initials icon<br>2. Click "Log out" | The current authenticated session is terminated and the application redirects to the login page. | High |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 10.LOGOUT-002 | Access to protected pages requires re-authentication after logout | User has logged out and the login page is displayed | 1. From the current page, click a protected page link in the top navigation (for example: "Dashboard")<br>2. Observe whether the protected page is displayed or whether the login page is shown | Access to the protected page is blocked and the user remains on or is redirected to the login page; re-authentication is required to view the protected page. | High |

---

## Navigation Graph

![Navigation Graph](Output/Moodle/navigation_graph.png)

### Pages

| Module | URL | Test Cases |
|--------|-----|------------|
| Login | /login | 8 |
| Dashboard | /dashboard | 32 |
| My Courses | /my-courses | 10 |
| Course Page | /course/{id} | 11 |
| Participants | /course/{id}/participants | 27 |
| Grades | /course/{id}/grades | 7 |
| Assignment | /course/{course_id}/assignment/{id} | 27 |
| Activities | /course/{id}/activities | 14 |
| Profile | /profile/{user_id} | 14 |
| Logout | /logout | 2 |
