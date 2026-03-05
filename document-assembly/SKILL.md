---
name: ocean-bank-deal-docs
description: >
  Generate Ocean Bank commercial real estate loan documents from a Credit Approval Summary (CAS).
  Use this skill whenever the user asks to generate, draft, or produce loan documents, commitment letters,
  promissory notes, mortgages, or any Ocean Bank closing documents from a CAS. Also trigger when the user
  references a CAS file, asks to "run" a deal, or mentions Ocean Bank document automation. This skill
  edits Word templates via tracked changes — it does NOT generate documents from scratch.
---

# Ocean Bank Deal Document Generator

## Overview

This skill produces attorney-ready loan document drafts by editing Word templates with tracked changes.
The AI reads a Credit Approval Summary (CAS), consults annotated template skills for decision guidance,
and surgically edits a maximum-version Word template — deleting inapplicable sections, inserting
deal-specific values, and flagging judgment calls as Word comments.

The output looks exactly like an associate's redline: red strikethrough for deletions, blue text for
insertions, margin comments for review items. The attorney accepts/rejects changes just like any
tracked-changes review.

## INVARIANT RULES

**These rules are absolute constraints. They override all other guidance.**

1. **Never rewrite template language.** The template text IS the Ocean Bank form. Only replace placeholders and delete conditional sections.
2. **Never paraphrase.** If a section applies, keep it verbatim. If it doesn't, delete it entirely.
3. **Preserve surrounding text.** When replacing a placeholder, the words before and after remain untouched.
4. **When in doubt, flag it.** Add a `[REVIEW]` Word comment rather than rewriting. A comment costs 5 seconds; a wrong provision costs hours.
5. **Edge cases are additive only.** Edge case handling may INSERT new language (tracked change + comment) but never modifies existing template text.
6. **Tracked changes for everything.** The attorney must see every decision the AI made.
7. **Three operations only:**
   - **Replace** `[PLACEHOLDER]` with extracted value (tracked del + ins)
   - **Delete** inapplicable `[IF:]` blocks (tracked del)
   - **Flag** edge cases with Word comments

## Architecture

```
CAS (PDF) ──► AI reads & extracts deal parameters
                    │
                    ▼
Annotated Template Skill (.md) ──► AI follows prescriptive operations:
                                    - Placeholder Operations Registry
                                    - Conditional Section Map
                                    - Edge Case Catalog
                    │
                    ▼
Maximum Word Template (.docx) ──► AI performs surgical edits:
                                    - Replace [PLACEHOLDER] → value (del + ins)
                                    - Delete inapplicable [IF:] blocks (del)
                                    - Flag edge cases (Word comments)
                    │
                    ▼
Output: Edited .docx with tracked changes + comments
```

### Three artifacts per document type:

1. **Maximum Word Template** — The Ocean Bank form with ALL conditional sections present.
   Uses bracketed placeholders (`[BORROWER NAME]`, `[$LOAN AMOUNT]`) and conditional
   markers (`[IF: NEW LOAN]`...`[END IF: NEW LOAN]`). Located in `new_templates/`.

2. **Annotated Template Skill** — Markdown reference with five parts:
   - **Part 1: CAS Field Mapping** — maps CAS fields to placeholders
   - **Part 2: Placeholder Operations Registry** — every placeholder and exactly how to fill it
   - **Part 3: Conditional Section Map** — every section that might be deleted and the exact condition
   - **Part 4: Edge Case Catalog** — situations the mechanical operations can't handle
   - **Part 5: Invariant Rules** — absolute constraints on AI behavior
   Located in `skills/`.

3. **CAS** — The deal-specific PDF input from the user.

4. **CAS Extraction Guide** — Shared reference for how to extract deal parameters from any CAS.
   Located in `skills/cas_extraction_guide.md`.

## File Structure

```
docauto/
├── SKILL.md                          ← this file (master skill)
├── CAS.pdf                           ← sample CAS input
├── jinja_templates/                  ← 24 original Jinja templates (reference only)
│   └── Ocean Bank - Commitment Letter.docx
├── new_templates/                    ← clean maximum templates
│   └── Ocean Bank - Commitment Letter.docx
├── skills/
│   ├── commitment_letter_skill.md    ← annotated template skill
│   ├── cas_extraction_guide.md       ← shared CAS extraction reference
│   └── annotation_format_spec.md     ← format spec for skills
├── scripts/
│   ├── jinja_to_max_template.py      ← convert Jinja → maximum template
│   ├── unpack.py                     ← unpack .docx to XML
│   ├── pack.py                       ← repack XML to .docx
│   ├── comment.py                    ← add Word comments
│   └── validate.py                   ← validate .docx structure
└── output/                           ← generated documents go here
```

## Workflow

### Phase 1: Extract Deal Parameters from CAS

1. Read the CAS PDF using `pdftotext -layout` or python PDF extraction
2. Read `skills/cas_extraction_guide.md` for field mapping and extraction rules
3. Extract all deal parameters into a structured JSON/dict format
4. Identify which document types are needed (consult Document Selection Rules in cas_extraction_guide.md)
5. Flag any parameters that are ambiguous or missing — these become `[REVIEW]` items

**Output of Phase 1:** A deal parameters object. Print a summary for the user to confirm:

```
Deal: [Borrower Name] — $[Amount] [Purpose]
Loan Type: [New/Existing] | Rate: [Structure] | Term: [X] years
Guarantor: [Name] ([Type])
Documents to generate: [list]
Items needing clarification: [list]
```

### Phase 2: Generate Each Document

For each document, follow this sub-workflow:

#### Step 2a: Read the Annotated Template Skill

Read the skill from `skills/`. It contains five parts:
- **Part 1: CAS Field Mapping** — which CAS fields map to which placeholders
- **Part 2: Placeholder Operations Registry** — every placeholder and how to fill it
- **Part 3: Conditional Section Map** — every section that might be deleted and the condition
- **Part 4: Edge Case Catalog** — situations needing human judgment
- **Part 5: Invariant Rules** — absolute constraints

#### Step 2b: Copy and Unpack the Template

```bash
cp new_templates/commitment_letter.docx working/commitment_letter_draft.docx
python scripts/unpack.py working/commitment_letter_draft.docx working/unpacked/
```

#### Step 2c: Execute Placeholder Replacements

Walk through the Placeholder Operations Registry (Part 2). For each placeholder:

1. **Find** `[PLACEHOLDER]` in the document XML
2. **Replace** with tracked change: `<w:del>` the placeholder text + `<w:ins>` the value
3. **Preserve formatting:** Copy `<w:rPr>` from the original run
4. **Nothing else changes** — surrounding text is untouched

#### Step 2d: Execute Conditional Deletions

Walk through the Conditional Section Map (Part 3). For each conditional:

1. **Evaluate** the condition against extracted deal parameters
2. **If FALSE:** Delete the entire `[IF:]`...`[END IF:]` block (markers + content) as tracked deletion
3. **If TRUE:** Delete only the `[IF:]` and `[END IF:]` markers (keep content between them)
4. **FOR EACH loops:** Expand by duplicating content for each item, removing markers

#### Step 2e: Handle Edge Cases

Check the Edge Case Catalog (Part 4). For each applicable edge case:

1. **INSERT** new language via tracked insertion (`<w:ins>`)
2. **ADD** a Word comment explaining the edge case
3. **Never modify** existing template text — only add

#### Step 2f: Add Review Comments

For any ambiguous or missing CAS data:
1. Add `[REVIEW]`, `[CONFIRM]`, or `[EDGE CASE]` Word comments
2. Use `scripts/comment.py` for comment creation

#### Step 2g: Repack and Validate

```bash
python scripts/pack.py working/unpacked/ output/commitment_letter_draft.docx \
  --original working/commitment_letter_draft.docx
python scripts/validate.py output/commitment_letter_draft.docx
```

**CRITICAL: Work section by section, not all at once.** After each section:
- Verify XML structure is valid
- Confirm tracked changes render correctly
- Check that no template language was rewritten

### Phase 3: Cross-Reference Validation

After generating all documents, verify consistency:

1. **Defined terms** — "Borrower", "Guarantor", "Property", "Loan" must be identical across all docs
2. **Deal parameters** — loan amount, rate, term, amortization must match everywhere
3. **Party names** — exact legal names and entity descriptions identical in every document
4. **Collateral descriptions** — property descriptions, folios match in Mortgage, Assignment, etc.
5. **Signature blocks** — identical for each party across all documents they sign

Report any inconsistencies to the user.

## XML Editing Reference

### Tracked Change: Delete Text

Replace the target `<w:r>` with a `<w:del>` wrapping:

```xml
<w:del w:id="[UNIQUE_ID]" w:author="Deal Agent" w:date="[ISO_DATE]">
  <w:r>
    <w:rPr>[COPY ORIGINAL FORMATTING]</w:rPr>
    <w:delText xml:space="preserve">[ORIGINAL TEXT]</w:delText>
  </w:r>
</w:del>
```

### Tracked Change: Insert Text

```xml
<w:ins w:id="[UNIQUE_ID]" w:author="Deal Agent" w:date="[ISO_DATE]">
  <w:r>
    <w:rPr>[MATCH SURROUNDING FORMATTING]</w:rPr>
    <w:t xml:space="preserve">[NEW TEXT]</w:t>
  </w:r>
</w:ins>
```

### Tracked Change: Replace Text (Delete + Insert)

```xml
<w:del w:id="[ID1]" w:author="Deal Agent" w:date="[ISO_DATE]">
  <w:r>
    <w:rPr>[ORIGINAL FORMATTING]</w:rPr>
    <w:delText>[OLD TEXT]</w:delText>
  </w:r>
</w:del>
<w:ins w:id="[ID2]" w:author="Deal Agent" w:date="[ISO_DATE]">
  <w:r>
    <w:rPr>[ORIGINAL FORMATTING]</w:rPr>
    <w:t>[NEW TEXT]</w:t>
  </w:r>
</w:ins>
```

### Delete Entire Paragraph

When removing a complete paragraph (e.g., an inapplicable conditional section), mark BOTH
the content AND the paragraph mark as deleted:

```xml
<w:p>
  <w:pPr>
    <w:rPr>
      <w:del w:id="[ID1]" w:author="Deal Agent" w:date="[ISO_DATE]"/>
    </w:rPr>
  </w:pPr>
  <w:del w:id="[ID2]" w:author="Deal Agent" w:date="[ISO_DATE]">
    <w:r>
      <w:rPr>[FORMATTING]</w:rPr>
      <w:delText>[ENTIRE PARAGRAPH TEXT]</w:delText>
    </w:r>
  </w:del>
</w:p>
```

### Add Word Comments

Use the comment script, then add markers to document.xml:

```bash
python scripts/comment.py working/unpacked/ [COMMENT_ID] "[COMMENT TEXT]"
```

Then in document.xml, wrap the relevant text:

```xml
<w:commentRangeStart w:id="[COMMENT_ID]"/>
<w:r><w:t>text being commented on</w:t></w:r>
<w:commentRangeEnd w:id="[COMMENT_ID]"/>
<w:r>
  <w:rPr><w:rStyle w:val="CommentReference"/></w:rPr>
  <w:commentReference w:id="[COMMENT_ID]"/>
</w:r>
```

### ID Management

Every `<w:del>`, `<w:ins>`, `<w:commentRangeStart>`, etc. needs a unique `w:id`.
Start at a high number (e.g., 1000) and increment. Never reuse IDs.

### Formatting Preservation

**Always copy `<w:rPr>` from the original run** into your tracked change runs.
This preserves font, size, bold, italic, etc. If you don't, the tracked change
text will render in the document's default style, not the section's style.

### Smart Quotes

Use XML entities for professional typography:

| Entity | Character |
|--------|-----------|
| `&#x2018;` | ' left single quote |
| `&#x2019;` | ' right single / apostrophe |
| `&#x201C;` | " left double quote |
| `&#x201D;` | " right double quote |

## Template Format

### Placeholders

Templates use bracketed placeholder patterns:

| Pattern | Meaning | Action |
|---------|---------|--------|
| `[BORROWER NAME]` | CAS-sourced field | Replace with extracted value via tracked change |
| `[TERM WORDS]` | Spelled-out number | Replace with "five (5)" format |
| `[$LOAN AMOUNT]` | Dollar amount | Replace with "$X,XXX,XXX.XX" |
| `[$LOAN AMOUNT WORDS]` | Spelled dollar amount | Replace with "Five Million and No/100 Dollars" |
| `[a/an]` | Grammatical article | Replace with "a" or "an" based on following word |
| `______________________` | Blank for manual fill | Leave as-is OR fill if value known |
| `[CLOSING DATE]` | Date placeholder | Replace if known, leave blank if not |

When replacing a placeholder, use a tracked deletion + insertion so the attorney
can see what was filled in.

### Conditional Markers

Templates use inline markers for conditional sections:

| Marker | Meaning |
|--------|---------|
| `[IF: LABEL]` | Start of conditional block |
| `[END IF: LABEL]` | End of conditional block |
| `[FOR EACH: COLLECTION]` | Start of repeating block |
| `[END FOR EACH: COLLECTION]` | End of repeating block |

**When condition is TRUE:** Delete only the markers (keep content between them).
**When condition is FALSE:** Delete the entire block (markers + all content).
**FOR EACH:** Duplicate the content for each item, removing the markers.

## Comment Conventions

Use Word comments (not inline text) for all review items. Comment categories:

| Prefix | Meaning | Example |
|--------|---------|---------|
| `REVIEW:` | Judgment call needed | "REVIEW: Payment-only guaranty — verify scope of Borrowers' Liabilities" |
| `POLICY EXCEPTION:` | CAS-approved deviation | "POLICY EXCEPTION: 30-year amortization exceeds 25-year max per CAS" |
| `CONFIRM:` | Missing/ambiguous data | "CONFIRM: UCC requirement — CAS silent, assumed required for commercial" |
| `CROSS-REF:` | Consistency check | "CROSS-REF: Rate must match Promissory Note Section 2" |
| `EDGE CASE:` | Non-standard structure | "EDGE CASE: Multiple borrowers — template handles single borrower only" |

## Decision Rules for Common Scenarios

### What to DELETE from the maximum template:

- **Construction sections** — delete if `loan_purpose` ≠ "Construction"
  (Construction Covenants, Construction Conditions Precedent, Sources & Uses Schedule,
  Construction Phase repayment, Conversion to Permanent)
- **Extension options** — delete if no extension
- **Holdback provisions** — delete if no holdback
- **Interest-only period** — delete if P&I from start
- **Prepayment penalty** — delete penalty language if no penalty; keep "without premium or penalty"
- **Cross-default** — delete if no cross-default
- **Tenant reserve** — delete if no tenant reserve
- **Existing loan provisions** — delete if new loan (and vice versa)
- **Reserve accounts** — delete each type not required
- **Franchise agreement** — delete if not franchised
- **Star reports** — delete if not hotel
- **Bond requirement** — delete if not bonded construction
- **Inapplicable signature block patterns** — keep only the pattern matching the actual signing chain

### What to KEEP but MODIFY:

- **Rate section** — keep the matching rate structure, delete alternatives
- **Repayment section** — keep matching repayment structure, delete alternatives
- **Fee section** — keep "Commitment" or "Underwriting", delete the other
- **UCC line** — keep "does" or "does not", delete the other
- **Escrow section** — keep matching escrow type, delete alternatives
- **Guarantor section** — keep matching guarantor structure, delete others
- **Reporting section** — keep applicable reporting items, delete non-applicable

### What to ADD (not in template):

Edge cases identified in the annotated skill that have no template equivalent.
These are inserted as tracked additions with an `EDGE CASE:` comment. Common ones:

- Multiple borrower / co-borrower structure
- Payment-only or limited guaranty language
- Multi-tier prepayment penalty
- Non-standard rate repricing
- Portfolio collateral descriptions
- DSCR cure mechanisms beyond standard template options

## Error Handling

### XML Breaks

If an edit produces invalid XML:
1. Revert to the last known-good state
2. Identify what broke (usually unclosed tags or misplaced elements)
3. Fix and retry
4. Re-validate before proceeding

### Missing CAS Data

If a required field is not in the CAS:
1. Check if the annotated skill provides a default or derivation method
2. If derivable, compute it and add a `CONFIRM:` comment
3. If not derivable, leave the placeholder and add a `CONFIRM:` comment
4. Never guess — blanks with comments are better than wrong values

### Ambiguous CAS Data

If the CAS is ambiguous about a parameter:
1. State both interpretations in a `REVIEW:` comment
2. Draft the section using the more conservative interpretation
3. Show the alternative in the comment text

## Usage Examples

### Basic: Single document from CAS

```
User: Generate the commitment letter from this CAS [attaches PDF]

AI workflow:
1. Extract CAS → summarize deal parameters → confirm with user
2. Read commitment_letter_skill.md
3. Copy + unpack commitment_letter.docx template
4. Edit section by section with tracked changes
5. Add comments for review items
6. Repack + validate
7. Deliver output/commitment_letter_draft.docx
```

### Full deal: All documents from CAS

```
User: Run the full closing package for this deal [attaches CAS]

AI workflow:
1. Extract CAS → identify required documents → confirm with user
2. For each document:
   a. Read its annotated skill
   b. Copy + unpack its template
   c. Edit with tracked changes
   d. Repack + validate
3. Cross-reference validation across all documents
4. Deliver all documents + cross-reference report
```

### Targeted: Edit specific section

```
User: The guaranty section needs to be a payment-only guaranty, not full recourse

AI workflow:
1. Read the current document's guarantor section
2. Consult the skill's Guarantor edge case for payment-only guaranty
3. Make targeted tracked-change edits
4. Add REVIEW comment on the modification
5. Deliver updated document
```

## Important Reminders

- **Three operations only.** Replace placeholders, delete conditional blocks, flag edge cases. Nothing else.
- **Never rewrite template language.** The template text IS the Ocean Bank form. Don't paraphrase, rephrase,
  or adjust any provision. If it applies, keep it verbatim. If it doesn't, delete it entirely.
- **Never generate from scratch.** Always edit the template. The template's formatting, spacing, and style
  are what make it an Ocean Bank document.
- **Work incrementally.** Edit one section, verify, move to next. Don't try to edit the entire document
  in a single pass.
- **Preserve all formatting.** Copy `<w:rPr>` blocks. Match fonts, sizes, alignment.
- **Use tracked changes for everything.** The attorney must be able to see every decision the AI made.
- **Comments over inline flags.** Use Word comments, not red `[REVIEW]` text in the document body.
- **When in doubt, flag it.** A `REVIEW:` comment on a correct provision costs the attorney 5 seconds.
  A silently wrong provision costs hours. Never silently resolve ambiguity.
- **The annotated skill is prescriptive.** Follow the Placeholder Operations Registry and Conditional
  Section Map exactly. The skill prescribes specific surgical operations, not general guidance.
- **Edge cases are additive only.** Edge case handling inserts new language (tracked addition + comment).
  It never modifies existing template text.
- **Cross-references matter.** A rate mismatch between the Commitment Letter and Note is a
  deal-breaking error. Values must be identical across all documents.
