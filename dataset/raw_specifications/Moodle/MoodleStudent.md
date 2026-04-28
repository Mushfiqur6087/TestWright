# Moodle Student Functional Description

---

## Navigation

The top navigation bar appears on every page and contains the site name "MoodleTest" on the left, which links to the home page, followed by links for Home, Dashboard, and My Courses. On the right side, a notifications bell icon shows alerts when clicked, a messaging icon opens the messaging drawer, and the user's initials in a circular icon opens the user menu dropdown. The user menu contains links for Profile, Grades, Calendar, Private Files, Reports, and Preferences, followed by a Log out option that ends the session and returns to the login page. When viewing a course, a horizontal tab bar appears below the course title with tabs for Course, Participants, Grades, Activities, and Competencies. Students do not see the Settings tab. When viewing an activity, breadcrumbs at the top show the full navigation path from the course, with each segment as a clickable link. The Course Index sidebar on the left side of course pages provides a hierarchical tree of all sections and activities, with expand/collapse arrows per section and a close button (X) to hide the sidebar. The currently active item is highlighted.

---

## Login

The login page displays a form with two required fields — Username and Password — followed by a "Log in" button. A "Lost password?" link is available (currently disabled on this test site). A separate section offers an "Access as a guest" button for unauthenticated browsing, and a "Cookies notice" button provides cookie usage information. On submission, valid credentials redirect the student to the Dashboard. Invalid or empty credentials show an inline error message, clear the password field, and retain the username for correction.

---

## Dashboard

The Dashboard displays a personalized greeting at the top. The main content area contains two blocks side by side: the Timeline block and the Calendar block. The Timeline block shows upcoming activities and deadlines across all enrolled courses. It includes a time range dropdown (e.g., "Next 7 days"), a sort order dropdown, and a search field to find activities by name or type. When no items exist within the selected range, an empty state is shown. The Calendar block shows a monthly view with the current month and year as a heading. It includes an "All courses" dropdown to filter events by course, a "New event" button to create personal calendar entries, and left/right arrows to navigate between months. The current date is highlighted, and dates with events display their names inline. Two links at the bottom — "Full calendar" and "Import or export calendars" — open the dedicated calendar view and calendar data management respectively. When Edit mode is toggled on, a "Reset page to default" button appears at the top right and a "+ Add a block" button appears below the Dashboard heading, opening a page listing all available block types. In Edit mode, each existing block shows a move icon and a three-dot menu for configure, move, and delete actions.

---

## My Courses

The My Courses page displays all courses in which the student is enrolled as visual cards. Each card shows the course banner image, course name as a clickable link, and the category name. Four controls appear above the grid: a status dropdown (All, In progress, Future, Past, Starred, Hidden), a search field, a sort dropdown, and a layout dropdown (Card, List, Summary). Each course card has a three-dot menu with two options: "Star this course" (pins the course to the top) and "Remove from view" (hides the course without unenrolling). Clicking the course name navigates to that course's main page.

---

## Course Page

The Course page displays the full course content organized into collapsible sections. The course name appears as the page heading, followed by the navigation tab bar. The main content area lists sections, each with a collapsible chevron and section name. A "Collapse all" link at the top right collapses all sections at once. Within each section, activities and resources are listed with a type icon and a clickable name. Students cannot enable Edit mode on course pages.

---

## Participants

The Participants page lists all users enrolled in the course. A filter system at the top allows building conditions using an "Any" toggle, a Select attribute dropdown, and an "+ Add condition" link, with "Clear filters" and "Apply filters" buttons. Alphabetical filter buttons for First name and Last name (All and A–Z) allow quick initial-based filtering. The participants table contains columns for checkbox, First/Last name (sortable, links to profile), Roles, Groups, and Last access to course. Students can click any participant name to view their profile but cannot enrol or unenrol users, edit roles, or access enrollment management features.

---

## Grades

The Grades page displays the student's own grades for the course via a User report. The grade table columns are: Grade item (course name as a collapsible header with graded activities indented beneath), Calculated weight, Grade (earned value or "–" if not yet graded), Range, Percentage, Feedback, and Contribution to course total. An "AGGREGATION Course total" row at the bottom displays the cumulative grade across all weighted items. Students can only view their own grades and cannot access the full gradebook or other students' grades.

---

## Assignment

The Assignment page displays the assignment's Opened date, Due date, and full Description. A "Add submission" button opens the submission form, which may include an online text editor, a file upload area, or both, depending on the assignment's configuration. The Submission status section shows a summary table with rows for Submission status (e.g., No submissions have been made yet, Submitted for grading), Grading status (e.g., Not graded, Graded), Time remaining, Last modified, and Submission comments. After submitting, the student may view or edit their submission if the due date has not passed and the teacher permits resubmission. Once graded, the earned grade and written feedback appear on this page.

---

## Activities

The Activities page provides a consolidated overview of every activity in the course, grouped by type. The Assignments section is expanded by default and displays a table with columns for Name (clickable link with parent section shown below), Due date, and Submission status. The Forums section and Resources section are collapsed by default and expandable via an arrow. Additional activity types appear as their own collapsible sections. Clicking any activity name navigates directly to that activity's page.

---

## Profile

The Profile page displays the student's circular initials icon, full name, a "Message" button, and an optional profile description. The page is organized into information cards: User details (email address, visibility note, timezone, and an "Edit profile" link), Privacy and policies (Data retention summary link), Course details (links to all enrolled course profiles), Miscellaneous (links to Blog entries, Forum posts, Forum discussions, and Learning plans), Reports (Browser sessions and Grades overview links), and Login activity (First and Last access to site with exact dates and relative time indicators). Clicking "Edit profile" opens the profile form, which contains collapsible panels for General (First name, Last name, Email address, Email visibility dropdown, MoodleNet profile ID, City/town, Country dropdown, Timezone dropdown, and Description), User picture (current picture, new picture upload, and picture description), Additional names, Interests, and Optional fields. "Update profile" validates all required fields before saving; "Cancel" exits without changes. Students can only modify their own profile.

---

## Logout

Selecting Log out terminates the current authenticated session and redirects to the login page. Access to all protected pages requires re-authentication after logout.