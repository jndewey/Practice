# Scripts

## jinja_to_max_template.py

Converts Jinja-templated `.docx` files into maximum templates with bracketed placeholders and conditional markers.

**Features:**
- XML defragmentation — reassembles Jinja expressions split across Word XML runs
- 170+ variable mappings (`{{ var }}` → `[PLACEHOLDER]`)
- 200+ condition label mappings (`{% if condition %}` → `[IF: LABEL]`)
- Handles compound conditions (`and`/`or`), dot-notation (`entity.field`), vowel checks
- Processes headers, footers, and document body
- Batch mode with per-template error handling
- Verification/audit function

**Usage:**

```bash
# Single template
python jinja_to_max_template.py jinja_templates/My\ Template.docx templates/My\ Template.docx

# Batch conversion
python jinja_to_max_template.py --batch --input-dir ../jinja_templates --output-dir ../templates

# Verify a converted template
python jinja_to_max_template.py --verify templates/My\ Template.docx
```

## generate_documents.py

Batch document generation engine. Reads maximum templates and produces deal-specific documents with tracked changes.

**Engine capabilities:**
- Stack-based multi-paragraph conditional resolution (Pass A)
- Inline conditional resolution (Pass B)
- FOR EACH loop expansion for collections (guarantors, folios, etc.)
- Tracked changes: `<w:del>/<w:delText>` + `<w:ins>/<w:t>` with author/date
- Word comments via `word/comments.xml`
- Header/footer processing
- Table cell paragraph processing (signature blocks, schedules)
- Marker stripping from tracked deletions

**Configuration sections to customize:**
- `PLACEHOLDER_VALUES` — deal-specific placeholder → value mappings
- `CONDITION_KEEPS` — conditional label → True/False decisions
- `FOR_EACH` — collection data for repeating blocks
- `DEAL_FLAGS` — which documents to generate
- `COMMENTS` — review items to flag
- `select_documents()` — document selection logic

**Usage:**

```bash
python generate_documents.py
```

## generate_commitment_letter.py

Single-document generation script. Same engine as `generate_documents.py` but configured for a single commitment letter. Useful as a simpler starting point or reference implementation.

**Usage:**

```bash
python generate_commitment_letter.py
```

## Dependencies

- Python 3.9+
- `lxml` — XML processing (`pip install lxml`)
- Standard library: `zipfile`, `re`, `os`, `copy`, `datetime`
