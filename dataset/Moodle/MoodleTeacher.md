# Moodle Teacher Functional Description

---

## 1. Login

The login page displays a centered card with the heading "Log in to Moodle Test Site." The form contains two required fields — **Username** and **Password** — followed by a blue **"Log in"** button. Below the button is a **"Lost password?"** link (currently disabled on this test site). A separate section below the form states "Some courses may allow guest access" with an **"Access as a guest"** button for unauthenticated browsing. A **"Cookies notice"** button at the bottom provides cookie usage information.

When the teacher submits the form, the system validates the credentials against stored accounts. If authentication succeeds, the system redirects to the Dashboard. If credentials are invalid or either field is left empty, an inline authentication error message appears, the password field is cleared, and the Username field remains populated to allow correction without re-entry. Empty fields block submission with inline validation before the request is sent.

---

## 2. Dashboard

The Dashboard serves as the teacher's home base after logging in. A personalized greeting at the top displays **"Hi, [Name]!"** with a waving hand emoji. The main content area contains two blocks displayed side by side: the **Timeline block** and the **Calendar block**.

The **Timeline block** aggregates upcoming teaching actions across all enrolled courses. It includes a **"Next 7 days"** dropdown to filter the visible time range, a **"Sort by dates"** dropdown to control ordering, and a search field to find activities by type or name. When no pending items exist within the selected range, the block displays a no-action state with an illustrative icon.

The **Calendar block** shows a monthly view with the current month and year displayed as a heading. It includes an **"All courses"** dropdown to filter events by a specific course, a **"New event"** button to create personal or course calendar entries, and left/right navigation arrows to move between months (labeled with the previous and next month names). The current date is visually highlighted, and dates containing scheduled events display the event names inline. At the bottom of the Calendar block, two links are available: **"Full calendar"** (opens a dedicated calendar view) and **"Import or export calendars"** (opens calendar data management).

---

## 3. Dashboard — Edit Mode

When **Edit mode** is toggled on, additional controls appear on the Dashboard. A **"Reset page to default"** button appears at the top right to restore the original layout. A **"+ Add a block"** button appears below the Dashboard heading, opening an **"Add a block"** page that lists all available block types in a vertical menu: Comments, Course overview, Latest announcements, Latest badges, Learning plans, Logged in user, Mentees, Online users, Private files, Random glossary entry, Recently accessed courses, Starred courses, Tags, Text, and Upcoming events. A **"Cancel"** link at the bottom of that page returns to the Dashboard without adding a block.

In Edit mode, each existing block displays a **move icon** (four-directional arrow) and a **three-dot options menu** for block-level actions such as configure, move, and delete. Layout customizations are persisted per user and can be fully reverted by clicking **"Reset page to default."**

---

## 4. My Courses

The My Courses page displays all courses to which the teacher has access. The page heading reads **"My courses"** with the subheading **"Course overview."**

Courses are displayed as visual cards, each showing the course banner image, the course name as a clickable link, and the category name beneath it. Four controls appear above the course grid: an **"All"** status dropdown to filter courses by enrollment state, a **"Search"** text field to locate a course by partial name, a **"Sort by course name"** dropdown to control ordering, and a **"Card"** layout dropdown to switch between Card, List, and Summary views.

Each course card includes a **three-dot menu** at the bottom right corner. Clicking it opens a dropdown with two options: **"Star this course"** (pins the course to the top of the list) and **"Remove from view"** (hides the course from this page without affecting enrollment). Clicking the course name navigates directly to that course's main page.

---

## 5. Course Page

The Course page displays the complete content of a single course organized into collapsible sections. At the top, the full course name appears as the page heading, followed by a horizontal navigation tab bar. For teachers, the available tabs are: **Course**, **Settings**, **Participants**, **Grades**, **Activities**, and **More**. The Settings tab is visible to teachers only and is not shown to students.

The main content area lists course sections, each preceded by a collapsible **chevron arrow** and a section name. A **"Collapse all"** link at the top right of the content area collapses every section simultaneously. Within each section, activities and resources are listed with a type icon and the activity name as a clickable link.

The **Course Index sidebar** on the left side of the page provides a persistent collapsible navigation tree showing all sections and their contained activities. Sections can be individually expanded or collapsed. The currently active item is highlighted. A close button **(X)** at the top of the Course Index hides the sidebar to maximize the content area width. The system renders course content according to teacher permissions and the current edit-state mode.

---

## 6. Course Edit Mode and Activity Chooser

Enabling **Edit mode** transforms the Course page into a full authoring interface. Each section and activity row gains a set of inline controls:

- **Edit icons** appear next to each activity name for quick renaming.
- A **section-level action menu** (three-dot) provides options to edit, duplicate, hide, delete, or move the section.
- An **activity-level action menu** (three-dot) per activity provides options to edit settings, move, duplicate, hide from students, set access restrictions, and delete.
- A **bulk actions toolbar** appears at the top of the content area, allowing teachers to select multiple activities and apply batch operations.
- An **"+ Add an activity or resource"** button appears at the bottom of each section.

Clicking **"+ Add an activity or resource"** opens the **Activity Chooser modal**. The modal contains:
- A **category filter bar** at the top to narrow the displayed tiles (e.g., All, Activities, Resources, Recommended).
- A **search field** to find a specific activity or resource type by name.
- **Activity/resource tiles** displayed in a grid, including (for example): Assignment, Forum, Quiz, File, Page, Lesson, SCORM, URL, and Workshop. Each tile shows the item's icon and name.
- A **star/favorite toggle** on each tile to mark frequently used types for quick access.
- An **"Add"** confirmation button once a tile is selected.

Clicking **"Add"** on a selected activity type opens that activity's creation form. An **"+ Add a subsection"** control is also available within each section to nest content hierarchically.

---

## 7. Assignment Creation

The assignment creation form opens after selecting "Assignment" from the Activity Chooser. The form is organized into collapsible sections. **Assignment name** is a required text field at the top.

The form's collapsible panels and their fields are:

- **General** — contains the required **Assignment name** field and a **Description** rich text editor. An optional **Additional files** upload area allows attaching supplementary resources for students.
- **Availability** — contains **Allow submissions from** (date/time picker with an **Enable** toggle), **Due date** (date/time picker with an **Enable** toggle), and **Cut-off date** (date/time picker with an **Enable** toggle). Disabled toggles exclude that date from enforcement.
- **Submission types** — contains checkboxes for **Online text** and **File submissions**. When **File submissions** is enabled, additional controls appear: **Maximum number of uploaded files** (numeric), **Maximum submission size** (dropdown), and **Accepted file types** (tag-based field).
- **Feedback types** — contains options for feedback comments, feedback files, and offline grading worksheet.
- **Submission settings** — contains options for requiring students to click a submit button, requiring submission statements, attempts reopened settings, and maximum attempts.
- **Group submission settings** — contains controls for students to submit in groups, requiring all group members to submit, and grouping selection.
- **Notifications** — contains toggles for notifying graders of new submissions and notifying graders of late submissions.
- **Grade** — contains the **Grade** type and maximum points field, grading method selector, and grade category and grade to pass fields.
- **Access restrictions** — contains an **"+ Add restriction"** button that opens a restriction-type picker.
- **Activity completion** — contains completion tracking options and required conditions.
- **Tags** — contains a tag entry field.
- **Competencies** — contains course competency linking controls.

At the bottom of the form, three action buttons are available: **"Save and return to course"** (creates the assignment and redirects to the course page), **"Save and display"** (creates the assignment and opens the newly created assignment's main page), and **"Cancel"** (discards all changes and returns to the course page). Required fields and date/file constraints are validated inline before saving; errors highlight the relevant field and block submission.

---

## 8. Course Settings

The Course Settings form is organized into collapsible panels. The form is organized into collapsible panels. Fields include:

- **Course full name** (required text field)
- **Course short name** (required text field)
- **Course category** (required dropdown)
- **Course visibility** (Show/Hide dropdown)
- **Course start date** (date/time picker)
- **Course end date** (date/time picker with Enable toggle)
- **Course ID number** (optional text field)
- **Course summary** (rich text editor)
- **Course image** (file upload area)
- **Course format** (dropdown: e.g., Topics format, Weekly format)
- **Layout controls** (section display options dependent on selected format)
- **Appearance settings** (language, news items, show activity dates, show activity completion conditions)
- **Files and uploads** — **Maximum upload size** (dropdown)
- **Completion tracking** — Enable/Disable toggle
- **Groups** — Group mode and Grouping dropdowns
- **Tags** — tag entry field

At the bottom, **"Save and display"** persists the configuration and returns to the course page; **"Cancel"** leaves existing settings unchanged. Required field and format validations are enforced inline; errors highlight the relevant field and block saving.

---

## 9. Participants Management

The Participants page lists all users enrolled in the course.

At the top, an **enrolled-users scope selector** dropdown filters the list by enrollment context. An **"Enrol users"** button opens the enrollment dialog (described below).

Below that, a **Match filter system** allows flexible participant filtering with an **"Any"** dropdown, a **"Select"** attribute dropdown, an **"X"** remove button per condition, and an **"+ Add condition"** link. **"Clear filters"** and **"Apply filters"** buttons control execution. A participant count updates after filtering.

**Alphabetical filter buttons** for First name and Last name (showing "All" and letters A–Z) allow quick initial-based filtering.

The main content area is a table with columns for: checkbox (bulk selection), **First name / Last name** (sortable, clickable link to participant profile), **Email address**, **Roles**, **Groups**, **Last access to course**, and **Status**. Each row also provides a **row-level action menu** with options such as viewing the participant's profile in course context, editing their role, and sending a message.

At the bottom of the table, a **"With selected users…"** label appears alongside a **"Choose…"** dropdown for bulk actions on checked participants.

The **Enrol users dialog** contains: a **user search field** to find users by name or email, a **Role** assignment dropdown, and an optional **Enrollment duration** control. Confirming enrollment adds the selected user to the course at the specified role.

Teachers can open any participant's profile or grade context, edit roles where permissions allow, perform row-level actions, and run bulk operations on selected users.

---

## 10. Assignment — Teacher View

The Assignment main page (teacher view) displays assignment details and grading controls. Breadcrumbs at the top show the full navigation path from the course home to the current assignment, with each segment as a clickable link.

The page displays the assignment's **metadata** section containing: **Opened** (date and time the assignment became available), **Due date** (submission deadline), and the full **Description** with any attached files.

A prominent **"Grade"** action button opens the grading interface for individual students.

The **Grading summary** panel below the description displays the following read-only metrics:
- **Number of participants** — total enrolled students
- **Number of submissions** — total submissions received
- **Needs grading** — count of submitted work awaiting a grade
- **Visibility** — whether the assignment is currently visible to students
- **Time remaining** — countdown to the due date

A horizontal tab bar below the summary provides navigation to: **Assignment** (the current metadata view), **Settings** (assignment configuration), **Submissions** (the full submission table), **Advanced grading** (grading method setup), and **More** (additional options).

---

## 11. Assignment Submissions

The Submissions view presents a full table of all student submission records. It presents a full table of all student submission records.

Above the table, **search and filter controls** allow narrowing by student name, submission status, and grading status.

The submissions table contains the following columns: **Student identity** (name and initials icon, clickable to profile), **Submission status** (e.g., "Submitted for grading," "No submission," "Draft — not submitted"), **Grading status** (e.g., "Graded," "Not graded"), **Submission date/time**, **Time since submission**, **Online text** (preview of submitted text if applicable), **File submissions** (links to uploaded files if applicable), **Submission comments**, **Feedback comments** (teacher-entered feedback), **Feedback files**, and **Final grade**.

Each row includes an **action menu** that opens the grading workflow for that student. A **"Quick grading"** mode can be enabled above the table to allow inline grade entry directly in the table without opening individual grading pages. Teacher actions (submitting a grade or feedback) update the grading status and control feedback visibility to the student.

---

## 12. Advanced Grading

The Advanced Grading section allows teachers to define a structured grading method beyond a simple numeric grade. It allows teachers to define a structured grading method beyond a simple numeric grade.

The page presents a **grading method selector** (e.g., Rubric) and options to create a grading form **from scratch** or **from a template**. When "Rubric" is selected and a new form is being created, the teacher defines criteria rows and performance level descriptors with associated point values.

The system validates that the grading form is complete and published before it becomes active for the assignment. If the grading form is incomplete or in draft state, the system falls back to simple direct grading for that assignment until the form reaches a valid, published status. Once a valid advanced grading form exists, it is used in place of the simple grade input field throughout the assignment grading workflow.

---

## 13. Gradebook — Grader Report

The Gradebook Grader report provides a spreadsheet-style view of grades. A **report-type selector** dropdown at the top left allows switching between available report views (e.g., Grader report, User report, Overview report).

Above the grade table, **user search and filter controls** allow narrowing the visible rows by student name or group.

The main content area is a spreadsheet-style grade table. Columns represent individual graded activities; rows represent enrolled students. Each cell displays the student's grade for that activity. A **per-column action menu** (accessible via a dropdown on the column header) provides options to edit the activity's grade settings. A **per-cell action menu** (three-dot) on individual grade cells allows editing that specific grade entry.

An **overall average row** at the bottom of the table displays the class average for each graded activity.

When **Edit mode** is enabled, grade cells become editable inline. Teachers can enter or modify grade values directly in the spreadsheet. A **"Save changes"** action applies edits. Validation prevents invalid grade entries outside the configured grade range for each activity; out-of-range values are flagged inline and block saving.

---

## 14. Profile

The Profile page displays the teacher's personal information. The top of the page shows the teacher's circular initials icon, their full name, and a **"Message"** button. A profile description text block appears below the name if the teacher has set one.

The page is organized into the following information cards:

- **User details** — includes an **"Edit profile"** link in the top-right corner of the card, the teacher's email address with a visibility note, and their timezone setting.
- **Privacy and policies** — contains a **"Data retention summary"** link.
- **Course details** — lists all course profiles with links to each course the teacher is associated with.
- **Miscellaneous** — provides links to Blog entries, Forum posts, Forum discussions, and Learning plans.
- **Reports** — contains links to Browser sessions and Grades overview.
- **Login activity** — displays First access to site and Last access to site with exact dates and relative time indicators.

---

## 15. Profile Edit

The Edit profile form contains collapsible sections for personal details and preferences. The form heading shows the teacher's name with an **"Expand all"** link at the top right to open all collapsible sections simultaneously.

The form is divided into collapsible panels:

- **General** — contains: First name (required), Last name (required), Email address (required), Email visibility dropdown, MoodleNet profile ID field, City/town field, Select a country dropdown, Timezone dropdown, and Description (rich text editor).
- **User picture** — shows the Current picture, a New picture upload area with drag-and-drop support (subject to file type and size constraints), and a Picture description field.
- **Additional names** — optional fields for alternative name formats.
- **Interests** — a tag-based field for personal interests.
- **Optional fields** — any site-defined custom fields.

Required fields are labeled "Required." The **"Update profile"** button validates all required fields and upload constraints before saving; a successful save refreshes the profile page with updated information. The **"Cancel"** button exits the form without making any changes.

---

## 18. Logout

Selecting **Log out** terminates the current authenticated session. Selecting it terminates the current authenticated session and redirects the browser to the login page. Access to all protected pages — including course pages, grading interfaces, participant management, and profile settings — requires re-authentication after logout.