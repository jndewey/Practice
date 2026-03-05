#!/usr/bin/env python3
"""
Generate a commitment letter from the maximum template using CAS-extracted parameters.
Graham Companies deal — $28,000,000 Refinance of portfolio from BankUnited.

This script:
1. Opens the maximum template .docx
2. Resolves all conditional sections (keep or delete)
3. Replaces all placeholders with CAS-extracted values
4. Handles FOR EACH loops
5. Applies tracked changes (w:del / w:ins) for attorney review
6. Adds Word comments for edge cases and review items
7. Saves the output .docx
"""

import zipfile
import copy
import re
import os
from lxml import etree
from datetime import datetime

# ============================================================
# NAMESPACES
# ============================================================

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
R_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
CT_NS = "http://schemas.openxmlformats.org/package/2006/content-types"
XML_NS = "http://www.w3.org/XML/1998/namespace"

NS = {"w": W_NS, "r": R_NS}

AUTHOR = "AI Document Generator"
DATE_STR = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")

# ============================================================
# DEAL PARAMETERS — Graham Companies $28M Refinance
# ============================================================

PLACEHOLDER_VALUES = {
    # --- Deal Identification ---
    "[BORROWER NAME]": "TGC Governors Square, LLC, TGC Parkside, LLC, and TGC Enrichment Center, LLC",
    "[BORROWER NAME CAPS]": "TGC GOVERNORS SQUARE, LLC, TGC PARKSIDE, LLC, AND TGC ENRICHMENT CENTER, LLC",
    "[BORROWER STATE]": "Florida",
    "[BORROWER ENTITY TYPE]": "limited liability company",
    "[RELATIONSHIP CONTACT]": "The Graham Companies",

    # --- Loan Amount ---
    "[$LOAN AMOUNT]": "$28,000,000.00",
    "[$LOAN AMOUNT WORDS]": "Twenty-Eight Million and No/100",
    "[EXISTING LENDER]": "BankUnited",
    "[PURPOSE ADD INFO]": "pay off the existing indebtedness owed to BankUnited",

    # --- Interest Rate ---
    "[FIXED RATE]": "5.65",
    "[FIXED RATE WORDS]": "five and sixty-five hundredths",
    "[INITIAL FIXED TERM]": "5",
    "[INITIAL FIXED TERM WORDS]": "five",
    "[MARGIN RATE]": "2.00",
    "[MARGIN RATE WORDS]": "two",
    "[FLOOR RATE]": "5.65",
    "[FLOOR RATE WORDS]": "five and sixty-five hundredths",

    # --- Term and Repayment ---
    "[TERM]": "15",
    "[TERM WORDS]": "fifteen",
    "[AMORTIZATION PERIOD]": "30",
    "[AMORTIZATION PERIOD WORDS]": "thirty",

    # --- Prepayment ---
    "[PREPAYMENT PERCENTAGE]": "0.25",
    "[PREPAYMENT PERCENTAGE WORDS]": "one-quarter of one",
    "[PREPAYMENT TERM]": "10",
    "[PREPAYMENT TERM WORDS]": "ten",

    # --- Guaranty ---
    "[EG NAME]": "Graham Group Holdings, Inc.",
    "[EG STATE]": "Florida",
    "[EG ENTITY TYPE]": "corporation",
    "[G NAME]": "Graham Group Holdings, Inc.",
    "[ENTITY NAME]": "Graham Group Holdings, Inc.",
    "[ENTITY STATE]": "Florida",
    "[ENTITY ENTITY TYPE]": "corporation",

    # --- Covenants ---
    "[DSCR COVENANT RATE]": "1.25",
    "[DSCR RATIO]": "1.25",
    "[DSCR MIN MGMT FEE]": "5",
    "[DSCR MIN MGMT FEE WORDS]": "five",
    "[LTV RATIO]": "65",
    "[LTV RATIO WORDS]": "sixty-five",

    # --- Property ---
    "[PROPERTY DESCRIPTION]": "a portfolio of four (4) office complexes consisting of seven (7) buildings totaling approximately 277,654 square feet",
    "[PROPERTY ADDRESS]": "various addresses in Miami Lakes, Miami-Dade County, Florida",
    "[PROPERTY COUNTY]": "Miami-Dade",

    # --- Bank Personnel ---
    "[SENIOR VP NAME]": "Wayne Smith",
    "[BANK OFFICER NAME]": "Jesus R. Garcia",

    # --- Dates and Fees ---
    "[COMMITMENT DATE]": "March ___, 2026",
    "[CLOSING DATE]": "[CLOSING DATE — not specified in CAS]",
    "[COMMITMENT FEE %]": "0.50",
    "[COMMITMENT FEE % WORDS]": "one-half of one percent (0.50%)",

    # --- Signature Blocks (EXTERNAL INPUT REQUIRED) ---
    "[BORROWER SIG 1 NAME]": "[EXTERNAL INPUT REQUIRED]",
    "[BORROWER SIG 1 TITLE]": "[EXTERNAL INPUT REQUIRED]",
    "[BORROWER SIG 1 ENTITY NAME]": "TGC LOC, LLC",
    "[BORROWER SIG 1 ENTITY TYPE]": "limited liability company",
    "[BORROWER SIG 1 ENTITY STATE]": "Florida",
    "[BORROWER SIG 1 RELATIONSHIP]": "Manager",
    "[BORROWER SIG 2 NAME]": "[EXTERNAL INPUT REQUIRED]",
    "[BORROWER SIG 2 TITLE]": "[EXTERNAL INPUT REQUIRED]",
    "[BORROWER SIG 2 ENTITY NAME]": "The Graham Companies",
    "[BORROWER SIG 2 ENTITY TYPE]": "corporation",
    "[BORROWER SIG 2 ENTITY STATE]": "Florida",
    "[BORROWER SIG 2 RELATIONSHIP]": "Manager",
    "[BORROWER SIG 3 NAME]": "[EXTERNAL INPUT REQUIRED]",
    "[BORROWER SIG 3 TITLE]": "[EXTERNAL INPUT REQUIRED]",
    "[ENTITY GUARANTOR SIG ONE INDY]": "[EXTERNAL INPUT REQUIRED]",
    "[ENTITY GUARANTOR SIG ONE INDY TITLE]": "[EXTERNAL INPUT REQUIRED]",
    "[ENTITY GUARANTOR SIG ONE ENTITY NAME]": "[EXTERNAL INPUT REQUIRED]",
    "[ENTITY GUARANTOR SIG ONE ENTITY TYPE]": "[EXTERNAL INPUT REQUIRED]",
    "[ENTITY GUARANTOR SIG ONE ENTITY STATE]": "[EXTERNAL INPUT REQUIRED]",
    "[ENTITY GUARANTOR SIG ONE ENTITY RELATIONSHIP]": "[EXTERNAL INPUT REQUIRED]",
    "[ENTITY GUARANTOR SIG TWO INDY]": "[EXTERNAL INPUT REQUIRED]",
    "[ENTITY GUARANTOR SIG TWO INDY TITLE]": "[EXTERNAL INPUT REQUIRED]",
    "[ENTITY GUARANTOR SIG TWO ENTITY NAME]": "[EXTERNAL INPUT REQUIRED]",
    "[ENTITY GUARANTOR SIG TWO ENTITY TYPE]": "[EXTERNAL INPUT REQUIRED]",
    "[ENTITY GUARANTOR SIG TWO ENTITY STATE]": "[EXTERNAL INPUT REQUIRED]",
    "[ENTITY GUARANTOR SIG TWO ENTITY RELATIONSHIP]": "[EXTERNAL INPUT REQUIRED]",
    "[ENTITY GUARANTOR SIG THREE ENTITY INDY]": "[EXTERNAL INPUT REQUIRED]",
    "[ENTITY GUARANTOR SIG THREE ENTITY INDY TITLE]": "[EXTERNAL INPUT REQUIRED]",

    # --- Items in conditional blocks that will be deleted ---
    # (included for completeness; these won't be reached in the output)
    "[BAD BOY GUARANTOR NAME]": "N/A",
    "[PERSON NAME]": "N/A",
    "[TG NAME]": "N/A",
    "[TRUST NAME]": "N/A",
    "[TRUST TRUST DATE]": "N/A",
    "[TRUST TRUSTEE NAME]": "N/A",
    "[$EXISTING BALANCE]": "N/A",
    "[$EXISTING BALANCE WORDS]": "N/A",
    "[$ORIGINAL LOAN AMOUNT]": "N/A",
    "[$FUTURE ADVANCE AMOUNT]": "N/A",
    "[$FUTURE ADVANCE AMOUNT WORDS]": "N/A",
    "[$FUTURE ADVANCE AMOUNT 2]": "N/A",
    "[$FUTURE ADVANCE AMOUNT 2 WORDS]": "N/A",
    "[$HOLDBACK AMOUNT]": "N/A",
    "[$HOLDBACK AMOUNT WORDS]": "N/A",
    "[HOLDBACK CONDITIONS]": "N/A",
    "[HOLDBACK CONDITIONS WORDS]": "N/A",
    "[$LOAN AMOUNT 2]": "N/A",
    "[$LOAN AMOUNT 2 WORDS]": "N/A",
    "[IO MONTHS]": "N/A",
    "[IO MONTHS WORDS]": "N/A",
    "[EXTENSION TERM]": "N/A",
    "[EXTENSION TERM WORDS]": "N/A",
    "[EXTENSION PERIOD]": "N/A",
    "[EXTENSION OPTIONS]": "N/A",
    "[EXTENSION OPTIONS WORDS]": "N/A",
    "[CONSTRUCTION TERM]": "N/A",
    "[CONSTRUCTION TERM WORDS]": "N/A",
    "[PERMANENT TERM]": "N/A",
    "[PERMANENT TERM WORDS]": "N/A",
    "[RATE SPREAD]": "N/A",
    "[DSCR START DATE]": "N/A",
    "[DSCR ADJUSTMENT BASIS]": "N/A",
    "[LTP RATIO]": "N/A",
    "[LTP RATIO WORDS]": "N/A",
    "[LTC RATIO]": "N/A",
    "[LTC RATIO WORDS]": "N/A",
    "[LTV MAINTENANCE RATIO]": "65",
    "[LTV MAINTENANCE RATIO WORDS]": "sixty-five",
    "[RESERVE FEE]": "4",
    "[RESERVE FEE WORDS]": "four",
    "[RESERVE MONTHS]": "N/A",
    "[RESERVE MONTHS WORDS]": "N/A",
    "[$STABILIZATION RESERVE AMOUNT]": "N/A",
    "[INTEREST RESERVE MONTHS]": "N/A",
    "[INTEREST RESERVE MONTHS WORDS]": "N/A",
    "[INTEREST RESERVE FLAG]": "N/A",
    "[EQUITY REQUIREMENT]": "N/A",
    "[EQUITY REQUIREMENT WORDS]": "N/A",
    "[FRANCHISOR NAME]": "N/A",
    "[CROSS BORROWER]": "N/A",
    "[CROSS PROPERTY]": "N/A",
    "[REMAINING PROCEEDS USE]": "fund related transaction costs",

    # --- Article ---
    "[a/an]": "a",
}

# ============================================================
# CONDITIONAL DECISIONS
# Maps each IF label to True (keep content) or False (delete content)
# ============================================================

CONDITION_KEEPS = {
    # --- Vowel checks (a/an article for state names) ---
    "BORROWER STATE[0]|LOWER IN [A, E, I, O, ]": False,       # Florida → F → not vowel
    "NOT BORROWER STATE[0]|LOWER IN ['A', 'E', 'I', 'O', ]": True,
    'BORROWER SIG ONE ENTITY STATE[0]|LOWER IN [A, E, I, O, ]': False,   # assume Florida
    "NOT BORROWER SIG ONE ENTITY STATE[0]|LOWER IN ['A', 'E', 'I', 'O', ]": True,
    'BORROWER SIG TWO ENTITY STATE[0]|LOWER IN [A, E, I, O, ]': False,
    "NOT BORROWER SIG TWO ENTITY STATE[0]|LOWER IN ['A', 'E', 'I', 'O', ]": True,

    # --- Borrower state existence ---
    "BORROWER STATE": True,
    "NOT BORROWER STATE": False,

    # --- New/Existing Loan ---
    "NEW LOAN": True,
    'NEW LOAN : " NEW LOAN"': True,
    'NEW LOAN : "NEW LOAN"': True,
    'NEW LOAN : "EXISTING LOAN"': False,
    'NEW LOAN : "EXISTING LOAN" AND NOT FUTURE ADVANCE': False,
    "EXISTING LOAN": False,
    "(NOT NEW LOAN IS NL AND FUTURE ADVANCE) OR NEW LOAN": True,
    "EXISTING LOAN AND FUTURE ADVANCE AND BASIS IS FUTURE ADVANCE": False,
    "EXISTING LOAN AND FUTURE ADVANCE AND BASIS IS LOAN AMOUNT": False,

    # --- Holdback ---
    "HOLDBACK": False,
    'HOLDBACK BASIS : "EXACT AMOUNT"': False,
    'HOLDBACK BASIS : "CALCULATION"': False,

    # --- Extension ---
    "EXTENSION OPTION": False,
    "MULTIPLE EXTENSION OPTIONS": False,

    # --- Future Advance ---
    "FUTURE ADVANCE": False,

    # --- Loan Purpose ---
    'LOAN PURPOSE : "ACQUISITION"': False,
    'LOAN PURPOSE : "CONSTRUCTION"': False,
    'LOAN PURPOSE : "REFINANCE WITH EXISTING DEBT"': True,
    'LOAN PURPOSE : "REFINANCE FREE AND CLEAR"': False,
    'NOT LOAN PURPOSE == "CONSTRUCTION"': True,

    # --- Rate Structure ---
    'INTEREST RATE STRUCTURE : "FIXED"': False,
    'INTEREST RATE STRUCTURE : "FLOATING"': False,
    'INTEREST RATE STRUCTURE : "VARIABLE"': True,
    'INTEREST RATE STRUCTURE : "SWAP"': False,
    'NOT INTEREST RATE STRUCTURE == "SWAP"': True,
    "FLOATING OR VARIABLE RATE": True,

    # --- Index ---
    'INDEX : "SOFR"': True,
    'INDEX : "PRIME"': False,

    # --- Rate details ---
    "FIXED RATE KNOWN": True,
    "FIXED RATE TBD": False,
    "INITIAL RATE KNOWN": True,
    "INITIAL RATE TBD": False,
    "INITIAL FIXED > 4 YEARS": True,
    "MARGIN": True,
    "FLOOR RATE": True,
    "FLOOR RATE KNOWN": True,
    "FLOOR RATE TBD": False,
    "SINGLE RATE ADJUSTMENT": False,
    "MULTIPLE RATE ADJUSTMENTS": True,

    # --- Interest Only ---
    "INTEREST ONLY": False,
    "NO INTEREST ONLY": True,

    # --- Fee ---
    "COMMITMENT FEE": False,
    "UNDERWRITING FEE": True,
    "FEE ON LOAN AMOUNT": True,
    "FEE ON FUTURE ADVANCE": False,

    # --- Prepayment ---
    "PREPAYMENT PENALTY": True,
    "NO PREPAYMENT PENALTY": False,
    'PREPAYMENT PENALTY TYPE : "BONA FIDE"': True,
    'PREPAYMENT PENALTY TYPE : "REFINANCE"': False,
    "PENALTY FULL TERM": False,
    "PENALTY PARTIAL TERM": True,

    # --- Guarantors ---
    "GUARANTOR SECTION": True,
    "GUARANTOR": True,
    "HAS GUARANTORS": True,
    "NO GUARANTORS": False,
    "PERSONAL GUARANTORS": False,
    "ENTITY GUARANTORS": True,
    "TRUST GUARANTORS": False,
    "BAD BOY GUARANTOR": False,
    "MULTIPLE GUARANTORS": False,
    "MULTIPLE PERSONAL GUARANTORS": False,
    "MULTIPLE ENTITY GUARANTORS": False,
    "MULTIPLE TRUST GUARANTORS": False,
    "EXISTING OWNERSHIP": False,
    "NOT EXISTING OWNERSHIP": True,

    # --- DSCR ---
    "DSCR COVENANT": True,
    "DSCR ANNUALLY": True,
    'DSCR BASIS : "INCOME AND EXPENSE STATEMENTS"': False,
    'DSCR BASIS : "COMPANY TAX RETURNS"': True,
    'DSCR START : "PARTICULAR YEAR"': False,
    "DSCR HYPOTHETICAL AMORTIZATION": False,
    "MIN DSCR ADJUSTMENT BASIS": False,
    "NOI-BASED DSCR": True,
    "NON-NOI DSCR": False,

    # --- Escrow ---
    'TAX ESCROW : "NO ESCROW"': True,
    'TAX ESCROW : "TAX AND FLOOD INSURANCE"': False,
    'TAX ESCROW : "TAX AND INSURANCE" OR TAX ESCROW : "TAX AND FLOOD INSURANCE"': False,
    'TAX ESCROW : "NO ESCROW DURING INTEREST ONLY PERIOD AND TAX AND INSURANCE ESCROW THEREAFTER"': False,

    # --- Other Covenants ---
    "CROSS DEFAULT": False,
    "CROSS LOAN NEW": False,
    "TENANT RESERVE": False,
    "LEASED PROPERTY": True,

    # --- Loan Amount Basis ---
    "LOAN AMOUNT STATED": True,
    "LOAN OVER $1M": True,
    "LOAN UNDER $1M": False,
    '"LTV" IN LOAN AMOUNT BASIS': True,
    '"LTV" NOT IN LOAN AMOUNT BASIS': False,
    '"DSCR" IN LOAN AMOUNT BASIS': False,
    '"DSCR" NOT IN LOAN AMOUNT BASIS AND LOAN PURPOSE != "CONSTRUCTION"': True,
    '"LOAN TO PURCHASE" IN LOAN AMOUNT BASIS': False,
    '"LOAN TO PURCHASE" NOT IN LOAN AMOUNT BASIS': True,
    '"LOAN TO PURCHASE" NOT IN LOAN AMOUNT BASIS AND "DSCR" NOT IN LOAN AMOUNT BASIS AND LOAN PURPOSE != "CONSTRUCTION"': True,

    # --- Property Conditions ---
    "CONDITION REPORTS": True,
    'PROPERTY CONDITION REPORTS : "FULL CONDITION"': True,
    'PROPERTY CONDITION REPORTS : "ROOF AND TERMITE" OR PROPERTY CONDITION REPORTS : "ROOF ONLY"': False,
    'NOT PROPERTY CONDITION REPORTS == "ROOF ONLY"': True,
    "ENVIRONMENTAL": True,
    "FRANCHISE": False,
    "STAR REPORTS": False,
    "STAR SEMI-ANNUAL": False,
    "BOND": False,
    "UCC REQUIRED": False,
    "UCC NOT REQUIRED": True,
    "RESERVE ACCOUNT": False,
    "STABILIZATION RESERVE": False,
    "INTEREST RESERVE": False,
    "GLOBAL CASH FLOW": False,
    "JV/LP AGREEMENTS": False,
    "PERMANENT PHASE": False,

    # --- Reporting ---
    "BORROWER OR ENTITY FINANCIALS": True,
    "BORROWER OR GUARANTOR TAX RETURNS": True,
    "RENT ROLL OR OPERATING STATEMENT": True,
    "BORROWER FINANCIALS": True,
    "BORROWER AND ENTITY FINANCIALS": True,
    "ENTITY GUARANTOR FINANCIALS": True,
    "BORROWER TAX RETURNS": True,
    "BORROWER AND GUARANTOR TAX RETURNS": True,
    "GUARANTOR TAX RETURNS": True,
    "TAX RETURN EXTEND C": False,
    "TAX RETURN EXTEND P": False,
    "OPERATING STATEMENT": True,
    "RENT ROLL": True,
    "RENT ROLL AND OPERATING STATEMENT": True,
    "BIZ INTERRUPTION INSURANCE": True,
    "PURPOSE ADDITIONAL INFO": False,

    # --- Bank Personnel ---
    'SENIOR VICE PRESIDENT : "WAYNE SMITH"': True,
    'SENIOR VICE PRESIDENT : "FARA KHAN"': False,
    'BANK OFFICER POSITION : "SVP"': True,

    # --- Signature Block Types ---
    "BORROWER SIG ONE TYPE :": False,          # Not blank
    "BORROWER SIG ONE TYPE: ENTITY": True,     # Entity signer
    "BORROWER SIG ONE TYPE: INDIVIDUAL": False,
    "BORROWER SIG TWO TYPE: ENTITY": True,
    "BORROWER SIG TWO TYPE: INDIVIDUAL": False,
    "ENTITY.GUARANTOR SIG ONE TYPE :": False,  # Not blank
    "ENTITY.GUARANTOR SIG ONE TYPE : ENTITY": True,
    "ENTITY.GUARANTOR SIG ONE TYPE : INDIVIDUAL": False,
    "ENTITY.GUARANTOR SIG TWO TYPE : ENTITY": True,
    "ENTITY.GUARANTOR SIG TWO TYPE : INDIVIDUAL": False,
    "BORROWER SIG ONE ENTITY STATE[0]": False,  # handled via vowel check
    "NOT BORROWER SIG ONE ENTITY STATE[0]": True,
    "BORROWER SIG TWO ENTITY STATE[0]": False,
    "NOT BORROWER SIG TWO ENTITY STATE[0]": True,
    "ENTITY.GUARANTOR SIG ONE ENTITY STATE[0]": False,
    "NOT ENTITY.GUARANTOR SIG ONE ENTITY STATE[0]": True,
    "ENTITY.GUARANTOR SIG TWO ENTITY STATE[0]": False,
    "NOT ENTITY.GUARANTOR SIG TWO ENTITY STATE[0]": True,
    "ENTITY.STATE[0]": False,
    "NOT ENTITY.STATE[0]": True,
    # Full vowel-check labels for entity guarantor state
    "ENTITY.STATE[0]|LOWER IN [A, E, I, O]": False,
    "NOT ENTITY.STATE[0]|LOWER IN ['A', 'E', 'I', 'O']": True,
    "ENTITY.GUARANTOR SIG ONE ENTITY STATE[0]|LOWER IN [A, E, I, O]": False,
    "NOT ENTITY.GUARANTOR SIG ONE ENTITY STATE[0]|LOWER IN ['A', 'E', 'I', 'O']": True,
    "ENTITY.GUARANTOR SIG TWO ENTITY STATE[0]|LOWER IN [A, E, I, O]": False,
    "NOT ENTITY.GUARANTOR SIG TWO ENTITY STATE[0]|LOWER IN ['A', 'E', 'I', 'O']": True,
    "ENTITY.STATE": True,
    "NOT ENTITY.STATE": False,

    # --- List punctuation (handled specially in FOR EACH) ---
    "LIST COMMA": True,   # Default: show comma (adjusted per item)
    "NOT LAST ITEM": True,  # Default: not last (adjusted per item)

    # --- Loan size ---
    "LOAN AMOUNT STATED": True,

    # --- Multiple folios ---
    "MULTIPLE FOLIOS": True,
}


def normalize_quotes(s):
    """Normalize curly/smart quotes to straight ASCII quotes."""
    s = s.replace("\u201c", '"').replace("\u201d", '"')  # double
    s = s.replace("\u2018", "'").replace("\u2019", "'")  # single
    return s


# Rebuild CONDITION_KEEPS with normalized keys
CONDITION_KEEPS = {normalize_quotes(k): v for k, v in CONDITION_KEEPS.items()}

# ============================================================
# FOR EACH DATA
# ============================================================

FOLIO_DATA = [
    {"folio_number": "32-2022-008-0010"},
    {"folio_number": "32-2022-008-0011"},
    {"folio_number": "32-2022-009-0030"},
    {"folio_number": "32-2022-009-0031"},
]

ENTITY_GUARANTOR_DATA = [
    {
        "name": "Graham Group Holdings, Inc.",
        "state": "Florida",
        "entity_type": "corporation",
    },
]

# ============================================================
# COMMENTS (edge cases and review items)
# ============================================================

COMMENTS_TO_ADD = [
    {
        "target_text": "TGC Governors Square, LLC, TGC Parkside, LLC, and TGC Enrichment Center, LLC",
        "comment": "EDGE CASE: Multiple borrowers — three borrowing entities (TGC Governors Square, TGC Parkside, TGC Enrichment Center) plus co-borrower (TGC LOC, LLC). Verify collective defined term 'Borrowers' and co-borrower naming. The ownership chain is: Graham Group Holdings Inc → The Graham Companies → TGC LOC LLC → [three borrowers]. NOTE: For multiple borrowers, add 'each' before 'a Florida limited liability company' in the RE line, Borrower definition, and borrower signature header.",
    },
    {
        "target_text": "Graham Group Holdings, Inc.",
        "comment": "REVIEW: Payment-only corporate guaranty — Graham Group Holdings, Inc. provides a PAYMENT ONLY guaranty limited to prompt and unconditional payment of Borrowers' Liabilities as they become due and payable through loan maturity. This is NOT a full recourse guaranty. Verify scope and whether additional carveout guaranty is required. POLICY EXCEPTION: Lack of significant and continuing guaranties (critical/reportable).",
        "first_only": True,
    },
    {
        "target_text": "Penalty:",
        "comment": "EDGE CASE: Multi-tier prepayment penalty — CAS specifies two tiers: (1) Years 1-10: 1/4% (0.25%), (2) Years 10-15: 1/8% (0.125%). Template handles single-tier only. The penalty language should be revised to reflect the tiered structure. Bona fide sale exception applies (arm's length sale to third party). No penalty if prepaid in full during last 90 days of the term.",
        "first_only": True,
    },
    {
        "target_text": "5.65",
        "comment": "REVIEW: Variable rate with 5-year repricing — Initial rate 5.65% fixed for first 5 years, then repriced every 5 years to 1-Month CME Term SOFR + 2.00%, with floor of 5.65%. Verify adjustment dates, index, and floor against CAS. Rate adjustments at years 5 and 10.",
        "first_only": True,
    },
    {
        "target_text": "thirty (30)",
        "comment": "POLICY EXCEPTION: 30-year amortization exceeds 25-year bank policy maximum. Confirmed as approved exception in CAS.",
        "first_only": True,
    },
    {
        "target_text": "BankUnited",
        "comment": "REVIEW: Portfolio refinance — Loan proceeds used to pay off existing debt at BankUnited. Four office complexes (7 buildings), 277,654 SF total, 67% occupied. Verify all properties included and collateral descriptions.",
        "first_only": True,
    },
    {
        "target_text": "does not require",
        "comment": "CONFIRM: UCC requirement not specified in CAS — defaulted to 'does not require'. Verify with attorney.",
        "first_only": True,
    },
    {
        "target_text": "CLOSING DATE",
        "comment": "CONFIRM: Closing date not specified in CAS. Attorney must provide.",
        "first_only": True,
    },
    {
        "target_text": "EXTERNAL INPUT REQUIRED",
        "comment": "EXTERNAL INPUT REQUIRED: Signatory information (signing chain, individual names, titles) must be provided by attorney for all borrower and guarantor signature blocks.",
        "first_only": True,
    },
    {
        "target_text": "Underwriting",
        "comment": "REVIEW: CAS labels the fee as 'PRICING – FEE: (ORIG.) ½%' — treated as origination/underwriting fee (not commitment fee). Verify correct fee characterization.",
        "first_only": True,
    },
    {
        "target_text": "a portfolio of four",
        "comment": "EDGE CASE: Multiple properties — four office complexes in Miami Lakes secured by single loan. Verify each property description, address, and folio number. Properties: (1) Andrew Jackson Bldg, 8100 Governors Square Blvd; (2) Spessard Holland Office Bldg, 8000 Governors Square Blvd; (3) Parkside Corporate Center I-IV, 15280/15150/15050/15000 NW 79th Ct; (4) KinderCare Enrichment Center, 8001 Oak Lane.",
        "first_only": True,
    },
    {
        "target_text": "Deposit Accounts",
        "comment": "REVIEW: Operating account requirement waived per CAS — subject to Borrower maintaining a meaningful banking relationship at Ocean Bank. Confirm waiver language is acceptable.",
        "first_only": True,
    },
    {
        "target_text": "four percent (4%) reserve for capital repairs",
        "comment": "CONFIRM: Capital repairs reserve percentage (4%) is a standard assumption — not explicitly stated in CAS. Verify with RM or use actual percentage if different.",
        "first_only": True,
    },
]

# ============================================================
# XML UTILITIES
# ============================================================


class RevIdGen:
    """Generate sequential revision IDs for tracked changes."""
    def __init__(self, start=1000):
        self._next = start

    def next(self):
        val = self._next
        self._next += 1
        return val


def w_elem(tag, attrib=None, nsmap=None):
    """Create an element in the w: namespace."""
    return etree.Element(f"{{{W_NS}}}{tag}", attrib=attrib or {}, nsmap=nsmap)


def w_sub(parent, tag, attrib=None):
    """Create a subelement in the w: namespace."""
    return etree.SubElement(parent, f"{{{W_NS}}}{tag}", attrib=attrib or {})


def get_para_text(para):
    """Get concatenated text from all runs in a paragraph."""
    texts = []
    for r in para.findall(f".//{{{W_NS}}}r"):
        t = r.find(f"{{{W_NS}}}t")
        if t is not None and t.text:
            texts.append(t.text)
    return "".join(texts)


def get_run_formatting(run):
    """Extract the rPr (run properties) element from a run, if any."""
    rpr = run.find(f"{{{W_NS}}}rPr")
    if rpr is not None:
        return copy.deepcopy(rpr)
    return None


# ============================================================
# CONDITIONAL RESOLUTION (text-level)
# ============================================================


def find_if_markers(text):
    """Find all [IF: ...] and [END IF: ...] markers in text, handling nested brackets."""
    markers = []
    i = 0
    while i < len(text):
        # Check for [IF: or [END IF:
        if text[i:i+5] == "[IF: " or text[i:i+9] == "[END IF: ":
            is_end = text[i:i+9] == "[END IF: "
            start = i
            depth = 0
            j = i
            found = False
            while j < len(text):
                if text[j] == "[":
                    depth += 1
                elif text[j] == "]":
                    depth -= 1
                    if depth == 0:
                        end = j + 1
                        marker_text = text[start:end]
                        if is_end:
                            label = marker_text[9:-1]  # Strip [END IF: and ]
                        else:
                            label = marker_text[5:-1]  # Strip [IF: and ]
                        markers.append({
                            "start": start,
                            "end": end,
                            "label": normalize_quotes(label),
                            "is_end": is_end,
                            "text": marker_text,
                        })
                        found = True
                        break
                j += 1
            i = end if found else j + 1
        # Check for [FOR EACH: or [END FOR EACH:
        elif text[i:i+11] == "[FOR EACH: " or text[i:i+15] == "[END FOR EACH: ":
            is_end = text[i:i+15] == "[END FOR EACH: "
            start = i
            depth = 0
            j = i
            found = False
            while j < len(text):
                if text[j] == "[":
                    depth += 1
                elif text[j] == "]":
                    depth -= 1
                    if depth == 0:
                        end = j + 1
                        marker_text = text[start:end]
                        if is_end:
                            label = "FOR:" + marker_text[15:-1]
                        else:
                            label = "FOR:" + marker_text[11:-1]
                        markers.append({
                            "start": start,
                            "end": end,
                            "label": label,
                            "is_end": is_end,
                            "is_for": True,
                            "text": marker_text,
                        })
                        found = True
                        break
                j += 1
            i = end if found else j + 1
        else:
            i += 1
    return markers


def resolve_inline_conditionals(text, condition_keeps):
    """Resolve all inline [IF: X]...[END IF: X] pairs where both markers are in the same text.
    Processes innermost pairs first (no nesting inside them)."""
    max_iterations = 200
    iteration = 0

    while iteration < max_iterations:
        iteration += 1
        markers = find_if_markers(text)

        # Filter to only IF/END IF markers (not FOR EACH)
        if_markers = [m for m in markers if not m.get("is_for")]
        if not if_markers:
            break

        # Find innermost pair: an IF marker followed by its matching END IF
        # with no other IF markers between them
        resolved = False
        for i, m in enumerate(if_markers):
            if m["is_end"]:
                continue
            label = m["label"]
            # Look for matching END IF
            for j in range(i + 1, len(if_markers)):
                if if_markers[j]["label"] == label and if_markers[j]["is_end"]:
                    # Check no nested IF between i and j
                    has_nested = False
                    for k in range(i + 1, j):
                        if not if_markers[k]["is_end"]:
                            has_nested = True
                            break
                    if not has_nested:
                        # Resolve this pair
                        start_m = m
                        end_m = if_markers[j]
                        keep = condition_keeps.get(label)
                        if keep is None:
                            # Try partial match or default to True with warning
                            print(f"  WARNING: Unknown condition label: '{label}' — defaulting to KEEP")
                            keep = True
                        if keep:
                            # Remove markers, keep content between
                            content = text[start_m["end"]:end_m["start"]]
                            text = text[:start_m["start"]] + content + text[end_m["end"]:]
                        else:
                            # Remove markers + content
                            text = text[:start_m["start"]] + text[end_m["end"]:]
                        resolved = True
                        break
            if resolved:
                break

        if not resolved:
            break

    return text


def resolve_inline_for_each(text, collection_name, items):
    """Resolve inline [FOR EACH: X]...[END FOR EACH: X] in text."""
    for_label = f"FOR:{collection_name}"
    markers = find_if_markers(text)
    for_markers = [m for m in markers if m.get("is_for") and m["label"] == for_label]

    if len(for_markers) < 2:
        return text

    start_m = None
    end_m = None
    for m in for_markers:
        if not m["is_end"]:
            start_m = m
        elif m["is_end"] and start_m is not None:
            end_m = m
            break

    if not start_m or not end_m:
        return text

    template_content = text[start_m["end"]:end_m["start"]]

    if not items:
        # Empty collection: remove everything
        return text[:start_m["start"]] + text[end_m["end"]:]

    # Expand for each item
    expanded_parts = []
    for idx, item in enumerate(items):
        part = template_content
        # Replace item-level placeholders
        for key, val in item.items():
            placeholder = f"[{key.upper().replace('_', ' ')}]"
            part = part.replace(placeholder, val)
        # Handle list punctuation
        is_last = (idx == len(items) - 1)
        # Resolve LIST COMMA and NOT LAST ITEM inline
        if is_last:
            part = resolve_inline_conditionals(part, {
                **CONDITION_KEEPS,
                "LIST COMMA": False,
                "NOT LAST ITEM": False,
            })
        else:
            part = resolve_inline_conditionals(part, {
                **CONDITION_KEEPS,
                "LIST COMMA": True,
                "NOT LAST ITEM": True,
            })
        expanded_parts.append(part)

    expanded = "".join(expanded_parts)
    return text[:start_m["start"]] + expanded + text[end_m["end"]:]


# ============================================================
# TRACKED CHANGES XML
# ============================================================


def create_del_run(text_content, rpr_elem, rev_id, author=AUTHOR, date=DATE_STR):
    """Create a w:del element wrapping a run with delText."""
    del_elem = w_elem("del", {
        f"{{{W_NS}}}id": str(rev_id),
        f"{{{W_NS}}}author": author,
        f"{{{W_NS}}}date": date,
    })
    run = w_sub(del_elem, "r")
    if rpr_elem is not None:
        run.append(copy.deepcopy(rpr_elem))
    dt = w_sub(run, "delText")
    dt.set(f"{{{XML_NS}}}space", "preserve")
    dt.text = text_content
    return del_elem


def create_ins_run(text_content, rpr_elem, rev_id, author=AUTHOR, date=DATE_STR):
    """Create a w:ins element wrapping a run with text."""
    ins_elem = w_elem("ins", {
        f"{{{W_NS}}}id": str(rev_id),
        f"{{{W_NS}}}author": author,
        f"{{{W_NS}}}date": date,
    })
    run = w_sub(ins_elem, "r")
    if rpr_elem is not None:
        run.append(copy.deepcopy(rpr_elem))
    t = w_sub(run, "t")
    t.set(f"{{{XML_NS}}}space", "preserve")
    t.text = text_content
    return ins_elem


def tracked_delete_paragraph(para, rev_gen):
    """Wrap all runs in a paragraph with w:del for tracked deletion."""
    runs = para.findall(f"{{{W_NS}}}r")
    for run in runs:
        rev_id = rev_gen.next()
        # Get run properties
        rpr = run.find(f"{{{W_NS}}}rPr")
        t = run.find(f"{{{W_NS}}}t")
        text_content = t.text if t is not None and t.text else ""

        # Create del element
        del_elem = create_del_run(text_content, rpr, rev_id)

        # Replace the run with the del element
        parent = run.getparent()
        idx = list(parent).index(run)
        parent.remove(run)
        parent.insert(idx, del_elem)

    # Also mark paragraph mark as deleted
    ppr = para.find(f"{{{W_NS}}}pPr")
    if ppr is None:
        ppr = w_sub(para, "pPr")
        para.insert(0, ppr)
    rpr_in_ppr = ppr.find(f"{{{W_NS}}}rPr")
    if rpr_in_ppr is None:
        rpr_in_ppr = w_sub(ppr, "rPr")
    del_mark = w_sub(rpr_in_ppr, "del", {
        f"{{{W_NS}}}id": str(rev_gen.next()),
        f"{{{W_NS}}}author": AUTHOR,
        f"{{{W_NS}}}date": DATE_STR,
    })


def apply_replacement_to_paragraph(para, old_text, new_text, rev_gen):
    """Apply a tracked replacement (del old + ins new) to a paragraph.
    This is a simplified approach: replaces the entire paragraph text."""
    runs = para.findall(f"{{{W_NS}}}r")
    if not runs:
        return

    # Get formatting from first run
    first_rpr = get_run_formatting(runs[0])

    # Remove all existing runs
    for run in runs:
        para.remove(run)

    # Find insertion point (after pPr if it exists)
    ppr = para.find(f"{{{W_NS}}}pPr")
    insert_idx = list(para).index(ppr) + 1 if ppr is not None else 0

    # Create del element for old text
    del_elem = create_del_run(old_text, first_rpr, rev_gen.next())
    para.insert(insert_idx, del_elem)

    # Create ins element for new text
    ins_elem = create_ins_run(new_text, first_rpr, rev_gen.next())
    para.insert(insert_idx + 1, ins_elem)


# ============================================================
# WORD COMMENTS
# ============================================================


def create_comments_xml(comments_list):
    """Create the word/comments.xml content."""
    nsmap = {
        "w": W_NS,
        "r": R_NS,
        "w14": "http://schemas.microsoft.com/office/word/2010/wordml",
    }
    comments_root = etree.Element(f"{{{W_NS}}}comments", nsmap=nsmap)

    for idx, comment_data in enumerate(comments_list):
        comment_id = str(comment_data["id"])
        comment_elem = w_sub(comments_root, "comment", {
            f"{{{W_NS}}}id": comment_id,
            f"{{{W_NS}}}author": AUTHOR,
            f"{{{W_NS}}}date": DATE_STR,
            f"{{{W_NS}}}initials": "AI",
        })
        p = w_sub(comment_elem, "p")
        # Annotation ref run
        ref_run = w_sub(p, "r")
        ref_rpr = w_sub(ref_run, "rPr")
        w_sub(ref_rpr, "rStyle", {f"{{{W_NS}}}val": "CommentReference"})
        w_sub(ref_run, "annotationRef")
        # Comment text run
        text_run = w_sub(p, "r")
        t = w_sub(text_run, "t")
        t.set(f"{{{XML_NS}}}space", "preserve")
        t.text = comment_data["text"]

    return comments_root


def add_comment_ref_to_paragraph(para, comment_id):
    """Add commentRangeStart, commentRangeEnd, and commentReference to a paragraph."""
    cid = str(comment_id)

    # Add commentRangeStart at the beginning (after pPr)
    range_start = w_elem("commentRangeStart", {f"{{{W_NS}}}id": cid})
    ppr = para.find(f"{{{W_NS}}}pPr")
    if ppr is not None:
        idx = list(para).index(ppr) + 1
    else:
        idx = 0
    para.insert(idx, range_start)

    # Add commentRangeEnd and reference at the end
    range_end = w_elem("commentRangeEnd", {f"{{{W_NS}}}id": cid})
    para.append(range_end)

    ref_run = w_elem("r")
    ref_rpr = w_sub(ref_run, "rPr")
    w_sub(ref_rpr, "rStyle", {f"{{{W_NS}}}val": "CommentReference"})
    w_sub(ref_run, "commentReference", {f"{{{W_NS}}}id": cid})
    para.append(ref_run)


# ============================================================
# MAIN PROCESSING
# ============================================================


def process_document(template_path, output_path):
    """Main processing function."""
    print(f"Opening template: {template_path}")

    # Read the template zip
    with zipfile.ZipFile(template_path, "r") as zin:
        file_contents = {}
        for name in zin.namelist():
            file_contents[name] = zin.read(name)

    # Parse document.xml
    doc_xml = file_contents["word/document.xml"]
    doc_tree = etree.fromstring(doc_xml)
    body = doc_tree.find(f"{{{W_NS}}}body")
    paras = body.findall(f"{{{W_NS}}}p")

    rev_gen = RevIdGen(start=1000)
    total_paras = len(paras)

    print(f"Total paragraphs: {total_paras}")

    # ---- PHASE 1: Get original text for each paragraph ----
    para_texts = []
    for p in paras:
        para_texts.append(get_para_text(p))

    # ---- PHASE 2: Resolve conditionals and placeholders at text level ----
    # Two-pass approach:
    #   Pass A: Walk paragraphs with stack to determine which paragraphs are in
    #           deleted multi-paragraph blocks. Also track unmatched markers.
    #   Pass B: For non-deleted paragraphs, resolve inline conditionals,
    #           strip trailing/leading content from partial-paragraph blocks,
    #           replace placeholders.

    resolved_texts = [""] * total_paras
    delete_flags = [False] * total_paras

    # --- Pass A-0: Handle multi-paragraph FOR EACH blocks ---
    # When a FOR EACH collection is empty, delete all paragraphs in the block.
    # When non-empty, strip the FOR EACH/END FOR EACH marker paragraphs only
    # (content paragraphs are kept and will have placeholders resolved in Pass B).
    for_each_collections = {
        "PERSONAL GUARANTORS": [],
        "ENTITY GUARANTORS": ENTITY_GUARANTOR_DATA,
        "TRUST GUARANTORS": [],
    }

    for collection_name, items in for_each_collections.items():
        start_marker = f"[FOR EACH: {collection_name}]"
        end_marker = f"[END FOR EACH: {collection_name}]"
        start_idx = None
        for pi, text in enumerate(para_texts):
            normalized = normalize_quotes(text.strip())
            # Only match standalone or near-standalone marker paragraphs
            # (skip inline markers embedded in content-heavy paragraphs)
            if start_marker in normalized and start_idx is None:
                # Check that this is a standalone marker paragraph, not inline
                marker_stripped = normalized.replace(start_marker, "").strip()
                # If removing the marker leaves very little text, it's standalone
                if len(marker_stripped) < 20:
                    start_idx = pi
            if end_marker in normalized and start_idx is not None and pi > start_idx:
                end_idx = pi
                if not items:
                    # Empty collection: delete all paragraphs from start to end (inclusive)
                    for di in range(start_idx, end_idx + 1):
                        delete_flags[di] = True
                else:
                    # Non-empty collection: delete marker-only paragraphs, keep content
                    if normalized == start_marker or para_texts[start_idx].strip() == start_marker:
                        delete_flags[start_idx] = True
                    # END FOR EACH paragraph may contain other markers too; just strip the FOR EACH part
                    end_text = para_texts[end_idx].strip()
                    end_normalized = normalize_quotes(end_text)
                    if end_normalized == end_marker:
                        delete_flags[end_idx] = True
                    # else: leave for inline processing (has other markers)
                start_idx = None  # Reset for next block
                break

    # --- Pass A: Stack-based multi-paragraph block tracking ---
    condition_stack = []  # (label, keep_bool)
    deletion_depth = 0

    # For each paragraph, record its unmatched markers for Pass B
    para_unmatched_starts = [[] for _ in range(total_paras)]
    para_unmatched_ends = [[] for _ in range(total_paras)]

    for i, text in enumerate(para_texts):
        markers_in_para = find_if_markers(text)
        if_starts = [m for m in markers_in_para if not m["is_end"] and not m.get("is_for")]
        if_ends = [m for m in markers_in_para if m["is_end"] and not m.get("is_for")]

        # Match IF starts with END IFs in the same paragraph (inline pairs)
        matched_starts = set()
        matched_ends = set()
        for si, s in enumerate(if_starts):
            for ei, e in enumerate(if_ends):
                if e["label"] == s["label"] and ei not in matched_ends and e["start"] > s["start"]:
                    matched_starts.add(si)
                    matched_ends.add(ei)
                    break

        unmatched_starts = [s for si, s in enumerate(if_starts) if si not in matched_starts]
        unmatched_ends = [e for ei, e in enumerate(if_ends) if ei not in matched_ends]

        para_unmatched_starts[i] = unmatched_starts
        para_unmatched_ends[i] = unmatched_ends

        # Check deletion_depth BEFORE processing any END IFs for this paragraph.
        # This ensures that the END IF paragraph of a False block also gets deleted.
        if deletion_depth > 0:
            delete_flags[i] = True

        # Process unmatched END IFs (close blocks from previous paragraphs)
        for end_m in sorted(unmatched_ends, key=lambda x: x["start"]):
            label = end_m["label"]
            found = False
            for si in range(len(condition_stack) - 1, -1, -1):
                if condition_stack[si][0] == label:
                    was_delete = not condition_stack[si][1]
                    condition_stack.pop(si)
                    if was_delete:
                        deletion_depth -= 1
                    found = True
                    break
            if not found:
                print(f"  WARNING: Unmatched END IF at P{i}: '{label}'")

        # Process unmatched IF starts (open new blocks)
        for start_m in sorted(unmatched_starts, key=lambda x: x["start"]):
            label = start_m["label"]
            keep = CONDITION_KEEPS.get(label)
            if keep is None:
                print(f"  WARNING: Unknown label starting block at P{i}: '{label}' — defaulting to KEEP")
                keep = True
            condition_stack.append((label, keep))
            if not keep:
                deletion_depth += 1

    if condition_stack:
        print(f"  WARNING: {len(condition_stack)} unclosed conditional blocks at end of document")
        for label, keep in condition_stack:
            print(f"    '{label}' (keep={keep})")

    print(f"  Pass A: {sum(delete_flags)} paragraphs marked for block deletion")

    # --- Pass B: Resolve inline conditionals and placeholders ---
    for i, text in enumerate(para_texts):
        if delete_flags[i]:
            resolved_texts[i] = ""
            continue

        resolved = text

        # Strip content AFTER unmatched False IF starts
        # (these start blocks that span to the next paragraph)
        for start_m in sorted(para_unmatched_starts[i], key=lambda x: x["start"], reverse=True):
            label = start_m["label"]
            keep = CONDITION_KEEPS.get(label, True)
            if not keep:
                # Remove from [IF: ...] marker to end of text
                resolved = resolved[:start_m["start"]]
            else:
                # Remove just the [IF: ...] marker text (keep content after it)
                resolved = resolved[:start_m["start"]] + resolved[start_m["end"]:]

        # Strip content BEFORE unmatched END IF markers that closed False blocks
        for end_m in sorted(para_unmatched_ends[i], key=lambda x: x["start"]):
            label = end_m["label"]
            # Check if this END IF was for a False block by checking what was on the stack
            # We need to know if the block was False. Find from previous paragraphs.
            # Simple approach: look up the label in CONDITION_KEEPS
            keep = CONDITION_KEEPS.get(label, True)
            if not keep:
                # Remove from start of text to after [END IF: ...] marker
                resolved = resolved[end_m["end"]:]
                # Adjust positions of subsequent markers
                break  # Only handle the first one; remaining will be at wrong positions
            else:
                # Remove just the [END IF: ...] marker text
                resolved = resolved[:end_m["start"]] + resolved[end_m["end"]:]

        # Resolve inline FOR EACH loops FIRST (they handle their own
        # inline conditionals with per-item NOT LAST ITEM / LIST COMMA values)
        resolved = resolve_inline_for_each(resolved, "FOLIOS", [
            {"folio number": f["folio_number"]} for f in FOLIO_DATA
        ])
        resolved = resolve_inline_for_each(resolved, "PERSONAL GUARANTORS", [])
        resolved = resolve_inline_for_each(resolved, "ENTITY GUARANTORS", [
            {"eg name": g["name"], "entity name": g["name"],
             "eg state": g["state"], "entity state": g["state"],
             "eg entity type": g["entity_type"], "entity entity type": g["entity_type"]}
            for g in ENTITY_GUARANTOR_DATA
        ])
        resolved = resolve_inline_for_each(resolved, "TRUST GUARANTORS", [])

        # Resolve inline conditionals AFTER FOR EACH (so list punctuation
        # markers inside loops are handled by the loop, not by defaults)
        resolved = resolve_inline_conditionals(resolved, CONDITION_KEEPS)

        # Replace placeholders
        for placeholder, value in PLACEHOLDER_VALUES.items():
            if placeholder in resolved:
                resolved = resolved.replace(placeholder, value)

        # Strip any remaining FOR EACH markers
        resolved = re.sub(r"\[(?:END )?FOR EACH: [^\]]+\]", "", resolved)

        # Strip any remaining standalone IF/END IF markers that are now orphaned
        # (These are markers for True blocks whose pair was already processed)
        resolved = re.sub(r"\[(?:END )?IF: (?:[^\[\]]*|\[[^\]]*\])*\]", "", resolved)

        # Check if paragraph is now empty
        if not resolved.strip():
            delete_flags[i] = True
            resolved_texts[i] = ""
        else:
            resolved_texts[i] = resolved

    # ---- PHASE 3: Apply changes to XML ----
    print("Applying changes to XML...")

    deleted_count = 0
    replaced_count = 0
    unchanged_count = 0

    for i, para in enumerate(paras):
        if i >= len(delete_flags):
            break

        old_text = para_texts[i]
        new_text = resolved_texts[i]

        if delete_flags[i]:
            # Delete this paragraph via tracked changes
            tracked_delete_paragraph(para, rev_gen)
            deleted_count += 1
        elif old_text != new_text and new_text.strip():
            # Text changed — apply tracked replacement
            apply_replacement_to_paragraph(para, old_text, new_text, rev_gen)
            replaced_count += 1
        else:
            unchanged_count += 1

    print(f"  Deleted: {deleted_count} paragraphs")
    print(f"  Replaced: {replaced_count} paragraphs")
    print(f"  Unchanged: {unchanged_count} paragraphs")

    # ---- PHASE 4: Add comments ----
    print("Adding comments...")

    comment_records = []
    comment_id_counter = 500  # Start comment IDs at 500

    for comment_spec in COMMENTS_TO_ADD:
        target = comment_spec["target_text"]
        first_only = comment_spec.get("first_only", False)
        found = False

        for i, para in enumerate(paras):
            if delete_flags[i]:
                continue
            text = resolved_texts[i] if i < len(resolved_texts) else ""
            if target in text:
                cid = comment_id_counter
                comment_id_counter += 1
                comment_records.append({
                    "id": cid,
                    "text": comment_spec["comment"],
                })
                add_comment_ref_to_paragraph(para, cid)
                found = True
                if first_only:
                    break

        if not found:
            print(f"  Comment target not found: '{target[:50]}...'")

    print(f"  Added {len(comment_records)} comments")

    # Create comments.xml
    if comment_records:
        comments_xml = create_comments_xml(comment_records)
        comments_bytes = etree.tostring(
            comments_xml, xml_declaration=True, encoding="UTF-8", standalone=True, pretty_print=True
        )
        file_contents["word/comments.xml"] = comments_bytes

        # Update [Content_Types].xml
        ct_xml = etree.fromstring(file_contents["[Content_Types].xml"])
        ct_nsmap = ct_xml.nsmap
        ct_ns = ct_nsmap.get(None, CT_NS)
        # Add override for comments.xml
        override = etree.SubElement(ct_xml, f"{{{ct_ns}}}Override")
        override.set("PartName", "/word/comments.xml")
        override.set("ContentType",
                      "application/vnd.openxmlformats-officedocument.wordprocessingml.comments+xml")
        file_contents["[Content_Types].xml"] = etree.tostring(
            ct_xml, xml_declaration=True, encoding="UTF-8", standalone=True
        )

        # Update document.xml.rels
        rels_xml = etree.fromstring(file_contents["word/_rels/document.xml.rels"])
        rels_ns = rels_xml.nsmap.get(None, "http://schemas.openxmlformats.org/package/2006/relationships")
        rel = etree.SubElement(rels_xml, f"{{{rels_ns}}}Relationship")
        rel.set("Id", "rIdComments")
        rel.set("Type", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/comments")
        rel.set("Target", "comments.xml")
        file_contents["word/_rels/document.xml.rels"] = etree.tostring(
            rels_xml, xml_declaration=True, encoding="UTF-8", standalone=True
        )

    # ---- PHASE 5: Serialize and save ----
    # Update document.xml
    file_contents["word/document.xml"] = etree.tostring(
        doc_tree, xml_declaration=True, encoding="UTF-8", standalone=True
    )

    # Write output zip
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zout:
        for name, data in file_contents.items():
            zout.writestr(name, data)

    print(f"\nOutput saved to: {output_path}")

    # ---- PHASE 6: Verification ----
    # Count remaining placeholders and markers in output
    remaining_placeholders = 0
    remaining_if_markers = 0
    for i, text in enumerate(resolved_texts):
        if delete_flags[i]:
            continue
        phs = re.findall(r"\[[A-Z\$][A-Z0-9 \$%/]+\]", text)
        remaining_placeholders += len(phs)
        ifs = re.findall(r"\[(?:END )?IF:", text)
        remaining_if_markers += len(ifs)

    print(f"\nVerification:")
    print(f"  Remaining placeholders: {remaining_placeholders}")
    print(f"  Remaining IF markers: {remaining_if_markers}")

    if remaining_placeholders > 0:
        print("  Remaining placeholder details:")
        for i, text in enumerate(resolved_texts):
            if delete_flags[i]:
                continue
            phs = re.findall(r"\[[A-Z\$][A-Z0-9 \$%/]+\]", text)
            for ph in phs:
                print(f"    P{i}: {ph}")

    if remaining_if_markers > 0:
        print("  Remaining IF marker details:")
        for i, text in enumerate(resolved_texts):
            if delete_flags[i]:
                continue
            if "[IF:" in text or "[END IF:" in text:
                print(f"    P{i}: {text[:100]}...")


if __name__ == "__main__":
    template_path = "new_templates/Ocean Bank - Commitment Letter.docx"
    output_path = "output/Graham Companies - Commitment Letter.docx"
    process_document(template_path, output_path)
