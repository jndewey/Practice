---
name: mezzanine-loan-cre
description: >
  Comprehensive knowledge base for mezzanine loans and equity pledge agreements in commercial real estate finance. Use this skill whenever the user mentions mezzanine loans, mezzanine financing, equity pledges, pledge and security agreements, intercreditor agreements between senior mortgage lenders and mezzanine lenders, UCC foreclosure of membership interests, Article 8 opt-in, capital stack structuring, LLC interest pledges, control agreements for mezzanine collateral, or any document drafting, review, or negotiation involving mezzanine loan transactions. Also trigger when discussing loan-to-own strategies, subordinate debt in CRE, CMBS mezzanine requirements, mezzanine loan secondary market sales, or mezzanine borrower entity structuring. This skill covers both conceptual knowledge and practical document drafting guidance.
---

# Mezzanine Loans & Equity Pledge Agreements in Commercial Real Estate Finance

This skill provides deep expertise on mezzanine loan transactions in commercial real estate, covering the full lifecycle from structuring and documentation through foreclosure and secondary market sales. It is organized into a core knowledge section (below) and detailed reference files for specific document forms and advanced topics.

## When to Read Reference Files

Before drafting or reviewing any specific document, read the relevant reference file:

- **Pledge and security agreement** drafting/review → Read `references/pledge-agreement.md`
- **Intercreditor agreement** negotiation or review → Read `references/intercreditor.md`
- **UCC collateral documents** (Article 8 opt-in, certificates, control agreements, proxies) → Read `references/ucc-collateral-docs.md`
- **Foreclosure and remedies** questions → Read `references/foreclosure-remedies.md`
- **Due diligence or closing checklist** tasks → Read `references/due-diligence-closing.md`

---

## Core Concepts

### What Is a Mezzanine Loan

A mezzanine loan is a form of subordinate debt in commercial real estate. Its defining characteristics are:

1. **Equity collateral.** Secured by a pledge of equity interests (typically LLC membership interests) in the entity that owns the mortgage borrower — not by a lien on real property.
2. **Structural subordination.** The mezzanine lender is not a creditor of the mortgage borrower, has no lien on the mortgaged property, and the mortgage lender has lien priority over property rents. Absent substantive consolidation in bankruptcy, the mortgage borrower is unaffected by a mezzanine borrower bankruptcy.
3. **Higher interest rate.** Compensates for the subordinate position and elevated risk.

Mezzanine financing allows property owners to borrow beyond the mortgage lender's LTV ceiling. Common uses include acquisition leverage, refinancing for major renovations, property conversions, and hotel re-branding.

### The Capital Stack

The financing package may consist of:
- Mortgage loan + single mezzanine loan
- Mortgage loan + senior mezzanine loan + junior (subordinate) mezzanine loan
- Mortgage loan + senior mezzanine loan + multiple subordinate mezzanine loans

### Why Mezzanine Instead of a Second Mortgage

Second mortgages fell out of favor because they create significant risks for the first mortgage lender: increased bankruptcy risk, the second lienor becoming a secured creditor of the mortgage borrower, potential challenges to first mortgage lien priority, and challenges to the first mortgage lender's rights to rents.

Mezzanine loans remedy these disadvantages by:
- Preserving the mortgage lender as the only member of its creditor class
- Avoiding lien priority challenges through structural subordination
- Leaving the mortgage borrower unaffected by mezzanine borrower bankruptcy

### LTV and the Equity Gap

Mortgage lenders typically cap LTV at 60-70%. The mezzanine loan bridges the gap, with mezzanine lenders permitting a combined (mortgage + mezzanine) LTV of 80-90% of appraised value. The mezzanine lender calculates its LTV using the combined principal balance of both loans as numerator and appraised property value as denominator.

### Entity Structure

The standard mezzanine structure requires two bankruptcy-remote SPEs:

```
Sponsor / Key Principal
        │
        ▼
┌─────────────────────────┐
│  MEZZANINE BORROWER     │  ← Pledges its membership interests
│  (SPE LLC, typically DE)│     in Mortgage Borrower to Mezz Lender
│  Sole member of         │
│  Mortgage Borrower      │
└─────────┬───────────────┘
          │ owns 100%
          ▼
┌─────────────────────────┐
│  MORTGAGE BORROWER      │  ← Grants mortgage lien on property
│  (SPE LLC)              │     to Mortgage Lender
│  Owns the real property │
└─────────────────────────┘
```

The mezzanine borrower is the sole member of the mortgage borrower, owning 100% of the issued and outstanding ownership interests.

---

## Mezzanine Loan Documents

The core document package includes:

1. **Pledge and Security Agreement** — Creates the lender's security interest in the equity collateral. Secured under the UCC, not real property law. See `references/pledge-agreement.md` for detailed drafting guidance.

2. **Promissory Note** — Evidences the debt and promises repayment.

3. **Mezzanine Loan Agreement** — Sets out terms, covenants, and agreements between loan parties.

4. **Nonrecourse Carveout Guaranty** ("Bad Boy Guaranty") — Personal guaranty for specific borrower misconduct.

5. **Environmental Indemnity Agreement** — Indemnification for environmental liabilities.

6. **Subordination of Property Management Agreement** — Since the management agreement is already assigned to the mortgage lender, it is subordinated (not assigned) to the mezzanine loan.

7. **Collateral Assignment of Interest Rate Hedge** — If the mezzanine loan has a floating rate.

8. **Secondary Market Cooperation Agreement** — May be separate or incorporated into the loan agreement.

9. **Intercreditor Agreement** — Governs the relationship between mortgage and mezzanine lenders. See `references/intercreditor.md`.

### Ancillary UCC Collateral Documents

- **Amendment to LLC Agreement (Opting into Article 8)** — Redesignates membership interests as "securities" under UCC Article 8.
- **Certificate of LLC Interests** — Physical certificate representing the pledged membership interests.
- **Control Agreement** — For uncertificated interests; mortgage borrower agrees to follow mezzanine lender's instructions.
- **Irrevocable Proxy Agreement** — Grants mezzanine lender voting rights over the pledged interests.
- **Acknowledgment, Consent, and Direction Letter** — Mortgage borrower acknowledges the pledge and registers it on company books.
- **UCC-1 Financing Statement** — Filed to perfect the security interest.

See `references/ucc-collateral-docs.md` for detailed drafting guidance on all of these.

---

## Mezzanine Pledge Mechanics

### Creation and Perfection of Security Interest

The pledge is created, perfected, and enforced under the UCC (not real property law). The classification of LLC interests affects perfection methods:

- **General intangibles** (default UCC classification): Can only be perfected by UCC-1 filing.
- **Investment property / securities** (after Article 8 opt-in): Can be perfected by filing, possession (certificated), or control.

**Perfection by control** takes priority over perfection by filing, even if control occurs after the filing date. This is why mezzanine lenders require the Article 8 opt-in — it enables protected purchaser status, which defeats competing claims perfected only by filing.

### Certificated vs. Uncertificated Interests

| Feature | Certificated | Uncertificated |
|---|---|---|
| How lender gets control | Delivery of original certificate indorsed in blank | Control agreement from mortgage borrower |
| Key document | Certificate of LLC Interests + stock power | Control Agreement |
| Protected purchaser status | Yes, via possession + Article 8 | Yes, via control agreement + Article 8 |

### The Confirmation Statement / Acknowledgment

The mortgage borrower must:
- Acknowledge and consent to the pledge
- Register the pledge on its books
- Confirm no liens or claims restrict the pledge
- Agree to follow lender's instructions after a default

---

## Drawbacks and Risks

### For Mezzanine Borrowers
- Faster, cheaper foreclosure by lender (30-90 days via UCC vs. years for mortgage foreclosure)
- Higher transaction costs from dual-lender structure
- Operating delays from multiple lender approvals
- Potential continuing guaranty liability post-foreclosure
- Risk of "loan-to-own" strategy by predatory mezzanine lenders

### For Mezzanine Lenders
- First loss position: monthly revenue shortfalls hit mezzanine debt service first
- Foreclosure shortfalls: if sale proceeds don't exceed mortgage debt, mezzanine is wiped out
- Lack of control: mortgage lender has superior rights over property decisions
- Collateral dilution from mortgage modifications, extensions, and future advances

### For Mortgage Lenders
- Mezzanine debt service drains property income and reduces DSCR
- Mezzanine guaranty enforcement can erode shared guarantor's value
- Operating delays from additional approval requirements
- Post-foreclosure, mezzanine lender controls mortgage borrower and could file bankruptcy
- Mezzanine loan transfer to objectionable successor

---

## Loan-to-Own Strategy

Some mezzanine lenders deliberately structure loans expecting default, anticipating they will gain direct ownership of the mortgage borrower (and indirect ownership of the property) at below-market cost. The total acquisition cost equals: outstanding mortgage debt + unpaid mezzanine debt + origination and foreclosure costs.

This strategy works best when the property is fundamentally sound but experiencing temporary difficulties, is in a market expected to improve, needs emergency repairs the sponsor cannot finance, or the sponsor has personal financial difficulties unrelated to the property.

---

## Secondary Market for Mezzanine Loans

Mezzanine loans are frequently sold on secondary markets. Key aspects:

**Assignment documents include:**
- Allonge (indorsement of promissory note to assignee)
- Assignment and assumption agreement
- Original promissory note
- Pledged collateral (certificates or control agreement)
- UCC-3 financing statement (assignment)
- Notice letters to borrower, mortgage lender, cash management bank, hedge provider

**Representations by seller** are typically minimal: sole ownership, no encumbrances, complete document delivery, no defaults, no waivers. The purchaser bears the due diligence burden.

**Borrower impact:** Borrowers generally have no consent rights over loan sales. With negotiating leverage, borrowers may restrict sale to competitors (only for initial sale, and only while not in default).

---

## Key Negotiation Points — Quick Reference

When representing a **mezzanine lender**, prioritize:
- Robust intercreditor protections (cure rights, purchase rights, anti-dilution)
- Article 8 opt-in and perfection by control
- Broad collateral description in pledge agreement
- UCC insurance coverage
- Mezzanine financing endorsement to mortgage borrower's title policy
- Comprehensive due diligence (property-level, as if purchasing)

When representing a **mezzanine borrower**, prioritize:
- Limiting cure right caps in intercreditor (maximize lender flexibility)
- Negotiating guarantor release on foreclosure or transfer
- Coordinating approval processes between lenders to minimize delays
- Restricting loan-to-own scenarios (notice periods, workout obligations)
- Limiting personal contract liability exposure
- Ensuring escrow coordination to avoid duplicative reserves

When representing a **mortgage lender**, prioritize:
- Tight time limits on mezzanine lender cure, purchase, and approval rights
- New guarantor requirements post-mezzanine foreclosure
- Anti-dilution limitations favorable to mortgage lender
- Emergency action carve-outs from approval requirements
- Transfer restrictions on mezzanine loan (qualified transferee requirements)
- Cash trap trigger protections
