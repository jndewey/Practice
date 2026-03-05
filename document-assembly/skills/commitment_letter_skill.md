# Commitment Letter — Annotated Template Skill

## Document Metadata
- **Template:** `new_templates/Ocean Bank - Commitment Letter.docx`
- **When to Generate:** Every deal (all loan types)
- **Generated Per:** Once per deal
- **Dependencies:** None — this is the master document that establishes deal terms
- **Cross-References:** Promissory Note (rate, repayment, prepayment, covenants); Mortgage (collateral, escrow); Assignment of Leases and Rents (collateral); Guaranty Agreements (guarantor identity, scope); Construction Loan Agreement (construction terms); Borrower's Reps (borrower identity, deal terms)

---

## Part 1: CAS Field Mapping

Maps CAS fields to template placeholders. See `skills/cas_extraction_guide.md` for extraction details.

### Deal Identification

| Placeholder | CAS Field | Extraction |
|---|---|---|
| `[BORROWER NAME]` | Borrower(s) | Exact legal name with entity suffix |
| `[BORROWER NAME CAPS]` | Same | ALL CAPS version |
| `[BORROWER STATE]` | Entity description | State from "a [State] [entity type]" pattern |
| `[BORROWER ENTITY TYPE]` | Entity description | Lowercase: "limited liability company", "corporation", etc. |
| `[a/an]` | Computed | "an" if state starts with A/E/I/O; else "a" |
| `[RELATIONSHIP CONTACT]` | Header / RM field | Primary contact name |
| `[NEW OR EXISTING]` | Deal structure | "New Loan" or "Existing Loan" |
| `[LOAN PURPOSE]` | PURPOSE field | "Acquisition", "Refinance with existing debt", "Refinance free and clear", or "Construction" |
| `[PURPOSE ADD INFO]` | PURPOSE field | Additional detail beyond standard categories |
| `[LEASED PROPERTY FLAG]` | Property type | True if income-producing with tenants |
| `[UCC REQUIRED]` | Collateral section | True if UCC financing statement required |

### Loan Amount and Structure

| Placeholder | CAS Field | Extraction |
|---|---|---|
| `[$LOAN AMOUNT]` | LOAN AMOUNT | Formatted dollar amount: $X,XXX,XXX.XX |
| `[$LOAN AMOUNT WORDS]` | Same | Spelled out: "Five Million and No/100" |
| `[$LOAN AMOUNT 2]` | Second tranche | Only for bifurcated facilities |
| `[$EXISTING BALANCE]` | Current balance | For modifications |
| `[$EXISTING BALANCE WORDS]` | Same | Spelled out |
| `[$ORIGINAL LOAN AMOUNT]` | Original amount | For modifications |
| `[EXISTING LENDER]` | Refinance section | Lender being refinanced |
| `[REMAINING PROCEEDS USE]` | PURPOSE field | Use of excess proceeds |
| `[LOAN AMOUNT OR FUTURE ADVANCE]` | Deal structure | "loan amount" or "future advance" |
| `[LOAN AMOUNT BASIS]` | LOAN AMOUNT section | List: "LTV", "Loan to Purchase", "DSCR" |
| `[$FUTURE ADVANCE AMOUNT]` | Future advance section | Dollar amount of advance |
| `[$FUTURE ADVANCE AMOUNT WORDS]` | Same | Spelled out |

### Holdback

| Placeholder | CAS Field | Extraction |
|---|---|---|
| `[HOLDBACK FLAG]` | Holdback section | True if portion withheld |
| `[$HOLDBACK AMOUNT]` | Holdback section | Dollar amount withheld |
| `[$HOLDBACK AMOUNT WORDS]` | Same | Spelled out |
| `[HOLDBACK BASIS]` | Holdback section | "Exact Amount" or "Calculation" |
| `[HOLDBACK CONDITIONS]` | Holdback section | Conditions for release |
| `[HOLDBACK CONDITIONS WORDS]` | Same | Spelled out |

### Interest Rate

| Placeholder | CAS Field | Extraction |
|---|---|---|
| `[RATE STRUCTURE]` | RATE section | "fixed", "floating", "variable", or "swap" |
| `[FIXED RATE]` | RATE section | Fixed rate as percentage |
| `[FIXED RATE WORDS]` | Same | Spelled out |
| `[INITIAL FIXED TERM]` | RATE section | Years before first adjustment |
| `[INITIAL FIXED TERM WORDS]` | Same | Spelled out |
| `[RATE ADJUSTMENTS]` | RATE section | Number of adjustment events |
| `[RATE SPREAD]` | RATE section | Spread for swap structures |
| `[INDEX]` | RATE section | "SOFR" or "Prime" |
| `[MARGIN RATE]` | RATE section | Spread over index |
| `[MARGIN RATE WORDS]` | Same | Spelled out |
| `[FLOOR RATE]` | RATE section | Minimum interest rate |
| `[FLOOR RATE WORDS]` | Same | Spelled out |

### Term and Repayment

| Placeholder | CAS Field | Extraction |
|---|---|---|
| `[TERM]` | TERM field | Total term in years |
| `[TERM WORDS]` | Same | Spelled out: "five (5)" |
| `[AMORTIZATION PERIOD]` | AMORTIZATION | Amortization in years |
| `[AMORTIZATION PERIOD WORDS]` | Same | Spelled out |
| `[IO MONTHS]` | REPAYMENT | IO period length in months |
| `[IO MONTHS WORDS]` | Same | Spelled out |
| `[EXTENSION TERM]` | EXTENSION | Length of extension |
| `[EXTENSION TERM WORDS]` | Same | Spelled out |
| `[EXTENSION PERIOD]` | EXTENSION | "months" or "years" |
| `[EXTENSION OPTIONS]` | EXTENSION | Number of extension options |
| `[EXTENSION OPTIONS WORDS]` | Same | Spelled out |
| `[CONSTRUCTION TERM]` | Construction section | Construction phase months |
| `[CONSTRUCTION TERM WORDS]` | Same | Spelled out |
| `[PERMANENT TERM]` | Construction section | Permanent phase years |
| `[PERMANENT TERM WORDS]` | Same | Spelled out |

### Prepayment

| Placeholder | CAS Field | Extraction |
|---|---|---|
| `[PREPAYMENT PENALTY FLAG]` | PREPAYMENT | True if penalty exists |
| `[PREPAYMENT PENALTY TYPE]` | PREPAYMENT | "bona fide" or "refinance" |
| `[PREPAYMENT PERCENTAGE]` | PREPAYMENT | Rate as percentage |
| `[PREPAYMENT PERCENTAGE WORDS]` | Same | Spelled out |
| `[PREPAYMENT TERM]` | PREPAYMENT | Years penalty applies |
| `[PREPAYMENT TERM WORDS]` | Same | Spelled out |

### Guaranty

| Placeholder | CAS Field | Extraction |
|---|---|---|
| `[PG NAME]` | GUARANTOR | Personal guarantor name (repeats per guarantor) |
| `[EG NAME]` | GUARANTOR | Entity guarantor name (repeats per guarantor) |
| `[EG STATE]` | GUARANTOR | Entity guarantor state |
| `[EG ENTITY TYPE]` | GUARANTOR | Entity guarantor entity type |
| `[TG NAME]` | GUARANTOR | Trust guarantor name |
| `[TG TRUSTEE NAME]` | GUARANTOR | Trustee name |
| `[TG TRUST DATE]` | GUARANTOR | Trust agreement date |
| `[BAD BOY GUARANTOR NAME]` | GUARANTOR | Carveout guarantor name |

### Covenants

| Placeholder | CAS Field | Extraction |
|---|---|---|
| `[DSCR RATIO]` | DSCR analysis | Actual DSCR ratio |
| `[DSCR COVENANT RATE]` | COVENANTS | Minimum required DSCR |
| `[DSCR MIN MGMT FEE]` | COVENANTS | Minimum management fee % |
| `[DSCR MIN MGMT FEE WORDS]` | Same | Spelled out |
| `[DSCR START DATE]` | COVENANTS | Date if "particular year" start |
| `[DSCR ADJUSTMENT BASIS]` | COVENANTS | Adjustment basis description |
| `[LTV RATIO]` | LOAN AMOUNT | Max LTV % |
| `[LTV RATIO WORDS]` | Same | Spelled out |
| `[LTP RATIO]` | Acquisitions | Loan-to-purchase % |
| `[LTP RATIO WORDS]` | Same | Spelled out |
| `[LTC RATIO]` | Construction | Loan-to-cost % |
| `[LTC RATIO WORDS]` | Same | Spelled out |
| `[LTV MAINTENANCE RATIO]` | LTV COVENANT | Max LTV triggering cure |
| `[LTV MAINTENANCE RATIO WORDS]` | Same | Spelled out |
| `[RESERVE FEE]` | RESERVES | Reserve fee percentage |
| `[RESERVE FEE WORDS]` | Same | Spelled out |

### Reserves and Conditions

| Placeholder | CAS Field | Extraction |
|---|---|---|
| `[RESERVE MONTHS]` | RESERVES | Months of P&I in reserve |
| `[RESERVE MONTHS WORDS]` | Same | Spelled out |
| `[$STABILIZATION RESERVE AMOUNT]` | RESERVES | Stabilization reserve amount |
| `[INTEREST RESERVE MONTHS]` | RESERVES | Interest reserve months |
| `[INTEREST RESERVE MONTHS WORDS]` | Same | Spelled out |
| `[EQUITY REQUIREMENT]` | Construction | Equity requirement percentage |
| `[EQUITY REQUIREMENT WORDS]` | Same | Spelled out |
| `[FRANCHISOR NAME]` | FRANCHISE | Franchisor name |
| `[CROSS BORROWER]` | CROSS-DEFAULT | Cross-default borrower name |
| `[CROSS PROPERTY]` | CROSS-DEFAULT | Cross-collateral property |

### Property

| Placeholder | CAS Field | Extraction |
|---|---|---|
| `[PROPERTY DESCRIPTION]` | PROPERTY | Brief description |
| `[PROPERTY ADDRESS]` | PROPERTY | Street address |
| `[PROPERTY COUNTY]` | PROPERTY | County name |
| `[FOLIO NUMBER]` | PROPERTY | Folio number(s) — repeats in `[FOR EACH: FOLIOS]` |

### Bank Personnel

| Placeholder | CAS Field | Extraction |
|---|---|---|
| `[SENIOR VP NAME]` | Bank approval | SVP name |
| `[BANK OFFICER NAME]` | Bank approval | RM name |
| `[BANK OFFICER POSITION]` | Bank approval | Title abbreviation |

### Fees and Dates

| Placeholder | CAS Field | Extraction |
|---|---|---|
| `[COMMITMENT DATE]` | Header | Month [___], Year |
| `[CLOSING DATE]` | CLOSING | Target closing date |
| `[COMMITMENT FEE %]` | FEE section | Fee percentage |
| `[COMMITMENT FEE % WORDS]` | Same | Spelled out |

### Signatory Information — [EXTERNAL INPUT REQUIRED]

| Placeholder | Source |
|---|---|
| `[BORROWER SIG 1 TYPE]` | Attorney provides: "entity", "individual", or "blank" |
| `[BORROWER SIG 1 ENTITY NAME]` | Signing entity name |
| `[BORROWER SIG 1 ENTITY NAME CAPS]` | Same, ALL CAPS |
| `[BORROWER SIG 1 ENTITY TYPE]` | Entity type |
| `[BORROWER SIG 1 ENTITY STATE]` | State of organization |
| `[BORROWER SIG 1 RELATIONSHIP]` | "Manager", "Managing Member", etc. |
| `[BORROWER SIG 1 NAME]` | Individual signer name |
| `[BORROWER SIG 1 NAME CAPS]` | Same, ALL CAPS |
| `[BORROWER SIG 1 TITLE]` | Signer title |
| `[BORROWER SIG 2 *]` | Same pattern for second tier |
| `[BORROWER SIG 3 *]` | Same pattern for third tier |

---

## Part 2: Placeholder Operations Registry

Every placeholder in the template and the exact operation to perform. **The AI replaces each placeholder with the extracted value. Nothing else in the surrounding paragraph changes.**

| # | Placeholder | Operation | Format Rule | Template Section(s) |
|---|---|---|---|---|
| P1 | `[BORROWER NAME]` | Replace with legal name | Exact legal name with entity suffix | §1 Header, §3 Borrower, §RE |
| P2 | `[BORROWER NAME CAPS]` | Replace with legal name | ALL CAPS | §RE, Sig block |
| P3 | `[BORROWER STATE]` | Replace with state name | Title case: "Florida" | §RE, §3 |
| P4 | `[BORROWER ENTITY TYPE]` | Replace with entity type | Lowercase: "limited liability company" | §RE, §3 |
| P5 | `[a/an]` | Replace with article | "an" if next word starts with vowel sound; "a" otherwise | §RE, §3 |
| P6 | `[RELATIONSHIP CONTACT]` | Replace with contact name | First Last | §1 Header, §2 Intro |
| P7 | `[COMMITMENT DATE]` | Replace with date | Month [___], Year format | §1 Header |
| P8 | `[$LOAN AMOUNT]` | Replace with dollar amount | $X,XXX,XXX.XX | §4 Amount, §RE |
| P9 | `[$LOAN AMOUNT WORDS]` | Replace with spelled amount | "Five Million and No/100" | §4 Amount |
| P10 | `[$EXISTING BALANCE]` | Replace with dollar amount | $X,XXX,XXX.XX | §4 Amount, §RE |
| P11 | `[$EXISTING BALANCE WORDS]` | Replace with spelled amount | Same pattern | §4 Amount |
| P12 | `[$ORIGINAL LOAN AMOUNT]` | Replace with dollar amount | $X,XXX,XXX.XX | §RE (existing loan) |
| P13 | `[EXISTING LENDER]` | Replace with lender name | Exact name | §5 Purpose |
| P14 | `[REMAINING PROCEEDS USE]` | Replace with description | Lowercase clause | §5 Purpose |
| P15 | `[$FUTURE ADVANCE AMOUNT]` | Replace with dollar amount | $X,XXX,XXX.XX | §4 Amount |
| P16 | `[$FUTURE ADVANCE AMOUNT WORDS]` | Replace with spelled amount | Same pattern | §4 Amount |
| P17 | `[$HOLDBACK AMOUNT]` | Replace with dollar amount | $X,XXX,XXX.XX | §4 Amount |
| P18 | `[$HOLDBACK AMOUNT WORDS]` | Replace with spelled amount | Same pattern | §4 Amount |
| P19 | `[HOLDBACK CONDITIONS]` | Replace with conditions | Narrative description | §4 Amount |
| P20 | `[HOLDBACK CONDITIONS WORDS]` | Replace with spelled number | "twelve (12)" | §4 Amount |
| P21 | `[TERM]` | Replace with number | Numeral only | §7 Term |
| P22 | `[TERM WORDS]` | Replace with spelled number | "five (5)" | §7 Term |
| P23 | `[AMORTIZATION PERIOD]` | Replace with number | Numeral only | §9 Repayment |
| P24 | `[AMORTIZATION PERIOD WORDS]` | Replace with spelled number | "twenty-five (25)" | §9 Repayment |
| P25 | `[IO MONTHS]` | Replace with number | Numeral only | §9 Repayment |
| P26 | `[IO MONTHS WORDS]` | Replace with spelled number | "twenty-four (24)" | §9 Repayment |
| P27 | `[EXTENSION TERM]` | Replace with number | Numeral only | §7 Term |
| P28 | `[EXTENSION TERM WORDS]` | Replace with spelled number | "one (1)" | §7 Term |
| P29 | `[EXTENSION PERIOD]` | Replace with unit | "months" or "years" | §7 Term |
| P30 | `[EXTENSION OPTIONS]` | Replace with number | Numeral only | §7 Term |
| P31 | `[EXTENSION OPTIONS WORDS]` | Replace with spelled number | "two (2)" | §7 Term |
| P32 | `[CONSTRUCTION TERM]` | Replace with number | Numeral only | §7 Term |
| P33 | `[CONSTRUCTION TERM WORDS]` | Replace with spelled number | "eighteen (18)" | §7 Term |
| P34 | `[PERMANENT TERM]` | Replace with number | Numeral only | §7 Term |
| P35 | `[PERMANENT TERM WORDS]` | Replace with spelled number | "five (5)" | §7 Term |
| P36 | `[FIXED RATE]` | Replace with rate | X.XX | §8 Rate |
| P37 | `[FIXED RATE WORDS]` | Replace with spelled rate | "five and sixty-five hundredths (5.65)" | §8 Rate |
| P38 | `[INITIAL FIXED TERM]` | Replace with number | Numeral only | §8 Rate |
| P39 | `[INITIAL FIXED TERM WORDS]` | Replace with spelled number | "five (5)" | §8 Rate |
| P40 | `[INDEX]` | Replace with index name | "SOFR" or "Prime" | §8 Rate |
| P41 | `[MARGIN RATE]` | Replace with rate | X.XX | §8 Rate |
| P42 | `[MARGIN RATE WORDS]` | Replace with spelled rate | Same pattern | §8 Rate |
| P43 | `[FLOOR RATE]` | Replace with rate | X.XX | §8 Rate |
| P44 | `[FLOOR RATE WORDS]` | Replace with spelled rate | Same pattern | §8 Rate |
| P45 | `[RATE SPREAD]` | Replace with spread | X.XX% | §8 Rate (swap) |
| P46 | `[COMMITMENT FEE %]` | Replace with rate | X.XX | §10 Fee |
| P47 | `[COMMITMENT FEE % WORDS]` | Replace with spelled rate | "one (1.00)" | §10 Fee |
| P48 | `[PREPAYMENT PERCENTAGE]` | Replace with rate | X.XX | §12 Prepayment |
| P49 | `[PREPAYMENT PERCENTAGE WORDS]` | Replace with spelled rate | Same pattern | §12 Prepayment |
| P50 | `[PREPAYMENT TERM]` | Replace with number | Numeral only | §12 Prepayment |
| P51 | `[PREPAYMENT TERM WORDS]` | Replace with spelled number | Same pattern | §12 Prepayment |
| P52 | `[DSCR RATIO]` | Replace with ratio | X.XX | §4, §17 Covenants |
| P53 | `[DSCR COVENANT RATE]` | Replace with ratio | X.XX | §17 Covenants |
| P54 | `[DSCR MIN MGMT FEE]` | Replace with rate | X | §17 Covenants |
| P55 | `[DSCR MIN MGMT FEE WORDS]` | Replace with spelled | Same pattern | §17 Covenants |
| P56 | `[DSCR START DATE]` | Replace with date/year | "2027" or "January 2027" | §17 Covenants |
| P57 | `[DSCR ADJUSTMENT BASIS]` | Replace with description | Narrative clause | §4 Amount |
| P58 | `[LTV RATIO]` | Replace with percentage | XX | §19 Conditions |
| P59 | `[LTV RATIO WORDS]` | Replace with spelled | Same pattern | §19 Conditions |
| P60 | `[LTP RATIO]` | Replace with percentage | XX | §4 Amount |
| P61 | `[LTP RATIO WORDS]` | Replace with spelled | Same pattern | §4 Amount |
| P62 | `[LTC RATIO]` | Replace with percentage | XX | §4, §18 Construction |
| P63 | `[LTC RATIO WORDS]` | Replace with spelled | Same pattern | §4, §18 Construction |
| P64 | `[LTV MAINTENANCE RATIO]` | Replace with percentage | XX | §17 Covenants |
| P65 | `[LTV MAINTENANCE RATIO WORDS]` | Replace with spelled | Same pattern | §17 Covenants |
| P66 | `[RESERVE FEE]` | Replace with percentage | X | §4 Holdback, §17 |
| P67 | `[RESERVE FEE WORDS]` | Replace with spelled | Same pattern | §4, §17 |
| P68 | `[RESERVE MONTHS]` | Replace with number | Numeral | §19 Conditions |
| P69 | `[RESERVE MONTHS WORDS]` | Replace with spelled | Same pattern | §19 Conditions |
| P70 | `[$STABILIZATION RESERVE AMOUNT]` | Replace with amount | $X,XXX,XXX.XX | §19 Conditions |
| P71 | `[INTEREST RESERVE MONTHS]` | Replace with number | Numeral | §19 Conditions |
| P72 | `[INTEREST RESERVE MONTHS WORDS]` | Replace with spelled | Same pattern | §19 Conditions |
| P73 | `[EQUITY REQUIREMENT]` | Replace with percentage | XX | §18 Construction |
| P74 | `[EQUITY REQUIREMENT WORDS]` | Replace with spelled | Same pattern | §18 Construction |
| P75 | `[FRANCHISOR NAME]` | Replace with name | Exact name | §19 Conditions |
| P76 | `[CROSS BORROWER]` | Replace with name | Exact legal name | §17 Covenants |
| P77 | `[CROSS PROPERTY]` | Replace with address | Property address | §17 Covenants |
| P78 | `[PROPERTY DESCRIPTION]` | Replace with description | Brief description | §5 Purpose, §RE |
| P79 | `[PROPERTY ADDRESS]` | Replace with address | Street address | §5 Purpose, §RE |
| P80 | `[PROPERTY COUNTY]` | Replace with county | County name | §5 Purpose |
| P81 | `[FOLIO NUMBER]` | Replace with folio | Folio number string | §5, §RE (in FOR EACH loop) |
| P82 | `[SENIOR VP NAME]` | Replace with name | First Last | Sig block |
| P83 | `[BANK OFFICER NAME]` | Replace with name | First Last | Sig block |
| P84 | `[BANK OFFICER POSITION]` | Replace with title | Abbreviated title | Sig block |
| P85 | `[CLOSING DATE]` | Replace with date | Month Day, Year | §20 Closing |
| P86 | `[INTEREST RESERVE FLAG]` | Replace with description | Months description | §18 Construction |
| P87-P99 | `[BORROWER SIG * ]` | Replace with signatory info | Per external input | Sig blocks |

---

## Part 3: Conditional Section Map

Every section that might be deleted, with the exact condition and scope. **The AI deletes the identified block (markers + content) via tracked changes. Nothing else changes.**

### Template Markers

The template uses inline markers to delineate conditional sections:
- `[IF: LABEL]` ... `[END IF: LABEL]` — conditional block
- `[FOR EACH: COLLECTION]` ... `[END FOR EACH: COLLECTION]` — repeating block

When a condition is **FALSE**, delete the entire block including markers. When **TRUE**, delete only the markers themselves (keep the content).

### Major Conditional Sections

| # | Section Marker | DELETE when | Scope | Notes |
|---|---|---|---|---|
| C1 | `[IF: NEW LOAN]` blocks | Existing loan | §RE, §4, §5, §19 | Multiple occurrences throughout |
| C2 | `[IF: EXISTING LOAN]` blocks | New loan | §RE, §4, §5, §17, §19 | Multiple occurrences |
| C3 | `[IF: HOLDBACK]` block | No holdback | §4 Amount | ~3 paragraphs: initial funding, holdback release conditions |
| C4 | `[IF: EXTENSION OPTION]` blocks | No extension | §7 Term | Extension language within term section |
| C5 | `[IF: LOAN PURPOSE: CONSTRUCTION]` blocks | Not construction | §7, §8, §9, §17, §18, §19 | Construction covenants, entire §18 |
| C6 | `[IF: NOT LOAN PURPOSE: CONSTRUCTION]` blocks | Construction | §7, §8, §9, §19 | Standard (non-construction) variants |
| C7 | `[IF: PERMANENT PHASE]` blocks | No permanent phase | §7 Term | Conversion language |
| C8 | `[IF: COMMITMENT FEE]` blocks | No commitment fee | §10 heading, §10 body | Commitment fee language |
| C9 | `[IF: UNDERWRITING FEE]` blocks | Has commitment fee | §10 heading | "Underwriting" heading variant |
| C10 | `[IF: PREPAYMENT PENALTY]` blocks | No penalty | §12 Prepayment | Penalty language |
| C11 | `[IF: NO PREPAYMENT PENALTY]` blocks | Has penalty | §12 Prepayment | "without premium or penalty" |
| C12 | `[IF: INTEREST RATE STRUCTURE: FIXED]` blocks | Not fixed rate | §8 Rate | Fixed rate language |
| C13 | `[IF: INTEREST RATE STRUCTURE: FLOATING]` blocks | Not floating rate | §8 Rate | Floating rate language |
| C14 | `[IF: INTEREST RATE STRUCTURE: VARIABLE]` blocks | Not variable rate | §8 Rate | Variable rate language |
| C15 | `[IF: INTEREST RATE STRUCTURE: SWAP]` blocks | Not swap rate | §8 Rate, §12 | Swap rate + breakage language |
| C16 | `[IF: INTEREST ONLY]` blocks | No IO period | §9 Repayment | IO period language |
| C17 | `[IF: NO INTEREST ONLY]` blocks | Has IO period | §9 Repayment | P&I from start language |
| C18 | `[IF: DSCR COVENANT]` blocks | No DSCR covenant | §17 Covenants | DSCR maintenance language |
| C19 | `[IF: NOI-BASED DSCR]` blocks | Non-NOI DSCR | §17 Covenants | NOI-based DSCR + LTV maintenance |
| C20 | `[IF: NON-NOI DSCR]` blocks | NOI-based DSCR | §17 Covenants | Simpler DSCR language |
| C21 | `[IF: TAX ESCROW: *]` blocks | Different escrow type | §17 Covenants | Keep matching escrow variant |
| C22 | `[IF: CROSS DEFAULT]` block | No cross-default | §17 Covenants | Cross-default language |
| C23 | `[IF: TENANT RESERVE]` block | No tenant reserve | §17 Covenants | Tenant reserve language |
| C24 | `[IF: GUARANTOR SECTION]` block | No guarantors and no bad boy | §6 Guarantor | Entire guarantor section |
| C25 | `[IF: LEASED PROPERTY]` block | Not leased property | §14 Leases | Entire leases section |
| C26 | `[IF: LOAN PURPOSE: ACQUISITION]` block | Not acquisition | §15 Purchase Agreement | Entire purchase agreement section |
| C27 | `[IF: RESERVE ACCOUNT]` block | No reserve account | §19 Conditions | Reserve account condition |
| C28 | `[IF: STABILIZATION RESERVE]` block | No stabilization reserve | §19 Conditions | Stabilization reserve condition |
| C29 | `[IF: INTEREST RESERVE]` block | No interest reserve | §19 Conditions | Interest reserve condition |
| C30 | `[IF: FRANCHISE]` block | Not franchised | §19 Conditions | Franchise agreement condition |
| C31 | `[IF: JV/LP AGREEMENTS]` block | No JV/LP | §19 Conditions | JV/LP agreements condition |
| C32 | `[IF: CONDITION REPORTS]` block | No condition reports | §19 Conditions | Property condition report |
| C33 | `[IF: STAR REPORTS]` block | No star reports | §16 Reporting | Star report language |
| C34 | `[IF: BOND]` block | No bond required | §18 Construction | Bond requirement |
| C35 | `[IF: UCC REQUIRED]` / `[IF: UCC NOT REQUIRED]` | Opposite state | §13 Collateral | "does" / "does not" |

### Reporting Section Conditionals

| # | Section Marker | DELETE when | Scope |
|---|---|---|---|
| C36 | `[IF: BORROWER OR ENTITY FINANCIALS]` | Neither required | §16 financial statements |
| C37 | `[IF: BORROWER OR GUARANTOR TAX RETURNS]` | Neither required | §16 tax returns |
| C38 | `[IF: RENT ROLL OR OPERATING STATEMENT]` | Neither required | §16 rent roll/operating |
| C39 | `[IF: BORROWER FINANCIALS]` / `[IF: ENTITY GUARANTOR FINANCIALS]` | Not applicable | §16 sub-conditions |
| C40 | `[IF: BORROWER TAX RETURNS]` / `[IF: GUARANTOR TAX RETURNS]` | Not applicable | §16 sub-conditions |
| C41 | `[IF: TAX EXTEND CORP]` / `[IF: TAX EXTEND PERSONAL]` | No extension | §16 tax return deadlines |

### Rate Section Sub-Conditionals

| # | Section Marker | DELETE when | Scope |
|---|---|---|---|
| C42 | `[IF: FIXED RATE KNOWN]` | Rate TBD | §8 Rate: specific rate |
| C43 | `[IF: FIXED RATE TBD]` | Rate known | §8 Rate: formula language |
| C44 | `[IF: SOFR INDEX]` / `[IF: PRIME INDEX]` | Other index | §8 Rate: index name |
| C45 | `[IF: MARGIN]` / `[IF: NO MARGIN]` | Opposite | §8 Rate: margin language |
| C46 | `[IF: FLOOR RATE]` / `[IF: NO FLOOR RATE]` | Opposite | §8 Rate: floor language |
| C47 | `[IF: FLOOR RATE KNOWN]` / `[IF: FLOOR RATE TBD]` | Opposite | §8 Rate: floor rate |
| C48 | `[IF: INITIAL RATE KNOWN]` / `[IF: INITIAL RATE TBD]` | Opposite | §8 Rate (variable) |

### Guarantor Sub-Conditionals

| # | Section Marker | DELETE when | Scope |
|---|---|---|---|
| C49 | `[IF: PERSONAL GUARANTORS]` | No personal guarantors | §6, §16 |
| C50 | `[IF: ENTITY GUARANTORS]` | No entity guarantors | §6, §16 |
| C51 | `[IF: TRUST GUARANTORS]` | No trust guarantors | §6 |
| C52 | `[IF: MULTIPLE GUARANTORS]` | Single guarantor | §6: "jointly and severally" |
| C53 | `[IF: BAD BOY GUARANTOR]` | No bad boy | §6: carveout language |
| C54 | `[IF: EXISTING OWNERSHIP]` | No existing ownership | §6: ownership language |

### Signature Block Conditionals

| # | Section Marker | DELETE when | Scope |
|---|---|---|---|
| C55 | `[IF: SIG 1 ENTITY]` | Not entity signer | Sig block tier 1 |
| C56 | `[IF: SIG 1 INDIVIDUAL]` | Not individual signer | Sig block tier 1 |
| C57 | `[IF: SIG 1 BLANK]` | Not blank signer | Sig block tier 1 |
| C58 | `[IF: SIG 2 *]` blocks | Per signing chain | Sig block tier 2 |
| C59 | `[IF: SIG 3 *]` blocks | Per signing chain | Sig block tier 3 |

### FOR EACH Loops

| # | Section Marker | Action | Scope |
|---|---|---|---|
| L1 | `[FOR EACH: FOLIOS]` | Duplicate content for each folio | §RE, §5 Purpose |
| L2 | `[FOR EACH: PERSONAL GUARANTORS]` | Duplicate for each personal guarantor | §6, Sig blocks |
| L3 | `[FOR EACH: ENTITY GUARANTORS]` | Duplicate for each entity guarantor | §6, Sig blocks |
| L4 | `[FOR EACH: TRUST GUARANTORS]` | Duplicate for each trust guarantor | §6, Sig blocks |

**FOR EACH handling:** Remove the `[FOR EACH:]` and `[END FOR EACH:]` markers. Duplicate the content block for each item in the collection, replacing the item-level placeholders (`[PG NAME]`, `[EG NAME]`, `[FOLIO NUMBER]`, etc.) with each item's value. Handle list punctuation: commas between items, "and" before the last item.

---

## Part 4: Edge Case Catalog

Edge cases that mechanical placeholder replacement and conditional deletion cannot handle. Each requires human-like judgment and is flagged with a `[REVIEW]` comment.

### EC1: Multiple Borrowers
**When:** More than one borrowing entity
**Template gap:** Template uses single `[BORROWER NAME]`
**Action:**
1. In §RE: Name all borrowers, establish collective defined term ("Borrowers")
2. In §3 Borrower: List each entity with description
3. If co-borrower exists: add separate "Co-Borrower" paragraph
4. Insert tracked addition + `[EDGE CASE: Multiple borrower structure — verify collective term and co-borrower naming]` comment
**Example:** "TGC GOVERNORS SQUARE, LLC, TGC PARKSIDE, LLC, AND TGC ENRICHMENT CENTER, LLC, each a Florida limited liability company (collectively, the 'Borrowers')"

### EC2: Payment-Only Corporate Guaranty
**When:** CAS limits guaranty to loan payments (not principal)
**Template gap:** Template assumes full recourse or bad boy
**Action:**
1. Modify standard guarantor language to reflect limitation
2. Add: "Guarantor's obligations shall be limited to the prompt and unconditional payment of the Borrowers' Liabilities as they become due and payable through the maturity of the Loan."
3. Insert `[REVIEW: Payment-only guaranty — verify scope of "Borrowers' Liabilities" and whether additional carveout guaranty is required]` comment

### EC3: Multi-Tier Prepayment Penalty
**When:** CAS specifies tiered penalty rates (e.g., 0.25% years 1-10, 0.125% years 11-15)
**Template gap:** Template handles single-tier penalty only
**Action:**
1. Replace single penalty language with tiered structure
2. Preserve bona fide sale exception if applicable
3. Insert `[REVIEW: Multi-tier penalty — verify breakpoints and rates against CAS]` comment

### EC4: Non-Standard Rate Repricing
**When:** Rate structure doesn't match standard fixed/floating/variable/swap patterns
**Template gap:** Template handles standard patterns only
**Action:**
1. Draft rate language following closest standard pattern
2. Insert specific repricing mechanics
3. Insert `[REVIEW: Non-standard rate repricing — verify adjustment dates, index, and floor against CAS]` comment
**Example:** "During the first five (5) years, fixed at 5.65%. On each fifth anniversary, adjusted to the greater of (A) 1-month CME Term SOFR + 2.00%, or (B) 5.65% Floor Rate."

### EC5: Non-Standard Amortization
**When:** Amortization exceeds 25-year policy maximum
**Action:**
1. Draft normally using CAS amortization period
2. Insert `[POLICY EXCEPTION: {X}-year amortization exceeds 25-year policy max — confirmed as exception in CAS]` comment

### EC6: Portfolio Refinance
**When:** Refinancing multiple properties from another lender as single transaction
**Action:**
1. Describe as portfolio transaction in §5 Purpose
2. List all properties with addresses and folios
3. Insert `[REVIEW: Portfolio refinance — verify all properties included and collateral descriptions]` comment

### EC7: Operating Account Waiver
**When:** CAS waives operating account requirement
**Action:**
1. Delete deposit account covenant in §17
2. Insert `[REVIEW: Operating account requirement waived per CAS — confirm]` comment

### EC8: Multiple Properties
**When:** Loan secured by more than one property
**Action:**
1. List all properties in collateral description
2. Separate recordings if different counties
3. Insert `[EDGE CASE: Multiple properties — verify each property description and folio]` comment

---

## Part 5: Invariant Rules

These rules are absolute constraints on the AI's behavior when editing the template.

### Rule 1: Never Rewrite Template Language
The template text IS the Ocean Bank form. The words, phrases, and legal provisions are approved language. Only replace placeholders and delete conditional sections. Never paraphrase, rephrase, or rewrite any template text.

### Rule 2: Never Paraphrase
If a section applies to the deal, keep it verbatim. If it doesn't apply, delete the entire conditional block. There is no middle ground — never "adjust" template language to better fit the deal.

### Rule 3: Preserve Surrounding Text
When replacing `[BORROWER NAME]` with "ABC Corp", the words before and after the placeholder remain untouched. When deleting a conditional block, adjacent text remains intact.

### Rule 4: When in Doubt, Flag It
If the CAS is ambiguous, the deal structure doesn't match a template scenario, or an edge case is unclear:
- Add a `[REVIEW]` Word comment
- Do NOT attempt to resolve the ambiguity by rewriting
- Draft using the more conservative interpretation
- State both interpretations in the comment

### Rule 5: Edge Cases Are Additive Only
Edge case handling (Part 4) may INSERT new language via tracked changes with a comment. It never MODIFIES existing template text. The insertion is always marked as a tracked addition so the attorney can see it clearly.

### Rule 6: Tracked Changes for Everything
- **Placeholder replacement:** `<w:del>` the placeholder + `<w:ins>` the value
- **Conditional deletion:** `<w:del>` the entire block including markers
- **Conditional keep:** `<w:del>` only the `[IF:]` and `[END IF:]` markers
- **Edge case insertion:** `<w:ins>` the new language + Word comment
- The attorney must be able to see every single change the AI made.

### Rule 7: Cross-Reference Consistency
These values must be identical across all deal documents:
- Party names and entity descriptions
- Loan amount, rate, term, amortization
- DSCR covenant rate and testing mechanics
- Prepayment penalty terms
- Collateral descriptions and folio numbers
- Signature blocks

---

## Formatting Specifications

- **Paper:** US Letter, ~1" margins
- **Font:** Times New Roman, 12pt
- **Alignment:** Justified body, centered heading/date
- **Dollar amounts:** Spelled out + parenthetical numerals: "Five Million and No/100 Dollars ($5,000,000.00)"
- **Percentages:** Spelled out + parenthetical: "one (1.00%)"
- **Numbers:** Spelled out + parenthetical: "five (5)"
- **Defined terms:** Quoted with parenthetical on first use: "Loan", "Property", "Borrower"
- **Signature names:** ALL CAPS
- **Entity types:** Lowercase in running text
- **Section labels:** Bold, tab-separated from content
