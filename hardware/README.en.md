[עברית](README.md) · English

# ROBOSKIN hardware

[Integrated project](../README.en.md)

Humanoid robot hardware based on RoboParty RP1, with English working filenames, ROBOSKIN part numbers and Hebrew translations of extractable Chinese text. Text inside images, outlines and Gerber graphics requires separate examination of the graphical source and is not presented as completely translated. Originals are retained separately for traceability and licensing.

| Area | Documents |
| --- | --- |
| Architecture | [Hardware system](00_Docs/ROBOSKIN_Hardware_Architecture.pdf) |
| Mechanics | [Models, drawings and manufacturing](01_Mechanic/README.en.md) |
| Printed circuit boards | [Components, Gerber and coordinates](02_PCB/README.en.md) |
| Harnesses | [Lists, drawings and assembly](03_Harness/README.en.md) |
| Complete robot | [Bills of materials by configuration](04_BOM/README.en.md) |
| Electronic skin | [Design, software and hardware additions](../README.en.md) |

The selected design baseline has 24 degrees of freedom, with five degrees of freedom in each arm and a motion-control head. Files for the seven-degree-of-freedom alternative are also retained and labeled separately.

The requested renaming example: [ROBOSKIN.0001_forearm_lower_body.pdf](01_Mechanic/02_Manufacturing/01_CNC/7DOF/ROBOSKIN.0001_forearm_lower_body.pdf). This part belongs to the 7DOF alternative; its number is retained as the first registry example and does not change the choice of the 5DOF configuration.

The name and upstream-part-number mapping is in the [part registry](provenance/part_registry.csv). Upstream records are retained for traceability and are not the working names.

Original SolidWorks archives are retained outside the translated working tree. Converting assembly references, drawings and internal properties requires the [CAD procedure](skin_integration.en.md). The procedure has not been run in SolidWorks.

Filenames and translations do not constitute manufacturing approval. Drawings, revisions, connectors and test data must be checked as a matching set before release to manufacturing.

RoboParty's upstream rights are preserved. Hardware designs are governed by CERN-OHL-W-2.0; explanatory documents by CC-BY-SA-4.0; third-party materials by their original terms. [License scope](LICENSES.en.md).

[Skin integration mapping and validation scope](skin_integration.en.md) · [Provenance and inventory record](provenance/README.en.md)
