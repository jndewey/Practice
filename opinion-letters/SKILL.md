---
name: legal-opinion-generator
description: >
  Generate transaction-specific third-party legal opinion letters for commercial
  real estate finance and corporate transactions. Use this skill whenever the user
  asks to draft, create, prepare, or generate a legal opinion letter, closing opinion,
  third-party opinion, or borrower's counsel opinion. Also trigger when the user
  mentions opinion letters in the context of loan closings, real estate finance
  transactions, construction loans, or any commercial transaction requiring legal
  opinions. This skill uses the Holland & Knight LLP standard form of opinion letter
  as the starting point and adapts it based on the specific transaction documents,
  organizational documents, and good standing certificates provided by the user.
  Even partial requests like "draft the opinion for the Ocean Bank deal" or
  "prepare closing opinions" should trigger this skill.
---

# Legal Opinion Generator

## Overview

This skill generates transaction-specific third-party legal opinion letters based on
the Holland & Knight LLP standard form of Corporate & Finance Opinion Letter. The
generated opinions comply with Florida customary practice as articulated in the
Florida Bar's "Report on Third-Party Legal Opinion Customary Practice in Florida"
(the "Florida Report").

## Before You Begin

**Always read the following reference files before generating an opinion:**

1. `references/hk-form-opinion.md` — The complete H&K standard form opinion letter
   (READ THIS FIRST — it is the template from which all opinions are generated)
2. `references/florida-practice-guide.md` — Key guidance from the Florida Report,
   Form B, and Form D on Florida customary opinion practice
3. `references/appendix-a-guide.md` — Guidance on transaction-specific addenda
   (UCC, securities, M&A, amendments, cross-border, fund formation, choice of law)
4. `references/appendix-b-florida.md` — Florida-specific opinion provisions from
   H&K Appendix B (existence, usury, choice of law, taxes, qualification)

Read all four references. Then analyze the user's uploaded transaction documents
and organizational documents to generate the opinion.

## Expected User Inputs

The user will typically provide some or all of:

- **Transaction Documents**: Credit agreement, loan agreement, note, mortgage,
  assignment of leases and rents, security agreement, guaranty, environmental
  indemnity, UCC financing statements, subordination agreements, etc.
- **Organizational Documents**: Articles/certificate of incorporation or formation,
  bylaws, operating agreement, limited partnership agreement, resolutions,
  incumbency certificates, secretary's certificates
- **Good Standing Certificates**: Certificates of status/good standing from the
  state of organization and any states where foreign qualification opinions are needed
- **Deal context**: Who the client is, who the lender is, whether H&K represents
  borrower or lender, the nature of the transaction (term loan, construction loan,
  revolving credit, etc.)

If key information is missing, ask the user before generating.

## Generation Workflow

### Step 1: Analyze the Transaction

Read all uploaded documents and identify:
- The parties (borrower, lender, guarantors, administrative agent)
- Entity types and states of organization for each Relevant Party
- The transaction structure (loan type, security package, guaranty structure)
- All Transaction Documents to be listed in the opinion
- The governing law of each Transaction Document
- Whether there are UCC security interests requiring Article 9 opinions
- Whether there is real property collateral (mortgage, assignment of rents)
- Whether there are construction loan elements
- Whether guaranties are upstream, downstream, or cross-stream
- Any unusual features (cross-collateralization, future advances, etc.)

### Step 2: Select Applicable Opinion Components

Starting from the H&K form, determine which opinions apply:

**Always include (if H&K represents the borrower/guarantors):**
- Opinion 1: Entity existence and good standing
- Opinion 2: Power, authorization, execution and delivery
- Opinion 4: Enforceability (valid, binding, enforceable)
- Opinion 5(a): No violation of organizational documents
- Opinion 5(b): No violation of Applicable Laws
- Opinion 6: No governmental consents required

**Include if applicable:**
- Opinion 3: Foreign qualification (if collateral/operations in other states)
- Opinion 5(c): No breach of Applicable Contracts (if lender requires)
- Opinion 7: Investment Company Act (if requested)
- Opinion 8: Margin regulations (if requested)
- Florida usury opinion (see Appendix B — standard for Florida deals)
- Florida choice of law opinion (if docs governed by non-Florida law)
- Florida documentary stamp tax opinion (if mortgage being recorded)
- Real property lien opinions (mortgage, assignment of rents)
- UCC/fixture filing opinions (if personal property or fixtures secured)
- Lender qualification opinion (if lender is out-of-state)

### Step 3: Adapt Assumptions

Select assumptions from the H&K form based on what opinions are being given:
- Always include assumptions (i) through (iv) (signatures, authenticity, copies, facts)
- Include assumptions (v) through (xiii) for enforceability opinions
- Include assumption (xiv)-(xvi) only for parties where entity opinions are NOT given
- Include the LLC/LP dissolution assumption (xiii) if Relevant Parties include LLCs or LPs
- Include the shareholders agreement assumption (xvii) if NY corporations involved
- Include GOL §5-1401 assumption (xviii) if NY governing law

For Florida transactions specifically:
- Include the documentary stamp tax payment assumption from Appendix B
- Include any choice-of-law factual assumptions needed for the choice of law opinion

### Step 4: Define Applicable Laws

Customize the Applicable Laws definition based on:
- The state(s) whose law governs the Transaction Documents
- The state of organization of the Relevant Parties
- What opinions are being given (entity statute must be included)
- Any specific statutes being opined on (margin regs, Investment Company Act, etc.)

The standard exclusions from Applicable Laws should be preserved. Add back
specific statutes only where opinions require them (e.g., the entity statute for
opinions 1, 2, and 5(a); margin regulations for opinion 8).

### Step 5: Customize Qualifications

Always include:
- Qualification (a): Limitation to Applicable Laws
- Qualification (b): Bankruptcy/insolvency exception
- Qualification (c): Equitable principles limitation
- Qualification (d): Reliance on public official certificates for existence opinion
- Qualification (e): Remedies qualification (unenforceability of certain provisions
  won't invalidate documents as a whole)

Select from qualification (f) sub-provisions based on which provisions actually
appear in the Transaction Documents. Delete any that clearly don't apply.

**Florida-specific qualifications** (from Appendix B and the Florida Report):
- Include the Florida usury qualification with the 25% or 18% rate as applicable
- For choice of law, use the Sailboat Key / Morgan Walton analysis
- For doc stamp taxes, note consequences of non-payment on enforceability
- For the remedies qualification, Florida practice follows the approach in Form B:
  unenforceability of certain provisions won't preclude judicial enforcement of
  repayment, acceleration upon material default, or foreclosure

### Step 6: Prepare Schedules

Generate the following schedules:
- Schedule I.A: List of Transaction Documents (with full names, dates, parties)
- Schedule I.B: Certificates of public officials relied upon
- Schedule I.C: States of foreign qualification (with dates of certificates)
- Schedule I.D: Applicable Contracts (if no-breach opinion is given)
- Schedule I.F: Required governmental consents already obtained

### Step 7: Format and Output

Generate the opinion as a .docx file using the docx skill. The opinion should:
- Use H&K letterhead formatting
- Follow the exact structure of the H&K form
- Use proper legal document formatting (numbered paragraphs, lettered sub-items)
- Include all bracketed choices resolved based on the transaction
- Remove all footnotes and internal annotations from the form
- Replace all placeholder text with transaction-specific information

## Key Principles from Florida Customary Practice

These principles from the Florida Report should guide opinion drafting:

1. **No implied opinions**: Only express opinions are given; nothing implied beyond
   what is expressly stated.

2. **Customary professional diligence**: The "Applicable Laws" standard is based on
   what a Florida lawyer exercising customary professional diligence would reasonably
   recognize as applicable — it is not an exhaustive review of all possible laws.

3. **Knowledge standard**: "To our knowledge" means conscious awareness of lawyers
   in the "primary lawyer group" — the signing partner, lawyers actively preparing
   the opinion, and lawyers actively involved in the transaction. No independent
   investigation is implied.

4. **Golden Rule**: Do not include opinions that a qualified attorney would not
   reasonably be willing to give under similar circumstances.

5. **Presumption of regularity**: Opining counsel may assume underlying corporate
   proceedings are in order absent red flags. Full minute book review is not required.

6. **Entity existence vs. good standing**: Under Florida law, "existing" confirms
   formation and no dissolution. "Active status" confirms the entity has not been
   administratively dissolved. Florida does not issue traditional "good standing"
   certificates — the Department of State issues "certificates of status."

7. **Enforceability opinion**: Means the document is valid, binding, and enforceable
   "in accordance with its terms" — always subject to the bankruptcy exception and
   equitable principles limitation.

8. **Remedies qualification**: Florida practice permits the "golden nugget" approach —
   despite potential unenforceability of specific provisions, the core obligations
   (repayment, acceleration, foreclosure) remain enforceable.

9. **Usury**: Florida has both an 18% rate (for loans ≤$500,000) and a 25% rate
   (for loans >$500,000) as the maximum lawful rate. The opinion should specify
   which rate applies. See §687.02 and §687.071, Florida Statutes.

10. **Choice of law**: Florida courts apply the "normal and reasonable relationship"
    test from Continental Mortgage Investors v. Sailboat Key and Morgan Walton.
    Choice of law opinions in Florida are typically "reasoned" or "explained" opinions
    using "more likely than not" language.

11. **Documentary stamp tax and intangible tax**: These are critical for Florida
    real property transactions. Failure to pay renders the document unenforceable
    until paid (but does not affect lien validity or constructive notice).

12. **Local counsel role**: When acting as local Florida counsel in a multi-state
    deal, the opinion is limited to Florida law matters. Use assumptions for
    matters covered by primary counsel's opinion. See Form D and Appendix A,
    Addendum X for guidance.

## Output Format

Generate a Word document (.docx) containing the complete opinion letter. Use the
docx skill for formatting. The document should be professional, clean, and ready
for partner review — but flag any items requiring attorney judgment with
[ATTORNEY REVIEW: ...] brackets.

Items that always require attorney review:
- Whether specific remedies qualifications apply to this transaction
- Whether the fraudulent conveyance savings clause qualification is needed
- The appropriate usury rate (18% vs 25%)
- Whether the choice of law opinion is supportable given the transaction's contacts
- Tax opinion amounts and calculations
- Any novel or unusual transaction features

## Important Caveats

- This skill generates a DRAFT opinion for attorney review. It is never final.
- Flag areas of uncertainty rather than guessing.
- When in doubt about whether a qualification or assumption applies, include it
  and flag it for review rather than omitting it.
- The generated opinion must be reviewed by a Designated Reviewer per H&K policy.
- Never fabricate document names, dates, party names, or other factual details
  that are not evident from the uploaded documents.
