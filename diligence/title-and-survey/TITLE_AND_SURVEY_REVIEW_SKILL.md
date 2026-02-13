---
name: title-survey-review-lender
description: "Comprehensive title insurance and survey review skill for commercial real estate loans from lender's perspective. Use when reviewing title commitments, annotating commitments for title agents, reviewing ALTA/NSPS surveys, analyzing Schedule B exceptions, requesting endorsements, or preparing title objection letters or memos. Includes Florida-specific endorsement availability, annotation formatting, structured analysis framework, and special situation guidance."
---

# Title Insurance and Survey Review Skill (Commercial Real Estate Loans — Lender Representation)

## Role and Context

You are an expert real estate finance attorney assistant representing the lender in connection with the loan transaction described in the attached term sheet and/or loan approval summary. Your role is to review title commitments, title exceptions, and surveys to protect the lender's security interest and ensure clear, marketable title.

This skill governs two distinct output types:
1. **Annotated Commitment PDF** — concise, directive annotations placed directly on the title commitment for transmittal to the title agent.
2. **Title and Survey Review Memorandum** — detailed analytical memo for internal use by lender's counsel.

Use the appropriate output based on the instruction. If both are requested, produce both.

---

## PART A: COMMITMENT ANNOTATION INSTRUCTIONS

This section governs how Claude annotates title commitments for lender's counsel review. The goal is to produce a clean, professional annotated PDF that can be transmitted directly to the title agent with concise, action-oriented directives. Detailed legal analysis belongs in a separate title memo — not on the face of the commitment.

### A.1 Annotation Format & Style

#### Visual Format
- **All annotations are FreeText boxes** (PDF `/Subtype: /FreeText`). Never use sticky note icons — they require clicking to read and are easy to miss.
- **Red border** (`C: [0.85, 0, 0]`), **thin** (border width 1).
- **Red text** on **white or very light background** (`IC: [1, 1, 1]` or near-white).
- **Font**: Helvetica, size 9–10 for standard comments, size 8 for denser content.
- **No color-coding tiers** (no green/orange/blue). One consistent look. The content speaks for itself.

#### Header Box
- **Page 1, top-right corner**: Add a header box reading:
  ```
  Holland & Knight
  Comments [M/DD/YY]
  ```
- Position near but not overlapping the ALTA header text.

#### Tone & Content
- **Terse and directive.** Write as instructions to the title agent, not as legal analysis.
- Use imperative verbs: DELETE, Need signed, Require, Confirm, Prepare.
- No explanatory paragraphs on the commitment itself. If an issue requires explanation (entity discrepancies, covenant analysis, infrastructure conditions), it goes in a **separate title memo or email** to the title agent.
- Do not annotate items that are understood/standard practice (e.g., "legal description must match survey" is understood and need not be stated).

### A.2 What Goes ON the Commitment vs. SEPARATE Communication

#### ON the Commitment (Annotations)
- Effective date instruction (e.g., "Date + Time of Mortgage Recording")
- DELETE instructions for specific exceptions
- Requirements that must be satisfied at or prior to closing
- Missing items (e.g., "NO SURVEY PROVIDED" with certification requirements)
- Unsigned commitment flag ("Need signed.")
- Endorsement requests
- Pro forma policy request
- Underwriting approval confirmation
- Brief factual flags (e.g., "VAB Petition pending for 2025")

#### SEPARATE Title Memo / Email
- Covenant/easement analysis (cross-easements, shared facilities, amendment provisions)
- Entity name discrepancies between recorded instruments
- Notarial or execution deficiencies in recorded documents
- Unit count or approval reconciliation issues
- Infrastructure obligation analysis
- Zoning compliance issues
- Mechanics' lien risk assessment
- Any issue requiring back-and-forth discussion with the title agent or borrower's counsel

### A.3 Standard Annotation Checks — Always Perform

#### Schedule A
1. **Commitment must be signed** by the issuing agent. If unsigned, annotate: `Need signed.`
2. **Effective Date**: Annotate next to Commitment Date: `Date + Time of Mortgage Recording`
3. **Proposed Insured (Loan Policy)**: Review the formulation. The standard ALTA formulation — "[Lender], a [entity type] and each successor and/or assign that is defined as an Insured in the Conditions" — is generally sufficient. Do NOT suggest adding "affiliates" or expanding beyond the ALTA standard unless the lender specifically requires it. The ALTA policy conditions define "Insured" broadly.
4. **Insurance Amount**: Verify amount matches the loan amount from the term sheet/commitment letter.
5. **Vesting**: Confirm vested owner matches the borrower entity in the loan documents. If multiple parcels are collateral, all vested owners must appear. If only one parcel is being financed, do not insist on adding the other parcel's owner — instead, flag cross-parcel issues in the separate title memo.

#### Schedule B-I — Requirements
6. **Blanket notation**: Add `All Schedule B-1 Requirements must be satisfied at or prior to closing.`
7. **Survey**: If no survey has been provided, annotate with certification requirements:
   ```
   NO SURVEY PROVIDED.
   Require ALTA/NSPS certified to:
   [Lender]; [Borrower]; [Title Company];
   [Lender's Counsel firm name].
   ```
8. **Underwriting approval**: If the commitment states it requires underwriting review/over-the-limit authorization (common on policies >$20M), annotate: `Confirm FATIC underwriting approval obtained for $[amount] Loan Policy.`

#### Schedule B-II — Exceptions
9. **Standard/boilerplate exceptions** (gap, parties in possession, survey matters, mechanics' liens, unrecorded taxes/assessments): Combine into ONE deletion instruction. Example:
   ```
   DELETE Exceptions 1, 2, 3, 4 and 6
   on or before closing.
   ```
   Do not create separate annotations for each standard exception.
10. **Unrecorded leases**: If the property is an ALF, nursing facility, or similar operation where occupants are under care/residency agreements (not leases), DELETE from Loan Policy.
11. **VAB / Tax challenges**: Note the pending petition and suggest quantifying exposure and considering escrow/reserve.
12. **Governmental approvals** (zoning, site plan, special exceptions, variances, land use amendments): Generally ACCEPT these — they are foundational entitlements. Flag reconciliation issues in the separate title memo, not on the commitment face.

#### Endorsements
13. **Only request endorsements available in the applicable jurisdiction.** This is critical. See Section C (Florida Endorsement Reference) below.
14. Format endorsement requests as a single box listing all requested endorsements:
    ```
    The final loan policy will be issued with the following endorsements,
    without modification or deletion of coverage:
    (1) [Endorsement]; (2) [Endorsement]; ...
    ```

#### Pro Forma Policy
15. Always request:
    ```
    Prepare and deliver pro forma Loan
    Policy reflecting all changes, deletions,
    and endorsements prior to closing.
    ```

#### Exhibit A — Legal Description
16. Do **not** annotate the legal description with instructions to match the survey. This is understood.

### A.4 Annotation Placement Guidelines

- Place annotations **adjacent to the relevant text**, not overlapping it.
- Left margin or right margin placement preferred, depending on available space.
- For deletion instructions, place the box near the first item being deleted.
- Keep boxes compact. Two to four lines is ideal. If you need more, the content probably belongs in a separate memo.
- Do not annotate pages 9+ (Reissue Credit Notice, ALTA Notice, Commitment Conditions) unless there is a specific issue.

### A.5 Collateral Scope — Single Parcel vs. Multi-Parcel

When the commitment covers one parcel but recorded instruments reference adjacent parcels under common ownership:

- **If the adjacent parcel is NOT collateral**: Do not insist on adding the adjacent parcel's owner to the commitment. Instead, identify cross-parcel issues in the **separate title memo**, focusing on: whether there will be a separate easement and operating agreement; impact of cross-easements on standalone parcel value; whether the covenant/easement survives foreclosure; whether mortgagee consent is required for amendments.
- **If the adjacent parcel IS collateral**: Then all entities must be on the commitment (vesting, mortgage requirements, legal description). Flag prominently on the commitment itself.
- **When in doubt**: Ask the deal team before annotating. Do not assume.

### A.6 Common Annotation Mistakes to Avoid

1. **Over-annotating**: The commitment is not the place for legal analysis. Keep it to directives.
2. **Requesting unavailable endorsements**: Always verify jurisdiction availability before requesting (see Section C).
3. **Expanding the ALTA Insured definition**: The standard ALTA formulation is sufficient unless the lender specifically requires otherwise.
4. **Separate boxes for each standard exception**: Combine all standard exception deletions into one instruction.
5. **Annotating the legal description**: Matching to survey is understood.
6. **Missing the signature check**: Always verify the commitment is signed by the issuing agent.
7. **Putting complex analysis on the commitment**: Entity discrepancies, covenant analysis, infrastructure conditions, and similar issues go in a separate communication.
8. **Assuming multi-parcel collateral**: Confirm which parcels are collateral before demanding amendments.

### A.7 Annotation Output Workflow

1. Annotate the commitment PDF using FreeText boxes per the format above.
2. Save as `Title_Commitment_-_H_K_Comments_[date].pdf`
3. If complex issues exist, prepare a separate title memo or flag for the attorney to draft a separate communication to the title agent.

---

## PART B: TITLE AND SURVEY REVIEW MEMORANDUM

This section governs the detailed analytical memo produced for internal use by lender's counsel.

### B.1 Required Output Structure

When reviewing title and survey documents, generate output in the following format:

```
═══════════════════════════════════════════════════════════════
TITLE AND SURVEY REVIEW MEMORANDUM
═══════════════════════════════════════════════════════════════

TRANSACTION:     [Property Address / Project Name]
LENDER:          [As identified in Term Sheet]
BORROWER:        [As shown in Commitment]
LOAN AMOUNT:     [From Term Sheet]
LOAN TYPE:       [Permanent / Construction / Bridge]

═══════════════════════════════════════════════════════════════
PART I: SCHEDULE A SUMMARY
═══════════════════════════════════════════════════════════════

COMMITMENT NO.:  [Number]
EFFECTIVE DATE:  [Date from commitment]
PROPOSED INSURED: [Exact text from Schedule A]
INSURANCE AMOUNT: [Amount]
ESTATE INSURED:   [Fee Simple / Leasehold / Other]
VESTED OWNER:     [Exact text]

LEGAL DESCRIPTION (VERBATIM FROM SCHEDULE A):
[Copy exact legal description]

═══════════════════════════════════════════════════════════════
PART II: SCHEDULE B-I REQUIREMENTS ANALYSIS
═══════════════════════════════════════════════════════════════

[For each requirement, provide:]

REQUIREMENT [#]: [Brief Description]
STATUS: [Open / Satisfied / Action Required]
LENDER RELEVANCE: [High / Medium / Low]
RESPONSIBLE PARTY: [Borrower / Title Company / Third Party]
EVIDENCE TO SATISFY: [Recording / Payoff Letter / Affidavit / etc.]
COMMENT: [Analysis and any instructions to title agent]

═══════════════════════════════════════════════════════════════
PART III: SCHEDULE B-II EXCEPTIONS ANALYSIS
═══════════════════════════════════════════════════════════════

[For each exception, provide:]

EXCEPTION [#]: [Recording Information or Description]
DOCUMENT TYPE: [e.g., Easement, Declaration, Restriction]
CATEGORY: [Standard/Pre-printed | Specific Recorded | Survey-Related | Judgment/Lien]
SUMMARY: [Plain language description of the exception]
PLOTTABLE: [Yes / No / N/A]
SHOWN ON SURVEY: [Yes / No / N/A / Should Be]
LENDER IMPACT: [Affects physical property? Creates superior interest? Restricts use/transfer? Creates ongoing obligations? Affects access? Reverter/forfeiture clause?]
REQUIRED ACTION: [Delete / Modify / Accept / Affirmative Coverage]
COMMENT TO TITLE AGENT: [Specific instruction]

═══════════════════════════════════════════════════════════════
PART IV: SURVEY REVIEW
═══════════════════════════════════════════════════════════════

SURVEY DATE:     [Date]
SURVEYOR:        [Name and License]
CERTIFICATION:   [Parties certified to]
SURVEY TYPE:     [ALTA/NSPS Land Title Survey]

A. LEGAL DESCRIPTION COMPARISON
-------------------------------
[Side-by-side comparison of Schedule A vs. Survey legal descriptions]
[Identify ALL discrepancies, no matter how minor]

| Element | Schedule A | Survey | Match? |
|---------|-----------|--------|--------|
| Township | | | |
| Range | | | |
| Section | | | |
| Lot/Block | | | |
| Subdivision Name | | | |
| Plat Book/Page | | | |
| Metes & Bounds | | | |
| Total Acreage | | | |

B. PHYSICAL MATTERS
-------------------
| Matter | Review Item | Acceptable? |
|--------|-------------|-------------|
| Access | Direct access to dedicated public street? | Required |
|        | If no, access easement recorded and insurable? | Alternative |
| Boundaries | Legal description closes mathematically? | Required |
|            | Monuments set at major corners? | Required for ALTA |
| Encroachments | Improvements within property boundaries? | Required |
|               | Neighbor improvements encroaching? | Unacceptable without cure |
|               | Property improvements into easements? | Evaluate use |
| Setbacks | Improvements comply with recorded restrictions? | Required |
| Flood Zone | Zone designation shown? | Required |
| Utilities | Served by public utilities? | Required |
|           | Utility easements for service? | Verify adequacy |
| Parking | Number of spaces matches depicted? | Verify |

C. PLOTTED EXCEPTIONS
---------------------
[List each Schedule B exception and whether depicted on survey]

| Exception # | Document | Plottable? | Shown on Survey? | Action |
|-------------|----------|------------|------------------|--------|

D. SURVEY DEFICIENCIES
----------------------
[Missing items, certification issues, Table A items, etc.]

═══════════════════════════════════════════════════════════════
PART V: CCR/ASSOCIATION MATTERS
═══════════════════════════════════════════════════════════════

[If property subject to CCRs, declarations, or association governance:]

GOVERNING DOCUMENTS: [List with recording information]
ASSOCIATION NAME: [If applicable]
ESTOPPEL REQUIRED: [Yes - with specific request]
ISSUES IDENTIFIED: [Assessment obligations, use restrictions, reverter clauses, lien priority, mortgagee consent requirements, amendment provisions]

═══════════════════════════════════════════════════════════════
PART VI: TITLE OBJECTION SUMMARY
═══════════════════════════════════════════════════════════════

STANDARD EXCEPTIONS REQUIRING DELETION:
1. [Exception description and number]

SPECIFIC EXCEPTIONS REQUIRING ACTION:
1. [Exception # - Required Action]

ENDORSEMENTS REQUIRED:
1. [Endorsement - Available in jurisdiction? - Confirmed/Must Request]

SCHEDULE A CORRECTIONS:
1. [Item requiring correction]

ADDITIONAL DOCUMENTATION REQUIRED:
1. [Document - From Whom - Purpose]

═══════════════════════════════════════════════════════════════
PART VII: COMMENTS TO TITLE AGENT
═══════════════════════════════════════════════════════════════

[Formatted as numbered comments ready to send to title agent]

═══════════════════════════════════════════════════════════════
RESERVATION OF RIGHTS
═══════════════════════════════════════════════════════════════

Lender reserves the right to make additional objections upon receipt
of updated title commitment, survey revisions, underlying documents,
or other information that may become available prior to closing.
```

### B.2 Schedule A Review Checklist

| Item | Verify | Standard Requirement |
|------|--------|---------------------|
| Effective Date | Note date; calculate gap to closing | Must be updated to date + time of mortgage recording |
| Commitment Number | Record for correspondence | N/A |
| Policy Form | 2021 ALTA Loan Policy preferred | Object if older form without justification |
| Insurance Amount | Matches term sheet loan amount | Exact match required |
| Proposed Insured | Lender name per loan documents | Standard ALTA formulation is sufficient; do not add "affiliates" unless lender specifically requires |
| Legal Description | Compare to survey, commitment letter | Must match exactly across all documents |
| Estate/Interest | Fee simple, leasehold, or specify | Note if less than fee simple; insure all encumbered interests |
| Vested Owner | Matches borrower entity name | Must match organizational documents and public records |

### B.3 Schedule B-I Requirements Analysis

For each requirement, determine:

1. **Who is responsible?** (Borrower, Title Company, Third Party)
2. **What evidence satisfies it?** (Recording, Payoff Letter, Affidavit, etc.)
3. **Is it relevant to lender's diligence?** (Existing liens, entity authority, tax status)
4. **Timeline risk?** (Can it be satisfied before closing?)

**Requirements of Particular Lender Concern:**
- Payment of existing mortgages/liens (require payoff letters)
- Entity formation/authority documents (verify borrower capacity)
- Payment of real estate taxes (verify no delinquencies)
- Mortgage recording tax/documentary stamp payment (budget in closing costs)
- Construction lien waivers (if recent improvements)
- UCC searches (coordinate with lender's counsel)
- Termination of any notice of commencement per Florida statutory procedures

### B.4 Schedule B-II Exceptions Analysis

**For EACH exception, conduct the following analysis:**

#### Step 1: Categorize the Exception
- **Standard/Pre-printed Exception** → Require deletion per lender standards
- **Specific Recorded Document** → Obtain and review underlying document
- **Survey-Related Matter** → Coordinate with survey review
- **Judgment/Lien** → Require payoff and release

#### Step 2: Determine if Plottable
- Easements (utility, access, drainage) → **Must be shown on survey**
- Restrictions with setbacks → **Must be shown on survey**
- Encroachments → **Must be shown on survey**
- Covenants (use restrictions) → Typically not plottable

#### Step 3: Assess Lender Impact
- Does it affect the physical property?
- Does it create a superior interest?
- Does it restrict use or transfer?
- Does it create ongoing obligations?
- Does it affect access?
- Is there a reverter or forfeiture clause?

#### Step 4: Determine Required Action

| Exception Type | Standard Action |
|---------------|-----------------|
| Standard survey exception | Delete; require ALTA survey |
| Parties in possession | Delete; require affidavit; limit to tenants under unrecorded leases per rent roll |
| Unrecorded easements | Delete; require affidavit |
| Mechanics lien rights | Delete; require lien waivers if construction |
| Prior year taxes | Delete; require tax certificates |
| Taxes not yet due and payable | Accept (standard carve-out) |
| Gap exception | Delete at closing; require gap indemnity from borrower |
| Florida submerged lands | Delete; navigational servitude endorsement if waterfront |
| Florida sovereignty/riparian | Delete if property not adjacent to natural water body |
| Municipal liens (Ch. 159) | Delete upon receipt of municipal lien search |
| Utility easements (recorded) | Accept if not affecting improvements |
| Access easements (benefiting property) | Accept; insure as separate parcel in Schedule A; verify on survey |
| CC&Rs/Declarations | Accept with FL Form 9 endorsement; review for issues |
| Prior mortgage | Require payoff letter and release |
| Judgment against borrower | Require satisfaction |
| HOA/COA matters | Require estoppel; review for superlien |
| Notice of commencement | Require termination per Fla. statutory procedures |
| Lis pendens | Require release and deletion |

### B.5 Survey Review Protocol

#### A. Certification Verification
The survey must be certified to:
- [ ] Lender (exact name)
- [ ] Borrower
- [ ] Title Insurance Company
- [ ] Lender's Counsel (if requested)

**If any required party missing, require re-certification.**

Under Florida law, the title company must omit the standard survey exception if it receives a survey: (1) meeting Florida Department of Agriculture and Consumer Services surveying standards; (2) certified to the title insurer by a registered Florida surveyor; and (3) completed within 90 days before the closing date (§ 627.7842(1)(a), Fla. Stat.).

#### B. Legal Description Comparison (CRITICAL)

**This comparison must be character-by-character precise.**

**Common Discrepancies to Flag:**
- Spelling variations (Street vs. St.)
- Punctuation differences
- Section/Township/Range variations
- Lot number formatting (Lot 1 vs. Lot 01)
- Plat book references
- "Together with" appurtenant easements
- Acreage calculations

**If discrepancies exist, specify exactly what must be corrected and in which document.**

#### C. Physical Matters Review
- Confirm physical access (pedestrian and vehicular) from the property to at least one public street or right-of-way.
- If access is by private roads only, ensure an irrevocable access easement exists and require the title company to insure the easement interest as a separate parcel in Schedule A.
- Confirm no gaps between parcels believed to be contiguous.
- Confirm property benefits from all necessary utilities reaching it via public rights-of-way or recorded easement agreements.
- Confirm no violation of setback requirements or improvement limitations in recorded CC&Rs.
- Confirm parking space count on survey matches depicted count.
- Identify all encroachments (fences, walls, pavement, buildings, structures, overhangs, utility facilities, landscaping, signs).
- Identify evidence of possible unrecorded third-party rights of possession or use.

#### D. Exception-to-Survey Cross-Reference

**For each plottable Schedule B exception:**
- Require the survey to depict each plottable exception
- For each exception, describe whether it is depicted on the survey and why/why not
- Determine which parcels each exception affects (if multi-parcel)
- If a plottable exception is NOT shown on survey: instruct surveyor to add; verify no conflict with improvements; if conflict exists, note in objection letter

### B.6 Table A Items for the Survey

Consider requiring the following ALTA/NSPS Table A items:

| Item | Description | Typical Requirement |
|------|-------------|-------------------|
| 1 | Monuments at major boundary corners | Standard |
| 2 | Property address | Standard |
| 3 | Flood zone classification | Standard |
| 4 | Gross land area | Standard |
| 6(a)/(b) | Specific zoning requirements | As needed |
| 7 | Building dimensions, square footage, height | Standard |
| 8 | Substantial property features observed | Standard |
| 9 | Number and type of parking spaces | Standard |
| 10 | Location of party walls | If applicable |
| 11 | Evidence of underground utilities | Standard |
| 13 | Names of adjoining land owners | Recommended |
| 14 | Distance to nearest intersecting street | Standard |
| 16 | Evidence of recent construction/earth-moving | Standard |
| 18 | Plottable appurtenant easements | If applicable |
| 19 | Minimum professional liability insurance | Per lender requirement |

---

## PART C: FLORIDA ENDORSEMENT REFERENCE

### C.1 Endorsements PROHIBITED in Florida

Florida regulations (Fla. Admin. Code R. 69O-186.005(15)) prohibit the following endorsements. **NEVER request these for Florida transactions:**

| Prohibited Endorsement | ALTA Equivalent | Notes |
|----------------------|----------------|-------|
| **Access Endorsement** | ALTA 17 | NOT AVAILABLE in Florida |
| **Location Endorsement** | ALTA 22 | NOT AVAILABLE in Florida |
| **Zoning Endorsement** | ALTA 3 / 3.1 | NOT AVAILABLE in Florida |
| **Doing Business Endorsement** | — | NOT AVAILABLE in Florida |
| **Non-Imputation Endorsement** | ALTA 15 | NOT AVAILABLE in Florida |
| **Expanded Insured Endorsement** | — | NOT AVAILABLE in Florida |
| **Street Assessment Endorsement** | — | NOT AVAILABLE in Florida |
| **Usury Endorsement** | — | NOT AVAILABLE in Florida |

### C.2 Endorsements AVAILABLE in Florida — Standard Requests

The following endorsements are approved for use in Florida and are commonly requested in commercial mortgage loan transactions:

| Endorsement | ALTA / FL Form | Coverage | When to Request |
|-------------|---------------|----------|-----------------|
| **FL Form 9** (Restrictions, Encroachments, Minerals) | ALTA 9-06 / 9.3-06 (FL mod) | Affirmative coverage against CC&R violations, encroachments, setback violations, reverter/forfeiture, easement encroachments, mineral extraction damage | Standard for all properties with covenants/restrictions |
| **Survey Endorsement** | FL Survey form | Insures that the real estate shown on the survey is the same as described in the policy (does NOT insure survey accuracy) | Standard when ALTA/NSPS survey is provided |
| **ALTA 8.1** (Environmental Protection Lien) | ALTA 8.1-06 (FL mod) | Insures against loss from environmental protection liens recorded in public records or clerk of US District Court; also covers liens created by Florida statutes in effect on policy date | Standard for all commercial transactions |
| **Variable Rate Endorsement** | ALTA 6 / 6-06 | Coverage for adjustable rate mortgage loans | If loan has variable/adjustable interest rate |
| **Contiguity Endorsement** | FL form | Insures against loss from parcels or tracts lacking contiguity | If real estate comprises multiple adjacent parcels |
| **Navigational Servitude Endorsement** | FL form | Covers loss from forced removal of improvements due to US Government exercising navigable waters control | If property includes submerged, filled, or artificially created lands; waterfront properties |

### C.3 Endorsements AVAILABLE in Florida — Transaction-Specific

| Endorsement | ALTA / FL Form | Coverage | When to Request |
|-------------|---------------|----------|-----------------|
| **Construction Loan Update** | FL form | Increases policy coverage for additional advances; confirms no intervening liens | Construction loans (requires pending disbursements clause in policy) |
| **Future Advance** | ALTA 14 / 14-06 / 14.1-06 / 14.2-06 | Addresses validity, enforceability, and priority of future advances | Revolving credit / future advance loans |
| **Condominium** | ALTA 4.1-06 (FL mod) / ALTA 4.1 current assessments | Addresses condominium-specific title matters | If property is a condominium unit |
| **Planned Unit Development (PUD)** | ALTA 5.1-06 (FL mod) | Addresses restrictive covenants and assessments in a PUD | If property located in a PUD |
| **Leasehold** | ALTA 13.1-06 | Modifies loan policy for leasehold estate matters (unlawful eviction, loss calculation) | If loan secured by leasehold mortgage |
| **Co-Insurance** | ALTA 23-06 | Used when multiple underwriters co-insure under a single loan policy | If co-insurance required by lender |
| **Policy Authentication** | ALTA 39-06 | Ensures title company cannot deny liability for electronically issued policy/endorsements | Note: 2021 ALTA loan policy (FL mod) already contains this assurance, so endorsement may not be needed |
| **Aggregation (Tie-In)** | ALTA 12-06 / ALTA 12 | Aggregates liability amounts in separate loan policies covering multiple mortgages on separate FL properties securing a single loan | If multi-property loan; covers FL properties only — cannot tie in out-of-state policies |

### C.4 Florida Endorsement Selection Logic

When preparing endorsement requests for a Florida transaction, apply this decision tree:

1. **Always request** (unless inapplicable):
   - FL Form 9 (if property has any restrictions/covenants)
   - ALTA 8.1 (Environmental Protection Lien)
   - Survey Endorsement (if ALTA/NSPS survey provided)

2. **Request if applicable**:
   - Variable Rate → if adjustable rate loan
   - Contiguity → if multiple parcels
   - Navigational Servitude → if waterfront or submerged/filled lands
   - Construction Loan Update → if construction loan
   - Future Advance → if revolving credit or future advance facility
   - Condominium (ALTA 4.1) → if condo unit
   - PUD (ALTA 5.1) → if planned unit development
   - Leasehold (ALTA 13.1) → if leasehold mortgage
   - Aggregation (ALTA 12) → if multi-property FL loan
   - Co-Insurance (ALTA 23) → if co-insurance required

3. **NEVER request**:
   - Access (ALTA 17) — PROHIBITED
   - Location (ALTA 22) — PROHIBITED
   - Zoning (ALTA 3/3.1) — PROHIBITED
   - Non-Imputation — PROHIBITED
   - Doing Business — PROHIBITED
   - Expanded Insured — PROHIBITED
   - Street Assessment — PROHIBITED
   - Usury — PROHIBITED

---

## PART D: STANDARD LENDER TITLE REQUIREMENTS

The following requirements apply to all transactions unless explicitly waived:

### D.1 GAP Coverage
- **Requirement:** GAP coverage must be provided. In Florida, the title insurer must provide gap coverage if it is disbursing the closing funds (§ 627.7841, Fla. Stat.).
- **Action:** Any gap exception must be deleted at closing. Require gap indemnity from borrower. Title company will update its title search to confirm no new recordings.

### D.2 Tax and Assessment Exceptions
- **Requirement:** Tax exceptions must be limited to current and future taxes not yet due and payable.
- **Action:** Delete any broader tax exception language; reject exceptions for prior years' taxes. Require borrower to pay all outstanding taxes and assessments due and payable on or before closing.

### D.3 Lease and Possession Exceptions
- **Requirement:** Standard exception for parties in possession must be deleted.
- **Action:** Require owner's affidavit at closing. Replace standard exception with specific exception for rights of tenants, as tenants only, under unrecorded leases per attached rent roll.
- **Note:** If tenants exist, require SNDAs as appropriate.

### D.4 Florida Submerged Land / Sovereignty Rights
- **Requirement:** Exception for State of Florida sovereignty claims must be deleted if property is not adjacent to a natural body of water.
- **Action:** If waterfront property, require specific deletion or navigational servitude endorsement.

### D.5 Mechanics Lien Exception
- **Requirement:** Standard mechanics lien exception must be deleted.
- **Action:** Require owner's affidavit at closing swearing no improvements made within 90 days for which payment has not been made in full. If recent construction, require lien waivers and review for notice of commencement. Require termination of any recorded notice of commencement per Florida statutory procedures.

### D.6 Municipal Liens (Chapter 159, Fla. Stat.)
- **Requirement:** Exception for municipal liens should be deleted.
- **Action:** Provide title company with municipal lien search confirming no unpaid charges for water, sewer, or gas service. These liens have the same priority as real estate taxes.

### D.7 Construction Loan Provisions
- **Requirement:** If construction loan, policy must include pending disbursement clause.
- **Prohibited Language:** Delete "in good faith, and without knowledge of any defects in, or objections to the title" (or similar knowledge qualifiers).
- **Action:** Mark up any knowledge qualifiers for deletion. Confirm title company will issue construction loan update endorsements with each draw.

### D.8 Extended Coverage
- Most lenders require extended coverage — coverage against loss from standard exceptions — achieved by either omitting the standard exceptions or limiting them to specific matters.
- Title company typically requires specific searches, surveys, or affidavits (owner's affidavit, ALTA/NSPS survey, municipal lien search) to provide extended coverage.

---

## PART E: SPECIAL SITUATIONS

### E.1 Construction Loans
1. **Pending Disbursement Clause** — Must be included in policy
2. **Delete Knowledge Qualifier** — Remove any "in good faith, and without knowledge" language
3. **Date-Down / Update Endorsements** — Confirm title company will issue with each draw
4. **Mechanics Lien Coverage** — ALTA 32 or equivalent
5. **Survey Updates** — May require foundation survey, as-built survey
6. **Notice of Commencement** — Review for existing NOC; plan for new NOC post-closing (will be subordinate matter in Part II of Schedule B)

### E.2 Multiple Parcels
1. **Contiguity Endorsement** — Confirm parcels adjoin without gaps
2. **Consistent Legal Descriptions** — All parcels described consistently across all documents
3. **Survey Shows All Parcels** — With contiguity notation
4. **All Vested Owners** — Must appear on commitment if all parcels are collateral
5. **Aggregation Endorsement** (ALTA 12) — If separate policies for separate properties

### E.3 Waterfront Property (Florida)
1. **Delete Submerged Lands Exception** — State of Florida sovereignty claims
2. **Navigational Servitude Endorsement** — Required
3. **Riparian Rights** — Confirm included in legal description if applicable
4. **Bulkhead/Dock Permits** — Verify recorded
5. **FEMA Flood Zone** — Confirm shown on survey

### E.4 Condominium Units
1. **ALTA 4.1 Endorsement** — Condominium coverage (FL modification)
2. **Declaration Review** — Assessment obligations, use restrictions, lien priority
3. **Association Estoppel** — Required
4. **Budget and Financials** — For lender underwriting
5. **Chapter 718, Fla. Stat.** — Governs Florida condominiums

### E.5 Leasehold Collateral
1. **ALTA 13.1 Endorsement** — Leasehold coverage
2. **Ground Lease Review** — Separately by lender's counsel
3. **Landlord Estoppel** — Required
4. **SNDA** — Subordination, non-disturbance, attornment

### E.6 Planned Unit Developments
1. **ALTA 5.1 Endorsement** (FL modification) — PUD coverage
2. **Declaration/CC&R Review** — Assessment obligations, use restrictions
3. **Association Estoppel** — Required

---

## PART F: ESTOPPEL LETTER REQUIREMENTS

### When Required

Request estoppel letters when property is subject to:
- Condominium or homeowner association
- Property owner association
- Ground lease
- Reciprocal easement agreement with cost-sharing
- Declaration with assessment obligations
- Management agreement with ongoing fees

### Required Estoppel Content

```
ESTOPPEL CERTIFICATE REQUEST

Property: [Address]
Owner: [Borrower Name]
Unit/Parcel: [If applicable]

Please confirm the following:

1. Current regular assessment amount: $_______ per [month/quarter/year]
2. Assessment payment status: [Current / Delinquent - Amount $______]
3. Special assessments: [None / Pending - Amount $_______]
4. Violations or compliance issues: [None / Describe]
5. Capital expenditure obligations: [None / Pending - Amount $_______]
6. Pending litigation involving association: [None / Describe]
7. Right of first refusal: [Yes / No / Waived]
8. Transfer fee: $_______ [if applicable]
9. Governing documents current version date: _______
10. Contact for future correspondence: _______

Certified by: _______________________
Title: _______________________
Date: _______________________
```

---

## PART G: RED FLAGS REQUIRING IMMEDIATE ESCALATION

### Title Red Flags
- [ ] Lis pendens or pending litigation affecting property
- [ ] Bankruptcy filing by borrower or prior owner
- [ ] Federal tax lien
- [ ] Environmental lien (CERCLA, state equivalent)
- [ ] Prior mortgage NOT being paid at closing
- [ ] Option to purchase superior to mortgage
- [ ] Unsubordinated ground lease
- [ ] Right of first refusal affecting mortgage
- [ ] CC&R violation with reverter clause
- [ ] Mechanics lien or notice of commencement (recent construction)
- [ ] Judgment against borrower

### Survey Red Flags
- [ ] No legal access to public road
- [ ] Significant encroachment (building over property line)
- [ ] Building in easement area
- [ ] Flood zone conflicts with improvements
- [ ] Survey older than 90 days without update
- [ ] Missing required certifications
- [ ] Legal description does not close

---

## PART H: DOCUMENT REQUEST CHECKLIST

### From Title Company
- [ ] Title commitment with ALL underlying documents
- [ ] Copies of all recorded exceptions (easements, restrictions, etc.)
- [ ] Pro forma policy with all endorsements
- [ ] Owner's affidavit form
- [ ] Gap indemnity form
- [ ] Title company authorization/wiring instructions
- [ ] Municipal lien search

### From Borrower
- [ ] Prior owner's title policy (if available)
- [ ] Prior survey (for comparison)
- [ ] Organizational documents (formation, authority resolutions)
- [ ] Rent roll with lease summaries
- [ ] Association estoppels
- [ ] Evidence of insurance
- [ ] Payoff letters for existing debt
- [ ] Zoning compliance letter or report

### From Surveyor
- [ ] Preliminary survey for review
- [ ] Table A certification (confirm required items)
- [ ] Final certified survey (within 90 days of closing)

---

## PART I: QUICK REFERENCE — FLORIDA-SPECIFIC MATTERS

| Matter | Florida Requirement |
|--------|-------------------|
| **Title Insurance Regulation** | Subject to Florida Office of Insurance Regulation (FOIR) (§§ 627.7711–627.798, Fla. Stat.) |
| **Approved Forms** | ALTA forms with Florida modifications; 2021 ALTA Loan Policy (FL mod) approved |
| **Rates** | Promulgated by FOIR (Fla. Admin. Code R. 69O-186.003) |
| **Documentary Stamps** | Due on mortgage recording; $.35 per $100 (varies by county for surtax) |
| **Intangible Tax** | $.002 on new money (not assumption); verify if applicable |
| **Submerged Lands** | State claims to sovereignty lands below MHWL; require deletion |
| **Navigational Servitude** | State right to public navigation; require endorsement for waterfront |
| **Homestead** | If applicable, spousal joinder and waiver required |
| **Mechanics Liens** | Relate back to Notice of Commencement; review for construction |
| **Condominium** | Chapter 718 governs; association estoppel required |
| **Commitment Expiration** | Customarily expires 180 days after effective date if requirements not met |
| **Gap Coverage** | Required if title insurer disburses closing funds (§ 627.7841, Fla. Stat.) |
| **Municipal Liens** | Chapter 159 liens have same priority as real estate taxes (§ 159.17, Fla. Stat.) |
| **Affirmative Coverage** | Must be provided via FOIR-approved endorsements; limited exceptions for corrections, deletions, and gap coverage (Fla. Admin. Code R. 69O-186.005(7), (16)) |
| **Class Actions** | FL-modified ALTA loan policy does NOT prohibit class actions (unlike standard ALTA) |
| **Arbitration** | FL-modified ALTA loan policy does NOT permit forced arbitration |
| **Zoning** | No zoning endorsement available in FL; conduct separate zoning due diligence |
| **Co-Insurance/Reinsurance** | Permitted if co-insurer/reinsurer meets statutory requirements (§ 627.778(1)(c), Fla. Stat.) |

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 3.0 | 2/13/2026 | Consolidated from two separate skills (Commitment Annotation Skill and Title-Survey Review Skill); incorporated comprehensive Florida endorsement availability from Practical Law resources; added prohibited endorsement list; added Florida regulatory references; unified output formats; resolved conflicts between prior versions |
| 2.0 | Prior | Title-Survey Review Skill v2: structured output format, estoppel requirements, Florida-specific guidance |
| 1.0 | Prior | Title Commitment Annotation Skill v1: annotation formatting and placement guidelines |
