# Real Estate Finance Practice

A collection of AI-assisted workflows, skills, prompts, and playbooks for commercial real estate finance — built to explore context engineering approaches with Claude Code.

## Repository Structure

```
.
├── context-engineering/        # Experiments with prompt design, context windows, and skill architecture
├── diligence/                  # Workflows, skills, and prompts for all due diligence workstreams
│   ├── matter-opening/         #   Closing agendas, matter intake checklists
│   ├── title-and-survey/       #   Title commitment and survey review (lender's perspective)
│   ├── zoning/                 #   Zoning diligence, compliance review, and loan document provisions
│   ├── entity-documents/       #   Org docs, SPE/bankruptcy remoteness, authority, good standing
│   ├── ucc-and-litigation-searches/  #   UCC, judgment, and litigation search review
│   ├── municipal-lien-searches/      #   Municipal and code violation lien searches
│   └── real-support-corporate-transactions/  #   Real estate support for healthcare M&A
├── drafting/                   # Claude Code for drafting legal documents
│   ├── skills/                 #   Reusable drafting skills
│   ├── prompts/                #   Prompt templates for document generation
│   └── workflows/              #   End-to-end drafting workflows
├── playbooks/                  # OB loan document playbooks — issue-spotting and negotiation guides
│   ├── construction-loan-agreements/  #   Construction loan negotiation cheat sheet
│   ├── mezzanine-loans-equity-pledges/  #   Mezzanine loans, equity pledges, intercreditor, UCC foreclosure
│   ├── mortgage/
│   ├── promissory-notes/
│   ├── alr/                    #   Assignment of Leases and Rents
│   └── guaranty/
├── document-assembly/          # Improving the OB document assembly workflow
├── procedures/                 # Workflow and procedures manuals
└── opinion-letters/            # Opinion letter generation and review workflows
    ├── opinion-generation/     #   Drafting third-party opinion letters (H&K form, Florida practice)
    └── opinion-review/         #   Reviewing opinions from lender's counsel perspective
```

## What's Here So Far

### Due Diligence

| Resource | Location | Description |
|----------|----------|-------------|
| Title & Survey Review Skill | `diligence/title-and-survey/` | Comprehensive title commitment annotation and survey review skill for lender representation. Includes Florida endorsement reference, standard lender requirements, special situations, and red flag checklists. |
| Entity Documents Due Diligence | `diligence/entity-documents/` | Skill for reviewing borrower entity formation, SPE requirements, bankruptcy remoteness, org doc checklists by entity type (LLC, corporation, partnership, JV), CTA compliance, and closing deliverables. |
| UCC Search Review | `diligence/ucc-and-litigation-searches/` | Systematic framework for ordering, reviewing, and dispositioning UCC lien search results in commercial mortgage lending. Covers debtor name verification, filing categorization, fixture filings, and SPE considerations. |
| Zoning Due Diligence | `diligence/zoning/` | Zoning compliance review framework covering permitted use, dimensional requirements, parking, certificates of occupancy, vested rights, flood zones, and loan document provisions checklist. |
| Real Estate for Healthcare M&A | `diligence/real-support-corporate-transactions/` | End-to-end guide for real estate counsel supporting large healthcare corporate transactions (asset acquisitions, stock purchases, mergers), from initial assessment through post-closing. |

### Playbooks

| Resource | Location | Description |
|----------|----------|-------------|
| Construction Loan Cheat Sheet | `playbooks/construction-loan-agreements/` | Negotiation guide covering 14 key provisions of construction loan agreements for residential condo projects (FL-focused). Includes lender, borrower, and market benchmark positions. |
| Mezzanine Loans & Equity Pledges | `playbooks/mezzanine-loans-equity-pledges/` | Comprehensive knowledge base covering mezzanine loan structure, pledge and security agreements, intercreditor agreements, UCC collateral documents, foreclosure remedies, and due diligence/closing checklists. |

### Opinion Letters

| Resource | Location | Description |
|----------|----------|-------------|
| Opinion Letter Generator | `opinion-letters/opinion-generation/` | Skill for generating transaction-specific third-party legal opinion letters based on the H&K standard form. Includes Florida customary practice guide, Appendix A (transaction-specific addenda), and Appendix B (Florida-specific provisions). |
| Opinion Letter Reviewer | `opinion-letters/opinion-review/` | Skill for reviewing borrower's counsel opinion letters from lender's counsel perspective. Includes section-by-section review checklist, common issues guide, and Florida-specific lender guidance. |

## Workstreams

### 1. Context Engineering Platform
Experiments with how to structure skills, prompts, and context for optimal Claude Code performance across real estate finance tasks.

### 2. Due Diligence Workflows
Skills and prompts for each stage of loan closing diligence — from matter opening through final title policy review.

### 3. Legal Document Drafting
Using Claude Code to draft and revise loan documents, with reusable skills and prompt templates.

### 4. OB Loan Document Playbooks
Issue-spotting and negotiation reference guides for each major loan document type in the OB lending practice.

### 5. Document Assembly Improvements
Streamlining the OB document assembly pipeline — templates, automation, and quality checks.

### 6. Workflow & Procedures Manuals
Standard operating procedures for recurring practice tasks.

### 7. Opinion Letters
Skills for both generating and reviewing third-party legal opinion letters, with Florida customary practice guidance, the H&K standard form, and a systematic review framework for lender's counsel.
