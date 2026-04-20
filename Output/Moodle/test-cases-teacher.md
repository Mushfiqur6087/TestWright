# Moodleteacher

**Base URL:** 
**Generated:** 2026-04-20T21:35:17.173076

## Summary

| Metric | Count |
|--------|-------|
| **Total Tests** | 282 |

### By Type

| Type | Count |
|------|-------|
| Positive | 199 |
| Negative | 47 |
| Edge Case | 36 |
| Standard | 0 |

### By Priority

| Priority | Count |
|----------|-------|
| High | 144 |
| Medium | 121 |
| Low | 17 |

---

## Test Cases

### Login

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 1.LOGIN-001 | Login with valid teacher credentials redirects to Dashboard | None | 1. Fill all required fields (Username with valid teacher username, Password with valid password)<br>2. Click "Log in" | User is redirected to the Dashboard. | High |
| 1.LOGIN-002 | Start unauthenticated browsing via Access as a guest | Login page is open | 1. Click the "Access as a guest" button on the page | An unauthenticated browsing session is started and the site is accessible without logging in. | High |
| 1.LOGIN-003 | View cookie usage information via Cookies notice button | Login page is open | 1. Click the "Cookies notice" button on the page | Cookie usage information is displayed to the user. | Medium |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 1.LOGIN-004 | Submit with all required fields empty | None | 1. Leave all required fields empty<br>2. Click "Log in" | Inline validation error shown for credentials; password remains cleared and username not provided. | Medium |
| 1.LOGIN-005 | Attempt login with invalid password preserves username and clears password | None | 1. Fill all required fields (Username with valid username, Password with invalid password)<br>2. Click "Log in" | Inline error message shown; the password field is cleared and the username remains in the username field for correction. | Medium |
| 1.LOGIN-006 | Verify 'Lost password?' link is disabled on the test site | None | 1. Attempt to click the "Lost password?" link on the login form | The "Lost password?" link is disabled and does not navigate. | Medium |

---

### Dashboard

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 2.DASHBO-001 | Find activities by name using the Timeline search | Timeline block contains upcoming activities with distinct names | 1. Fill the Timeline search field with a valid activity name and execute the search<br>2. Observe the Timeline results listed in the block | Timeline displays activities whose names match the search query | High |
| 2.DASHBO-002 | Find activities by type using the Timeline search | Timeline block contains upcoming activities of different types | 1. Fill the Timeline search field with an activity type and execute the search<br>2. Observe the Timeline results listed in the block | Timeline displays activities whose type matches the search query | High |
| 2.DASHBO-003 | Timeline aggregates upcoming teaching actions across enrolled courses | User is enrolled in multiple courses that have upcoming teaching activities | 1. Leave the Timeline search field empty and view the Timeline block<br>2. Inspect the list of upcoming items shown in the Timeline | Timeline shows upcoming teaching activities coming from the user's enrolled courses | High |
| 2.DASHBO-004 | Show empty state when selected time range contains no items | No upcoming activities exist within the chosen time range | 1. Select a time range in the Timeline time range dropdown that contains no upcoming activities<br>2. Observe the Timeline block contents | An empty state is shown in the Timeline block | High |
| 2.DASHBO-005 | Filter timeline shows aggregated upcoming teaching actions for selected range | User is enrolled in at least two courses and has upcoming teaching actions within the chosen time range | 1. Click the timeline time range dropdown<br>2. Select a time range that includes known upcoming teaching actions<br>3. Verify the Timeline block lists upcoming teaching actions and includes items from all enrolled courses | Timeline displays upcoming teaching actions from all enrolled courses that fall within the selected time range. | High |
| 2.DASHBO-006 | Change timeline sort order updates the displayed item order | Timeline block displays multiple upcoming teaching actions. | 1. Click the Timeline block's sort order dropdown<br>2. Select an alternate sort order option<br>3. Verify the timeline items reorder according to the selected option | Timeline item order updates to reflect the selected sort order. | High |
| 2.DASHBO-007 | Change timeline sort order to the opposite option reorders items | Timeline block displays multiple upcoming teaching actions. | 1. Click the Timeline block's sort order dropdown<br>2. Select the other available sort order option<br>3. Verify the timeline items reorder according to the newly selected option | Timeline item order updates to reflect the newly selected sort order. | High |
| 2.DASHBO-008 | Create a calendar entry via New event and verify it appears in monthly view | Calendar block is visible on the page | 1. Click the "New event" button in the Calendar block<br>2. Fill all required fields in the New Event form (event title, event date, and other mandatory fields)<br>3. Click the form's Save/Create button | New calendar entry is created and appears in the monthly view on the selected date; the date displays the event name inline and the monthly heading shows the current month and year. | High |
| 2.DASHBO-009 | Calendar monthly view displays current month and year heading | Calendar block is visible on the page | 1. Observe the Calendar block heading in the monthly view | Heading shows the current month and year. | High |
| 2.DASHBO-010 | Calendar monthly view displays current month heading, highlighted current date, and inline event names | Calendar block visible on the page | 1. Observe the Calendar block monthly view heading<br>2. Inspect the calendar grid for the highlighted current date and for dates that display event names inline | Calendar shows the current month and year as the heading; the current date is highlighted; dates with events display their names inline. | High |
| 2.DASHBO-011 | Navigate to next month using the Right arrow | Calendar block visible on the page | 1. Click the Right arrow in the Calendar block<br>2. Observe the Calendar monthly view heading and the calendar grid | Calendar updates to the next month and displays the appropriate month and year in the heading; dates with events in the new month display their names inline. | High |
| 2.DASHBO-012 | Navigate to previous month using the Left arrow | Calendar block visible on the page | 1. Click the Left arrow in the Calendar block<br>2. Observe the Calendar monthly view heading and the calendar grid | Calendar updates to the previous month and displays the appropriate month and year in the heading; dates with events in the new month display their names inline. | High |
| 2.DASHBO-013 | Filter calendar to a specific course displays only that course's events | Calendar contains events from multiple courses | 1. Open the Calendar block's "All courses" dropdown and select a specific course<br>2. Wait for the calendar view to update | Calendar displays only events for the selected course in the monthly view and dates with events display their names inline. | High |
| 2.DASHBO-014 | Selecting 'All courses' shows events from all courses in the monthly view | Calendar has previously been filtered by a course | 1. Open the Calendar block's "All courses" dropdown and select the "All courses" option<br>2. Wait for the calendar view to update | Calendar displays events from all courses in the monthly view and dates with events display their names inline. | High |
| 2.DASHBO-015 | Calendar block shows monthly view with current month and year heading | None | 1. Locate the Calendar block on the Dashboard | Calendar shows a monthly view with the current month and year as a heading. | High |
| 2.DASHBO-016 | Filtering timeline by a narrower time range updates displayed items | User has upcoming teaching actions across different dates such that a narrower time range will exclude some items | 1. Select a broader time range via the timeline time range dropdown<br>2. Select a narrower time range via the timeline time range dropdown<br>3. Verify the Timeline block updates to show only actions within the newly selected narrower range | Timeline content is refreshed and only items within the newly selected time range are shown. | Medium |
| 2.DASHBO-017 | Sort order dropdown is visible in the Timeline block | Timeline block is visible on the Dashboard. | 1. Observe the Timeline block<br>2. Verify the sort order dropdown is present and displays the current sort selection | Sort order dropdown is visible in the Timeline block and shows the current selection. | Medium |
| 2.DASHBO-024 | Timeline time range dropdown displays selectable options | None | 1. Click the timeline time range dropdown<br>2. Verify the available time range options are displayed and selectable | Time range options are visible and can be selected (e.g., next week, next month). | Low |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 2.DASHBO-018 | Search with no matching activities shows empty state | Timeline contains activities but none match the intended search query within the current time range | 1. Fill the Timeline search field with text that does not match any activity name or type and execute the search<br>2. Observe the Timeline block results | An empty state is shown because no activities match the search criteria | Medium |
| 2.DASHBO-019 | Submit New Event form with all required fields empty | Calendar block is visible on the page | 1. Click the "New event" button in the Calendar block<br>2. Leave all required fields empty and click the form's Save/Create button | Validation errors shown for all required fields and the event is not created. | Medium |

#### Edge Case Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 2.DASHBO-020 | Search results are limited to the currently selected time range | An activity exists outside the currently selected (narrow) time range | 1. Select a narrow time range that excludes the known activity<br>2. Fill the Timeline search field with the excluded activity's name and execute the search | No results are shown (empty state) because the activity falls outside the selected time range | Medium |
| 2.DASHBO-021 | Change sort order when actions span multiple courses retains aggregation and reorders items | Timeline block displays upcoming teaching actions from multiple enrolled courses. | 1. Confirm the Timeline block lists actions from more than one enrolled course<br>2. Click the Timeline block's sort order dropdown and select a different sort order<br>3. Verify the timeline still shows actions from all enrolled courses and that items are reordered per the selection | Timeline reorders items according to the selected sort order while continuing to include actions from all enrolled courses. | Medium |
| 2.DASHBO-022 | Navigate across year boundary by advancing month using the Right arrow | Calendar block currently displays the last month of a year | 1. Click the Right arrow in the Calendar block<br>2. Observe the Calendar monthly view heading and the calendar grid | Calendar advances to the next month's view and the heading shows the incremented year; dates with events in the new month display their names inline. | Medium |
| 2.DASHBO-023 | Filter when multiple courses have events on the same date shows only selected course's events | Calendar contains multiple events on the same date from different courses | 1. Open the Calendar block's "All courses" dropdown and select one of the courses that has an event on that date<br>2. Wait for the calendar view to update | On the shared date the calendar displays only the event names belonging to the selected course and hides other courses' events on that date. | Medium |
| 2.DASHBO-025 | Selecting a time range with no upcoming actions shows the empty state | User has no upcoming teaching actions within the selected time range across all enrolled courses | 1. Click the timeline time range dropdown<br>2. Select a time range that contains no upcoming teaching actions<br>3. Verify the Timeline block shows its empty state | An empty state is shown in the Timeline block when no items exist in the selected range. | Low |

---

### Dashboard — Edit Mode

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 3.D—EM-001 | Toggle Edit mode on reveals Reset and Add a block controls | Dashboard page is open | 1. Click the Edit mode toggle to enable Edit mode | A "Reset page to default" button appears at the top right and a "+ Add a block" button appears below the Dashboard heading. | High |
| 3.D—EM-002 | Open Add a block page lists all available block types | Edit mode is on | 1. Click the "+ Add a block" button | An Add a block page opens and lists all available block types: Comments, Course overview, Latest announcements, Latest badges, Learning plans, Logged in user, Mentees, Online users, Private files, Random glossary entry, Recently accessed courses, Starred courses, Tags, Text, and Upcoming events. | High |
| 3.D—EM-003 | In Edit mode, existing blocks show move icon and options menu with configure/move/delete | Edit mode is on and the Dashboard shows at least one existing block | 1. For a visible block, confirm the move icon is present and click its three-dot options menu | The move icon is visible for the block and the three-dot options menu reveals Configure, Move, and Delete actions. | High |
| 3.D—EM-004 | Reset reverts a single persisted layout change | User is on their Dashboard and Edit mode can be toggled | 1. Toggle Edit mode on<br>2. Make a single layout change (move an existing block or add a block) and ensure the change is persisted<br>3. Click "Reset page to default"<br>4. Verify the Dashboard layout matches the system default and the made change is reverted | Dashboard layout returns to the system default and the single persisted change is reverted. | High |
| 3.D—EM-005 | Reset fully reverts multiple persisted layout changes (added and moved blocks) | User is on their Dashboard and Edit mode can be toggled | 1. Toggle Edit mode on<br>2. Make multiple layout changes (add a block and move a different block) and ensure changes are persisted<br>3. Click "Reset page to default"<br>4. Verify all added and moved blocks are restored to the system default layout | "Reset page to default" fully reverts multiple persisted layout changes and restores the system default layout. | High |
| 3.D—EM-006 | Open block configuration from options menu in Edit mode | Dashboard is in Edit mode and a block is visible. | 1. Click the block's three-dot options menu<br>2. Click "Configure" in the options menu | The block's configuration interface (panel or dialog) is displayed. | High |
| 3.D—EM-007 | Block displays move icon and three-dot options menu while Edit mode is enabled | Dashboard is in Edit mode and a block is visible. | 1. Visually inspect the block header<br>2. Verify the block shows a move icon and a three-dot options menu | Each block shows a move icon and a three-dot options menu. | High |
| 3.D—EM-008 | Move a block using move control (triggerable from: move icon, three-dot menu) | User is on Dashboard with Edit mode enabled and at least two blocks present. | 1. Activate the move control for a target block using the move icon or the three-dot options menu<br>2. Move the block to a different column/position and release or confirm the placement<br>3. Exit Edit mode | The block appears in the new position and remains in that position after exiting Edit mode. | High |
| 3.D—EM-009 | Reset page to default reverts moved block layout | User is on Dashboard and has moved a block from its original position while in Edit mode. | 1. Click the "Reset page to default" control<br>2. Confirm the reset if prompted | Dashboard layout returns to the default and the previously moved block is restored to its original position. | High |
| 3.D—EM-010 | Delete a block while Edit mode is enabled | Edit mode is enabled and at least one dashboard block is present | 1. Open the block's three-dot options menu<br>2. Click the "Delete" option for the block<br>3. Verify the block is removed from the dashboard layout | The selected block is removed from the dashboard for the current user. | High |
| 3.D—EM-011 | Deleted block remains removed after page reload (per-user persistence) | Edit mode is enabled and at least one dashboard block is present | 1. Open the block's three-dot options menu and click the "Delete" option<br>2. Reload the dashboard page<br>3. Verify the previously deleted block remains absent from the layout | The block deletion persists after reload for the current user. | High |
| 3.D—EM-013 | Edit mode displays Reset and Add a block controls | User is on their Dashboard | 1. Toggle Edit mode on<br>2. Verify the "Reset page to default" button appears at the top right and the "+ Add a block" button appears below the Dashboard heading | "Reset page to default" and "+ Add a block" controls are visible when Edit mode is on. | Medium |
| 3.D—EM-014 | Options menu lists Configure, Move, and Delete actions | Dashboard is in Edit mode and a block is visible. | 1. Click the block's three-dot options menu<br>2. Verify the menu contains options labeled "Configure", "Move", and "Delete" | The options menu includes Configure, Move, and Delete actions. | Medium |
| 3.D—EM-015 | Edit mode displays move icon and three-dot options menu for each block | User is on Dashboard. | 1. Enable Edit mode | Each existing block displays a move icon and a three-dot options menu for configure, move, and delete actions. | Medium |
| 3.D—EM-016 | Block shows move icon and three-dot options menu in Edit mode | Edit mode is enabled and at least one dashboard block is present | 1. Locate a block on the dashboard<br>2. Verify a move icon is visible for the block<br>3. Open the block's three-dot options menu and verify it contains Configure, Move, and Delete options | Move icon is visible and the options menu lists Configure, Move, and Delete. | Medium |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 3.D—EM-017 | Cancel adding a block returns to the Dashboard without adding a block | Add a block page is open | 1. Click the "Cancel" link at the bottom of the Add a block page | The view returns to the Dashboard and no new block is added. | Medium |
| 3.D—EM-018 | Reset button is not visible when Edit mode is off | User is on their Dashboard with Edit mode off | 1. Ensure Edit mode is off<br>2. Verify the "Reset page to default" button is not visible | "Reset page to default" control is not present when Edit mode is off. | Medium |
| 3.D—EM-019 | Configure option inaccessible when Edit mode is disabled | Dashboard is not in Edit mode and a block is visible. | 1. Attempt to click the block's three-dot options menu | The options menu is not available and the Configure action cannot be accessed. | Medium |
| 3.D—EM-020 | Error state when Configure action is missing from options menu | Dashboard is in Edit mode and a block is visible. | 1. Click the block's three-dot options menu<br>2. Verify whether a "Configure" option is present | If "Configure" is absent the user cannot open block configuration via the menu. | Medium |
| 3.D—EM-021 | Delete option is not available when Edit mode is disabled | Edit mode is disabled and at least one dashboard block is present | 1. Locate a block on the dashboard with Edit mode disabled<br>2. Verify the three-dot options menu is not visible for the block and no Delete action is available | The delete action is not available when Edit mode is disabled. | Medium |

#### Edge Case Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 3.D—EM-012 | Reset page to default restores a previously deleted block | Edit mode is enabled and a block was previously deleted from the dashboard | 1. Click the "Reset page to default" control<br>2. Verify the previously deleted block is restored to the dashboard layout | The dashboard layout is restored and the previously deleted block reappears. | High |
| 3.D—EM-022 | Reset persists after page refresh | User is on their Dashboard with at least one persisted layout change | 1. Toggle Edit mode on<br>2. Click "Reset page to default"<br>3. Refresh the Dashboard page<br>4. Verify the Dashboard remains in the system default layout after refresh | The reverted default layout remains after page refresh, indicating the reset updated the persisted state. | Medium |
| 3.D—EM-023 | Move controls are not available when Edit mode is off | User is on Dashboard with Edit mode disabled and at least two blocks present. | 1. Attempt to locate or activate the move icon and the three-dot options menu for a target block | Move controls are not visible and blocks cannot be moved when Edit mode is off. | Medium |

---

### My Courses

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 4.MYCOU-001 | Star a course via the course card three-dot menu | My Courses page is open and course cards are visible. | 1. Open the three-dot menu on a course card<br>2. Click "Star this course" | The course is pinned to the top of the My Courses view and appears under the Starred status. | High |
| 4.MYCOU-002 | Starred course appears when filtering My Courses by Starred | My Courses page is open and at least one course card is visible. | 1. Open the three-dot menu on a course card and click "Star this course"<br>2. Open the status dropdown and select "Starred" | The starred course appears in the filtered results. | High |
| 4.MYCOU-003 | Three-dot menu exposes Remove from view action | A course card is visible in the My Courses listing | 1. Click the three-dot menu on a course card<br>2. Verify the menu contains the "Remove from view" option and that it is selectable | "Remove from view" is present in the course card menu and can be selected | High |
| 4.MYCOU-004 | Remove a course from view via course card menu | A course card is visible in the My Courses listing | 1. Click the three-dot menu on the target course card<br>2. Click the "Remove from view" option | The course is removed from the My Courses listing (no longer visible in the current listing) | High |
| 4.MYCOU-005 | Removed course appears when filtering by Hidden status | The course has been removed from view | 1. Open the status dropdown on the My Courses page<br>2. Select "Hidden" from the status dropdown | Courses removed from view appear in the listing when the status filter is set to Hidden | High |
| 4.MYCOU-006 | Removed course's card under Hidden shows banner, clickable name, and category (indicating continued access) | The course has been removed from view | 1. Open the status dropdown on the My Courses page and select "Hidden"<br>2. Verify the removed course's card is listed and displays the banner image, the course name as a clickable link, and the category name | The removed course is listed under Hidden and its card shows the banner image, clickable course name, and category name | High |
| 4.MYCOU-008 | Course card displays banner image, clickable name, and category | My Courses page is open and course cards are visible. | 1. Locate any course card on the page<br>2. Verify the card shows a banner image, the course name rendered as a clickable link, and the category name | Course card displays the banner image, the course name as a clickable link, and the category name. | Medium |
| 4.MYCOU-009 | Course card displays banner image, clickable course name, and category | A course card is visible in the My Courses listing | 1. Verify a course card is present on the My Courses page<br>2. Verify the course card displays the course banner image, the course name as a clickable link, and the category name | Each course card shows the banner image, the course name as a clickable link, and the category name | Medium |

#### Edge Case Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 4.MYCOU-007 | Star a lower-positioned course pins it to the top | My Courses page is open and multiple course cards are present with at least one not positioned at the top. | 1. Open the three-dot menu on a course that is not currently at the top and click "Star this course"<br>2. Observe the My Courses view | The previously lower-positioned course is moved to and displayed at the top of the My Courses view. | High |

---

### Course Page

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 5.COUPAG-001 | Collapse all sections using the "Collapse all" link | Course page is open with multiple sections expanded | 1. Click the "Collapse all" link in the course header<br>2. Verify every section displays the collapsed state and that activities/resources within all sections are not visible | All sections are collapsed and their activities/resources are hidden. | High |
| 5.COUPAG-002 | Expand a collapsed section shows its activities and resources | Course page is open and at least one section is collapsed and contains activities/resources | 1. Click the collapsed section's collapsible chevron | The clicked section expands and its activities and resources become visible with their type icons and clickable names. | High |
| 5.COUPAG-003 | Collapse an expanded section hides its activities and resources | Course page is open and at least one section is expanded and showing activities/resources | 1. Click the expanded section's collapsible chevron | The clicked section collapses and its activities and resources are hidden from view. | High |
| 5.COUPAG-004 | Toggling one section does not change other sections' expand/collapse states | Course page is open with multiple sections in a mix of expanded and collapsed states | 1. Record the expand/collapse state of at least one other section<br>2. Click a different section's collapsible chevron | Only the targeted section toggles state; the previously recorded other section's state remains unchanged. | High |
| 5.COUPAG-005 | Collapse all collapses all sections from a mixed expanded/collapsed state | Course page is open with at least one expanded and one collapsed section | 1. Click the "Collapse all" link in the course header<br>2. Verify every section is set to the collapsed state and no section content is visible | All sections become collapsed and their activities/resources are hidden. | Medium |
| 5.COUPAG-006 | Course page displays collapsible sections with chevrons and section names | Course page is open | 1. Inspect the course content area<br>2. Verify each section shows a collapsible chevron and its section name | Each section displays a chevron and section name consistent with collapsible sections behavior. | Medium |
| 5.COUPAG-007 | Each section displays a collapsible chevron and a section name | Course page is open and sections are listed in the main content area | 1. Inspect one or more section rows in the main content area | Each inspected section row contains a collapsible chevron and the section name is visible. | Medium |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 5.COUPAG-008 | Section missing collapsible chevron prevents toggling (UI violation) | Course page is open and a section is present that does not show a chevron (defect scenario) | 1. Attempt to locate and click the section's collapsible chevron | No collapsible chevron is present for the section and the section cannot be toggled via the chevron control. | Medium |

#### Edge Case Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 5.COUPAG-009 | Click "Collapse all" when all sections are already collapsed | Course page is open with all sections already collapsed | 1. Click the "Collapse all" link in the course header<br>2. Verify all sections remain collapsed and no section content becomes visible | Sections remain collapsed and activities/resources remain hidden after clicking the link. | Low |

---

### Course Edit Mode and Activity Chooser

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 6.CEMAC-001 | Enable Edit mode displays authoring interface with inline controls and authoring buttons | Course page is open and user has teacher role | 1. Click the control to enable Edit mode on the current Course page<br>2. Observe the course content area for authoring UI elements (inline controls on section and activity rows, edit icons, bulk actions area, '+ Add an activity or resource' buttons, and '+ Add a subsection' controls) | The Course page transforms into an authoring interface and the listed inline controls, edit icons, bulk actions area, '+ Add an activity or resource' buttons, and '+ Add a subsection' controls are visible. | High |
| 6.CEMAC-002 | Bulk actions toolbar appears only after selecting multiple activities in Edit mode | Course page is open with at least two activities and user has teacher role | 1. Click the control to enable Edit mode on the current Course page<br>2. Select multiple activities using their selection checkboxes<br>3. Observe whether the bulk actions toolbar becomes visible | After selecting multiple activities, the bulk actions toolbar is displayed and available for batch operations. | High |
| 6.CEMAC-003 | Inline edit controls appear for sections and activities in edit mode | Edit mode is enabled on the course page. | 1. Hover over a section row to reveal inline controls<br>2. Hover over an activity row to reveal inline controls | Each hovered section and activity row displays inline controls and the edit icon is visible. | High |
| 6.CEMAC-004 | Quick rename a section using the inline edit icon | Edit mode is enabled and at least one section exists. | 1. Click the section's edit icon<br>2. Enter a new valid section name in the inline name field and save | Section title updates inline and the new name is persisted in the course content. | High |
| 6.CEMAC-005 | Quick rename an activity using the inline edit icon | Edit mode is enabled and at least one activity exists. | 1. Click the activity's edit icon<br>2. Enter a new valid activity name in the inline name field and save | Activity title updates inline and the new name is persisted in the course content. | High |
| 6.CEMAC-006 | Enable Edit mode shows inline controls on sections and activities | User has course editing permissions and course page is open | 1. Click the Edit mode toggle to enable Edit mode | Each section and activity row gains inline controls. | High |
| 6.CEMAC-007 | Duplicate a section via section-level three-dot menu creates a copy with same activities | Edit mode is enabled and a section containing one or more activities is visible | 1. Click the section-level three-dot menu for the target section<br>2. Click "Duplicate" from the menu | A copy of the section appears immediately after the original containing the same activities and the new section shows inline controls. | High |
| 6.CEMAC-008 | Hide a section via section-level three-dot menu | Edit mode is enabled and a visible section exists | 1. Click the section's three-dot menu<br>2. Click "Hide" | The section is marked as hidden (hidden indicator shown) and the section is removed from learner view | High |
| 6.CEMAC-009 | Hidden section is not visible to learners in Course Index sidebar | A section has been hidden and a learner session is active | 1. Open the Course Index sidebar<br>2. Verify the hidden section is not listed in the sidebar or course content for the learner | Learners cannot see the hidden section in the Course Index sidebar or course content | High |
| 6.CEMAC-010 | Show inline controls for sections and activities in edit mode | Edit mode is enabled for the course | 1. Locate a section row and an activity row on the course page<br>2. Verify inline controls are visible on both rows (icons and section-level three-dot menu) | Inline controls are displayed on the section and activity rows. | High |
| 6.CEMAC-011 | Section-level three-dot menu lists expected actions | Edit mode is enabled for the course | 1. Open the section-level three-dot menu for a section<br>2. Inspect the menu options | The menu shows options: edit, duplicate, hide, delete, and move. | High |
| 6.CEMAC-012 | Delete a section via the section-level three-dot menu | Edit mode is enabled and the target section is visible | 1. Open the section-level three-dot menu for the target section<br>2. Click "Delete"<br>3. Confirm deletion in the confirmation dialog | The section is removed from the course page and no longer appears in the Course Index sidebar. | High |
| 6.CEMAC-013 | Edit an activity's settings via activity-level three-dot menu | Edit mode is enabled and the course page is open. | 1. Click the activity-level three-dot menu for a target activity<br>2. Click "Edit settings"<br>3. Modify one or more editable fields in the activity settings form<br>4. Click "Save changes" | The activity settings are updated and the change is reflected in the activity row or activity details. | High |
| 6.CEMAC-014 | Activity-level three-dot menu shows all expected actions | Edit mode is enabled and the course page is open. | 1. Click the activity-level three-dot menu for a target activity<br>2. Inspect the menu options list | The menu contains the options: Edit settings, Move, Duplicate, Hide, Set access restrictions, and Delete. | High |
| 6.CEMAC-015 | Move an activity to a different section using the activity-level menu | Edit mode is enabled and activity-level inline controls are visible on the course page. | 1. Click the activity's three-dot menu<br>2. Click the "Move" option<br>3. In the move UI select a different target section and a target position, then confirm the move | Activity appears in the chosen section at the selected position; Course Index sidebar reflects the new location and the moved activity is highlighted as the active item. | High |
| 6.CEMAC-016 | Reorder an activity within the same section using the activity-level menu | Edit mode is enabled and activity-level inline controls are visible on the course page. | 1. Click the activity's three-dot menu<br>2. Click the "Move" option<br>3. In the move UI select a new position within the same section, then confirm the move | Activity is placed at the new position within the same section and is highlighted as the active item in the Course Index sidebar. | High |
| 6.CEMAC-017 | Duplicate an activity via the activity-level three-dot menu | Edit mode is enabled and activity inline controls are visible | 1. Open the activity-level three-dot menu for the target activity<br>2. Click "Duplicate" and confirm duplication in any confirmation dialog | A new activity row is created as a duplicate of the original and appears as a separate item in the Course Index and activity list | High |
| 6.CEMAC-018 | Hide an activity from learners using the activity-level menu | Edit mode enabled and a visible activity row is present | 1. Click the activity's three-dot menu<br>2. Click "Hide" (confirm if a confirmation appears) | Activity becomes hidden from learners and the activity row indicates hidden status | High |
| 6.CEMAC-019 | Set access restrictions from an activity's three-dot menu | User is a teacher and the course page is in edit mode with activities visible | 1. Open the activity-level three-dot menu for a specific activity row<br>2. Click "Set access restrictions"<br>3. Configure a valid access restriction using the available controls and click "Save" | Access restriction is saved and the activity displays an updated access indicator or summary | High |
| 6.CEMAC-020 | Inline controls appear on each section and activity row when edit mode is enabled | User is a teacher and the course page is open with sections and activities visible | 1. Enable edit mode on the course page<br>2. Observe the section and activity rows for inline controls | Each section and activity row displays inline controls | High |
| 6.CEMAC-021 | Delete an activity via activity-level three-dot menu | Edit mode enabled on the course page and the target activity row is visible | 1. Open the activity-level three-dot menu for the target activity<br>2. Click "Delete"<br>3. Confirm deletion in the confirmation dialog | Activity is removed from the course content list and no longer appears in the Course Index sidebar; active item highlighting updates accordingly. | High |
| 6.CEMAC-022 | Bulk actions toolbar appears when multiple activities are selected | Edit mode enabled and multiple activities visible in the course | 1. Select multiple activities using their selection checkboxes<br>2. Observe the bulk actions toolbar | Bulk actions toolbar becomes visible and shows available batch actions. | High |
| 6.CEMAC-023 | Hide multiple activities via bulk actions toolbar | Edit mode enabled and multiple visible activities present | 1. Select multiple visible activities<br>2. Click the "Hide" action in the bulk actions toolbar<br>3. Confirm the hide action if a confirmation dialog appears | Selected activities are hidden (marked as hidden or no longer visible in their section). | High |
| 6.CEMAC-024 | Duplicate multiple activities via bulk actions toolbar | Edit mode enabled and multiple activities present | 1. Select multiple activities<br>2. Click the "Duplicate" action in the bulk actions toolbar<br>3. Confirm duplication if prompted | Copies of the selected activities are created and appear in the course index. | High |
| 6.CEMAC-025 | Move multiple activities to another section via bulk actions toolbar | Edit mode enabled, multiple activities present, and at least one destination section exists | 1. Select multiple activities<br>2. Click the "Move" action in the bulk actions toolbar<br>3. Choose the destination section in the move dialog and confirm the move | Selected activities are relocated to the chosen section in the course index. | High |
| 6.CEMAC-026 | Delete multiple activities using the bulk actions toolbar | Edit mode enabled and multiple deletable activities available | 1. Select multiple activities<br>2. Click the "Delete" action in the bulk actions toolbar<br>3. Confirm deletion in the confirmation dialog | Selected activities are removed and no longer appear in the course index. | High |
| 6.CEMAC-027 | Open Activity Chooser modal via '+ Add an activity or resource' button | Edit mode is enabled on the course page | 1. Click the '+ Add an activity or resource' button at the bottom of a section | The Activity Chooser modal opens and is displayed. | High |
| 6.CEMAC-028 | Activity Chooser displays category filter bar with expected options | Activity Chooser modal is open | 1. Observe the category filter bar in the Activity Chooser modal<br>2. Verify the filter bar contains options labeled All, Activities, Resources, and Recommended | Category filter bar is visible and contains the four expected options. | High |
| 6.CEMAC-029 | Selecting a category filters the Activity Chooser tiles appropriately | Activity Chooser modal is open and tiles for multiple categories are present | 1. Click each category filter option in turn (Activities, Resources, Recommended, All)<br>2. After each click, verify the tile list updates to show only tiles belonging to the selected category and that selecting All shows all tiles | Selecting a category updates the tile list to show only tiles within that category; All displays all tiles. | High |
| 6.CEMAC-030 | Search for an activity or resource using the Activity Chooser search field | Activity Chooser modal is open | 1. Fill the search field with a term that should match a specific activity or resource<br>2. Trigger the search action (press Enter or click the search icon)<br>3. Inspect the chooser results and attempt to select the matching item | Activity Chooser displays matching activities or resources, non-matching items are not shown, and the target item is selectable | High |
| 6.CEMAC-031 | Activity Chooser displays all expected activity and resource tiles | Activity Chooser modal is open | 1. Observe the grid of activity/resource tiles on the Activity Chooser modal<br>2. Confirm tiles for Assignment, Forum, Quiz, File, Page, Lesson, SCORM, URL, and Workshop are present in the grid | All listed activity and resource tiles are visible in the Activity Chooser grid. | High |
| 6.CEMAC-032 | Open selected activity's creation form by selecting a tile and clicking 'Add' | Activity Chooser modal is open | 1. Select an activity/resource tile from the grid<br>2. Click "Add" | The creation form for the selected activity opens. | High |
| 6.CEMAC-033 | Each activity/resource tile displays a star/favorite toggle | Course page with activity/resource tiles visible | 1. Observe the grid of activity/resource tiles on the page<br>2. Verify each tile displays a star/favorite toggle control | Every tile in the grid shows a star/favorite toggle. | High |
| 6.CEMAC-034 | Mark an activity/resource tile as favorite using the star toggle | Course page with activity/resource tiles visible | 1. Click the star/favorite toggle on a chosen activity/resource tile<br>2. Verify the toggle visually indicates the tile is favorited | The tile's star toggle shows the favorited state after clicking. | High |
| 6.CEMAC-035 | Unmark a previously favorited activity/resource tile using the star toggle | At least one activity/resource tile is currently favorited and visible in the grid | 1. Click the star/favorite toggle on a previously favorited tile<br>2. Verify the toggle visually indicates the tile is no longer favorited | The tile's star toggle returns to the non-favorited state after clicking. | High |
| 6.CEMAC-036 | Add a subsection under a section | Edit mode is enabled and the course page is open | 1. Click the section's "+ Add a subsection" control<br>2. Fill all required fields for the new subsection (e.g., title) if prompted and click "Save" or "Add" | A new subsection is created as a child of the selected section, appears indented under the parent in the Course Index sidebar as nested content, and is highlighted as the active item. | High |
| 6.CEMAC-037 | Create a nested subsection within an existing subsection (two-level nesting) | Edit mode is enabled and the course page is open | 1. Add a subsection under a section (create first-level child) using the "+ Add a subsection" control and save<br>2. Click the newly created subsection's "+ Add a subsection" control, fill all required fields for the nested subsection, and click "Save" or "Add" | The second subsection is created as a child of the first subsection and the Course Index sidebar shows a two-level nested hierarchy reflecting parent -> child -> grandchild. | High |
| 6.CEMAC-038 | '+ Add a subsection' control creates a nested subsection in Edit mode | Course page is open with at least one section and user has teacher role | 1. Click the control to enable Edit mode on the current Course page<br>2. Click the '+ Add a subsection' control on a chosen section<br>3. Fill the required subsection details (title) and confirm creation | A new subsection is created and appears nested under the selected section in the course structure. | Medium |
| 6.CEMAC-039 | Section-level three-dot menu contains duplicate option | Edit mode is enabled and a course section row is visible | 1. Click the section-level three-dot menu for a section<br>2. Inspect the list of menu options | Section-level three-dot menu includes: edit, duplicate, hide, delete, move. | Medium |
| 6.CEMAC-040 | Duplicated section appears in Course Index sidebar and active highlighting is retained | Edit mode is enabled and the Course Index sidebar is open | 1. Duplicate a section using the section-level three-dot menu<br>2. Inspect the Course Index sidebar for the newly created section entry | The Course Index sidebar lists the duplicated section and the currently active item remains highlighted. | Medium |
| 6.CEMAC-041 | Section-level three-dot menu lists expected actions | Edit mode is enabled and a section is visible | 1. Click the section's three-dot menu<br>2. Verify the menu lists the available actions (edit, duplicate, hide, delete, move) | Menu contains edit, duplicate, hide, delete and move options | Medium |
| 6.CEMAC-042 | Activity-level three-dot menu shows all expected options including Move | Edit mode is enabled and activity-level inline controls are visible on the course page. | 1. Click the activity's three-dot menu<br>2. Observe the listed options in the menu | Menu lists the expected options: edit settings, move, duplicate, hide, set access restrictions, and delete. | Medium |
| 6.CEMAC-043 | Activity-level three-dot menu lists the Duplicate action | Edit mode is enabled and activity inline controls are visible | 1. Open the activity-level three-dot menu for a sample activity<br>2. Verify the menu contains the 'Duplicate' option among the listed actions | The 'Duplicate' option is present in the activity-level menu | Medium |
| 6.CEMAC-044 | Activity-level menu lists expected options including Hide | Edit mode enabled and a course page with at least one activity open | 1. Click the activity's three-dot menu<br>2. Inspect the menu options | Menu includes options: edit settings, move, duplicate, hide, set access restrictions, delete | Medium |
| 6.CEMAC-045 | Activity-level three-dot menu shows all expected options including set access restrictions | User is a teacher and the course page is open with activities visible | 1. Open the activity-level three-dot menu for an activity row | Menu lists edit settings, move, duplicate, hide, set access restrictions, and delete | Medium |
| 6.CEMAC-046 | Activity-level three-dot menu shows expected actions including Delete | Edit mode enabled on the course page and the target activity row is visible | 1. Open the activity-level three-dot menu for the target activity<br>2. Verify the menu lists the actions: edit settings, move, duplicate, hide, set access restrictions, and delete | All listed actions are present in the activity-level three-dot menu. | Medium |
| 6.CEMAC-047 | '+ Add an activity or resource' button is present at the bottom of each section | Edit mode is enabled on the course page | 1. For each visible course section, verify the '+ Add an activity or resource' button is visible at the bottom of the section | The '+ Add an activity or resource' button is visible at the bottom of every section. | Medium |
| 6.CEMAC-048 | Add opens the correct creation form matching the selected tile | Activity Chooser modal is open | 1. Select an activity/resource tile and note its label<br>2. Click "Add"<br>3. Verify the opened creation form's header and fields correspond to the selected activity/resource type | The displayed creation form matches the selected activity or resource type. | Medium |
| 6.CEMAC-049 | Mark multiple activity/resource tiles as favorites using their star toggles | Course page with multiple activity/resource tiles visible | 1. Click the star/favorite toggles on multiple distinct tiles in the grid<br>2. Verify each clicked tile displays the favorited state | All selected tiles show the favorited state after toggling their stars. | Medium |
| 6.CEMAC-050 | Create multiple sibling subsections under the same section | Edit mode is enabled and the course page is open | 1. Click the section's "+ Add a subsection" control, fill all required fields for the new subsection, and click "Save" or "Add"<br>2. Repeat the previous step to add a second subsection under the same parent section | Both subsections appear as child items of the parent section in the Course Index sidebar, listed as siblings beneath the parent and preserving hierarchical ordering. | Medium |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 6.CEMAC-051 | Authoring controls are not visible when Edit mode is disabled | Course page is open and Edit mode is disabled | 1. Ensure Edit mode is not enabled on the current Course page<br>2. Verify that section and activity rows do not display inline controls and that '+ Add an activity or resource' buttons are not present | Authoring inline controls and '+ Add an activity or resource' buttons are not visible when Edit mode is disabled. | Medium |
| 6.CEMAC-052 | Quick rename not available when inline controls are not present | Edit mode is disabled or inline controls are hidden on the course page. | 1. Verify no inline controls or edit icons are visible for sections or activities<br>2. Attempt to initiate a quick rename where the edit icon would normally appear | No edit icon is available and quick rename cannot be initiated. | Medium |
| 6.CEMAC-053 | Attempt to hide a section when inline controls are not present | Edit mode is not enabled and a section is visible | 1. Attempt to open the section's three-dot menu<br>2. Attempt to click "Hide" if the option is available | Hide action is not available because inline controls are not present | Medium |
| 6.CEMAC-054 | Cancel deletion retains the section | Edit mode is enabled and the target section is visible | 1. Open the section-level three-dot menu for the target section<br>2. Click "Delete"<br>3. Cancel the deletion in the confirmation dialog | The section remains on the course page and in the Course Index sidebar. | Medium |
| 6.CEMAC-055 | Delete option is not available when edit mode is disabled | Edit mode is disabled for the course | 1. Inspect a section row for inline controls<br>2. If a section-level three-dot menu is present, open it and verify the delete option is not listed | Section-level delete option is not available when edit mode is disabled. | Medium |
| 6.CEMAC-056 | Inline edit controls and 'Edit settings' are not available when edit mode is disabled | Edit mode is not enabled and the course page is open. | 1. Observe the section and activity rows for inline controls<br>2. Attempt to open the activity-level three-dot menu for an activity | Inline edit controls are not present and the 'Edit settings' option is not available. | Medium |
| 6.CEMAC-057 | Attempt to initiate move when the activity-level menu does not include the Move option | Edit mode is enabled and the activity's three-dot menu is visible but the Move option is not present. | 1. Click the activity's three-dot menu<br>2. Verify whether the "Move" option is present in the menu | Move action cannot be initiated from the activity-level menu because the Move option is not available. | Medium |
| 6.CEMAC-058 | Attempt to access activity-level move when inline controls are not present on rows | Edit mode is disabled or inline controls are not present for sections and activities on the course page. | 1. Observe whether inline controls (including the activity-level three-dot menu) are present on section and activity rows<br>2. If inline controls are absent, attempt to open the activity-level three-dot menu | Activity-level three-dot menu and its Move option are not available when inline controls are not present; user cannot initiate a move from the activity row. | Medium |
| 6.CEMAC-059 | Attempt to duplicate activity when inline controls are not visible | Edit mode is disabled and activity inline controls are not visible | 1. Attempt to open the activity-level three-dot menu for the target activity | The activity-level three-dot menu (and therefore the Duplicate action) is not available when inline controls are not visible | Medium |
| 6.CEMAC-060 | Hide option not available when inline controls are not present (Edit mode disabled) | Edit mode disabled and a course page with activities open | 1. Verify inline controls are not shown on section and activity rows<br>2. Attempt to open the activity-level three-dot menu (if present) and inspect options | The "Hide" option is not available in the activity-level menu | Medium |
| 6.CEMAC-061 | Failure: 'Set access restrictions' option missing from activity menu | User is a teacher and the course page is open with activities visible | 1. Open the activity-level three-dot menu for an activity row<br>2. Check the list of menu options for presence of the access restrictions option | "Set access restrictions" option is not present and cannot be selected | Medium |
| 6.CEMAC-062 | Attempt to delete activity when inline controls are not present | Edit mode disabled on the course page and the target activity row is visible | 1. Verify inline controls are not present on the activity row<br>2. Attempt to open the activity-level three-dot menu for the target activity | The delete action is not available because activity-level inline controls are not present. | Medium |
| 6.CEMAC-063 | Attempt bulk action with no activities selected | Edit mode enabled and course page displays activities | 1. Ensure no activity selection checkboxes are selected<br>2. Attempt to invoke a bulk action from the bulk actions toolbar | Bulk actions are disabled or a prompt indicates activities must be selected before performing batch operations. | Medium |
| 6.CEMAC-064 | Activity Chooser modal does not open when '+ Add an activity or resource' is clicked | Edit mode is enabled on the course page | 1. Click the '+ Add an activity or resource' button at the bottom of a section | The Activity Chooser modal does not open and no chooser is displayed. | Medium |
| 6.CEMAC-065 | Section missing '+ Add an activity or resource' button | Edit mode is enabled on the course page | 1. Inspect a course section and confirm the '+ Add an activity or resource' button is not visible at the bottom of that section | The section does not show the '+ Add an activity or resource' button and cannot open the Activity Chooser from that section. | Medium |
| 6.CEMAC-066 | Submit with all required fields empty | Activity Chooser modal is open | 1. Leave the search field empty<br>2. Trigger the search action (press Enter or click the search icon) | Validation errors shown for all required fields. | Medium |

#### Edge Case Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 6.CEMAC-067 | Edge case: Attempt to access set access restrictions when inline controls are not present | User is a teacher and the course page is open with activities visible and edit mode disabled | 1. Open the activity-level three-dot menu for an activity row<br>2. Attempt to activate or open the access restrictions control | Access restrictions action is not available because inline controls are not present | Medium |
| 6.CEMAC-068 | Bulk actions toolbar not available when only one activity is selected | Edit mode enabled and multiple activities visible in the course | 1. Select exactly one activity using its selection checkbox<br>2. Observe whether the bulk actions toolbar is presented or remains hidden/disabled | Bulk actions toolbar is not presented or batch actions remain disabled when only one activity is selected. | Medium |
| 6.CEMAC-069 | Filter bar contains only the documented categories | Activity Chooser modal is open | 1. List the visible options in the category filter bar<br>2. Verify there are no additional category options beyond All, Activities, Resources, and Recommended | Only the documented category options (All, Activities, Resources, Recommended) appear in the filter bar. | Medium |
| 6.CEMAC-070 | Toggling Edit mode off removes inline controls and authoring buttons | Course page is open, user has teacher role, and Edit mode is currently enabled | 1. Click the control to disable Edit mode on the current Course page<br>2. Verify that inline controls, edit icons, the bulk actions toolbar, '+ Add an activity or resource' buttons, and '+ Add a subsection' controls are no longer visible | Disabling Edit mode returns the Course page to its regular view and hides all authoring controls and buttons. | Low |

---

### Assignment Creation

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 7.ASSCRE-001 | Create assignment and Save and return to course redirects to course page and lists assignment | Assignment creation form is open | 1. Fill all required fields (Assignment name) and optionally fill Description and select desired Submission types and Feedback types<br>2. If using file submissions, enable File submissions and populate the revealed file controls (maximum number of uploaded files, maximum submission size, accepted file types)<br>3. Click "Save and return to course" | The assignment is created; the user is redirected to the course page; the new assignment appears in the course listing and in the Course Index sidebar with the item highlighted | High |
| 7.ASSCRE-002 | Create an assignment and open its page using Save and display | None | 1. Fill all required fields (Assignment name) and set desired options (Description, Submission types, Availability, Grade as applicable)<br>2. Click "Save and display" | The assignment is created and the new assignment's page is opened for viewing/editing; the Course Index highlights the new assignment as the active item. | High |
| 7.ASSCRE-003 | Edit an existing assignment's details from its page | An assignment exists and its detail page is open. | 1. Click "Edit"<br>2. Modify one or more editable fields<br>3. Click "Save and display" | The assignment detail page reflects the updated values. | High |
| 7.ASSCRE-004 | Cancel with empty assignment form returns to previous context without creating assignment | Assignment creation form is open | 1. Ensure all fields remain in their initial empty/default state<br>2. Click the "Cancel" button | User is returned to the previous context (e.g., course page) and no assignment is created. | High |
| 7.ASSCRE-005 | Cancel after making edits discards all changes (triggerable after filling fields, uploading files, changing settings) | Assignment creation form is open | 1. Fill all required fields (Assignment name) and optional fields (Description, Tag entry field)<br>2. Upload one or more additional files and change several settings (enable toggles, set availability dates, select submission types and feedback options)<br>3. Click the "Cancel" button | User is returned to the previous context, no assignment is created, and none of the entered data or uploaded files are saved. | High |
| 7.ASSCRE-006 | Submission types shows Online text and File submissions checkboxes | Assignment creation form is open | 1. Inspect the Submission types section on the form | Submission types contains checkboxes for Online text and File submissions | Medium |
| 7.ASSCRE-007 | Enabling File submissions reveals file-related controls | Assignment creation form is open | 1. Check the File submissions checkbox in the Submission types section | Controls for maximum number of uploaded files, maximum submission size, and accepted file types become visible | Medium |
| 7.ASSCRE-008 | + Add restriction button opens restriction-type picker | Assignment creation form is open | 1. Click the "+ Add restriction" button in the Access restrictions panel | A restriction-type picker is displayed | Medium |
| 7.ASSCRE-009 | Submission types show Online text and File submissions checkboxes | Assignment creation form is open | 1. Expand the "Submission types" panel<br>2. Observe that Online text and File submissions checkboxes are present | The "Submission types" panel contains checkboxes for Online text and File submissions. | Medium |
| 7.ASSCRE-010 | Enabling File submissions reveals file-related controls | Assignment creation form is open | 1. Expand the "Submission types" panel<br>2. Enable the File submissions checkbox<br>3. Observe the visibility of maximum number of uploaded files, maximum submission size, and accepted file types controls | Enabling File submissions reveals controls for maximum number of uploaded files, maximum submission size, and accepted file types. | Medium |
| 7.ASSCRE-011 | + Add restriction button opens restriction-type picker | Assignment creation form is open | 1. Expand the "Access restrictions" panel<br>2. Click the "+ Add restriction" button | A restriction-type picker is displayed. | Medium |
| 7.ASSCRE-012 | Assignment detail page shows breadcrumbs with clickable course navigation segments | An assignment's detail page is open | 1. Observe the breadcrumbs at the top of the page showing the navigation path from the course<br>2. Click a breadcrumb segment link | Breadcrumb segments are clickable and navigating via a breadcrumb link opens the corresponding parent page. | Medium |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 7.ASSCRE-013 | Submit with all required fields empty | Assignment creation form is open | 1. Leave all required fields empty<br>2. Click "Save and return to course" | Validation errors shown for all required fields and the assignment is not saved | Medium |
| 7.ASSCRE-014 | Submit with all required fields empty | None | 1. Leave all required fields empty<br>2. Click "Save and display" | Validation errors shown for all required fields. | Medium |
| 7.ASSCRE-015 | Submit with Assignment name empty | None | 1. Fill all other required fields, leave Assignment name empty<br>2. Click "Save and display" | Validation error indicating Assignment name is required. | Medium |

#### Edge Case Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 7.ASSCRE-016 | Save without entering Due date when Due date toggle is disabled still creates assignment | Assignment creation form is open | 1. Fill all required fields (Assignment name) and ensure the Due date Enable toggle is switched off<br>2. Click "Save and return to course" | The assignment is created and the user is redirected to the course page; no due date enforcement is applied | Medium |
| 7.ASSCRE-017 | Cancel discards all changes when advanced panels and multiple settings are modified | Assignment creation form is open | 1. Expand multiple collapsible panels (Availability, Submission types, Feedback types, Grade, Access restrictions, Activity completion) and modify fields across them (set dates, toggle options, change grade settings, add a restriction)<br>2. Click the "Cancel" button | User is returned to the previous context and none of the modifications in the expanded panels are persisted; no assignment is created. | Medium |
| 7.ASSCRE-018 | Disable Due date toggle excludes that date from enforcement when saved | None | 1. In the "Availability" panel, disable the Due date Enable toggle<br>2. Fill all required fields (Assignment name)<br>3. Click "Save and display" | The assignment is created and the disabled Due date is not enforced for the assignment. | Low |

---

### Course Settings

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 8.COUSET-001 | Save and display persists all course settings and returns to course page | Course Settings form is open | 1. Fill all required fields (Course full name, Course short name, Course category) and configure additional fields (Course visibility, Course start date, Course ID number, Course summary, Course format, appearance settings, Maximum upload size, Completion tracking, Tags)<br>2. Click "Save and display" | All configured settings are persisted, the user is returned to the course page, and the course page reflects the saved settings. | High |
| 8.COUSET-002 | Select course format, configure format-specific layout controls, and Save and display persists format and layout | Course Settings form is open | 1. Fill all required fields (Course full name, Course short name, Course category), select a Course format that exposes layout controls, and configure the visible layout controls<br>2. Click "Save and display" | The selected course format and its format-specific layout settings are persisted and applied on the course page. | High |
| 8.COUSET-003 | Cancel discards a single text-field change | Course Settings form is open with the current course settings displayed. | 1. Modify Course full name field<br>2. Click "Cancel" | Course Settings form closes and the course's full name remains unchanged. | High |
| 8.COUSET-004 | Cancel discards multiple field changes including dropdowns and toggles | Course Settings form is open with the current course settings displayed. | 1. Modify multiple fields (Course short name, Course category, Course visibility, toggle Completion tracking)<br>2. Click "Cancel" | Form closes and all modified fields remain at their previous values. | High |
| 8.COUSET-005 | Cancel discards format change and its dependent layout adjustments | Course Settings form is open with the current course settings displayed. | 1. Change Course format and modify layout controls that appear for that format<br>2. Click "Cancel" | Form closes and course format and layout settings remain unchanged. | High |
| 8.COUSET-006 | Cancel discards uploaded image and rich-text summary edits | Course Settings form is open with the current course settings displayed. | 1. Upload a Course image and edit Course summary in the rich text editor<br>2. Click "Cancel" | Form closes and the course image and summary remain as they were before editing. | High |
| 8.COUSET-007 | Save and display persists uploaded course image | Course Settings form is open | 1. Fill all required fields (Course full name, Course short name, Course category) and upload a valid Course image<br>2. Click "Save and display" | Uploaded course image is persisted and is displayed on the course page. | Medium |
| 8.COUSET-008 | Enable end date and Save and display persists the end date | Course Settings form is open | 1. Fill all required fields (Course full name, Course short name, Course category), enable the Course end date toggle and set a valid end date<br>2. Click "Save and display" | The enabled end date is persisted and the course page displays the configured end date. | Medium |
| 8.COUSET-009 | Configure group mode and grouping and Save and display persists group settings | Course Settings form is open | 1. Fill all required fields (Course full name, Course short name, Course category), set Group mode and select a Grouping if applicable<br>2. Click "Save and display" | Group mode and grouping selection are saved and the course page or settings reflect the configured group settings. | Medium |
| 8.COUSET-010 | Modify appearance settings and Save and display persists appearance preferences | Course Settings form is open | 1. Fill all required fields (Course full name, Course short name, Course category) and modify Appearance settings (language, news items, activity dates, completion conditions display, Maximum upload size)<br>2. Click "Save and display" | Appearance preferences are persisted and the course page reflects the updated appearance settings. | Medium |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 8.COUSET-011 | Submit with all required fields empty | Course Settings form is open | 1. Leave all required fields empty<br>2. Click "Save and display" | Validation errors shown for all required fields. | Medium |
| 8.COUSET-012 | Save with missing format-dependent controls triggers inline validation | Course Settings form is open | 1. Fill all required fields (Course full name, Course short name, Course category), select a Course format that requires additional format-specific controls, and leave those format-dependent controls blank<br>2. Click "Save and display" | Inline validation errors are shown for the missing format-specific controls and save is blocked. | Medium |

#### Edge Case Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 8.COUSET-013 | Cancel after enabling end date and setting dates discards enabled state and dates | Course Settings form is open with the current course settings displayed. | 1. Enable Course end date and fill in start and end dates<br>2. Click "Cancel" | Form closes and the end date enable state and date values remain unchanged. | Medium |
| 8.COUSET-014 | Cancel does not perform validation and still discards unsaved invalid entries | Course Settings form is open with the current course settings displayed. | 1. Clear or enter invalid values in required fields (so the form would be invalid if saved)<br>2. Click "Cancel" | Form closes without blocking on validation and the course settings remain unchanged. | Medium |

---

### Participants Management

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 9.PARMAN-001 | Confirm enrollment adds selected user with chosen role | Participants management panel is open and enrollment dialog is available | 1. Click "Enrol users" button<br>2. Fill all required fields (user search field, Role dropdown)<br>3. Click "Confirm" in the enrollment dialog | Selected user is added to the course and appears in the participants list with the assigned role. | High |
| 9.PARMAN-002 | Confirm enrollment with enrollment duration set | Participants management panel is open and enrollment dialog is available | 1. Click "Enrol users" button<br>2. Fill all required fields and set an enrollment duration (user search field, Role dropdown, Enrollment duration control)<br>3. Click "Confirm" in the enrollment dialog | Selected user is added to the course with the assigned role and the specified enrollment duration is recorded. | High |
| 9.PARMAN-003 | Apply a single built filter condition | A single filter condition is already built and visible in the filter panel. | 1. Verify the filter panel shows a single configured condition<br>2. Click "Apply filters" | Participants list is narrowed to display only participants matching the built condition. | High |
| 9.PARMAN-004 | Apply multiple built filter conditions with 'Any' toggle off | Multiple filter conditions are already built and the 'Any' toggle is off. | 1. Verify the filter panel shows multiple configured conditions and the 'Any' toggle is off<br>2. Click "Apply filters" | Participants list is filtered according to all built conditions. | High |
| 9.PARMAN-005 | Apply multiple built filter conditions with 'Any' toggle on | Multiple filter conditions are already built and the 'Any' toggle is on. | 1. Verify the filter panel shows multiple configured conditions and the 'Any' toggle is on<br>2. Click "Apply filters" | Participants list is filtered according to the built conditions, respecting the 'Any' toggle state. | High |
| 9.PARMAN-006 | Build filter conditions using controls and then apply filters | Filter panel and participants list are visible. | 1. Use the Select attribute dropdown to choose an attribute and configure its condition, click "+ Add condition" and configure an additional condition, set the 'Any' toggle as desired<br>2. Click "Apply filters" | Participants list is narrowed according to the newly built filter conditions. | High |
| 9.PARMAN-007 | Clear filters removes all built filter conditions and restores unfiltered participants list | At least one filter condition is applied using the available filter controls | 1. Click the "Clear filters" button | All filter conditions are removed, the "Any" toggle and Select attribute dropdown return to their default states, no additional condition rows remain, and the participants list shows the unfiltered set. | High |
| 9.PARMAN-008 | Clear filters restores participants list count to pre-filter state | A filter is applied that reduces the visible participants list | 1. Record the participant count while the filter is applied<br>2. Click the "Clear filters" button | Participant count returns to the unfiltered total and the participants listing reflects the full unfiltered set. | High |
| 9.PARMAN-009 | Filter participants list by selecting an enrollment context | Participants page is open and the participants list and enrolled-users scope dropdown are visible | 1. Click the enrolled-users scope dropdown and select an enrollment context option<br>2. Observe the participants list contents | The participants list updates to show only users who belong to the selected enrollment context. | High |
| 9.PARMAN-010 | Filter participants by First name initial | Participants management list is visible with multiple participants having varied first-name initials. | 1. Click any First name alphabetical button for a specific letter<br>2. Observe the participants list | Participants list displays only participants whose First name begins with the selected letter. | High |
| 9.PARMAN-011 | Show all participants using the First name 'All' button | Participants management list is visible and a first-name alphabetical filter may currently be active. | 1. Click the First name "All" alphabetical button<br>2. Observe the participants list | Participants list displays all participants (no initial-based filtering applied). | High |
| 9.PARMAN-012 | Filter participants by a Last name initial | Participants list is visible and Last name alphabetical filter controls are displayed | 1. Click a Last name alphabetical filter button for a specific letter<br>2. Observe the participants list | Only participants whose last name starts with the selected letter are displayed in the list | High |
| 9.PARMAN-013 | Reset Last name filter using the 'All' button | A Last name alphabetical filter is currently active and the 'All' button is visible | 1. Click a Last name alphabetical filter button for a specific letter<br>2. Click the Last name 'All' filter button | Participants list returns to showing all participants (filter cleared) | High |
| 9.PARMAN-014 | Apply a bulk action to checked participants | Participants list is visible with multiple participants | 1. Check the row checkboxes for one or more participants to select them<br>2. Select the desired bulk action from the "With selected users…" dropdown<br>3. Confirm any confirmation prompt if presented | The chosen bulk action is applied to each checked participant and the participant listing reflects the changes. | High |
| 9.PARMAN-015 | Sort participants list by First/Last name ascending | Participants list is visible with multiple participants having distinct names. | 1. Click the "First/Last name" column header | Participants list is ordered alphabetically by name in ascending order. | High |
| 9.PARMAN-016 | Toggle First/Last name column sort to descending | Participants list is visible with multiple participants having distinct names. | 1. Click the "First/Last name" column header<br>2. Click the "First/Last name" column header again | Participants list is ordered alphabetically by name in descending order. | High |
| 9.PARMAN-017 | Apply a single filter condition | None | 1. Build a single filter condition (select an attribute from the Select attribute dropdown and provide matching criteria)<br>2. Click "Apply filters" | Participants list displays only participants matching the single condition. | High |
| 9.PARMAN-018 | Apply multiple filter conditions combined using the Any toggle | None | 1. Build multiple filter conditions (for each condition: select an attribute from the Select attribute dropdown and provide matching criteria)<br>2. Enable the "Any" toggle<br>3. Click "Apply filters" | Participants list displays participants that match any of the built conditions. | High |
| 9.PARMAN-019 | Apply multiple filter conditions combined without the Any toggle (all conditions required) | None | 1. Build multiple filter conditions (for each condition: select an attribute from the Select attribute dropdown and provide matching criteria)<br>2. Ensure the "Any" toggle is disabled<br>3. Click "Apply filters" | Participants list displays participants that match all of the built conditions. | High |
| 9.PARMAN-020 | Open enrollment dialog via Enrol users button | Participants management panel is open | 1. Click "Enrol users" button | The enrollment dialog opens, allowing user and role selection. | Medium |
| 9.PARMAN-021 | First-name filter updates when selecting a different letter | Participants management list is visible with participants having multiple first-name initials. | 1. Click any First name alphabetical button for a specific letter<br>2. Click a different First name alphabetical button for another letter<br>3. Observe the participants list after each selection | Participants list updates to reflect the currently selected letter, showing only participants whose First name begins with the newly selected letter. | Medium |
| 9.PARMAN-022 | First name alphabetical buttons (All and A–Z) are present | Participants management list is visible. | 1. Locate the First name alphabetical filter area<br>2. Verify presence of the "All" button and alphabetical buttons representing A through Z | First name alphabetical filter area contains an "All" button and buttons for each letter A–Z. | Medium |
| 9.PARMAN-023 | Apply a different Last name initial updates the participants list | Participants list is visible and a Last name filter can be applied | 1. Click a Last name alphabetical filter button for a specific letter<br>2. Click a different Last name alphabetical filter button for another letter | Participants list updates to show only participants whose last name starts with the newly selected letter | Medium |
| 9.PARMAN-024 | Filtered participant rows show First and Last name as profile links | Participants list is visible and Last name alphabetical filter controls are displayed | 1. Click a Last name alphabetical filter button for a specific letter<br>2. Inspect each displayed participant row for First and Last name elements | Each displayed participant's First and Last name appears as a clickable link to the participant profile | Medium |
| 9.PARMAN-025 | Participant name links remain functional after sorting | Participants list is visible with at least one participant. | 1. Click the "First/Last name" column header<br>2. Click a participant's name link in the sorted list | The participant's profile page opens. | Medium |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 9.PARMAN-026 | Submit with all required fields empty | Participants management panel is open and enrollment dialog is visible | 1. Leave all required fields empty<br>2. Click "Confirm" in the enrollment dialog | Validation errors shown for all required fields. | Medium |
| 9.PARMAN-027 | Apply bulk action with no participants selected | Participants list is visible with multiple participants | 1. Leave all row checkboxes unchecked<br>2. Select a bulk action from the "With selected users…" dropdown | No participants are affected; the bulk action does not change any participant records (UI shows no changes or an appropriate message). | Medium |

#### Edge Case Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 9.PARMAN-028 | Selecting a letter with no matching First names yields no results | Participants management list is visible and no participant has a First name starting with the test letter. | 1. Click a First name alphabetical button for a letter that has no matching participants<br>2. Observe the participants list area | Participants list shows no entries (or a no-results message) indicating there are no participants whose First name begins with the selected letter. | Medium |
| 9.PARMAN-029 | Only checked participants are affected by the bulk action | Participants list is visible with at least two participants | 1. Check the row checkboxes for a subset of participants leaving others unchecked<br>2. Select a bulk action from the "With selected users…" dropdown<br>3. Confirm any confirmation prompt if presented | The bulk action is applied only to the checked participants; unchecked participants remain unchanged in the listing. | Medium |
| 9.PARMAN-030 | Apply filters with no conditions built | None | 1. Ensure no filter conditions are present (no attributes selected and no conditions added)<br>2. Click "Apply filters" | No filtering is applied and the participants list remains unchanged. | Medium |
| 9.PARMAN-031 | Confirm enrollment leaving optional duration empty | Participants management panel is open and enrollment dialog is available | 1. Click "Enrol users" button<br>2. Fill all required fields, leave the Enrollment duration control empty (user search field, Role dropdown)<br>3. Click "Confirm" in the enrollment dialog | Selected user is added to the course with the assigned role and no enrollment duration is set. | Low |
| 9.PARMAN-032 | Apply filters with no filter conditions present | No filter conditions are built. | 1. Ensure the filter panel has no conditions configured<br>2. Click "Apply filters" | Participants list remains unfiltered and all participants are displayed. | Low |
| 9.PARMAN-033 | Apply filters when conditions match no participants | At least one built filter condition exists that matches no participants. | 1. Ensure a built filter condition is present that should match no participants<br>2. Click "Apply filters" | No participants are displayed and an appropriate 'no results' indicator is shown. | Low |
| 9.PARMAN-034 | Click Clear filters when no filter conditions exist (idempotent) | No filter conditions are present | 1. Confirm no filter conditions are present<br>2. Click the "Clear filters" button | No error is shown, filter controls remain at default states, and the participants list remains unchanged (still unfiltered). | Low |
| 9.PARMAN-035 | Selecting an enrollment context that has no enrolled users shows empty results | Participants page is open and the enrolled-users scope dropdown is visible | 1. Click the enrolled-users scope dropdown and select an enrollment context known to have no enrolled users<br>2. Observe the participants list area | The participants list displays no user rows and shows the appropriate empty-state indication for no matching users. | Low |

---

### Assignment — Teacher View

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 10.A—TV-001 | Assignment view displays metadata, description, and attachments | Assignment page is open and user is a teacher | 1. Verify the Opened date is visible in the assignment metadata area<br>2. Verify the Due date is visible in the assignment metadata area<br>3. Verify the full Description is visible<br>4. Verify any attached files are listed under the Description | Assignment page shows Opened date, Due date, full Description, and any attached files. | High |
| 10.A—TV-002 | Click Grade button opens grading interface for individual students | Assignment page is open and user is a teacher | 1. Click the "Grade" button<br>2. Verify the grading interface for individual students is displayed and active | Grading interface for individual students opens. | High |
| 10.A—TV-003 | Grading summary panel displays read-only metrics | Grading interface for the assignment is open and user is a teacher | 1. Locate the Grading summary panel<br>2. Verify Number of participants, Number of submissions, Needs grading, Visibility, and Time remaining are displayed with values | Grading summary panel shows Number of participants, Number of submissions, Needs grading, Visibility, and Time remaining. | High |
| 10.A—TV-004 | Settings tab opens teacher settings for the assignment | Assignment page is open and user is a teacher | 1. Locate the tab bar below the grading summary<br>2. Click the "Settings" tab<br>3. Verify the Settings content for the assignment is displayed | Settings tab content is displayed for the teacher. | Medium |
| 10.A—TV-005 | Submissions tab shows submissions list and reflects submission count | Assignment page is open and user is a teacher | 1. Click the "Submissions" tab in the tab bar<br>2. Verify the submissions list is displayed and entries are visible<br>3. Verify the displayed number of submissions is present in the Submissions tab header or list and corresponds to the summary metric | Submissions tab displays the submissions list and the number of submissions is visible. | Medium |
| 10.A—TV-006 | Advanced grading tab opens advanced grading options | Assignment page is open and user is a teacher | 1. Click the "Advanced grading" tab in the tab bar<br>2. Verify the advanced grading interface or options are displayed | Advanced grading interface/options are displayed. | Medium |
| 10.A—TV-007 | Breadcrumbs show full navigation path with clickable segments | An activity (assignment) page is open | 1. Locate the breadcrumbs at the top of the activity page<br>2. Verify the full navigation path is displayed and each breadcrumb segment is clickable | Breadcrumbs display the full navigation path and each segment is a clickable link. | Medium |
| 10.A—TV-008 | More tab reveals additional assignment actions | Assignment page is open and user is a teacher | 1. Click the "More" tab in the tab bar<br>2. Verify the More menu or additional action items are displayed | More tab opens and displays additional assignment actions or options. | Low |

---

### Assignment Submissions

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 11.ASSSUB-001 | Narrow submissions by student name | Submissions table is visible. | 1. Enter a student's full name into the student name search field<br>2. Apply the search/filter controls | Table shows only submission rows for that student; each visible row corresponds to that student's submissions and displays student identity. | High |
| 11.ASSSUB-002 | Narrow submissions by submission status | Submissions table is visible and submission status filter is available. | 1. Select a submission status value in the submission status filter<br>2. Apply the filter controls | Table shows only rows with the selected submission status and each row displays the submission status value. | High |
| 11.ASSSUB-003 | Narrow submissions by grading status | Submissions table is visible and grading status filter is available. | 1. Select a grading status value in the grading status filter<br>2. Apply the filter controls | Table shows only rows with the selected grading status and each row displays the grading status value. | High |
| 11.ASSSUB-004 | Narrow submissions using student name plus submission and grading status filters | Submissions table is visible and multiple filters are available. | 1. Enter a student's name into the student name search field and select values for submission status and grading status<br>2. Apply the filters | Table shows only submission rows that match all selected criteria (student name, submission status, and grading status). | High |
| 11.ASSSUB-005 | Open grading workflow from a submission row action menu | At least one submission row is visible. | 1. Click the action menu for a visible submission row<br>2. Select the grading action from the menu | The grading workflow opens for that student. | High |
| 11.ASSSUB-006 | Submissions table displays student submission records | Submissions view is open | 1. Observe the Submissions table on the page | The Submissions table lists student submission records (one row per student). | High |
| 11.ASSSUB-007 | Enable Quick grading mode shows inline grade inputs | Submissions view is open | 1. Click the 'Quick grading' mode toggle<br>2. Verify inline grade input fields appear and become editable within the submissions table | Inline grade input fields are available and editable in the table when Quick grading is enabled. | High |
| 11.ASSSUB-008 | Enter a final grade inline in Submissions table (Quick grading enabled) | Quick grading mode is enabled and the Submissions table is visible | 1. Click the Final grade cell for a student's row to activate inline edit<br>2. Enter a valid final grade and commit the change (press Enter or click the inline Save control)<br>3. Verify the Final grade cell displays the entered grade | The entered final grade is saved and shown in the student's Final grade cell. | High |
| 11.ASSSUB-009 | Edit an existing inline final grade and save the update | Quick grading mode is enabled and a student row already has a Final grade | 1. Click the student's Final grade cell to enable inline edit<br>2. Modify the grade value and commit the change<br>3. Verify the table row displays the updated grade value | The updated final grade is saved and displayed in the table. | High |
| 11.ASSSUB-011 | Submissions table displays expected columns and student identity links | Submissions table is visible with at least one row. | 1. Inspect a visible submission row and its columns | Each row displays student identity (name and initials icon) with a link to the student's profile, submission status, grading status, submission date/time, submission preview or file links, submission comments, feedback/comments or files if present, final grade, and an action menu. | Medium |
| 11.ASSSUB-012 | Disable Quick grading mode hides or makes inline grade inputs read-only | Submissions view is open and Quick grading mode may be enabled | 1. If Quick grading is enabled, click the 'Quick grading' mode toggle to disable it<br>2. Verify inline grade input fields are removed or are no longer editable in the submissions table | Inline grade input fields are not editable or are not present when Quick grading is disabled. | Medium |
| 11.ASSSUB-013 | Submissions table displays student records with expected columns | Submissions view is open and contains student submission records | 1. Inspect the Submissions table<br>2. Verify each row corresponds to a student and the table shows columns including Final grade, Submission status, Grading status, and Submission date/time | The Submissions table lists student submission records and includes the expected columns. | Medium |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 11.ASSSUB-014 | Filter by student name that matches no records | Submissions table is visible. | 1. Enter a student name that does not match any submission record into the student name search field<br>2. Apply the search/filter controls | No submission rows are displayed (no matches found). | Medium |
| 11.ASSSUB-015 | Combine filters that result in no submissions | Submissions table is visible and multiple filters are available. | 1. Enter a student's name and select submission and/or grading status values that do not apply to that student<br>2. Apply the filters | No submission rows are displayed (no matches found for the combination). | Medium |
| 11.ASSSUB-016 | Attempt inline grade entry when Quick grading is disabled | Submissions view is open and Quick grading is disabled | 1. Attempt to focus and type a grade into a submissions row's grade cell<br>2. Confirm that the cell does not accept input or is not editable | Inline grade entry is not permitted while Quick grading mode is disabled. | Medium |
| 11.ASSSUB-017 | Submit with all required fields empty | Quick grading mode is enabled and the Submissions table is visible | 1. Leave all inline grade fields empty for one or more student rows<br>2. Click the control to save or apply quick grading changes | Validation errors shown for all required fields. | Medium |

#### Edge Case Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 11.ASSSUB-010 | Attempt inline grade entry when Quick grading mode is disabled | Quick grading mode is disabled and the Submissions table is visible | 1. Attempt to click the Final grade cell for a student's row<br>2. Observe whether an inline editor appears or the cell remains read-only | Inline editing is not available and Final grade cells remain read-only when Quick grading is disabled. | High |
| 11.ASSSUB-018 | Partial student name search returns matching subset of submissions | Submissions table is visible and there are multiple students with similar names. | 1. Enter a partial student name into the student name search field<br>2. Apply the search/filter controls | Table shows submission rows for students whose names match the partial text. | Low |
| 11.ASSSUB-019 | Enable Quick grading with multiple submission rows shows inline inputs for visible rows | Submissions view is open and contains multiple student submission rows | 1. Click the 'Quick grading' mode toggle<br>2. Verify inline grade input fields are present for multiple visible rows in the submissions table | Inline grade inputs are available for each visible submission row when Quick grading is enabled. | Low |

---

### Gradebook — Grader Report

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 12.G—GR-001 | Switch to Grader report via report-type selector | Gradebook page is open and the report-type selector dropdown is visible | 1. Click the report-type selector dropdown<br>2. Select the Grader report option from the dropdown<br>3. Observe the page content and the selector's displayed value | The Grader report view is displayed and the report-type selector shows Grader report | High |
| 12.G—GR-002 | Switch to User report via report-type selector | Gradebook page is open and the report-type selector dropdown is visible | 1. Click the report-type selector dropdown<br>2. Select the User report option from the dropdown<br>3. Observe the page content and the selector's displayed value | The User report view is displayed and the report-type selector shows User report | High |
| 12.G—GR-003 | Switch to Overview report via report-type selector | Gradebook page is open and the report-type selector dropdown is visible | 1. Click the report-type selector dropdown<br>2. Select the Overview report option from the dropdown<br>3. Observe the page content and the selector's displayed value | The Overview report view is displayed and the report-type selector shows Overview report | High |
| 12.G—GR-004 | Narrow grader rows by student name using User search | Grader report is open and grade table contains multiple enrolled students across groups. | 1. Enter a student name into the User search field<br>2. Trigger the search control (e.g., press Enter or click search) | Grade table displays only enrolled students whose names match the search query; non-matching rows are hidden. | High |
| 12.G—GR-005 | Narrow grader rows by selected group using filter controls | Grader report is open and grade table contains enrolled students assigned to multiple groups. | 1. Open the group filter control and select a group<br>2. Apply the group filter if an explicit apply action is required | Grade table displays only enrolled students who belong to the selected group; students in other groups are hidden. | High |
| 12.G—GR-006 | Narrow grader rows by student name within a selected group | Grader report is open and grade table contains enrolled students across groups. | 1. Select a group in the group filter control<br>2. Enter a student name into the User search field and trigger the search control | Grade table displays only enrolled students who both belong to the selected group and match the name search. | High |
| 12.G—GR-007 | Edit an activity's grade settings via per-column action menu | Grader report is open and user has teacher privileges. | 1. Open the per-column action menu in the target activity's column header<br>2. Click "Edit grade settings"<br>3. Modify one or more editable settings in the grade settings form<br>4. Click "Save" or "Submit" | Changes are saved and the activity's grade settings are updated and reflected in the grader report. | High |
| 12.G—GR-008 | Per-column action menu present on each column header and shows Edit option | Grader report is open and user has teacher privileges. | 1. For two different activity column headers: open the per-column action menu<br>2. Verify the menu contains an "Edit grade settings" option for each opened menu | Each column header's per-column action menu includes an "Edit grade settings" option. | High |
| 12.G—GR-009 | Edit a single student's grade via per-cell three-dot menu and save valid value | Grader report page is open and the grade table with per-cell three-dot menus is visible | 1. Click the per-cell three-dot menu for the target student's activity cell<br>2. Click "Edit" in the per-cell menu<br>3. Fill the grade value with a valid value within the configured grade range<br>4. Click "Save" or confirm the edit | The grade cell displays the updated value and no inline out-of-range flag is shown; the table reflects the persisted change. | High |
| 12.G—GR-010 | Enable Edit mode makes grade cells editable | User is a teacher and the Grader report page is open. | 1. Click "Edit mode" to enable editing<br>2. Attempt to edit a grade cell by entering a valid grade value | The grade cell enters an edit state and accepts input. | High |
| 12.G—GR-011 | Save changes applies inline edits and updates overall average | User is a teacher and the Grader report page is open. | 1. Click "Edit mode" to enable editing<br>2. Edit one or more grade cells with valid grade values<br>3. Click "Save changes" | Edited grades are applied to the grade table and the overall average row updates to reflect the saved changes. | High |
| 12.G—GR-012 | Overall average row displays class average per activity | User is a teacher and the Grader report page is open. | 1. Locate the overall average row at the bottom of the grade table<br>2. Observe the displayed averages for each activity | The overall average row shows the class average for each activity. | High |
| 12.G—GR-014 | Cancel a per-cell grade edit leaves original grade unchanged | Grader report page is open and the grade table with per-cell three-dot menus is visible | 1. Click the per-cell three-dot menu for the target student's activity cell<br>2. Click "Edit" in the per-cell menu<br>3. Modify the grade value<br>4. Click "Cancel" or close the edit without saving | The grade cell retains the original value and no changes are applied. | Medium |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 12.G—GR-013 | Prevent saving when an edited grade is outside configured range | User is a teacher and the Grader report page is open. | 1. Click "Edit mode" to enable editing<br>2. Enter an out-of-range value into a grade cell<br>3. Click "Save changes" | Saving is blocked, the out-of-range cell shows inline validation, and no edits are applied. | High |
| 12.G—GR-015 | Search for non-matching student name shows no rows | Grader report is open and grade table contains enrolled students. | 1. Enter a student name that does not match any enrolled student into the User search field<br>2. Trigger the search control (e.g., press Enter or click search) | Grade table shows no student rows and displays an empty-state or no-results indicator. | Medium |
| 12.G—GR-016 | Save grade settings with all required fields empty | Grader report is open and user has teacher privileges. | 1. Open the per-column action menu in the target activity's column header<br>2. Click "Edit grade settings"<br>3. Leave all required fields empty<br>4. Click "Save" or "Submit" | Validation errors shown for all required fields. | Medium |
| 12.G—GR-017 | Entering an out-of-range grade via per-cell edit shows inline flag | Grader report page is open and the grade table with per-cell three-dot menus is visible | 1. Click the per-cell three-dot menu for the target student's activity cell<br>2. Click "Edit" in the per-cell menu<br>3. Fill the grade value with a value outside the configured grade range<br>4. Click "Save" or confirm the edit | The grade cell shows the entered value and displays an inline flag indicating the value is outside the allowed range. | Medium |
| 12.G—GR-018 | Multiple edits including an out-of-range value block saving | User is a teacher and the Grader report page is open. | 1. Click "Edit mode" to enable editing<br>2. Edit several grade cells so at least one contains an out-of-range value<br>3. Click "Save changes" | Save is blocked, inline flags appear for the invalid cells, and none of the edits are applied. | Medium |
| 12.G—GR-019 | Editing is not allowed when Edit mode is disabled | User is a teacher and the Grader report page is open. | 1. Ensure "Edit mode" is disabled<br>2. Attempt to modify a grade cell | Grade cells are not editable when Edit mode is disabled. | Medium |

#### Edge Case Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 12.G—GR-020 | Canceling an edit does not persist grade settings changes | Grader report is open and user has teacher privileges. | 1. Open the per-column action menu in the target activity's column header<br>2. Click "Edit grade settings"<br>3. Modify one or more editable settings in the grade settings form<br>4. Click "Cancel" or close the settings dialog<br>5. Re-open "Edit grade settings" for the same activity | Previously saved settings remain unchanged and the unsubmitted modifications are not persisted. | Medium |
| 12.G—GR-021 | Flag out-of-range values inline when editing | User is a teacher and the Grader report page is open. | 1. Click "Edit mode" to enable editing<br>2. Enter an out-of-range value into a grade cell | The edited cell is visibly flagged inline to indicate the value is outside the configured range. | Medium |
| 12.G—GR-022 | Apply group filter for a group with no enrolled students results in empty table | Grader report is open and at least one group exists that contains no enrolled students. | 1. Open the group filter control and select the group that has no enrolled students<br>2. Apply the group filter if an explicit apply action is required | Grade table shows no student rows and displays an empty-state or no-results indicator. | Low |

---

### Profile

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 13.PROFIL-001 | Profile page displays all core profile elements | User is logged in and Profile page is open | 1. Verify the following elements are visible on the Profile page: teacher's circular initials icon, full name, Message button, email address, visibility note, timezone, Edit profile link, Data retention summary link, links to associated course profiles, links to Blog entries, Forum posts, Forum discussions, Learning plans, Browser sessions link, Grades overview link, and Login activity showing First and Last access with exact dates and relative time indicators | All listed profile elements are visible and correctly labeled. | High |
| 13.PROFIL-002 | Edit profile updates and persists profile description | User is logged in and Profile page is open | 1. Click the Edit profile link<br>2. Modify the profile description field and any other editable user detail<br>3. Click Save (or equivalent) to persist changes | Profile page reflects the updated profile description and saved details. | High |
| 13.PROFIL-003 | Open an associated course profile (triggerable from: any course link) | User is logged in and Profile page is open | 1. Click any course link under the Course details section<br>2. Verify the destination shows the course profile or course title/header | The selected associated course profile opens and displays the expected course identifier or title. | High |
| 13.PROFIL-004 | Login activity shows exact dates and relative time indicators | User is logged in and Profile page is open | 1. Locate the Login activity section<br>2. Verify that First access and Last access entries display exact date values and also show relative time indicators (e.g., 'x days ago') | Login activity lists First and Last access with both exact dates and relative time indicators. | High |
| 13.PROFIL-005 | Send a message to the teacher via Message button | User is logged in and Profile page is open | 1. Click the Message button<br>2. Compose a message in the messaging drawer and click Send | Message is sent and a confirmation or the sent message appears in the conversation thread. | Medium |
| 13.PROFIL-006 | Access Data retention summary from Privacy and policies | User is logged in and Profile page is open | 1. Click the Data retention summary link in the Privacy and policies section<br>2. Verify the Data retention summary content or heading is displayed | Data retention summary content or page is displayed. | Medium |
| 13.PROFIL-007 | Open Miscellaneous links: Blog, Forum posts, Forum discussions, and Learning plans | User is logged in and Profile page is open | 1. Click each link under the Miscellaneous section (Blog entries, Forum posts, Forum discussions, Learning plans) one at a time<br>2. Verify each link opens the corresponding list or page for that content type | Each Miscellaneous link navigates to and displays the appropriate list or page. | Medium |
| 13.PROFIL-008 | Access Reports links for Browser sessions and Grades overview | User is logged in and Profile page is open | 1. Click the Browser sessions link and verify browser session information or report is displayed<br>2. Click the Grades overview link and verify the grades overview is displayed | Browser sessions and Grades overview pages or reports are displayed when their links are clicked. | Medium |

#### Edge Case Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 13.PROFIL-009 | Login activity entries include First and Last access to site values | User is logged in and Profile page is open | 1. Locate the Login activity section<br>2. Verify that both First and Last access to site are shown with exact dates | Both First and Last access to site are displayed with exact date values. | Medium |
| 13.PROFIL-010 | Profile renders correctly when description is not provided | User is logged in and Profile page is open for a teacher without a profile description | 1. Confirm the profile description area is empty or absent<br>2. Verify other profile elements (initials icon, full name, Message button, user details, and links) are still visible and the page layout remains consistent | Profile displays correctly without a profile description; other elements are present and layout is unaffected. | Low |

---

### Profile Edit

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 14.PROEDI-001 | Update profile with valid required fields and new picture | User is on the Edit Profile page | 1. Fill all required fields (First name, Last name, Email address) and other editable fields to change (City/town, Country, Timezone, Description)<br>2. Upload a valid new picture via the new picture upload area (drag-and-drop or file select) and fill Picture description if applicable<br>3. Click "Update profile" | Profile page refreshes and displays the updated field values and the new user picture. | High |
| 14.PROEDI-002 | Update profile saving optional fields without changing picture | User is on the Edit Profile page | 1. Fill all required fields (First name, Last name, Email address) and fill optional fields (Additional names, Interests, any site-defined Optional custom fields)<br>2. Click "Update profile" | Profile page refreshes and displays the saved optional field values. | High |
| 14.PROEDI-003 | Drag-and-drop picture upload updates picture and refreshes profile page | User is on the Edit Profile page and all required fields are filled with valid values | 1. Drag-and-drop a valid image into the new picture upload area<br>2. Click "Update profile" | Profile page refreshes and the new picture is displayed as the user picture. | High |
| 14.PROEDI-004 | Cancel after editing multiple profile fields | Edit Profile form is open and current profile values are visible | 1. Modify multiple fields (First name, Last name, Email address, City/town, Country, Timezone, Email visibility)<br>2. Click "Cancel" | No edits are saved; profile displays the original values and changes are discarded. | High |
| 14.PROEDI-005 | Cancel after selecting a new user picture (drag-and-drop) | Edit Profile form is open and current user picture is displayed | 1. Upload a new picture using the new picture upload area (drag-and-drop or file select) and fill the Picture description field<br>2. Click "Cancel" | Original user picture and picture description remain; the uploaded picture is not saved. | High |
| 14.PROEDI-006 | User picture area displays current picture on Edit Profile page | User is on the Edit Profile page | 1. Inspect the User picture area | The current user picture is visible in the User picture area. | Medium |
| 14.PROEDI-007 | Cancel after changing the Description rich text | Edit Profile form is open and the current Description is visible | 1. Edit the Description using the rich text editor<br>2. Click "Cancel" | Description remains unchanged; the edited rich text is not saved. | Medium |
| 14.PROEDI-008 | Cancel after expanding and modifying optional and custom fields | Edit Profile form is open and optional/custom fields are available | 1. Click the "Expand all" link to reveal optional fields<br>2. Modify additional names, interests (tag-based), and any site-defined custom fields<br>3. Click "Cancel" | No changes to optional or custom fields are saved; fields retain their original values. | Medium |
| 14.PROEDI-011 | Click Cancel without making any edits | Edit Profile form is open | 1. Click "Cancel" | No action is taken and the profile remains unchanged; no errors occur. | Low |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 14.PROEDI-009 | Submit with all required fields empty | User is on the Edit Profile page | 1. Leave all required fields empty<br>2. Click "Update profile" | Validation errors shown for all required fields. | Medium |
| 14.PROEDI-010 | Upload unsupported picture file type is rejected | User is on the Edit Profile page and all required fields are filled with valid values | 1. Upload an unsupported file type via the new picture upload area<br>2. Click "Update profile" | Upload validation error shown and the profile is not saved. | Medium |

#### Edge Case Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 14.PROEDI-012 | Upload picture exceeding allowed size is rejected | User is on the Edit Profile page and all required fields are filled with valid values | 1. Upload a picture file exceeding the allowed upload size via the new picture upload area<br>2. Click "Update profile" | Upload size validation error shown and the profile is not saved. | Low |

---

### Logout

#### Functional Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 15.LOGOUT-001 | Log out terminates session and redirects to login page | User is authenticated and the top navigation bar is visible | 1. Click the user's initials icon in the top navigation<br>2. Click "Log out" in the user menu | The current authenticated session is terminated and the application redirects to the login page. | High |

#### Negative Tests

| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |
|-------|-----------|---------------|-------|-----------------|----------|
| 15.LOGOUT-002 | Access to protected pages requires re-authentication after logout (triggerable via browser Back or direct link) | User is authenticated and a protected page is open | 1. Click the user's initials icon in the top navigation<br>2. Click "Log out" in the user menu<br>3. Use the browser Back button to return to the previous (protected) page or attempt to open a protected link such as "Dashboard" | Access to the protected page is blocked and the login page or re-authentication prompt is shown; protected content is not accessible without signing in. | High |

---

## Navigation Graph

![Navigation Graph](Output/Moodle/navigation_graph.png)

### Pages

| Module | URL | Test Cases |
|--------|-----|------------|
| Login | /login | 6 |
| Dashboard | /dashboard | 25 |
| Dashboard — Edit Mode | /dashboard/edit | 23 |
| My Courses | /my | 9 |
| Course Page | /course/{id} | 9 |
| Course Edit Mode and Activity Chooser | /course/{id}/edit | 70 |
| Assignment Creation | /mod/assign/create | 18 |
| Course Settings | /course/{id}/settings | 14 |
| Participants Management | /course/{id}/participants | 35 |
| Assignment — Teacher View | /assignment/{id}/view | 8 |
| Assignment Submissions | /assignment/{id}/submissions | 19 |
| Gradebook — Grader Report | /course/{id}/gradebook | 22 |
| Profile | /user/{id}/profile | 10 |
| Profile Edit | /user/{id}/edit | 12 |
| Logout | /logout | 2 |
