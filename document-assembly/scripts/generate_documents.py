#!/usr/bin/env python3
"""
Generate a full set of Bank loan documents from maximum templates.
Graham Companies deal — $28,000,000 Refinance of portfolio from BankUnited.

This script:
1. Determines which documents to generate based on deal parameters
2. For each document: resolves conditionals, replaces placeholders, expands FOR EACH loops
3. Applies tracked changes (w:del / w:ins) for attorney review
4. Adds Word comments for edge cases and review items
5. Runs verification on each output

Reuses the proven engine from generate_commitment_letter.py, generalized for all templates.
"""

import argparse
import copy
import os
import re
import sys
import zipfile
from datetime import datetime
from lxml import etree

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


def normalize_quotes(s):
    """Normalize curly/smart quotes to straight ASCII quotes."""
    s = s.replace("\u201c", '"').replace("\u201d", '"')
    s = s.replace("\u2018", "'").replace("\u2019", "'")
    return s


# ============================================================
# DEAL PARAMETERS — Graham Companies $28M Refinance
# ============================================================

# Master placeholder values covering ALL templates.
# Shared across all documents — per-template overrides applied at runtime.
PLACEHOLDER_VALUES = {
    # --- Deal Identification ---
    "[BORROWER NAME]": "TGC Governors Square, LLC, TGC Parkside, LLC, and TGC Enrichment Center, LLC",
    "[BORROWER NAME CAPS]": "TGC GOVERNORS SQUARE, LLC, TGC PARKSIDE, LLC, AND TGC ENRICHMENT CENTER, LLC",
    "[BORROWER STATE]": "Florida",
    "[BORROWER ENTITY TYPE]": "limited liability company",
    "[RELATIONSHIP CONTACT]": "The Graham Companies",

    # --- Borrower Address ---
    "[BORROWER STREET ADDRESS]": "[BORROWER STREET ADDRESS — not in CAS]",
    "[BORROWER CITY]": "Miami Lakes",
    "[BORROWER MAILING STATE]": "Florida",
    "[BORROWER ZIP]": "[BORROWER ZIP — not in CAS]",

    # --- Loan Amount ---
    "[$LOAN AMOUNT]": "$28,000,000.00",
    "[$LOAN AMOUNT WORDS]": "Twenty-Eight Million and No/100",
    "[$LOAN AMOUNT DOUBLED]": "$56,000,000.00",
    "[$LOAN AMOUNT DOUBLED WORDS]": "Fifty-Six Million and No/100",
    "[EXISTING LENDER]": "BankUnited",
    "[PURPOSE ADD INFO]": "pay off the existing indebtedness owed to BankUnited",

    # --- Interest Rate ---
    "[FIXED RATE]": "5.65",
    "[FIXED RATE WORDS]": "five and sixty-five hundredths",
    "[INITIAL FIXED TERM]": "5",
    "[INITIAL FIXED TERM WORDS]": "five",
    "[INITIAL FIXED TERM DATE]": "[INITIAL FIXED TERM DATE — computed at closing]",
    "[MARGIN RATE]": "2.00",
    "[MARGIN RATE WORDS]": "two",
    "[FLOOR RATE]": "5.65",
    "[FLOOR RATE WORDS]": "five and sixty-five hundredths",
    "[INDEX]": "SOFR",
    "[RATE STRUCTURE]": "variable",

    # --- Term and Repayment ---
    "[TERM]": "15",
    "[TERM WORDS]": "fifteen",
    "[AMORTIZATION PERIOD]": "30",
    "[AMORTIZATION PERIOD WORDS]": "thirty",
    "[MATURITY DATE]": "[MATURITY DATE — computed at closing]",
    "[PAYMENT DATE]": "[PAYMENT DATE — computed at closing]",

    # --- Interest Only (not applicable for this deal) ---
    "[IO MONTHS]": "N/A",
    "[IO MONTHS WORDS]": "N/A",
    "[IO END DATE]": "N/A",

    # --- Extension (not applicable for this deal) ---
    "[EXTENSION TERM]": "N/A",
    "[EXTENSION TERM WORDS]": "N/A",
    "[EXTENSION PERIOD]": "N/A",
    "[EXTENSION OPTIONS]": "N/A",
    "[EXTENSION OPTIONS WORDS]": "N/A",
    "[EXTENDEDMATURITYDATE]": "N/A",

    # --- Prepayment ---
    "[PREPAYMENT PERCENTAGE]": "0.25",
    "[PREPAYMENT PERCENTAGE WORDS]": "one-quarter of one",
    "[PREPAYMENT TERM]": "10",
    "[PREPAYMENT TERM WORDS]": "ten",

    # --- Holdback (not applicable) ---
    "[$HOLDBACK AMOUNT]": "N/A",
    "[$HOLDBACK AMOUNT WORDS]": "N/A",
    "[HOLDBACK CONDITIONS]": "N/A",
    "[HOLDBACK CONDITIONS WORDS]": "N/A",
    "[$INITIAL FUNDING]": "$28,000,000.00",
    "[$INITIAL FUNDING WORDS]": "Twenty-Eight Million and No/100",

    # --- Future Advance (not applicable) ---
    "[$FUTURE ADVANCE AMOUNT]": "N/A",
    "[$FUTURE ADVANCE AMOUNT WORDS]": "N/A",
    "[$FUTURE ADVANCE AMOUNT 2]": "N/A",
    "[$FUTURE ADVANCE AMOUNT 2 WORDS]": "N/A",
    "[$LOAN AMOUNT 2]": "N/A",
    "[$LOAN AMOUNT 2 WORDS]": "N/A",
    "[$ORIGINAL LOAN AMOUNT]": "N/A",
    "[$ORIGINAL LOAN AMOUNT WORDS]": "N/A",

    # --- Existing Loan Reference ---
    "[ORIGINAL CLOSING DATE]": "[ORIGINAL CLOSING DATE — from BankUnited docs]",
    "[RECORDS BOOK NUMBER]": "[RECORDS BOOK NUMBER — from title search]",
    "[RECORDS MTG PAGE NUMBER]": "[RECORDS MTG PAGE NUMBER — from title search]",
    "[RECORDS ALR PAGE NUMBER]": "[RECORDS ALR PAGE NUMBER — from title search]",

    # --- Guaranty —- Entity guarantor (Graham Group Holdings, Inc.) ---
    "[GUARANTOR NAME]": "Graham Group Holdings, Inc.",
    "[GUARANTOR NAME CAPS]": "GRAHAM GROUP HOLDINGS, INC.",
    "[GUARANTOR ADDRESS]": "[GUARANTOR ADDRESS — not in CAS]",
    "[GUARANTOR ENTITY TYPE]": "corporation",
    "[GUARANTOR STATE]": "Florida",

    # Guarantor FOR EACH placeholders (entity guarantor loop)
    "[EG NAME]": "Graham Group Holdings, Inc.",
    "[EG STATE]": "Florida",
    "[EG ENTITY TYPE]": "corporation",
    "[G NAME]": "N/A",
    "[ENTITY NAME]": "Graham Group Holdings, Inc.",
    "[ENTITY STATE]": "Florida",
    "[ENTITY ENTITY TYPE]": "corporation",

    # Guarantor FOR EACH placeholders (personal/trust — empty for this deal)
    "[PERSON NAME]": "N/A",
    "[TG NAME]": "N/A",
    "[TRUST NAME]": "N/A",
    "[TRUST TRUST DATE]": "N/A",
    "[TRUST TRUSTEE NAME]": "N/A",
    "[TRUSTEE NAME CAPS]": "N/A",
    "[TRUST AGREEMENT DATE]": "N/A",
    "[BAD BOY GUARANTOR NAME]": "N/A",
    "[BAD BOY GUARANTOR NAME CAPS]": "N/A",
    "[NOTARIAL SEAL]": "N/A",

    # --- Guarantor Signature Blocks ---
    "[GUARANTOR SIG 1 NAME]": "[EXTERNAL INPUT REQUIRED]",
    "[GUARANTOR SIG 1 TITLE]": "[EXTERNAL INPUT REQUIRED]",
    "[GUARANTOR SIG 1 ENTITY NAME]": "[EXTERNAL INPUT REQUIRED]",
    "[GUARANTOR SIG 1 ENTITY TYPE]": "[EXTERNAL INPUT REQUIRED]",
    "[GUARANTOR SIG 1 ENTITY STATE]": "[EXTERNAL INPUT REQUIRED]",
    "[GUARANTOR SIG 1 RELATIONSHIP]": "[EXTERNAL INPUT REQUIRED]",
    "[GUARANTOR SIG 2 NAME]": "[EXTERNAL INPUT REQUIRED]",
    "[GUARANTOR SIG 2 TITLE]": "[EXTERNAL INPUT REQUIRED]",
    "[GUARANTOR SIG 2 ENTITY NAME]": "[EXTERNAL INPUT REQUIRED]",
    "[GUARANTOR SIG 2 ENTITY TYPE]": "[EXTERNAL INPUT REQUIRED]",
    "[GUARANTOR SIG 2 ENTITY STATE]": "[EXTERNAL INPUT REQUIRED]",
    "[GUARANTOR SIG 2 RELATIONSHIP]": "[EXTERNAL INPUT REQUIRED]",
    "[GUARANTOR SIG 3 NAME]": "[EXTERNAL INPUT REQUIRED]",
    "[GUARANTOR SIG 3 TITLE]": "[EXTERNAL INPUT REQUIRED]",

    # Entity guarantor sig placeholders in FOR EACH context (Cooperation, Post-Closing)
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

    # --- Covenants ---
    "[DSCR COVENANT RATE]": "1.25",
    "[DSCR RATIO]": "1.25",
    "[DSCR MIN MGMT FEE]": "5",
    "[DSCR MIN MGMT FEE WORDS]": "five",
    "[DSCR BASIS]": "company tax returns",
    "[DSCR START DATE]": "N/A",
    "[DSCR ADJUSTMENT BASIS]": "N/A",
    "[LTV RATIO]": "65",
    "[LTV RATIO WORDS]": "sixty-five",
    "[LTV MAINTENANCE RATIO]": "65",
    "[LTV MAINTENANCE RATIO WORDS]": "sixty-five",
    "[LTP RATIO]": "N/A",
    "[LTP RATIO WORDS]": "N/A",
    "[LTC RATIO]": "N/A",
    "[LTC RATIO WORDS]": "N/A",
    "[RESERVE FEE]": "4",
    "[RESERVE FEE WORDS]": "four",

    # --- Property ---
    "[PROPERTY DESCRIPTION]": "a portfolio of four (4) office complexes consisting of seven (7) buildings totaling approximately 277,654 square feet",
    "[PROPERTY ADDRESS]": "various addresses in Miami Lakes, Miami-Dade County, Florida",
    "[PROPERTY COUNTY]": "Miami-Dade",
    "[PROPERTY COUNTY CAPS]": "MIAMI-DADE",
    "[FOLIO NUMBER]": "See attached",
    "[TENANT]": "N/A",
    "[FRANCHISOR NAME]": "N/A",
    "[PREPARED BY]": "[PREPARED BY — attorney to provide]",

    # --- Bank Personnel ---
    "[SENIOR VP NAME]": "Wayne Smith",
    "[BANK OFFICER NAME]": "Jesus R. Garcia",
    "[BANK OFFICER POSITION]": "SVP",

    # --- Dates and Fees ---
    "[COMMITMENT DATE]": "March ___, 2026",
    "[CLOSING DATE]": "[CLOSING DATE — not specified in CAS]",
    "[COMMITMENT FEE %]": "0.50",
    "[COMMITMENT FEE % WORDS]": "one-half of one percent (0.50%)",

    # --- Reserves (not applicable) ---
    "[RESERVE MONTHS]": "N/A",
    "[RESERVE MONTHS WORDS]": "N/A",
    "[$STABILIZATION RESERVE AMOUNT]": "N/A",
    "[INTEREST RESERVE MONTHS]": "N/A",
    "[INTEREST RESERVE MONTHS WORDS]": "N/A",
    "[INTEREST RESERVE FLAG]": "N/A",
    "[EQUITY REQUIREMENT]": "N/A",
    "[EQUITY REQUIREMENT WORDS]": "N/A",
    "[CROSS BORROWER]": "N/A",
    "[CROSS PROPERTY]": "N/A",
    "[CROSS LOAN NEW]": "N/A",
    "[REMAINING PROCEEDS USE]": "fund related transaction costs",
    "[RATE SPREAD]": "N/A",

    # --- Borrower Signature Blocks ---
    "[BORROWER SIG 1 NAME]": "[EXTERNAL INPUT REQUIRED]",
    "[BORROWER SIG 1 TITLE]": "[EXTERNAL INPUT REQUIRED]",
    "[BORROWER SIG 1 ENTITY NAME]": "TGC LOC, LLC",
    "[BORROWER SIG 1 ENTITY TYPE]": "limited liability company",
    "[BORROWER SIG 1 ENTITY STATE]": "Florida",
    "[BORROWER SIG 1 RELATIONSHIP]": "Manager",
    "[BORROWER SIG 1 NAME CAPS]": "[EXTERNAL INPUT REQUIRED]",
    "[BORROWER SIG 2 NAME]": "[EXTERNAL INPUT REQUIRED]",
    "[BORROWER SIG 2 TITLE]": "[EXTERNAL INPUT REQUIRED]",
    "[BORROWER SIG 2 ENTITY NAME]": "The Graham Companies",
    "[BORROWER SIG 2 ENTITY NAME CAPS]": "THE GRAHAM COMPANIES",
    "[BORROWER SIG 2 ENTITY TYPE]": "corporation",
    "[BORROWER SIG 2 ENTITY STATE]": "Florida",
    "[BORROWER SIG 2 RELATIONSHIP]": "Manager",
    "[BORROWER SIG 2 NAME CAPS]": "[EXTERNAL INPUT REQUIRED]",
    "[BORROWER SIG 3 NAME]": "[EXTERNAL INPUT REQUIRED]",
    "[BORROWER SIG 3 NAME CAPS]": "[EXTERNAL INPUT REQUIRED]",
    "[BORROWER SIG 3 TITLE]": "[EXTERNAL INPUT REQUIRED]",

    # --- Article ---
    "[a/an]": "a",
}


# ============================================================
# CONDITIONAL DECISIONS — comprehensive for ALL templates
# Maps each IF label to True (keep content) or False (delete content)
# ============================================================

CONDITION_KEEPS = {
    # --- Borrower state existence ---
    "BORROWER HAS STATE": True,
    "NOT BORROWER HAS STATE": False,
    "BORROWER STATE": True,
    "NOT BORROWER STATE": False,

    # --- Vowel checks (a/an article) ---
    # Florida starts with "F" → not a vowel
    "BORROWER STATE STARTS WITH VOWEL": False,
    "NOT BORROWER STATE[0": True,     # else branch of vowel check
    "BORROWER SIG ONE ENTITY STATE STARTS WITH VOWEL": False,
    "NOT BORROWER SIG ONE ENTITY STATE[0": True,
    "BORROWER SIG TWO ENTITY STATE STARTS WITH VOWEL": False,
    "NOT BORROWER SIG TWO ENTITY STATE[0": True,
    # Entity guarantor vowel checks (Florida)
    "ENTITY STATE STARTS WITH VOWEL": False,
    "NOT ENTITY.STATE[0": True,
    "ENTITY GUARANTOR SIG ONE ENTITY STATE STARTS WITH VOWEL": False,
    "NOT ENTITY.GUARANTOR SIG ONE ENTITY STATE[0": True,
    "ENTITY GUARANTOR SIG TWO ENTITY STATE STARTS WITH VOWEL": False,
    "NOT ENTITY.GUARANTOR SIG TWO ENTITY STATE[0": True,

    # Full vowel-check else-branch labels (these appear in templates as-is)
    "NOT BORROWER STATE[0]|LOWER IN ['A', 'E', 'I', 'O', ]": True,
    "NOT BORROWER SIG ONE ENTITY STATE[0]|LOWER IN ['A', 'E', 'I', 'O', ]": True,
    "NOT BORROWER SIG TWO ENTITY STATE[0]|LOWER IN ['A', 'E', 'I', 'O', ]": True,
    "NOT ENTITY.STATE[0]|LOWER IN ['A', 'E', 'I', 'O']": True,
    "NOT ENTITY.GUARANTOR SIG ONE ENTITY STATE[0]|LOWER IN ['A', 'E', 'I', 'O']": True,
    "NOT ENTITY.GUARANTOR SIG TWO ENTITY STATE[0]|LOWER IN ['A', 'E', 'I', 'O']": True,
    # Positive vowel-check labels (for completeness)
    "BORROWER STATE[0]|LOWER IN [A, E, I, O, ]": False,
    "BORROWER SIG ONE ENTITY STATE[0]|LOWER IN [A, E, I, O, ]": False,
    "BORROWER SIG TWO ENTITY STATE[0]|LOWER IN [A, E, I, O, ]": False,
    "ENTITY.STATE[0]|LOWER IN [A, E, I, O]": False,
    "ENTITY.GUARANTOR SIG ONE ENTITY STATE[0]|LOWER IN [A, E, I, O]": False,
    "ENTITY.GUARANTOR SIG TWO ENTITY STATE[0]|LOWER IN [A, E, I, O]": False,

    # Entity state existence (Cooperation, Post-Closing FOR EACH context)
    "ENTITY HAS STATE": True,
    "NOT ENTITY HAS STATE": False,

    # --- New/Existing Loan ---
    "NEW LOAN": False,                     # This is an existing loan (refinance)
    "EXISTING LOAN": True,
    'NEW LOAN : "NEW LOAN"': False,
    'NEW LOAN : "EXISTING LOAN"': True,
    'NEW LOAN : " NEW LOAN"': False,

    # --- Holdback ---
    "HOLDBACK": False,

    # --- Extension ---
    "EXTENSION OPTION": False,
    'EXTENSION TERM PERIOD : "MONTHS"': False,
    'EXTENSION TERM PERIOD : "YEARS"': False,

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
    'INTEREST RATE STRUCTURE : "FLOATING" OR INTEREST RATE STRUCTURE : "VARIABLE"': True,
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

    # --- Line of Credit ---
    "LINE OF CREDIT": False,

    # --- Fee ---
    "COMMITMENT FEE": False,
    "UNDERWRITING FEE": True,
    "FEE ON LOAN AMOUNT": True,
    "FEE ON FUTURE ADVANCE": False,
    "BASIS IS LOAN AMOUNT": True,
    "BASIS IS FUTURE ADVANCE": False,

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
    "HAS GUARANTORS OR CROSS DEFAULT": True,
    "PERSONAL GUARANTORS": False,
    "ENTITY GUARANTORS": True,
    "TRUST GUARANTORS": False,
    "ENTITY OR TRUST GUARANTORS": True,
    "BAD BOY GUARANTOR": False,
    "MULTIPLE GUARANTORS": False,
    "MULTIPLE PERSONAL GUARANTORS": False,
    "MULTIPLE ENTITY GUARANTORS": False,
    "MULTIPLE TRUST GUARANTORS": False,
    "EXISTING OWNERSHIP": False,
    "NOT EXISTING OWNERSHIP": True,
    "PERSONAL GUARANTORS AND NO TRUST": False,
    "PERSONAL GUARANTORS COUNT == 0": True,  # No personal guarantors

    # --- Guarantor financials ---
    "ENTITY GUARANTOR FINANCIALS": True,
    "PERSONAL GUARANTOR FINANCIALS": False,
    "TRUST GUARANTOR FINANCIALS": False,
    "GUARANTOR TAX RETURNS": True,
    "GLOBAL CASH FLOW": False,

    # --- DSCR ---
    "DSCR COVENANT": True,
    "DSCR ANNUALLY": True,
    'DSCR BASIS : "INCOME AND EXPENSE STATEMENTS"': False,
    'DSCR BASIS : "COMPANY TAX RETURNS"': True,
    'DSCR START : "AT CLOSING"': False,
    'DSCR START : "PARTICULAR YEAR"': False,
    'DSCR START : "CONVERSION TO P AND I"': False,
    "DSCR HYPOTHETICAL AMORTIZATION": False,
    "MIN DSCR ADJUSTMENT BASIS": False,
    "NOI-BASED DSCR": True,
    "NON-NOI DSCR": False,

    # --- Escrow ---
    'TAX ESCROW : "NO ESCROW"': True,
    'TAX ESCROW : "TAX AND FLOOD INSURANCE"': False,
    'NOT TAX ESCROW == "TAX AND FLOOD INSURANCE"': True,
    'TAX ESCROW : "TAX AND INSURANCE" OR TAX ESCROW : "TAX AND FLOOD INSURANCE"': False,
    'TAX ESCROW : "NO ESCROW" OR TAX ESCROW : "NO ESCROW DURING INTEREST ONLY PERIOD AND TAX AND INSURANCE ESCROW THEREAFTER"': True,
    'TAX ESCROW : "NO ESCROW DURING INTEREST ONLY PERIOD AND TAX AND INSURANCE ESCROW THEREAFTER"': False,

    # --- Other Covenants ---
    "CROSS DEFAULT": False,
    "NO CROSS DEFAULT": True,
    "CROSS LOAN NEW": False,
    "TENANT RESERVE": False,
    "LEASED PROPERTY": True,

    # --- Loan Amount Basis ---
    "LOAN AMOUNT STATED": True,
    "LOAN AMOUNT ACTUAL": True,
    "NOT LOAN AMOUNT ACTUAL": False,
    "LOAN AMOUNT NOT STATED": False,
    "LOAN OVER $1M": True,
    "LOAN UNDER $1M": False,
    "LOAN OVER $500K": True,
    "LOAN UNDER $500K": False,
    '"LTV" IN LOAN AMOUNT BASIS': True,
    '"LTV" NOT IN LOAN AMOUNT BASIS': False,
    '"DSCR" IN LOAN AMOUNT BASIS': False,
    '"DSCR" NOT IN LOAN AMOUNT BASIS': True,
    '"LOAN TO PURCHASE" IN LOAN AMOUNT BASIS': False,
    '"LOAN TO PURCHASE" NOT IN LOAN AMOUNT BASIS': True,

    # --- Property Conditions ---
    "CONDITION REPORTS": True,
    'PROPERTY CONDITION REPORTS : "FULL CONDITION"': True,
    'PROPERTY CONDITION REPORTS : "ROOF AND TERMITE" OR PROPERTY CONDITION REPORTS : "ROOF ONLY"': False,
    'NOT PROPERTY CONDITION REPORTS == "ROOF ONLY"': True,
    "ENVIRONMENTAL": True,
    "FRANCHISE": False,
    "STAR REPORTS": False,
    "STAR SEMI-ANNUAL": False,
    "NOT STAR SEMI-ANNUAL": True,
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
    "BORROWER TAX RETURNS": True,
    "BORROWER AND GUARANTOR TAX RETURNS": True,
    "TAX EXTEND CORP": False,
    "TAX EXTEND PERSONAL": False,
    "OPERATING STATEMENT": True,
    "RENT ROLL": True,
    "RENT ROLL AND OPERATING STATEMENT": True,
    "BIZ INTERRUPTION INSURANCE": True,
    "PURPOSE ADDITIONAL INFO": False,

    # --- Loan amount combined conditions ---
    '"DSCR" NOT IN LOAN AMOUNT BASIS AND LOAN PURPOSE != "CONSTRUCTION"': True,
    '"LOAN TO PURCHASE" NOT IN LOAN AMOUNT BASIS AND "DSCR" NOT IN LOAN AMOUNT BASIS AND LOAN PURPOSE != "CONSTRUCTION"': True,

    # --- Borrower Signature Block Types ---
    # For Graham Companies: Entity → Entity → Individual
    "BORROWER SIG ONE TYPE: BLANK": False,
    "BORROWER SIG ONE TYPE: ENTITY": True,
    "BORROWER SIG ONE TYPE: INDIVIDUAL": False,
    "BORROWER SIG TWO TYPE: ENTITY": True,
    "BORROWER SIG TWO TYPE: INDIVIDUAL": False,
    "BORROWER SIG ONE AND TWO: ENTITY": True,
    "BORROWER SIG ONE: ENTITY AND SIG TWO: INDIVIDUAL": False,

    # Officer's Certificate format (with quotes in label)
    'BORROWER SIG ONE TYPE : "ENTITY"': True,
    'BORROWER SIG ONE TYPE : "INDIVIDUAL"': False,
    'BORROWER SIG ONE TYPE : "ENTITY" AND BORROWER SIG TWO TYPE : "ENTITY"': True,
    'BORROWER SIG ONE TYPE : "ENTITY" AND BORROWER SIG TWO TYPE : "INDIVIDUAL"': False,
    'BORROWER SIG ONE ENTITY TYPE : "CORPORATION"': False,     # TGC LOC is LLC
    'BORROWER SIG ONE ENTITY TYPE : "LIMITED LIABILITY COMPANY"': True,
    'BORROWER SIG ONE ENTITY TYPE : "LIMITED PARTNERSHIP"': False,
    'BORROWER ENTITY : "CORPORATION"': False,
    'BORROWER ENTITY : "LIMITED LIABILITY COMPANY"': True,
    'BORROWER ENTITY : "LIMITED PARTNERSHIP"': False,

    # --- Guarantor Signature Block Types ---
    # Guarantor signer info is EXTERNAL INPUT REQUIRED — default to Individual for now
    "GUARANTOR SIG ONE TYPE: BLANK": False,
    "GUARANTOR SIG ONE TYPE: ENTITY": False,
    "GUARANTOR SIG ONE TYPE: INDIVIDUAL": True,
    "GUARANTOR SIG TWO TYPE: ENTITY": False,
    "GUARANTOR SIG TWO TYPE: INDIVIDUAL": False,
    "GUARANTOR SIG ONE AND TWO: ENTITY": False,
    "GUARANTOR SIG ONE: ENTITY AND SIG TWO: INDIVIDUAL": False,

    # Officer's Certificate Guarantor format
    'GUARANTOR SIG ONE TYPE : "ENTITY"': False,
    'GUARANTOR SIG ONE TYPE : "INDIVIDUAL"': True,
    'GUARANTOR SIG ONE TYPE : "ENTITY" AND GUARANTOR SIG TWO TYPE : "ENTITY"': False,
    'GUARANTOR SIG ONE TYPE : "ENTITY" AND GUARANTOR SIG TWO TYPE : "INDIVIDUAL"': False,
    'GUARANTOR SIG ONE ENTITY TYPE : "CORPORATION"': False,
    'GUARANTOR SIG ONE ENTITY TYPE : "LIMITED LIABILITY COMPANY"': False,
    'GUARANTOR SIG ONE ENTITY TYPE : "LIMITED PARTNERSHIP"': False,

    # Entity type conditions (Officer Cert Guarantor — entity context)
    'ENTITY : "CORPORATION"': True,       # Graham Group Holdings is a corporation
    'ENTITY : "LIMITED LIABILITY COMPANY"': False,
    'ENTITY : "LIMITED PARTNERSHIP"': False,

    # Dot-notation entity guarantor conditions (Cooperation, Post-Closing FOR EACH)
    "ENTITY GUARANTOR SIG ONE TYPE: BLANK": False,
    "ENTITY GUARANTOR SIG ONE TYPE: ENTITY": False,
    "ENTITY GUARANTOR SIG ONE TYPE: INDIVIDUAL": True,
    "ENTITY GUARANTOR SIG TWO TYPE: ENTITY": False,
    "ENTITY GUARANTOR SIG TWO TYPE: INDIVIDUAL": False,

    # --- Loan Related Restricted Account ---
    "ADDITIONAL COLLATERAL RESERVE ACCOUNT": False,
    "INTEREST RESERVE AND ADDITIONAL COLLATERAL RESERVE ACCOUNT": False,
    "INTEREST RESERVE OR ADDITIONAL COLLATERAL RESERVE ACCOUNT": False,

    # --- List punctuation (handled specially in FOR EACH) ---
    "LIST COMMA": True,
    "NOT LAST ITEM": True,

    # --- Multiple folios ---
    "MULTIPLE FOLIOS": True,
}

# Normalize all keys
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

# Placeholder mappings for FOR EACH item contexts
ENTITY_GUARANTOR_ITEMS = [
    {
        "eg name": "Graham Group Holdings, Inc.",
        "entity name": "Graham Group Holdings, Inc.",
        "eg state": "Florida",
        "entity state": "Florida",
        "eg entity type": "corporation",
        "entity entity type": "corporation",
        # Cooperation/Post-Closing entity guarantor sig placeholders
        "entity guarantor sig one indy": "[EXTERNAL INPUT REQUIRED]",
        "entity guarantor sig one indy title": "[EXTERNAL INPUT REQUIRED]",
        "entity guarantor sig one entity name": "[EXTERNAL INPUT REQUIRED]",
        "entity guarantor sig one entity type": "[EXTERNAL INPUT REQUIRED]",
        "entity guarantor sig one entity state": "[EXTERNAL INPUT REQUIRED]",
        "entity guarantor sig one entity relationship": "[EXTERNAL INPUT REQUIRED]",
        "entity guarantor sig two indy": "[EXTERNAL INPUT REQUIRED]",
        "entity guarantor sig two indy title": "[EXTERNAL INPUT REQUIRED]",
        "entity guarantor sig two entity name": "[EXTERNAL INPUT REQUIRED]",
        "entity guarantor sig two entity type": "[EXTERNAL INPUT REQUIRED]",
        "entity guarantor sig two entity state": "[EXTERNAL INPUT REQUIRED]",
        "entity guarantor sig two entity relationship": "[EXTERNAL INPUT REQUIRED]",
        "entity guarantor sig three entity indy": "[EXTERNAL INPUT REQUIRED]",
        "entity guarantor sig three entity indy title": "[EXTERNAL INPUT REQUIRED]",
    },
]


# ============================================================
# DOCUMENT SELECTION
# ============================================================

def select_documents(deal):
    """Determine which documents to generate based on deal parameters."""
    docs = []

    # Always generated
    for name in [
        "Promissory Note",
        "Mortgage",
        "Borrowers Reps",
        "Officer's Certificate (Borrower)",
        "Cooperation Agreement",
        "Garnishment Waiver",
        "Post-Closing Agreement",
        "Anti-Coercion",
    ]:
        docs.append(name)

    # Conditional
    if deal.get("leased_property"):
        docs.append("Assignment of Leases and Rents")
    if deal.get("entity_guarantors"):
        docs.append("Guaranty Agreement (Entity)")
        docs.append("Officer's Certificate (Guarantor)")
    if deal.get("personal_guarantors"):
        docs.append("Guaranty Agreement (Personal)")
    if deal.get("trust_guarantors"):
        docs.append("Guaranty Agreement (Trust)")
        docs.append("Trustee Affidavit")
    if deal.get("bad_boy_guarantor"):
        docs.append("Bad Boy Guaranty Agreement")
    if deal.get("construction"):
        docs.append("Construction Loan Agreement")
        docs.append("Assignment of Construction Docs")
        docs.append("Notice of Commencement")
        docs.append("Affidavit of Posting")
    if deal.get("ucc_required"):
        docs.append("UCC Financing Statement Florida")
        docs.append("UCC Financing Statement Other")
    if deal.get("reserve_account"):
        docs.append("Loan Related Restricted Account Agmt")
    if deal.get("subordination"):
        docs.append("Subordination Agreement")

    return sorted(docs)


# Graham Companies deal flags
DEAL_FLAGS = {
    "leased_property": True,
    "entity_guarantors": True,
    "personal_guarantors": False,
    "trust_guarantors": False,
    "bad_boy_guarantor": False,
    "construction": False,
    "ucc_required": False,
    "reserve_account": False,
    "subordination": False,
}


# ============================================================
# COMMENTS (shared + per-template)
# ============================================================

SHARED_COMMENTS = [
    {
        "target_text": "TGC Governors Square, LLC, TGC Parkside, LLC, and TGC Enrichment Center, LLC",
        "comment": "EDGE CASE: Multiple borrowers — three borrowing entities. Verify collective defined term and co-borrower structure.",
        "first_only": True,
    },
    {
        "target_text": "EXTERNAL INPUT REQUIRED",
        "comment": "EXTERNAL INPUT REQUIRED: Signatory information must be provided by attorney.",
        "first_only": True,
    },
    {
        "target_text": "CLOSING DATE",
        "comment": "CONFIRM: Closing date not specified in CAS. Attorney must provide.",
        "first_only": True,
    },
]

TEMPLATE_COMMENTS = {
    "Promissory Note": [
        {
            "target_text": "5.65",
            "comment": "REVIEW: Variable rate with 5-year repricing — Initial rate 5.65% fixed for first 5 years, then repriced every 5 years to SOFR + 2.00%, floor 5.65%.",
            "first_only": True,
        },
        {
            "target_text": "Graham Group Holdings, Inc.",
            "comment": "REVIEW: Payment-only corporate guaranty — verify scope of Borrowers' Liabilities.",
            "first_only": True,
        },
    ],
    "Mortgage": [
        {
            "target_text": "$56,000,000.00",
            "comment": "CONFIRM: Double loan amount for mortgage recording purposes ($28M x 2 = $56M).",
            "first_only": True,
        },
    ],
    "Guaranty Agreement (Entity)": [
        {
            "target_text": "Graham Group Holdings, Inc.",
            "comment": "REVIEW: Payment-only corporate guaranty per CAS. Verify scope is limited to prompt payment of Borrowers' Liabilities through maturity. POLICY EXCEPTION: Lack of significant and continuing guaranties.",
            "first_only": True,
        },
    ],
}


# ============================================================
# XML UTILITIES (engine from generate_commitment_letter.py)
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
    return etree.Element(f"{{{W_NS}}}{tag}", attrib=attrib or {}, nsmap=nsmap)


def w_sub(parent, tag, attrib=None):
    return etree.SubElement(parent, f"{{{W_NS}}}{tag}", attrib=attrib or {})


def get_para_text(para):
    texts = []
    for r in para.findall(f".//{{{W_NS}}}r"):
        t = r.find(f"{{{W_NS}}}t")
        if t is not None and t.text:
            texts.append(t.text)
    return "".join(texts)


def get_run_formatting(run):
    rpr = run.find(f"{{{W_NS}}}rPr")
    if rpr is not None:
        return copy.deepcopy(rpr)
    return None


# ============================================================
# CONDITIONAL RESOLUTION
# ============================================================


def find_if_markers(text):
    """Find all [IF: ...], [END IF: ...], [FOR EACH: ...], [END FOR EACH: ...] markers."""
    markers = []
    i = 0
    while i < len(text):
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
                        label = marker_text[9:-1] if is_end else marker_text[5:-1]
                        markers.append({
                            "start": start, "end": end,
                            "label": normalize_quotes(label),
                            "is_end": is_end, "text": marker_text,
                        })
                        found = True
                        break
                j += 1
            i = end if found else j + 1
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
                        label = "FOR:" + (marker_text[15:-1] if is_end else marker_text[11:-1])
                        markers.append({
                            "start": start, "end": end,
                            "label": label, "is_end": is_end,
                            "is_for": True, "text": marker_text,
                        })
                        found = True
                        break
                j += 1
            i = end if found else j + 1
        else:
            i += 1
    return markers


def resolve_inline_conditionals(text, condition_keeps):
    """Resolve all inline [IF: X]...[END IF: X] pairs."""
    max_iterations = 200
    iteration = 0

    while iteration < max_iterations:
        iteration += 1
        markers = find_if_markers(text)
        if_markers = [m for m in markers if not m.get("is_for")]
        if not if_markers:
            break

        resolved = False
        for i, m in enumerate(if_markers):
            if m["is_end"]:
                continue
            label = m["label"]
            for j in range(i + 1, len(if_markers)):
                if if_markers[j]["label"] == label and if_markers[j]["is_end"]:
                    has_nested = any(
                        not if_markers[k]["is_end"] for k in range(i + 1, j)
                    )
                    if not has_nested:
                        start_m = m
                        end_m = if_markers[j]
                        keep = condition_keeps.get(label)
                        if keep is None:
                            print(f"  WARNING: Unknown condition label: '{label}' — defaulting to KEEP")
                            keep = True
                        if keep:
                            content = text[start_m["end"]:end_m["start"]]
                            text = text[:start_m["start"]] + content + text[end_m["end"]:]
                        else:
                            text = text[:start_m["start"]] + text[end_m["end"]:]
                        resolved = True
                        break
            if resolved:
                break
        if not resolved:
            break

    return text


def resolve_inline_for_each(text, collection_name, items, condition_keeps):
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
        return text[:start_m["start"]] + text[end_m["end"]:]

    expanded_parts = []
    for idx, item in enumerate(items):
        part = template_content
        for key, val in item.items():
            placeholder = f"[{key.upper().replace('_', ' ')}]"
            part = part.replace(placeholder, val)
        is_last = (idx == len(items) - 1)
        overrides = {
            "LIST COMMA": not is_last,
            "NOT LAST ITEM": not is_last,
        }
        part = resolve_inline_conditionals(part, {**condition_keeps, **overrides})
        expanded_parts.append(part)

    return text[:start_m["start"]] + "".join(expanded_parts) + text[end_m["end"]:]


# ============================================================
# TRACKED CHANGES XML
# ============================================================


def create_del_run(text_content, rpr_elem, rev_id):
    del_elem = w_elem("del", {
        f"{{{W_NS}}}id": str(rev_id),
        f"{{{W_NS}}}author": AUTHOR,
        f"{{{W_NS}}}date": DATE_STR,
    })
    run = w_sub(del_elem, "r")
    if rpr_elem is not None:
        run.append(copy.deepcopy(rpr_elem))
    dt = w_sub(run, "delText")
    dt.set(f"{{{XML_NS}}}space", "preserve")
    dt.text = text_content
    return del_elem


def create_ins_run(text_content, rpr_elem, rev_id):
    ins_elem = w_elem("ins", {
        f"{{{W_NS}}}id": str(rev_id),
        f"{{{W_NS}}}author": AUTHOR,
        f"{{{W_NS}}}date": DATE_STR,
    })
    run = w_sub(ins_elem, "r")
    if rpr_elem is not None:
        run.append(copy.deepcopy(rpr_elem))
    t = w_sub(run, "t")
    t.set(f"{{{XML_NS}}}space", "preserve")
    t.text = text_content
    return ins_elem


def _strip_markers(text):
    """Strip IF/END IF/FOR EACH markers from text (for clean tracked deletions)."""
    text = re.sub(r"\[(?:END )?FOR EACH: [^\]]+\]", "", text)
    text = re.sub(r"\[(?:END )?IF: (?:[^\[\]]*|\[[^\]]*\])*\]", "", text)
    return text


def tracked_delete_paragraph(para, rev_gen):
    runs = para.findall(f"{{{W_NS}}}r")
    for run in runs:
        rev_id = rev_gen.next()
        rpr = run.find(f"{{{W_NS}}}rPr")
        t = run.find(f"{{{W_NS}}}t")
        text_content = t.text if t is not None and t.text else ""
        text_content = _strip_markers(text_content)
        del_elem = create_del_run(text_content, rpr, rev_id)
        parent = run.getparent()
        idx = list(parent).index(run)
        parent.remove(run)
        parent.insert(idx, del_elem)

    ppr = para.find(f"{{{W_NS}}}pPr")
    if ppr is None:
        ppr = w_sub(para, "pPr")
        para.insert(0, ppr)
    rpr_in_ppr = ppr.find(f"{{{W_NS}}}rPr")
    if rpr_in_ppr is None:
        rpr_in_ppr = w_sub(ppr, "rPr")
    w_sub(rpr_in_ppr, "del", {
        f"{{{W_NS}}}id": str(rev_gen.next()),
        f"{{{W_NS}}}author": AUTHOR,
        f"{{{W_NS}}}date": DATE_STR,
    })


def apply_replacement_to_paragraph(para, old_text, new_text, rev_gen):
    runs = para.findall(f"{{{W_NS}}}r")
    if not runs:
        return
    first_rpr = get_run_formatting(runs[0])
    for run in runs:
        para.remove(run)

    ppr = para.find(f"{{{W_NS}}}pPr")
    insert_idx = list(para).index(ppr) + 1 if ppr is not None else 0

    del_elem = create_del_run(_strip_markers(old_text), first_rpr, rev_gen.next())
    para.insert(insert_idx, del_elem)
    ins_elem = create_ins_run(new_text, first_rpr, rev_gen.next())
    para.insert(insert_idx + 1, ins_elem)


# ============================================================
# WORD COMMENTS
# ============================================================


def create_comments_xml(comments_list):
    nsmap = {
        "w": W_NS,
        "r": R_NS,
        "w14": "http://schemas.microsoft.com/office/word/2010/wordml",
    }
    comments_root = etree.Element(f"{{{W_NS}}}comments", nsmap=nsmap)

    for comment_data in comments_list:
        comment_id = str(comment_data["id"])
        comment_elem = w_sub(comments_root, "comment", {
            f"{{{W_NS}}}id": comment_id,
            f"{{{W_NS}}}author": AUTHOR,
            f"{{{W_NS}}}date": DATE_STR,
            f"{{{W_NS}}}initials": "AI",
        })
        p = w_sub(comment_elem, "p")
        ref_run = w_sub(p, "r")
        ref_rpr = w_sub(ref_run, "rPr")
        w_sub(ref_rpr, "rStyle", {f"{{{W_NS}}}val": "CommentReference"})
        w_sub(ref_run, "annotationRef")
        text_run = w_sub(p, "r")
        t = w_sub(text_run, "t")
        t.set(f"{{{XML_NS}}}space", "preserve")
        t.text = comment_data["text"]

    return comments_root


def add_comment_ref_to_paragraph(para, comment_id):
    cid = str(comment_id)
    range_start = w_elem("commentRangeStart", {f"{{{W_NS}}}id": cid})
    ppr = para.find(f"{{{W_NS}}}pPr")
    idx = list(para).index(ppr) + 1 if ppr is not None else 0
    para.insert(idx, range_start)

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


def process_document(template_path, output_path, placeholder_values, condition_keeps,
                     for_each_collections, comments_to_add):
    """Process a single template into an output document with tracked changes."""
    doc_name = os.path.basename(template_path).replace("Bank - ", "")
    print(f"\n{'='*60}")
    print(f"Generating: {doc_name}")
    print(f"{'='*60}")

    with zipfile.ZipFile(template_path, "r") as zin:
        file_contents = {}
        for name in zin.namelist():
            file_contents[name] = zin.read(name)

    # Process document.xml
    doc_xml = file_contents["word/document.xml"]
    doc_tree = etree.fromstring(doc_xml)
    body = doc_tree.find(f"{{{W_NS}}}body")
    paras = list(body.iter(f"{{{W_NS}}}p"))

    rev_gen = RevIdGen(start=1000)
    total_paras = len(paras)

    # Also process header/footer XML
    hf_trees = {}
    for name in file_contents:
        if re.match(r'word/(header|footer)\d*\.xml', name):
            hf_tree = etree.fromstring(file_contents[name])
            hf_trees[name] = hf_tree

    # ---- PHASE 1: Get original text for each paragraph ----
    para_texts = [get_para_text(p) for p in paras]

    # ---- PHASE 2: Resolve conditionals and placeholders ----

    resolved_texts = [""] * total_paras
    delete_flags = [False] * total_paras

    # --- Pass A-0: Handle multi-paragraph FOR EACH blocks ---
    for collection_name, items in for_each_collections.items():
        start_marker = f"[FOR EACH: {collection_name}]"
        end_marker = f"[END FOR EACH: {collection_name}]"
        start_idx = None
        for pi, text in enumerate(para_texts):
            normalized = normalize_quotes(text.strip())
            if start_marker in normalized and start_idx is None:
                marker_stripped = normalized.replace(start_marker, "").strip()
                if len(marker_stripped) < 20:
                    start_idx = pi
            if end_marker in normalized and start_idx is not None and pi > start_idx:
                end_idx = pi
                if not items:
                    for di in range(start_idx, end_idx + 1):
                        delete_flags[di] = True
                else:
                    if normalized == start_marker or para_texts[start_idx].strip() == start_marker:
                        delete_flags[start_idx] = True
                    end_text = para_texts[end_idx].strip()
                    end_normalized = normalize_quotes(end_text)
                    if end_normalized == end_marker:
                        delete_flags[end_idx] = True
                start_idx = None
                break

    # --- Pass A: Stack-based multi-paragraph block tracking ---
    condition_stack = []
    deletion_depth = 0
    para_unmatched_starts = [[] for _ in range(total_paras)]
    para_unmatched_ends = [[] for _ in range(total_paras)]

    for i, text in enumerate(para_texts):
        markers_in_para = find_if_markers(text)
        if_starts = [m for m in markers_in_para if not m["is_end"] and not m.get("is_for")]
        if_ends = [m for m in markers_in_para if m["is_end"] and not m.get("is_for")]

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

        if deletion_depth > 0:
            delete_flags[i] = True

        for end_m in sorted(unmatched_ends, key=lambda x: x["start"]):
            label = end_m["label"]
            for si in range(len(condition_stack) - 1, -1, -1):
                if condition_stack[si][0] == label:
                    was_delete = not condition_stack[si][1]
                    condition_stack.pop(si)
                    if was_delete:
                        deletion_depth -= 1
                    break

        for start_m in sorted(unmatched_starts, key=lambda x: x["start"]):
            label = start_m["label"]
            keep = condition_keeps.get(label)
            if keep is None:
                print(f"  WARNING: Unknown label at P{i}: '{label}' — defaulting to KEEP")
                keep = True
            condition_stack.append((label, keep))
            if not keep:
                deletion_depth += 1

    if condition_stack:
        print(f"  WARNING: {len(condition_stack)} unclosed conditional blocks")
        for label, keep in condition_stack:
            print(f"    '{label}' (keep={keep})")

    print(f"  Pass A: {sum(delete_flags)} of {total_paras} paragraphs marked for deletion")

    # --- Pass B: Resolve inline conditionals and placeholders ---
    for i, text in enumerate(para_texts):
        if delete_flags[i]:
            resolved_texts[i] = ""
            continue

        resolved = text

        for start_m in sorted(para_unmatched_starts[i], key=lambda x: x["start"], reverse=True):
            label = start_m["label"]
            keep = condition_keeps.get(label, True)
            if not keep:
                resolved = resolved[:start_m["start"]]
            else:
                resolved = resolved[:start_m["start"]] + resolved[start_m["end"]:]

        for end_m in sorted(para_unmatched_ends[i], key=lambda x: x["start"]):
            label = end_m["label"]
            keep = condition_keeps.get(label, True)
            if not keep:
                resolved = resolved[end_m["end"]:]
                break
            else:
                resolved = resolved[:end_m["start"]] + resolved[end_m["end"]:]

        # Resolve inline FOR EACH loops
        for collection_name, items in for_each_collections.items():
            resolved = resolve_inline_for_each(resolved, collection_name, items, condition_keeps)

        # Resolve inline conditionals
        resolved = resolve_inline_conditionals(resolved, condition_keeps)

        # Replace placeholders
        for placeholder, value in placeholder_values.items():
            if placeholder in resolved:
                resolved = resolved.replace(placeholder, value)

        # Strip remaining markers
        resolved = re.sub(r"\[(?:END )?FOR EACH: [^\]]+\]", "", resolved)
        resolved = re.sub(r"\[(?:END )?IF: (?:[^\[\]]*|\[[^\]]*\])*\]", "", resolved)

        if not resolved.strip():
            delete_flags[i] = True
            resolved_texts[i] = ""
        else:
            resolved_texts[i] = resolved

    # ---- PHASE 3: Apply changes to XML ----
    deleted_count = 0
    replaced_count = 0
    unchanged_count = 0

    for i, para in enumerate(paras):
        if i >= len(delete_flags):
            break
        old_text = para_texts[i]
        new_text = resolved_texts[i]

        if delete_flags[i]:
            tracked_delete_paragraph(para, rev_gen)
            deleted_count += 1
        elif old_text != new_text and new_text.strip():
            apply_replacement_to_paragraph(para, old_text, new_text, rev_gen)
            replaced_count += 1
        else:
            unchanged_count += 1

    # Process header/footer text (simple placeholder replacement + conditional strip)
    for hf_name, hf_tree in hf_trees.items():
        for p in hf_tree.findall(f".//{{{W_NS}}}p"):
            p_text = get_para_text(p)
            if not p_text.strip():
                continue
            resolved = p_text
            resolved = resolve_inline_conditionals(resolved, condition_keeps)
            for placeholder, value in placeholder_values.items():
                if placeholder in resolved:
                    resolved = resolved.replace(placeholder, value)
            resolved = re.sub(r"\[(?:END )?IF: (?:[^\[\]]*|\[[^\]]*\])*\]", "", resolved)
            if resolved != p_text:
                runs = p.findall(f"{{{W_NS}}}r")
                if runs:
                    first_rpr = get_run_formatting(runs[0])
                    for run in runs:
                        p.remove(run)
                    ppr = p.find(f"{{{W_NS}}}pPr")
                    insert_idx = list(p).index(ppr) + 1 if ppr is not None else 0
                    del_elem = create_del_run(p_text, first_rpr, rev_gen.next())
                    p.insert(insert_idx, del_elem)
                    ins_elem = create_ins_run(resolved, first_rpr, rev_gen.next())
                    p.insert(insert_idx + 1, ins_elem)

    print(f"  Deleted: {deleted_count} | Replaced: {replaced_count} | Unchanged: {unchanged_count}")

    # ---- PHASE 4: Add comments ----
    comment_records = []
    comment_id_counter = 500

    for comment_spec in comments_to_add:
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
                comment_records.append({"id": cid, "text": comment_spec["comment"]})
                add_comment_ref_to_paragraph(para, cid)
                found = True
                if first_only:
                    break

    if comment_records:
        comments_xml = create_comments_xml(comment_records)
        comments_bytes = etree.tostring(
            comments_xml, xml_declaration=True, encoding="UTF-8", standalone=True, pretty_print=True
        )
        file_contents["word/comments.xml"] = comments_bytes

        ct_xml = etree.fromstring(file_contents["[Content_Types].xml"])
        ct_ns = ct_xml.nsmap.get(None, CT_NS)
        override = etree.SubElement(ct_xml, f"{{{ct_ns}}}Override")
        override.set("PartName", "/word/comments.xml")
        override.set("ContentType",
                      "application/vnd.openxmlformats-officedocument.wordprocessingml.comments+xml")
        file_contents["[Content_Types].xml"] = etree.tostring(
            ct_xml, xml_declaration=True, encoding="UTF-8", standalone=True
        )

        rels_xml = etree.fromstring(file_contents["word/_rels/document.xml.rels"])
        rels_ns = rels_xml.nsmap.get(None, "http://schemas.openxmlformats.org/package/2006/relationships")
        rel = etree.SubElement(rels_xml, f"{{{rels_ns}}}Relationship")
        rel.set("Id", "rIdComments")
        rel.set("Type", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/comments")
        rel.set("Target", "comments.xml")
        file_contents["word/_rels/document.xml.rels"] = etree.tostring(
            rels_xml, xml_declaration=True, encoding="UTF-8", standalone=True
        )

    print(f"  Comments: {len(comment_records)}")

    # ---- PHASE 5: Serialize and save ----
    file_contents["word/document.xml"] = etree.tostring(
        doc_tree, xml_declaration=True, encoding="UTF-8", standalone=True
    )
    for hf_name, hf_tree in hf_trees.items():
        file_contents[hf_name] = etree.tostring(
            hf_tree, xml_declaration=True, encoding="UTF-8", standalone=True
        )

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zout:
        for name, data in file_contents.items():
            zout.writestr(name, data)

    # ---- Verification ----
    remaining_placeholders = 0
    remaining_if_markers = 0
    for i, text in enumerate(resolved_texts):
        if delete_flags[i]:
            continue
        phs = re.findall(r"\[[A-Z\$][A-Z0-9 \$%/\-]+\]", text)
        remaining_placeholders += len(phs)
        ifs = re.findall(r"\[(?:END )?IF:", text)
        remaining_if_markers += len(ifs)

    print(f"  Remaining placeholders: {remaining_placeholders}")
    print(f"  Remaining IF markers: {remaining_if_markers}")
    print(f"  Output: {output_path}")

    return {
        "doc_name": doc_name,
        "deleted": deleted_count,
        "replaced": replaced_count,
        "unchanged": unchanged_count,
        "comments": len(comment_records),
        "remaining_placeholders": remaining_placeholders,
        "remaining_if_markers": remaining_if_markers,
    }


# ============================================================
# MAIN
# ============================================================


def main():
    parser = argparse.ArgumentParser(description="Generate Bank loan documents from CAS")
    parser.add_argument("--template-dir", default="new_templates",
                        help="Directory containing maximum templates")
    parser.add_argument("--output-dir", default="output",
                        help="Output directory for generated documents")
    parser.add_argument("--deal-name", default="Graham Companies",
                        help="Deal name for output file naming")
    parser.add_argument("--only", nargs="*",
                        help="Generate only specific document types (partial name match)")
    args = parser.parse_args()

    # Determine which documents to generate
    selected = select_documents(DEAL_FLAGS)
    print(f"Deal: {args.deal_name} — $28,000,000 Refinance")
    print(f"Documents selected: {len(selected)}")

    if args.only:
        filtered = []
        for s in selected:
            if any(o.lower() in s.lower() for o in args.only):
                filtered.append(s)
        selected = filtered
        print(f"Filtered to: {len(selected)}")

    for doc in selected:
        print(f"  - {doc}")

    # Build FOR EACH collections
    for_each_collections = {
        "PERSONAL GUARANTORS": [],
        "ENTITY GUARANTORS": ENTITY_GUARANTOR_ITEMS,
        "TRUST GUARANTORS": [],
        "FOLIOS": [{"folio number": f["folio_number"]} for f in FOLIO_DATA],
    }

    # Generate each document
    results = []
    for doc_name in selected:
        template_file = f"Bank - {doc_name}.docx"
        template_path = os.path.join(args.template_dir, template_file)
        output_file = f"{args.deal_name} - {doc_name}.docx"
        output_path = os.path.join(args.output_dir, output_file)

        if not os.path.exists(template_path):
            print(f"\n  ERROR: Template not found: {template_path}")
            continue

        # Build comments for this template
        comments = list(SHARED_COMMENTS)
        if doc_name in TEMPLATE_COMMENTS:
            comments.extend(TEMPLATE_COMMENTS[doc_name])

        try:
            result = process_document(
                template_path, output_path,
                PLACEHOLDER_VALUES, CONDITION_KEEPS,
                for_each_collections, comments,
            )
            results.append(result)
        except Exception as e:
            print(f"\n  FAILED: {doc_name} — {e}")
            import traceback
            traceback.print_exc()
            results.append({"doc_name": doc_name, "error": str(e)})

    # Print summary
    print(f"\n{'='*60}")
    print(f"GENERATION SUMMARY — {args.deal_name}")
    print(f"{'='*60}")
    print(f"{'Document':<45} {'Del':>5} {'Rep':>5} {'Unc':>5} {'Com':>4} {'PH':>4} {'IF':>4}")
    print(f"{'-'*45} {'-'*5} {'-'*5} {'-'*5} {'-'*4} {'-'*4} {'-'*4}")

    success_count = 0
    for r in results:
        if "error" in r:
            print(f"{r['doc_name']:<45} FAILED: {r['error']}")
        else:
            print(f"{r['doc_name']:<45} {r['deleted']:5d} {r['replaced']:5d} "
                  f"{r['unchanged']:5d} {r['comments']:4d} {r['remaining_placeholders']:4d} "
                  f"{r['remaining_if_markers']:4d}")
            success_count += 1

    print(f"\nGenerated: {success_count}/{len(selected)} documents")
    print(f"Output directory: {args.output_dir}/")


if __name__ == "__main__":
    main()
