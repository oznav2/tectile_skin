# Release status

Working engineering release, 25 October 2026.

| Area | Delivered | Not yet established |
| --- | --- | --- |
| Sensing design | Materials, diagnostic circuits, protective stack and verification specification | Measured sensitivity, hysteresis, creep, seams, thermal delay and lifetime |
| Electronics | Original pin-level circuit models, connection tables, diagrams and KiCad-format netlists | Native schematic/footprints, routed PCB, ERC/DRC and assembled qualification |
| Firmware | Wire contract and reference event/identity/timing behavior | Board-specific compilation, flashing, scan deadlines and power/fault measurements |
| Software | Executable codec, freshness gates, generic observer, synthetic demo and regressions | Physical CAN transfer, target load/latency and installed performance |
| Mechanics | Original generic templates and carrier/strain-relief design | Printed/mounted fit, full motion envelope, fatigue and measured inertia |
| Economics | Itemized allowances and executable calculations | Supplier quotes, actual unit yield, tooling, labour and delivered prototype prices |
| Literature | 84-reference evidence register with explicit reading depth | Universal novelty, patentability, partner commitment or freedom-to-operate finding |

The repository has no robot-specific driver, actuator interface or embedded robot model. The generic frame names are labels, not measured transforms. Local contact intensity is not calibrated physical force. The software exposes no control-ready state suitable for actuator use.

Every physical phase requires raw measurements and a recorded pass/fail decision. Keep measured data separate from calculations and synthetic test output. Do not label missing firmware, unrouted circuit exports or untested material performance as a completed manufacturable product.
