[עברית](README.md) · English

# ROBOSKIN mechanical design

[Hardware page](../README.en.md) · [Robot bill of materials](../04_BOM/README.en.md)

This directory contains mechanical manufacturing files originating from RP1. Quantities appear in the configuration bill of materials. Materials and surface finishes are defined in the drawings and CMF specifications.

## CAD sources

The source tree's STEP files and manufacturing drawings are included here. Editable SolidWorks, Parasolid and SolidWorks drawing archives are separate upstream release assets; they are not part of the 550 files in the Git tree and are not included in this repository version.

Asset links and the upstream license are in the [provenance record](../provenance/README.en.md). Renaming SolidWorks files requires updating assembly and drawing references within a compatible CAD environment. External file renaming must not be presented as a completed conversion.

## Manufacturing files

The manufacturing lists collect per-robot quantities by part number, with separate columns for 5DOF and 7DOF arms. Both refer to the motion-control head.

| Process | Files | Finish specification |
| --- | --- | --- |
| CNC | [Bill of materials](02_Manufacturing/01_CNC/ROBOSKIN_CNC_BOM.xlsx), [shared parts](02_Manufacturing/01_CNC/Common/), [5DOF](02_Manufacturing/01_CNC/5DOF/), [7DOF](02_Manufacturing/01_CNC/7DOF/) | [CMF specification](02_Manufacturing/01_CNC/CMF_Specification/ROBOSKIN_CNC_CMF_Specification.xlsx) |
| 3D printing | [Bill of materials](02_Manufacturing/02_3D_Printing/ROBOSKIN_3D_Print_BOM.xlsx), [models](02_Manufacturing/02_3D_Printing/STEP_3D_Models/), [drawings](02_Manufacturing/02_3D_Printing/PDF_Drawings/) | [CMF specification](02_Manufacturing/02_3D_Printing/CMF_Specification/ROBOSKIN_3D_Print_CMF_Specification.xlsx) |
| Rubber parts | [Bill of materials](02_Manufacturing/03_Rubber/ROBOSKIN_Rubber_BOM.xlsx), [models](02_Manufacturing/03_Rubber/STEP_3D_Models/), [drawings](02_Manufacturing/03_Rubber/PDF_Drawings/) | [CMF specification](02_Manufacturing/03_Rubber/CMF_Specification/ROBOSKIN_Rubber_CMF_Specification.xlsx) |

The part number and revision suffix link each drawing to its model. Revisions and mirrored variants are not merged merely because they share a part number.

[Electronic-skin carriers and templates](../../mechanics/README.en.md)
