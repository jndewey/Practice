#!/usr/bin/env python3
"""
Convert a Jinja-templated .docx to a clean "maximum template" with [PLACEHOLDER] syntax.

Steps:
1. Unpack .docx (ZIP) → extract word/document.xml
2. Defragment Jinja expressions split across XML runs
3. Replace {{ variable }} with [PLACEHOLDER] using mapping
4. Strip {% %} control structures, keep all content from all branches
5. Insert [IF:] / [END IF:] markers around mutually exclusive sections
6. Clean up empty runs, merge adjacent same-format runs
7. Repack to new .docx
"""

import argparse
import copy
import json
import os
import re
import shutil
import sys
import tempfile
import zipfile
from lxml import etree

# Word XML namespaces
NSMAP = {
    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
    'mc': 'http://schemas.openxmlformats.org/markup-compatibility/2006',
    'w14': 'http://schemas.microsoft.com/office/word/2010/wordml',
    'w15': 'http://schemas.microsoft.com/office/word/2012/wordml',
}

W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'


# ---------------------------------------------------------------------------
# Variable → Placeholder mapping for Commitment Letter
# ---------------------------------------------------------------------------
COMMITMENT_LETTER_MAP = {
    # Borrower
    'borrower_name': '[BORROWER NAME]',
    'borrower_name|upper': '[BORROWER NAME CAPS]',
    'borrower_state': '[BORROWER STATE]',
    'borrower_entity': '[BORROWER ENTITY TYPE]',
    'borrower_entity|lower': '[BORROWER ENTITY TYPE]',
    'borrower_financials': '[BORROWER FINANCIALS]',
    'borrower_tax_returns': '[BORROWER TAX RETURNS]',
    'borrower_state_article': '[a/an]',
    'borrower_sig_one_entity_state_article': '[a/an]',
    'borrower_sig_two_entity_state_article': '[a/an]',

    # Signatory
    'borrower_sig_one_type': '[BORROWER SIG 1 TYPE]',
    'borrower_sig_one_entity_name': '[BORROWER SIG 1 ENTITY NAME]',
    'borrower_sig_one_entity_name|upper': '[BORROWER SIG 1 ENTITY NAME CAPS]',
    'borrower_sig_one_entity_type': '[BORROWER SIG 1 ENTITY TYPE]',
    'borrower_sig_one_entity_type|lower': '[BORROWER SIG 1 ENTITY TYPE]',
    'borrower_sig_one_entity_state': '[BORROWER SIG 1 ENTITY STATE]',
    'borrower_sig_one_entity_relationship': '[BORROWER SIG 1 RELATIONSHIP]',
    'borrower_sig_one_indy': '[BORROWER SIG 1 NAME]',
    'borrower_sig_one_indy|upper': '[BORROWER SIG 1 NAME CAPS]',
    'borrower_sig_one_indy_title': '[BORROWER SIG 1 TITLE]',
    'borrower_sig_two_type': '[BORROWER SIG 2 TYPE]',
    'borrower_sig_two_entity_name': '[BORROWER SIG 2 ENTITY NAME]',
    'borrower_sig_two_entity_name|upper': '[BORROWER SIG 2 ENTITY NAME CAPS]',
    'borrower_sig_two_entity_type': '[BORROWER SIG 2 ENTITY TYPE]',
    'borrower_sig_two_entity_type|lower': '[BORROWER SIG 2 ENTITY TYPE]',
    'borrower_sig_two_entity_state': '[BORROWER SIG 2 ENTITY STATE]',
    'borrower_sig_two_entity_relationship': '[BORROWER SIG 2 RELATIONSHIP]',
    'borrower_sig_two_indy': '[BORROWER SIG 2 NAME]',
    'borrower_sig_two_indy|upper': '[BORROWER SIG 2 NAME CAPS]',
    'borrower_sig_two_indy_title': '[BORROWER SIG 2 TITLE]',
    'borrower_sig_three_entity_indy': '[BORROWER SIG 3 NAME]',
    'borrower_sig_three_entity_indy|upper': '[BORROWER SIG 3 NAME CAPS]',
    'borrower_sig_three_entity_indy_title': '[BORROWER SIG 3 TITLE]',

    # Loan basics
    'new_loan': '[NEW OR EXISTING]',
    'la_or_fa': '[LOAN AMOUNT OR FUTURE ADVANCE]',
    'loan_amount': '[$LOAN AMOUNT]',
    'loan_amount_2': '[$LOAN AMOUNT 2]',
    'loan_amount_basis': '[LOAN AMOUNT BASIS]',
    'original_loan_amount': '[$ORIGINAL LOAN AMOUNT]',
    'existing_balance': '[$EXISTING BALANCE]',
    'loan_purpose': '[LOAN PURPOSE]',
    'existing_lender': '[EXISTING LENDER]',
    'remaining_proceeds': '[REMAINING PROCEEDS USE]',
    'line_of_credit': '[LINE OF CREDIT]',

    # Property
    'property_description': '[PROPERTY DESCRIPTION]',
    'property_address': '[PROPERTY ADDRESS]',
    'property_county': '[PROPERTY COUNTY]',
    'property_condition_reports': '[PROPERTY CONDITION REPORTS]',

    # Guarantors
    'guarantor': '[GUARANTOR EXISTS]',
    'bad_boy_guarantor': '[BAD BOY GUARANTOR FLAG]',
    'bad_boy_guarantor_name': '[BAD BOY GUARANTOR NAME]',
    'bad_boy_guarantor_name|upper': '[BAD BOY GUARANTOR NAME CAPS]',
    'existing_ownership': '[EXISTING OWNERSHIP]',
    'entity_guarantor_financials': '[ENTITY GUARANTOR FINANCIALS]',
    'guarantor_tax_returns': '[GUARANTOR TAX RETURNS]',
    'global_cash_flow': '[GLOBAL CASH FLOW]',

    # Term
    'term': '[TERM]',
    'extension': '[EXTENSION FLAG]',
    'extension_term': '[EXTENSION TERM]',
    'extension_term_period': '[EXTENSION PERIOD]',
    'extension_term_options': '[EXTENSION OPTIONS]',
    'construction_term': '[CONSTRUCTION TERM]',
    'perm_term': '[PERMANENT TERM]',
    'permanent_phase': '[PERMANENT PHASE FLAG]',

    # Interest rate
    'interest_rate_structure': '[RATE STRUCTURE]',
    'fixed_interest_rate': '[FIXED RATE]',
    'fixed_rate_now': '[FIXED RATE KNOWN]',
    'initial_fixed_rate_now': '[INITIAL FIXED RATE KNOWN]',
    'initial_fixed_rate_term': '[INITIAL FIXED TERM]',
    'interest_rate_adjustments': '[RATE ADJUSTMENTS]',
    'interest_rate_spread': '[RATE SPREAD]',
    'index': '[INDEX]',
    'margin': '[MARGIN FLAG]',
    'margin_rate': '[MARGIN RATE]',
    'floor': '[FLOOR FLAG]',
    'floor_rate': '[FLOOR RATE]',
    'floor_rate_now': '[FLOOR RATE KNOWN]',

    # Repayment
    'amortization_period': '[AMORTIZATION PERIOD]',
    'interest_only_period': '[IO PERIOD FLAG]',
    'interest_only_months': '[IO MONTHS]',

    # Prepayment
    'prepayment_penalty': '[PREPAYMENT PENALTY FLAG]',
    'prepayment_penalty_type': '[PREPAYMENT PENALTY TYPE]',
    'pppercentage': '[PREPAYMENT PERCENTAGE]',
    'ppterm': '[PREPAYMENT TERM]',
    'ppfullterm': '[PREPAYMENT FULL TERM]',

    # Holdback
    'holdback': '[HOLDBACK FLAG]',
    'holdback_amount': '[$HOLDBACK AMOUNT]',
    'holdback_basis': '[HOLDBACK BASIS]',
    'holdback_funding': '[HOLDBACK CONDITIONS]',

    # Future advance
    'future_advance': '[FUTURE ADVANCE FLAG]',
    'future_advance_amount': '[$FUTURE ADVANCE AMOUNT]',
    'future_advance_amount_2': '[$FUTURE ADVANCE AMOUNT 2]',

    # Covenants
    'dscr': '[DSCR RATIO]',
    'dscr_covenant': '[DSCR COVENANT FLAG]',
    'dscr_covenant_rate': '[DSCR COVENANT RATE]',
    'dscr_net_operating_income': '[DSCR NOI FLAG]',
    'dscr_basis': '[DSCR BASIS]',
    'dscr_start': '[DSCR START TRIGGER]',
    'dscr_start_date': '[DSCR START DATE]',
    'dscr_annually': '[DSCR ANNUAL FLAG]',
    'dscr_debt_service_basis': '[DSCR DS BASIS]',
    'dscr_min_management_fee': '[DSCR MIN MGMT FEE]',
    'min_dscr_adjustment_basis': '[DSCR ADJUSTMENT BASIS]',
    'ltv': '[LTV RATIO]',
    'ltp': '[LTP RATIO]',
    'ltc': '[LTC RATIO]',
    'ltv_maintenance_ratio': '[LTV MAINTENANCE RATIO]',
    'tax_escrow': '[TAX ESCROW TYPE]',
    'business_interruption_insurance': '[BIZ INTERRUPTION INSURANCE]',
    'cross_default': '[CROSS DEFAULT FLAG]',
    'cross_borrower': '[CROSS BORROWER]',
    'cross_property': '[CROSS PROPERTY]',
    'cross_loan_new': '[CROSS LOAN NEW]',
    'tenant_reserve': '[TENANT RESERVE FLAG]',

    # Reserves
    'reserve_account': '[RESERVE ACCOUNT FLAG]',
    'reserve_months': '[RESERVE MONTHS]',
    'reserve_fee': '[RESERVE FEE]',
    'stabilization_reserve': '[STABILIZATION RESERVE FLAG]',
    'stabilization_reserve_amount': '[$STABILIZATION RESERVE AMOUNT]',
    'interest_reserve': '[INTEREST RESERVE FLAG]',
    'interest_reserve_account': '[INTEREST RESERVE ACCOUNT FLAG]',
    'interest_reserve_months': '[INTEREST RESERVE MONTHS]',
    'franchise': '[FRANCHISE FLAG]',
    'franchisor': '[FRANCHISOR NAME]',
    'joint_venture_and_others': '[JV/LP FLAG]',
    'environmental_report': '[ENVIRONMENTAL FLAG]',
    'star_report': '[STAR REPORT FLAG]',
    'star_semi_annual': '[STAR SEMI-ANNUAL FLAG]',
    'bond': '[BOND FLAG]',
    'equity_req': '[EQUITY REQUIREMENT]',

    # Reporting
    'leased_property': '[LEASED PROPERTY FLAG]',
    'content_included': '[UCC REQUIRED]',
    'rent_roll': '[RENT ROLL FLAG]',
    'operating_statement': '[OPERATING STATEMENT FLAG]',
    'tax_return_extend_c': '[TAX EXTEND CORP]',
    'tax_return_extend_p': '[TAX EXTEND PERSONAL]',

    # Fees and dates
    'commitment_fee': '[COMMITMENT FEE FLAG]',
    'commitment_fee_amount': '[COMMITMENT FEE %]',
    'commitment_fee_basis': '[COMMITMENT FEE BASIS]',
    'commitment_date': '[COMMITMENT DATE]',
    'closing_date': '[CLOSING DATE]',

    # Bank personnel
    'senior_vice_president': '[SENIOR VP NAME]',
    'bank_officer': '[BANK OFFICER NAME]',
    'bank_officer_position': '[BANK OFFICER POSITION]',

    # Computed
    'total_guarantors': '[TOTAL GUARANTORS]',
    'relationship_name': '[RELATIONSHIP CONTACT]',

    # Borrower address fields (Assignment of Leases, Cooperation, Notice, UCC forms)
    'borrower_street_address': '[BORROWER STREET ADDRESS]',
    'borrower_city': '[BORROWER CITY]',
    'borrower_mailing_state': '[BORROWER MAILING STATE]',
    'borrower_zip': '[BORROWER ZIP]',
    'prepared_by': '[PREPARED BY]',

    # Guarantor signature fields (Entity Guaranty, Officer Cert Guarantor)
    'guarantor_sig_one_entity_name': '[GUARANTOR SIG 1 ENTITY NAME]',
    'guarantor_sig_one_entity_type': '[GUARANTOR SIG 1 ENTITY TYPE]',
    'guarantor_sig_one_entity_type|lower': '[GUARANTOR SIG 1 ENTITY TYPE]',
    'guarantor_sig_one_entity_state': '[GUARANTOR SIG 1 ENTITY STATE]',
    'guarantor_sig_one_entity_relationship': '[GUARANTOR SIG 1 RELATIONSHIP]',
    'guarantor_sig_one_indy': '[GUARANTOR SIG 1 NAME]',
    'guarantor_sig_one_indy_title': '[GUARANTOR SIG 1 TITLE]',
    'guarantor_sig_two_entity_name': '[GUARANTOR SIG 2 ENTITY NAME]',
    'guarantor_sig_two_entity_type': '[GUARANTOR SIG 2 ENTITY TYPE]',
    'guarantor_sig_two_entity_type|lower': '[GUARANTOR SIG 2 ENTITY TYPE]',
    'guarantor_sig_two_entity_state': '[GUARANTOR SIG 2 ENTITY STATE]',
    'guarantor_sig_two_entity_relationship': '[GUARANTOR SIG 2 RELATIONSHIP]',
    'guarantor_sig_two_indy': '[GUARANTOR SIG 2 NAME]',
    'guarantor_sig_two_indy_title': '[GUARANTOR SIG 2 TITLE]',
    'guarantor_sig_three_entity_indy': '[GUARANTOR SIG 3 NAME]',
    'guarantor_sig_three_entity_indy_title': '[GUARANTOR SIG 3 TITLE]',

    # Guaranty-specific contextual variables (inside FOR EACH loops)
    'name': '[GUARANTOR NAME]',
    'name|upper': '[GUARANTOR NAME CAPS]',
    'address': '[GUARANTOR ADDRESS]',
    'entity': '[GUARANTOR ENTITY TYPE]',
    'entity|lower': '[GUARANTOR ENTITY TYPE]',
    'state': '[GUARANTOR STATE]',
    'trustee_name|upper': '[TRUSTEE NAME CAPS]',
    'trust_agreement_date|dateformat': '[TRUST AGREEMENT DATE]',

    # Promissory Note specific
    'maturity_date': '[MATURITY DATE]',
    'interest_only_end_date': '[IO END DATE]',
    'payment_date': '[PAYMENT DATE]',
    'original_closing_date|dateformat': '[ORIGINAL CLOSING DATE]',
    'initial_fixed_rate_term_date': '[INITIAL FIXED TERM DATE]',
    'initial_funding': '[$INITIAL FUNDING]',
    'tenant': '[TENANT]',
    'records_book_number': '[RECORDS BOOK NUMBER]',
    'records_mtg_page_number': '[RECORDS MTG PAGE NUMBER]',
    'records_alr_page_number': '[RECORDS ALR PAGE NUMBER]',
    'personal_guarantor_financials': '[PERSONAL GUARANTOR FINANCIALS]',

    # Mortgage
    'loan_amount_double_rounded': '[$LOAN AMOUNT DOUBLED]',
    'borrower_entity': '[BORROWER ENTITY TYPE]',
    'borrower_sig_one_entity_type': '[BORROWER SIG 1 ENTITY TYPE]',
    'borrower_sig_two_entity_type': '[BORROWER SIG 2 ENTITY TYPE]',
}

# Condition labels for [IF:] / [END IF:] markers
CONDITION_LABELS = {
    'new_loan == "New Loan"': 'NEW LOAN',
    'new_loan == " New Loan"': 'NEW LOAN',  # typo in template
    'new_loan_is_nl': 'NEW LOAN',
    'new_loan == "Existing Loan"': 'EXISTING LOAN',
    'not new_loan_is_nl': 'EXISTING LOAN',
    'interest_rate_structure == "fixed"': 'FIXED RATE',
    'interest_rate_structure == "floating"': 'FLOATING RATE',
    'interest_rate_structure == "variable"': 'VARIABLE RATE',
    'interest_rate_structure == "swap"': 'SWAP RATE',
    'holdback': 'HOLDBACK',
    'not holdback': 'NO HOLDBACK',
    'extension': 'EXTENSION OPTION',
    'not extension': 'NO EXTENSION',
    'future_advance': 'FUTURE ADVANCE',
    'not future_advance': 'NO FUTURE ADVANCE',
    'prepayment_penalty': 'PREPAYMENT PENALTY',
    'not prepayment_penalty': 'NO PREPAYMENT PENALTY',
    'commitment_fee': 'COMMITMENT FEE',
    'not commitment_fee': 'UNDERWRITING FEE',
    'dscr_covenant': 'DSCR COVENANT',
    'not dscr_covenant': 'NO DSCR COVENANT',
    'cross_default': 'CROSS DEFAULT',
    'not cross_default': 'NO CROSS DEFAULT',
    'tenant_reserve': 'TENANT RESERVE',
    'reserve_account': 'RESERVE ACCOUNT',
    'stabilization_reserve': 'STABILIZATION RESERVE',
    'interest_reserve_account': 'INTEREST RESERVE',
    'franchise': 'FRANCHISE',
    'joint_venture_and_others': 'JV/LP AGREEMENTS',
    'environmental_report': 'ENVIRONMENTAL',
    'star_report': 'STAR REPORTS',
    'star_semi_annual': 'STAR SEMI-ANNUAL',
    'bond': 'BOND',
    'guarantor': 'GUARANTOR',
    'not guarantor': 'NO GUARANTOR',
    'bad_boy_guarantor': 'BAD BOY GUARANTOR',
    'not bad_boy_guarantor': 'NO BAD BOY GUARANTOR',
    'existing_ownership': 'EXISTING OWNERSHIP',
    'interest_only_period': 'INTEREST ONLY',
    'not interest_only_period': 'NO INTEREST ONLY',
    'permanent_phase': 'PERMANENT PHASE',
    'not permanent_phase': 'NO PERMANENT PHASE',
    'leased_property': 'LEASED PROPERTY',
    'not leased_property': 'NOT LEASED PROPERTY',
    'loan_purpose == "Acquisition"': 'ACQUISITION',
    'loan_purpose == "Refinance with existing debt"': 'REFINANCE WITH DEBT',
    'loan_purpose == "Refinance free and clear"': 'REFINANCE FREE AND CLEAR',
    'loan_purpose == "Construction"': 'CONSTRUCTION',
    'loan_purpose != "Construction"': 'NOT CONSTRUCTION',
    'content_included': 'UCC REQUIRED',
    'not content_included': 'UCC NOT REQUIRED',
    'tax_escrow == "no escrow"': 'NO ESCROW',
    'tax_escrow == "tax and insurance"': 'TAX AND INSURANCE ESCROW',
    'tax_escrow == "tax and flood insurance"': 'TAX AND FLOOD ESCROW',
    'dscr_net_operating_income': 'NOI-BASED DSCR',
    'not dscr_net_operating_income': 'NON-NOI DSCR',
    'index == "SOFR"': 'SOFR INDEX',
    'index == "Prime"': 'PRIME INDEX',
    'floor': 'FLOOR RATE',
    'not floor': 'NO FLOOR RATE',
    'fixed_rate_now': 'FIXED RATE KNOWN',
    'not fixed_rate_now': 'FIXED RATE TBD',
    'floor_rate_now': 'FLOOR RATE KNOWN',
    'not floor_rate_now': 'FLOOR RATE TBD',
    'initial_fixed_rate_now': 'INITIAL RATE KNOWN',
    'not initial_fixed_rate_now': 'INITIAL RATE TBD',
    'margin': 'MARGIN',
    'not margin': 'NO MARGIN',
    'rent_roll': 'RENT ROLL',
    'operating_statement': 'OPERATING STATEMENT',
    'global_cash_flow': 'GLOBAL CASH FLOW',
    'business_interruption_insurance': 'BIZ INTERRUPTION INSURANCE',
    'conditional_reporting_reg': 'CONDITION REPORTS',
    'ppfullterm': 'PENALTY FULL TERM',
    'not ppfullterm': 'PENALTY PARTIAL TERM',
    # Computed variables
    'loan_amount_actual': 'LOAN AMOUNT STATED',
    'not loan_amount_actual': 'LOAN AMOUNT NOT STATED',
    'fa_basis': 'FEE ON FUTURE ADVANCE',
    'not fa_basis': 'FEE ON LOAN AMOUNT',
    'is_la': 'BASIS IS LOAN AMOUNT',
    'not is_la': 'BASIS IS FUTURE ADVANCE',
    # Reporting
    'borrower_financials': 'BORROWER FINANCIALS',
    'not borrower_financials': 'NO BORROWER FINANCIALS',
    'entity_guarantor_financials': 'ENTITY GUARANTOR FINANCIALS',
    'borrower_tax_returns': 'BORROWER TAX RETURNS',
    'not borrower_tax_returns': 'NO BORROWER TAX RETURNS',
    'guarantor_tax_returns': 'GUARANTOR TAX RETURNS',
    'not guarantor_tax_returns': 'NO GUARANTOR TAX RETURNS',
    'purpose_add_info': 'PURPOSE ADDITIONAL INFO',
    'not purpose_add_info': 'NO PURPOSE ADDITIONAL INFO',
    # Combined conditions
    'borrower_financials or entity_guarantor_financials': 'BORROWER OR ENTITY FINANCIALS',
    'borrower_financials and entity_guarantor_financials': 'BORROWER AND ENTITY FINANCIALS',
    'borrower_tax_returns or guarantor_tax_returns': 'BORROWER OR GUARANTOR TAX RETURNS',
    'borrower_tax_returns and guarantor_tax_returns': 'BORROWER AND GUARANTOR TAX RETURNS',
    'rent_roll or operating_statement': 'RENT ROLL OR OPERATING STATEMENT',
    'rent_roll and operating_statement': 'RENT ROLL AND OPERATING STATEMENT',
    'prepayment_penalty_type == "bona fide"': 'BONA FIDE SALE EXCEPTION',
    'prepayment_penalty_type == "refinance"': 'REFINANCE PENALTY',
    # Loan amount conditions
    '"LTV" in loan_amount_basis': 'LTV BASIS',
    '"Loan to Purchase" in loan_amount_basis': 'LTP BASIS',
    '"DSCR" in loan_amount_basis': 'DSCR BASIS',
    '"Loan to Purchase" not in loan_amount_basis': 'NO LTP BASIS',
    '"DSCR" not in loan_amount_basis': 'NO DSCR BASIS',
    '"LTV" not in loan_amount_basis': 'NO LTV BASIS',
    # Escrow combined
    'tax_escrow == "tax and insurance" or tax_escrow == "tax and flood insurance"': 'TAX ESCROW REQUIRED',
    'tax_escrow == "no escrow during interest only period and tax and insurance escrow thereafter"': 'IO NO ESCROW THEN ESCROW',
    # Guarantor type conditions
    'personal_guarantors|length > 0': 'PERSONAL GUARANTORS',
    'entity_guarantors|length > 0': 'ENTITY GUARANTORS',
    'trust_guarantors|length > 0': 'TRUST GUARANTORS',
    'personal_guarantors|length > 1': 'MULTIPLE PERSONAL GUARANTORS',
    'entity_guarantors|length > 1': 'MULTIPLE ENTITY GUARANTORS',
    'trust_guarantors|length > 1': 'MULTIPLE TRUST GUARANTORS',
    # Interest rate combined
    'interest_rate_structure == "floating" or interest_rate_structure == "variable"': 'FLOATING OR VARIABLE RATE',
    # DSCR conditions
    'dscr_start == "at closing"': 'DSCR FROM CLOSING',
    'dscr_start == "particular year"': 'DSCR FROM SPECIFIC DATE',
    'dscr_start == "conversion to p and i"': 'DSCR FROM CONVERSION',
    'dscr_basis == "income and expense statements"': 'DSCR BASIS I&E',
    'dscr_basis == "company tax returns"': 'DSCR BASIS TAX RETURNS',
    'dscr_debt_service_basis': 'DSCR HYPOTHETICAL AMORTIZATION',
    # Signature types
    'borrower_sig_one_type == "entity"': 'SIG 1 ENTITY',
    'borrower_sig_one_type == "individual"': 'SIG 1 INDIVIDUAL',
    'borrower_sig_one_type == "blank"': 'SIG 1 BLANK',
    'borrower_sig_two_type == "entity"': 'SIG 2 ENTITY',
    'borrower_sig_two_type == "individual"': 'SIG 2 INDIVIDUAL',
    'borrower_sig_two_type == "blank"': 'SIG 2 BLANK',
    # Folio conditions
    'folios|length > 1': 'MULTIPLE FOLIOS',
    'not folios|length > 1': 'SINGLE FOLIO',
    # Property condition reports
    'property_condition_reports == "full condition"': 'FULL CONDITION REPORT',
    'property_condition_reports == "roof and termite"': 'ROOF AND TERMITE REPORT',
    'property_condition_reports == "roof only"': 'ROOF ONLY REPORT',
    'property_condition_reports == "roof and termite" or property_condition_reports == "roof only"': 'ROOF REPORT',
    'not property_condition_reports == "roof only"': 'NOT ROOF ONLY',
    # Rate adjustments
    'interest_rate_adjustments > 0': 'MULTIPLE RATE ADJUSTMENTS',
    'interest_rate_adjustments == 1': 'SINGLE RATE ADJUSTMENT',
    'initial_fixed_rate_term > 4': 'INITIAL FIXED > 4 YEARS',
    # Total guarantors
    'total_guarantors > 0': 'HAS GUARANTORS',
    'not total_guarantors > 0': 'NO GUARANTORS',
    'total_guarantors > 1': 'MULTIPLE GUARANTORS',
    'total_guarantors > 0 or bad_boy_guarantor': 'GUARANTOR SECTION',
    # Extension options
    'extension_term_options > 1': 'MULTIPLE EXTENSION OPTIONS',
    'not extension_term_options > 1': 'SINGLE EXTENSION OPTION',
    # Loan amount comparisons
    'loan_amount > 999999': 'LOAN OVER $1M',
    'loan_amount < 1000000': 'LOAN UNDER $1M',
    'loan_amount > 500000': 'LOAN OVER $500K',
    'loan_amount < 500001': 'LOAN UNDER $500K',

    # Signature type patterns (with capitalized values, used across 15+ templates)
    'borrower_sig_one_type == "Entity"': 'BORROWER SIG ONE TYPE: ENTITY',
    'borrower_sig_one_type == "Individual"': 'BORROWER SIG ONE TYPE: INDIVIDUAL',
    'borrower_sig_one_type == ""': 'BORROWER SIG ONE TYPE: BLANK',
    'borrower_sig_two_type == "Entity"': 'BORROWER SIG TWO TYPE: ENTITY',
    'borrower_sig_two_type == "Individual"': 'BORROWER SIG TWO TYPE: INDIVIDUAL',
    'borrower_sig_two_type == ""': 'BORROWER SIG TWO TYPE: BLANK',
    'guarantor_sig_one_type == "Entity"': 'GUARANTOR SIG ONE TYPE: ENTITY',
    'guarantor_sig_one_type == "Individual"': 'GUARANTOR SIG ONE TYPE: INDIVIDUAL',
    'guarantor_sig_one_type == ""': 'GUARANTOR SIG ONE TYPE: BLANK',
    'guarantor_sig_two_type == "Entity"': 'GUARANTOR SIG TWO TYPE: ENTITY',
    'guarantor_sig_two_type == "Individual"': 'GUARANTOR SIG TWO TYPE: INDIVIDUAL',

    # Compound signature conditions
    'borrower_sig_one_type == "Entity" and borrower_sig_two_type == "Entity"': 'BORROWER SIG ONE AND TWO: ENTITY',
    'borrower_sig_one_type == "Entity" and borrower_sig_two_type == "Individual"': 'BORROWER SIG ONE: ENTITY AND SIG TWO: INDIVIDUAL',
    'guarantor_sig_one_type == "Entity" and guarantor_sig_two_type == "Entity"': 'GUARANTOR SIG ONE AND TWO: ENTITY',
    'guarantor_sig_one_type == "Entity" and guarantor_sig_two_type == "Individual"': 'GUARANTOR SIG ONE: ENTITY AND SIG TWO: INDIVIDUAL',

    # Entity type conditions (Officer Certs)
    'entity == "corporation"': 'ENTITY IS CORPORATION',
    'entity == "limited liability company"': 'ENTITY IS LLC',
    'entity == "limited partnership"': 'ENTITY IS LP',
    'borrower_entity == "corporation"': 'BORROWER IS CORPORATION',
    'borrower_entity == "limited liability company"': 'BORROWER IS LLC',
    'borrower_entity == "limited partnership"': 'BORROWER IS LP',
    'guarantor_sig_one_entity_type == "corporation"': 'GUARANTOR SIG ONE ENTITY: CORPORATION',
    'guarantor_sig_one_entity_type == "limited liability company"': 'GUARANTOR SIG ONE ENTITY: LLC',
    'guarantor_sig_one_entity_type == "limited partnership"': 'GUARANTOR SIG ONE ENTITY: LP',

    # Dot-notation conditions (FOR EACH entity context)
    'entity.state': 'ENTITY HAS STATE',
    'entity.guarantor_sig_one_type == "Entity"': 'ENTITY GUARANTOR SIG ONE TYPE: ENTITY',
    'entity.guarantor_sig_one_type == "Individual"': 'ENTITY GUARANTOR SIG ONE TYPE: INDIVIDUAL',
    'entity.guarantor_sig_one_type == ""': 'ENTITY GUARANTOR SIG ONE TYPE: BLANK',
    'entity.guarantor_sig_two_type == "Entity"': 'ENTITY GUARANTOR SIG TWO TYPE: ENTITY',
    'entity.guarantor_sig_two_type == "Individual"': 'ENTITY GUARANTOR SIG TWO TYPE: INDIVIDUAL',

    # Boolean flags and compound conditions
    'dscr_annually': 'DSCR ANNUALLY',
    'tax_return_extend_c': 'TAX EXTEND CORP',
    'tax_return_extend_p': 'TAX EXTEND PERSONAL',
    'line_of_credit': 'LINE OF CREDIT',
    'personal_guarantor_financials': 'PERSONAL GUARANTOR FINANCIALS',
    'total_guarantors > 0 or cross_default': 'HAS GUARANTORS OR CROSS DEFAULT',
    'entity_guarantors or trust_guarantors': 'ENTITY OR TRUST GUARANTORS',
    'entity_guarantors': 'ENTITY GUARANTORS',
    'trust_guarantors': 'TRUST GUARANTORS',
    'personal_guarantors': 'PERSONAL GUARANTORS',
    'total_guarantors == 0': 'NO GUARANTORS',
    'entity_guarantors|length > 0 or trust_guarantors|length > 0': 'ENTITY OR TRUST GUARANTORS',
    'personal_guarantors|length > 0 and trust_guarantors|length == 0': 'PERSONAL GUARANTORS AND NO TRUST',
    'not interest_rate_structure == "swap"': 'NOT SWAP RATE',
    'interest_rate_adjustments > 1': 'MULTIPLE RATE ADJUSTMENTS',
    'not tax_escrow == "tax and flood insurance"': 'NOT TAX AND FLOOD ESCROW',
    'tax_escrow == "no escrow" or tax_escrow == "no escrow during interest only period and tax and insurance escrow thereafter"': 'NO ESCROW OR IO NO ESCROW',
    'tax_escrow == "no escrow during interest only period and tax and insurance escrow thereafter"': 'IO NO ESCROW THEN ESCROW',
    'borrower_state': 'BORROWER HAS STATE',

    # Extension term period
    'extension_term_period == "months"': 'EXTENSION IN MONTHS',
    'extension_term_period == "years"': 'EXTENSION IN YEARS',

    # Cooperation Agreement computed conditions
    'lone_amount_actual': 'LOAN AMOUNT ACTUAL',
    'not lone_amount_actual': 'NOT LOAN AMOUNT ACTUAL',
}


def get_label_for_condition(cond_text):
    """Get a human-readable label for a Jinja condition."""
    cond = cond_text.strip()
    # Strip trailing whitespace-trim marker
    cond = cond.rstrip('-').strip()

    # Direct lookup
    if cond in CONDITION_LABELS:
        return CONDITION_LABELS[cond]
    # Try normalizing whitespace
    normalized = re.sub(r'\s+', ' ', cond).strip()
    if normalized in CONDITION_LABELS:
        return CONDITION_LABELS[normalized]

    # Handle loop variables — these are formatting helpers, label as such
    if 'loop.' in cond:
        if 'loop.last' in cond:
            return 'NOT LAST ITEM' if 'not' in cond.lower() else 'LAST ITEM'
        if 'loop.revindex' in cond:
            return 'LIST COMMA' if '> 2' in cond else 'LIST AND'
        return 'LOOP CONTROL'

    # Handle |length conditions
    length_match = re.match(r'(not\s+)?(\w+)\|length\s*(>|==|!=|<|>=|<=)\s*(\d+)', normalized)
    if length_match:
        negated, var, op, num = length_match.groups()
        var_label = var.replace('_', ' ').upper()
        if op == '>' and num == '0':
            prefix = 'NO ' if negated else ''
            return f'{prefix}{var_label}'
        if op == '>' and num == '1':
            prefix = 'NOT ' if negated else ''
            return f'{prefix}MULTIPLE {var_label}'
        return f'{var_label} COUNT {op} {num}'

    # Handle "x in y" conditions (e.g., '"LTV" in loan_amount_basis')
    in_match = re.match(r'"([^"]+)"\s+(not\s+)?in\s+(\w+)', normalized)
    if in_match:
        val, negated, var = in_match.groups()
        var_label = var.replace('_', ' ').upper()
        val_label = val.upper()
        prefix = 'NO ' if negated else ''
        return f'{prefix}{val_label} {var_label}'

    # Handle compound or/and conditions — try each part
    if ' or ' in normalized:
        parts = normalized.split(' or ')
        labels = []
        for p in parts:
            p = p.strip()
            if p in CONDITION_LABELS:
                labels.append(CONDITION_LABELS[p])
            else:
                labels.append(get_label_for_condition(p))
        return ' OR '.join(labels)

    if ' and ' in normalized:
        parts = normalized.split(' and ')
        labels = []
        for p in parts:
            p = p.strip()
            if p in CONDITION_LABELS:
                labels.append(CONDITION_LABELS[p])
            else:
                labels.append(get_label_for_condition(p))
        return ' AND '.join(labels)

    # Handle parenthesized conditions
    if normalized.startswith('(') and normalized.endswith(')'):
        return get_label_for_condition(normalized[1:-1])
    if normalized.startswith('not (') and normalized.endswith(')'):
        inner = get_label_for_condition(normalized[5:-1])
        return f'NOT ({inner})'

    # Handle dot-notation conditions (e.g., entity.field == "value")
    dot_eq_match = re.match(r'(\w+)\.(\w+)\s*==\s*"([^"]+)"', normalized)
    if dot_eq_match:
        obj, field, val = dot_eq_match.groups()
        label = f'{obj.upper()} {field.replace("_", " ").upper()}: {val.upper()}'
        return label

    # Handle dot-notation boolean (e.g., entity.state)
    dot_bool_match = re.match(r'^(\w+)\.(\w+)$', normalized)
    if dot_bool_match:
        obj, field = dot_bool_match.groups()
        return f'{obj.upper()} {field.replace("_", " ").upper()}'

    # Handle vowel-check conditions (e.g., borrower_state[0]|lower in ['a', 'e', ...])
    vowel_match = re.match(r"([\w.]+)\[0\]\|lower\s+in\s+\[.*?\]", normalized)
    if vowel_match:
        var = vowel_match.group(1).replace('.', ' ').replace('_', ' ').upper()
        return f'{var} STARTS WITH VOWEL'

    # Handle dot-notation vowel checks (e.g., entity.guarantor_sig_one_entity_state[0]...)
    dot_vowel_match = re.match(r"(\w+)\.([\w]+)\[0\]\|lower\s+in\s+\[.*?\]", normalized)
    if dot_vowel_match:
        obj, field = dot_vowel_match.groups()
        return f'{obj.upper()} {field.replace("_", " ").upper()} STARTS WITH VOWEL'

    # Handle == comparisons
    eq_match = re.match(r'(not\s+)?(\w+)\s*==\s*"([^"]+)"', normalized)
    if eq_match:
        negated, var, val = eq_match.groups()
        var_label = var.replace('_', ' ').upper()
        val_label = val.upper()
        prefix = 'NOT ' if negated else ''
        return f'{prefix}{var_label}: {val_label}'

    # Handle != comparisons
    neq_match = re.match(r'(\w+)\s*!=\s*"([^"]+)"', normalized)
    if neq_match:
        var, val = neq_match.groups()
        return f'NOT {var.replace("_", " ").upper()}: {val.upper()}'

    # Handle > < comparisons
    cmp_match = re.match(r'(not\s+)?(\w+)\s*(>|<|>=|<=)\s*(\d+)', normalized)
    if cmp_match:
        negated, var, op, num = cmp_match.groups()
        var_label = var.replace('_', ' ').upper()
        op_labels = {'>': 'OVER', '<': 'UNDER', '>=': 'AT LEAST', '<=': 'AT MOST'}
        prefix = 'NOT ' if negated else ''
        return f'{prefix}{var_label} {op_labels.get(op, op)} {num}'

    # Handle simple negation
    if normalized.startswith('not '):
        inner = normalized[4:].strip()
        if inner in CONDITION_LABELS:
            return f'NOT {CONDITION_LABELS[inner]}'
        return f'NOT {inner.replace("_", " ").upper()}'

    # Fallback: clean up the condition text
    label = cond.replace('"', '').replace("'", "").replace('==', ':')
    label = label.replace('_', ' ').upper().strip()
    return label


def extract_text_from_paragraph(p_elem):
    """Extract concatenated text from all runs in a paragraph."""
    texts = []
    for t in p_elem.iter(f'{W}t'):
        if t.text:
            texts.append(t.text)
    return ''.join(texts)


def defragment_jinja_in_paragraph(p_elem):
    """
    Defragment Jinja expressions that are split across multiple XML runs.

    Walk through all runs, concatenate text to find complete Jinja expressions,
    then consolidate each expression into a single run.
    """
    # Get all direct child elements (runs, proofErr, etc.)
    runs = list(p_elem)

    # First pass: collect all text content with positions
    text_segments = []  # (run_element, text_content, is_run)
    for elem in runs:
        if elem.tag == f'{W}r':
            t_elems = elem.findall(f'{W}t')
            for t in t_elems:
                if t.text:
                    text_segments.append((elem, t, t.text))

    if not text_segments:
        return

    # Concatenate all text
    full_text = ''.join(seg[2] for seg in text_segments)

    # Find all Jinja expressions
    jinja_pattern = re.compile(r'\{\{.*?\}\}|\{%.*?%\}', re.DOTALL)
    matches = list(jinja_pattern.finditer(full_text))

    if not matches:
        return

    # For each match, find which runs it spans and consolidate
    # Build a map: char_offset → (run_element, t_element)
    char_map = []  # (global_offset, run_elem, t_elem, local_offset)
    global_offset = 0
    for run_elem, t_elem, text in text_segments:
        for i, ch in enumerate(text):
            char_map.append((global_offset, run_elem, t_elem, i))
            global_offset += 1

    # Process matches in reverse order to preserve offsets
    for match in reversed(matches):
        start, end = match.start(), match.end()
        expr_text = match.group()

        if start >= len(char_map) or end - 1 >= len(char_map):
            continue

        # Find the first run containing this expression
        first_run = char_map[start][1]
        first_t = char_map[start][2]

        # Find all runs involved
        involved_runs = set()
        for i in range(start, min(end, len(char_map))):
            involved_runs.add(id(char_map[i][1]))

        if len(involved_runs) <= 1:
            # Already in a single run, no defragmentation needed
            continue

        # Get the formatting from the first run
        rpr = first_run.find(f'{W}rPr')

        # Replace text in first run's t element with the full expression
        # But we need to handle the text before and after the expression in this run
        first_local_start = char_map[start][3]
        first_t_text = first_t.text or ''
        before_text = first_t_text[:first_local_start]

        # Find the last char in the expression
        last_idx = min(end - 1, len(char_map) - 1)
        last_run = char_map[last_idx][1]
        last_t = char_map[last_idx][2]
        last_local_end = char_map[last_idx][3] + 1
        last_t_text = last_t.text or ''
        after_text = last_t_text[last_local_end:]

        # Set first t element to: before_text + expr_text + (after if same run, else empty)
        if first_run == last_run and first_t == last_t:
            first_t.text = before_text + expr_text + after_text
        else:
            first_t.text = before_text + expr_text

            # Clear text from intermediate runs
            for i in range(start + 1, min(end, len(char_map))):
                run_e = char_map[i][1]
                t_e = char_map[i][2]
                if run_e != first_run or t_e != first_t:
                    if i == last_idx and t_e == last_t:
                        t_e.text = after_text if after_text else ''
                    elif t_e.text and id(run_e) in involved_runs:
                        # Only clear if this is a middle run
                        pass  # Will be handled below

            # Clear all text in involved runs except the first
            seen_runs = set()
            for i in range(start, min(end, len(char_map))):
                run_e = char_map[i][1]
                t_e = char_map[i][2]
                run_id = id(run_e)
                if run_id != id(first_run) and run_id not in seen_runs:
                    # Clear this run's text
                    for t in run_e.findall(f'{W}t'):
                        if t == last_t and run_e == last_run:
                            t.text = after_text
                        else:
                            t.text = ''
                    seen_runs.add(run_id)

        if first_t.text:
            first_t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')


def replace_jinja_variables(text, var_map):
    """Replace {{ variable|filter }} expressions with [PLACEHOLDER]."""

    def replace_var(match):
        expr = match.group(1).strip()
        # Try exact match first
        if expr in var_map:
            return var_map[expr]

        # Handle format expressions like "${:,.2f}".format(var)
        # Also handles arithmetic: "${:,.2f}".format(loan_amount-holdback_amount)
        fmt_match = re.search(r'\.format\(([^)]+)\)', expr)
        if fmt_match:
            inner = fmt_match.group(1).strip()
            # Check if it's a simple variable
            if inner in var_map:
                return var_map[inner]
            # Check if it's arithmetic (e.g., loan_amount-holdback_amount)
            arith_vars = re.findall(r'\w+', inner)
            if arith_vars:
                parts = []
                for v in arith_vars:
                    if v in var_map:
                        parts.append(var_map[v].strip('[]'))
                    else:
                        parts.append(v.replace('_', ' ').upper())
                return f'[{"−".join(parts)}]'

        # Handle num2words filter with various formats
        nw_match = re.match(r'(\w+)\|num2words(?:\(.*?\))?', expr)
        if nw_match:
            var_name = nw_match.group(1)
            base = var_map.get(var_name, f'[{var_name.replace("_", " ").upper()}]')
            # Add WORDS suffix if not already present
            if 'WORDS' not in base:
                return base.replace(']', ' WORDS]')
            return base

        # Handle dateformat filter
        df_match = re.match(r'(\w+)\|dateformat(?:\(.*?\))?', expr)
        if df_match:
            var_name = df_match.group(1)
            if var_name in var_map:
                return var_map[var_name]
            return f'[{var_name.replace("_", " ").upper()}]'

        # Handle |upper filter
        upper_match = re.match(r'(\w+)\|upper', expr)
        if upper_match:
            key = f'{upper_match.group(1)}|upper'
            if key in var_map:
                return var_map[key]
            var_name = upper_match.group(1)
            if var_name in var_map:
                return var_map[var_name].replace(']', ' CAPS]')
            return f'[{var_name.replace("_", " ").upper()} CAPS]'

        # Handle |lower filter
        lower_match = re.match(r'(\w+)\|lower', expr)
        if lower_match:
            key = f'{lower_match.group(1)}|lower'
            if key in var_map:
                return var_map[key]
            var_name = lower_match.group(1)
            if var_name in var_map:
                return var_map[var_name]
            return f'[{var_name.replace("_", " ").upper()}]'

        # Handle any other filter
        filter_match = re.match(r'(\w+)\|(\w+)', expr)
        if filter_match:
            var_name = filter_match.group(1)
            if var_name in var_map:
                return var_map[var_name]

        # Handle dot notation (e.g., pg.name, folio.folio_number)
        dot_match = re.match(r'(\w+)\.(\w+)', expr)
        if dot_match:
            collection, field = dot_match.groups()
            # Common patterns
            if field == 'name':
                return f'[{collection.upper()} NAME]'
            if field == 'folio_number':
                return '[FOLIO NUMBER]'
            if field == 'entity':
                return f'[{collection.upper()} ENTITY TYPE]'
            if field == 'state':
                return f'[{collection.upper()} STATE]'
            if field == 'trustee_name':
                return f'[{collection.upper()} TRUSTEE NAME]'
            if field == 'trust_agreement_date':
                return f'[{collection.upper()} TRUST DATE]'
            return f'[{collection.upper()} {field.replace("_", " ").upper()}]'

        # Simple variable lookup
        if expr in var_map:
            return var_map[expr]

        # Fallback: generate placeholder from variable name
        clean = re.sub(r'\|.*', '', expr)  # strip filters
        clean = re.sub(r'"[^"]*"\.format\(([^)]+)\)', r'\1', clean)  # extract from format()
        clean = clean.strip().replace('_', ' ').upper()
        if clean:
            return f'[{clean}]'
        return match.group()  # keep original if nothing extracted

    return re.sub(r'\{\{\s*(.*?)\s*\}\}', replace_var, text)


def process_control_structure(text):
    """
    Process {% %} control structures.
    Returns (action, label) where action is 'if_start', 'endif', 'else', 'elif',
    'for_start', 'endfor', 'set', or None.
    """
    match = re.match(r'\{%-?\s*(if|elif|else|endif|for|endfor|set)\s*(.*?)\s*-?%\}', text, re.DOTALL)
    if not match:
        return None, None, None

    keyword = match.group(1)
    body = match.group(2).strip()

    if keyword == 'if':
        label = get_label_for_condition(body)
        return 'if_start', label, body
    elif keyword == 'elif':
        label = get_label_for_condition(body)
        return 'elif', label, body
    elif keyword == 'else':
        return 'else', None, None
    elif keyword == 'endif':
        return 'endif', None, None
    elif keyword == 'for':
        # e.g., "pg in personal_guarantors"
        return 'for_start', body, body
    elif keyword == 'endfor':
        return 'endfor', None, None
    elif keyword == 'set':
        return 'set', body, body
    return None, None, None


def process_paragraph_text(text, var_map, if_stack):
    """
    Process a paragraph's text: replace variables, handle control structures.
    Returns the processed text and updates if_stack.
    """
    result_parts = []
    pos = 0

    # Find all Jinja expressions
    pattern = re.compile(r'(\{\{.*?\}\}|\{%.*?%\})', re.DOTALL)

    for match in pattern.finditer(text):
        # Add text before this expression
        before = text[pos:match.start()]
        if before:
            result_parts.append(before)

        expr = match.group()
        pos = match.end()

        if expr.startswith('{{'):
            # Variable expression → replace with placeholder
            replaced = replace_jinja_variables(expr, var_map)
            result_parts.append(replaced)
        elif expr.startswith('{%'):
            # Control structure
            action, label, body = process_control_structure(expr)

            if action == 'set':
                # Strip {% set %} directives entirely
                pass
            elif action == 'if_start':
                if_stack.append({'label': label, 'condition': body, 'has_else': False})
                result_parts.append(f'[IF: {label}]')
            elif action == 'elif':
                # Close previous branch, open new one
                if if_stack:
                    prev = if_stack[-1]
                    result_parts.append(f'[END IF: {prev["label"]}]')
                    prev['label'] = label
                    prev['condition'] = body
                result_parts.append(f'[IF: {label}]')
            elif action == 'else':
                if if_stack:
                    prev = if_stack[-1]
                    old_label = prev['label']
                    result_parts.append(f'[END IF: {old_label}]')
                    prev['has_else'] = True
                    # Try to infer the else label
                    cond = prev.get('condition', '')
                    if cond.startswith('not '):
                        else_label = get_label_for_condition(cond[4:])
                    elif '==' in cond:
                        else_label = f'NOT {old_label}'
                    else:
                        else_label = get_label_for_condition(f'not {cond}')
                    prev['label'] = else_label
                    prev['condition'] = f'not ({cond})'
                    result_parts.append(f'[IF: {else_label}]')
            elif action == 'endif':
                if if_stack:
                    prev = if_stack.pop()
                    result_parts.append(f'[END IF: {prev["label"]}]')
            elif action == 'for_start':
                # For loops: insert a marker showing repetition
                for_match = re.match(r'(\w+)\s+in\s+(\w+)', body or '')
                if for_match:
                    item_var = for_match.group(1)
                    collection = for_match.group(2)
                    label_text = collection.replace('_', ' ').upper()
                    if_stack.append({'label': f'EACH {label_text}', 'is_for': True})
                    result_parts.append(f'[FOR EACH: {label_text}]')
            elif action == 'endfor':
                if if_stack and if_stack[-1].get('is_for'):
                    prev = if_stack.pop()
                    result_parts.append(f'[END FOR EACH: {prev["label"].replace("EACH ", "")}]')

    # Add remaining text
    remaining = text[pos:]
    if remaining:
        result_parts.append(remaining)

    return ''.join(result_parts)


def process_document(tree, var_map):
    """Process the entire document XML tree."""
    root = tree.getroot()
    if_stack = []

    # First: defragment Jinja across all paragraphs
    for p in root.iter(f'{W}p'):
        defragment_jinja_in_paragraph(p)

    # Second: remove proofErr elements (they interfere and aren't needed)
    for proof_err in root.iter(f'{W}proofErr'):
        parent = proof_err.getparent()
        if parent is not None:
            parent.remove(proof_err)

    # Third: process text in each run
    for p in root.iter(f'{W}p'):
        for r in p.findall(f'{W}r'):
            for t in r.findall(f'{W}t'):
                if t.text:
                    t.text = process_paragraph_text(t.text, var_map, if_stack)
                    t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')

    # Fourth: remove empty runs
    for p in root.iter(f'{W}p'):
        for r in list(p.findall(f'{W}r')):
            has_text = False
            for t in r.findall(f'{W}t'):
                if t.text and t.text.strip():
                    has_text = True
                    break
            # Also check for other content (images, tabs, breaks)
            has_other = (r.find(f'{W}tab') is not None or
                        r.find(f'{W}br') is not None or
                        r.find(f'{W}drawing') is not None or
                        r.find(f'{W}sym') is not None)
            if not has_text and not has_other:
                # Check if this run has only empty t elements
                t_elems = r.findall(f'{W}t')
                if t_elems and all((t.text is None or t.text == '') for t in t_elems):
                    p.remove(r)

    return tree


def convert_template(input_path, output_path, var_map=None):
    """Main conversion function."""
    if var_map is None:
        var_map = COMMITMENT_LETTER_MAP

    print(f"Converting: {input_path}")
    print(f"Output: {output_path}")

    # Create a temp directory for working
    with tempfile.TemporaryDirectory() as tmpdir:
        # Extract the docx
        extract_dir = os.path.join(tmpdir, 'extracted')
        with zipfile.ZipFile(input_path, 'r') as zf:
            zf.extractall(extract_dir)

        # Collect all XML files to process: document.xml + headers + footers
        word_dir = os.path.join(extract_dir, 'word')
        xml_files_to_process = [os.path.join(word_dir, 'document.xml')]
        for fname in os.listdir(word_dir):
            if re.match(r'(header|footer)\d*\.xml', fname):
                xml_files_to_process.append(os.path.join(word_dir, fname))

        parser = etree.XMLParser(remove_blank_text=False)
        for xml_path in xml_files_to_process:
            if not os.path.exists(xml_path):
                continue
            tree = etree.parse(xml_path, parser)
            tree = process_document(tree, var_map)
            tree.write(xml_path, xml_declaration=True, encoding='UTF-8', standalone=True)

        # Repack as docx
        os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            for root_dir, dirs, files in os.walk(extract_dir):
                for file in files:
                    file_path = os.path.join(root_dir, file)
                    arcname = os.path.relpath(file_path, extract_dir)
                    zf.write(file_path, arcname)

    print(f"Done! Created: {output_path}")

    # Print summary
    with zipfile.ZipFile(output_path, 'r') as zf:
        all_xml = ''
        for name in zf.namelist():
            if name == 'word/document.xml' or re.match(r'word/(header|footer)\d*\.xml', name):
                all_xml += zf.read(name).decode('utf-8')
        placeholders = re.findall(r'\[([A-Z][A-Z /\$%\-]+)\]', all_xml)
        if_markers = re.findall(r'\[(?:IF|END IF|FOR EACH|END FOR EACH): ([^\]]+)\]', all_xml)
        remaining_jinja_vars = re.findall(r'\{\{.*?\}\}', all_xml)
        remaining_jinja_ctrl = re.findall(r'\{%.*?%\}', all_xml)

        print(f"\nSummary:")
        print(f"  Placeholders found: {len(placeholders)}")
        print(f"  Unique placeholders: {len(set(placeholders))}")
        print(f"  IF/FOR markers: {len(if_markers)}")
        print(f"  Remaining {{ }} expressions: {len(remaining_jinja_vars)}")
        print(f"  Remaining {{% %}} expressions: {len(remaining_jinja_ctrl)}")

        if remaining_jinja_vars:
            print(f"\n  Unconverted variables:")
            for v in set(remaining_jinja_vars):
                print(f"    {v}")

        if remaining_jinja_ctrl:
            print(f"\n  Unconverted control structures:")
            for c in set(remaining_jinja_ctrl[:20]):
                print(f"    {c}")


def verify_template(output_path):
    """Verify a converted template for completeness and correctness."""
    print(f"\n{'='*60}")
    print(f"VERIFICATION: {os.path.basename(output_path)}")
    print(f"{'='*60}")

    issues = []

    with zipfile.ZipFile(output_path, 'r') as zf:
        all_xml = ''
        for name in zf.namelist():
            if name == 'word/document.xml' or re.match(r'word/(header|footer)\d*\.xml', name):
                all_xml += zf.read(name).decode('utf-8')

    # Check remaining Jinja
    remaining_vars = re.findall(r'\{\{.*?\}\}', all_xml)
    remaining_ctrl = re.findall(r'\{%.*?%\}', all_xml)
    if remaining_vars:
        issues.append(f"  FAIL: {len(remaining_vars)} remaining {{{{ }}}} expression(s)")
        for v in sorted(set(remaining_vars)):
            issues.append(f"        {v}")
    else:
        print("  PASS: Zero remaining {{ }} expressions")

    if remaining_ctrl:
        issues.append(f"  FAIL: {len(remaining_ctrl)} remaining {{% %}} expression(s)")
        for c in sorted(set(remaining_ctrl)):
            issues.append(f"        {c}")
    else:
        print("  PASS: Zero remaining {% %} expressions")

    # Check IF/END IF matching
    if_starts = re.findall(r'\[IF: ([^\]]+)\]', all_xml)
    if_ends = re.findall(r'\[END IF: ([^\]]+)\]', all_xml)
    if len(if_starts) == len(if_ends):
        print(f"  PASS: IF/END IF balanced ({len(if_starts)} pairs)")
    else:
        issues.append(f"  WARN: IF/END IF mismatch — {len(if_starts)} opens vs {len(if_ends)} closes")

    # Check FOR EACH/END FOR EACH matching
    for_starts = re.findall(r'\[FOR EACH: ([^\]]+)\]', all_xml)
    for_ends = re.findall(r'\[END FOR EACH: ([^\]]+)\]', all_xml)
    if len(for_starts) == len(for_ends):
        print(f"  PASS: FOR EACH/END FOR EACH balanced ({len(for_starts)} pairs)")
    else:
        issues.append(f"  WARN: FOR EACH mismatch — {len(for_starts)} opens vs {len(for_ends)} closes")

    # Count placeholders
    placeholders = re.findall(r'\[([A-Z][A-Z0-9 /\$%\-]+)\]', all_xml)
    unique_ph = sorted(set(placeholders))
    print(f"  INFO: {len(placeholders)} placeholders ({len(unique_ph)} unique)")

    if issues:
        print("\n  ISSUES:")
        for i in issues:
            print(i)
        return False
    else:
        print("  RESULT: ALL CHECKS PASSED")
        return True


def batch_convert(input_dir, output_dir, skip=None, var_map=None):
    """Batch convert all .docx templates in input directory."""
    if var_map is None:
        var_map = COMMITMENT_LETTER_MAP
    if skip is None:
        skip = []

    templates = sorted([
        f for f in os.listdir(input_dir)
        if f.endswith('.docx') and not f.startswith('~$')
    ])

    print(f"Found {len(templates)} templates in {input_dir}")
    print(f"Skipping: {skip}")
    print(f"{'='*60}\n")

    success = []
    failed = []
    skipped = []

    for fname in templates:
        if fname in skip:
            skipped.append(fname)
            print(f"SKIP: {fname}")
            continue

        input_path = os.path.join(input_dir, fname)
        output_path = os.path.join(output_dir, fname)

        try:
            convert_template(input_path, output_path, var_map)
            success.append(fname)
        except Exception as e:
            failed.append((fname, str(e)))
            print(f"FAILED: {fname} — {e}")

    # Run verification on all successful conversions
    print(f"\n{'='*60}")
    print(f"BATCH VERIFICATION")
    print(f"{'='*60}")

    all_pass = True
    for fname in success:
        output_path = os.path.join(output_dir, fname)
        if not verify_template(output_path):
            all_pass = False

    # Print final summary
    print(f"\n{'='*60}")
    print(f"BATCH SUMMARY")
    print(f"{'='*60}")
    print(f"  Total templates: {len(templates)}")
    print(f"  Converted: {len(success)}")
    print(f"  Skipped: {len(skipped)}")
    print(f"  Failed: {len(failed)}")
    if failed:
        for fname, err in failed:
            print(f"    FAILED: {fname} — {err}")
    print(f"  All verifications passed: {all_pass}")

    return len(failed) == 0 and all_pass


def main():
    parser = argparse.ArgumentParser(
        description='Convert Jinja .docx template to clean maximum template'
    )
    parser.add_argument('input', nargs='?', help='Path to Jinja .docx template (single mode)')
    parser.add_argument('output', nargs='?', help='Path for output maximum template .docx (single mode)')
    parser.add_argument('--mapping', help='Path to JSON variable mapping file (optional)')
    parser.add_argument('--batch', action='store_true',
                        help='Batch mode: convert all .docx in input dir to output dir')
    parser.add_argument('--input-dir', default='jinja_templates',
                        help='Input directory for batch mode (default: jinja_templates)')
    parser.add_argument('--output-dir', default='new_templates',
                        help='Output directory for batch mode (default: new_templates)')
    parser.add_argument('--skip', nargs='*', default=[],
                        help='Filenames to skip in batch mode')
    parser.add_argument('--verify', help='Verify a single converted template')

    args = parser.parse_args()

    var_map = COMMITMENT_LETTER_MAP
    if args.mapping:
        with open(args.mapping) as f:
            var_map = json.load(f)

    if args.verify:
        verify_template(args.verify)
    elif args.batch:
        ok = batch_convert(args.input_dir, args.output_dir, args.skip, var_map)
        sys.exit(0 if ok else 1)
    elif args.input and args.output:
        convert_template(args.input, args.output, var_map)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()
