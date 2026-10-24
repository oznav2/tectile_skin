# ROBOSKIN bench assembly and acceptance

## 1. Validate one passive sensor channel

Use a stationary fixture, an isolated current-limited supply, a DMM and calibrated resistor standards. Connect a 22 kΩ 1% resistor from 3.3 V to `SNS0`; connect the test sensor and a 100 kΩ end-of-line resistor in parallel from `SNS0` to ground. The end-of-line resistor belongs at the remote sensor location. Add 1 kΩ series resistance from `SNS0` to the mux input and 100 pF from that input to ground. Follow the repeated circuit in [patch_schematic.svg](../assets/electronics/patch_schematic.svg).

Start at 3.3 V with a 100 mA source limit. With a high-resistance unloaded sensor, the nominal divider voltage is 2.705 V. Opening the remote conductor should raise the measured voltage toward 3.3 V; reducing sensor resistance should lower it. Use open, 100 kΩ, 47 kΩ, 10 kΩ, 1 kΩ and short standards to establish the full range before testing printed film. A sustained short and a saturated contact can be indistinguishable; preserve that ambiguity in reported validity.

## 2. Validate analog selection and digitization

Fit one TMUX1308PWR on a verified TSSOP16 adapter. Connect VDD pin 16 to the analog 3.3 V rail, ground pin 8, common output pin 3 and address pins 11/10/9. EN pin 6 is active low; pin 7 is unconnected. The S0–S7 package order is **13, 14, 15, 12, 1, 5, 2, 4**. It is not sequential pin order. Fit distinct known resistors to the inputs and verify every address.

The MCU ADC path includes a 4.7 kΩ mux-output resistor and 100 pF ADC shunt. Start with 250 µs settling after address changes, including the required ADC acquisition time. Record loaded/unloaded transitions and increase settling only if measurements demand it. The ADC scan, timer, DMA and serial transport require MCU firmware; host Python code is not a flashable substitute. A development-board header number is not the controller's LQFP48 package pin number.

The four bank-reference dividers use top/bottom resistances 30k/10k, 15k/10k, 10k/15k and 10k/30k. For a 12-bit full scale of 4095, nominal codes are 1024, 1638, 2457 and 3071. Initial validity windows are ±80 counts. Distinct levels expose bank swaps and stuck addressing. Validate every sensing channel as well as these references.

With 22 kΩ bias and a 100 kΩ ±20% end-of-line path, nominal unloaded code is 3357. The total selected-path leakage allocation is **3 µA**, shared across mux, MCU, ESD devices, PCB contamination and surface leakage. Require the analog reference to remain at least 3.1 V. Initial open detection is above 3900 for three successive scans; the initial short/overload threshold is below 30. Clearing a latched service fault requires 100 good scans plus operator acknowledgment. These thresholds must survive the measured temperature/leakage tests; they are not permission to hide a broken trace by relaxing limits.

## 3. Build the controller and protected region

Transcribe [patch_circuit.json](patch_circuit.json) and [region_circuit.json](region_circuit.json) into a native EDA project with qualified package footprints. Review the complete schematic, unused pins, thermal pads, reference return, connector orientation, clock bypass mode and programmer connections. Run ERC, then route with continuous ground and short bypass/protection return paths, and run DRC. The supplied XML netlists do not perform these steps.

Order three assembled controllers first. Inspect solder joints and measure unpowered rail resistance. Power one from isolated 5.00 V with a 100 mA source limit. Measure `5V_NODE`, `3V3` and `3V3_A`; investigate excessive startup current before increasing the limit. Confirm the 8 MHz oscillator, reset behavior, CAN standby during reset and no back-power from UART or SWD. The debugger's 3.3 V pad is a voltage sense connection, not an extra supply input.

The regional TPS259530DSGR uses a 2.05 kΩ ILM resistor, 180 nF dVdt capacitor, 100 kΩ/39 kΩ enable divider and manual reset button. The separate input-side 3.3 V monitor rail keeps the fault indicator meaningful after the protected output turns off. Verify actual inrush, trip current and latch reset with a controlled load before connecting several patches. Component and pin details are in the [manufacturer source register](datasheet_traceability.md).

## 4. Assemble the communication harness

Use the endpoint table in [harness_connections.csv](harness_connections.csv). The trunk carries 5 V, ground, CANH and CANL. Use a nominal 120 Ω twisted pair for CAN and 24 AWG power conductors. A stationary prototype may use an appropriate stranded cable; moving use needs a specifically qualified bend/torsion-rated cable. No moving-cable lifetime is claimed here.

Create short 26 AWG branches, at most 50 mm, with GHR-04V-S housings and SSHL-002T-P0.2 contacts mating to BM04B-GHS-TBT headers. Verify wire/insulation range and use the contact manufacturer's crimp process. Do not force a 24 AWG conductor into the selected 26 AWG branch terminal. Preserve the continuous trunk at each tap. Label connector orientation and electrically check all numbered endpoints before power; the table's pin numbers are not a connector-view drawing.

Fit the two fixed 120 Ω 1% terminators at the near and far ends. Check approximately 60 Ω between CANH and CANL with power off. Connect the isolated CAN FD adapter, commission one node with its 96-bit UID and physical sensor map, and then add nodes individually. Test duplicate identities, stale data, invalid masks and removal/reinstallation. Disconnect supply before servicing these connectors.

## 5. Record acceptance evidence

| Test | Method | Initial acceptance target |
|---|---|---|
| Channel identity | Distinct standards on every sensor/reference input | No channel permutation or false simultaneous contact |
| Analog/leakage | Five controllers; standards above; 10/25/40 °C; minimum/maximum supply | At least 100 counts between measured idle/open distributions; 3 µA aggregate leakage allocation; references in their windows; settled repeatability within 20 counts |
| Temperature | Five assembled-channel temperatures between 10 and 60 °C, plus independent check points | Monotonic calibration; individual point locations recorded; surface temperature not inferred from two points |
| Loaded supply | Eight nodes at measured peak current; distal differential measurement | Regional input 4.75–5.25 V, ripple ≤100 mVpp at 20 MHz, protected distal LDO input ≥3.8 V |
| Node short | Controlled fault downstream of one node limiter | Other nodes retain valid supply/reporting or recover within the declared 40 ms design target; failed node stays invalid |
| Trunk short | Current-limited regional test fixture | Region latches off; separately protected regions remain valid |
| Power interruption | Controlled ramp down and back to 5 V | All lost coverage becomes stale/invalid; no assumed recovery until fresh identity/validity checks |
| Maximum bus load | Eight nodes, actual 2 m harness, real host and USB hub | Correct 1M/2M timing; record errors, loss, bus load and 99.9th-percentile data age against application budget |
| Mechanical interference | Bend mounted panel and exercise the intended cable route | No false contact caused by preload, cable strain or rubbing; no damaged latch/trace |
| Service | Remove one powered-off node and reinstall | Permanent trunk and both terminations survive; identity remains unambiguous |

Save raw data, fixture identity, component lots, firmware/build hashes and failures. A design target or simulation result is not a measured pass. The electronics are not a safety-rated contact-protection system.

## 6. Manufacturing sequence

Keep the printed sensing laminate, two-point thermal flex, assembled controller and protective cover as separately inspectable subassemblies. Do not route the 28 analog channels through a moving joint. Quote printed resistance, end-of-line tolerance, laminate adhesion, pressure hysteresis/creep, venting, protective-layer thickness, scrap, tooling, minimum order and 100% electrical test explicitly. The printed sheet remains an unquoted process-dependent cost assumption until real supplier samples and lot tests exist.

Use the removable keyed cassette to replace worn film without discarding the controller. Before scaling beyond three boards, pass the electrical tests with the actual laminate and cover, inspect three material lots and record assembly/programming/test time. Obtain quantity-specific prototype quotes: the published per-patch cost model assumes 1,000 patches and does not establish an eight-unit retail price.
