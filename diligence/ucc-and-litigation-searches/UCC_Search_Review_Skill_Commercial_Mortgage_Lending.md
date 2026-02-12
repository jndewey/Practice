# Skill: Reviewing UCC Searches for Lenders in Commercial Mortgage Loans

## Purpose

This skill provides a systematic framework for reviewing UCC lien search results on behalf of a lender in a commercial mortgage loan transaction. The goal is to confirm that the borrower's and guarantor's assets are encumbered only by liens permitted under the loan documents, and that no liens have priority over or conflict with the lender's security interest in the loan collateral.

---

## 1. Understanding Why UCC Searches Matter in Commercial Mortgage Lending

In a commercial mortgage loan, the lender typically takes a mortgage on the real property and a UCC security interest in the borrower's personal property collateral (rents, accounts, equipment, fixtures, etc.). Before funding, the lender needs assurance that:

- No prior perfected security interests exist that would have priority over the lender's lien on personal property collateral.
- No undisclosed liens exist that would violate the borrower's representations and warranties or the negative covenants in the loan agreement.
- All existing liens are either (a) permitted under the loan documents, or (b) will be terminated at or before closing.

The UCC operates as a **notice filing system** — a UCC-1 financing statement does not itself create a lien but provides public notice that a party *may* have a security interest in the described collateral. If search results raise uncertainty, further inquiry with the secured party or debtor is necessary to determine the actual state of affairs.

---

## 2. What Searches to Order

### Core UCC Searches

For each loan party (borrower, guarantor, any pledgor of personal property collateral), order UCC searches at the **Secretary of State's office in the state of the entity's organization** (for registered organizations such as LLCs and corporations). This is the central filing office under UCC § 9-307.

- **Delaware-organized entities** → Search the Delaware Secretary of State.
- **Florida-organized entities** → Search the Florida Department of State.
- If a loan party has **changed its state of organization within the last four months**, also search the prior state.

### Supplemental Searches

Depending on deal requirements, also consider ordering:

- **Federal tax lien searches** — Filed where the property is located or where the debtor is organized (varies by state; in Delaware, indexed together with UCC filings).
- **State tax lien searches** — Varies by jurisdiction; may be at the county or state level.
- **Judgment lien and litigation searches** — Typically at the county level where the borrower is located or where the property sits; also check federal court (PACER).
- **Fixture filing searches** — Recorded in the county recorder's office where the real property is located (separate from the central UCC filing).
- **Bankruptcy searches** — Federal court (PACER) for any pending or recent filings.
- **ERISA lien searches** — If the borrower maintains defined benefit plans with potential unfunded liabilities exceeding $1 million.
- **Intellectual property searches** — USPTO and Copyright Office if IP is part of the collateral package.

### Practical Tips on Ordering

- Order searches **at the start of the transaction** — service companies can take several weeks.
- Confirm with the client and borrower's counsel **who is responsible** for ordering which searches to avoid duplication.
- Obtain a **cost and timing estimate** from the search company before proceeding and discuss with the client.
- Use the borrower's **perfection certificate** to confirm exact legal names, prior names, jurisdictions of organization, and tax return names.
- **Verify** the perfection certificate information against organizational documents (certificates of formation, articles of incorporation, amendments, etc.).

---

## 3. Ensuring the Correct Debtor Name

Getting the debtor name right is critical. Under UCC § 9-503(a)(1), for registered organizations the correct name is the **exact name on the entity's public organic record** (e.g., the certificate of formation filed with the Secretary of State).

### Search Name Checklist

For each loan party, search under:

1. **Exact legal name** as shown on the public organic record.
2. **Trade names / d/b/a names** — While not legally required, searching these may reveal filings by parties who used a trade name.
3. **Prior names** — If the entity has changed its name, search under former names.
4. **Tax return name** — The name used on the debtor's tax returns may differ from the legal name (see *In re Spearing Tool and Manufacturing Co., Inc.*, 412 F.3d 653 (6th Cir. 2005), where an IRS tax lien filed under the tax return name was held valid over a properly perfected UCC security interest).
5. **Name variations** — Searching variations may disclose filings against related entities in the organizational structure.

### Standard Search Logic Considerations

Filing offices apply their own **standard search logic** when processing search requests. For example, the Delaware Secretary of State ignores spacing, punctuation, case, a leading "The," and certain organizational suffixes and noise words. A financing statement with a slightly incorrect debtor name may still appear in results if it falls within the search logic — but it also may *not* appear if the error falls outside the logic. Do not rely solely on the filing office's search logic to catch all relevant filings.

---

## 4. How to Review UCC Search Results

When search results are received, review each filing systematically by answering the following questions:

### For Each UCC-1 Filing

| Question | What to Look For |
|---|---|
| **Who is the secured party?** | Identify the lender or creditor. Is it a known existing lender? A vendor? A lessor? |
| **Who is the debtor?** | Confirm the debtor name matches the loan party. If it does not match exactly, assess whether it is the same entity or a different one caught by the search logic. |
| **What collateral is described?** | Review the collateral description carefully. Does it cover assets that overlap with your lender's collateral package (e.g., "all assets," rents, accounts, equipment, fixtures, deposit accounts)? |
| **What is the purpose of the filing?** | Is it a true security interest, a precautionary filing (e.g., for a true lease or consignment), or an informational filing? |
| **What is the filing date?** | Determines priority. Earlier filing date = higher priority under the first-to-file-or-perfect rule. |
| **Has it been amended, assigned, continued, or terminated?** | Check for any UCC-3 amendments linked to the UCC-1. A termination means the lien has been released (but the filing remains visible for one year after lapse). |
| **Is the filing still effective?** | A UCC-1 is effective for five years from the filing date. If not continued, it lapses. Check whether a continuation statement was filed within the six-month window before the five-year anniversary. |

### For Each UCC-3 Filing (Amendment, Assignment, Continuation, Termination)

| Question | What to Look For |
|---|---|
| **Does it reference the correct UCC-1?** | Confirm the UCC-3 cites the correct initial financing statement file number. |
| **Is the authorizing party correct?** | The party authorizing the UCC-3 should be the secured party of record (or the debtor, if authorized). Watch for **"rogue" amendments** — unauthorized filings that reference the wrong file number or are filed by a party with no interest in the financing statement. |
| **What action does it take?** | Amendment (collateral change, debtor name change, secured party change), assignment, continuation, or termination. |
| **Is a terminated filing being continued?** | A continuation filed by a secured party on a UCC-1 that has already been terminated is a red flag for an unauthorized or erroneous filing. |

---

## 5. Categorizing and Dispositioning Each Filing

After reviewing each filing, categorize it into one of the following buckets:

### A. Terminated / Lapsed — No Action Required
The filing has been terminated by a UCC-3 termination statement or has lapsed (more than five years from filing with no continuation). Document it as cleared.

### B. Permitted Lien — Acceptable
The lien is expressly permitted under the loan agreement's negative covenant on liens (e.g., existing indebtedness scheduled as a permitted exception, purchase money security interests in equipment, capital lease obligations). Confirm it is listed on the schedule of permitted liens and that the collateral description does not conflict with the lender's collateral package.

### C. Informational / Precautionary Filing — No Action Required
The filing is a precautionary UCC-1 filed in connection with a true lease, consignment, or similar arrangement where no actual security interest exists. Confirm with the borrower and document the basis for treating it as precautionary.

### D. Must Be Terminated at Closing — Action Required
The filing secures indebtedness that will be repaid at closing. Require delivery of a **payoff letter** from the existing secured party confirming the payoff amount and agreeing to file a UCC-3 termination upon receipt of payment. The lender should receive either (a) a filed UCC-3 termination before closing, or (b) an executed UCC-3 termination in escrow to be filed at closing, along with the payoff letter.

### E. Requires Further Investigation — Action Required
The filing is unclear, potentially unauthorized, or raises concerns. Examples include filings by unknown secured parties, filings with overly broad collateral descriptions, filings that appear to be "rogue" or bogus, or filings where the authorizing party on a UCC-3 does not match the secured party of record. Follow up with the borrower and/or the listed secured party to resolve.

---

## 6. Preparing the Results Chart

Prepare a lien search results chart to track and present findings. The chart should include:

### Header Information
- Transaction name and client
- Responsible attorney(s)
- Search company name and contact
- Date last updated

### Table 1: Searches Ordered and Received

| Loan Party | Jurisdiction | Search Type | Date Ordered | Date Received | Effective Through |
|---|---|---|---|---|---|
| [Borrower name] | [State] SOS | UCC | [Date] | [Date] | [Date] |
| [Borrower name] | [County] | Fed/State Tax Lien | [Date] | [Date] | [Date] |
| [Guarantor name] | [State] SOS | UCC | [Date] | [Date] | [Date] |

### Table 2: Filings Found

| # | Filing Type | Secured Party | Debtor | Jurisdiction | Filing Date | File Number | Related UCC-1 | Collateral Summary | Status / Disposition |
|---|---|---|---|---|---|---|---|---|---|
| 1 | UCC-1 | [Name] | [Name] | [State] | [Date] | [Number] | N/A | All assets | To be terminated at closing |
| 2 | UCC-3 Term. | [Name] | [Name] | [State] | [Date] | [Number] | [UCC-1 #] | — | Terminated; no action |
| 3 | UCC-1 | [Name] | [Name] | [State] | [Date] | [Number] | N/A | Leased equipment | Precautionary; permitted |

---

## 7. Key Issues Specific to Commercial Mortgage Loans

### Fixtures
In commercial mortgage transactions, the lender's collateral typically includes fixtures. Confirm that no prior UCC-1 fixture filings exist in the **county recorder's office** where the property is located that would have priority over the lender's interest. Although recording a mortgage generally serves as a fixture filing in most states, best practice is to also file a separate UCC-1 fixture filing.

### Rents and Leases
Many commercial mortgage lenders take an assignment of rents and leases. Check whether any prior UCC filings cover rents, lease payments, or accounts that could conflict with the lender's assignment of rents.

### Deposit Accounts
If the lender is taking a security interest in deposit accounts, note that perfection of a security interest in deposit accounts is accomplished by **control** (not by filing a UCC-1), so a UCC search will not reveal a competing perfected interest in deposit accounts. Separate due diligence (e.g., deposit account control agreements) is required.

### SPE / Single-Purpose Entity Borrowers
In commercial mortgage lending, the borrower is often a single-purpose entity formed specifically to hold the property. The UCC search should ideally return **no filings** against an SPE borrower (other than the lender's own filing). Any existing filing against an SPE is a significant red flag that warrants immediate investigation.

### Mezzanine Lenders and Pledge of Equity
If there is a mezzanine loan in the capital stack, the mezzanine lender will typically file a UCC-1 against the **mezzanine borrower** (usually the direct or indirect parent of the mortgage borrower) covering the pledged equity interests. This filing should appear on a search of the mezzanine borrower — not the mortgage borrower. Confirm the mezzanine lender's UCC-1 does not encumber the mortgage borrower's assets.

---

## 8. Timing Considerations

- **Initial search**: Order at the start of the transaction as part of due diligence.
- **Bring-down search**: Order a second search shortly before closing to confirm no new filings have been recorded since the initial search. If borrower's counsel is delivering a legal opinion, they will typically conduct this bring-down search as part of their opinion due diligence.
- **Post-closing**: After the lender's UCC-1 is filed, confirm receipt of the filing acknowledgment and verify the filing appears correctly in a post-closing search.

---

## 9. Common Pitfalls

1. **Searching under the wrong name** — Always verify the exact legal name from the public organic record; do not rely solely on the name in the loan documents or the borrower's representations.
2. **Ignoring lapsed filings that are still visible** — A terminated or lapsed filing may still appear in search results (filings are retained for one year after lapse). Confirm it is truly terminated or lapsed before dismissing it.
3. **Missing "rogue" or unauthorized amendments** — Always check that the authorizing party on a UCC-3 matches the secured party of record on the related UCC-1.
4. **Overlooking fixture filings** — These are recorded at the county level, not with the Secretary of State. A central UCC search alone will not reveal fixture filings.
5. **Forgetting the tax return name** — Under *Spearing Tool*, an IRS tax lien filed under the debtor's tax return name can prime a properly perfected UCC security interest.
6. **Not searching prior names or prior jurisdictions** — Name changes and redomiciliations within the last four months require searches in the prior name/jurisdiction.
7. **Assuming a "clean" search means no liens exist** — UCC searches only reveal liens perfected by filing. Security interests perfected by control (deposit accounts, securities accounts) or possession will not appear in UCC search results.

---

## 10. Deliverables Checklist

Before closing, confirm the following have been completed:

- [ ] All UCC, tax lien, judgment lien, and other searches ordered and received for each loan party
- [ ] Each search reviewed and each filing categorized and dispositioned
- [ ] Results chart prepared, circulated to the deal team, and approved by the client
- [ ] Payoff letters received for all liens to be terminated at closing
- [ ] UCC-3 termination statements received (or in escrow) for all liens to be terminated
- [ ] Bring-down search ordered and reviewed shortly before closing
- [ ] Lender's UCC-1 financing statement prepared and ready to file at closing
- [ ] Fixture filing (if applicable) prepared and ready to record at closing
- [ ] Search results consistent with borrower's representations and warranties and the schedule of permitted liens in the loan agreement
