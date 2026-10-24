<div dir="rtl" lang="he">

עברית · [English](README.en.md)

# התכנון המכני של ROBOSKIN

[עמוד החומרה](../README.he.md) · [רשימת חומרים לרובוט](../04_BOM/README.md)

כאן נמצאים קובצי הייצור המכני שמקורם ב־RP1. הכמויות מופיעות ברשימת החומרים של התצורה. חומרים וגימור פני שטח מוגדרים בשרטוטים ובמפרטי CMF.

## מקורות CAD

קובצי STEP ושרטוטי הייצור של עץ המקור נכללים כאן. ארכיוני SolidWorks, Parasolid ושרטוטי SolidWorks הניתנים לעריכה הם נכסי שחרור נפרדים של המקור; הם אינם חלק מ־550 הקבצים שבעץ Git ואינם כלולים בגרסה זו של המאגר.

קישורי הנכסים ורישיון המקור נמצאים ב[רישום המקור](../provenance/README.md). שינוי שמות של קובצי SolidWorks מחייב עדכון של הפניות המכלול והשרטוט מתוך סביבת CAD תואמת. אין להציג שינוי שם חיצוני כהמרה שהושלמה.

## קובצי ייצור

רשימות הייצור מרכזות את הכמות לרובוט לפי מספר חלק, בעמודות נפרדות לזרועות 5DOF ו־7DOF. שתיהן מתייחסות לראש בקרת תנועה.

| תהליך | קבצים | מפרט גימור |
| --- | --- | --- |
| CNC | [רשימת חומרים](02_Manufacturing/01_CNC/ROBOSKIN_CNC_BOM.xlsx), [חלקים משותפים](02_Manufacturing/01_CNC/Common/), [5DOF](02_Manufacturing/01_CNC/5DOF/), [7DOF](02_Manufacturing/01_CNC/7DOF/) | [מפרט CMF](02_Manufacturing/01_CNC/CMF_Specification/ROBOSKIN_CNC_CMF_Specification.xlsx) |
| הדפסת תלת־ממד | [רשימת חומרים](02_Manufacturing/02_3D_Printing/ROBOSKIN_3D_Print_BOM.xlsx), [מודלים](02_Manufacturing/02_3D_Printing/STEP_3D_Models/), [שרטוטים](02_Manufacturing/02_3D_Printing/PDF_Drawings/) | [מפרט CMF](02_Manufacturing/02_3D_Printing/CMF_Specification/ROBOSKIN_3D_Print_CMF_Specification.xlsx) |
| חלקי גומי | [רשימת חומרים](02_Manufacturing/03_Rubber/ROBOSKIN_Rubber_BOM.xlsx), [מודלים](02_Manufacturing/03_Rubber/STEP_3D_Models/), [שרטוטים](02_Manufacturing/03_Rubber/PDF_Drawings/) | [מפרט CMF](02_Manufacturing/03_Rubber/CMF_Specification/ROBOSKIN_Rubber_CMF_Specification.xlsx) |

מספר החלק וסיומת המהדורה מקשרים בין שרטוט למודל. מהדורות וגרסאות מראה אינן מתאחדות בגלל מספר חלק משותף.

[תושבות ותבניות לעור האלקטרוני](../../mechanics/README.md)

</div>
