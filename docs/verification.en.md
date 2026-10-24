[עברית](verification.md) · English

# Offline verification record

Date: 2026-10-25. All checks below use synthetic inputs or design artifacts; none exercises a physical sensor, CAN adapter or actuator.

| Check | Result |
| --- | --- |
| Protocol, event reporting, wrench math and generic observer | 78 tests passed |
| Circuit connectivity and exported netlists | 8 tests passed |
| Generic mechanics and measured-inertia calculations | 7 tests passed |
| Synthetic observer demonstration | 88 available sites, followed by 0 after expiry |
| Document links, filenames and calculation snapshots | Checked by tools/verify_repository.py |
| Research register | References 1–84, each exactly once |

Reproduce from the repository root:

```bash
python3 tools/verify_repository.py
python3 -m unittest discover -s tests -v
python3 -m unittest discover -s electronics -p 'test_*.py' -v
python3 -m unittest discover -s mechanics -p 'test_*.py' -v
python3 -m software --demo
```

The software tests include rejected identity reuse, synchronization expiry, dropped sync retries, stale data, malformed masks, unavailable channels, overloaded contacts, temperature hold age and region faults. The mechanical tests compare generated geometry/accounting and physical inertia identities. Circuit tests check the design's explicit nets and pin constraints; they do not replace schematic ERC, PCB DRC or a powered board test.

These checks cover the original skin implementation and offline verification. The imported hardware package is documented separately in the [source register](../hardware/provenance/README.en.md); its inclusion does not turn these checks into physical robot validation. Git records the published file revisions.

## Documentation and imported-hardware checks

| Check | Result and scope |
| --- | --- |
| Markdown documentation | 29 Hebrew/English pairs; heading/table structure and code preserved; 30 plan navigation anchors in each language |
| Import completeness | All 550 source-tree files represented; CNC — 303, 3D printing — 78, rubber — 20 |
| STEP geometry | 186 documents including one archive member; 1,383 translated labels with unchanged non-string data streams |
| Manufacturing spreadsheets | 7,280 numeric cells in 49 spreadsheets identical to source |
| PCB and harness file access | All 88 source PCB files and all 46 source harness files are present and mapped; bilingual catalogues link directly to manufacturing and support assets |
| Overview image | Hebrew visual adaptation embedded in both landing pages; all 26 callouts recorded in both languages; no claim of pixel identity or geometric validation from the image |
| PDF technical information | 281 files and 384 source pages, including 380 positional-check pages; four redrawn architecture pages excluded; 27,167 eligible technical spans checked at original positions, with no unresolved collateral deletions |
| Archive images | All 15 archives inspected; the only two table images recreated in Hebrew, 82 values/blank cells checked, Gerber and drill files unchanged |

Per-stage reports and file hashes are in the [provenance register](../hardware/provenance/README.en.md). The PDF check distinguishes technical annotations from intentional identifier replacement and translated text; it does not certify that every translated note, baked-in graphic or tolerance has been requalified as engineering. SolidWorks release assemblies remain separate from the imported source tree, and Gerber silkscreen has not been redesigned.
