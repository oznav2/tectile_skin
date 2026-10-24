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

## Direct links to every manufacturing file

Checked against the source tree on 25 October 2026 at revision `18ca38832cde37a8a4349cff8fbb565f05c6f254`: **all 88 PCB-directory files** are present in this repository—85 manufacturing/support files and three README documents. Three English Markdown companions and an English MAIN assembly note bring this directory to 92 files. Adapted paths are recorded in the [source-to-delivery inventory](../provenance/delivery_inventory.json).

The table links directly to the files. To download a binary file on GitHub, choose **Download raw file**. Gerber archives contain board manufacturing outputs; they do not replace editable schematic sources.

| Board | Bill of materials | Manufacturing outputs | 3D model | Component placement | Assembly requirements | Board drawing |
| --- | --- | --- | --- | --- | --- | --- |
| [USB3 flexible interconnect](01_USB3_Flexible_Interconnect/) | [XLSX](01_USB3_Flexible_Interconnect/01_BOM_FPC_2026-09-18.xlsx) | [ZIP](01_USB3_Flexible_Interconnect/02_Gerber_FPC_2026-09-18.zip) | [STEP](01_USB3_Flexible_Interconnect/03_3D_FPC_2026-09-18.step) | [XLSX](01_USB3_Flexible_Interconnect/04_CPL_FPC_2026-09-18.xlsx) | [XLSX](01_USB3_Flexible_Interconnect/05_Assembly_Requirements_FPC.xlsx) | [PDF](01_USB3_Flexible_Interconnect/06_PCB_PDF_FPC_2026-09-18.pdf) |
| [433 transmitter](02_RBE-COMM-433TX/) | [XLSX](02_RBE-COMM-433TX/01_BOM_433TX_2026-09-20.xlsx) | [ZIP](02_RBE-COMM-433TX/02_Gerber_433TX_2026-09-20.zip) | [STEP](02_RBE-COMM-433TX/03_3D_433TX_2026-09-20.step) | [XLSX](02_RBE-COMM-433TX/04_CPL_433TX_2026-09-20.xlsx) | [XLSX](02_RBE-COMM-433TX/05_Assembly_Requirements_433TX.xlsx) | [PDF](02_RBE-COMM-433TX/06_PCB_PDF_433TX_2026-09-20.pdf) |
| [Main controller](03_RBE-MAIN-RK3588S/) | [XLSX](03_RBE-MAIN-RK3588S/01_BOM_MAIN_2026-09-18.xlsx) | [ZIP](03_RBE-MAIN-RK3588S/02_Gerber_MAIN_2026-09-18.zip) | [STEP](03_RBE-MAIN-RK3588S/03_3D_MAIN_2026-09-09.step) | [XLSX](03_RBE-MAIN-RK3588S/04_CPL_MAIN_2026-09-18.xlsx) | [XLSX](03_RBE-MAIN-RK3588S/05_Assembly_Requirements_MAIN.xlsx) | Absent upstream |
| [Fan](04_RBE-PWR-FAN/) | [XLSX](04_RBE-PWR-FAN/01_BOM_FAN_V2.0.xlsx) | [ZIP](04_RBE-PWR-FAN/02_Gerber_FAN_V2.0.zip) | [STEP](04_RBE-PWR-FAN/03_3D_FAN_V2.0.step) | [XLSX](04_RBE-PWR-FAN/04_CPL_FAN_V2.0.xlsx) | [XLSX](04_RBE-PWR-FAN/05_Assembly_Requirements_FAN_V2.0.xlsx) | [PDF](04_RBE-PWR-FAN/06_PCB_PDF_FAN_V2.0.pdf) |
| [Hand adapter](05_RBE-PWR-HANDPlusPro/) | [XLSX](05_RBE-PWR-HANDPlusPro/01_BOM_HAND_2026-09-09.xlsx) | [ZIP](05_RBE-PWR-HANDPlusPro/02_Gerber_HAND.zip) | [STEP](05_RBE-PWR-HANDPlusPro/03_3D_HAND.step) | [XLSX](05_RBE-PWR-HANDPlusPro/04_CPL_HAND.xlsx) | [XLSX](05_RBE-PWR-HANDPlusPro/05_Assembly_Requirements_HAND.xlsx) | [PDF](05_RBE-PWR-HANDPlusPro/06_PCB_PDF_HAND.pdf) |
| [Head](06_RBE-PWR-HEAD/) | [XLSX](06_RBE-PWR-HEAD/01_BOM_HEAD_2026-09-09.xlsx) | [ZIP](06_RBE-PWR-HEAD/02_Gerber_HEAD.zip) | [STEP](06_RBE-PWR-HEAD/03_3D_HEAD_2026-09-28.step) | [XLSX](06_RBE-PWR-HEAD/04_CPL_HEAD_2026-09-16.xlsx) | [XLSX](06_RBE-PWR-HEAD/05_Assembly_Requirements_HEAD.xlsx) | [PDF](06_RBE-PWR-HEAD/06_PCB_PDF_HEAD_2026-09-16.pdf) |
| [Backup and hot swap](07_RBE-PWR-HOTSWAP/) | [XLSX](07_RBE-PWR-HOTSWAP/01_BOM_HOTSWAP_2026-09-18.xlsx) | [ZIP](07_RBE-PWR-HOTSWAP/02_Gerber_HOTSWAP_2026-09-17.zip) | [STEP](07_RBE-PWR-HOTSWAP/03_3D_HOTSWAP_2026-09-18.step) | [XLSX](07_RBE-PWR-HOTSWAP/04_CPL_HOTSWAP_2026-09-18.xlsx) | [XLSX](07_RBE-PWR-HOTSWAP/05_Assembly_Requirements_HOTSWAP.xlsx) | [PDF](07_RBE-PWR-HOTSWAP/06_PCB_PDF_HOTSWAP_2026-09-18.pdf) |
| [Motor capacitors](08_RBE-PWR-MCAP/) | [XLSX](08_RBE-PWR-MCAP/01_BOM_MCAP_2026-09-07.xlsx) | [ZIP](08_RBE-PWR-MCAP/02_Gerber_MCAP.zip) | [STEP](08_RBE-PWR-MCAP/03_3D_MCAP_2026-09-16.step) | [XLSX](08_RBE-PWR-MCAP/04_CPL_MCAP_2026-09-16.xlsx) | [XLSX](08_RBE-PWR-MCAP/05_Assembly_Requirements_MCAP.xlsx) | [PDF](08_RBE-PWR-MCAP/06_PCB_PDF_MCAP_2026-09-16.pdf) |
| [Battery adapter](09_RBE-PWR-MINGMEI-BC/) | Absent upstream | [ZIP](09_RBE-PWR-MINGMEI-BC/02_Gerber_MINGMEI-BC.zip) | [STEP](09_RBE-PWR-MINGMEI-BC/03_3D_MINGMEI-BC_2026-09-16.step) | [XLSX](09_RBE-PWR-MINGMEI-BC/04_CPL_MINGMEI-BC_2026-09-16.xlsx) | [XLSX](09_RBE-PWR-MINGMEI-BC/05_Assembly_Requirements_MINGMEI-BC.xlsx) | [PDF](09_RBE-PWR-MINGMEI-BC/06_PCB_PDF_MINGMEI-BC_2026-09-16.pdf) |
| [Inertial sensor](10_RBE-SENS-IMU/) | [XLSX](10_RBE-SENS-IMU/01_BOM_IMU_2026-09-09.xlsx) | [ZIP](10_RBE-SENS-IMU/02_Gerber_IMU.zip) | [STEP](10_RBE-SENS-IMU/03_3D_IMU_2026-09-16.step) | [XLSX](10_RBE-SENS-IMU/04_CPL_IMU_2026-09-16.xlsx) | [XLSX](10_RBE-SENS-IMU/05_Assembly_Requirements_IMU.xlsx) | [PDF](10_RBE-SENS-IMU/06_PCB_PDF_IMU_2026-09-16.pdf) |
| [Charger](11_RBE_PWR_140WCHG/) | [XLSX](11_RBE_PWR_140WCHG/01_BOM_140WCHG_2026-09-09.xlsx) | [ZIP](11_RBE_PWR_140WCHG/02_Gerber_140WCHG.zip) | [STEP](11_RBE_PWR_140WCHG/03_3D_140WCHG_2026-09-16.step) | [XLSX](11_RBE_PWR_140WCHG/04_CPL_140WCHG_2026-09-16.xlsx) | [XLSX](11_RBE_PWR_140WCHG/05_Assembly_Requirements_140WCHG.xlsx) | [PDF](11_RBE_PWR_140WCHG/06_PCB_PDF_140WCHG_2026-09-16.pdf) |
| [Rear hub](12_RBE_PWR_BACKHUB/) | [XLSX](12_RBE_PWR_BACKHUB/01_BOM_BACKHUB_2026-09-14.xlsx) | [ZIP](12_RBE_PWR_BACKHUB/02_Gerber_BACKHUB_V2.1.zip) | [STEP / ZIP](12_RBE_PWR_BACKHUB/03_3D_BACKHUB_2026-09-28.zip) | [XLSX](12_RBE_PWR_BACKHUB/04_CPL_BACKHUB_V2.1.xlsx) | [PDF](12_RBE_PWR_BACKHUB/05_Assembly_Requirements_BACKHUB.pdf) | [PDF](12_RBE_PWR_BACKHUB/06_PCB_PDF_BACKHUB_V2.1.pdf) |
| [Lighting](13_Lighting_Board/) | [XLSX](13_Lighting_Board/01_BOM_LAMP_2026-09-07.xlsx) | [ZIP](13_Lighting_Board/02_Gerber_LAMP.zip) | [STEP](13_Lighting_Board/03_3D_LAMP_2026-09-16.step) | [XLSX](13_Lighting_Board/04_CPL_LAMP_2026-09-16.xlsx) | [XLSX](13_Lighting_Board/05_Assembly_Requirements_LAMP.xlsx) | [PDF](13_Lighting_Board/06_PCB_PDF_LAMP_2026-09-16.pdf) |
| [Rear power indicator](14_Rear_Power_Indicator/) | [XLSX](14_Rear_Power_Indicator/01_BOM_INDICATOR_2026-09-16.xlsx) | [ZIP](14_Rear_Power_Indicator/02_Gerber_INDICATOR.zip) | [STEP](14_Rear_Power_Indicator/03_3D_INDICATOR_2026-09-16.step) | [XLSX](14_Rear_Power_Indicator/04_CPL_INDICATOR_2026-09-16.xlsx) | [XLSX](14_Rear_Power_Indicator/05_Assembly_Requirements_INDICATOR.xlsx) | [PDF](14_Rear_Power_Indicator/06_PCB_PDF_INDICATOR_2026-09-16.pdf) |

Additional support files:

- FPC: [assembly reference photograph](01_USB3_Flexible_Interconnect/07_Assembly_Reference_FPC.jpg).
- MAIN: [assembly reference photograph](03_RBE-MAIN-RK3588S/07_Assembly_Reference_MAIN.jpg), [Hebrew assembly note](03_RBE-MAIN-RK3588S/07_Assembly_Reference_MAIN.txt) and [English assembly note](03_RBE-MAIN-RK3588S/07_Assembly_Reference_MAIN.en.txt).
- HEAD: [do-not-populate instructions](06_RBE-PWR-HEAD/README.en.md).
- 140WCHG: [do-not-populate instructions](11_RBE_PWR_140WCHG/README.en.md).

Source gaps are explicit: MINGMEI-BC has no board BOM, and MAIN has no separate PCB PDF. No native editable schematic or PCB-layout files occur in the source tree. Missing files have not been invented, and differing filename dates are preserved; verify revision compatibility against assembly requirements before ordering. The imported boards belong to the robot platform; the new skin-sensing circuits are documented separately at the link below.

[New skin circuit design](../../electronics/README.en.md)
