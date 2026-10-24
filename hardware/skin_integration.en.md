[עברית](skin_integration.md) · English

# Integrating robot hardware with electronic skin

The hardware package is imported from a pinned source revision and adapted through filenames, part identifiers and document text. Geometry, dimensions and electrical ratings are not changed by translation. The repository has independent Git history; the imported hardware files are derivatives governed by the upstream license.

## Baseline configuration and directory relationships

The initial working configuration has 24 degrees of freedom, 5DOF arms and a motion-control head. The 7DOF alternative is retained in full, but quantities, parts and cable routes must not be mixed between the two configurations. ROBOSKIN.0001 belongs to the 7DOF alternative and does not establish compatibility with the 5DOF baseline.

| Imported area | Connection to the skin design | Required integration check |
| --- | --- | --- |
| CNC | Select rigid body surfaces and anchoring points for a removable carrier | Match the model and drawing at the same revision; do not drill a load-bearing part without structural design |
| 3D printing | Covers, spacers and external carriers | Joint movement, ventilation, heat and cover removal for maintenance |
| Rubber | Existing protective surfaces and their effect on sensing | Hardness, thickness, creep and pressure spreading; do not assume an existing rubber part is a calibrated sensing layer |
| PCB boards | Check volumes, connectors and interference around the skin controllers | Skin controllers remain in the electronics directory; do not connect to the motor network or battery based on a connector name |
| Harnesses | Plan a separate route for the four wires carrying skin power and CAN FD | Dynamic bend radius, torsion, anchoring and separation from motor power |
| Bills of materials | Add skin components and quantities to a controlled configuration list | Measured mass, center of mass, power, price and assembly times |

## Required prototype workflow

1. Select the configuration bill of materials and record part revisions. STEP files, PDF drawings and the CMF specification form a design set that must be checked together.
2. Print the [skin templates](../mechanics/README.en.md) and prepare dummy carriers. Measure every surface and movement envelope; the repository does not yet contain installation transforms measured on a physical robot.
3. Anchor each panel and controller to the same rigid body. Sensing film and analog wiring must not cross a joint. Joint motion must be accommodated by a communication cable selected and tested for bending and torsion.
4. First build the [skin circuit](../electronics/README.en.md) on a stationary fixture with an isolated 5 V bench supply. The imported hardware package does not approve connecting this circuit to the robot battery.
5. Approve measured short-circuit, open-circuit, identification-error, data-aging and loaded-communication behavior before installation. The repository contains neither controller firmware ready to flash nor a routed and validated skin PCB.
6. Run the [receiver software](../software/README.en.md) only on dedicated skin interfaces. Record each panel's UID, sheet serial number, calibration, channel mask and physical location.
7. Perform motion tests on a supported limb, initially without actuation and then within approved limits. Compare current, temperature, tracking error and false contacts before and after installation.
8. Update a combined bill of materials only after measuring quantities, mass and current. Adding the prices in upstream files does not produce a current quotation for a robot or skin system.

## Boundaries of the adaptation performed

All 550 source-tree files are represented in the import map. Working files use English names and ROBOSKIN identifiers; extractable Chinese text in manufacturing documents has been translated into Hebrew. Numeric information and spreadsheet formulas were preserved, and PDF editing preserved vector graphics. STEP labels were changed without changing the non-string geometry data stream.

Replacing titles and identifiers is not a new mechanical design of the parts and is not manufacturing approval. Symbols and text drawn as lines, images and Gerber silkscreen cannot be verified through text search. Do not state that all source graphics were replaced or that the circuits were rerouted. The pinned source and name map enable examination and further editing in suitable CAD tools.

SolidWorks and Parasolid archives from release assets are separate sources not included here. Opening them, renaming them while preserving references, rebuilding an assembly and exporting drawings require a compatible CAD environment; this work has not been performed.

[Licensing and attribution](LICENSES.en.md) · [Inventory and source](provenance/README.en.md) · [Detailed skin plan](../electronic_skin.en.md)
