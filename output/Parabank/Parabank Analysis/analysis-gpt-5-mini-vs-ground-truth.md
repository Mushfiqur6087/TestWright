# Analysis: GPT-5-mini Generated Tests vs Ground Truth (Updated)
**Project:** ParaBank
**Ground Truth:** `Parabank-ground-truth/test-cases.md` (updated — UI/UX tests removed)
**Generated:** `Parabank-gpt-5-mini/test-cases.md` (updated run)
**Analysis Date:** 2026-03-24

---

## 1. Executive Summary

| Metric | Ground Truth | GPT-5-mini Generated |
|--------|-------------|----------------------|
| Total Tests | 173 | 247 |
| Modules | 13 | 13 |
| Expansion Factor | — | 1.43× |
| GT Coverage | — | ~87% (≈151/173 GT intents covered) |
| Missing GT Tests | — | ~22 not found in generated |
| Extra Tests | — | ~94 beyond GT |

> **Comparison with previous run:** Old gpt-5-mini generated 388 tests (2.16×). New run produces 247 (1.43×) — a 36% reduction in total tests and significantly tighter alignment with GT. GT was also trimmed from 180 → 173 (7 UI/UX tests removed).

**Top 3 Findings:**

1. **Per-field individual update tests still absent** — Update Contact Info covers only 11/18 GT intents; all 7 per-field individual update positives (First Name, Last Name, Address, City, State, ZIP, Phone individually) are missing.
2. **Security Settings password policy collapsed** — GT has 5 specific tests (no uppercase, no lowercase, no number, no special char, too short); agent generates 1 generic "policy violation" test. Coverage appears complete but granularity is lost.
3. **Defect-detection negatives persist in Accounts Overview** — Agent inverts display tests into 8 extra "missing element" negative tests (e.g., "footer row missing", "account number unmasked"). GT has 6 straightforward positive display tests; agent generates 16.

---

## 2. Module Coverage Scorecard

| Module | GT Count | Generated | Coverage | Status |
|--------|----------|-----------|----------|--------|
| Login | 13 | 14 | 92% | ✅ Good |
| Registration | 24 | 25 | 83% | ⚠️ Partial |
| Accounts Overview | 6 | 16 | 100% | ✅ Full (over-generated) |
| Open New Account | 13 | 14 | 85% | ⚠️ Partial |
| Transfer Funds | 14 | 16 | 86% | ⚠️ Partial |
| Bill Pay | 15 | 20 | 87% | ⚠️ Partial |
| Request Loan | 18 | 27 | 89% | ✅ Good |
| Update Contact Info | 18 | 17 | 61% | ❌ Poor |
| Manage Cards | 10 | 25 | 100% | ✅ Full (over-generated) |
| Investments | 13 | 25 | 100% | ✅ Full (over-generated) |
| Account Statements | 9 | 20 | 100% | ✅ Full (over-generated) |
| Security Settings | 9 | 8 | 89% | ⚠️ Partial |
| Support Center | 11 | 20 | 91% | ✅ Good |
| **TOTAL** | **173** | **247** | **~87%** | |

---

## 3. Missing Tests (GT → Not Found in Generated)

### Login (1 missing)
| GT ID | GT Test Title | Why It's Missing |
|-------|---------------|-----------------|
| MW-LOGIN-006 | Unregistered email — error message displayed | Merged into 1.LOGIN-004 "Incorrect credentials" which covers both wrong password and unregistered email as a single test |

_All other Login GT tests are covered._

---

### Registration (4 missing)
| GT ID | GT Test Title | Why It's Missing |
|-------|---------------|-----------------|
| MW-REG-003 | State dropdown shows all US states | Agent checks form field presence (2.REGIST-002) but does not verify dropdown option completeness |
| MW-REG-022 | All fields empty — submit empty form triggers field-level errors | Agent generates per-field empty tests individually; no simultaneous all-empty scenario |
| MW-REG-023 | Minimum valid inputs — registration succeeds with minimal data | Agent does not test "just enough data" success boundary |
| MW-REG-024 | Maximum length inputs — system handles very long strings gracefully | Agent tests length as rejection, not graceful handling |

---

### Open New Account (2 missing)
| GT ID | GT Test Title | Why It's Missing |
|-------|---------------|-----------------|
| MW-ONA-007 | Savings deposit below minimum ($50 entered for $100 min) | Agent tests only Checking below-minimum; Savings-specific boundary not generated |
| MW-ONA-012 | Exact minimum Savings ($100) — account opens successfully | Same pattern — exact-minimum boundary only tested for Checking, not Savings |

---

### Transfer Funds (2 missing)
| GT ID | GT Test Title | Why It's Missing |
|-------|---------------|-----------------|
| MW-TF-009 | Same account selected as source and destination — error or prevented | Agent tests empty source/destination but not same-account conflict |
| MW-TF-014 | Minimum transfer ($0.01) — succeeds or shows minimum amount error | Agent tests balance-relative boundaries (equal-to-balance) but not absolute minimum |

---

### Bill Pay (2 missing)
| GT ID | GT Test Title | Why It's Missing |
|-------|---------------|-----------------|
| MW-BP-002 | Quick select payee — fields auto-populated from preset payees | Agent has no knowledge of quick-select payee feature from the spec |
| MW-BP-003 | Balance updated after successful payment (standalone state verification) | 6.PAYMEN-004 tests "payment = full balance → zero" which is a boundary variant, not a general post-payment balance verification |

---

### Request Loan (2 missing)
| GT ID | GT Test Title | Why It's Missing |
|-------|---------------|-----------------|
| MW-RL-004 | Loan type cards display exact APR rates (7.5%, 4.5%, 3.5%) | 7.REQUES-008 checks form elements are displayed but does not verify specific APR values |
| MW-RL-017 | Exact maximum Personal loan ($50,000) — loan processed | Agent tests exact minimum boundaries for all three loan types but not exact maximum |

---

### Update Contact Info (7 missing)
| GT ID | GT Test Title | Why It's Missing |
|-------|---------------|-----------------|
| MW-UCI-003 | Update First Name individually — success | Agent only tests "update all fields" (8.UPDATE-002) and state verification; no per-field positive tests |
| MW-UCI-004 | Update Last Name individually — success | Same pattern |
| MW-UCI-005 | Update Street Address individually — success | Same pattern |
| MW-UCI-006 | Update City individually — success | Same pattern |
| MW-UCI-007 | Update State individually — success | Same pattern |
| MW-UCI-008 | Update ZIP Code individually — success | Same pattern |
| MW-UCI-009 | Update Phone individually — success | Same pattern |

_Note: This is the largest single gap. Agent covers all 9 negative tests correctly but generates only 3 positive tests (pre-populated display, general update success, state verification) instead of 9._

---

### Security Settings (1 missing — quality concern on 5 more)
| GT ID | GT Test Title | Why It's Missing |
|-------|---------------|-----------------|
| MW-SS-009 | Collapsible panel — panel collapses/expands on header click | 12.SECURI-004 verifies the panel "displays all fields" but does not test the collapse/expand interaction |

**Quality concern (not missing, but collapsed):**
GT tests MW-SS-003 through MW-SS-007 as 5 separate tests (too short, no uppercase, no lowercase, no number, no special char). Agent covers all in a single test 12.SECURI-008 "New Password violates strong-password policy." Technically covered but diagnostic value is reduced.

---

### Support Center (1 missing)
| GT ID | GT Test Title | Why It's Missing |
|-------|---------------|-----------------|
| MW-SC-011 | Email confirmation received after callback submitted | Agent mentions callback success but does not generate a standalone email-receipt verification test |

---

### Root Cause Summary of Missing Tests

| Root Cause Category | Count | Examples |
|--------------------|-------|---------|
| **Per-field individual update (positive)** | 7 | UCI First Name / Last Name / Address / City / State / ZIP / Phone individually |
| **Account-type-specific boundaries** | 2 | Savings deposit below min, Savings exact min |
| **Exact content/value verification** | 2 | APR values on loan cards, state dropdown option completeness |
| **Quick-select / auto-populate flows** | 1 | Quick payee selection |
| **Same-object cross-validation** | 1 | Same source and destination account |
| **UI interaction (click behavior)** | 1 | Collapsible panel expand/collapse |
| **Absolute minimum boundaries** | 1 | $0.01 minimum transfer |
| **Post-action state (standalone)** | 1 | Balance after bill payment |
| **Global validation (all-empty)** | 1 | Submit completely empty registration form |
| **Graceful boundary handling** | 1 | Max length inputs handled without crash |

---

## 4. Extra Tests (Generated → Not in GT)

### a) Accounts Overview: +10 extra tests
GT: 6 tests. Generated: 16 tests.

**Pattern — Defect-Detection Negatives:**
The agent inverts every GT positive display test into a corresponding negative "element missing" test:
- `3.ACCOUN-007`: Account number shown unmasked → security defect flag
- `3.ACCOUN-008`: Footer row missing → structural defect flag
- `3.ACCOUN-009` through `3.ACCOUN-013`: Individual column cells missing → defect flags
- `3.ACCOUN-014`: Footer total doesn't match sum → calculation defect
- `3.ACCOUN-015`: Rows not sorted by date → ordering defect
- `3.ACCOUN-016`: Masking shows exactly last 4 chars (edge case precision)

GT verifies presence positively; agent also verifies absence as failure modes. Useful for regression but not in GT style.

---

### b) Manage Cards: +15 extra tests
GT: 10 tests. Generated: 25 tests.

**Valuable additions:**
- `9.MANAGE-004`: Update multiple controls simultaneously (compound state change)
- `9.MANAGE-011`: Add travel notice with dates and destinations (GT has this as MW-MC-006 ✓)
- `9.MANAGE-022/023`: Spending limit exactly at max / just below max (boundary pair)
- `9.MANAGE-024/025`: Travel notice same-day date range / future dates (edge cases)

**Noise additions:**
- `9.MANAGE-010/012`: Two form-display tests (form accessibility, pre-populated card data) — UI/UX style; GT no longer includes these
- `9.MANAGE-013/014/015/016`: Individual empty-field tests for Card Request form (Card Type, Account, Shipping Address, Incomplete Address) — GT has one combined `MW-MC-003/004`
- `9.MANAGE-018/019/020`: Additional validation tests for controls form (limit empty, status empty, invalid format) — not in GT

---

### c) Investments: +12 extra tests
GT: 13 tests. Generated: 25 tests.

**Valuable additions:**
- `10.INVEST-005`: Plan created and visible in schedules list (state persistence verification)
- `10.INVEST-008`: Contribution exactly at minimum value accepted (boundary)
- `10.INVEST-024`: Negative quantity rejected (boundary edge)
- `10.INVEST-025`: Start date equal to today rejected — GT only tests past date, agent adds today boundary

**Noise additions:**
- `10.INVEST-010/011`: Portfolio snapshot display + form field layout (UI display tests; GT removed these)
- `10.INVEST-012` through `10.INVEST-015`: Individual empty-field tests for Execute Trade (Action, Symbol, Quantity, Account each tested separately vs GT's workflow-level approach)

---

### d) Account Statements: +11 extra tests
GT: 9 tests. Generated: 20 tests.

**Valuable additions:**
- `11.ACCOUN-006`: Opt-out of paperless (uncheck → updates without needing email) — not in GT
- `11.ACCOUN-018`: Future dates in custom range — not in GT
- `11.ACCOUN-019`: Same start and end date — not in GT
- `11.ACCOUN-020`: Save preference without changing anything preserves state — not in GT

**Noise additions:**
- `11.ACCOUN-008/009`: Form element display and field enablement tests (UI/UX style; GT removed these)
- `11.ACCOUN-010` through `11.ACCOUN-013`: Individual field-empty tests for each date/account field separately — GT covers with broader validation tests

---

### e) Support Center: +9 extra tests
GT: 11 tests. Generated: 20 tests.

**Valuable additions:**
- `13.SUPPOR-004`: Preferred date = exact next business day (boundary accepted)
- `13.SUPPOR-008`: Message body with rich text formatting (not in GT)
- `13.SUPPOR-014`: Subject length validation
- `13.SUPPOR-020`: Preferred date on non-business day rejected (weekend edge case)

**Noise additions:**
- `13.SUPPOR-009/010/011`: Form display tests for category options, pre-filled phone, callback fields (UI/UX style)
- `13.SUPPOR-016/017/018/019`: Individual field-empty tests for callback form (Reason, Date, Time Window, Phone each separately)

---

### f) Request Loan: +9 extra tests
GT: 18 tests. Generated: 27 tests.

**Valuable additions:**
- `7.REQUES-005`: Insufficient funds in collateral account (distinct from 7.REQUES-006 inadequate collateral value %)
- `7.REQUES-007`: Credit engine denies due to insufficient credit history — not in GT
- `7.REQUES-020/022/024`: Exact minimum boundaries for all three loan types
- `7.REQUES-021/023/025`: Just-below minimum for all three loan types
- `7.REQUES-026/027`: Exactly 10% down / just below 10% down — GT only has one combined test

---

## 5. Category Gap Analysis

| GT Category | GT Count | Generated Equivalent | Approx Coverage |
|-------------|----------|----------------------|-----------------|
| Functional Tests | 55 | positive | ~84% |
| Negative Tests | 89 | negative | ~97% |
| UI/UX Tests | 0 | ~12 form display tests generated | N/A (GT removed) |
| Boundary Tests | 29 | edge_case | ~90% |
| E2E Scenarios | 0 | ~10 state-verification tests | N/A (not in GT) |

**Key insight:** GT no longer carries UI/UX tests. The agent still generates ~12 form-display/element-visibility tests (login form elements, payment form fields, portfolio snapshot display, etc.) — these now appear entirely as extra tests. The agent's strong suit remains negative validation (97% coverage) while the functional positive tests, especially per-field individual updates, are the weakest area (missing 7 UCI tests pulls functional coverage to ~84%).

---

## 6. Test Quality Comparison (Sample Pairs)

### Pair 1: Transfer Funds — Empty Amount (Inflection Point)
**Old gpt-5-mini behaviour:** Generated "Amount empty" twice — once for internal transfer, once for external = +1 duplicate.

**New gpt-5-mini (5.TRANSF-009):** Single test "Transfer Amount field empty validation" — covers both modes. ✅ Fixed.

**Verdict:** Transfer Funds inflation fully resolved. Old: 71 tests vs 14 GT (5×). New: 16 vs 14 (1.14×).

---

### Pair 2: Security Settings — Password Policy
**GT (MW-SS-003 to MW-SS-007):** 5 separate tests, one per missing complexity rule.

**Generated (12.SECURI-008):** 1 test — "New Password violates strong-password policy."

**Verdict:** Coverage is present but diagnostic precision is lost. If the uppercase check fails independently, only a combined test won't pinpoint which rule broke. Granularity gap.

---

### Pair 3: Update Contact Info — Per-Field Positives
**GT (MW-UCI-003 to MW-UCI-009):** 7 separate tests updating First Name, Last Name, Address, City, State, ZIP, Phone individually.

**Generated (8.UPDATE-002):** 1 test — "Successful profile update shows success message."

**Verdict:** Same systematic gap as previous run. Agent generates a general success test but misses isolated field-update verification. Regression risk: a bug in ZIP-only update would not be caught.

---

### Pair 4: Request Loan — Boundary Coverage
**GT (MW-RL-016 to MW-RL-018):** Exact minimum Personal, exact maximum Personal, exactly 10% down.

**Generated:** 7.REQUES-020 (exact min Personal) ✓, 7.REQUES-026 (exactly 10% down) ✓, but **no exact maximum boundary** for any loan type.

**Verdict:** Minimum boundaries well covered; maximum boundaries partially missed. Minor gap.

---

### Pair 5: Accounts Overview — Display Approach
**GT (MW-AO-001 to MW-AO-006):** 6 straightforward positive checks (welcome message shown, accounts listed, masking applied, total correct, sorted, badge visible).

**Generated:** Same 6 positive checks plus 8 negative "defect-detection" tests (element missing, value wrong, order wrong).

**Verdict:** Generated adds regression-oriented tests GT doesn't include. Novel pattern — useful but diverges from GT style. Not a coverage gap, but an over-generation concern.

---

## 7. Over-Generation Patterns (Ranked by Impact)

### #1 — Defect-Detection Negatives (Accounts Overview, +10 tests)
Agent inverts every UI display positive into a negative "what if this element is missing/wrong" test. GT tests presence; agent also tests absence.
- **Impact:** +10 tests in Accounts Overview

### #2 — Manage Cards Field-Level Breakdown (+9 tests)
GT tests card request with one "incomplete address" and one "no account" test. Agent breaks down every field in both forms into individual empty-field tests.
- **Impact:** +9 tests

### #3 — State-Verification Standalones (+8 tests)
Agent extracts post-action state checks as separate test cases:
- `4.OPEN_N-003`: New account visible in overview after creation
- `5.TRANSF-003`: Balance updated and transaction recorded after transfer
- `7.REQUES-004`: Loan success message with account details
- `8.UPDATE-003`: Form fields reflect new values after update
- `10.INVEST-005`: Plan visible in schedules list
- etc.
GT typically folds expected state into the main test's Expected Result column.
- **Impact:** +8 tests

### #4 — Boundary Pairs (min + just-below) for All Loan Types (+6 tests)
GT has one set of boundaries for Personal loan. Agent generates exact-min + just-below-min for all three loan types (Personal, Auto, Home) plus down-payment boundary pair.
- **Impact:** +6 tests

### #5 — UI/UX Form Display Tests (+12 tests)
Since GT now excludes UI/UX, all agent form-display tests are extra:
- Form elements displayed (login, payments, loan, update contact, manage cards, investments, account statements, support)
- Pre-populated field verification (update contact, callback form)
- Portfolio snapshot display
- **Impact:** +12 tests (entire category is now over-generation relative to GT)

### #6 — Account Statements Extra Scenarios (+11 tests)
Opt-out flow, future-date edge cases, same-day range, element display, individual field-empty tests.
- **Impact:** +11 tests

---

## 8. Comparison with Previous gpt-5-mini Run

| Metric | Old Run | New Run | Change |
|--------|---------|---------|--------|
| Total Generated | 388 | 247 | −36% ✅ |
| GT Total | 180 | 173 | −4% (UI/UX removed) |
| Expansion Factor | 2.16× | 1.43× | ✅ Improved |
| GT Coverage | ~90% | ~87% | ≈ Same |
| Missing GT Tests | ~18 | ~22 | ⚠️ Slightly worse |
| Transfer Funds | 71 vs 14 (5×) | 16 vs 14 (1.14×) | ✅ Fixed |
| Format Sub-variants | ~25 extra | ~8 extra | ✅ Reduced |
| Per-field UCI gap | 5 missing | 7 missing | ⚠️ Worse (GT expanded) |

The new run is significantly leaner. The #1 inflation cause (per-mode field-empty split in Transfer Funds) is resolved. Format sub-variants are reduced. The remaining gaps are structural: per-field individual updates, account-type-specific boundaries, and the defect-detection negative pattern in Accounts Overview.

---

## 9. Agent Improvement Recommendations

| Priority | Recommendation | Addresses |
|----------|---------------|-----------|
| High | Add prompt instruction: "for profile/form pages, generate individual field update tests — one test per updatable field" | Missing UCI per-field update tests (7 tests) |
| High | Add prompt instruction: "when a form supports multiple account/entity types (Checking vs Savings, Personal vs Auto vs Home), generate boundary tests for each type separately" | Missing Savings ONA tests, missing loan max boundaries |
| High | Expand password policy coverage: "generate one negative test per policy rule (length, uppercase, lowercase, number, special char) rather than a single combined policy test" | Security Settings granularity collapse |
| Medium | Add `collapsible_ui` and `toggle_behavior` as explicit test patterns | Collapsible panel, transfer type toggle coverage |
| Medium | Suppress defect-detection negative pattern in Accounts Overview — convert back to positive presence checks matching GT style | AO over-generation (+10 tests) |
| Medium | Add `quick_select` / `auto_populate` as a test pattern | Missing quick payee selection |
| Medium | Add prompt: "generate a standalone post-action balance/state verification test for transactions that modify account balance" | Missing MW-BP-003, MW-SC-011 email confirmation |
| Low | Suppress UI/UX form-display tests unless spec explicitly describes unique field interactions | ~12 extra form-display tests now outside GT scope |
| Low | Add `exact_content_verification` pattern: "when cards or dropdowns display specific values from the spec (APR rates, state options), generate a test that verifies those exact values" | Missing APR values test, state dropdown completeness |
