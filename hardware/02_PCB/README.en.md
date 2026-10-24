[עברית](README.md) · English

# Printed circuit boards - ROBOSKIN

[Hardware](../README.en.md) · [Robot bill of materials](../04_BOM/README.en.md) · [Harnesses](../03_Harness/README.en.md)

This directory contains manufacturing data for 14 board families in the hardware platform. Part numbers and revisions are based on the assembly-requirements documents. This is a manufacturing package, not a complete editable schematic source.

| Directory | Part number | Revision |
| --- | --- | --- |
| [USB3 flexible interconnect](01_USB3_Flexible_Interconnect/) | ROBOSKIN.0066 | V1.0 |
| [433 transmitter](02_RBE-COMM-433TX/) | ROBOSKIN.0041 | V1.0 |
| [Main controller](03_RBE-MAIN-RK3588S/) | ROBOSKIN.0073 | V1.6.1pro |
| [Fan](04_RBE-PWR-FAN/) | ROBOSKIN.0009 | V2.0 |
| [Hand adapter](05_RBE-PWR-HANDPlusPro/) | ROBOSKIN.0040 | V1.0 |
| [Head](06_RBE-PWR-HEAD/) | ROBOSKIN.0298 | V2.0 |
| [Backup and hot swap](07_RBE-PWR-HOTSWAP/) | ROBOSKIN.0064 | V2.0 |
| [Motor capacitors](08_RBE-PWR-MCAP/) | ROBOSKIN.0006 | V3.1 |
| [Battery adapter](09_RBE-PWR-MINGMEI-BC/) | ROBOSKIN.0008 | V1.1 |
| [Inertial sensor](10_RBE-SENS-IMU/) | ROBOSKIN.0007 | V1.0 |
| [Charger](11_RBE_PWR_140WCHG/) | ROBOSKIN.0042 | V1.0 |
| [Rear hub](12_RBE_PWR_BACKHUB/) | ROBOSKIN.0297 | V2.1 |
| [Lighting](13_Lighting_Board/) | ROBOSKIN.0010 | V2.0 |
| [Rear power indicator](14_Rear_Power_Indicator/) | ROBOSKIN.0056 | V1.0 |

| Prefix | Format | Use |
| --- | --- | --- |
| 01_BOM | XLSX | Components and quantities for one board |
| 02_Gerber | ZIP | Circuit manufacturing data |
| 03_3D | STEP / ZIP | Mechanical envelope and assembled-volume reference |
| 04_CPL | XLSX | Component placement coordinates |
| 05_Assembly_Requirements | XLSX / PDF | Manufacturing requirements, part number and revision |
| 06_PCB_PDF | PDF | Board view |

The board component list describes one board. The robot bill of materials specifies which boards and quantities the configuration requires. Use files from the same revision for purchasing and assembly.

C30 on the HEAD board and R59 on the 140WCHG board are not populated. The [HEAD instructions](06_RBE-PWR-HEAD/README.en.md) and [140WCHG instructions](11_RBE_PWR_140WCHG/README.en.md) explain how to use NC_List.

The BACKHUB model is in the [STEP archive](12_RBE_PWR_BACKHUB/03_3D_BACKHUB_2026-09-28.zip). Extraction produces `03_3D_BACKHUB_2026-09-28.step`.

[BACKHUB V2.1 drawing](12_RBE_PWR_BACKHUB/06_PCB_PDF_BACKHUB_V2.1.pdf)

The reviewed source lacks a board component list for MINGMEI-BC. Hebrew names do not fill a missing manufacturing-data item. Graphics embedded in Gerber are not replaced automatically.

[New skin circuit design](../../electronics/README.en.md)
