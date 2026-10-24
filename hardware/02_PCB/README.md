<div dir="rtl" lang="he">

עברית · [English](README.en.md)

# מעגלים מודפסים - ROBOSKIN

[חומרה](../README.he.md) · [רשימת חומרים לרובוט](../04_BOM/README.md) · [צמות](../03_Harness/README.md)

כאן נתוני ייצור ל־14 משפחות לוחות של פלטפורמת החומרה. מספר החלק והמהדורה מבוססים על מסמכי דרישות ההרכבה. זוהי חבילת ייצור, לא מקור סכמטי מלא שניתן לעריכה.

| תיקייה | מספר חלק | מהדורה |
| --- | --- | --- |
| [חיבור גמיש USB3](01_USB3_Flexible_Interconnect/) | ROBOSKIN.0066 | V1.0 |
| [משדר 433](02_RBE-COMM-433TX/) | ROBOSKIN.0041 | V1.0 |
| [בקר ראשי](03_RBE-MAIN-RK3588S/) | ROBOSKIN.0073 | V1.6.1pro |
| [מאוורר](04_RBE-PWR-FAN/) | ROBOSKIN.0009 | V2.0 |
| [מתאם כף יד](05_RBE-PWR-HANDPlusPro/) | ROBOSKIN.0040 | V1.0 |
| [ראש](06_RBE-PWR-HEAD/) | ROBOSKIN.0298 | V2.0 |
| [גיבוי והחלפה חמה](07_RBE-PWR-HOTSWAP/) | ROBOSKIN.0064 | V2.0 |
| [קבלי מנוע](08_RBE-PWR-MCAP/) | ROBOSKIN.0006 | V3.1 |
| [מתאם סוללה](09_RBE-PWR-MINGMEI-BC/) | ROBOSKIN.0008 | V1.1 |
| [חיישן אינרציאלי](10_RBE-SENS-IMU/) | ROBOSKIN.0007 | V1.0 |
| [מטען](11_RBE_PWR_140WCHG/) | ROBOSKIN.0042 | V1.0 |
| [רכזת אחורית](12_RBE_PWR_BACKHUB/) | ROBOSKIN.0297 | V2.1 |
| [תאורה](13_Lighting_Board/) | ROBOSKIN.0010 | V2.0 |
| [חיווי הספק אחורי](14_Rear_Power_Indicator/) | ROBOSKIN.0056 | V1.0 |

| קידומת | פורמט | שימוש |
| --- | --- | --- |
| 01_BOM | XLSX | רכיבים וכמויות ללוח יחיד |
| 02_Gerber | ZIP | נתוני ייצור המעגל |
| 03_3D | STEP / ZIP | מעטפת מכנית וייחוס לנפח ההרכבה |
| 04_CPL | XLSX | קואורדינטות השמת רכיבים |
| 05_Assembly_Requirements | XLSX / PDF | דרישות ייצור, מספר חלק ומהדורה |
| 06_PCB_PDF | PDF | תצוגת הלוח |

רשימת רכיבי הלוח מתארת לוח אחד. רשימת החומרים של הרובוט מגדירה אילו לוחות ובאילו כמויות דרושים לתצורה. לרכש ולהרכבה יש להשתמש בקבצים מאותה מהדורה.

C30 בלוח HEAD ו־R59 בלוח 140WCHG אינם מורכבים. [הוראות HEAD](06_RBE-PWR-HEAD/README.md) ו[הוראות 140WCHG](11_RBE_PWR_140WCHG/README.md) קובעות כיצד להשתמש ב־NC_List.

מודל BACKHUB נמצא ב[ארכיון STEP](12_RBE_PWR_BACKHUB/03_3D_BACKHUB_2026-09-28.zip). לאחר חילוץ מתקבל `03_3D_BACKHUB_2026-09-28.step`.

[שרטוט BACKHUB V2.1](12_RBE_PWR_BACKHUB/06_PCB_PDF_BACKHUB_V2.1.pdf)

ל־MINGMEI-BC חסרה רשימת רכיבי לוח במקור שנסקר. שמות בעברית אינם משלימים נתון ייצור חסר. סימון גרפי צרוב ב־Gerber אינו מוחלף אוטומטית.

[תכנון המעגלים החדשים לעור](../../electronics/README.md)

</div>
