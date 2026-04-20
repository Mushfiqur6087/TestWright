# Test Case Verification Structure Specification

> **Purpose:** This document defines the canonical verification structure for automated test case verification agents. It specifies how to model, classify, and execute verification for any test case across web applications, along with rules for reporting uncoverable cases.

---

## Table of Contents

1. [Core Concepts](#1-core-concepts)
2. [Top-Level Schema](#2-top-level-schema)
3. [Verification Types — Reference](#3-verification-types-reference)
   - 3.1 same_actor_navigation
   - 3.2 in_page_dynamic
   - 3.3 cross_actor
   - 3.4 credential_mutation
   - 3.5 out_of_band
   - 3.6 unobservable_by_design
4. [Coverage Classification](#4-coverage-classification)
5. [Decision Tree — Choosing Verification Type](#5-decision-tree--choosing-verification-type)
6. [Field Reference](#6-field-reference)
7. [Real Examples from Known Applications](#7-real-examples-from-known-applications)
8. [Coverage Report Format](#8-coverage-report-format)
9. [Agent Execution Rules](#9-agent-execution-rules)
10. [Common Failure Modes by App Domain](#10-common-failure-modes-by-app-domain)

---

## 1. Core Concepts

### What Is a Verification Record?

A verification record is a JSON object that describes **how to confirm the effect of a test case** — not how to perform the test case itself. The test case steps are already defined in the test case document. The verification record answers: *"After the test case action is complete, how do we confirm the system state changed as expected?"*

### The Fundamental Principle

Every test case produces an **effect** somewhere in the system. The verification record must identify:
1. **Where** that effect is observable (a page, an external channel, another actor's view, or nowhere)
2. **What** to observe (specific fields, values, messages, state changes)
3. **Whether** it is even possible to observe it within this environment

### The Three-Part Structure

Every verification record has three parts regardless of type:

```
[PRE-STATE] → [ACTION (test case ID reference)] → [POST-STATE]
```

The verification record defines PRE-STATE and POST-STATE only. The ACTION is already defined by the test case.

### Why verification_type Matters

`verification_type` is a **discriminated union**. It controls which fields are required. An agent must read `verification_type` first and then apply only the fields relevant to that type. Fields from other types are ignored.

---

## 2. Top-Level Schema

Every verification record must contain exactly these top-level fields:

```json
{
  "test_case_id": "string",
  "verification_type": "same_actor_navigation | in_page_dynamic | cross_actor | credential_mutation | out_of_band | unobservable_by_design",
  "coverage": "verifiable | manual_only | not_coverable",
  "coverage_note": "string — REQUIRED when coverage is manual_only or not_coverable",
  "body": { }
}
```

### Field Constraints

| Field | Type | Required | Notes |
|---|---|---|---|
| `test_case_id` | string | Always | Must match the ID in the test case document exactly |
| `verification_type` | enum | Always | One of the six types defined in Section 3 |
| `coverage` | enum | Always | See Section 4 |
| `coverage_note` | string | Conditional | Required when coverage is not `verifiable` |
| `body` | object | Always | Shape is determined by `verification_type` |

---

## 3. Verification Types — Reference

---

### 3.1 `same_actor_navigation`

**Definition:** The effect of the test case action is observable by the same authenticated user on a different page within the application. The actor navigates away from the action page and observes the state change elsewhere.

**When to use:**
- A balance or numeric value changes and is visible on a summary/overview page
- A record was created and appears in a listing page
- A setting was updated and is reflected on a profile or settings page
- An account was created/modified and appears in a dashboard table

**Coverage:** Always `verifiable`

**Body schema:**
```json
{
  "body": {
    "pre_check": {
      "navigate_to": "string — page name or URL path",
      "observe": ["array of specific fields, values, or UI elements to record"]
    },
    "post_check": {
      "login_required": "boolean — false if session persists, true if re-auth is needed",
      "navigate_to": "string — page name or URL path",
      "observe": ["array of specific fields, values, or UI elements to check"],
      "expected_change": "string — precise description of how observed values should differ from pre_check"
    }
  }
}
```

**Rules:**
- `pre_check.navigate_to` and `post_check.navigate_to` are often the same page (dashboard, overview) but CAN differ
- `observe` arrays must be specific enough that an agent knows exactly what element to read — avoid vague terms like "check the page"
- `expected_change` must be deterministic — describe the change in terms of the pre-check values
- If `login_required` is true, this is a borderline case with `credential_mutation` — use `credential_mutation` instead unless the action itself (not a password change) requires re-login

**Example:**
```json
{
  "test_case_id": "5.TRAFUN-001",
  "verification_type": "same_actor_navigation",
  "coverage": "verifiable",
  "body": {
    "pre_check": {
      "navigate_to": "Accounts Overview",
      "observe": ["balance of source account", "balance of destination account"]
    },
    "post_check": {
      "login_required": false,
      "navigate_to": "Accounts Overview",
      "observe": ["balance of source account", "balance of destination account"],
      "expected_change": "Source account balance decreased by transfer amount; destination account balance increased by the same amount; combined total of both accounts unchanged."
    }
  }
}
```

---

### 3.2 `in_page_dynamic`

**Definition:** The effect of the test case action is observable on the **same page** without any navigation. The UI updates in-place in response to a trigger action.

**When to use:**
- Sidebar filters update the results grid dynamically
- An inline form field shows a validation error without page reload
- A toggle changes the visible state of a section on the same page
- A search field narrows results as the user types
- CAPTCHA appears after repeated failed attempts
- A payment form retains its state after a failed submission
- Inline grade editing in a gradebook

**Coverage:** Always `verifiable`

**Body schema:**
```json
{
  "body": {
    "page": "string — page the actor is currently on",
    "trigger": "string — the specific UI action taken on this page",
    "observe": "string — what element or region of the page to watch",
    "expected_change": "string — precise description of the in-place change"
  }
}
```

**Rules:**
- `page` should be a named page or route — not a vague description
- `trigger` must be a specific action: which control, what value, what interaction
- `observe` should point to a specific section, component, or element
- This type MUST NOT be used when the observation requires any navigation

**Example:**
```json
{
  "test_case_id": "6.HOTFIL-003",
  "verification_type": "in_page_dynamic",
  "coverage": "verifiable",
  "body": {
    "page": "Hotels Listing",
    "trigger": "Set price range filter slider to $50–$100 per night",
    "observe": "Results grid and result count displayed above the grid",
    "expected_change": "Only hotel cards with starting price within $50–$100 per night remain visible; result count updates to reflect the filtered set; active filter appears in the filter summary bar at the top."
  }
}
```

---

### 3.3 `cross_actor`

**Definition:** The effect of the test case action by Actor A is observable by a **different user or role** (Actor B) on a page within the application. This requires two separate sessions.

**When to use:**
- A teacher creates content (assignment, quiz) that a student must see in their course view
- An admin creates a user account that the new user can then log in with
- A user submits a review that is visible to unauthenticated visitors on the listing page
- A manager approves a loan application that the client officer can then see as approved
- A maker creates a transaction in a maker-checker system that the checker sees in a pending queue

**Coverage:** Always `verifiable` (requires two sessions, but both are in-app)

**Body schema:**
```json
{
  "body": {
    "actor_a": {
      "role": "string — role performing the action (e.g. teacher, admin, maker)",
      "action": "string — what actor_a does, referencing the test case"
    },
    "actor_b": {
      "role": "string — role observing the effect (e.g. student, new_user, checker)",
      "session": "string — new_session | same_session_different_account",
      "navigate_to": "string — page actor_b navigates to",
      "observe": ["array of specific elements to check"],
      "expected_change": "string — what actor_b should see as a result of actor_a's action"
    }
  }
}
```

**Rules:**
- `actor_b.session` should be `new_session` when a completely separate login is needed
- Both actors must be explicitly identified by role, not username — usernames change between environments
- The observation from actor_b's perspective must be fully specified; do not assume the agent infers it

**Example:**
```json
{
  "test_case_id": "TC-MOODLE-ASSIGN-001",
  "verification_type": "cross_actor",
  "coverage": "verifiable",
  "body": {
    "actor_a": {
      "role": "teacher",
      "action": "Create assignment named 'Week 1 Essay' in Course X with due date set to next Friday"
    },
    "actor_b": {
      "role": "student",
      "session": "new_session",
      "navigate_to": "Course X → Activities tab → Assignments section",
      "observe": ["assignment name", "due date", "submission status"],
      "expected_change": "Assignment 'Week 1 Essay' appears in the Assignments section with the correct due date and submission status showing 'No submission'."
    }
  }
}
```

---

### 3.4 `credential_mutation`

**Definition:** The test case action changes authentication credentials (password, username, or security settings). Verification requires **terminating the current session** and attempting re-authentication to confirm the mutation took effect.

**When to use:**
- Password change via Security Settings / Change Password
- Password reset via Forgot Password flow
- Admin resets a user's password
- Any action that modifies the credentials used to authenticate

**Coverage:** Always `verifiable`

**Body schema:**
```json
{
  "body": {
    "pre_check": {
      "navigate_to": "string — page where credential change is performed",
      "observe": ["confirmation that current credentials are valid before mutation"]
    },
    "mutation": "string — description of the credential change (e.g. 'change password from old to new')",
    "post_check": [
      {
        "attempt": "string — description of login attempt",
        "credential_used": "old | new",
        "expected_outcome": "success | failure",
        "expected_message": "string — message the system should display"
      }
    ]
  }
}
```

**Rules:**
- `post_check` is always an array with at minimum **two entries**: one for old credentials (expect failure) and one for new credentials (expect success)
- Never test only new credentials — confirming old credentials are rejected is equally important
- The current session must be terminated (logout) before post_check attempts
- Do not use `same_actor_navigation` for password change tests — the cross-session requirement makes this a fundamentally different type

**Example:**
```json
{
  "test_case_id": "12.SECSET-001",
  "verification_type": "credential_mutation",
  "coverage": "verifiable",
  "body": {
    "pre_check": {
      "navigate_to": "Security Settings → Change Password panel",
      "observe": ["current session is active and authenticated"]
    },
    "mutation": "Change password from current_password to new_strong_password via Change Password form",
    "post_check": [
      {
        "attempt": "Log in with old password after logout",
        "credential_used": "old",
        "expected_outcome": "failure",
        "expected_message": "Incorrect email or password. Please try again."
      },
      {
        "attempt": "Log in with new password",
        "credential_used": "new",
        "expected_outcome": "success",
        "expected_message": "Signed in successfully."
      }
    ]
  }
}
```

---

### 3.5 `out_of_band`

**Definition:** The primary verifiable effect of the test case action exists **outside the application UI** — typically in email, SMS, push notifications, or an external payment system. There is no page within the application where the agent can navigate to confirm the effect.

**When to use:**
- Booking confirmation email sent after payment
- Password reset link sent via email
- Callback request confirmation email
- Support ticket creation confirmation email
- Cancellation/modification notification email
- Refund initiated to external payment method (credit card, PayPal)
- SMS OTP delivery

**Coverage:** Always `manual_only`

**Body schema:**
```json
{
  "body": {
    "trigger_action": "string — the in-app action that causes the out-of-band event",
    "channel": "email | sms | push_notification | external_payment_system",
    "recipient": "string — who receives the out-of-band communication",
    "expected_content": ["array of content elements the communication must contain"],
    "in_app_partial_check": {
      "navigate_to": "string or null — if any partial in-app indicator exists",
      "observe": "string or null — what in-app element partially confirms the action"
    },
    "verification_method": "string — how a human tester should verify this"
  }
}
```

**Rules:**
- `channel` must be specific — do not use a generic "notification" if the type is known
- `expected_content` must list each required piece of content separately (reference number, amounts, dates, etc.)
- `in_app_partial_check` can capture partial in-app evidence (e.g. a confirmation page showing a ticket ID) but this does NOT make coverage `verifiable` — the email/external effect is still unconfirmed by in-app checks alone
- `verification_method` should specify tooling: test inbox (Mailtrap, Mailhog), email logs, etc.
- `coverage_note` is mandatory and must explain specifically what cannot be checked in-app

**Example:**
```json
{
  "test_case_id": "PHPTRV-BOOK-007",
  "verification_type": "out_of_band",
  "coverage": "manual_only",
  "coverage_note": "Email delivery and content cannot be observed within the PHPTravels UI. Requires access to the test inbox or email testing tool.",
  "body": {
    "trigger_action": "Complete hotel booking and payment with valid card",
    "channel": "email",
    "recipient": "lead passenger email address entered in booking form",
    "expected_content": [
      "Booking confirmation subject line",
      "Unique booking reference number",
      "Hotel name and address",
      "Check-in and check-out dates",
      "Total amount charged",
      "Cancellation policy summary"
    ],
    "in_app_partial_check": {
      "navigate_to": "Booking Confirmation page (immediate post-payment)",
      "observe": "Reference number displayed on confirmation page matches reference number in email"
    },
    "verification_method": "Check test inbox at Mailtrap or equivalent. Confirm email arrives within 2 minutes of booking. Verify all expected_content items are present."
  }
}
```

---

### 3.6 `unobservable_by_design`

**Definition:** The expected state change from the test case action is **intentionally suppressed** by the system — either because this is a mock/demo environment, a simulation, or the system architecture explicitly prevents the observable side effect in this context. The test case cannot be fully verified as written.

**When to use:**
- A mock banking system that does not debit accounts on loan disbursement
- A demo environment where payment processing is simulated (no real card charges)
- A sandbox where email sending is disabled
- A system where a specific feature flag disables an otherwise expected side effect
- Scheduler jobs that are configured to never run in the test environment

**Coverage:** Always `not_coverable`

**Body schema:**
```json
{
  "body": {
    "reason": "string — explanation of why the system suppresses this effect",
    "suppressed_assertion": "string — what the test case expected to happen that does not occur",
    "alternative_assertion": "string — what CAN be verified instead, as a proxy",
    "environment_condition": "string — the specific condition that causes unobservability (e.g. mock flag, disabled feature)"
  }
}
```

**Rules:**
- Always provide `alternative_assertion` — document what partial verification IS possible
- `reason` must reference specific system behavior from the functional spec or known environment config
- This type must NOT be used as an escape hatch for `out_of_band` cases — they are different: `out_of_band` is observable with the right tooling; `unobservable_by_design` is never observable regardless of tooling
- `coverage_note` must describe what would need to change in the environment for full coverage to be possible

**Example:**
```json
{
  "test_case_id": "7.LOAFUN-005",
  "verification_type": "unobservable_by_design",
  "coverage": "not_coverable",
  "coverage_note": "The Parabank mock system explicitly does not debit the collateral account when a loan is approved. Balance verification will always pass regardless of whether the loan logic executed correctly.",
  "body": {
    "reason": "Per the functional specification: 'In this mock system, no actual balance debits occur.' Collateral account balance is never modified on loan approval in this environment.",
    "suppressed_assertion": "Collateral account balance should decrease by the down payment amount following loan approval.",
    "alternative_assertion": "Verify that a new loan account appears in the Accounts Overview table with the correct principal amount, account type 'Loan', and status 'Active'. Verify the loan account number is unique and the open date matches today.",
    "environment_condition": "Mock banking environment — balance mutation disabled globally"
  }
}
```

---

## 4. Coverage Classification

Every verification record must declare its coverage level. This drives the coverage report.

| Coverage | Meaning | Allowed Types |
|---|---|---|
| `verifiable` | The effect can be fully confirmed by navigating within the app or using two sessions | `same_actor_navigation`, `in_page_dynamic`, `cross_actor`, `credential_mutation` |
| `manual_only` | The effect exists but requires a human or external tooling to confirm | `out_of_band` |
| `not_coverable` | The effect is suppressed by system design and cannot be confirmed in this environment | `unobservable_by_design` |

### Coverage Note Rules

`coverage_note` is **required** when coverage is `manual_only` or `not_coverable`. It must:
- Explain the specific reason why automated verification is impossible
- Reference the functional spec or environment behavior that causes the limitation
- For `manual_only`: specify what tooling or external access would enable verification
- For `not_coverable`: specify what environment change would enable coverage

`coverage_note` should be **omitted** (not left blank) when coverage is `verifiable`.

---

## 5. Decision Tree — Choosing Verification Type

Use this decision tree when assigning a verification type to a test case:

```
START: What is the primary observable effect of this test case action?
│
├─► The effect cannot be seen anywhere in the app (email, SMS, external payment)
│     └─► out_of_band | coverage: manual_only
│
├─► The system explicitly suppresses the expected state change (mock, sandbox, disabled feature)
│     └─► unobservable_by_design | coverage: not_coverable
│
├─► The action changes login credentials (password, username)
│     └─► credential_mutation | coverage: verifiable
│
├─► The effect is visible to a DIFFERENT user/role than the one who performed the action
│     └─► cross_actor | coverage: verifiable
│
├─► The effect is visible on the SAME page without any navigation
│   (filter update, inline validation, in-place toggle, dynamic search results)
│     └─► in_page_dynamic | coverage: verifiable
│
└─► The effect is visible on a DIFFERENT page, same session, same user
      └─► same_actor_navigation | coverage: verifiable
```

### Disambiguation Rules

**`out_of_band` vs `unobservable_by_design`:**
- `out_of_band` = effect exists and is real, but lives outside the app. Can be verified with email tooling.
- `unobservable_by_design` = effect is intentionally absent. No tooling helps.

**`same_actor_navigation` vs `in_page_dynamic`:**
- If the actor clicks a link, button, or uses browser navigation to move to a new URL → `same_actor_navigation`
- If the page updates without a URL change (AJAX, reactive UI) → `in_page_dynamic`

**`cross_actor` vs `same_actor_navigation`:**
- If the observing session uses the same credentials as the acting session → `same_actor_navigation`
- If a different account/role must log in to observe the effect → `cross_actor`

**`credential_mutation` vs `same_actor_navigation`:**
- If the test case changes what credentials are used to authenticate → `credential_mutation`
- Any other profile update (name, address, phone) → `same_actor_navigation`

---

## 6. Field Reference

### Common Fields Across All Types

| Field | Description |
|---|---|
| `navigate_to` | The page name or URL path an actor navigates to. Use the canonical page name from the functional spec (e.g. "Accounts Overview", "My Bookings", "Course X → Activities tab"). |
| `observe` | An array of strings specifying exactly what to read or check on the page. Be specific: "balance of account ending in 5001" not "balance". |
| `expected_change` | A description of how the observed values should differ from the pre-check baseline. Always express in terms of the pre-check observation. |
| `role` | The actor's role in the system. Use the functional spec's role names (e.g. "student", "teacher", "authenticated_user", "admin", "maker", "checker"). |

### Field Specificity Guidelines

**Too vague — agent cannot act on these:**
```
"observe": ["the account"]
"expected_change": "balance changes"
"navigate_to": "some dashboard"
```

**Correct specificity:**
```
"observe": ["current balance of Checking account ending in ****5001", "current balance of Savings account ending in ****5002"]
"expected_change": "Checking account balance decreased by $200.00; Savings account balance increased by $200.00; total of both accounts unchanged."
"navigate_to": "Accounts Overview"
```

---

## 7. Real Examples from Known Applications

### Parabank

**Transfer Funds — Internal Transfer**
```json
{
  "test_case_id": "5.TRAFUN-001",
  "verification_type": "same_actor_navigation",
  "coverage": "verifiable",
  "body": {
    "pre_check": {
      "navigate_to": "Accounts Overview",
      "observe": ["balance of source account", "balance of destination account"]
    },
    "post_check": {
      "login_required": false,
      "navigate_to": "Accounts Overview",
      "observe": ["balance of source account", "balance of destination account"],
      "expected_change": "Source account balance decreased by transfer amount; destination account balance increased by the same amount; combined total unchanged."
    }
  }
}
```

**Open New Account**
```json
{
  "test_case_id": "3.OPNACC-001",
  "verification_type": "same_actor_navigation",
  "coverage": "verifiable",
  "body": {
    "pre_check": {
      "navigate_to": "Accounts Overview",
      "observe": ["total number of accounts in the table", "total balance row"]
    },
    "post_check": {
      "login_required": false,
      "navigate_to": "Accounts Overview",
      "observe": ["total number of accounts", "new account row", "funding source account balance"],
      "expected_change": "Account count increased by 1; new account row appears with correct type, Active status, and today's open date; funding source account balance decreased by initial deposit amount."
    }
  }
}
```

**Request Loan — Collateral Balance (Mock System)**
```json
{
  "test_case_id": "7.LOAFUN-002",
  "verification_type": "unobservable_by_design",
  "coverage": "not_coverable",
  "coverage_note": "Parabank mock system does not debit collateral accounts. Balance assertions on collateral account will always show no change regardless of test outcome.",
  "body": {
    "reason": "Functional spec states: 'In this mock system, no actual balance debits occur.'",
    "suppressed_assertion": "Collateral account balance should decrease by down payment amount on loan approval.",
    "alternative_assertion": "Verify a new loan account appears in Accounts Overview with correct principal, type 'Loan', status 'Active', and open date matching today.",
    "environment_condition": "Mock environment — balance mutation globally disabled"
  }
}
```

**Password Change**
```json
{
  "test_case_id": "12.SECSET-001",
  "verification_type": "credential_mutation",
  "coverage": "verifiable",
  "body": {
    "pre_check": {
      "navigate_to": "Security Settings",
      "observe": ["authenticated session is active"]
    },
    "mutation": "Submit Change Password form with valid current password and new strong password",
    "post_check": [
      {
        "attempt": "Log out then attempt login with old password",
        "credential_used": "old",
        "expected_outcome": "failure",
        "expected_message": "Incorrect email or password. Please try again."
      },
      {
        "attempt": "Attempt login with new password",
        "credential_used": "new",
        "expected_outcome": "success",
        "expected_message": "Signed in successfully."
      }
    ]
  }
}
```

---

### PHPTravels

**Hotel Listing — Sidebar Filter**
```json
{
  "test_case_id": "PHPTRV-HOTFIL-001",
  "verification_type": "in_page_dynamic",
  "coverage": "verifiable",
  "body": {
    "page": "Hotels Listing",
    "trigger": "Drag price range slider to $50–$100 per night",
    "observe": "Hotel result cards and result count displayed above the grid",
    "expected_change": "Only hotels with starting price between $50 and $100 remain visible; result count updates; active filter chip '$50–$100' appears in the filter summary bar."
  }
}
```

**Booking Confirmation Email**
```json
{
  "test_case_id": "PHPTRV-BOOK-003",
  "verification_type": "out_of_band",
  "coverage": "manual_only",
  "coverage_note": "Booking confirmation email is sent to an external inbox and cannot be observed within the PHPTravels application UI.",
  "body": {
    "trigger_action": "Complete hotel booking payment with valid credit card",
    "channel": "email",
    "recipient": "email address entered in the booking lead passenger form",
    "expected_content": [
      "Unique booking reference number",
      "Hotel name",
      "Check-in date",
      "Check-out date",
      "Room type",
      "Total amount paid",
      "Cancellation policy"
    ],
    "in_app_partial_check": {
      "navigate_to": "Booking Confirmation page (immediate post-payment screen)",
      "observe": "Reference number displayed on page — must match reference number in email"
    },
    "verification_method": "Access test inbox (Mailtrap or equivalent). Confirm email arrives within 2 minutes. Verify all expected_content fields are present."
  }
}
```

**Review Submitted by User — Visible to Visitor**
```json
{
  "test_case_id": "PHPTRV-REV-001",
  "verification_type": "cross_actor",
  "coverage": "verifiable",
  "body": {
    "actor_a": {
      "role": "authenticated_user_with_completed_booking",
      "action": "Submit 4-star review with text feedback for Hotel X via dashboard Reviews section"
    },
    "actor_b": {
      "role": "unauthenticated_visitor",
      "session": "new_session",
      "navigate_to": "Hotel X detail page → Reviews section",
      "observe": ["review text", "star rating", "reviewer name", "review date", "aggregate rating score"],
      "expected_change": "New 4-star review appears in the Reviews section; aggregate rating updates to reflect the new review."
    }
  }
}
```

---

### Moodle (Teacher → Student)

**Assignment Created by Teacher — Visible to Student**
```json
{
  "test_case_id": "MOODLE-ASSIGN-TC001",
  "verification_type": "cross_actor",
  "coverage": "verifiable",
  "body": {
    "actor_a": {
      "role": "teacher",
      "action": "Create assignment 'Week 1 Essay' in Course X with due date, online text submission enabled"
    },
    "actor_b": {
      "role": "student",
      "session": "new_session",
      "navigate_to": "Course X → Activities tab → Assignments section",
      "observe": ["assignment name", "due date", "submission status column"],
      "expected_change": "Assignment 'Week 1 Essay' appears in the Assignments section with correct due date and submission status 'No submission'."
    }
  }
}
```

**Gradebook Inline Edit**
```json
{
  "test_case_id": "MOODLE-GRADE-TC004",
  "verification_type": "in_page_dynamic",
  "coverage": "verifiable",
  "body": {
    "page": "Gradebook — Grader Report (Edit mode ON)",
    "trigger": "Click grade cell for Student A in Assignment 1 column; enter value 85; click outside cell",
    "observe": "Grade cell for Student A in Assignment 1 column; overall average row at the bottom",
    "expected_change": "Cell displays 85; class average row updates to reflect the new value; cell is no longer in edit state."
  }
}
```

---

### Mifos

**Client Created — Appears in Client Listing**
```json
{
  "test_case_id": "MIFOS-CLI-TC001",
  "verification_type": "same_actor_navigation",
  "coverage": "verifiable",
  "body": {
    "pre_check": {
      "navigate_to": "Clients listing page",
      "observe": ["total client count", "absence of new client name in table"]
    },
    "post_check": {
      "login_required": false,
      "navigate_to": "Clients listing page",
      "observe": ["presence of new client name", "client status badge", "assigned office"],
      "expected_change": "New client row appears in table with status 'Pending', correct office assignment, and account number assigned by system."
    }
  }
}
```

**Admin Creates User — User Can Log In**
```json
{
  "test_case_id": "MIFOS-USR-TC001",
  "verification_type": "cross_actor",
  "coverage": "verifiable",
  "body": {
    "actor_a": {
      "role": "admin",
      "action": "Create new user with username, password, assigned office, and role via Users page"
    },
    "actor_b": {
      "role": "new_user",
      "session": "new_session",
      "navigate_to": "Login page → submit credentials",
      "observe": ["redirect destination after login", "username displayed in top navigation"],
      "expected_change": "Login succeeds and user is redirected to the Home/Dashboard page; username visible in top-right profile area."
    }
  }
}
```

**Account Transfer — Balance Delta**
```json
{
  "test_case_id": "MIFOS-TRF-TC001",
  "verification_type": "same_actor_navigation",
  "coverage": "verifiable",
  "body": {
    "pre_check": {
      "navigate_to": "Source client detail page → Savings account tab",
      "observe": ["available balance of source savings account"]
    },
    "post_check": {
      "login_required": false,
      "navigate_to": "Source client detail page → Savings account tab",
      "observe": ["available balance of source savings account"],
      "expected_change": "Source account available balance decreased by transfer amount. Navigate separately to destination account to verify balance increased by the same amount."
    }
  }
}
```

---

## 8. Coverage Report Format

After generating verification records for all test cases, produce a coverage report in the following format:

```
VERIFICATION COVERAGE REPORT
=============================
Application:      [App Name]
Total Test Cases: [N]
Generated:        [ISO timestamp]

COVERAGE SUMMARY
----------------
verifiable    [N]  ([X]%)   ← can be confirmed by navigating within the app
manual_only   [N]  ([X]%)   ← requires external tooling or human check
not_coverable [N]  ([X]%)   ← system design prevents verification

BREAKDOWN BY VERIFICATION TYPE
-------------------------------
same_actor_navigation    [N]
in_page_dynamic          [N]
cross_actor              [N]
credential_mutation      [N]
out_of_band              [N]  ← all manual_only
unobservable_by_design   [N]  ← all not_coverable

MANUAL_ONLY CASES (require external tooling)
--------------------------------------------
[test_case_id] | [module] | [channel] | [verification_method]
...

NOT_COVERABLE CASES (known gaps)
---------------------------------
[test_case_id] | [module] | [reason] | [alternative_assertion]
...
```

---

## 9. Agent Execution Rules

These are the rules an agent must follow when executing verification records.

### Rule 1 — Read verification_type first
Before processing any other field, read `verification_type`. This determines which fields are required and which execution path to follow.

### Rule 2 — Skip not_coverable cases
If `coverage` is `not_coverable`, do not attempt execution. Log the case as a known gap using the `coverage_note` and `body.reason` fields. Attempt `body.alternative_assertion` as a proxy check if one is provided, but mark it clearly as a partial proxy, not a full pass.

### Rule 3 — Flag manual_only cases without failing them
If `coverage` is `manual_only`, do not mark the test as failed. Log it as pending manual verification. Execute `body.in_app_partial_check` if present and report its result as partial evidence only.

### Rule 4 — Pre-check must be recorded before action
For `same_actor_navigation` and `credential_mutation`, the pre_check observation MUST be recorded before the test case action is executed. An agent must not infer pre-check values from the post-check observation.

### Rule 5 — Cross-actor requires session isolation
For `cross_actor`, Actor B's session must be completely independent of Actor A's session. Do not reuse cookies, tokens, or browser state between the two actors.

### Rule 6 — Specificity over inference
If an `observe` field is ambiguous, do not guess what element to check. Flag the observation field as underspecified in the run log and ask for clarification. Guessing produces false positives.

### Rule 7 — expected_change is deterministic
`expected_change` descriptions must be evaluated deterministically. For numeric deltas ("decreased by transfer amount"), use the actual value observed in pre_check to calculate the expected post_check value. "Transfer amount" is not acceptable as an evaluation criterion — the specific value must be resolved from test data before evaluation.

### Rule 8 — Credential mutation requires logout between attempts
For `credential_mutation`, the current session must be fully terminated before post_check attempts. Do not test credential validity while still authenticated — this produces false positives.

### Rule 9 — Do not navigate during in_page_dynamic
For `in_page_dynamic`, no navigation must occur between `trigger` and `observe`. If the agent causes a navigation (URL change), the result is invalid.

### Rule 10 — Report alternative_assertion as proxy, not pass
When executing `body.alternative_assertion` for an `unobservable_by_design` case, the result must be reported as "PROXY PASS" or "PROXY FAIL", never as a full "PASS". The distinction must be preserved in the report.

---

## 10. Common Failure Modes by App Domain

### Banking / Microfinance (Parabank, Mifos)
| Scenario | Correct Type | Common Mistake |
|---|---|---|
| Balance change after transfer | `same_actor_navigation` | Verifying on the transfer confirmation screen instead of Accounts Overview |
| Loan approval with collateral | `unobservable_by_design` (mock) | Expecting balance debit that never happens |
| Password change | `credential_mutation` | Using `same_actor_navigation` and skipping old-password rejection check |
| New account created | `same_actor_navigation` | Not recording pre-check account count |
| Maker-checker approval | `cross_actor` | Using `same_actor_navigation` with a role-switch in the same session |

### Travel Booking (PHPTravels)
| Scenario | Correct Type | Common Mistake |
|---|---|---|
| Booking confirmation email | `out_of_band` | Treating confirmation page reference number as full verification |
| Sidebar filter | `in_page_dynamic` | Using `same_actor_navigation` (no URL change occurs) |
| Review visibility to public | `cross_actor` | Not testing from a logged-out session |
| External refund on cancellation | `out_of_band` | Checking only the in-app cancellation status |
| Currency change for guest | `in_page_dynamic` | Not noting that this is cookie-based, not profile-based |

### LMS (Moodle)
| Scenario | Correct Type | Common Mistake |
|---|---|---|
| Teacher creates assignment | `cross_actor` | Only verifying from teacher's view |
| Inline grade edit | `in_page_dynamic` | Navigating away before checking the updated cell |
| Student submits assignment | `same_actor_navigation` → teacher's submissions view requires `cross_actor` | Confusing student-side confirmation with teacher-side grading queue update |
| Profile update | `same_actor_navigation` | Treating as `credential_mutation` if only name/address changed |
| Dashboard block edit mode | `in_page_dynamic` | Navigating away and back to check persistence — should be `same_actor_navigation` if you navigate back |

### General
| Scenario | Correct Type |
|---|---|
| Any email notification | `out_of_band` |
| CAPTCHA appears after failed logins | `in_page_dynamic` |
| Payment retry preserves form state | `in_page_dynamic` |
| Social/OAuth login | Flag as `out_of_band` with `verification_method: "manual — observe redirect and return"` |
| Session expiry redirect | `in_page_dynamic` (observe redirect on same interaction) |
| Browser back after logout | `in_page_dynamic` |

---

*End of Specification*
