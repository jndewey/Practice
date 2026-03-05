# Document Assembly

Automated loan document generation from Credit Approval Summaries (CAS). Converts Jinja-templated Word documents into "maximum templates" with bracketed placeholders and conditional markers, then generates deal-specific document sets with tracked changes for attorney review.

## How It Works

```
1. CONVERT               2. EXTRACT               3. GENERATE
Jinja templates    ──►   CAS (PDF)          ──►   Deal documents
   {{ var }}              AI reads & extracts       with tracked changes
   {% if %}               deal parameters           (del + ins + comments)
       │                       │                         │
       ▼                       ▼                         ▼
Maximum templates         Deal parameters          Attorney-ready drafts
   [PLACEHOLDER]          + condition flags         ready for accept/reject
   [IF: LABEL]            + document selection
```

### Three operations only:
1. **Replace** `[PLACEHOLDER]` with extracted value (tracked del + ins)
2. **Delete** inapplicable `[IF:]` blocks (tracked del)
3. **Flag** edge cases with Word comments

The output looks like an associate's redline: strikethrough for deletions, colored text for insertions, margin comments for review items.

## Quick Start

### Prerequisites

- Python 3.9+
- `lxml` (`pip install lxml`)

### Step 1: Convert Jinja Templates

Place your Jinja-templated `.docx` files in `jinja_templates/`, then run the converter:

```bash
python scripts/jinja_to_max_template.py --batch \
  --input-dir jinja_templates \
  --output-dir templates
```

This converts `{{ variable }}` and `{% if/for %}` syntax into `[PLACEHOLDER]` and `[IF: LABEL]`/`[END IF: LABEL]` markers. The converter includes 170+ variable mappings and 200+ condition label mappings. Unmapped variables get auto-generated placeholder names.

To verify a converted template:

```bash
python scripts/jinja_to_max_template.py --verify templates/My\ Template.docx
```

### Step 2: Configure Deal Data

Edit `scripts/generate_documents.py` to set your deal parameters:

- **`PLACEHOLDER_VALUES`** — maps each `[PLACEHOLDER]` to its deal-specific value
- **`CONDITION_KEEPS`** — maps each `[IF: LABEL]` to True (keep) or False (delete)
- **`FOR_EACH`** — data for repeating blocks (guarantors, folios, etc.)
- **`DEAL_FLAGS`** — controls which documents are generated
- **`COMMENTS`** — review items to flag with Word comments

The included configuration is a working example (Graham Companies $28M refinance) that demonstrates every feature.

### Step 3: Generate Documents

```bash
python scripts/generate_documents.py
```

Output lands in `output/` as `[Deal Name] - [Document Type].docx` files with full tracked changes.

## Directory Structure

```
document-assembly/
├── SKILL.md                          # Master skill — architecture, rules, XML reference
├── README.md                         # This file
├── jinja_templates/                  # Your Jinja-templated .docx files go here
├── templates/                        # Converted maximum templates (output of Step 1)
├── output/                           # Generated deal documents (output of Step 3)
├── scripts/
│   ├── jinja_to_max_template.py      # Jinja → maximum template converter
│   ├── generate_documents.py         # Batch document generation engine
│   ├── generate_commitment_letter.py # Single-document generation (reference)
│   └── README.md                     # Script details
└── skills/
    ├── cas_extraction_guide.md       # How to extract deal parameters from a CAS
    ├── annotation_format_spec.md     # Format spec for annotated template skills
    └── commitment_letter_skill.md    # Example: annotated skill for commitment letters
```

## Template Format

### Placeholders

| Pattern | Example | Action |
|---------|---------|--------|
| `[FIELD NAME]` | `[BORROWER NAME]` | Replace with CAS value via tracked change |
| `[$AMOUNT]` | `[$LOAN AMOUNT]` | Dollar amount: "$X,XXX,XXX.XX" |
| `[$AMOUNT WORDS]` | `[$LOAN AMOUNT WORDS]` | Spelled: "Five Million and No/100 Dollars" |
| `[a/an]` | | Grammatical article based on following word |
| `[[FIELD]]` | `[[CLOSING DATE]]` | Double-bracketed = not in CAS, attorney fills in |

### Conditional Markers

| Marker | Meaning |
|--------|---------|
| `[IF: LABEL]` | Start of conditional block |
| `[END IF: LABEL]` | End of conditional block |
| `[FOR EACH: COLLECTION]` | Start of repeating block |
| `[END FOR EACH: COLLECTION]` | End of repeating block |

**TRUE condition:** Delete markers only, keep content.
**FALSE condition:** Delete markers + all content between them.
**FOR EACH:** Duplicate content for each collection item, remove markers.

## Adapting for Your Templates

1. **Variable mappings** — If your Jinja templates use different variable names, add entries to `COMMITMENT_LETTER_MAP` in `jinja_to_max_template.py`
2. **Condition labels** — If the auto-generated labels aren't readable enough, add entries to `CONDITION_LABELS` in `jinja_to_max_template.py`
3. **Deal parameters** — Replace the example `PLACEHOLDER_VALUES` and `CONDITION_KEEPS` in `generate_documents.py` with your deal's data
4. **Document selection** — Update `select_documents()` and `DEAL_FLAGS` for your document set
5. **Annotated skills** — Create per-document skill files in `skills/` following the format in `annotation_format_spec.md`

## Key Design Decisions

- **Tracked changes, not regeneration.** The engine edits templates rather than generating from scratch. This preserves the firm's formatting, style, and boilerplate exactly.
- **Three operations constraint.** Replace, delete, flag. The AI never rewrites template language.
- **Comments over silence.** Ambiguous items get Word comments rather than silent assumptions. A comment costs 5 seconds to review; a wrong provision costs hours.
- **Table cell support.** The engine processes paragraphs inside tables (signature blocks, schedules), not just body-level paragraphs.
- **Marker stripping in deletions.** Struck-through text shows clean content, not raw `[IF:]` markers.

## References

- `SKILL.md` — Full architecture, invariant rules, XML editing reference, and workflow
- `skills/cas_extraction_guide.md` — CAS field extraction rules and document selection logic
- `skills/annotation_format_spec.md` — How to write annotated template skills
