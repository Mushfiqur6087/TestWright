# Moodle Student Functional Description

**Test Account:** teststudent / Test@1234

---

## 1. Login

The login page displays a centered card with the heading "Log in to Moodle Test Site." The form contains two required fields — **Username** and **Password** — followed by a blue **"Log in"** button. Below the button is a **"Lost password?"** link (currently disabled on this test site). A separate section below the form states "Some courses may allow guest access" with an **"Access as a guest"** button for unauthenticated browsing. A **"Cookies notice"** button at the bottom provides cookie usage information.

When the student submits the form, the system validates the credentials against the user database. If authentication succeeds, the system redirects the user to the Dashboard. If the credentials are invalid or either field is left empty, an inline error message appears below the form, the password field is cleared, and the username field remains populated to allow correction without re-entry.

---

## 2. Dashboard

The Dashboard serves as the student's home base after logging in. A personalized greeting at the top displays **"Hi, [Name]!"** with a waving hand emoji. The main content area contains two blocks displayed side by side: the **Timeline block** and the **Calendar block**.

The **Timeline block** shows upcoming activities and deadlines across all enrolled courses. It includes a **"Next 7 days"** dropdown to filter the visible time range, a **"Sort by dates"** dropdown to control ordering, and a search field to find activities by type or name. When no activities are pending within the selected range, the block displays "No activities require action" with an illustrative icon.

The **Calendar block** shows a monthly view with the current month and year displayed as a heading. It includes an **"All courses"** dropdown to filter events by a specific course, a **"New event"** button to create personal calendar entries, and left/right navigation arrows to move between months (labeled with the previous and next month names). The current date is visually highlighted. Dates that contain scheduled events display the event names inline. At the bottom of the Calendar block, two links are available: **"Full calendar"** (opens a dedicated calendar view) and **"Import or export calendars"** (opens calendar data management).

When **Edit mode** is toggled on via the switch in the top navigation bar, additional controls appear. A **"Reset page to default"** button appears at the top right to restore the original layout. A **"+ Add a block"** button appears below the Dashboard heading, opening an **"Add a block"** page that lists all available block types in a vertical menu: Comments, Course overview, Latest announcements, Latest badges, Learning plans, Logged in user, Mentees, Online users, Private files, Random glossary entry, Recently accessed courses, Starred courses, Tags, Text, and Upcoming events. A **"Cancel"** link at the bottom of that page returns to the Dashboard without adding a block. In Edit mode, each existing block also displays a **move icon** (four-directional arrow) and a **three-dot menu** for block-level options such as configure, move, and delete.

---

## 3. My Courses

The My Courses page provides a view of all courses in which the student is currently enrolled. The page heading reads **"My courses"** with the subheading **"Course overview."**

Courses are displayed as visual cards, each showing the course banner image, the course name as a clickable link, and the category name beneath it. Four controls appear above the course grid: an **"All"** status dropdown to filter courses by enrollment state (e.g., In progress, Future, Past), a **"Search"** text field to locate a course by partial name, a **"Sort by course name"** dropdown to control ordering, and a **"Card"** layout dropdown to switch between Card, List, and Summary views.

Each course card includes a **three-dot menu** at the bottom right corner. Clicking it opens a dropdown with two options: **"Star this course"** (pins the course to the top of the list) and **"Remove from view"** (hides the course without unenrolling). Clicking the course name navigates directly to that course's main page.

---

## 4. Course Page (View Only)

The Course page displays the complete content of a single course, organized into collapsible sections. At the top, the full course name appears as the page heading (e.g., "Business Management Fundamentals"), followed by a horizontal navigation tab bar. For students, the available tabs are: **Course**, **Participants**, **Grades**, **Activities**, and **Competencies**. Students do not see the **Settings** tab and cannot enable Edit mode on course pages.

The main content area lists course sections, each preceded by a collapsible **chevron arrow** and a section name (e.g., "General," "New section," "New subsection"). A **"Collapse all"** link at the top right of the content area collapses every section simultaneously. Within each section, activities and resources are listed with a type icon and the activity name as a clickable link. Representative activities include: "Announcements" (forum icon), "BUS301 Course Overview" (page icon), "BUS301 Business Discussion" (forum icon), "BUS301 - Case Study Analysis" (assignment icon), "BUS301 - Business Plan Draft" (assignment icon), and "BUS301 - Final Presentation" (assignment icon).

The **Course Index sidebar** on the left side of the page provides a persistent collapsible navigation tree showing all sections and their contained activities. Sections in the Course Index can be individually expanded or collapsed. Clicking any item navigates directly to that section or activity. The currently active activity is highlighted. A close button **(X)** at the top of the Course Index hides the sidebar to maximize content area width.

---

## 5. Participants

The Participants page lists all users enrolled in the course and is accessed via the **Participants** tab in the course navigation bar.

At the top, a **Match filter system** allows flexible participant filtering. It contains an **"Any"** dropdown (to match any or all conditions), a **"Select"** dropdown (to choose the filter attribute), an **"X"** button to remove the current filter condition, and an **"+ Add condition"** link to stack additional filters. **"Clear filters"** and **"Apply filters"** buttons control filter execution. A participant count updates after filtering is applied.

Below the filter controls, **alphabetical filter buttons** are provided for both First name and Last name. Each set shows "All" plus individual letters A through Z to quickly narrow participants by initial.

The main content area is a table with columns for: checkbox (for bulk selection), **First name / Last name** (sortable, displayed as a clickable link), **Roles**, **Groups**, and **Last access to course**. Each row displays the participant's circular initials icon, their full name as a clickable link to their profile, their assigned role (Teacher or Student), group membership if applicable, and a relative last-access timestamp (e.g., "3 days ago").

At the bottom of the table, a **"With selected users…"** label appears alongside a **"Choose…"** action dropdown for bulk actions on checked participants. Students can click any participant name to view their profile page. Unlike teachers, students cannot enrol or unenrol users, edit roles, or access enrollment management features.

---

## 6. Grades (User Report)

The Grades page displays the student's own grades for the course and is accessed via the **Grades** tab in the course navigation bar. A **"User report"** dropdown at the top indicates the current report type. The student's name and circular initials icon appear below.

The main content is a grade table with the following columns: **Grade item** (lists the course name as a collapsible section header, with all graded activities indented beneath it), **Calculated weight** (the percentage weight of each item toward the final grade; shows "(Empty)" for unsubmitted items), **Grade** (the earned grade value or "–" if not yet graded, with a three-dot context menu per row), **Range** (the minimum and maximum possible grade), **Percentage** (the percentage score achieved), **Feedback** (any written feedback provided by the teacher), and **Contribution to course total** (how many points each item contributes to the overall grade).

Each graded activity row is prefixed with a type label (e.g., "ASSIGNMENT") above the clickable activity name link. At the bottom of the table, an **"AGGREGATION Course total"** row displays the cumulative grade across all weighted items.

Students can only view their own grades. They cannot access the full gradebook, see other students' grades, or change grade settings.

---

## 7. Assignment (Student View)

The Assignment page displays assignment details and the student submission interface. Breadcrumbs at the top show the full navigation path from the course home to the current assignment (each segment is a clickable link). An assignment icon and the assignment name appear as the page heading.

The page displays three key dates and details:
- **Opened:** the date and time when the assignment became available for submission
- **Due date:** the submission deadline date and time
- **Description:** the full assignment instructions provided by the teacher

A blue **"Add submission"** button initiates the submission process. Clicking it opens the submission form, which may include an online text editor, a file upload area, or both, depending on the assignment's configuration.

The **Submission status** section displays a summary table with the following rows: **Submission status** (e.g., "No submissions have been made yet" or "Submitted for grading"), **Grading status** (e.g., "Not graded" or "Graded"), **Time remaining** (a live countdown to the due date), **Last modified** (the date and time the submission was most recently updated), and **Submission comments** (a collapsible section where students can add notes visible to the teacher).

After submitting, the student may view their submission, edit it (if the due date has not passed and the teacher permits resubmission), or remove it. Once the teacher grades the submission, the earned grade and written feedback appear directly on this page.

---

## 8. Activities

The Activities page provides a consolidated overview of every activity in the course, grouped by type. It is accessed via the **Activities** tab in the course navigation bar. The page heading reads "Activities" with the description: "An overview of all activities in the course, with dates and other information."

Activities are organized into collapsible type-sections. The **Assignments section** is expanded by default and displays a table with three columns: **Name** (the assignment name as a clickable link, with its parent section name shown below in smaller text), **Due date** (the submission deadline), and **Submission status** (the student's current state, e.g., "Submitted for grading" or "No submission").

The **Forums section** (collapsed by default, expandable via a **>** arrow) lists all forum activities. The **Resources section** (also collapsed by default) lists all file and page resources. Additional activity types, if present, appear as their own collapsible sections. Clicking any activity name navigates directly to that activity's page.

---

## 9. Profile

The Profile page displays the student's personal information and is accessed by clicking the user's initials icon in the top navigation bar and selecting **"Profile"** from the dropdown menu. The top of the page shows the user's circular initials icon, their full name, and a **"Message"** button to initiate a direct message. A profile description text block appears below the name if the student has set one.

The page is organized into several information cards:

- **User details** — includes an **"Edit profile"** link in the top-right corner of the card, the student's email address with a visibility note (e.g., "Visible to other course participants"), and their timezone setting.
- **Privacy and policies** — contains a **"Data retention summary"** link.
- **Course details** — lists all course profiles with links to each enrolled course.
- **Miscellaneous** — provides links to Blog entries, Forum posts, Forum discussions, and Learning plans.
- **Reports** — contains links to Browser sessions and Grades overview.
- **Login activity** — displays the First access to site and Last access to site with exact dates and relative time indicators.

Clicking **"Edit profile"** opens the profile editing form. The form heading shows the student's name with an **"Expand all"** link at the top right to open all collapsible sections simultaneously. The form is divided into collapsible panels:

- **General** — contains: First name (required), Last name (required), Email address (required), Email visibility dropdown, MoodleNet profile ID field, City/town field, Select a country dropdown, Timezone dropdown, and Description (rich text editor).
- **User picture** — shows the Current picture, a New picture upload area with drag-and-drop support, and a Picture description field.
- **Additional names** — optional fields for alternative name formats.
- **Interests** — a tag-based field for personal interests.
- **Optional fields** — any site-defined custom fields.

Required fields are labeled "Required." The form ends with **"Update profile"** and **"Cancel"** buttons. Students can only modify their own profile; they cannot edit other users' profiles or access administrative settings.

---

## 10. Logout

Selecting **Log out** terminates the current authenticated session. Selecting it terminates the current authenticated session and redirects the browser to the login page. Access to all protected pages — including course pages, grading interfaces, participant management, and profile settings — requires re-authentication after logout.

---
