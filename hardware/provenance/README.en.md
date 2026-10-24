[עברית](README.md) · English

# Hardware package provenance, inventory and traceability

Source: [RoboParty rp1_hardware](https://github.com/Roboparty/rp1_hardware), pinned Git revision `18ca38832cde37a8a4349cff8fbb565f05c6f254`. The reference is retained for attribution and traceability of derivative designs; this repository contains no upstream submodule or Git dependency.

| Document | Role |
| --- | --- |
| [Final delivery inventory](delivery_inventory.json) | Final byte identity of all 550 source-mapped files after translation and repair |
| [Source file map](file_manifest.json) | All 550 source paths, working paths and source hashes; the initial export hash is not the post-translation output hash |
| [Path map](path_map.json) | One-to-one correspondence between upstream names and working names |
| [Part registry](part_registry.csv) | Upstream identifiers mapped to ROBOSKIN, keeping revisions and mirrored variants separate |
| [Translation report](translation_report.json) | PDF, spreadsheet, Office-document and archive translation operations |
| [Supplementary translations](supplemental_translation.json) | Supplemental review and removal of stale duplicate exports; canonical source-mapped files retained |
| [Branding changes](branding_changes.json) | Adapted text fields and preservation of upstream attribution |
| [STEP verification](step_geometry_checks.json) | 186 documents, 1,383 translated labels and unchanged non-text geometry stream |
| [Spreadsheet verification](office_numeric_checks.json) | 7,280 numeric cells in 49 spreadsheets compared with original source |
| [PDF annotation repair](pdf_glyph_repair_report.json) | Restored exact technical glyph outlines lost in text editing, without restoring source branding or Chinese |

Chinese source names in JSON records are encoded for traceability. They are not a substitute for translating working names and documents.

Manufacturing-directory counts: CNC — 303 files; 3D printing — 78; rubber — 20. All are included in the working tree. The source also includes documents, boards, harnesses and bills of materials.

The [original release assets](https://github.com/Roboparty/rp1_hardware/releases/tag/v0.1.0), including SolidWorks and Parasolid archives, are separate from the 550-file Git tree. They must not be presented as imported or adapted in this version.

License scope is detailed in the [licensing document](../LICENSES.en.md). The source permits adaptations subject to its terms; attribution does not make RoboParty a partner, sponsor or approver of ROBOSKIN.

The part registry includes three aliases requiring specification review before procurement: `ROBOSKIN.0369`, `ROBOSKIN.0370` and `ROBOSKIN.0371`. The last maps an incomplete mechanical identifier in the source; assigning a new number does not resolve the source ambiguity or authorize production.

Verify the final inventory from the repository root:

```bash
python3 tools/verify_hardware_inventory.py
```

## Reproducing checks and editing tools

Repository and inventory checks use only the Python standard library. PDF/table rendering tools were checked with `PyMuPDF 1.28.2` and `Pillow 12.3.0`, using `NotoSansHebrew-Regular.ttf` and `DejaVuSans.ttf` at the Linux paths specified in the scripts. Relevant rendering reports record font names and hashes.

The [STEP localization tool](../../tools/localize_step_labels.py) and [impedance table builder](../../tools/rebuild_impedance_tables.py) accept `--source` pointing to an unchanged source checkout. Without `--apply` they do not replace STEP files or archive members; the table builder still creates rendered artifacts for review. An approved change then requires an explicit delivery-inventory update with `--write`.

PDF repair tools reproduce documented repair stages; they are not general CAD converters. Repair plans identify source/intermediate versions and glyph coordinates. Use a working copy and backup directory appropriate to the recorded stage. Per-stage reports may contain intermediate hashes; `delivery_inventory.json` is authoritative for delivered file hashes.
