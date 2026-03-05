# Ocean Bank — CAS Extraction Guide

## Purpose

This guide standardizes how deal parameters are extracted from any Credit Approval Summary (CAS). It is referenced by all per-document annotated template skills.

---

## 1. CAS Structure Map

A typical Ocean Bank CAS has this layout (may vary by RM and deal type):

### Page 1: Header / Summary
- **Borrower Name(s)** — top of page, sometimes in header
- **Relationship Manager** — RM name and contact
- **Loan Amount** — prominently displayed
- **Property Description** — brief, with address
- **Deal Type** — New Loan / Modification / Renewal

### Body Sections (order varies)
- **BORROWER(S)** — Legal entity name, type, state of organization
- **GUARANTOR(S)** — Names, types, relationship to borrower
- **LOAN AMOUNT** — Amount, basis (LTV, LTP, DSCR), sizing constraints
- **PURPOSE** — Acquisition, refinance, construction, modification
- **TERM** — Loan term, extension options
- **RATE / INTEREST RATE** — Structure, index, margin, floor
- **AMORTIZATION** — Amortization schedule
- **REPAYMENT** — Payment structure, IO period
- **PREPAYMENT** — Penalty terms
- **COLLATERAL** — Property description, UCC requirement
- **COVENANTS** — DSCR, LTV maintenance, escrow, cross-default
- **CONDITIONS PRECEDENT** — Appraisal, title, survey, reserves
- **REPORTING** — Financial statement requirements
- **FEE** — Commitment or underwriting fee
- **PROPERTY** — Detailed description, address, county, folios
- **CLOSING** — Target closing date

### Approval Section
- **Senior VP** — Approving officer name
- **Bank Officer** — RM name and title

---

## 2. Field Extraction Rules

### Direct Extraction (value appears explicitly in CAS)

| Field | CAS Location | Notes |
|---|---|---|
| Borrower Name | BORROWER(S) section | Use exact legal name including entity suffix (e.g., ", LLC") |
| Borrower Entity Type | After name or in description | "limited liability company", "corporation", "limited partnership", "trust" |
| Borrower State | "a [State] [entity type]" pattern | Extract state from entity description |
| Loan Amount | LOAN AMOUNT field | Dollar amount — verify against any sizing constraints |
| Term | TERM field | Number in years |
| Amortization | AMORTIZATION field | Number in years |
| Interest Rate | RATE section | Read structure carefully — may be fixed, floating, variable, or swap |
| Guarantor Names | GUARANTOR(S) section | List each with type (personal, entity, trust) |
| Property Address | PROPERTY section | Full street address |
| Property County | PROPERTY section | County name |
| Folio Numbers | PROPERTY section | May be single or multiple |
| Closing Date | CLOSING section | Target date |

### Computed Extraction (derived from CAS data)

| Field | Derivation | Formula |
|---|---|---|
| Article (a/an) | First letter of state name | "an" if state starts with A, E, I, O; "a" otherwise |
| Total Guarantors | Count all guarantor lists | len(personal) + len(entity) + len(trust) |
| Maturity Date | Closing date + term | `closing_date + term_years` |
| First Payment Date | Closing date + 30 days | `closing_date + 30 days` |
| IO End Date | Closing date + IO months | `closing_date + io_months` |
| Initial Funding | Loan amount - holdback | `loan_amount - holdback_amount` |
| Commitment Fee ($) | Fee % × basis | `fee_pct × (loan_amount or future_advance)` |

### Boolean Flag Extraction

These are True/False flags derived from whether a CAS section exists or contains specific content:

| Flag | TRUE when | FALSE when |
|---|---|---|
| Holdback | CAS mentions holdback or withheld amount | No holdback section |
| Extension | CAS specifies extension option(s) | No extension section |
| Future Advance | CAS mentions future advance on existing loan | New loan or no advance |
| Commitment Fee | CAS specifies commitment fee | CAS specifies underwriting fee only |
| Prepayment Penalty | CAS specifies penalty rate/terms | CAS says "no penalty" or omits |
| DSCR Covenant | CAS specifies DSCR maintenance covenant | No DSCR covenant section |
| Cross Default | CAS mentions cross-default with another loan | No cross-default section |
| Tenant Reserve | CAS requires tenant reserve | No tenant reserve mentioned |
| Interest Only | CAS specifies IO period | P&I from start |
| Leased Property | Property is income-producing with tenants | Owner-occupied or vacant land |
| UCC Required | CAS mentions UCC filing | No UCC requirement |
| Construction | Purpose is "Construction" | Any other purpose |
| Permanent Phase | Construction loan converts to permanent | Construction only |
| Bad Boy Guarantor | CAS mentions carveout/non-recourse guaranty | Full recourse or no guarantor |
| Reserve Account | CAS requires debt service reserve | No reserve |
| Stabilization Reserve | CAS requires stabilization reserve | No stabilization reserve |
| Interest Reserve | CAS requires interest reserve (usually construction) | No interest reserve |
| Franchise | Property is franchised | Not franchised |
| Star Report | CAS requires STR reports (hotels) | Not a hotel |
| Environmental | CAS requires Phase I or environmental report | No environmental requirement |
| Bond | CAS requires construction bonds | No bond requirement |

### Enumerated Field Extraction

| Field | Possible Values | How to Determine |
|---|---|---|
| New/Existing | "New Loan", "Existing Loan" | Look for "new", "origination" vs. "modification", "renewal", "extension" |
| Loan Purpose | "Acquisition", "Refinance with existing debt", "Refinance free and clear", "Construction" | PURPOSE section — distinguish refinance types by whether existing debt is mentioned |
| Rate Structure | "fixed", "floating", "variable", "swap" | RATE section — "fixed" = one rate for entire term; "floating" = continuously adjusting; "variable" = initial fixed then periodic adjustment; "swap" = mentions swap agreement |
| Index | "SOFR", "Prime" | RATE section — look for "SOFR", "Term SOFR", "CME" (→ SOFR) or "Prime", "Prime Rate", "WSJ" (→ Prime) |
| Prepayment Type | "bona fide", "refinance" | PREPAYMENT section — "bona fide sale" exception vs. "refinance" trigger |
| Tax Escrow | "no escrow", "tax and insurance", "tax and flood insurance", "no escrow during interest only period..." | ESCROW/COVENANTS section |
| Holdback Basis | "Exact Amount", "Calculation" | HOLDBACK section — specific dollar vs. formula |
| DSCR Start | "at closing", "particular year", "conversion to p and i" | COVENANTS section — when DSCR testing begins |
| DSCR Basis | "income and expense statements", "company tax returns" | COVENANTS section — what financials are used |
| Fee Basis | "loan amount", "future advance" | FEE section — basis for commitment fee calculation |
| Property Condition | "full condition", "roof and termite", "roof only", "environmental report" | CONDITIONS section |

---

## 3. Ambiguity Resolution

### Missing Fields

When a CAS field is absent:

1. **Required field with standard default:** Use the default, add `[CONFIRM]` comment
   - Example: No escrow section → default to "no escrow", add `[CONFIRM: Tax escrow — CAS silent, assumed no escrow]`

2. **Required field without default:** Leave placeholder unfilled, add `[CONFIRM]` comment
   - Example: No closing date → leave `[CLOSING DATE]`, add `[CONFIRM: Closing date not specified in CAS]`

3. **Optional field:** Treat as FALSE/not applicable, delete corresponding section
   - Example: No cross-default section → delete cross-default covenant

### Ambiguous Values

When a CAS value could be interpreted multiple ways:

1. **State both interpretations** in a `[REVIEW]` comment
2. **Draft using the more conservative interpretation** (the one that includes more protective language for the bank)
3. **Show the alternative** so the attorney can quickly switch if needed

Example: CAS says "interest rate to be determined at closing"
- Draft with formula language (rate TBD): "[IF: FIXED RATE TBD]" variant
- Add: `[REVIEW: Rate not stated in CAS — drafted with index + margin formula. If rate is known at closing, replace with specific rate.]`

### Conflicting Values

When CAS contains contradictory information:

1. **Note both values** in a `[REVIEW]` comment
2. **Use the value from the most specific section** (e.g., RATE section overrides summary)
3. **Never silently resolve** — the attorney must see the conflict

---

## 4. Output Format

After extracting all fields, produce a structured parameter object. Print a summary for user confirmation.

### Parameter Dictionary Structure

```json
{
  "deal": {
    "borrower_name": "ABC PROPERTIES, LLC",
    "borrower_state": "Florida",
    "borrower_entity": "limited liability company",
    "new_loan": "New Loan",
    "loan_purpose": "Acquisition",
    "loan_amount": 5000000.00,
    "relationship_name": "John Smith"
  },
  "rate": {
    "structure": "fixed",
    "fixed_rate": 6.25,
    "fixed_rate_now": true,
    "index": null,
    "margin_rate": null,
    "floor_rate": null
  },
  "term": {
    "term": 5,
    "amortization_period": 25,
    "interest_only_period": false,
    "extension": false,
    "construction_term": null,
    "permanent_phase": false
  },
  "guarantor": {
    "guarantor": true,
    "personal_guarantors": [{"name": "John Smith"}],
    "entity_guarantors": [],
    "trust_guarantors": [],
    "bad_boy_guarantor": false,
    "existing_ownership": false
  },
  "covenants": {
    "dscr_covenant": true,
    "dscr_covenant_rate": 1.25,
    "dscr_net_operating_income": true,
    "tax_escrow": "no escrow",
    "cross_default": false,
    "tenant_reserve": false
  },
  "property": {
    "description": "retail shopping center",
    "address": "123 Main St, Miami, FL 33131",
    "county": "Miami-Dade",
    "folios": [{"folio_number": "01-3456-789-0010"}]
  },
  "fees": {
    "commitment_fee": true,
    "commitment_fee_amount": 1.00,
    "commitment_fee_basis": "loan amount",
    "closing_date": "2026-06-01"
  },
  "flags": {
    "holdback": false,
    "future_advance": false,
    "prepayment_penalty": true,
    "leased_property": true,
    "content_included": true,
    "reserve_account": false,
    "construction": false
  },
  "signatory": {
    "status": "EXTERNAL INPUT REQUIRED",
    "note": "Attorney must provide signing chain"
  },
  "bank": {
    "senior_vice_president": "Wayne Smith",
    "bank_officer": "Jane Doe",
    "bank_officer_position": "VP"
  },
  "review_items": [
    "Closing date not specified — left as placeholder",
    "Signatory information required from attorney"
  ]
}
```

### Confirmation Summary Format

```
═══════════════════════════════════════
Deal: ABC PROPERTIES, LLC — $5,000,000 Acquisition
═══════════════════════════════════════
Type: New Loan | Fixed Rate: 6.25% | Term: 5 years | Amort: 25 years
Guarantor: John Smith (Personal, Full Recourse)
Property: Retail shopping center, 123 Main St, Miami-Dade County
Fee: 1.00% Commitment Fee

Documents to generate:
  ✓ Commitment Letter
  ✓ Promissory Note
  ✓ Mortgage
  ✓ Assignment of Leases and Rents
  ✓ Guaranty Agreement (Personal)
  ✓ Borrower's Reps
  ✓ Officer's Certificate (Borrower)

Items needing clarification:
  ⚠ Closing date not specified in CAS
  ⚠ Signatory information required from attorney
═══════════════════════════════════════
```

---

## 5. Document Selection Rules

Based on extracted parameters, determine which documents to generate:

| Document | Generate When |
|---|---|
| Commitment Letter | Always |
| Promissory Note | Always |
| Mortgage | Always |
| Assignment of Leases and Rents | Leased property |
| Guaranty Agreement (Personal) | Personal guarantors exist |
| Guaranty Agreement (Entity) | Entity guarantors exist |
| Guaranty Agreement (Trust) | Trust guarantors exist |
| Bad Boy Guaranty Agreement | Bad boy guarantor |
| Borrower's Reps | Always |
| Officer's Certificate (Borrower) | Always |
| Officer's Certificate (Guarantor) | Entity guarantors exist |
| Construction Loan Agreement | Construction purpose |
| Assignment of Construction Docs | Construction purpose |
| Notice of Commencement | Construction purpose |
| Cooperation Agreement | Always |
| Garnishment Waiver | Always |
| Post-Closing Agreement | Always |
| Anti-Coercion | Always |
| Subordination Agreement | When required by conditions |
| UCC Financing Statement (FL) | UCC required, FL property |
| UCC Financing Statement (Other) | UCC required, out-of-state |
| Loan Related Restricted Account Agmt | Reserve account required |
| Affidavit of Posting | Construction purpose |
| Trustee Affidavit | Trust guarantors exist |
