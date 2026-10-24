# ROBOSKIN · Electronic skin

[עברית](README.he.md) · [Detailed engineering plan](electronic_skin.md)

An independent electronic-skin project for contact location, approximate contact intensity and sparse temperature sensing. The design combines replaceable protected sensor sheets, local acquisition and a segmented CAN FD network.

The full reference patch has **28 touch sites and two temperature points**. An optional compact demonstration uses eight controllers with **88 installed touch sites and 16 temperature points**. Panel dimensions and counts are generic examples; they do not prove fit on a particular robot.

| Start here | Contents |
| --- | --- |
| [Engineering plan](electronic_skin.md) | Materials, circuits, firmware contract, calibration, manufacturing, costs, test phases, competition and Israeli partner research |
| [Electronics](electronics/README.md) | Editable pin-level circuits, connection tables, netlists, BOM, isolated 5 V bench supply and wiring |
| [Mechanics](mechanics/README.md) | Generic film templates, removable carrier, strain relief and mounting tests |
| [Software](software/README.md) | Protocol, event reporting, identity, timing, multi-region observer and synthetic demo |
| [Research register](research/reference_index.md) | All 84 requested references with explicit access and review depth |
| [Release status](docs/release_status.md) | What exists, what was checked and what still requires physical evidence |

Run the software without any hardware or additional Python packages:

```bash
python3 -m unittest discover -s tests -v
python3 -m software --demo
python3 engineering/models.py
```

The demo uses synthetic packets through the actual protocol gates: available coverage expires when measurements become stale. It opens no device and sends no actuator command. Live use requires independently commissioned identities, calibration and dedicated sensor interfaces.

The cost model uses a **$34.78 good-patch manufacturing allowance at 1,000 patches** and separately priced laboratory gateways. This is not a retail prototype quotation. The complete 80-patch laboratory-interface scenario is $7,852.40 before spare patches, tax, freight and engineering. See the detailed assumptions before using any number in a budget.

This repository contains original project implementations and academic citations. It has fresh Git history, no submodules, no robot SDK dependency and no bundled robot CAD or inherited robot manufacturing package. Filenames are English; Hebrew documentation is provided. Published sensing and control principles remain attributed to their research authors.

**Current state:** engineering prototype specification and tested host software. Sensor performance, routed PCBs, compiled board firmware, installed fit, durability and commercial readiness have not been demonstrated by the offline tests.
