[עברית](datasheet_traceability.md) · English

# ROBOSKIN circuit source register

Checked against manufacturer documents on 2026-10-25. The pin-level design uses the exact package/variant named below. Substituting a similar family member requires a fresh pin, voltage and behavior review. Connectivity checks do not replace PCB layout review or measurements.

| Circuit reference | Exact part / source | Design decision supported by source |
|---|---|---|
| U1 | [ST STM32G0B1, DS13560](https://www.st.com/resource/en/datasheet/stm32g0b1vc.pdf) | STM32G0B1CBT6, non-N LQFP48. Package pin table and alternate functions determine ADC, FDCAN, SWD and optional I2C2 assignments. |
| U2 | [TI TPS2553-1, SLVS841F](https://www.ti.com/lit/ds/symlink/tps2553-1.pdf) | DBV pins: IN 1, GND 2, EN 3, FAULT 4, ILIM 5, OUT 6. The **-1** variant latches off; the ordinary TPS2553 does not have the same fault response. A 200 kΩ current-setting resistor lies within the specified range; trip current must be measured over the intended conditions. |
| U3; region U_MON | [TI TPS7A24, SBVS386E](https://www.ti.com/lit/ds/symlink/tps7a24.pdf) | Fixed 3.3 V version: IN 1, GND 2, EN 3, NC 4, OUT 5. The manufacturer permits tying fixed-version NC to ground for thermal performance. EN is tied to IN. Effective output capacitance must meet the stability requirement after bias/temperature derating. |
| U4 | [TI TCAN3413, SLLSFS8A](https://www.ti.com/lit/ds/symlink/tcan3413.pdf) | SOIC8: TXD 1, GND 2, VCC 3, RXD 4, VIO 5, CANL 6, CANH 7, STB 8. VCC and VIO use 3.3 V. Hardware pull-up holds standby during reset. |
| U_MUX0–3 | [TI TMUX1308, SCDS426E](https://www.ti.com/lit/ds/symlink/tmux1308.pdf) | PW/TSSOP16: S0…S7 map to pins 13,14,15,12,1,5,2,4; D=3; EN=6 active low; 7=NC; 8=GND; A2/A1/A0=9/10/11; VDD=16. Keep sensor voltages within the normal supply range; fault injection behavior is not an operating mode. |
| D_A0–7 | [TI TPD4E1U06, SLVSBQ9E](https://www.ti.com/lit/ds/symlink/tpd4e1u06.pdf) | DBV/SOT23-6 protection channels on 1,6,3,4; ground 2; NC 5. Place at the connector with short discharge return paths. Part-level ESD ratings do not establish the skin system's immunity. |
| D_CAN | [Nexperia PESD2CANFD24V-T](https://assets.nexperia.com/documents/data-sheet/PESD2CANFD24V-T.pdf) | Two bus lines on pins 1/2 and shared return on 3, as the CAN application circuit shows. Avoid long ground loops and parallel protected/unprotected paths. |
| Y1 | [Abracon ASV oscillator](https://abracon.com/Oscillators/ASV.pdf) | Pin 1 enable, 2 ground/case, 3 output, 4 supply. ASV-8.000MHZ-LC-T selects 8 MHz, 3.3 V, −40…85 °C and ±50 ppm. HSE bypass configuration is required; this is an oscillator, not a bare crystal. |
| Region U_REG | [TI TPS2595, SLVSE57C](https://www.ti.com/lit/ds/symlink/tps2595.pdf) | TPS259530 is the 5.7 V clamp, active-high-enable, latch-off variant. dVdt 1, EN/UVLO 2, IN 3/4, OUT 5, FAULT 6, ILM 7, GND 8; exposed pad goes to ground. Pin 9 in the interchange netlist denotes that exposed pad. |
| Harness J1 / branch housing | [JST GH series](https://www.jst-mfg.com/product/pdf/eng/eGH.pdf) | BM04B-GHS-TBT header with GHR-04V-S housing and SSHL-002T-P0.2 contacts. Confirm terminal wire/insulation range, crimp tool and mating orientation. Electrical pin numbering alone is not a connector-view drawing. |
| Optional inertial variant | [ST LSM6DSOX](https://www.st.com/resource/en/datasheet/lsm6dsox.pdf), [Adafruit 4438 module](https://www.adafruit.com/product/4438) | Separate local IMU variant; its current, firmware, synchronization and calibration are not silently included in the base patch. |

There is no manufacturer datasheet for the custom printed taxel stack. Its resistance range, hysteresis, creep, aging, humidity response and laminate tolerances must come from the recorded coupon/lot measurements. A printed end-of-line resistor proves a conductor path, not an intact pressure-sensitive coating. The final film, connector and board combination must pass the acceptance sequence before the system can report usable skin coverage.
