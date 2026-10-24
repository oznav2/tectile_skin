[עברית](README.md) · English

# ROBOSKIN mechanical development kit

These original, platform-neutral assets define three removable skin-panel sizes, a bench carrier, strain relief, and mass-property calculations. They are suitable for dimensional mock-ups and controlled prototype development. They contain no robot-specific geometry or qualified mounting location. A particular robot's surfaces, motion envelopes, cover temperatures, cable paths, and permitted loads must be measured before installation.

The sensing objective is contact location and approximate pressure, with two local temperature channels per controller. The first demonstration concerns arms and legs. Neither calibrated force, shear measurement, full thermal imaging, whole-body coverage, nor a safety-rated collision sensor follows from the mechanical design.

## Reproduce and inspect the assets

From the repository root:

```sh
python mechanics/generate_templates.py
python -m unittest discover -s mechanics -p 'test_*.py' -v
```

The Python tools use only the standard library. The tests check channel geometry, physical units, reproducibility, and analytical mass-property cases. They do not validate physical fit, fatigue, sealing, or sensing performance.

| File | Purpose |
|---|---|
| `assets/mechanics/*_template.svg` | Print-at-100% dimensional stencils with a 25 mm scale bar and channel locations |
| `assets/mechanics/panel_profiles.json` | Local sensor coordinates, active masks, dimensions and explicit unknown tail/temperature geometry |
| `removable_carrier.scad` | Editable original perimeter fixture and separate sleeved-cable tie-down |
| `added_inertia.py` | Combine measured masses, centers of mass, and physically valid inertia tensors |
| `commissioning_record.example.json` | Record the measurements needed to commission one real panel |

The SVG circles mark site centers, not electrode sizes. These stencils are **not electrode artwork, flex-PCB files, or a manufacturing release**. The nominal 3 mm perimeter does not yet prove enough room for the adhesive seal and electrical traces. Sensor-tail geometry and temperature-element placement are intentionally undefined until the chosen laminate and controller interconnect are specified and measured.

## Film profiles and identification

| Profile | Contact sites | Sensing field | Film rectangle excluding tail | Active contact mask |
|---|---:|---:|---:|---|
| `compact_2x2` | 4 | 50 × 50 mm | 56 × 56 mm | `0x0000000f` |
| `compact_3x2` | 6 | 75 × 50 mm | 81 × 56 mm | `0x0000003f` |
| `standard_7x4` | 28 | 175 × 100 mm | 181 × 106 mm | `0x0fffffff` |

Contact-site pitch is 25 mm in both directions. The coordinate origin is the center of the sensing field; +x runs along its length, +y across its width, and +z points outward. Index = row × columns + column; row zero is at negative y. Consequently, the bottom-left site in the drawing is site zero. Each smaller profile has its own contiguous indices: never apply seven-column indexing to a compact panel.

The controller can retain 28 contact inputs for bench reuse. Disable inactive inputs in acquisition and reporting; do not report them as failed sensors. Temperature inputs are separate from the contact mask. A new physical layout requires its own profile identifier and calibration. Cutting a wired large panel into a smaller panel is not equivalent to manufacturing that smaller layout.

An illustrative eight-panel purchase comprises two 2×2 panels, four 3×2 panels, and two 7×4 panels: **88 contact sites and 16 local temperature channels**. Its film rectangles total **0.062788 m²**, and its nominal sensing fields total **0.0550 m²**. This is an arithmetic example, not an assignment to any particular robot or a full-body coverage claim. Different surfaces may require different counts, smaller geometries or segmented panels.

Assign a stable serial number, profile/revision, orientation arrow, communication address and measured parent-body frame to each finished panel. A replacement should be recognized by serial/profile and require its own calibration record. Do not assume that communication address alone identifies its physical location.

## Build one passive mock-up first

1. Print the selected SVG without fit-to-page scaling. Measure the 25 mm bar with calipers; reject a print outside 25.00 ± 0.25 mm. Make a paper stencil and then a thin, nonconductive plastic dummy with the planned laminate thickness. Record the actual film-tail and connector envelopes separately.
2. Choose a surface wholly on one rigid robot body. A nonstretchable sensing laminate must not cross a joint or crease. Avoid compound curvature unless separate coupon tests establish that the selected stack tolerates it. Small flat or singly curved segments are easier to validate than one large forced wrap.
3. Open `removable_carrier.scad`. Select `columns`, `rows`, and `part="carrier"`. Its default planar frame is 1.5 mm thick, with a 3 mm rim and two independent 10 mm strap paths. The overall frame envelope is film length + 6 mm by film width + 20 mm: 62×76, 87×76, or 187×126 mm. Include the tail, connector, controller, and dynamic cable loop when checking the complete envelope.
4. Set `tail_slot_width` from the **measured** tail width plus assembly clearance. A value of zero makes a passive fit fixture only; it does not authorize trapping a live sensor tail under the rim. Inspect the exported geometry, slot edges and slicer preview before printing. No OpenSCAD compilation or physical print is claimed by this repository's tests.
5. Use a compliant nonconductive material for the first fixture and separately verify its temperature and creep behavior. No particular printable polymer is qualified here. A flexible frame is not proof that the laminate tolerates the same bend. Where the sensing stack requires a back support, provide a continuous electrically insulating surface of known compliance; the frame's open center does not itself provide that support.
6. Strap the frame to the same rigid body, with pads only beneath the rim and strap contact areas. Keep strap tension out of the sensing field. Measure unloaded sensor offsets before and after tightening. Reject a fixture whose retention preload produces contact indications or changes the calibrated response materially.
7. Mount the controller on that same body and take the short sensor tail into it before a moving joint. Export `part="strain_relief"` for the separate 30×16×2 mm tie-down. Tie a soft sleeve around the cable; do not crush bare insulation or bend at a crimp exit. The cable, rather than the film or sensor tail, accommodates joint motion.

Do not drill load-bearing members, disturb motor/bearing fits, cover vents, or reuse an unverified structural fastener for this development fixture. Obtain mounting loads and permitted attachment points from the selected robot's engineering owner. A removable external carrier keeps these measurements and service operations accessible.

## Protective cover and temperature construction

Start with flat coupons assembled from the same pressure laminate, perimeter adhesive, outer cover, support and electrical tail intended for the panel. A nominal 0.5 mm nonconductive silicone cover is one candidate; a thin TPU cover is a separate candidate requiring its own material/process validation. The actual material grade, hardness, cure, adhesive, thickness tolerance and supplier batch belong in the build record. Do not combine supplier-incompatible primers and elastomers into an untested recipe.

The cover changes pressure spreading, neighboring-site response, hysteresis and thermal delay, so calibrate the finished stack. Keep adhesive away from active electrodes and strain-sensitive regions. Edge seams and cable exits require explicit sealing and pull tests; a silicone top face alone does not establish an ingress rating. Make the wear cover replaceable and repeat the calibration checks after replacement.

Locate each temperature element beneath a thin local cover, away from motor housings, regulator heat and the principal pressure electrodes. Record its exact position in the panel coordinate frame. Two elements provide two local readings; temperature at an arbitrary contact point may remain unobserved. Compare the reading against a reference probe during warm-contact and ambient-change tests, with robot electronics both cold and operating. Quantify motor-heating bias before describing the measurement as external-object temperature.

For each of at least three coupons, record thickness at five points, unloaded offset, contact threshold, hysteresis, creep, neighboring-site response, thermal step response and peel behavior. Repeat after representative cleaning, abrasion and environmental exposure. Define the actual cleaning chemicals, dwell time, humidity and temperature from the intended application before the test; passing an arbitrary exposure does not qualify a different use environment.

## Motion, clearance and fatigue qualification

Begin with a supported robot and powered motion disabled. Use its commissioned limits and approved service procedure. A model's numerical joint limits do not by themselves authorize physical travel. An independent emergency-stop path remains necessary for powered testing; these prototype skin signals are not its replacement.

1. Record the surface revision, datum, neighboring joints, permitted joint intervals, mounting transform, local outward normal, cable specification and permitted dynamic bend radius. Leave `commissioned=false` until the record is complete and reviewed.
2. Move each adjacent joint through its permitted interval, then sweep combinations of adjacent joints. Inspect the continuous sweep, not only endpoints. Measure minimum clearance to rigid structures, cable loops, covers and linkages, including deformation and tolerance. A 5 mm nominal rigid-clearance target is an initial project screen, not a universally adequate margin or a safety standard; require a larger measured margin wherever deflection can consume it.
3. Check the cable's dynamic bend-radius and torsion ratings throughout the sweep. A static bend rating is insufficient for a moving joint. Use two strain-relief anchors and a controlled loop. Eliminate pinch, rubbing, snagging, connector traction and self-contact. A cable with no usable dynamic rating must be separately fatigue-tested before it becomes a production choice.
4. Measure joint current/torque proxy, tracking error, temperature and mechanical interference first without the skin and then with dummy fixtures/cabling, at identical trajectories and loads. Reject binding, blocked cooling or a cable force that changes the robot's motion appreciably.
5. Instrument a joint fixture for an initial 10,000-cycle screen and then a 100,000-cycle pilot gate at the intended stroke, speed and temperature. Log communication errors and continuity, inspect every 10,000 cycles, repeat retention checks and sensor calibration. These are proposed development gates, not a claimed service life. Commercial life must be related to actual cycles per day, duty cycle and warranty duration.

Keep mass, collision and sensor-frame commissioning separate. A correctly measured location does not validate a cable's fatigue life, and a good sensor reading does not prove adequate joint clearance.

## Measure mass and inertia before integration

Weigh the finished film, cover, adhesive, carrier, straps, controller enclosure, connectors and installed cable lengths. Record each component's mass and center of mass in its parent body's coordinate frame. For scale, the eight-panel example's 0.5 mm cover alone weighs approximately 34.5 g **if** its density is 1,100 kg/m³. Substitute the supplier's actual density and measured thickness; this is not a finished-skin mass estimate.

The inertia helper implements the parallel-axis theorem and rejects invalid masses and physically inconsistent tensors. Supply each component's intrinsic inertia about its own center of mass, already rotated into the same parent axes. A zero tensor is an explicit point-mass approximation; it is inappropriate when the component's own size materially affects the result. Moving cable loops need measurements or bounds over configuration. Review the combined mass, center of mass and inertia before updating the robot's model, balance controller or actuator margins.

At ideal 25 mm square pitch the sensing-field density is 1,600 sites/m². Boundaries, inaccessible surfaces, seams, joint gaps and controller packaging reduce installed coverage. A thousand sites imply at least 0.625 m² of sensing-field area at this pitch, before those losses. Report measured covered area, blind zones, total added mass and installed cost rather than scaling a single panel's headline value.

## Required evidence at each phase

| Gate | Concrete work | Required record |
|---|---|---|
| M0 configuration | Identify the selected robot, mounting surfaces, allowable attachments and motion limits | Hardware identity and approved constraints |
| M1 passive fit | Print stencils, construct dummy fixture, sweep individual and combined joints | Measured transform, full envelope, clearance and cable-radius photographs |
| M2 one static panel | Calibrate the complete protected stack using small and broad contacts, then thermal steps | Contact localization, pressure categories, cross-talk, drift and thermal delay |
| M3 moving limb | Run a supported limb at approved conservative motion limits | Latency, communication integrity, false contacts, retention, current and temperature comparisons |
| M4 durability | Complete cycle, cleaning, wear and retention procedures; replace one cover | Drift/wear results, service time and measured mass/inertia |
| M5 multiple panels | Repeat serial/profile-bound commissioning and synchronized acquisition | Correct sensor identification, no address collisions, measured bus loading and blind-zone map |
| M6 production tooling | Freeze material and adhesive grades, tolerances, tail/connector drawing and manufacturing process | Reviewed fabrication package, supplier quotes, inspection plan and pilot yield |

A production release requires the recorded results, not only this checklist. The geometry and files provided here make those tests reproducible without implying that physical qualification has already happened.
