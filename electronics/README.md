# ROBOSKIN sensing electronics

This is an independent, low-voltage sensing subsystem for modular electronic skin. A full patch measures 28 individual contact sites and two local temperatures. Each patch converts its signals locally and sends them over a four-wire power/CAN FD harness. The initial build uses an isolated, regulated **5 V bench supply**.

## What is provided

- [Patch circuit](patch_circuit.json), [pin connections](patch_circuit_connections.csv) and [circuit drawing](../assets/electronics/patch_schematic.svg): 222 components and 104 nets, including remote printed sensors and diagnostic resistors. The controller has 88 resistors and 52 capacitors; the 28 remote end-of-line resistors are additional.
- [Regional circuit](region_circuit.json), [regional connections](region_circuit_connections.csv) and [harness drawing](../assets/electronics/wiring_diagram.svg): protected supply, fault indicator, manual reset, two fixed terminations and eight distributed taps on a continuous linear trunk.
- [Harness endpoint table](harness_connections.csv), [supply contract](supply_contract.json), [assembly and acceptance](assembly_and_acceptance.md), [manufacturer source register](datasheet_traceability.md), [component cost inputs](patch_cost_inputs.csv), [system BOM](system_bom.csv) and [cost scenarios](cost_scenarios.json).

The JSON is an editable **pin-level circuit specification**. Matching `.net` files are KiCad XML interchange exports. Package strings are hints, not qualified footprint-library references. These files are not a native schematic, routed PCB, stencil or fabrication release. Schematic/ERC, footprint verification, PCB routing/DRC and physical tests remain necessary engineering steps. No hardware validation is claimed.

Regenerate and check the original circuit files offline:

```sh
python3 electronics/build_circuit.py
python3 electronics/test_circuit.py
```

Eight checks cover connectivity, package pin assignments, independent sensor addressing, protection coverage, supply topology, standby state, termination and interchange consistency. They do not establish EMI immunity, production yield or a working MCU firmware image.

## Electrical contract

Use 4.75–5.25 V at the regional input, nominally 5.00 V. Ripple target is at most 100 mV peak-to-peak with a 20 MHz measurement bandwidth. At the farthest node, the protected LDO input must remain at least 3.8 V under the measured peak load. A patch is budgeted at 30 mA average and 80 mA peak; an eight-node region at 240 mA average and 640 mA peak. These are design allocations until measured. The regional latch-off eFuse is nominally 1 A; the bench source limit is 1.5 A after individual-node startup tests.

CAN FD uses 1 Mbit/s arbitration and 2 Mbit/s data. Limit the linear trunk to 2 m and each branch to 50 mm. Fit exactly two 120 Ω terminators on the permanent trunk. Powered-off CANH–CANL resistance should be approximately 60 Ω. Unplugging a node leaves the trunk and terminations intact; a trunk short can still disable that entire region.

The lab adapter reference is the isolated **PEAK IPEH-004022**. Its D-sub connection is pin 7 CANH, pin 2 CANL and pin 3/6 sensor ground. Leave optional supply pin 1 disconnected and internal termination off. Bind the host interface to the physical adapter serial/USB path. A name such as `can0` is not device identity. [Manufacturer interface and pinout](https://www.peak-system.com/products/hardware/external-pc-interfaces/pcan-usb-fd/).

The isolated adapter's bus-side ground belongs to the sensor supply. A grounded oscilloscope or programmer can inadvertently bridge that isolation. Use appropriate isolated/differential measurement and verify all return paths before energizing the fixture.

## Sensing scope and example cost

The base patch provides contact location, ordinal contact intensity and two **actual point temperatures**. It does not provide calibrated force, shear, proximity, a continuous thermal image or a safety-rated stop. The remote end-of-line path detects some broken conductors; it cannot prove an intact pressure-sensitive coating.

The [generic eight-controller example](example_configuration.json) has active site counts `4, 6, 4, 6, 6, 28, 6, 28`: **88 touch sites and 16 NTC points**. This is a stationary test configuration, not a claim of fit or coverage on a particular robot. Commissioned masks disable unused ADC channels.

The modeled full-patch unit cost is **$34.78 at an assumed 1,000-patch manufacturing quantity**: ($29.24 material/outsourced assembly + $3.30 final process + $0.50 expected rework) / 95% yield. The process allowance is 345 attended seconds at $24/hour plus 300 station seconds at $12/hour. This is not an eight-unit retail prototype quotation. The short-sheet example holds controller costs fixed and assumes six sheets at $6 and two at $12, giving $242.24 of modeled patch hardware. With one $400 lab gateway, $67 regional harness/distributor/enclosure allowance and $300 reusable supply budget, the example totals **$1,009.24**. Actual low-volume material, PCB and assembly quotes may be substantially higher. Tooling, engineering, host computer, other instruments, tax and shipping are excluded.

Four independent regions with the same eight patches model to $2,410.24. Eight full 28-site patches in one region model to $1,045.24; 80 full patches with ten isolated lab gateways and two USB hubs model to $7,852.40. These are clearly labeled procurement scenarios, not promised selling prices.

[Optional local inertial calibration](optional_calibration.md) adds a separate eight-IMU hardware allowance of $159.60, with firmware, synchronization and calibration engineering excluded. The base touch/temperature patch has no IMU and cannot perform inertial self-calibration by itself.
