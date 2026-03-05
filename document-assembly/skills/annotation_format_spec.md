# Bank — Annotated Template Skill Format Specification

## Purpose

This document defines the standard format for annotated template "skills" used in AI-guided generation of Bank loan documents. Each skill prescribes exact surgical operations the AI performs on a maximum Word template: replacing bracketed placeholders with CAS-extracted values, deleting inapplicable conditional sections, and flagging edge cases with Word comments.

**Key principle:** The AI performs three operations and ONLY three operations:
1. **Replace** `[PLACEHOLDER]` with extracted value (tracked change: del + ins)
2. **Delete** inapplicable `[IF:]` blocks (tracked change: del)
3. **Flag** edge cases with Word comments

The AI NEVER rewrites, paraphrases, or modifies existing template language.

---

## Architecture Overview

```
CAS (PDF) ──► AI extracts deal parameters (per cas_extraction_guide.md)
                         │
                         ▼
Annotated Template Skill (.md) ──► AI follows prescriptive operations:
                                    - Placeholder Operations Registry
                                    - Conditional Section Map
                                    - Edge Case Catalog
                         │
                         ▼
Maximum Word Template (.docx) ──► AI performs surgical edits:
                                    - Replace [PLACEHOLDER] → value
                                    - Delete inapplicable [IF:] blocks
                                    - Flag edge cases (Word comments)
                         │
                         ▼
Output: Edited .docx with tracked changes + comments
```

Each deal requires:

1. **CAS Extraction Guide** — one shared document (`skills/cas_extraction_guide.md`) standardizing how deal parameters are extracted from any CAS
2. **Maximum Word Templates** — clean .docx files with bracketed placeholders and `[IF:]`/`[END IF:]` conditional markers (in `new_templates/`)
3. **Per-Document Annotated Template Skills** — one per template, prescribing exact surgical operations

---

## Annotated Template Skill Structure

Each template skill is a single markdown file with **five parts** in order:

### Part 1: HEADER + CAS FIELD MAPPING

```markdown
# [Document Name] — Annotated Template Skill

## Document Metadata
- **Template:** `new_templates/[template filename]`
- **When to Generate:** [Conditions]
- **Generated Per:** [Once per deal | Once per borrower | Once per guarantor]
- **Dependencies:** [Other documents needed first]
- **Cross-References:** [Documents that must be consistent]

## Part 1: CAS Field Mapping

Maps CAS fields to template placeholders. See `skills/cas_extraction_guide.md` for extraction details.

| Placeholder | CAS Field | Extraction |
|---|---|---|
| `[BORROWER NAME]` | Borrower(s) | Exact legal name with entity suffix |
| `[$LOAN AMOUNT]` | LOAN AMOUNT | Formatted dollar amount |
| ... | ... | ... |
```

**Rules:**
- Every placeholder in the template must appear in this mapping
- Use placeholder names (not Jinja variable names) as the primary identifier
- Extraction method must be specific enough for the AI to follow unambiguously
- Fields not in the CAS are marked `[EXTERNAL INPUT REQUIRED]`

### Part 2: PLACEHOLDER OPERATIONS REGISTRY

An explicit, exhaustive table of every placeholder and exactly how to handle it.

```markdown
## Part 2: Placeholder Operations Registry

| # | Placeholder | Operation | Format Rule | Template Section(s) |
|---|---|---|---|---|
| P1 | `[BORROWER NAME]` | Replace with legal name | Exact legal name | §1, §3, §RE |
| P2 | `[$LOAN AMOUNT]` | Replace with amount | $X,XXX,XXX.XX | §4 Amount |
| P3 | `[COMMITMENT FEE %]` | Replace with rate | X.XX | §10 Fee |
| ... | ... | ... | ... | ... |
```

**Rules:**
- Every unique placeholder gets a numbered entry
- "Operation" is always "Replace with [value]" — nothing else
- "Format Rule" specifies exact formatting (spelled out, dollar, percentage, etc.)
- "Template Section(s)" identifies where in the document this placeholder appears
- **The AI replaces each placeholder with the extracted value. Nothing else in the surrounding paragraph changes.**

### Part 3: CONDITIONAL SECTION MAP

An explicit table of every conditional block that might be deleted.

```markdown
## Part 3: Conditional Section Map

| # | Section Marker | DELETE when | Scope | Notes |
|---|---|---|---|---|
| C1 | `[IF: NEW LOAN]` blocks | Existing loan | §RE, §4, §5 | Multiple occurrences |
| C2 | `[IF: EXISTING LOAN]` blocks | New loan | §RE, §4 | Multiple occurrences |
| C3 | `[IF: HOLDBACK]` block | No holdback | §4 Amount | ~3 paragraphs |
| ... | ... | ... | ... | ... |
```

**Rules:**
- Every `[IF:]`/`[END IF:]` marker pair in the template gets an entry
- "DELETE when" specifies the exact condition for deletion
- "Scope" identifies affected sections and approximate paragraph count
- **When TRUE:** Delete only the markers. Keep all content between them.
- **When FALSE:** Delete the entire block (markers + content).
- **The AI deletes the identified block via tracked changes. Nothing else changes.**

### Part 4: EDGE CASE CATALOG

Situations where mechanical placeholder replacement and conditional deletion cannot handle the deal.

```markdown
## Part 4: Edge Case Catalog

### EC1: [Edge Case Name]
**When:** [Description of when this arises]
**Template gap:** [What the template doesn't handle]
**Action:**
1. [Specific step — usually INSERT new language]
2. [Add REVIEW/EDGE CASE comment]
**Example:** [Concrete example text]
```

**Rules:**
- Each edge case is numbered (EC1, EC2, ...)
- Action steps are specific and actionable
- Edge case handling may INSERT new language (tracked addition + comment)
- Edge case handling NEVER modifies existing template text
- Always include a Word comment explaining the edge case
- Include at least one concrete example where possible

### Part 5: INVARIANT RULES

Explicit constraints on AI behavior, repeated in every skill.

```markdown
## Part 5: Invariant Rules

1. **Never rewrite template language.** Only replace placeholders and delete sections.
2. **Never paraphrase.** Keep applied sections verbatim; delete inapplicable ones entirely.
3. **Preserve surrounding text.** Placeholder replacement changes only the placeholder.
4. **When in doubt, flag it.** Add a [REVIEW] comment rather than rewriting.
5. **Edge cases are additive only.** May INSERT; never MODIFY existing text.
6. **Tracked changes for everything.** Attorney must see every AI decision.
7. **Cross-reference consistency.** Values must match across all documents.
```

### FORMATTING SPECIFICATIONS (appendix)

```markdown
## Formatting Specifications
- **Paper:** US Letter, ~1" margins
- **Font:** Times New Roman, 12pt
- **Dollar amounts:** Spelled out + ($X,XXX.XX)
- **Percentages:** Spelled out + (X.XX%)
- **Numbers:** Spelled out + (N)
- **Defined terms:** Quoted with parenthetical on first use
- **Signature names:** ALL CAPS
- **Entity types:** Lowercase
```

---

## Template Marker Reference

The following markers appear in maximum Word templates:

| Marker | Purpose | Example |
|--------|---------|---------|
| `[PLACEHOLDER NAME]` | Bracketed placeholder — replace with CAS value | `[BORROWER NAME]`, `[$LOAN AMOUNT]` |
| `[$PLACEHOLDER]` | Dollar amount placeholder ($ prefix) | `[$LOAN AMOUNT]`, `[$HOLDBACK AMOUNT]` |
| `[PLACEHOLDER WORDS]` | Spelled-out version of a value | `[$LOAN AMOUNT WORDS]`, `[TERM WORDS]` |
| `[a/an]` | Grammatical article placeholder | Based on following word |
| `______________________` | Manual fill blank | Leave as-is or fill if known |
| `[IF: LABEL]` | Start of conditional block | `[IF: NEW LOAN]`, `[IF: HOLDBACK]` |
| `[END IF: LABEL]` | End of conditional block | `[END IF: NEW LOAN]` |
| `[FOR EACH: COLLECTION]` | Start of repeating block | `[FOR EACH: FOLIOS]` |
| `[END FOR EACH: COLLECTION]` | End of repeating block | `[END FOR EACH: FOLIOS]` |

### Comment Conventions (in Word comments)

| Prefix | Meaning | Example |
|--------|---------|---------|
| `REVIEW:` | Judgment call needed | "REVIEW: Payment-only guaranty — verify scope" |
| `POLICY EXCEPTION:` | CAS-approved deviation | "POLICY EXCEPTION: 30-year amortization" |
| `CONFIRM:` | Missing/ambiguous data | "CONFIRM: Closing date not in CAS" |
| `CROSS-REF:` | Consistency check | "CROSS-REF: Rate must match Note §2" |
| `EDGE CASE:` | Non-standard structure | "EDGE CASE: Multiple borrowers" |
| `EXTERNAL INPUT REQUIRED:` | Attorney must provide | "EXTERNAL INPUT REQUIRED: Signing chain" |

---

## Placeholder Naming Convention

Placeholders use descriptive UPPER CASE names in brackets:

```
[DESCRIPTIVE NAME]     — general fields
[$DOLLAR AMOUNT]       — dollar amounts ($ prefix)
[NAME WORDS]           — spelled-out version (WORDS suffix)
[NAME CAPS]            — ALL CAPS version (CAPS suffix)
[a/an]                 — grammatical articles
```

**Examples:**
- `[BORROWER NAME]` — party name
- `[$LOAN AMOUNT]` — dollar amount
- `[TERM WORDS]` — spelled-out number: "five (5)"
- `[BORROWER NAME CAPS]` — ALL CAPS: "ABC PROPERTIES, LLC"
- `[COMMITMENT FEE %]` — percentage

**Rules:**
- Names are self-explanatory without reference to Jinja schema
- Dollar amounts always start with `$`
- Spelled-out versions always end with `WORDS`
- ALL CAPS versions always end with `CAPS`
- For items in repeating blocks, use short prefixes: `[PG NAME]`, `[EG STATE]`, `[FOLIO NUMBER]`

---

## Edge Case Handling Philosophy

Edge cases are cataloged in Part 4 of each skill. The guiding principles:

1. **Identify the gap.** State what the template provides vs. what the deal requires. Example: "Template handles single borrower; CAS describes three co-borrowers."

2. **Prescribe specific actions.** Unlike the old narrative approach, edge case handling prescribes exact steps: what to insert, where, and what comment to add.

3. **Include concrete examples.** Use real examples (Graham Companies, etc.) to show exactly how the edge case should be drafted.

4. **Flag for review.** Always add a Word comment. The threshold: if a competent associate would need to ask a partner, the AI should flag it.

5. **Additive only.** Edge case handling may INSERT new language (tracked addition + comment). It NEVER modifies existing template text.

---

## Cross-Document Consistency Rules

These rules apply across all template skills and are enforced during generation:

1. **Defined Terms.** A term defined in one document must be used consistently (same capitalization, same definition) in all other documents in the set. The Commitment Letter is the "master" — other documents should reference its definitions.

2. **Party Names.** Borrower, Guarantor, and Lender names must be identical across all documents. Entity descriptions (state, entity type) must match. The CAS Field Mapping in each template should reference the same source fields.

3. **Deal Parameters.** Loan amount, interest rate, term, maturity date, DSCR covenant, prepayment penalty, and escrow requirements must be consistent across Commitment Letter, Promissory Note, and Mortgage. Any discrepancy is an error.

4. **Dates.** Closing date, maturity date, and computed dates (payment date, interest-only end date, rate adjustment dates) must be consistent. Show computations explicitly.

5. **Collateral Description.** Property legal description, county, and folio numbers must be identical in the Mortgage, Assignment of Leases and Rents, and any document that references the property.

6. **Signature Blocks.** Entity descriptions and signatory information must be identical across all documents a party signs. A change to any signature block must propagate to all documents.

---

## Multi-Entity / Multi-Property Handling

For deals with multiple borrowers, co-borrowers, or properties (like the Graham Companies deal with three borrowing entities, a co-borrower, and four property complexes):

### Borrower Identification
- List all borrowing entities with proper legal names and entity descriptions
- Identify the co-borrower separately if applicable
- Describe the ownership chain (parent → intermediate → borrowing entities)
- Use "Borrower" as a defined term encompassing all borrowing entities collectively unless the document requires individual references

### Property Description
- Each property gets its own legal description, folio number, and address
- The Mortgage and Assignment of Leases and Rents must cover all properties
- DSCR and LTV covenants may apply to individual properties or the portfolio collectively — the CAS will specify

### Document Multiplication
- Some documents are generated once per borrower (Officer Certificate)
- Some documents are generated once per guarantor (Guaranty Agreement)
- The Commitment Letter, Promissory Note, Mortgage, and Assignment are generated once covering all borrowers/properties
- The Rules spreadsheet column "generated_per" specifies multiplication

---

## File Naming Convention

```
ocean_bank_[document_name]_skill.md
```

**Examples:**
- `ocean_bank_commitment_letter_skill.md`
- `ocean_bank_promissory_note_skill.md`
- `ocean_bank_mortgage_skill.md`
- `ocean_bank_entity_guaranty_skill.md`
- `ocean_bank_cas_extraction_guide.md` (shared)
- `ocean_bank_document_selection_rules.md` (shared)

---

## Validation Checklist

Before finalizing any annotated template skill, verify:

- [ ] Every placeholder in the maximum template has an entry in the Placeholder Operations Registry (Part 2)
- [ ] Every `[IF:]`/`[END IF:]` marker pair has an entry in the Conditional Section Map (Part 3)
- [ ] Every `[FOR EACH:]` loop has handling instructions
- [ ] All CAS fields needed for this document appear in Part 1 (CAS Field Mapping)
- [ ] Edge cases identified from real deals are cataloged in Part 4
- [ ] Invariant Rules are present in Part 5
- [ ] Cross-references to other documents are specific (section + document name)
- [ ] Formatting specifications match the template's formatting
- [ ] No operation in the skill rewrites, paraphrases, or modifies template language
- [ ] Every edge case action includes a Word comment
- [ ] The maximum template opens correctly in Word with all formatting intact
