# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

ROBOSKIN: a standalone electronic-skin project for contact location, approximate contact intensity and sparse temperature sensing. Its thesis is a proof of concept: **removable panels over the rigid arm and leg segments, with gaps left for joint movement**, reporting over zoned CAN FD. Each panel stacks, outside in: a replaceable protective cover, two temperature points, a touch-sensing laminate, an insulating carrier and a local controller. The reference panel has 28 touch sites + 2 temperature points; the compact demo layout has 8 controllers, 88 sites and 16 temperature points.

The renders in `hardware/assets/images/skin-*.png` (and `docs/skin_visualizations*.md`) are design visualizations. Colours, coverage, cable routes and the exaggerated layer thicknesses illustrate the concept; they do not establish physical fit, so never take dimensions or claims from them. Geometry comes from `mechanics/` and the part drawings.

The repo also carries an imported, Hebrew-translated derivative of the RoboParty `rp1_hardware` package under `hardware/` (the base robot the skin is drawn on). Everything is Python 3.10+ **standard library only**; no install step, no third-party packages in CI.

## Commands

The CI sequence (`.github/workflows/verify.yml`), run from the repo root:

```bash
python3 tools/verify_repository.py                              # docs, links, filenames, estimates (see rules below)
python3 tools/verify_hardware_inventory.py                      # sha256 of all 550 imported hardware files
python3 -m unittest discover -s tests -v                        # software: protocol, events, wrench, observer
python3 -m unittest discover -s electronics -p 'test_*.py' -v   # circuit nets/pins vs exported netlists
python3 -m unittest discover -s mechanics -p 'test_*.py' -v     # stencil geometry, inertia
python3 -m software --demo                                      # 2 JSON lines: 88 sites fresh, then 0 after expiry
```

Single test: `python3 -m unittest tests.test_protocol.<Class>.<method>` (root-level `tests/` imports `software.*`). The `electronics/` and `mechanics/` tests import their siblings by bare module name, so run them via `discover -s <dir>` or from inside that directory.

`verify_repository.py` walks the **filesystem**, not `git ls-files`: any untracked `.md` or a stray `.gitmodules` in the working tree makes it fail. If it fails on files you did not create (e.g. sandbox placeholder files), run it against a clean export: `git archive HEAD | tar -x -C "$TMPDIR/x"`.

## Generated artifacts — regenerate, never hand-edit

| Output | Generator | Checked by |
|---|---|---|
| `engineering/model_results.json` | `python3 engineering/models.py > engineering/model_results.json` (inputs: `engineering/cost_inputs.csv`) | `verify_repository.py` compares it to `calculate()` |
| `electronics/{patch,region}_circuit.{json,net}`, `*_connections.csv` | `python3 electronics/build_circuit.py` (the circuit is defined in code there) | `electronics/test_circuit.py` |
| `assets/mechanics/*_template.svg`, `panel_profiles.json` | `python3 mechanics/generate_templates.py` | `mechanics/test_mechanics.py` |
| `hardware/provenance/delivery_inventory.json` | `python3 tools/verify_hardware_inventory.py --write`, only after a reviewed change to hardware files | the same script without `--write` |

Numbers derived from these (costs, site counts, test counts) are also quoted in the prose docs (`README*.md`, `docs/verification*.md`, `docs/release_status*.md`). Update both languages when they change.

## Documentation rules enforced by `tools/verify_repository.py`

- Hebrew is the primary language. Every `*.md` that is not `*.en.md`/`*.he.md` must begin with `<div dir="rtl" lang="he">`, contain Hebrew, have an English companion `*.en.md`, and be listed in `docs/languages.json`. `CLAUDE.md` is exempt.
- Fenced code blocks must be **identical** between the Hebrew and English versions.
- Filenames must be ASCII; no CJK characters in `.md/.json/.csv/.py/.svg/.scad/.net/.yml` (Chinese upstream names live only in encoded form in provenance JSON).
- Relative Markdown links must resolve on disk.
- `research/reference_index.json` must contain references 1–84 exactly once.
- No git submodules; `hardware/provenance/file_manifest.json` must map exactly 550 files, all present.

## Architecture

**`software/`** is a receive-side observer with no actuator path. `control_ready` and `actuation_enabled` are always false, and nothing subscribes to joint state. Keep it that way.
- `skin_protocol.py`: v2 binary frame codec, physical UID/boot-epoch identity, sequence checks, nonce-based clock sync (2.5 s lifetime, 2 s renew, 20 ms retry).
- `transport.py` + `can_wire.py`: Linux SocketCAN FD on dedicated `can_skin_<region>` interfaces; feeds decoded frames to the observer.
- `observer.py`: loads a commissioned config (`config/limb_skin.example.json`), applies per-patch installed-channel masks (28 wire slots, unused slots = 255), expires held samples (touch 40 ms, temperature 250 ms total) and emits `tectile_skin.observation.v1` JSON with an 89-features-per-patch vector.
- `skin_events.py`: producer-side send-on-delta reporter (Cheng et al. 2019); the baseline only advances on successful transmit.
- `skin_wrench.py`: pure wrench/frame math.
- `demo.py`: synthetic packets through the **real** codec and validation gate; `--demo` never opens a device.
- `software/README.en.md` is the contract (frame layout, masks, freshness rules, feature offsets). Read it before changing protocol or observer semantics.

**`electronics/`, `mechanics/`, `engineering/`** hold design specs as code: the pin-level circuit, the fit stencils and inertia, and the cost/timing model with embedded `assert`s. Their outputs are design artifacts, not ERC/DRC or physical validation, and the docs say so explicitly. Preserve that framing.

**`hardware/`** is imported content (STEP, PDF, Gerber, XLSX), pinned to upstream revision `18ca388…` and tracked byte-for-byte in `hardware/provenance/`. Changing any of those files means updating the matching provenance record and re-running `--write`. The `tools/` scripts other than the two verifiers are one-shot import and repair passes (STEP label localisation, PDF glyph repair, impedance-table rebuild). They need `pymupdf`/`Pillow`, are not part of CI, and should not be re-run casually because they rewrite imported binaries.

**`research/`** holds literature reviews over the 84-reference register. `templates/` holds RFQ, manifest and test-record templates.

## Conventions

- Docs keep an explicit "what is NOT proven" stance: offline tests, synthetic data, no physical sensor/board/fit validation. Do not upgrade claims without physical evidence.
- Commissioned configs (`commissioned*.json`) and `recordings/` are git-ignored on purpose.
