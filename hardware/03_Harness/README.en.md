[עברית](README.md) · English

# Wiring harnesses

This directory contains the harness bill of materials, 43 PDF drawings and a preparation and assembly specification.

| Document | Contents |
| --- | --- |
| [Bill of materials](ROBOSKIN_Harness_BOM.xlsx) | 42 harness types: name, conductor cross-section, connectors, contacts and quantities |
| [Manufacturing drawings](Drawings/) | Dimensions, orientations, tolerances and connections for each harness |
| [Assembly specification](Harness_Manufacturing_Specification.docx) | Preparation, terminations and tests |

Match each harness name to its drawing. ARM_10 refers to ARM_10_Signal_Cable.pdf. Do not infer one harness's connections from a similarly named harness.

The example controller supply cable uses 18AWG silicone wire and a male XT30 plug; its finished length is 120±5 mm. The battery-to-controller cable is a different harness, with 14AWG, XT60 and 300±10 mm.

[BODY01 drawing](Drawings/ROBOSKIN-BODY01-0_Cable.pdf) · [Robot bill of materials](../04_BOM/README.en.md) · [Hardware](../README.en.md)

## Complete harness drawing catalogue

Comparison with source revision `18ca38832cde37a8a4349cff8fbb565f05c6f254` confirms that all **46 source files** are in this repository: 43 PDF drawings, one BOM, one assembly specification and one README. The English README companion brings this directory to 47 files. The [source-to-delivery inventory](../provenance/delivery_inventory.json) records original and adapted paths.

Numbers 1–42 below are the first BOM worksheet's item numbers, not newly assigned part numbers. Quantities are copied from that sheet and total 60 harnesses; confirm their applicability to the robot configuration being built. The second sheet repeats items 35–42 and is not an additional quantity list. Each drawing has a direct link; to download it on GitHub, choose **Download raw file**.

| BOM item | Harness name and PDF drawing | BOM region | First-sheet quantity |
| --- | --- | --- | --- |
| 1 | [NX-to-head Ethernet](Drawings/NX_Ethernet_HEAD_Cable.pdf) | Head | 1 |
| 2 | [Head harness ROBOSKIN-HEAD1](Drawings/ROBOSKIN-HEAD1_Cable.pdf) | Head | 1 |
| 3 | [Head harness ROBOSKIN-HEAD2](Drawings/ROBOSKIN-HEAD2_Cable.pdf) | Head | 1 |
| 4 | [Head harness ROBOSKIN-HEAD3](Drawings/ROBOSKIN-HEAD3_Cable.pdf) | Head | 1 |
| 5 | [Body harness ROBOSKIN-BODY01-0](Drawings/ROBOSKIN-BODY01-0_Cable.pdf) | Main controller | 1 |
| 6 | [Body harness ROBOSKIN-BODY02-0](Drawings/ROBOSKIN-BODY02-0_Cable.pdf) | Main controller | 1 |
| 7 | [Body harness ROBOSKIN-BODY03-0](Drawings/ROBOSKIN-BODY03-0_Cable.pdf) | Main controller | 1 |
| 8 | [Body harness ROBOSKIN-BODY04-0](Drawings/ROBOSKIN-BODY04-0_Cable.pdf) | Main controller | 1 |
| 9 | [Body harness ROBOSKIN-BODY05-0](Drawings/ROBOSKIN-BODY05-0_Cable.pdf) | Main controller | 1 |
| 10 | [Body harness ROBOSKIN-BODY06-0](Drawings/ROBOSKIN-BODY06-0_Cable.pdf) | Main controller | 1 |
| 11 | [Body_ETH Ethernet](Drawings/Body_Ethernet_Cable.pdf) | Main controller | 2 |
| 12 | [Body-485 communication](Drawings/Body_RS485_Cable.pdf) | Main controller | 1 |
| 13 | [BODY-stop emergency stop](Drawings/BODY_Estop_Cable.pdf) | Main controller | 1 |
| 14 | [Lighting-board harness](Drawings/Lighting_Board_Cable.pdf) | Main controller | 1 |
| 15 | [Arm harness ROBOSKIN-ARM01-0](Drawings/ROBOSKIN-ARM01-0_Cable.pdf) | Arm / hand | 2 |
| 16 | [Arm harness ROBOSKIN-ARM02-0](Drawings/ROBOSKIN-ARM02-0_Cable.pdf) | Arm / hand | 2 |
| 17 | [Arm harness ROBOSKIN-ARM03-0](Drawings/ROBOSKIN-ARM03-0_Cable.pdf) | Arm / hand | 2 |
| 18 | [Arm harness ROBOSKIN-ARM04-0](Drawings/ROBOSKIN-ARM04-0_Cable.pdf) | Arm / hand | 2 |
| 19 | [Arm harness ROBOSKIN-ARM05-0](Drawings/ROBOSKIN-ARM05-0_Cable.pdf) | Arm / hand | 2 |
| 20 | [Arm harness ROBOSKIN-ARM06-0](Drawings/ROBOSKIN-ARM06-0_Cable.pdf) | Arm / hand | 2 |
| 21 | [Arm harness ROBOSKIN-ARM07-0](Drawings/ROBOSKIN-ARM07-0_Cable.pdf) | Arm / hand | 2 |
| 22 | [Arm harness ROBOSKIN-ARM08-0](Drawings/ROBOSKIN-ARM08-0_Cable.pdf) | Arm / hand | 2 |
| 23 | [ARM_10 signal cable](Drawings/ARM_10_Signal_Cable.pdf) | Arm / hand | 2 |
| 24 | [Hand adapter cable](Drawings/Hand_Adapter_Cable.pdf) | Arm / hand | 2 |
| 25 | [Leg harness ROBOSKIN-LEG01-0](Drawings/ROBOSKIN-LEG01-0_Cable.pdf) | Leg | 2 |
| 26 | [Leg harness ROBOSKIN-LEG02-0](Drawings/ROBOSKIN-LEG02-0_Cable.pdf) | Leg | 2 |
| 27 | [Leg harness ROBOSKIN-LEG03-0](Drawings/ROBOSKIN-LEG03-0_Cable.pdf) | Leg | 2 |
| 28 | [Leg harness ROBOSKIN-LEG04-0](Drawings/ROBOSKIN-LEG04-0_Cable.pdf) | Leg | 2 |
| 29 | [Leg harness ROBOSKIN-LEG05-0](Drawings/ROBOSKIN-LEG05-0_Cable.pdf) | Leg | 2 |
| 30 | [Leg harness ROBOSKIN-LEG06-0](Drawings/ROBOSKIN-LEG06-0_Cable.pdf) | Leg | 2 |
| 31 | [Leg harness ROBOSKIN-LEG07-0](Drawings/ROBOSKIN-LEG07-0_Cable.pdf) | Leg | 2 |
| 32 | [Back-GPIO signals](Drawings/Back_GPIO_Cable.pdf) | Back board | 1 |
| 33 | [Back-Key button](Drawings/Back_Key_Cable.pdf) | Back board | 1 |
| 34 | [Back-to-NX Ethernet](Drawings/Back_Ethernet_NX_Cable.pdf) | Back board | 1 |
| 35 | [BACK-POWER-NX supply](Drawings/BACK_POWER_NX_Cable.pdf) | Back board | 1 |
| 36 | [Battery-to-back-board supply](Drawings/Battery_to_Back_Power_Cable.pdf) | Back board | 1 |
| 37 | [Battery-to-main-controller supply](Drawings/Battery_to_Main_Power_Cable.pdf) | Back board | 1 |
| 38 | [Battery power cable](Drawings/Battery_Power_Cable.pdf) | Back board | 1 |
| 39 | [Long backup-battery protection cable](Drawings/Backup_Battery_Protection_Long_Cable.pdf) | Back board | 1 |
| 40 | [Short backup-battery protection cable](Drawings/Backup_Battery_Protection_Short_Cable.pdf) | Back board | 1 |
| 41 | [Power harness ROBOSKIN-POWER01-0](Drawings/ROBOSKIN-POWER01-0_Cable.pdf) | Waist | 1 |
| 42 | [Power harness ROBOSKIN-POWER02-0](Drawings/ROBOSKIN-POWER02-0_Cable.pdf) | Waist | 1 |
| No separate row | [Controller supply cable](Drawings/Controller_Supply_Cable.pdf) | Main controller | Not specified in BOM |

## Source discrepancies to resolve before manufacturing

- **ARM_10:** BOM item 23 specifies `28AWG`, whereas the original drawing specifies `22AWG`. The discrepancy is preserved and documented; obtain an agreed specification before ordering either size.
- **ROBOSKIN-POWER02-0:** the original drawing's material table and main dimension specify a `190 mm` total signal-wire length, while its pin-connection table states `260 mm`. Do not select the length by analogy with POWER01.
- **Controller supply cable:** the 43rd drawing is present but has no separate row among the 42 BOM harness types. Define its quantity and configuration assignment before issuing an order.

These are discrepancies found during the catalogue check, not engineering approval of every pin or current rating. Assembly requires cross-checking the matching drawing, BOM and preparation specification; verify connector viewing direction, polarity, continuity and absence of shorts before applying power. The skin-sensing subsystem has a separate wiring and quantity document linked below.

[Separate electronic-skin wiring](../../electronics/harness_connections.csv)
