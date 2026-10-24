# Sensing, materials and application references: critical review

Prepared 24 October 2026 for the project engineering plan. Coverage: Cheng et al. references **1–19, 30–34 and 36–40**, exactly 29 records. The other references and ProxySKIN 2024 are handled by the coordinating review. No original paper has been purchased and no author has been contacted.

## Integration memo

The defensible baseline is an inexpensive, replaceable limb covering that detects several contacts and ordinal normal loading, with explicitly sparse temperature sensing. This review supports local digitization and regional networking, but does **not** establish that the proposed material stack has passed fatigue, coverage, cost or industrial-yield requirements. Evidence levels below distinguish complete main text, selected full-text sections, indexed original excerpts, primary abstracts and citation-only verification.

Concrete changes recommended to the project specification:

1. **Make installed-layer mechanics a release gate.** Qualify the final cover, adhesive, sensor, backing and cable assembly on the intended limb curvature. Measure baseline/preload after fitting and after replacing the cover. Use a sliding/overlapping seam or leave a mapped blind band at joints; do not stretch an ordinary flex laminate across a crease. The relevant methodological basis is [8], chapter 4.1, and [9], sections III–IV. A bendable conductor alone does not validate a skin assembly.
2. **Separate the thermal promises.** The two NTCs measure their own local thermal environment. A small hot object elsewhere can be missed. Map a controlled heated/cooled contact across each panel and seam with independent surface thermometry, record location, force, temperature step, response delay and false pressure signal. Test local heat and uniform ambient change separately. The combined-layer precedent [7] and structural compensation in [17], sections III and IV-E, are different mechanisms. Do not claim full thermal coverage or use these NTCs as pressure-compensation references without evidence.
3. **Add matched dynamic and static tests.** A small actuator/indenter with an independently sampled load reference should apply repeatable contact profiles at randomized phases of the 100 Hz scan. Capture force onset, ADC acquisition, transmitted timestamp and host decision on one timebase. Use the deployed filter settings. Record detection probability, peak force before response, release/recovery time and post-overload offset. Begin with low-energy bench indentation; the thin outer film is not an impact absorber. [8], chapter 4.1, supplies the evaluation distinction.
4. **Characterize force/contact geometry honestly.** Measure center, edge, seam and between-taxel locations with at least small, nominal and broad indenters. Add two simultaneous contacts, several adjacent contacts, and a broad-area load; report confusion between neighboring sites. Publish contact-class performance rather than converting arbitrary ADC readings to kPa. [16], section VI-B–D, exposes contact-area dependence and receptive-field effects. For our 25 mm-pitch patch, nearest-site coordinate quantization alone is up to 12.5 mm on each axis, about 17.7 mm diagonally inside an ideal square cell; real mechanics and dead zones can be worse. This is a geometric bound, not measured accuracy.
5. **Keep adaptation auditable.** At boot, distinguish confirmed unloaded calibration from unknown/preloaded state. Freeze baseline while contact is latched or suspect, and log any rebasing. Test a slow force ramp, a 10-minute sustained load and a thermally drifting unloaded panel. Confirm release separately. [16], section V, gives an established touched-taxel freeze pattern, but its extracted pseudocode has a sign inconsistency; our implementation must be unit-tested against its intended signed deadband.
6. **Use a fair alternative benchmark.** If the resistive coupon fails repeatability, thermal stability or aging requirements, compare a spacer-fabric capacitive stack based on [17] with the same area, installed thickness, cover, contact fixture, sampling and acceptance limits. Do not call it a drop-in substitution or assume its published rate and thickness meet our specification. Obtain current material/process quotes independently; old papers establish feasibility routes, not 2026 prices.
7. **Budget information rather than wire count alone.** Four-wire centroid schemes cannot uniquely identify arbitrary multiple contacts [39]; active local scanning [9, 15, 16] preserves more information at the expense of electronics and power. Keep all 28 taxel identities. Record full-frame rate, scan skew, sample age and transport latency separately. [37], section IV, is a concrete warning against misreading per-conversion rate as full-array rate.
8. **Scope the application and novelty claim.** Whole-body haptics, protective layers, multi-modal skin, CAN/local processing and thousands of flexible tactile sites are all prior art. An investable contribution can be a measured combination of installed cost per area, low mass, fast replacement, dependable multi-contact reporting and reproducible production. Demonstrate those with matched benchmarks and disclose blind regions. Skin sensing alone does not prove safe physical interaction, force control, balance, dexterity or human-equivalent perception.

### Proposed coupon/limb experiments (our engineering recommendations)

Use five independently assembled panels, including at least two sensor-material/adhesive batches when available. Keep manufacturing records: film lot, surface preparation, adhesive thickness, lamination pressure/time, alignment and cure/settle time. Do not silently discard failed panels; report first-pass yield and rework.

- Electrical isolation: replace sensors with fixed resistors, vary one channel over the intended impedance range, and verify the other 27 channels; repeat with motor PWM active and with cable flexing. Then repeat mechanically with real two-point and broad loads. This separates electrical coupling from legitimate mechanical spreading.
- Drift and creep: record both constant-force holds (deadweight with known contact geometry) and constant-displacement holds (fixed indenter), followed by release and recovery. Randomize loading order; include repeated cycles without long rests. Publish raw traces and thresholds, including false positives/negatives.
- Curvature and service: compare flat, minimum-radius and nominal-radius mounting; cover replacement; cable installation; dry wiping and specified cleaning fluid. Repeat detection tests after each operation. Limit claims to the conditions actually tested.
- Motion: use a joint fixture across the intended angular range and velocity, with the assembled routing. Measure added torque/drag, cable slack, wrinkle-induced events and connector strain. Cycle the installed assembly, not just the foil. Separate exploratory cycles from qualification cycles and document failures.
- Thermal: place a known-temperature contact both above and between NTCs and on seams. Record effective detection region and delay with the robot electronics powered. Repeat with constant mechanical load to reveal cross-sensitivity. An undetected heated contact outside the claimed region is a coverage result, not a firmware defect.
- Production economics: time placement, lamination, connector assembly, programming, test, calibration and replacement on each panel. Calculate cost per accepted panel after scrap and rework, not raw material cost. Keep sensors, controller, mounting, protection and harness in the installed mass total.

These are test instructions and decision gates, not assertions of an experimentally validated finished product. Failure must change the stack, requirement or product claim; a favorable paper cannot replace that evidence.

## Access accounting

- `citation_only`: 3 references.
- `primary_abstract`: 8 references.
- `primary_full_text_main`: 1 reference.
- `primary_full_text_selected`: 12 references.
- `primary_indexed_excerpt`: 5 references.

`primary_full_text_main` means the substantive paper text was read; it does not imply independent replication or a complete audit of all cited work. `primary_full_text_selected` is deliberately narrower. `primary_indexed_excerpt` means only the search-accessible portions of an original author/repository PDF were available, even when a full PDF URL exists. `primary_abstract` supports only abstract-level claims. `citation_only` supplies bibliographic history and no audited experimental claim. Figure captions were inspected where indicated; unavailable images are not represented as visually inspected.

PDF download attempts through the shell failed DNS in this sandbox. Browser retrieval supplied many full texts, while some publishers returned verification pages, 403, timeout or subscription-only responses. These are access gaps, not evidence that a paper has no useful results. The unreviewed portions must not be cited as verified circuit details. No modern supplier availability, quotations, patent freedom-to-operate or safety certification is established by this review.

## Numbered records

### [1] Automated tactile sensing

L. D. Harmon, International Journal of Robotics Research 1(2), 3–32, 1982. [Primary source or identity record](https://journals.sagepub.com/doi/10.1177/027836498200100201)

**Evidence:** citation_only

**Read scope:** Publisher metadata and exposed footnotes; full article unavailable. Not treated as a full-text or abstract review.

**Finding:** An early review establishing the historical depth of automated tactile sensing. No quantitative sensor result from this article is adopted here.

**Limit:** Published material reflects information acquired before January 1981; historical recommendations are not current component specifications.

**Plan action:** Use only as historical background. Set limb requirements from the actual contact tasks and acceptance tests, rather than invoking human-equivalence targets from an unread historical review.

**Novelty implication:** Broad tactile sensing cannot be claimed as a new concept.

**Bibliographic/access note:** Publisher gives pages 3–32; Cheng bibliography/user transcription gives 3–31. DOI 10.1177/027836498200100201.

### [2] E-skin: From humanoids to humans

R. Dahiya, Proceedings of the IEEE 107(2), 247–252, 2019. [Primary source or identity record](https://eprints.gla.ac.uk/183481/1/183481.pdf)

**Evidence:** primary_full_text_selected

**Read scope:** Accepted manuscript: introduction and sections comparing electronic-skin requirements, integration routes and flexible/printed electronics; not every concluding paragraph or cited work.

**Finding:** The viewpoint contrasts conventional components on flexible substrates with printed and ultrathin electronics. More discrete functionality competes with conformability; requirements depend on the application.

**Limit:** A perspective article is not evidence that a particular printed film has acceptable fatigue life, manufacturing yield, cost or multimodal accuracy.

**Plan action:** Keep a small number of proven modalities in the first product. Put packaged electronics on mechanically supported islands; qualify the complete interconnect and cover. Track area, installed mass and repair time separately from sensor-element thickness.

**Novelty implication:** Flexible multimodal skin and distributed electronics were already established research directions.

**Bibliographic/access note:** DOI 10.1109/JPROC.2018.2890729; repository manuscript is a primary author source.

### [3] Tactile sensing—From humans to humanoids

R. S. Dahiya, G. Metta, M. Valle and G. Sandini, IEEE Transactions on Robotics 26(1), 1–20, 2010. [Primary source or identity record](https://www.robotcub.org/misc/papers/10_Dahiya_etal.pdf)

**Evidence:** primary_indexed_excerpt

**Read scope:** Indexed author/project PDF excerpts: classification figure 2, section III physiology, encoding and regional sensing requirements. Direct PDF retrieval failed; author-uploaded proof excerpts also located.

**Finding:** The review distinguishes cutaneous from joint/force sensing, fingertip arrays from large-area skin, and slowly adapting from rapidly adapting tactile channels. Receptor density and required temporal/spatial performance differ by body site.

**Limit:** Biological receptor counts and perceptual acuity do not directly specify electronic taxel pitch, ADC resolution or required robot bandwidth. This is a review, not validation of our sensor stack.

**Plan action:** Preserve held-contact state alongside onset/change events. Specify coarse arm/leg contact localization independently from fingertip dexterity; retain joint encoders and actuator feedback. Test a sustained load so baseline adaptation cannot erase a real contact.

**Novelty implication:** Biomimetic layering and biological data reduction are prior art.

**Bibliographic/access note:** DOI 10.1109/TRO.2009.2033627; author proof: https://www.researchgate.net/publication/220032969_Tactile_Sensing-From_Humans_to_Humanoids

### [4] Directions toward effective utilization of tactile skin: A review

R. S. Dahiya et al., IEEE Sensors Journal 13(11), 4121–4138, 2013. [Primary source or identity record](https://eprints.gla.ac.uk/95989/)

**Evidence:** primary_abstract

**Read scope:** Glasgow institutional abstract and bibliographic record; TUM institutional abstract. Full original text not read.

**Finding:** The authors frame useful tactile skin as a system problem involving distributed coverage, simultaneous contacts, acquisition, calibration and real-time interpretation.

**Limit:** The abstract supplies no verified circuit values, experimental operating envelope or manufacturing economics.

**Plan action:** Keep an acceptance matrix spanning material, acquisition, communication, body coordinates and application. A working single taxel cannot close the multi-contact, coverage or latency requirements.

**Novelty implication:** System-level integration, distributed control and calibration are longstanding research topics.

**Bibliographic/access note:** DOI 10.1109/JSEN.2013.2279056. TUM corroboration: https://portal.fis.tum.de/en/publications/directions-toward-effective-utilization-of-tactile-skin-a-review/

### [5] Proximity sensing in robot manipulator motion planning: System and implementation issues

E. Cheung and V. J. Lumelsky, IEEE Transactions on Robotics and Automation 5(6), 740–751, 1989. [Primary source or identity record](https://www.edcheung.com/job/sbr/IEEE88.pdf)

**Evidence:** primary_full_text_selected

**Read scope:** Author-hosted manuscript: system architecture/local planning, approximately manuscript pages 2–4; author project page identifying the publication. Not all experiments.

**Finding:** The tested infrared arrangement provides a roughly 10–15 cm obstacle-detection envelope around the arm and coordinates sensing with about 50 commanded positions per second. Motion is constrained by the sensed free envelope.

**Limit:** The collision-avoidance argument depends on coverage, robot velocities, sensor characteristics and control timing; it is not a guarantee for arbitrary robots or objects.

**Plan action:** Do not describe our pressure-only skin as detecting obstacles before touch. If proximity is added, validate every joint pose and object reflectance/angle against the actual stopping envelope and measured latency.

**Novelty implication:** Distributed sensitive-arm obstacle avoidance predates the proposed product by decades.

**Bibliographic/access note:** Author source identifies this file with the 1989 publication despite its IEEE 88 filename; project page https://www.edcheung.com/job/sbr/sbr.html.

### [6] Sensitive skin

V. J. Lumelsky, M. S. Shur and S. Wagner, IEEE Sensors Journal 1(1), 41–51, 2001. [Primary source or identity record](https://resenv.media.mit.edu/classarchive/MAS965/readings/sensitiveskin.pdf)

**Evidence:** primary_full_text_selected

**Read scope:** Original article via MIT teaching archive: introduction; hardware/device requirements and low-cost-process discussion, printed pp.46–47. Other portions not exhaustively read.

**Finding:** The paper explicitly links local processing, simple sensing structures, fault tolerance, repairability and manufacture. It discusses rigid active islands joined by flexible interconnects and warns that large-area signal paths collect noise.

**Limit:** The manufacturing costs and forecasts are historical; they cannot be imported into a 2026 BOM. Proposed future millions-of-sensors systems are not demonstrated production yield.

**Plan action:** Keep analog runs short, digitize regionally, provide failed-channel reporting, and cost scrap/rework and replacement operations. Compare complete installed harnesses rather than copper mass alone.

**Novelty implication:** Low-cost, fault-tolerant, distributed artificial skin is an old objective; differentiation must be measured in implementation.

**Bibliographic/access note:** DOI 10.1109/JSEN.2001.923586.

### [7] Conformable, flexible, large-area networks of pressure and thermal sensors with organic transistor active matrixes

T. Someya et al., PNAS 102(35), 12321–12325, 2005. [Primary source or identity record](https://pmc.ncbi.nlm.nih.gov/articles/PMC1187825/)

**Evidence:** primary_full_text_selected

**Read scope:** Open primary main text, fabrication and pressure/thermal experiments, figures 1–5 captions; not supplementary data or independent replication.

**Finding:** A 12×12 network with 4 mm pitch combines pressure and thermal layers. Net geometry permits 25% extension; larger extension breaks strut wiring. The reported 2, 000 cycles at 20% concern simplified gold test structures, not complete skin. Organic circuitry uses −20/−40 V biases.

**Limit:** The combined thermal demonstration and transistor protection do not establish long-term humidity, abrasion or joint-fatigue performance of a commercial laminate.

**Plan action:** Use the established layered idea with simpler low-voltage electronics, but test heat paths and full-assembly strain independently. Do not substitute conductor-coupon fatigue for connector, adhesive, sensor and wear-cover fatigue.

**Novelty implication:** Pressure-plus-temperature laminated skin is explicit prior art from 2005.

**Bibliographic/access note:** DOI 10.1073/pnas.0502392102. Full paper read through the substantive main experiments; no claim to have visually inspected all images.

### [8] Artificial Skin in Robotics: A Comprehensive Interface for System-Environment Interaction

M. Strohmayr, doctoral dissertation, Karlsruhe Institute of Technology, 2012. [Primary source or identity record](https://publikationen.bibliothek.kit.edu/1000028782/2186259)

**Evidence:** primary_full_text_selected

**Read scope:** Selected thesis text: design tradeoffs in chapter 3; chapter 4.1 test procedures, printed pp.152–159; conclusions. Not the complete 217-page PDF.

**Finding:** The thesis separates sensitivity and collision protection and evaluates the sensor with its electronics. Its proposed testing includes static indentation, repeatability, dynamic impact, recovery and overload; filtering affects sensitivity and reaction time.

**Limit:** These proposed evaluation procedures are not a universal certification standard. The thesis itself identifies unresolved performance tradeoffs.

**Plan action:** Add controlled dynamic indentation with an independent load/time reference, overload recovery and identical deployed filter settings. The thin TPU wear film is not an impact-energy absorber. Measure seam and mounted-curvature behavior, not flat coupons alone.

**Novelty implication:** Combining mechanical protection with sensing is established; a quantified thin, serviceable implementation can still differentiate.

**Bibliographic/access note:** KIT title above is fuller than Cheng’s shortened “Artificial skin for robots.” DOI 10.5445/IR/1000028782.

### [9] Conformable and scalable tactile sensor skin for curved surfaces

Y. Ohmura, Y. Kuniyoshi and A. Nagakubo, ICRA 2006, 1348–1353. [Primary source or identity record](https://bdml.stanford.edu/twiki/pub/Haptics/TactileChapterReferences/Ohmura-ICRA06.pdf)

**Evidence:** primary_full_text_selected

**Read scope:** Original six-page article: abstract, requirements, sections III–IV and beginning of V, figure captions 1–10. Remaining experiment/conclusion paragraphs not exhaustively read.

**Finding:** The implementation places 32 photo-reflector sensing elements and a microcontroller on a cut/fold flexible substrate. Optical emitters are time-shared to control power; local SMBus connects to an in-body ring network. Bus capacitance constrains scaling.

**Limit:** Address-space capacity is not simultaneous full-skin throughput. The reported bare-sheet mass excludes subsequently added foam and the complete installed network. Foldability does not imply repeated stretchability.

**Plan action:** Use a small panel family and controlled mechanical relief. Measure aggregate power at the actual scan duty cycle, installed mass, and complete-frame freshness at maximum node count. Retain compact local analog wiring and a robust regional digital link.

**Novelty implication:** Local scanning, reduced wiring, conformable modules and cut-to-shape skin were demonstrated in 2006.

**Bibliographic/access note:** DOI 10.1109/ROBOT.2006.1641896.

### [10] Development of the tactile sensor system of a human-interactive robot RI-MAN

T. Mukai, M. Onishi, T. Odashima, S. Hirano and Z. Luo, IEEE Transactions on Robotics 24(2), 505–512, 2008. [Primary source or identity record](https://repository.gatech.edu/bitstreams/39fe7cef-a8a4-4ebb-81a4-097c885fa7bd/download)

**Evidence:** primary_indexed_excerpt

**Read scope:** Indexed original first-page abstract/introduction from Georgia Tech repository. PDF download returned 403; main experiments not read.

**Finding:** The original abstract reports an integrated soft areal tactile system on RI-MAN and a human-dummy lifting demonstration. No numerical sensor accuracy or robustness result from the full article is adopted here.

**Limit:** Demonstrating a complete robot handling a dummy does not isolate sensor contribution or validate the proposed resistive panel. Semiconductive-pressure-sensor construction described in other reviews is secondary evidence only.

**Plan action:** Use a supported, low-mass test object for initial arm/body contact experiments. Document independently what skin detection contributes, what robot actuation contributes, and what protection is provided mechanically.

**Novelty implication:** Large-area soft robot skin for physical assistance is established prior art.

**Bibliographic/access note:** DOI 10.1109/TRO.2008.917006; publisher article 4458232. Related open chapters were not substituted for this original.

### [11] ARMAR-III: An integrated humanoid platform for sensory-motor control

T. Asfour et al., IEEE-RAS Humanoid Robots, 2006, 169–175. [Primary source or identity record](https://h2t.iar.kit.edu/pdf/Asfour2006b.pdf)

**Evidence:** primary_full_text_selected

**Read scope:** Original article sections on arm sensing and artificial skin, pp.2–3 of PDF, and hierarchical architecture/figure 5. Not all platform experiments.

**Finding:** Shoulder and arm skin is integrated through dedicated controllers into CAN, alongside separate joint-torque and wrist force/torque sensors. The architecture separates task planning, coordination and execution.

**Limit:** This platform paper does not provide a standalone production recipe or prove that coarse skin replaces accurate joint or wrist sensing.

**Plan action:** Expose timestamped contact, location, confidence and faults through a dedicated driver. Leave actuator regulation in the existing robot control layer; test timeout handling at every boundary.

**Novelty implication:** CAN-connected local skin processing and whole-robot integration were already present in 2006.

**Bibliographic/access note:** DOI 10.1109/ICHR.2006.321380.

### [12] Design of human symbiotic robot TWENDY-ONE

H. Iwata and S. Sugano, ICRA 2009, 580–586. [Primary source or identity record](https://waseda.elsevierpure.com/en/publications/design-of-human-symbiotic-robot-twendy-one/)

**Evidence:** primary_abstract

**Read scope:** Author-institution publication record and abstract. Original seven-page article not accessed.

**Finding:** The design combines passive arm mechanisms and mechanical softness in joints and skin, derived from a set of assistance-task requirements.

**Limit:** The abstract does not expose contact-force limits, hazard validation, individual skin accuracy or a component-level manufacturing cost.

**Plan action:** Specify service tasks before adding modalities. Verify joint range, friction, cable pull and sensor prestress on a limb fixture; sensing alone cannot make an otherwise stiff mechanism mechanically compliant.

**Novelty implication:** Soft covering combined with passive joint mechanisms is prior art.

**Bibliographic/access note:** DOI 10.1109/ROBOT.2009.5152702. Related Japanese 2008 appearance-design paper is a distinct publication.

### [13] Humanoid robot which can lift a 30 kg box by whole body contact and tactile feedback

Y. Ohmura and Y. Kuniyoshi, IROS 2007, 1136–1141. [Primary source or identity record](https://www.isi.imi.i.u-tokyo.ac.jp/publication/)

**Evidence:** citation_only

**Read scope:** Author laboratory bibliography and publisher record link verified. Original article unavailable; secondary syndicated abstract seen but not used as verified experimental evidence.

**Finding:** The article identity/title documents an early whole-body-contact and tactile-feedback claim. The 30 kg result is a title-level reported claim here, not an audited replication.

**Limit:** No verified gains, failure statistics, force distribution or safety conditions from the original are available in this review.

**Plan action:** Cite the precedent without importing its payload. For our proof, compare skin-enabled and disabled behavior on the same restrained, low-energy fixture with objective contact-detection and response metrics.

**Novelty implication:** Whole-body tactile lifting is not a new application concept.

**Bibliographic/access note:** DOI 10.1109/IROS.2007.4399592; publisher https://ieeexplore.ieee.org/document/4399592 requires JavaScript verification.

### [14] Whole body haptics for augmented humanoid task capabilities

Y. Kuniyoshi, Y. Ohmura and A. Nagakubo, Robotics Research, Springer Tracts in Advanced Robotics 66, 61–73. [Primary source or identity record](https://link.springer.com/chapter/10.1007/978-3-642-14743-2_6)

**Evidence:** primary_abstract

**Read scope:** Publisher abstract, chapter metadata and references; subscription full chapter unavailable.

**Finding:** The abstract reports whole-body tactile covering of an adult-size humanoid and contact-motion experiments including a 66 kg human dummy.

**Limit:** The abstract alone cannot validate the loading conditions, control robustness or economics. It cannot justify human-lifting demonstrations with a home-lab prototype.

**Plan action:** Keep the early demonstrator on arms and legs, with bounded low-load contact tasks and no human support. Explain the eventual application without implying its hardware/control validation is already complete.

**Novelty implication:** Whole-body contact capability and human-like distributed haptics are established motivations.

**Bibliographic/access note:** Publisher citation/copyright says 2010; Cheng/user list says 2011 and lab bibliography also lists the 2011 book. Keep this edition/year discrepancy visible. DOI 10.1007/978-3-642-14743-2_6.

### [15] An embedded artificial skin for humanoid robots

G. Cannata, M. Maggiali, G. Metta and G. Sandini, MFI 2008, 434–438. [Primary source or identity record](https://robotcub.org/misc/papers/08_cannata.pdf)

**Evidence:** primary_full_text_main

**Read scope:** Entire substantive five-page original article, including architecture, transducer, microcontroller, experiments and conclusions; figure captions. Images not independently resolved.

**Finding:** Twelve capacitive taxels per triangle use AD7147 conversion; up to 16 triangles/192 taxels connect through local buses to one MCU/CAN. A grounded deformable electrode enables contact from insulating objects and shielding. About 500 Hz averaged sensing trades spatial detail for speed; individual channels are slower.

**Limit:** The reported prototype is six triangles, with quantitative experiments ongoing. Three-to-five-millimeter foam differs from our thin laminate. Port count does not imply adaptive rerouting.

**Plan action:** Keep local aggregation and distinguish normal-force sensing from bare capacitive human-touch detection. If evaluating capacitive alternatives, include the full ground-electrode, dielectric and cover stack and measure both spatial detail and response time.

**Novelty implication:** Modularity, local conversion, CAN aggregation and adaptive spatial resolution are prior art.

**Bibliographic/access note:** DOI 10.1109/MFI.2008.4648033. Extracted area/power units in early PDF are ambiguous; no power-density number is adopted.

### [16] Methods and technologies for the implementation of large-scale robot tactile sensors

A. Schmitz et al., IEEE Transactions on Robotics 27(3), 389–400, 2011. [Primary source or identity record](https://www.researchgate.net/publication/224238240_Methods_and_Technologies_for_the_Implementation_of_Large-Scale_Robot_Tactile_Sensors)

**Evidence:** primary_full_text_selected

**Read scope:** Author-uploaded manuscript: sections I, III, V and VI-A–D, assembly figure captions. Not every hysteresis equation or grasping trial.

**Finding:** The 16-bit CDC yielded 8 usable signal bits in that assembly. Drift adaptation freezes while touched. Probe geometry changes response, and some body configurations omit a top electrode and rely on a human ground plane.

**Limit:** The extracted drift pseudocode has an apparent missing minus sign versus its stated ±0.5 deadband; never copy it blindly. Published sensor performance does not transfer to our resistive laminate.

**Plan action:** Freeze baseline during contact; test slow ramps and sustained loads. Measure actual noise-limited resolution. Test plastic, metal and gloved contacts. Calibrate several probe diameters and mounted curvature rather than claiming pressure accuracy from one probe.

**Novelty implication:** Cheap replaceable COTS-based skin with distributed buses and calibration is prior art.

**Bibliographic/access note:** DOI 10.1109/TRO.2011.2132930. Uploader is coauthor Marco Maggiali; original author-site URL currently 404.

### [17] A flexible and robust large scale capacitive tactile system for robots

P. Maiolino, M. Maggiali, G. Cannata, G. Metta and L. Natale, IEEE Sensors Journal 13(10), 3910–3917, 2013. [Primary source or identity record](https://arxiv.org/pdf/1411.6837)

**Evidence:** primary_full_text_selected

**Read scope:** Author manuscript sections III–IV, integration text and experimental figure captions; most main text read, not supplementary data.

**Finding:** The design uses clothing-industry 3D spacer fabric and removable covers. On the flat 2 mm dielectric prototype, 15 load cycles with one-minute rests gave a maximum 9.1 fF cycle difference at 28.6 kPa, roughly 5% of range. Pressure-insensitive reference capacitors compensate structural thermal drift; they are not surface thermometers. The reported acquisition operates at 25 Hz.

**Limit:** Ten-minute constant-displacement relaxation is not a constant-force creep or lifetime test. Neither its thickness nor performance transfers to a 1.5 mm 100 Hzresistive stack.

**Plan action:** Use this as a capacitive fallback benchmark, subject to full-stack comparison. Separate thermal-point sensing from pressure compensation. Test both constant-force and constant-displacement holds plus local heating while loaded.

**Novelty implication:** Fabric-based, protected, serviceable robot skin predates this proposal.

**Bibliographic/access note:** DOI 10.1109/JSEN.2013.2258149. arXiv submission 2014 is an author copy of the 2013 article.

### [18] A new silicone structure for uSkin—A soft, distributed, digital 3-axis skin sensor and its integration on humanoid robot iCub

T. P. Tomo et al., IEEE Robotics and Automation Letters 3(3), 2584–2591, 2018. [Primary source or identity record](https://qmro.qmul.ac.uk/xmlui/bitstream/handle/123456789/55045/Jamone%20A%20New%20Silicone%202018%20Accepted.pdf?isAllowed=y&sequence=2)

**Evidence:** primary_indexed_excerpt

**Read scope:** Indexed primary accepted manuscript section III-A/B, tableI and figure 1–2 captions; direct repository PDF retrieval failed. Calibration/results not fully read.

**Finding:** Sixteen magnetic 3-axis cells occupy 26×27×6.05 mm; approximately 1 mm mounting tape adds thickness. Bumps and air gaps reduce normal-to-shear mechanical coupling. A first soft-silicone attempt allowed magnets to attract each other.

**Limit:** Full assembly is thicker and more complex than a thin resistive film. Performance in motor magnetic fields, chosen cover adhesives and our limb geometry remains unverified.

**Plan action:** Reserve this modality for a shear-sensing variant. If evaluated, test magnetic interference with motors energized, overload, cross-axis coupling and mounting-tape creep; include every protective/mounting layer in thickness and cost.

**Novelty implication:** Soft protected digital 3-axis skin is already demonstrated; simplified normal-contact coverage targets a different specification.

**Bibliographic/access note:** Use the accepted 2018 manuscript as the source; no unverified calibration accuracy or DOI is invented.

### [19] An adjustable force sensitive sensor with an electromagnet for a soft, distributed, digital 3-axis skin sensor

A. C. Holgado et al., IROS 2018, 2582–2588. [Primary source or identity record](https://waseda.elsevierpure.com/en/publications/an-adjustable-force-sensitive-sensor-with-an-electromagnet-for-a-/)

**Evidence:** primary_abstract

**Read scope:** Author-institution abstract and publication identity; original full text not read.

**Finding:** The prototype replaces a permanent magnet with an electromagnet so current can change force sensitivity in a soft magnetic sensor.

**Limit:** The abstract does not establish a mass-production cost or justify extra power, thermal coupling and calibration for approximate normal-pressure sensing.

**Plan action:** Exclude electromagnets from the baseline. Add them only if a specified force-range problem cannot be met passively and a measured benefit exceeds coil-power, heat and driver cost.

**Novelty implication:** Electronically adjustable magnetic tactile sensitivity is prior art.

**Bibliographic/access note:** DOI 10.1109/IROS.2018.8593757.

### [30] Tactile sensing in intelligent robotic manipulation—A review

J. Tegin and J. Wikander, Industrial Robot 32(1), 64–70, 2005. [Primary source or identity record](https://www.researchgate.net/publication/228667424_Tactile_sensing_in_intelligent_robotic_manipulation_-_a_review)

**Evidence:** primary_full_text_selected

**Read scope:** Author-uploaded text: introduction, sections 5.2–5.7 and conclusions. KTH thesis reprint located but oversized PDF could not be retrieved.

**Finding:** The review separates distributed contact sensing from intrinsic force/torque sensing. It discusses mechanical inversion through soft covers, FSR/capacitive drift and hysteresis, and the loss of contact-pattern information in few-wire analog schemes.

**Limit:** Its supplier listings and dimensions are historical. A single resultant force/position cannot identify an arbitrary set of simultaneous contacts.

**Plan action:** Preserve separate taxel identities for multi-contact limb sensing. Do not infer shear, friction, material hardness or accurate force from ordinal normal readings without additional measurement and a validated model.

**Novelty implication:** Resistive arrays, capacitance sensing, local processing and few-wire tactile tradeoffs are established.

**Bibliographic/access note:** DOI 10.1108/01439910510573318; uploader identified as author Johan Tegin.

### [31] Sensitive manipulation: Manipulation through tactile feedback

E. Torres-Jara and L. Natale, International Journal of Humanoid Robotics 15(1), 1850012, 2018. [Primary source or identity record](https://lornat75.github.io/pdfs/2018-torresjara-sensitive.pdf)

**Evidence:** primary_full_text_selected

**Read scope:** Author manuscript abstract/introduction, hardware figure 1 and sections 4.1.3–4.3, PDFpp.12–15. Not all experiments.

**Finding:** Obrero combines compliant actuation with tactile strategies for acquiring and maintaining contact. The text explicitly notes missed contacts at unsensed joint regions and a lift/retry strategy when immediate slip sensing is inadequate.

**Limit:** Success depends on hand hardware, force control and exploration strategies absent from our coarse arm/leg panels. It does not show that simply adding taxels delivers dexterity.

**Plan action:** Include unsensed joint seams in coverage maps. Demonstrate one bounded contact-aware behavior and compare against a baseline, recording missed contacts; do not claim general slip detection or dexterous grasping.

**Novelty implication:** Tactile-first manipulation and active contact exploration are prior art.

**Bibliographic/access note:** Accepted manuscript datedOctober 2017 for the 2018 publication.

### [32] High-density conformable tactile sensing glove

T. Sagisaka et al., IEEE-RAS Humanoids 2011, 537–542. [Primary source or identity record](https://ieeexplore.ieee.org/document/6100898)

**Evidence:** citation_only

**Read scope:** Author laboratory bibliography verified; original full text not accessed. Exact-paper syndicated abstract and a distinct 2012 JRSJarticle abstract were seen, and are not substituted for the original.

**Finding:** An established high-density sensing-glove research line. Original-paper performance numbers are not independently verified in this record.

**Limit:** Bibliographic aggregators merge the 2011 conference and 2012 Japanese journal article. Their results must not be silently treated as the same document.

**Plan action:** For our arm/leg application, evaluate range-of-motion change, cable pull and pressure offsets with the covering installed. Tree/branch geometry is a useful candidate, but requires complete laminate fatigue testing.

**Novelty implication:** High-density conformable sensing and joint-motion-aware routing are prior art, not a new conceptual claim.

**Bibliographic/access note:** DOI 10.1109/Humanoids.2011.6100898. Related primary 2012 paper: https://www.jstage.jst.go.jp/article/jrsj/30/7/30_30_711/_article/-char/en (DOI 10.7210/jrsj.30.711).

### [33] Development and applications of high-density tactile sensing glove

T. Sagisaka, Y. Ohmura, A. Nagakubo, K. Ozaki and Y. Kuniyoshi, EuroHaptics 2012, LNCS 7282, 445–456. [Primary source or identity record](https://link.springer.com/chapter/10.1007/978-3-642-31401-8_40)

**Evidence:** primary_abstract

**Read scope:** Publisher abstract and bibliographic record; subscription chapter not read in full.

**Finding:** The abstract describes 1, 052 pressure sites per hand using 1 mm elements on FPC, and human experiments relating pressure distribution to external-force direction and exploratory behavior.

**Limit:** Correlation in a human-worn glove does not establish calibrated robot shear-force measurement, full-body fatigue or inexpensive manufacturing.

**Plan action:** Keep human-dexterity claims out of the limb-panel proof. If comparing density, state active area, sensor-element size and pitch separately, with installed mass and connectivity included.

**Novelty implication:** Thousands of tactile channels with flexible routing were already demonstrated in human sensing equipment.

**Bibliographic/access note:** DOI 10.1007/978-3-642-31401-8_40. Different publication from[32].

### [34] Tactile object class and internal state recognition for mobile manipulation

S. Chitta, M. Piccoli and J. Sturm, ICRA 2010, 2342–2348. [Primary source or identity record](https://jsturm.de/publications/data/chitta10icra.pdf)

**Evidence:** primary_indexed_excerpt

**Read scope:** Indexed author-hosted original conference PDF methods/results excerpts, especially tablesII–IV. Direct PDF retrieval timed out; later journal version was kept distinct.

**Finding:** At 20 N probing, reported container-class accuracy is 93.9%, while internal-state accuracy varies substantially by container (water bottles 32.5%). Stronger probing improves one container result, illustrating task and stimulus dependence.

**Limit:** An overall recognition number cannot be transferred across object types or contact forces; high probing forces can damage objects. These are controlled gripper observations, not generic limb-skin intelligence.

**Plan action:** For any classifier, report per-class confusion matrices and separate test objects/sessions from training. Keep active exploratory-force tests outside the baseline ordinal-contact product unless actuator force is independently measured.

**Novelty implication:** Tactile object/state classification is prior art; any claimed advantage needs a matched task benchmark.

**Bibliographic/access note:** DOI 10.1109/ROBOT.2010.5509923. Do not substitute chitta 10 tro.pdf journal expansion for this conference paper.

### [36] A simple tactile sensing foot for humanoid robot and active ground slope recognition

K. Suwanratchatamanee, M. Matsumoto and S. Hashimoto, IEEE International Conference on Mechatronics, 2009, 1–6. [Primary source or identity record](https://doi.org/10.1109/ICMECH.2009.4957223)

**Evidence:** primary_abstract

**Read scope:** Publisher abstract and introduction excerpt, not the complete sensor/control evaluation.

**Finding:** The work uses a small set of thin force-sensitive resistors and active foot interaction to classify ground slope rather than requiring a dense whole-foot image.

**Limit:** A foot-slope demonstration does not validate arm/leg pressure sensing or balance stability. Its load paths and contact geometry differ from shell-mounted skin.

**Plan action:** Keep feet as a separate subsystem. Establish whether a future task needs contact presence, center of pressure, slope or detailed pressure distribution before selecting sensor count.

**Novelty implication:** Task-specific sparse sensing and active haptic inference are established.

**Bibliographic/access note:** DOI 10.1109/ICMECH.2009.4957223.

### [37] Design and experiment of the NAO humanoid robot’s plantar tactile sensor for surface classification

Q. Yuan and J. Wang, ICISCE 2017, 931–935. [Primary source or identity record](https://www.researchgate.net/publication/321122717_Design_and_Experiment_of_the_NAO_Humanoid_Robot%27s_Plantar_Tactile_Sensor_for_Surface_Classification)

**Evidence:** primary_full_text_selected

**Read scope:** Author-uploaded original: abstract, sections III–Vthrough classifier setup, diagrams/captions. Final result table and conclusion not exhaustively read.

**Finding:** A 10×16 resistive array uses 400 samples/s acquisition, but the authors explicitly state 0.4 s per full image; a 20-site subset supports faster tracking. Classification aggregates multiple walking steps.

**Limit:** The text’s 360 total datasets versus 224 training+36 test is arithmetically inconsistent. The headline accuracy is not immediate response or demonstrated cross-robot generalization. Matrix bypass-current rejection is not established by the viewed block diagram.

**Plan action:** Publish ADC rate, per-taxel rate, full-frame rate, scan skew and reaction latency separately. Never borrow 400 Hz as a full-array benchmark. Retain independent sensing islands unless simultaneous-contact electrical crosstalk is experimentally bounded.

**Novelty implication:** Low-cost resistive skin plus simple classification is prior art.

**Bibliographic/access note:** DOI 10.1109/ICISCE.2017.197. Uploader is coauthor Jianxiao Wang; no outreach performed.

### [38] An adaptive sensor foot for a bipedal and quadrupedal robot

K. Fondahl et al., BioRob 2012; Cheng lists 270–275. [Primary source or identity record](https://www.dfki.de/web/forschung/projekte-publikationen/publikation/6214)

**Evidence:** primary_abstract

**Read scope:** DFKI institutional publication abstract and metadata. Original paper not read.

**Finding:** The work concerns an adaptive foot mechanism and its sensor integration for different legged platforms, rather than simply applying a sensing film to an unchanged foot.

**Limit:** The abstract is insufficient to reproduce mechanics, control or load qualification. The institutional page’s pagination conflicts with Cheng’s bibliography.

**Plan action:** Do not roll feet into the limb-panel BOM. A foot version needs its own contact mechanics, abrasion, overload, water/soil and gait-interface requirements.

**Novelty implication:** Adaptive sensorized feet are an established separate product/problem class.

**Bibliographic/access note:** DFKI displays 2780–2786 whereas Cheng and other citations show 270–275. Flag the discrepancy; do not silently choose unverified metadata.

### [39] A ZMP sensor for a biped robot

M. Shimojo, T. Araki, A. Ming and M. Ishikawa, ICRA 2006, 1200–1205. [Primary source or identity record](https://researchmap.jp/read0072509/published_papers/15818833/attachment_file.pdf)

**Evidence:** primary_indexed_excerpt

**Read scope:** Indexed author-hosted first-page abstract. Direct PDF retrieval 403; complete derivation and experiments not read.

**Finding:** The abstract reports four wires, response within 1 ms, 0.2 g/cm²areal mass, and simultaneous total load and center-of-load position.

**Limit:** These are compressed aggregate outputs, not independent contact locations.0.2 g/cm²equals 2 kg/m²; “lightweight” must be compared using consistent units. No claim about general dynamic ZMP equivalence is adopted.

**Plan action:** Test observability before replacing arrays: two equal separated contacts and one central contact can share a centroid. Our multi-contact requirement needs independent sites or another demonstrated reconstruction method.

**Novelty implication:** Extreme wire reduction with analog spatial aggregation is prior art; it trades away information.

**Bibliographic/access note:** DOI 10.1109/ROBOT.2006.1641872.

### [40] High-speed pressure sensor grid for humanoid robot foot

Y. Takahashi, K. Nishiwaki, S. Kagami, H. Mizoguchi and H. Inoue, IROS 2005, 3909–3914. [Primary source or identity record](https://tus.elsevierpure.com/en/publications/high-speed-pressure-sensor-grid-for-humanoid-robot-foot/)

**Evidence:** primary_abstract

**Read scope:** Author-institution abstract and bibliographic record. Original six-page paper not accessed.

**Finding:** The abstract reports a 32×32 matrix, 1 kHz sampling, 14-bit conversion and 0.6 mm force-sensitive rubber. It explicitly identifies bypass-current interference and a mitigation method.

**Limit:** The abstract cannot supply the exact mitigation circuit or demonstrate our laminate’s independence, accuracy or fatigue. ADC resolution is not mechanical force accuracy.

**Plan action:** Our 100 Hzbody panels should not be marketed as equivalent to high-speed sole sensing. Any cheaper shared resistive matrix must pass a multi-contact test including unselected-row leakage, not merely isolated single presses.

**Novelty implication:** Dense, thin resistive tactile arrays and scanning-crosstalk remedies are well-established research.

**Bibliographic/access note:** DOI 10.1109/IROS.2005.1545126.
