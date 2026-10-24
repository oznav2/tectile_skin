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

No upstream repository history, submodule, robot SDK or external robot manufacturing assets are part of this snapshot. Git records the exact published file revisions.
