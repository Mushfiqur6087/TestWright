# Analysis: GPT-5-mini Generated Tests vs Ground Truth
**Project:** ParaBank
**Ground Truth:** `Parabank-ground-truth/test-cases.md`
**Generated:** `Parabank-gpt-5-mini/test-cases.md`
**Analysis Date:** 2026-03-24

---

## 1. Executive Summary

| Metric | Ground Truth | GPT-5-mini Generated |
|--------|-------------|----------------------|
| Total Tests | 180 | 388 |
| Modules | 13 | 13 |
| Expansion Factor | — | 2.16× |
| GT Coverage | — | ~90% (≈162/180 GT intents covered) |
| Extra Tests | — | ~226 not in GT |

**Top 3 Findings:**

1. **UI/UX tests are almost entirely absent** — GT has 15 UI/UX tests (password masking, navigation menu highlight, column headers, etc.); the agent generates none of these.
2. **Negative tests are massively over-generated** — Transfer Funds alone has 71 generated tests vs 14 in GT (5×), mostly because every field is tested for empty/invalid in both internal and external transfer modes separately.
3. **Per-field format splitting inflates counts** — GT writes 1 "invalid email format" test; the agent splits it into 5 separate tests (missing `@`, missing domain, missing local part, invalid characters, multiple `@`). Same pattern applies to ZIP, phone, account numbers across all modules.

---

## 2. Module Coverage Scorecard

| Module | GT Count | Generated | Coverage | Status |
|--------|----------|-----------|----------|--------|
| Login | 16 | 18 | 94% | ✅ Good |
| Registration | 24 | 32 | 83% | ⚠️ Partial |
| Accounts Overview | 10 | 31 | 90% | ✅ Good |
| Open New Account | 13 | 16 | 92% | ✅ Good |
| Transfer Funds | 14 | 71 | 93% | ✅ Good (over-generated) |
| Bill Pay / Payments | 15 | 24 | 87% | ⚠️ Partial |
| Request Loan | 18 | 30 | 94% | ✅ Good |
| Update Contact Info | 18 | 23 | 83% | ⚠️ Partial |
| Manage Cards | 10 | 32 | 90% | ✅ Good |
| Investments | 13 | 37 | 92% | ✅ Good |
| Account Statements | 9 | 28 | 100% | ✅ Full |
| Security Settings | 9 | 13 | 89% | ✅ Good |
| Support Center | 11 | 33 | 91% | ✅ Good |
| **TOTAL** | **180** | **388** | **~90%** | |

---

## 3. Missing Tests (GT → Not Found in Generated)

### Login (1 missing)
| GT ID | GT Test Title | Why It's Missing |
|-------|---------------|-----------------|
| MW-LOGIN-014 | Password masking (characters are masked in field) | UI/UX — agent doesn't generate visual behavior tests |

_All other Login GT tests are covered._

### Registration (4 missing)
| GT ID | GT Test Title | Why It's Missing |
|-------|---------------|-----------------|
| MW-REG-003 | State dropdown shows all US states | UI/UX — agent doesn't verify dropdown option completeness |
| MW-REG-022 | All fields empty — submit empty form triggers field-level errors | Agent generates per-field empty tests, not "all empty simultaneously" |
| MW-REG-023 | Minimum valid inputs — registration succeeds with minimal data | Boundary — agent doesn't test "just enough data" scenarios |
| MW-REG-024 | Maximum length inputs — system handles very long strings gracefully | Boundary — agent tests max length as rejection, not graceful handling |

### Accounts Overview (1 missing)
| GT ID | GT Test Title | Why It's Missing |
|-------|---------------|-----------------|
| MW-AO-010 | Navigation menu "Accounts Overview" highlighted when active | UI/UX — agent never tests active nav state |

_Note: Generated over-generates here (31 vs 10 tests) with defect-detection negative tests that GT doesn't have (see Section 4)._

### Open New Account (1 missing)
| GT ID | GT Test Title | Why It's Missing |
|-------|---------------|-----------------|
| MW-ONA-003 | Interactive account type cards show features and min deposit requirements | UI/UX — agent generates a form elements check but doesn't verify card content |

### Transfer Funds (1 missing)
| GT ID | GT Test Title | Why It's Missing |
|-------|---------------|-----------------|
| MW-TF-014 | Minimum transfer ($0.01) — succeeds or shows minimum amount error | Agent tests zero and negative but not the $0.01 boundary minimum |

### Bill Pay / Payments (2 missing)
| GT ID | GT Test Title | Why It's Missing |
|-------|---------------|-----------------|
| MW-BP-002 | Quick select payee — fields auto-populated from preset payees | Agent doesn't know about the quick-payee feature from the spec |
| MW-BP-003 | Balance updated after successful payment (state verification) | Agent generates functional tests but doesn't add post-action balance verification as a standalone test |

### Request Loan (1 missing)
| GT ID | GT Test Title | Why It's Missing |
|-------|---------------|-----------------|
| MW-RL-004 | Loan type cards display exact APR rates (7.5%, 4.5%, 3.5%) | Agent tests form elements but doesn't verify the specific APR values |

### Update Contact Info (3 missing)
| GT ID | GT Test Title | Why It's Missing |
|-------|---------------|-----------------|
| MW-UCI-004 | Update Last Name individually — success | Agent only tests full profile update and phone-only update, not each field in isolation |
| MW-UCI-005 | Update Street Address individually — success | Same — agent doesn't generate per-field update positive tests |
| MW-UCI-006 | Update City individually — success | Same |
| MW-UCI-007 | Update State individually — success | Same |
| MW-UCI-008 | Update ZIP Code individually — success | Same |

_Note: The agent covers "update all fields" and "update phone only" but not "update each field individually". This is a systematic gap — GT tests per-field updates as separate positive tests._

### Manage Cards (1 missing)
| GT ID | GT Test Title | Why It's Missing |
|-------|---------------|-----------------|
| MW-MC-010 | Invalid date range — travel end date before start date | Agent tests invalid date format but not inverted start/end date order |

### Investments (1 missing)
| GT ID | GT Test Title | Why It's Missing |
|-------|---------------|-----------------|
| MW-INV-004 | Fund symbol autocomplete shows suggestions while typing | Agent tests with/without autocomplete selection but not the autocomplete dropdown appearing |

### Account Statements (0 missing)
_All GT tests fully covered._

### Security Settings (1 missing)
| GT ID | GT Test Title | Why It's Missing |
|-------|---------------|-----------------|
| MW-SS-009 | Collapsible panel — panel collapses/expands on header click | Agent references the panel in preconditions but never tests the collapse/expand behavior itself |

### Support Center (1 missing)
| GT ID | GT Test Title | Why It's Missing |
|-------|---------------|-----------------|
| MW-SC-011 | Email confirmation received after callback submitted | Agent mentions "confirmation email" in expected results but doesn't test email receipt as a standalone case |

---

### Root Cause Summary of Missing Tests

| Root Cause Category | Count | Examples |
|--------------------|-------|---------|
| **UI/UX tests** | 5 | Password masking, nav highlight, collapsible panel, state dropdown, card content |
| **Per-field individual update (positive)** | 5 | Update First Name / Last Name / Address / City / ZIP individually |
| **Quick select / pre-populated flows** | 1 | Quick payee selection |
| **"All empty" global validation** | 1 | Submit completely empty registration form |
| **Exact content verification** | 2 | APR values on cards, autocomplete dropdown appearing |
| **Post-action state verification (standalone)** | 1 | Balance after bill payment |
| **Behavior/interaction tests** | 2 | Collapse/expand panel, $0.01 minimum transfer |

---

## 4. Extra Tests (Generated → Not in GT)

### What the Agent Adds Beyond GT

#### a) Transfer Funds: 57 extra tests
GT covers the core 14 scenarios cleanly. The agent generates 71 by:

**Valuable additions:**
- `TRANSF-059`: Amount just below available balance (boundary, not in GT)
- `TRANSF-064/065/066`: Min/max transfer amount boundaries (not in GT)
- External transfer max account number length (TRANSF-062/063)

**Likely noise (~40 tests):**
- Every field empty/invalid is tested twice — once for internal transfer, once for external transfer
- Example: "Amount empty" appears as both TRANSF-010 (internal) and TRANSF-030 (external), etc.
- GT correctly handles this with one test per validation rule

#### b) Accounts Overview: 21 extra tests
GT: 10 tests. Generated: 31 tests.

**Unique pattern — "Defect detection negatives":** The agent inverts the UI/UX display tests into negative tests:
- "Accounts table **missing**" → flags as defect
- "Account number shown **unmasked**" → flags security defect
- "Footer row **missing**" → flags defect
- "Footer total does **not** equal sum" → flags calculation defect

This is a novel pattern not present in GT — useful for automated regression but verifies the absence of expected elements rather than their presence.

#### c) Account Statements: 19 extra tests
GT: 9 tests. Generated: 28 tests.

**Valuable additions:**
- `ACCOUN-017/018`: Reject future dates in statement period (not in GT)
- `ACCOUN-019/020/021/022/023`: 5 email format sub-variants vs GT's 1 test
- `ACCOUN-024`: Single-day date range (same start = end date)
- `ACCOUN-025/026/027/028`: Email length boundary tests

#### d) Support Center: 22 extra tests
GT: 11. Generated: 33.

**Valuable additions:**
- `SUPPOR-001 to SUPPOR-004`: One test per category (Account/Technical/Security/Other) — GT has just 1 "send message successfully"
- `SUPPOR-016`: Message body with only whitespace rejected
- `SUPPOR-025`: Weekend date rejected (business day rule)
- `SUPPOR-026/027/028`: Phone format/length boundary tests

**Conflict with GT:**
- Generated `SUPPOR-007`: "Send message with **no subject** (subject optional)" — PASSES
- GT `MW-SC-003`: "Empty subject" — should FAIL with validation error
- **This is a test assumption conflict** — the agent treats Subject as optional, GT treats it as required

#### e) Investments: 24 extra tests
GT: 13. Generated: 37.

**Valuable additions:**
- `INVEST-019`: Contribution amount exactly at minimum boundary
- `INVEST-034`: Fractional quantity test (if platform supports it)
- `INVEST-035`: Very large quantity beyond max
- `INVEST-016`: Start date equal to today (boundary — GT only tests past date)
- Separate empty-field tests for all 5 Create Plan fields

#### f) Security Settings: 4 extra tests
**Valuable additions:**
- `SECURI-012`: New password exceeds maximum length (not in GT)
- `SECURI-013`: New password exactly at maximum length (not in GT)
- `SECURI-004`: Post-success state — form cleared and success message (not in GT)

---

## 5. Category Gap Analysis

| GT Category | GT Count | Generated Equivalent | Approx Coverage |
|-------------|----------|----------------------|-----------------|
| Functional Tests | 55 | positive | ~88% |
| Negative Tests | 89 | negative | ~97% |
| UI/UX Tests | 15 | (no equivalent) | ~13% |
| Boundary Tests | 21 | edge_case | ~95% |
| E2E Scenarios | 4 | (none) | 0% |

**Key insight:** The agent excels at Negative and Boundary tests. It completely skips UI/UX tests. E2E scenarios are structurally absent — the agent generates single-feature tests only.

**UI/UX tests missed (15 total):**
| GT ID | Test |
|-------|------|
| MW-LOGIN-014 | Password masking |
| MW-LOGIN-015 | Success flash message (covered in expected result, not standalone) |
| MW-AO-007 | Table column headers visible |
| MW-AO-008 | Currency formatting ($X,XXX.XX) |
| MW-AO-009 | Negative balance display |
| MW-AO-010 | Navigation menu highlight |
| MW-ONA-003 | Interactive cards show features |
| MW-REG-002 | All form fields displayed (partially covered) |
| MW-REG-003 | State dropdown lists all US states |
| MW-TF-003 | Source account filter (Checking/Savings only) — COVERED (TRANSF-061) |
| MW-TF-004 | Transfer type toggle changes destination options — COVERED |
| MW-INV-004 | Fund symbol autocomplete shows suggestions |
| MW-SS-009 | Collapsible panel behavior |
| MW-SC-006 | Category dropdown shows all options — COVERED |
| MW-SC-008 | Phone pre-filled in callback form — COVERED (SUPPOR-009) |

_Effectively ~6 UI/UX tests are fully absent; the rest are partially covered in preconditions or expected results but not as explicit test goals._

---

## 6. Test Quality Comparison (Sample Pairs)

### Pair 1: Valid Login
**GT (MW-LOGIN-001):**
- Steps: 4 steps, mentions specific credentials (admin@parabank.com / Admin123!@#)
- Expected: Flash message "Signed in successfully." + redirect
- Quality: Concise, uses real mock data

**Generated (1.LOGIN-001):**
- Steps: 4 steps, uses generic "valid registered email address"
- Expected: "System flashes 'Signed in successfully.' and redirects to Accounts Overview"
- Quality: More verbose, no hardcoded values (by design), matches expected result text

**Verdict:** Generated matches GT quality; deliberate choice to avoid hardcoded values.

---

### Pair 2: Incorrect Password
**GT (MW-LOGIN-005):**
- Expected: `"Incorrect email or password. Please try again."`, password field cleared
- Combines error message verification + UI behavior in one test

**Generated (1.LOGIN-004 + 1.LOGIN-006):**
- SPLIT into 2 tests: one for error message, one for field cleared
- Both tests are present; more granular but same total coverage

**Verdict:** Generated correctly covers both scenarios but is more verbose.

---

### Pair 3: Transfer Funds — Empty Amount
**GT (MW-TF-005):** 1 test: "Empty amount → Validation error"

**Generated:** `5.TRANSF-005` (internal) + `5.TRANSF-026` (external) = 2 tests for same scenario
- Generates the same test twice for internal vs external transfer type
- This pattern repeats for all 7 field-empty tests = 14 tests instead of 7

**Verdict:** This is the primary cause of test count inflation in Transfer Funds.

---

### Pair 4: Update Contact Info — Per-field Updates
**GT:** 7 separate tests (MW-UCI-003 to MW-UCI-009): update First Name, Last Name, Address, City, State, ZIP, Phone individually

**Generated:** Only 2 positive tests:
- "Update all fields simultaneously" (8.UPDATE-002)
- "Update phone number only" (8.UPDATE-003)

**Verdict:** GT has better granularity for positive tests here. Generated misses 5 individual field update tests.

---

### Pair 5: Account Statements — E-Statement Email Validation
**GT (MW-AS-008):** 1 test: "Invalid email → validation error, field highlighted"

**Generated:** 5 tests (ACCOUN-019 to ACCOUN-023): missing `@`, missing domain, missing local part, invalid characters, multiple `@`

**Verdict:** Generated provides significantly better coverage for email validation edge cases.

---

## 7. Overall: What Types of Tests Does the Agent Generate Extra?

The agent systematically over-generates in these patterns, ranked by volume:

### #1 — Field-Empty Tests Split by Transfer Mode (largest inflator)
When a form has multiple modes (e.g., Internal vs External Transfer), the agent generates every required-field-empty test for **each mode separately**. GT writes them once.
- Impact: **+40 tests** in Transfer Funds alone

### #2 — Format Validation Sub-variants
GT: 1 test for "invalid email format"
Agent: 3–5 tests splitting the format error into sub-categories (missing `@`, missing domain, etc.)
This pattern occurs for: email, ZIP code, phone number, account number, fund symbols
- Impact: **+25 tests** across all modules

### #3 — Boundary Tests for Field Lengths
Agent adds `max length accepted` + `just over max length rejected` + `just below min length rejected` for almost every text input field.
GT only does this where the spec explicitly mentions length constraints.
- Impact: **+30 tests** across all modules

### #4 — Defect-Detection Negatives (Accounts Overview pattern)
Agent inverts display/UI tests into negative tests that verify absence of elements.
"Account table missing → flag defect", "Footer row missing → flag defect", etc.
GT doesn't use this pattern; it tests presence positively.
- Impact: **+12 tests** in Accounts Overview

### #5 — Per-Category Functional Variants
When a dropdown has N options, agent creates N separate positive tests (one per option).
Example: Support Center sends message with Category=Account, Technical, Security, Other = 4 tests.
GT has 1 "send message successfully" test.
- Impact: **+10 tests** across modules

### #6 — State Verification as Standalone Tests
Agent extracts the "state after action" check from expected results and makes it a separate test.
Example: `ACCOUN-012` "Footer total updates correctly when balances change" vs GT verifying total in MW-AO-004.
- Impact: **+8 tests** across modules

---

## 8. Agent Improvement Recommendations

| Priority | Recommendation | Addresses |
|----------|---------------|-----------|
| High | Add `ui_ux` as a 4th test type in the Test Generation Agent prompt | Missing UI/UX tests (masking, layout, nav state) |
| High | Deduplicate field-empty tests across form modes — write once, note both modes | Transfer Funds inflation |
| High | Add prompt instruction: "test per-field updates individually for profile/form pages" | Missing UCI per-field update tests |
| Medium | Add `quick_select` / `auto_populate` as a test pattern to cover pre-fill flows | Missing quick payee select |
| Medium | Add E2E test generation as a separate pipeline step after module tests | Missing E2E scenarios |
| Medium | Instruct agent to verify exact flash/error message text from the spec | Expected result vagueness |
| Low | Reduce format sub-variants to 2 max (valid, invalid) unless spec specifies multiple rules | Format test inflation |
| Low | Add `collapsible_ui` and `dropdown_content` as explicit test patterns | Collapsible panel, dropdown content |
