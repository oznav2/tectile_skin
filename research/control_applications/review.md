# Control and application references: systematic audit

Reviewed 2026-10-24 for Ilan's affordable electronic-skin plan. Assigned references: **25–29, 35, 63–84**, all 28 accounted for in [references.json](references.json). This review owns control/application implications; it does not assess component purchasing or change the main plan.

The proposed baseline is 28 independent normal-contact resistive cells plus two temperature points per patch, 100 Hz acquisition and a 40 ms maximum freshness envelope. It has **no proximity sensor, per-cell IMU, shear sensor, calibrated six-axis force sensor or certified protective controller**. These facts determine which research algorithms can be implemented faithfully.

## Integration memo: changes to make before any motor demonstration

The most defensible first product is a distributed contact-perception system with explicit coverage validity, a serviceable cover and reproducible installation/calibration. The literature establishes that skin-informed robot behavior is feasible. It does **not** establish the proposed low-cost laminate's durability, force accuracy, loop stability, manufacturing yield or market novelty. The actions below are engineering requirements inferred for this project; they are not claimed published performance.

### 1. Separate measurement, virtual interaction and motion command

Preserve three interfaces:

1. `SkinObservation`: patch UID, boot/session ID, map/calibration version, taxel index, acquisition-time interval, raw code, contact state, relative intensity, temperature channel age and validity flags.
2. `ContactPolicyRequest`: valid contact list, rigid link, contact position/normal, allowed-zone classification, and a bounded virtual interaction request. This is a policy output, not a force measurement.
3. `RobotSupervisorDecision`: accept, limit, refuse, hold or fault, with reason and applied command. The existing robot controller owns actuator constraints and balance.

The [2016 control framework, §IV-A](https://mediatum.ub.tum.de/doc/1335611/document.pdf) maps weighted tactile signals to virtual normal forces. Maintain that distinction. A film signal is affected by load distribution, preload, cover mechanics and drift. Do not put raw intensity into a field named `force_N`, or infer object pressure from force divided by the nominal taxel area.

Summed intensity also depends on contact spreading and taxel density. Keep a bounded total virtual-effort budget per rigid link and test it with the same external load applied through small and broad probes. Limit control requests independently of diagnostic contact intensity; a command limit must not erase evidence of overload or simultaneous contact. A design that reacts more strongly merely because one cover spreads a touch over four cells has a calibration/policy defect.

### 2. Make frames, normals and aggregation auditable

For each taxel store `link_id`, position `r_i` in metres, a unit normal `n_i`, and the transform/map version. Define whether `n_i` points outward from the robot. Determine the reaction sign with a fixture test; never assume every paper's sensor z-axis has the same convention.

At one coherent robot state, form each chosen virtual vector `f_i`. For cells fixed to the same rigid link and expressed in the same frame, the equivalent wrench at link origin O is

```text
F_link = sum_i f_i
M_link = sum_i ((r_i - r_O) cross f_i)
W_link = [F_link; M_link]
tau_link = transpose(J_link_at_O) * W_link
```

The Jacobian convention here is `[linear velocity at O; angular velocity]`. A different ordering requires permuting both wrench and Jacobian. A point force may have zero free couple at its application point, but generally produces a nonzero moment at the link origin. The supplied Cheng 2019 paper's link aggregation is appropriate; naive summation of forces alone is not.

Required software tests: compare cell-by-cell and link-aggregated results; rotate the entire scene; change wrench origin; place equal/opposite forces to create a couple; place contacts whose resultant cancels; verify zero influence from joints downstream of a contact link; check `f·(Jv*qdot) = (Jv^T*f)·qdot`. Keep the original individual contacts even when net wrench is zero. A zero resultant is not an empty or unconstrained contact set.

### 3. Enforce time coherence beyond packet freshness

Log both acquisition and receive times. A heartbeat received now does not make an old contact or old robot pose current. At policy evaluation, reject uncertain/future timestamps, wrong boot identity, wrong body map and robot joint states that cannot be aligned to the contact acquisition interval. The 40 ms skin freshness limit is an exclusion boundary, not a target control latency or a stability proof.

Quantify position error from time skew with a conservative bound:

```text
contact_position_error <= geometry_error + v_contact_max * time_skew
```

For illustration, 0.5 m/s over 40 ms adds 20 mm before calibration error, comparable to the baseline 25 mm pitch. Choose the permitted robot speed/state skew from the actual localization-error budget. Preserve scan-offset information or bound the oldest sample in a multiplexed frame. Exercise delayed, reordered, duplicated, wrapped and rebooted streams at the **application consumer**, not only the gateway.

### 4. Do not implement a torque-to-position shortcut

The [torque resolver in ref. 64, §IV-F](https://mediatum.ub.tum.de/doc/1335611/document.pdf) contains virtual dynamics and real-state feedback. Its symbolic dynamic model does not determine actual mass, centre of mass, friction or inertia merely from a D–H table. The project must identify an OEM-supported compliance/admittance interface or specify a separate trajectory-generator implementation with its own validation.

Required integration fields: robot model/firmware, controlled joints and units; command update/deadline; accepted joint-state timestamps; acceleration/jerk/velocity/torque bounds; joint and workspace limits; gravity/load support; command-versus-actual position-error threshold; actuator saturation reporting; behavior on stale data, process death or bus loss; re-enable and virtual-state initialization. If any required field is absent, the demonstrator remains sensing/visualization only. This is an execution boundary with a concrete checklist, not an invitation to guess gains.

### 5. Keep constraints above optional tactile behavior

[Ref. 67, §§4.2 and 5](https://elib.dlr.de/101443/2/NullspaceSurvey.pdf) makes actuator limits and projection choice material. [Ref. 68, §§4.3–5](https://ai.stanford.edu/~lsentis/files/ijhr-05.pdf) explicitly considers infeasible lower-priority motion. A weighted sum of skin and trajectory commands is not a hard-constraint hierarchy.

Use the OEM controller/constraint solver for support, joint/actuator limits and self-collision. Application behavior can request yielding only inside that feasible set. Required adversarial tests include three conflicting tasks, a rank-deficient pose, contact at a proximal link, both sides of one link pressed, two limbs contacted, a blocked retreat direction, task enable/disable during motion and an actuator hitting its command limit. Record the applied command, not only the unsaturated requested command.

The [2016 mobile force-propagation model, §II](https://mediatum.ub.tum.de/doc/1336140/document.pdf) omits base tilting/instability and upper-limb coupling. It therefore cannot justify autonomous biped leg withdrawal. Begin with a fixed base. A later walking integration must keep support contacts and balance in the robot's existing whole-body controller.

### 6. Treat compliance and passivity as properties of the complete loop

Positive virtual damping is not proof of passivity after sample/hold, delay, saturation, changing gains and position-servo dynamics. [Hogan's illustrative derivation, pp. 17–20](https://bpb-us-e1.wpmucdn.com/sites.mit.edu/dist/5/1384/files/2025/02/1985-impedance-control-an-approach-to-manipulation-part-III-applications.pdf) states the simplifying mechanical assumptions behind its impedance selection. Do not copy a damping ratio or gain as universal.

Use an independent load cell/force transducer and fixture displacement/encoder measurement for physical interaction tests. Virtual intensity has no physical work unit; multiplying it by displacement does not measure joules. A claim of energy/passivity monitoring would require valid physical wrench and velocity observations and a separately reviewed controller.

Before enabled contact reactions, test soft, medium and rigid fixture contacts; increasing gain within the platform-approved range; actual measured delay plus injected 10/20/40 ms delay; packet bursts and loss; saturation; abrupt onset/release; boot/reset; and switched contact zones. Pre-register allowable peak reference force, excursion, oscillation amplitude, settling and stop distance from the chosen fixture/robot specification. Stop the test on violation. Results establish an operating envelope for that setup only.

### 7. Use a state machine with a real fault destination

Suggested non-safety application states:

```text
INIT -> MONITOR_ONLY -> ENABLED_INTERACTION -> CONTROLLED_HOLD
          |                    |                     |
          +--------------------+--------------------> FAULT_LATCHED
```

Initialization requires valid identity, calibration, map, fresh observations and current robot state. Explicit enable and allowed contact zones are needed before interaction. Unknown/forbidden contact, conflicting contacts or infeasible relief requests a supervisor hold. Invalid/stale coverage enters a latched fault with explicit operator acknowledgment plus fresh successful checks before re-enable. On a load-bearing robot, do not implement fault handling as indiscriminate removal of motor torque; the platform must maintain its validated load/support behavior.

[Ref. 82, §III Remark 1 and §IV](https://www.diag.uniroma1.it/~deluca/pHRI_elective/IROS17_Magrini_ADL_HRCoexistenceContactRedundant.pdf) distinguishes its reported single-contact setting and smooth task abort. Smooth stopping consumes time and distance; both are measured requirements. Skin cannot infer intentional human guidance solely from contact intensity; that is also why a deliberate mode switch belongs in the product.

### 8. Preserve the publication's scientific credibility

Publish a sensing-first baseline and a separate bounded motion demonstration. Measure detection/localization, sensor validity, communication load, installation/service time and installed mass/cost. Do not equate demonstration with a safety certificate or a manufacturable product. [Ref. 72's own productization footnote](https://mediatum.ub.tum.de/doc/1446657/883306792253.pdf) is a useful reminder that research integration and commercial qualification are distinct evidence levels.

Novelty should be stated as a falsifiable engineering advantage: lower installed lifecycle cost for a specified area, contact resolution, fault coverage and replaceability, demonstrated against matched alternatives. Thousands of sensors, artificial skin, touch teaching, send-on-delta, Jacobian mapping and distributed control already have explicit prior art. No patentability or freedom-to-operate opinion follows from this literature review.

## Phased control-validation work package

| Gate | Concrete execution | Required artifact / decision |
|---|---|---|
| C0: observation only | Log one patch and a fixture load reference; verify polarity, baseline, contact onset/release, invalid channels, boot identity and mapping | Dataset with raw signals, independent fixture load, timestamps and map/calibration hashes; no motor output |
| C1: geometry/math | Run deterministic frame, moment, virtual-work, downstream-joint and aggregation/cancellation tests | Passing regression output and failing negative cases that demonstrate the checks detect an incorrect implementation |
| C2: timing/fault replay | Replay stale/reordered/rebooted streams and old joint states to the real consumer; sever branch/region/host paths | Every invalid input results in declared invalid coverage and specified supervisor state within the documented deadline |
| C3: shadow policy | Run contact policy on live data while blocking its motor output; replay allowed, forbidden and conflicting contact scenarios | Auditable requested/applied/blocked decision log; no surprise automatic recovery |
| C4: fixed-base fixture | Use supported OEM control with physical bounds; exercise delay, stiffness, saturation and transition matrix above | Measured operating envelope; peak load, excursion, jerk/command slope, settling and stop-time record; retain all failures |
| C5: limb integration | Measure clearance over full permitted joint motion, skin mass/inertia and cable load; repeat C2/C4 after assembly | Platform-specific signed integration configuration; unchanged OEM support/balance ownership |
| C6: publication/pilot | Repeat with replacement covers and different laminate lots; timed service; compare matched sensing alternatives | Reproducible raw data, unit counts, failed-unit accounting, scripts, installation/service cost and stated limitations |

These gates do not require inventing universal actuator gains. C4 remains explicitly unapproved until its robot-specific interface and numerical limits have been supplied and verified; C0–C3 are executable without live robot control.

## Access audit and reference-by-reference index

`FULL_TEXT` means an original/author manuscript was accessible and the stated technical sections were read; it does **not** claim cover-to-cover study or replication. `ABSTRACT_ONLY` is used conservatively where direct full-text access failed, even if a few body passages were available through a search index. `CITATION_ONLY` records bibliographic coverage without relying on unverified technical claims. Author-hosted manuscript versions are noted. Secondary summaries are not used to fill inaccessible equations or experimental details.

Counts: **11 FULL_TEXT, 12 ABSTRACT_ONLY, 5 CITATION_ONLY.** Exact identities, URLs, read scopes, findings, limitations, project actions and novelty assessments are in [references.json](references.json). The table below provides a quick audit trail.

| Ref | Access | Material examined / implementation consequence |
|---|---|---|
| [25](https://doi.org/10.1109/ROBOT.2002.1014313) | CITATION_ONLY | Tactile interaction historical record; no reproduced controller |
| [26](https://ntrs.nasa.gov/citations/19930059726) | ABSTRACT_ONLY | Teleoperation/whole-arm awareness; no pre-contact claim from contact film |
| [27](https://dblp.org/rec/conf/icra/BoddyT93) | CITATION_ONLY | Historical reactive avoidance; define infeasible withdrawal explicitly |
| [28](https://elib.dlr.de/11914/) | CITATION_ONLY | Touch-teaching prior art; explicit operator-enabled teaching mode |
| [29](https://iris.univpm.it/handle/11566/228093) | ABSTRACT_ONLY | Manual guidance using F/T sensing; film intensity is a different input |
| [35](https://www.robertocalandra.com/papers/calandra_icra_2016.pdf) | FULL_TEXT | §§II–IV; learning still uses independent F/T and calibrated torque targets |
| [63](https://staff.aist.go.jp/e.yoshida/papers/Mittendorfer_2014AR.pdf) | FULL_TEXT | Hardware, calibration and applications; required motion sensors absent from baseline |
| [64](https://mediatum.ub.tum.de/doc/1335611/document.pdf) | FULL_TEXT | Models/control/resolver; no direct torque-to-position shortcut |
| [65](https://portal.fis.tum.de/en/publications/whole-body-active-compliance-control-for-humanoid-robots-with-rob/) | ABSTRACT_ONLY | Whole-body humanoid compliance prior art; original controller details unavailable |
| [66](https://portal.fis.tum.de/en/publications/tomm-tactile-omnidirectional-mobile-manipulator/) | ABSTRACT_ONLY | Wheeled integration platform; budget integration separately |
| [67](https://elib.dlr.de/101443/2/NullspaceSurvey.pdf) | FULL_TEXT | Consistency, saturation, rank and task-priority limits |
| [68](https://ai.stanford.edu/~lsentis/files/ijhr-05.pdf) | FULL_TEXT | Hierarchical formulation and simulated example; detect infeasible tasks |
| [69](https://portal.fis.tum.de/en/publications/efficient-distributed-torque-computation-for-large-scale-robot-sk/) | ABSTRACT_ONLY | Distributed computation concept; profile before distributing kinematics |
| [70](https://portal.fis.tum.de/en/publications/tactile-based-whole-body-compliance-with-force-propagation-for-mo/) | ABSTRACT_ONLY | Constrained mobile compliance; no imported biped guarantee |
| [71](https://doi.org/10.1109/ROBOT.2004.1307969) | CITATION_ONLY | HRP-2 identity; no assumed actuator/platform capability |
| [72](https://mediatum.ub.tum.de/doc/1446657/883306792253.pdf) | FULL_TEXT | Deployment experiment and productization caveat; time full installation/service |
| [73](https://repository.tudelft.nl/record/uuid%3Ae16cac95-3ada-4950-b9ac-a0cdfc8cdaef) | ABSTRACT_ONLY | Point-cloud grasp planning; outside arm/leg skin scope |
| [74](https://khatib.stanford.edu/publications/pdfs/Khatib_1987_RA.pdf) | ABSTRACT_ONLY | Operational-space background; formulas cross-checked in accessible sources |
| [75](https://books.google.com/books/about/Robot_Control.html?id=-DZSAAAAMAAJ) | CITATION_ONLY | Book identity only; no chapter-level claim |
| [76](https://elib.dlr.de/79360/4/Dietrich_TRO2012.pdf) | FULL_TEXT | Task transitions, damping and experimental timing; test discontinuities |
| [77](https://mediatum.ub.tum.de/doc/1336140/document.pdf) | FULL_TEXT | Model assumptions omit tilt/instability; fixed-base first |
| [78](https://www.diag.uniroma1.it/~labrob/pub/papers/PHRIDOM_IROS06.pdf) | FULL_TEXT | Author workshop manuscript; dependability/fault handling, historical standards excluded |
| [79](https://bpb-us-e1.wpmucdn.com/sites.mit.edu/dist/5/1384/files/2025/02/1985-impedance-control-an-approach-to-manipulation-part-III-applications.pdf) | FULL_TEXT | Impedance selection assumptions; test the complete sampled loop |
| [80](https://khatib.stanford.edu/publications/pdfs/Zinn_2004_IJRR.pdf) | ABSTRACT_ONLY | Abstract plus indexed saturation passage; actuation constraints remain |
| [81](https://www.diag.uniroma1.it/deluca/pHRI_elective/ICRA15_Magrini_Flacco_ADL_ContactMotionForceControl_pHRI.pdf) | ABSTRACT_ONLY | Abstract and early modeling excerpts; use contact-specific Jacobian |
| [82](https://www.diag.uniroma1.it/~deluca/pHRI_elective/IROS17_Magrini_ADL_HRCoexistenceContactRedundant.pdf) | FULL_TEXT | Single-contact scope, staged handling and smooth abort |
| [83](https://sites.utexas.edu/hcrl/files/2016/01/paper-kwan-suk-icra.pdf) | ABSTRACT_ONLY | Scanner/torque fusion for gesture classification; intensity alone is not intent |
| [84](https://www.nature.com/articles/srep30383) | ABSTRACT_ONLY | Combined rehabilitation protocol; no skin-only clinical claim |

## What the references leave unspecified for this product

None of the accessed material validates the proposed 28-cell sheet's assembled load transfer, long-term drift, wear, chemical resistance, transfer of calibration after replacement, temperature spatial coverage, production yield or quoted unit cost. Control publications also do not determine the new robot's command limits, plant dynamics, response to loss of communication, motor thermal behavior or balance envelope. Those are closed engineering work packages in the gates above and the main electrical/mechanical plan; they must produce measured evidence before the corresponding claim is published.

The strongest low-cost design choice is to avoid claiming capabilities that require omitted sensors. Retain deterministic observations, geometry, identity, freshness and fault reporting. Use existing robot control infrastructure. Spend experimental effort on whether the protective stack and replacement process preserve detection at a lower installed cost. That is a specific, testable venture hypothesis.
