<div dir="rtl" lang="he">

עברית · [English](README.en.md)

# מעגלים מודפסים - ROBOSKIN

[חומרה](../README.md) · [רשימת חומרים לרובוט](../04_BOM/README.md) · [צמות](../03_Harness/README.md)

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

## קישורים ישירים לכל קובצי הייצור

בבדיקה מול עץ המקור בתאריך 25 באוקטובר 2026, מהדורה `18ca38832cde37a8a4349cff8fbb565f05c6f254`, נמצאו **כל 88 קובצי תיקיית המעגלים** גם במאגר זה: 85 קובצי ייצור ועזר ושלושה מסמכי README. נוספו להם שלוש גרסאות Markdown באנגלית ותרגום אנגלי להערת ההרכבה של MAIN, ובסך הכול 92 קבצים בתיקייה זו. נתיבי הקבצים המותאמים מופיעים ב[רשומת המקור והמסירה](../provenance/delivery_inventory.json).

הקישורים בטבלה פותחים את הקבצים עצמם. להורדת קובץ בינרי ב־GitHub יש לבחור **Download raw file**. ארכיון Gerber מכיל את נתוני ייצור הלוח; הוא אינו תחליף למקור סכמטי הניתן לעריכה.

| לוח | רשימת רכיבים | נתוני ייצור | מודל תלת־ממד | מיקומי רכיבים | דרישות הרכבה | תצוגת מעגל |
| --- | --- | --- | --- | --- | --- | --- |
| [חיבור גמיש USB3](01_USB3_Flexible_Interconnect/) | [XLSX](01_USB3_Flexible_Interconnect/01_BOM_FPC_2026-09-18.xlsx) | [ZIP](01_USB3_Flexible_Interconnect/02_Gerber_FPC_2026-09-18.zip) | [STEP](01_USB3_Flexible_Interconnect/03_3D_FPC_2026-09-18.step) | [XLSX](01_USB3_Flexible_Interconnect/04_CPL_FPC_2026-09-18.xlsx) | [XLSX](01_USB3_Flexible_Interconnect/05_Assembly_Requirements_FPC.xlsx) | [PDF](01_USB3_Flexible_Interconnect/06_PCB_PDF_FPC_2026-09-18.pdf) |
| [משדר 433](02_RBE-COMM-433TX/) | [XLSX](02_RBE-COMM-433TX/01_BOM_433TX_2026-09-20.xlsx) | [ZIP](02_RBE-COMM-433TX/02_Gerber_433TX_2026-09-20.zip) | [STEP](02_RBE-COMM-433TX/03_3D_433TX_2026-09-20.step) | [XLSX](02_RBE-COMM-433TX/04_CPL_433TX_2026-09-20.xlsx) | [XLSX](02_RBE-COMM-433TX/05_Assembly_Requirements_433TX.xlsx) | [PDF](02_RBE-COMM-433TX/06_PCB_PDF_433TX_2026-09-20.pdf) |
| [בקר ראשי](03_RBE-MAIN-RK3588S/) | [XLSX](03_RBE-MAIN-RK3588S/01_BOM_MAIN_2026-09-18.xlsx) | [ZIP](03_RBE-MAIN-RK3588S/02_Gerber_MAIN_2026-09-18.zip) | [STEP](03_RBE-MAIN-RK3588S/03_3D_MAIN_2026-09-09.step) | [XLSX](03_RBE-MAIN-RK3588S/04_CPL_MAIN_2026-09-18.xlsx) | [XLSX](03_RBE-MAIN-RK3588S/05_Assembly_Requirements_MAIN.xlsx) | לא פורסם במקור |
| [מאוורר](04_RBE-PWR-FAN/) | [XLSX](04_RBE-PWR-FAN/01_BOM_FAN_V2.0.xlsx) | [ZIP](04_RBE-PWR-FAN/02_Gerber_FAN_V2.0.zip) | [STEP](04_RBE-PWR-FAN/03_3D_FAN_V2.0.step) | [XLSX](04_RBE-PWR-FAN/04_CPL_FAN_V2.0.xlsx) | [XLSX](04_RBE-PWR-FAN/05_Assembly_Requirements_FAN_V2.0.xlsx) | [PDF](04_RBE-PWR-FAN/06_PCB_PDF_FAN_V2.0.pdf) |
| [מתאם כף יד](05_RBE-PWR-HANDPlusPro/) | [XLSX](05_RBE-PWR-HANDPlusPro/01_BOM_HAND_2026-09-09.xlsx) | [ZIP](05_RBE-PWR-HANDPlusPro/02_Gerber_HAND.zip) | [STEP](05_RBE-PWR-HANDPlusPro/03_3D_HAND.step) | [XLSX](05_RBE-PWR-HANDPlusPro/04_CPL_HAND.xlsx) | [XLSX](05_RBE-PWR-HANDPlusPro/05_Assembly_Requirements_HAND.xlsx) | [PDF](05_RBE-PWR-HANDPlusPro/06_PCB_PDF_HAND.pdf) |
| [ראש](06_RBE-PWR-HEAD/) | [XLSX](06_RBE-PWR-HEAD/01_BOM_HEAD_2026-09-09.xlsx) | [ZIP](06_RBE-PWR-HEAD/02_Gerber_HEAD.zip) | [STEP](06_RBE-PWR-HEAD/03_3D_HEAD_2026-09-28.step) | [XLSX](06_RBE-PWR-HEAD/04_CPL_HEAD_2026-09-16.xlsx) | [XLSX](06_RBE-PWR-HEAD/05_Assembly_Requirements_HEAD.xlsx) | [PDF](06_RBE-PWR-HEAD/06_PCB_PDF_HEAD_2026-09-16.pdf) |
| [גיבוי והחלפה חמה](07_RBE-PWR-HOTSWAP/) | [XLSX](07_RBE-PWR-HOTSWAP/01_BOM_HOTSWAP_2026-09-18.xlsx) | [ZIP](07_RBE-PWR-HOTSWAP/02_Gerber_HOTSWAP_2026-09-17.zip) | [STEP](07_RBE-PWR-HOTSWAP/03_3D_HOTSWAP_2026-09-18.step) | [XLSX](07_RBE-PWR-HOTSWAP/04_CPL_HOTSWAP_2026-09-18.xlsx) | [XLSX](07_RBE-PWR-HOTSWAP/05_Assembly_Requirements_HOTSWAP.xlsx) | [PDF](07_RBE-PWR-HOTSWAP/06_PCB_PDF_HOTSWAP_2026-09-18.pdf) |
| [קבלי מנוע](08_RBE-PWR-MCAP/) | [XLSX](08_RBE-PWR-MCAP/01_BOM_MCAP_2026-09-07.xlsx) | [ZIP](08_RBE-PWR-MCAP/02_Gerber_MCAP.zip) | [STEP](08_RBE-PWR-MCAP/03_3D_MCAP_2026-09-16.step) | [XLSX](08_RBE-PWR-MCAP/04_CPL_MCAP_2026-09-16.xlsx) | [XLSX](08_RBE-PWR-MCAP/05_Assembly_Requirements_MCAP.xlsx) | [PDF](08_RBE-PWR-MCAP/06_PCB_PDF_MCAP_2026-09-16.pdf) |
| [מתאם סוללה](09_RBE-PWR-MINGMEI-BC/) | לא פורסם במקור | [ZIP](09_RBE-PWR-MINGMEI-BC/02_Gerber_MINGMEI-BC.zip) | [STEP](09_RBE-PWR-MINGMEI-BC/03_3D_MINGMEI-BC_2026-09-16.step) | [XLSX](09_RBE-PWR-MINGMEI-BC/04_CPL_MINGMEI-BC_2026-09-16.xlsx) | [XLSX](09_RBE-PWR-MINGMEI-BC/05_Assembly_Requirements_MINGMEI-BC.xlsx) | [PDF](09_RBE-PWR-MINGMEI-BC/06_PCB_PDF_MINGMEI-BC_2026-09-16.pdf) |
| [חיישן אינרציאלי](10_RBE-SENS-IMU/) | [XLSX](10_RBE-SENS-IMU/01_BOM_IMU_2026-09-09.xlsx) | [ZIP](10_RBE-SENS-IMU/02_Gerber_IMU.zip) | [STEP](10_RBE-SENS-IMU/03_3D_IMU_2026-09-16.step) | [XLSX](10_RBE-SENS-IMU/04_CPL_IMU_2026-09-16.xlsx) | [XLSX](10_RBE-SENS-IMU/05_Assembly_Requirements_IMU.xlsx) | [PDF](10_RBE-SENS-IMU/06_PCB_PDF_IMU_2026-09-16.pdf) |
| [מטען](11_RBE_PWR_140WCHG/) | [XLSX](11_RBE_PWR_140WCHG/01_BOM_140WCHG_2026-09-09.xlsx) | [ZIP](11_RBE_PWR_140WCHG/02_Gerber_140WCHG.zip) | [STEP](11_RBE_PWR_140WCHG/03_3D_140WCHG_2026-09-16.step) | [XLSX](11_RBE_PWR_140WCHG/04_CPL_140WCHG_2026-09-16.xlsx) | [XLSX](11_RBE_PWR_140WCHG/05_Assembly_Requirements_140WCHG.xlsx) | [PDF](11_RBE_PWR_140WCHG/06_PCB_PDF_140WCHG_2026-09-16.pdf) |
| [רכזת אחורית](12_RBE_PWR_BACKHUB/) | [XLSX](12_RBE_PWR_BACKHUB/01_BOM_BACKHUB_2026-09-14.xlsx) | [ZIP](12_RBE_PWR_BACKHUB/02_Gerber_BACKHUB_V2.1.zip) | [STEP / ZIP](12_RBE_PWR_BACKHUB/03_3D_BACKHUB_2026-09-28.zip) | [XLSX](12_RBE_PWR_BACKHUB/04_CPL_BACKHUB_V2.1.xlsx) | [PDF](12_RBE_PWR_BACKHUB/05_Assembly_Requirements_BACKHUB.pdf) | [PDF](12_RBE_PWR_BACKHUB/06_PCB_PDF_BACKHUB_V2.1.pdf) |
| [תאורה](13_Lighting_Board/) | [XLSX](13_Lighting_Board/01_BOM_LAMP_2026-09-07.xlsx) | [ZIP](13_Lighting_Board/02_Gerber_LAMP.zip) | [STEP](13_Lighting_Board/03_3D_LAMP_2026-09-16.step) | [XLSX](13_Lighting_Board/04_CPL_LAMP_2026-09-16.xlsx) | [XLSX](13_Lighting_Board/05_Assembly_Requirements_LAMP.xlsx) | [PDF](13_Lighting_Board/06_PCB_PDF_LAMP_2026-09-16.pdf) |
| [חיווי הספק אחורי](14_Rear_Power_Indicator/) | [XLSX](14_Rear_Power_Indicator/01_BOM_INDICATOR_2026-09-16.xlsx) | [ZIP](14_Rear_Power_Indicator/02_Gerber_INDICATOR.zip) | [STEP](14_Rear_Power_Indicator/03_3D_INDICATOR_2026-09-16.step) | [XLSX](14_Rear_Power_Indicator/04_CPL_INDICATOR_2026-09-16.xlsx) | [XLSX](14_Rear_Power_Indicator/05_Assembly_Requirements_INDICATOR.xlsx) | [PDF](14_Rear_Power_Indicator/06_PCB_PDF_INDICATOR_2026-09-16.pdf) |

קובצי עזר נוספים:

- FPC: [תמונת ייחוס להרכבה](01_USB3_Flexible_Interconnect/07_Assembly_Reference_FPC.jpg).
- MAIN: [תמונת ייחוס להרכבה](03_RBE-MAIN-RK3588S/07_Assembly_Reference_MAIN.jpg), [הערת הרכבה בעברית](03_RBE-MAIN-RK3588S/07_Assembly_Reference_MAIN.txt) ו[באנגלית](03_RBE-MAIN-RK3588S/07_Assembly_Reference_MAIN.en.txt).
- HEAD: [הוראות רכיבים שאינם מורכבים](06_RBE-PWR-HEAD/README.md).
- 140WCHG: [הוראות רכיבים שאינם מורכבים](11_RBE_PWR_140WCHG/README.md).

הפערים במקור מסומנים במפורש: אין BOM ללוח MINGMEI-BC ואין PDF נפרד של המעגל ללוח MAIN. אין בעץ המקור קובצי סכמות או עריכת PCB בפורמט המקורי. לא הומצאו קבצים חסרים, ותאריכים שונים בשמות הקבצים נשמרו; התאמת מהדורות חייבת להיבדק לפי דרישות ההרכבה לפני הזמנה. הלוחות המיובאים הם לוחות פלטפורמת הרובוט; מעגלי החישה החדשים של העור מתועדים בנפרד בקישור להלן.

[תכנון המעגלים החדשים לעור](../../electronics/README.md)

</div>
