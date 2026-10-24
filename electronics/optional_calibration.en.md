[עברית](optional_calibration.md) · English

# ROBOSKIN optional inertial calibration variant

The base skin has touch and temperature only. Add one six-axis IMU rigidly referenced to each of the eight example controllers if testing Cheng-style joint-axis/patch localization. This is a separately costed hardware/firmware variant. Eight inertial observations are not 88 independently moving taxel observations; assume a stable known patch-to-link transform only where the mounting is actually rigid.

Lab module: **Adafruit 4438, LSM6DSOX**. Manufacturer page lists$11.95,6-axis measurements, I²C/SPI and a25.6×17.8×4.6 mm board at1.7 g. Current availability differs between indexed pages, so the price is an observed list price, not a delivered quote. Eight modules plus$3 local leads and$5 mounting/test allowance each total**$159.60**, excluding firmware, synchronization, fixture and calibration engineering. Do not fold this into the base-skin cost or claim it gives automatic calibration without implementation. [Module and source design](https://www.adafruit.com/product/4438), [ST sensor datasheet](https://www.st.com/resource/en/datasheet/lsm6dsox.pdf).

Production-controller add-on wiring:

| Module connection | Controller connection | Rule |
|---|---|---|
| VIN |3V3 |Use3.3 V supply for this add-on; include its measured current in the node budget |
| GND |GND |Short local return |
| SCL |PA11, LQFP48 pin33, AF6 I2C2_SCL |Local≤50 mm; no I²C through the limb |
| SDA |PA12, LQFP48 pin34, AF6 I2C2_SDA |Local≤50 mm; inspect breakout pull-ups before adding parallel resistors |
| INT1 |PA4, LQFP48 pin15, EXTI4 |Timestamp sample-ready interrupt in the same hardware clock domain as skin samples |

These three MCU pins are unused in the base netlist and must be changed deliberately in the variant. Do not apply PA9/PA10 remapping, which conflicts with fault/service functions, and do not reassign the skin CAN RX/TX pins47/48. The peripheral mapping is documented in ST DS13560, table13; package33/34 follows table12. [ST MCU data](https://www.st.com/resource/en/datasheet/stm32g0b1vc.pdf).

Start with 416 Hz synchronized accelerometer/gyro output,±4 g and±500 degrees/s ranges; confirm register encodings, chip identity and timestamp/overrun behavior against the actual sensor revision. Use local I²C 400 kHz interrupt/DMA transfers and record sample-ready timestamps, sequence, scale, axis orientation and FIFO overruns. Keep raw data and joint encoder samples, not only fused orientation. A calibration mode must have its own declared packet format and measured CAN load; the base 64-byte touch frame does not contain an invented inertial payload.

Before fitting a model: six-face accelerometer calibration; stationary gyro bias at relevant temperatures; timestamp offset/drift measurement against joint encoder capture; verify sign/frame with a known small motion. Move one supported joint at a time within the mechanically validated narrow range, with repeatable slow velocity and adequate measurable angular acceleration. Compare gravity-subtracted/tangential acceleration with the model. A cell near an axis or insufficient excitation produces an unobservable radius; report this rather than returning a confident zero. Validate the inferred transforms against independent measured landmarks. Keep commissioning and robot command permissions separate.

A single central IMU cannot replace these eight spatial observations. Flexible sheet deformation also breaks a rigid-patch assumption; narrow panels and stable backing reduce that problem, while removing sensors to save cost makes some self-calibration claims unavailable.
