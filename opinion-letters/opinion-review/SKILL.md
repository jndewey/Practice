---
name: opinion-letter-reviewer
description: >
  Review and analyze third-party legal opinion letters from the perspective of
  lender's counsel (the opinion recipient). Use this skill whenever the user asks
  to review, analyze, check, vet, or evaluate a legal opinion letter, closing
  opinion, or borrower's counsel opinion received in connection with a loan
  transaction. Also trigger when the user mentions reviewing opinion letters,
  checking closing conditions, preparing opinion comments, redlining an opinion,
  or evaluating whether an opinion is acceptable for closing. This skill applies
  customary opinion practice standards from the TriBar Opinion Committee, ABA
  Statement of Opinion Practices, Florida Bar guidance, and Practical Law
  resources to systematically identify gaps, problematic assumptions, missing
  opinions, gutting qualifications, and negotiation points. Even partial requests
  like "look at this opinion" or "is this opinion acceptable" or "review the
  borrower's counsel opinion" should trigger this skill.
---

# Opinion Letter Reviewer — Lender's Counsel Perspective

## Overview

This skill reviews third-party legal opinion letters delivered (or to be
delivered) by borrower's counsel as a condition precedent to closing a loan
transaction. The review is conducted from the perspective of lender's counsel,
whose duties include:

- Carefully checking the opinions given, assumptions taken, and qualifications
  made in the borrower's counsel opinion
- Advising the lender whether the opinion is acceptable for closing
- Identifying missing opinions, problematic provisions, and negotiation points
- Ensuring the opinion is consistent with customary practice and the
  expectations set forth in the loan agreement's conditions precedent

**Malpractice risk**: Lender's counsel may be subject to malpractice liability
if they negligently advise the lender to accept a deficient closing opinion.
This skill helps mitigate that risk through systematic review.

## Before You Begin

**Always read the following reference files before reviewing an opinion:**

1. `references/review-checklist.md` — Section-by-section review checklist
   covering every component of a standard opinion letter (READ THIS FIRST)
2. `references/common-issues.md` — Red flags, problematic provisions, and
   negotiation strategies drawn from TriBar, ABA, and Practical Law guidance
3. `references/florida-lender-guide.md` — Florida-specific considerations for
   lender's counsel reviewing opinions on Florida transactions

Read all three references. Then analyze the uploaded opinion letter against
the checklist, flagging issues by severity.

## Expected User Inputs

The user will typically provide some or all of:

- **Opinion letter**: The draft or final opinion from borrower's counsel (PDF,
  DOCX, or text) — this is the primary document under review
- **Loan agreement / credit agreement**: To cross-check conditions precedent
  and opinion requirements
- **Transaction documents**: To verify the opinion covers all required documents
- **Form of opinion**: If the lender's form was provided to borrower's counsel,
  to compare against what was delivered
- **Deal context**: Transaction type (bilateral/syndicated, secured/unsecured,
  term/revolving/construction), entity types, governing law, collateral package,
  whether local counsel opinions are also expected

If the opinion letter is not uploaded, ask the user to provide it before
proceeding.

## Review Workflow

### Step 1: Identify Transaction Parameters

Before diving into the opinion text, establish the transaction context:

- **Transaction type**: Bilateral or syndicated; secured or unsecured; term
  loan, revolving credit, construction loan, floor plan, etc.
- **Loan parties**: Borrower(s), guarantor(s), pledgor(s) — entity types
  (corporation, LLC, LP, trust) and jurisdictions of organization
- **Governing law**: Which state's law governs the transaction documents
- **Collateral**: Real property, personal property, pledged equity, deposit
  accounts, etc.
- **Opinion giver**: Firm name, jurisdiction of practice, relationship to
  borrower (outside counsel, special counsel, etc.)
- **Addressees**: Lender(s), agent, any other addressees
- **Conditions precedent**: If the loan agreement is available, extract the
  exact opinion requirements from the CP section

### Step 2: Structural Completeness Check

Verify the opinion contains all required sections:

- [ ] Introductory paragraph / preamble (identifies parties, transaction, role)
- [ ] Definitions (or incorporation by reference)
- [ ] Documents reviewed (Transaction Documents list)
- [ ] Assumptions
- [ ] Opinions
- [ ] Qualifications / Exceptions
- [ ] Applicable Laws / Covered Law definition
- [ ] Reliance and disclosure provisions
- [ ] Date and signature

Flag any missing section as **CRITICAL**.

### Step 3: Cross-Check Against Conditions Precedent

If the loan agreement is available, compare the opinion requirements in the
CP section against what was actually delivered. Common gaps:

- Opinion required for guarantor(s) but not covered
- Local counsel opinion required but not delivered
- Specific opinions required (e.g., UCC perfection, no litigation) but omitted
- Opinion required to cover all "Loan Documents" but opinion only covers a
  subset (narrower "Opinion Documents" definition)

### Step 4: Review Each Opinion Section

Apply the detailed checklist from `references/review-checklist.md` to evaluate
each section. For each issue found, classify it as:

- 🔴 **CRITICAL** — Opinion is deficient; must be corrected before closing.
  Examples: missing enforceability opinion, assumption that guts a core opinion,
  opinion limited to wrong jurisdiction's laws.
- 🟡 **NEGOTIATE** — Departure from customary practice or lender expectations
  that should be pushed back on. Examples: overly broad Applicable Laws
  exclusions, unnecessary assumptions, narrow reliance provisions.
- 🟢 **ACCEPTABLE** — Consistent with customary practice. May note as
  informational if the provision has implications the lender should understand.
- ℹ️ **NOTE** — Informational item for lender's counsel's awareness. Examples:
  opinion speaks only as of its date, no update obligation (both customary).

### Step 5: Analyze Assumptions for Appropriateness

Assumptions deserve special scrutiny. For each assumption, ask:

1. **Is it customary?** Implicit/unstated assumptions (genuineness of
   signatures, authenticity of originals, conformity of copies, legal capacity)
   are always acceptable whether stated or not.
2. **Is it reasonable?** The opinion giver cannot assume facts they know to be
   false. But assumptions about matters not readily verifiable are generally
   acceptable.
3. **Is it relevant?** Assumptions should relate to this transaction and the
   opinions being given. Boilerplate assumptions irrelevant to the deal should
   be flagged — they shift analytical burden to the recipient.
4. **Does it gut an opinion?** An assumption that undermines or renders
   meaningless an opinion being given is never acceptable. Example: opining
   on due authorization while assuming all corporate formalities were observed.
5. **Is it transaction-specific?** Non-standard assumptions must be expressly
   stated. If the opinion giver is relying on local counsel, that should be
   disclosed.

### Step 6: Analyze Qualifications for Scope

For each qualification/exception:

1. **Is it customary?** Bankruptcy exception, equitable principles, and
   remedies qualification are standard and expected.
2. **Does it effectively nullify an opinion?** A qualification so broad it
   renders the related opinion meaningless should be flagged as CRITICAL.
3. **Are the sub-qualifications tailored?** Specific enforceability
   exceptions (e.g., for waivers, indemnities, choice of law, jury trial
   waiver) should relate to provisions actually in the transaction documents.
4. **Is the remedies qualification adequate?** It should preserve the lender's
   core rights — repayment, acceleration, foreclosure, realization on
   collateral — despite unenforceability of specific provisions.

### Step 7: Evaluate Reliance and Disclosure Provisions

Critical for syndicated transactions:

- Does the reliance provision cover the administrative agent AND each lender?
- Does it permit reliance by assignees? Under what conditions?
- Is the Wachovia limitation (or equivalent) included? Is it acceptable?
- Does it permit disclosure to regulators and prospective assignees?
- Are there any unusual restrictions on reliance or disclosure?

### Step 8: Identify Missing Opinions

Based on the transaction type, flag any opinions that should have been
included but were not. See `references/review-checklist.md` § "Expected
Opinions by Transaction Type" for the full matrix.

### Step 9: Generate Review Memorandum

Produce a structured review memorandum as a .docx file with:

1. **Executive Summary**: Overall assessment (Acceptable / Acceptable with
   Comments / Not Acceptable) and key issues count by severity
2. **Transaction Overview**: Parties, transaction type, governing law
3. **Findings Table**: Each issue with section reference, severity rating,
   description, and recommended action or comment language
4. **Missing Opinions**: List of opinions expected but not delivered
5. **Recommended Comments**: Draft redline comments or response language
   for each CRITICAL and NEGOTIATE item
6. **Closing Recommendation**: Whether lender's counsel can advise the
   lender to fund based on the opinion as delivered

Mark all items requiring attorney judgment with **[ATTORNEY REVIEW]**.

### Step 10: Output

- Generate the review memorandum as a .docx file
- If the user requests, generate a redline-style comment list that can be
  sent to borrower's counsel
- Provide a brief conversational summary of the top issues

## Key Principles for Lender's Counsel

1. **Golden Rule**: Do not request opinions you would not give if the roles
   were reversed (ABA Guidelines). Push back only on genuine deficiencies,
   not customary practice.
2. **Customary practice controls**: The opinion is a representation that it
   meets customary practice. Lender's counsel may assume borrower's counsel
   followed customary practice (TriBar §1.4).
3. **Not an insurance policy**: The opinion is not a guarantee of the
   transaction's success or that a court will reach a particular result.
4. **Lender's counsel's duty**: To explain the opinion to the lender client,
   identify what it covers and what it does not, and advise whether it is
   adequate for the transaction.
5. **Malpractice exposure**: Lender's counsel should carefully check the
   opinions given, and the assumptions and qualifications made. Negligent
   advice to accept a deficient opinion creates liability.
6. **Timing**: Agree on opinion language early in the transaction, not at
   closing when pressure to fund is highest.
7. **No implied opinions**: Only the opinions expressly stated are given.
   Do not assume the opinion covers matters not expressly addressed.
8. **Speaks as of its date**: No update obligation exists. If there is a
   delayed closing, consider whether a bring-down or new opinion is needed.

## Authority References

When citing authority for a position, reference these sources:

- TriBar Opinion Committee, Third-Party "Closing" Opinions, 53 Bus. Law.
  591 (1998)
- ABA Statement of Opinion Practices, 74 Bus. Law. 807 (2019)
- ABA Guidelines for the Preparation of Closing Opinions, 57 Bus. Law.
  875 (2002)
- ABA Legal Opinion Principles, 53 Bus. Law. 831 (1998)
- TriBar Opinion Committee, The Remedies Opinion, 59 Bus. Law. 1483 (2004)
- TriBar Opinion Committee, UCC Security Interest Opinions - Revised
  Article 9, 58 Bus. Law. 1450 (2003)
- TriBar Opinion Committee, Third-Party Closing Opinions: LLCs (Revised
  2021), 77 Bus. Law. 201 (2022)
- TriBar Opinion Committee, Third-Party Closing Opinions: Limited
  Partnerships, 73 Bus. Law. 1107 (2018)
- Laws Commonly Excluded from Coverage of Third-Party Legal Opinions in
  U.S. Commercial Loan Transactions, 76 Bus. Law. 889 (2021)
- Restatement (Third) of the Law Governing Lawyers (2000) §§51, 52, 95
- Restatement (Second) of Torts (1976) §§299A, 552
- ABA Model Rules of Professional Conduct, Rules 1.2, 1.6, 2.3, 4.1
- Florida Bar, Report on Third-Party Legal Opinion Customary Practice in
  Florida (the "Florida Report")
- Dean Foods Co. v. Pappathanasi, 2004 WL 3019442 (Mass. Super. 2004)
- Prudential Ins. Co. v. Dewey Ballantine, 590 N.Y.S.2d 831 (1992)
