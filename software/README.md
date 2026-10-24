# Standalone electronic-skin software

This is a dependency-free Python reference for tactile sensing, temperature
monitoring, event reporting and CAN FD reception. It has no robot SDK, joint
model, actuator driver, motion commands or middleware dependency. Python 3.10
or newer is required. Live transport additionally requires Linux SocketCAN
and the `ip` utility; offline tests and the demo require neither.

From the repository root:

```bash
python3 -m unittest discover -s tests -v
python3 -m software --demo
```

The demo emits two JSON lines. The first has 88 available sensing sites across
eight example patches; the second has zero available sites after the capture
deadline. Both identify the input as simulated. No interface or device opens.
`python3 -m software.skin_receiver --demo` is an alias for the same code path.

## Files and responsibilities

| File | Responsibility |
|---|---|
| `skin_protocol.py` | Version 2 binary frames, physical identity, boot epochs, sequence validation and bounded clock synchronization |
| `skin_events.py` | Send-on-delta reporting of complete snapshots; successful transmission advances the reporting baseline |
| `skin_wrench.py` | Pure reference wrench/frame mathematics; no actuator interface |
| `observer.py` | Commissioned patch configuration, installed-channel masks, held-sample expiry and JSON observations |
| `transport.py` | Dedicated SocketCAN FD ownership, bounded reads, overflow/error handling and nonce requests |
| `can_wire.py` | Linux CAN FD socket structures and constants |
| `demo.py` | Synthetic packets through the actual codec and validation gate |
| `config/limb_skin.example.json` | Uncommissioned example; generic frame labels with no kinematic assumptions |

The reference reports ordinary sampled sensors using the send-on-delta approach
described by Cheng et al., *Comprehensive Realization of Robot Skin: Sensors,
Sensing, Control, and Applications* (2019). This software is an implementation
of documented principles, not a claim that those principles are new.

## Example geometry and channel profiles

The optional example has four regional networks, each with two patches:

| Generic location | Profile | Installed sites per patch |
|---|---:|---:|
| Left/right upper arm | 2 × 2 | 4 |
| Left/right forearm | 3 × 2 | 6 |
| Left/right thigh | 3 × 2 | 6 |
| Left/right shin | 7 × 4 | 28 |

The total is 88 installed sites and 16 temperature channels. Frame names such as
`upper_arm_left` are labels only. The observer accepts user-defined local frames;
it neither infers geometry nor transforms observations into a robot base frame.
Changing a mounting requires its own measured geometry record.

Each controller reserves 28 wire slots. Installed sites occupy contiguous slots
`0..N-1`. Unused slots have value 255 and clear validity/open/overload bits. The
profile masks are `0000000f`, `0000003f` and `0fffffff`. A set status bit outside
the configured mask rejects a frame. An installed sensor failure decreases
coverage; an unused slot does not count as a failed sensor.

Configuration accepts 1–256 patches, up to eight unique node IDs per interface.
This is a software validation ceiling, not a measured bandwidth or latency
capacity. Add independent regional interfaces as required and measure host load,
bus utilization and fault recovery on the actual target.

## Observation and freshness contract

The JSON schema is `tectile_skin.observation.v1`. Each record contains:

- Physical UID, node/interface, configuration CRC, sheet serial and calibration
  hash for each patch.
- Expected, valid, unavailable, disabled and contact-or-fault masks.
- Ordinal touch intensity and temperature in Celsius; unavailable values are
  `null`. Intensity is not calibrated force in newtons.
- Boot epoch, sequence, bounded expiry, explicit health and coverage.
- A feature vector with schema `tectile_skin.features.v1.89_per_patch`.

Each patch contributes 89 features in configuration order:

| Offset | Count | Meaning |
|---:|---:|---|
| 0 | 28 | Intensity / 254; unavailable entries zero-filled |
| 28 | 28 | Per-site validity bits |
| 56 | 28 | Overload/contact-or-fault bits |
| 84 | 2 | Temperature Celsius / 100; unavailable entries zero-filled |
| 86 | 2 | Temperature validity bits |
| 88 | 1 | Acquisition record freshness |

The example produces 712 features. Consumers must use the validity masks and
must preserve configuration order. `control_ready` and `actuation_enabled` are
always false in this reference. There is no joint-state subscription or policy
input injection. An application must supply and validate its own control and
coordinate-frame integration.

The protocol requires a matching announcement followed by a nonce exchange.
Touch expires at the conservative 40 ms acquisition deadline, including time
held by the receiver. Clock synchronization lasts at most 2.5 seconds; samples
cannot outlive it. Requests renew every two seconds, with unanswered requests
retried after 20 ms. Invalid replies revoke the old clock mapping. Rejected
announcements revoke identity even when the boot number is unchanged.

Temperature validity includes sensor age, capture/transport age and held time,
with a 250 ms total limit. Missing temperatures produce degraded health even
when touch remains available. Overload stays an explicit fault/contact state.
An acquisition with every installed site failed remains a fresh fault report,
not a valid no-contact measurement.

All expiry fields use the producing host's monotonic clock. A consumer on
another machine needs its own receive watchdog and a clock-transfer bound;
comparing unrelated monotonic clocks is invalid. A stopped publisher does not
make its last message valid indefinitely. Identity checks detect configuration
and wiring mistakes; the bus protocol does not authenticate hostile senders.

## Live commissioning

1. Build and independently verify the sensor controller firmware. This package
   does not contain a flashed MCU implementation or verified analog hardware.
2. Use a dedicated CAN FD interface named `can_skin_<region>` and record its
   resolved `/sys/class/net/<interface>/device` path. Keep actuator buses under
   their existing owner's control.
3. Configure only the verified skin interface for 1 Mbit/s arbitration,
   2 Mbit/s data, FD enabled and MTU 72. The observer checks these properties
   and `ERROR-ACTIVE` status; it does not configure or reset interfaces.
4. Copy `config/limb_skin.example.json` and replace its synthetic identities,
   CRCs, sheet serials, calibration SHA-256 values and device paths with the
   measured commissioning record. Match the physical channel profiles.
5. With the host machine's actuators disabled, verify complete 100 Hz acquisition,
   at least 20 ms quiet refresh, reboot identification, nonce timing and error
   behavior from recorded traffic. Mark the manifest commissioned only after
   these measurements exist. Changing the example's boolean alone fails.
6. Start the observer with the commissioned file:

```bash
python3 -m software --config /absolute/path/to/commissioned.json
```

The receiver polls every 2 ms and publishes JSON approximately every 10 ms.
Each poll reads at most 128 frames per ready interface. These are scheduling
intentions, not a hard real-time guarantee. A regional socket error, overflow,
malformed frame or uncommissioned node clears that region and pending nonces.
Other regions retain independent health. The only transmitted messages are
freshness nonce requests to skin controllers.

Bench acceptance must measure reaction latency, open/short faults, identity
swaps, bus loss, power disturbances, full-load traffic, reboot recovery and
temperature faults. The 78 software tests exercise codec, masks, event scheduling,
freshness, transport fault sequences and reference mathematics. They do not
establish physical sensor accuracy, EMC, product safety or manufacturing yield.
