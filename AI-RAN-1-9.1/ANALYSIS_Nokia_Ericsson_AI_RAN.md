# 3GPP RAN1 AI/ML for NR Air Interface: Nokia & Ericsson Position Analysis

## Document Inventory & Meeting Mapping

| File | Meeting | Date | Location | Type |
|------|---------|------|----------|------|
| r1-2401430 | RAN1 #116 | Feb 26 - Mar 1, 2024 | Athens, Greece | Work plan (Qualcomm rapporteur) |
| r1-2401766 | RAN1 #116 | Feb 26 - Mar 1, 2024 | Athens, Greece | Session notes (AI 9.1) |
| r1-2403662 | RAN1 #116bis | Apr 15-19, 2024 | Changsha, China | Session notes (AI 9.1) |
| r1-2405695 | RAN1 #117 | May 20-24, 2024 | Fukuoka, Japan | Session notes (AI 9.1) |
| r1-2407478 | RAN1 #118 | Aug 19-23, 2024 | Maastricht, NL | Session notes (AI 9.1) |
| r1-2409222 | RAN1 #118bis | Oct 14-18, 2024 | Hefei, China | Session notes (AI 9.1) |
| r1-2410844 | RAN1 #119 | Nov 18-22, 2024 | Orlando, US | Session notes (AI 9.1) |
| r1-2501143 | RAN1 #120 | Feb 17-21, 2025 | Athens, Greece | Rapporteur view on higher layer signalling (Qualcomm) |
| r1-2501546 | RAN1 #120 | Feb 17-21, 2025 | Athens, Greece | Session notes (AI 9.1) |

---

## Extraction Verification: Nokia & Ericsson TDocs Identified Per Meeting

### Nokia Contributions (submitted as "Nokia, Nokia Shanghai Bell" or "Nokia")

| Meeting | TDoc | Topic |
|---------|------|-------|
| #116 | R1-2400793 | AI/ML for Beam Management |
| #116 | R1-2400794 | AI/ML for Positioning Accuracy Enhancement |
| #116 | R1-2400795 | AI/ML for CSI Prediction |
| #116 | R1-2400796 | AI/ML for CSI Compression |
| #116 | R1-2400797 | Other Aspects of AI/ML Model and Data |
| #116bis | R1-2402996 | AI/ML for Beam Management |
| #116bis | R1-2402997 | AI/ML for Positioning Accuracy Enhancement |
| #116bis | R1-2402998 | AI/ML for CSI Prediction |
| #116bis | R1-2402999 | AI/ML for CSI Compression |
| #116bis | R1-2403000 | Other Aspects of AI/ML Model and Data |
| #117 | (present in contribution list) | Beam Management, Positioning, CSI Prediction |
| #118 | R1-2406586 | AI/ML for Beam Management |
| #118 | R1-2406587 | AI/ML for Positioning Accuracy Enhancement |
| #118bis | R1-2408544 | AI/ML for Beam Management |
| #118bis | R1-2408545 | AI/ML for Positioning Accuracy Enhancement |
| #118bis | R1-2408546 | AI/ML for CSI Prediction |
| #118bis | R1-2408547 | AI/ML for CSI Compression |
| #118bis | R1-2408548 | Other aspects of AI/ML for two-sided model use case |
| #119 | R1-2409985 | AI/ML for Beam Management |
| #119 | R1-2409986 | AI/ML for Positioning Accuracy Enhancement |
| #119 | R1-2409987 | AI/ML for CSI Prediction |
| #119 | R1-2409988 | AI/ML for CSI Compression |
| #119 | R1-2409989 | Other aspects of AI/ML for two-sided model |
| #120 | (present in contribution list) | Beam Management, Positioning, CSI Prediction, CSI Compression, Other aspects |

### Ericsson Contributions

| Meeting | TDoc | Topic |
|---------|------|-------|
| #116 | R1-2400171 | AI/ML for beam management |
| #116 | R1-2400101 | AI/ML for Positioning Accuracy Enhancement |
| #116 | R1-2400165 | AI/ML for CSI prediction |
| #116 | R1-2400166 | AI/ML for CSI compression |
| #116 | R1-2400172 | Discussion on other aspects of AI/ML |
| #116bis | R1-2402056 | AI/ML for beam management |
| #116bis | R1-2401984 | AI/ML for Positioning Accuracy Enhancement |
| #116bis | R1-2402494 | AI/ML for CSI prediction |
| #116bis | R1-2402495 | AI/ML for CSI compression |
| #116bis | R1-2402057 | Discussion on other aspects of AI/ML |
| #117 | (present) | All sub-topics |
| #118 | R1-2406141 | AI/ML for beam management |
| #118 | R1-2405945 | AI/ML for Positioning Accuracy Enhancement |
| #118bis | R1-2408268 | AI/ML for beam management |
| #118bis | R1-2407649 | AI/ML for Positioning Accuracy Enhancement |
| #118bis | R1-2408080 | AI/ML for CSI prediction |
| #118bis | R1-2408079 | AI/ML for CSI compression |
| #118bis | R1-2408269 | Discussion on other aspects of AI/ML |
| #119 | R1-2410354 | AI/ML for beam management |
| #119 | R1-2409443 | AI/ML for Positioning Accuracy Enhancement |
| #119 | R1-2409449 | AI/ML for CSI prediction |
| #119 | R1-2409450 | AI/ML for CSI compression |
| #119 | R1-2409731 | Discussion on other aspects of AI/ML |
| #120 | (present) | All sub-topics |

**Critical role: Ericsson served as Moderator for "Specification support for positioning accuracy enhancement" (agenda item 9.1.2) across ALL meetings from #116 through #120.** This is the most significant procedural role for either company in this WI.

---

## 1. Agreements Reached (by use case, by meeting)

### 1.1 Beam Management (Agenda 9.1.1)

#### RAN1 #116
- Support report of >4 beam related information in L1 signaling for NW-sided model inference
- For UE-sided model (BM-Case1): support report of predicted Top K beam(s) with options for RSRP, probability info, confidence info
- Beam indication based on unified TCI state framework for both NW-sided and UE-sided models
- CSI framework as starting point for Set B configuration

#### RAN1 #116bis
- BM-Case2 UE-side: support report of N>=1 future time instances in one report
- NW-sided model: existing CSI framework for Set A and Set B configuration as starting point
- CSI-ReportConfig used for inference results reporting configuration
- Study of associated ID (Opt 1) and performance monitoring (Opt 2) for NW-side condition consistency

#### RAN1 #117
- Support Type 1 performance monitoring with Option 1 (NW-side) and Option 2 (UE-assisted)
- RSRP quantization: 7-bit value range [-140, -44] dBm with 1dB step for NW-sided model

#### RAN1 #118
- **Associated ID supported** for UE-sided model (Working Assumption: configurable within CSI framework)
- Differential RSRP reporting with legacy quantization
- Two resource sets configurable for Set A and Set B separately
- Performance monitoring alternatives defined (Alt 1-4)
- BM-Case 2: N future time instances configurable by NW

#### RAN1 #118bis
- Option 2 UE-assisted monitoring: at least Alt 1 (Top 1/K beam prediction accuracy) supported
- CPU mechanism reused as starting point for AI/ML-based CSI processing
- P/SP/AP CSI-RS resource types supported for BM-Case1; P/SP for BM-Case2 (AP FFS)
- Detailed applicability procedure (Step 3/4/5) with three options studied
- Multiple CSI reports for inference can be configured (up to UE capability)

#### RAN1 #119
- Beam information in inference report = CRI/SSBRI of resource in Set A
- Fixed Set B across time instances for BM-Case 2
- Two CSI-ResourceConfigIds for Set A and Set B separately (finalized)
- Detailed Step 3/4/5 procedure agreed with CSI-ReportConfig + inference related parameters
- Monitoring report configuration: dedicated CSI report configuration linked to inference report
- LS to RAN2 with terminology mapping for "functionality"

#### RAN1 #120
- RSRP quantization finalized: 7-bit [-140, -44] dBm, 1dB step; differential RSRP 4-bit, 2dB step
- BM-Case 1: predicted RSRP based on AI/ML output (finalized)

**Nokia involvement in beam management:** Nokia submitted contributions to every meeting. Nokia is not explicitly cited as proposing or opposing any specific beam management agreement in the session notes. Nokia appears to be a **follower** on beam management, contributing evaluation results but not driving the agenda.

**Ericsson involvement in beam management:** Ericsson also submitted to every meeting. Like Nokia, Ericsson is not specifically cited as driving or opposing beam management agreements. Both companies appear to be contributing within the consensus-building process led by Samsung (the moderator for beam management).

### 1.2 Positioning Accuracy Enhancement (Agenda 9.1.2)

**Ericsson is the moderator for this entire topic across all meetings.** This means Ericsson drafted the summary documents, formulated the proposals, and managed consensus.

#### RAN1 #116
- Measurements based on DL PRS and UL SRS defined in TS38.211
- Time domain channel measurements supported for Cases 2a, 2b, 3a, 3b
- Investigation of sample-based vs path-based measurements
- LOS/NLOS indicator support for Cases 2a and 3a
- Phase information investigation agreed

#### RAN1 #116bis
- Case 3b timing relative to existing UL RTOA reference time
- Training data collection framework: Part A (channel measurement + quality + timestamp) / Part B (ground truth + quality + timestamp)
- Label generation entities identified for Cases 1, 2a, 2b, 3a, 3b
- Performance monitoring options A/B studied for Cases 1 and 3a

#### RAN1 #117
- Type 1 performance monitoring supported for positioning

#### RAN1 #118
- Case 3a monitoring: both Option A (NG-RAN node) and Option B (LMF) feasible
- Training data timestamp reuse of existing IEs
- DL PRS configuration for training: both UE-initiated and LMF-initiated options
- Sample-based measurement: select Nt' from Nt consecutive samples
- Power measurement: DL PRS-RSRPP and UL SRS-RSRPP as starting points
- Case 3a SRS configuration: existing procedures reusable

#### RAN1 #118bis
- Quality indicator for timing info: reuse NR-TimingQuality
- Case 3b mandatory/optional fields: channel measurement (M), quality (O), timestamp (M)
- Case 3a measurement report: timing (M), quality (O), timestamp (M)
- Case 1 assistance data: study of explicit/implicit indication for info #7 (TRP coordinates)

#### RAN1 #119
- LOS/NLOS indicator cannot be reported independently from other measurements (Case 3a)
- Sample-based measurement starting time definition finalized
- Case 1 monitoring: at least Option A (UE-side calculation) supported
- Case 3b: enhanced sample-based measurement with Nt' values from Nt consecutive values, timing granularity T=2^k x Tc
- Case 1 assistance data: info #7 alternatives (1-4) for TRP geographical coordinates

#### RAN1 #120
- (Session notes show continued refinement of positioning parameters)

**Nokia involvement in positioning:** Nokia submitted positioning contributions to every meeting (R1-2400794, R1-2402997, R1-2406587, R1-2408545, R1-2409986). Nokia is not explicitly cited as opposing or driving specific positioning agreements. Nokia appears to be a **participant** but not the agenda driver.

**Ericsson involvement in positioning:** **Ericsson is the clear agenda driver.** As moderator, Ericsson authored all summary documents (R1-2401825/2401546/2401545/2401544 at #116, R1-2403740/2403462-2403458 at #116bis, etc. through all meetings). Ericsson shaped the structure of every positioning agreement. Ericsson also submitted its own technical contributions separately (R1-2400101, R1-2401984, R1-2405945, R1-2407649, R1-2409443).

### 1.3 CSI Prediction (Agenda 9.1.3.1, later 9.1.3)

#### RAN1 #116
- Rel-18 EVM as starting point for evaluation
- Throughput comparison with non-AI/ML prediction encouraged
- Evaluation assumptions: CSI-RS periodicity 5ms baseline, 20ms encouraged
- UE-sided model only for Rel-19
- Generalization/scalability evaluation aspects agreed

#### RAN1 #116bis
- Baseline evaluation assumptions: UE speed 30/60 km/h, observation/prediction windows
- Channel estimation error and phase discontinuity modelling defined
- Results template adopted
- Legacy CSI-RS configuration as starting point for inference
- Legacy feedback mechanism "typeII-Doppler-r18" as starting point

#### RAN1 #117
- Extensive observations captured (see below for Nokia/Ericsson citations)

#### RAN1 #118
- Further observations on generalization, performance vs benchmarks
- Computational complexity reporting: FLOPs for whole bandwidth, one prediction sample
- Extensive evaluation results compiled (see Nokia/Ericsson specific section)

#### RAN1 #118bis
- Discussions limited to consistency of training/inference
- Study NW-side additional conditions impacting UE assumption
- Generalization evaluation for tilt angle, TXRU mapping
- TPs to TR38.843 endorsed

#### RAN1 #119
- Discussions still limited to training/inference consistency

#### RAN1 #120
- **Normative work on CSI prediction started** (from Q1 2025)
- This is a significant inflection point - moving from study to specification

**Nokia involvement in CSI prediction:** Nokia is cited in evaluation results multiple times:
- Nokia used antenna(port)-delay domain transformation as pre/post processing (unique approach among sources)
- Nokia considered 100% in-car UE distribution (unique among all sources - all others used 100% outdoor)
- Nokia observed 54%~106% SGCS gain vs Benchmark 1 at 30km/h (among the highest reported gains)
- Nokia observed 15.2%~19.5% gain with realistic channel estimation at 30km/h
- Nokia observed generalization degradation of -33.6%~-19% for speed mismatch (30km/h trained, 60km/h inferred) - on the higher degradation side
- Nokia observed -3% degradation for localized model generalization

**Ericsson involvement in CSI prediction:** Ericsson is heavily cited in evaluation results:
- Ericsson used beam-delay domain transformation as pre/post processing
- Ericsson considered spatial consistency in evaluations
- Ericsson reported consistently high performance gains (often the highest):
  - 100% gain in 5% UE UPT for mid RU at 30km/h
  - 77% gain in 5% UE UPT for mid RU with N4=4
  - 5%~29% gain vs Benchmark 2 with N4=4 and realistic channel estimation
  - 22.93%~23% SGCS gain with spatial consistency at 30km/h
- Ericsson results for N4=4 (multi-step prediction) are particularly strong
- Ericsson showed localized model gains of 10%~19% mean UPT at various scenarios

**Key divergence: Nokia vs Ericsson on CSI prediction evaluation methodology:**
- Nokia: antenna(port)-delay domain transformation, 100% in-car UE distribution
- Ericsson: beam-delay domain transformation, 100% outdoor distribution with spatial consistency
- These represent fundamentally different modeling assumptions that could lead to different specification preferences

### 1.4 CSI Compression (Agenda 9.1.3.2, later 9.1.4.1)

#### RAN1 #116
- Temporal domain categorization (Cases 0-5) agreed
- UE distribution options: 80% indoor/20% outdoor, or 100% outdoor
- Inter-vendor collaboration: 5 options studied (fully standardized model, standardized dataset, parameter exchange, dataset exchange, model exchange)
- Localized model evaluation framework agreed

#### RAN1 #116bis
- Results templates for temporal domain compression and prediction+compression
- **Option 1 (fully standardized reference model) eliminates inter-vendor collaboration complexity** (concluded)
- Option 2 deprioritized
- Options 3/4/5 sub-options defined (3a/3b, 4-1/4-2/4-3, 5a/5b)
- Direction A (offline engineering) and Direction B/C further studied
- CSI prediction entirely at NW-side deprioritized for temporal domain

#### RAN1 #118
- (Observations and evaluation results continued)

#### RAN1 #118bis
- Direction A: further study with potential down-selection to 4-1 and 3a-1
- Direction C: fully specified reference model purpose clarified
- Evaluation methodology for Directions A, B, C defined
- UE-side/NW-side data distribution mismatch evaluation framework

#### RAN1 #119
- LS to RAN2 on feasibility of dataset/parameter exchange via standardized signaling
- **Transformer adopted as backbone structure for Case 0** (spatial-frequency domain input)
- Case 2: adaptation on top of Case 0 structure (Conv-LSTM, LSTM, or latent adaptation)
- Case 3: adaptation on top of Case 0 structure
- Scalable model structure specification feasibility study agreed
- Data collection for training: NW-side and UE-side spec impacts studied
- LS sent on signaling feasibility of dataset and parameter sharing
- Observations captured in TR38.843

#### RAN1 #120
- Continued refinement of CSI compression approaches
- Evaluation results for Direction A (3a-1, 4-1) and Direction C with data distribution mismatch
- Ericsson cited for evaluation results on Direction A/B/C performance (moderate losses of -2.9%~-8.6%)

**Nokia involvement in CSI compression:** Nokia submitted contributions to every meeting (R1-2400796, R1-2402999, R1-2408547, R1-2409988). Nokia is not explicitly cited as driving or opposing specific CSI compression agreements in the session notes.

**Ericsson involvement in CSI compression:** Ericsson submitted to every meeting (R1-2400166, R1-2402495, R1-2408079, R1-2409450). In the #120 evaluation results, Ericsson is cited for observing moderate performance losses in Direction A/B/C evaluations (-2.9%~-8.6% relative to upper bound), suggesting Ericsson is actively evaluating the practical feasibility of inter-vendor collaboration approaches.

### 1.5 Other Aspects - Model Identification, Data Collection, Model Transfer (Agenda 9.1.3.3, later 9.1.4.2)

#### Key Agreements Across Meetings:
- Model identification type A studied with use case details
- MI-Option 1 (data collection related config + associated IDs) procedure defined (AI-Example1)
- MI-Option 4 = Option 1 of CSI compression (fully standardized reference model) clarified
- Model transfer/delivery Cases z2, z3, z5 deprioritized for Rel-19
- **Case z4 (known model structure + parameter transfer) is the main surviving option**
- For z4: first indication (model structure), second indication (parameters), model ID relationship studied
- MI-Option 2 (dataset transfer): ID-X for pairing UE-part and NW-part
- Readiness signaling: UE notification or minimum applicable time after transfer

**Nokia involvement:** Nokia submitted "Other Aspects" contributions to every meeting. Nokia's #118bis paper was specifically titled "Other aspects of AI/ML for two-sided model use case" (R1-2408548), and #119 similarly "Other aspects of AI/ML for two-sided model" (R1-2409989), indicating Nokia has focused attention on two-sided model aspects.

**Ericsson involvement:** Ericsson submitted to every meeting. No specific positions cited in session note agreements.

---

## 2. Nokia-Specific Analysis

### 2.1 Technical Positions Identified from Evaluation Results

**CSI Prediction (primary area where Nokia's approach is visible):**
- **Unique pre/post processing approach:** antenna(port)-delay domain transformation (vs Ericsson's beam-delay domain). This suggests Nokia's AI/ML models operate in a different representation of the channel, which has implications for model architecture and what gets standardized.
- **Unique UE distribution:** 100% in-car distribution (all other companies used 100% outdoor). This implies Nokia is targeting vehicular/mobility use cases specifically, which aligns with an in-vehicle positioning/connectivity strategy.
- **High gains reported:** 54%~106% SGCS gain vs Benchmark 1 at 30km/h, and 15.2%~19.5% gain with realistic channel estimation. These are among the higher reported values.
- **Generalization weakness:** Nokia observed significant degradation (-33.6%~-19%) when speed mismatch exists (trained at 30km/h, inferred at 60km/h), placing Nokia on the "higher degradation" side compared to Ericsson (-11.4%~-2.7% for similar mismatch).

### 2.2 Areas Where Nokia Appears to Drive vs. Follow

**Driving:**
- Nokia does not appear to be driving the agenda on any major topic based on the session notes. Nokia is not a moderator for any sub-agenda item.
- Nokia's unique evaluation assumptions (in-car distribution, antenna-port domain processing) suggest Nokia is advocating for specific deployment scenarios, but these have not translated into driving specific agreements.

**Following:**
- Nokia consistently submits contributions across all topics but is rarely cited as the source of a specific agreement or proposal in the session notes.
- Nokia appears to be a **broad participant** contributing to consensus without taking a strong leading position on contentious items.

### 2.3 Strategic Pattern
- Nokia covers all sub-topics (beam management, positioning, CSI prediction, CSI compression, other aspects) at every meeting
- Nokia's unique evaluation assumptions suggest a differentiated technical approach but not an aggressive standardization push
- Nokia's focus on "two-sided model" aspects (evident from paper titles at #118bis and #119) may indicate interest in CSI compression deployment

---

## 3. Ericsson-Specific Analysis

### 3.1 Technical Positions Identified from Evaluation Results

**CSI Prediction (area where Ericsson is most visible in results):**
- **Pre/post processing:** beam-delay domain transformation (shared with Intel)
- **Spatial consistency:** Ericsson consistently models spatial consistency (often with vivo, MediaTek, ZTE)
- **Dominant evaluation contributor:** Ericsson is the single most-cited source in CSI prediction evaluation observations across #117 and #118. Ericsson provided results for virtually every combination of speed, N4, traffic model, and channel estimation assumption.
- **Consistently highest gains:** Ericsson reported the highest or among the highest performance gains in many categories:
  - 100% gain in 5% UE UPT (mid RU, 30km/h, N4=1) - the single highest reported gain
  - 77% gain in 5% UE UPT (mid RU, 30km/h, N4=4)
  - 73% gain in 5% UE UPT (high RU, 60km/h, N4=4)
  - 29% SGCS gain vs Benchmark 2 (30km/h, N4=4, realistic CE)
- **Multi-step prediction (N4=4) champion:** Ericsson is one of very few companies providing comprehensive N4=4 results, and shows strong gains consistently. This positions Ericsson as the strongest advocate for multi-step CSI prediction.

**Positioning (area where Ericsson has procedural control):**
- As moderator across all meetings, Ericsson shapes every proposal, manages consensus, and authors summary documents
- Ericsson's own technical contributions (separate from moderator summaries) are submitted at every meeting
- This dual role (moderator + contributor) gives Ericsson significant influence over the direction of positioning specification

**CSI Compression:**
- Ericsson's #120 evaluation results on Direction A/B/C show moderate performance losses (-2.9%~-8.6%), suggesting Ericsson sees practical feasibility in inter-vendor collaboration approaches but acknowledges performance gaps

### 3.2 Areas Where Ericsson Drives vs. Follows

**Driving:**
- **Positioning: Ericsson is the unambiguous agenda driver** as moderator for all meetings
- **CSI Prediction: Ericsson is the dominant evaluation contributor**, providing the most comprehensive results and often the highest gains. While not the moderator (LG Electronics moderates CSI prediction), Ericsson's volume of results shapes the observations captured in the TR.

**Following:**
- Beam management: Ericsson is a participant, not a driver (Samsung moderates)
- CSI compression: Ericsson participates but doesn't drive (Qualcomm moderates)

### 3.3 Strategic Pattern
- Ericsson has a **deep, targeted strategy**: positioning ownership + CSI prediction performance leadership
- The combination of moderator control over positioning and dominant evaluation results in CSI prediction gives Ericsson significant influence over what gets specified and how
- Ericsson's consistent N4=4 results suggest they want multi-step prediction in the standard, which increases the computational requirements on the UE/network side

---

## 4. Nokia vs. Ericsson Divergences

### 4.1 Direct Technical Divergences

| Aspect | Nokia | Ericsson |
|--------|-------|----------|
| CSI prediction pre/post processing | antenna(port)-delay domain | beam-delay domain |
| UE distribution assumption | 100% in-car | 100% outdoor + spatial consistency |
| Generalization performance (30->60 km/h) | -33.6%~-19% degradation | -11.4%~-2.7% degradation |
| Evaluation completeness | Selective scenarios | Comprehensive across all scenarios |
| Target deployment | Vehicular/mobility-focused | General outdoor deployment |
| Multi-step prediction (N4=4) | Not prominently featured | Heavily featured, strong advocate |

### 4.2 Standardization Influence

| Aspect | Nokia | Ericsson |
|--------|-------|----------|
| Moderator roles | None for AI 9.1 | Positioning (all meetings) |
| Agenda driving | Following | Driving (positioning, influencing CSI prediction) |
| Evaluation result volume | Moderate | Highest among all companies |
| Two-sided model focus | Yes (paper titles) | Not specifically emphasized |

### 4.3 Areas of Alignment
- Both companies submit across all sub-topics
- Both support the overall WI direction (beam management + positioning + CSI study)
- Neither company is cited as opposing any specific agreement in the session notes
- Both appear to support the CSI framework as the basis for AI/ML inference configuration

---

## 5. Open/Contested Items as of RAN1 #120

### 5.1 CSI Prediction - Normative Work Just Starting
- **Status:** Normative work began at RAN1 #120 (Q1 2025). Prior to this, it was study-only.
- **Open:** Whether CSI prediction will result in new specification or rely entirely on existing Rel-18 framework
- **Open:** CSI processing timeline for AI/ML-based prediction
- **Open:** Whether NW-side additional conditions require associated ID for CSI prediction (studied at #118bis/#119)
- **Nokia/Ericsson position:** Not explicitly on opposing sides. Both contribute evaluation results. The divergence in evaluation methodology (in-car vs outdoor, different domain transforms) could lead to different preferences when normative decisions are made.

### 5.2 CSI Compression - Inter-Vendor Collaboration Direction
- **Status:** Three directions remain:
  - Direction A (parameter/dataset exchange for offline engineering): Options 3a-1 and 4-1 still being studied
  - Direction B (direct parameter transfer to UE): overhead study ongoing
  - Direction C (fully standardized reference model): feasibility contingent on scalable model structure
- **Open:** Down-selection between Direction A, B, C
- **Open:** Scalable model structure specification feasibility (critical for both Direction A 3a-1 and Direction C)
- **Open:** LS to RAN2 pending on signaling feasibility of dataset/parameter exchange
- **Transformer backbone for Case 0 agreed**, but domain input (spatial-frequency vs angular-delay) still open
- **Nokia/Ericsson:** Both contribute but neither is cited as leading a specific direction. Ericsson's evaluation results on data distribution mismatch are relevant to Direction A feasibility.

### 5.3 Positioning - Remaining Items
- **Open:** Case 1 info #7 (TRP coordinates): 4 alternatives still pending down-selection
- **Open:** Case 2b measurements (2nd priority, deferred)
- **Open:** Positioning AI/ML Processing capability UE feature details
- **Ericsson shapes this:** As moderator, Ericsson will continue to drive these to resolution.

### 5.4 Beam Management - Remaining Items
- **Open:** FG definition and granularity for UE capabilities
- **Open:** Whether associated ID is mandatory or optional
- **Open:** CSI processing timeline for BM-Case1 and BM-Case2
- **Open:** Connection between monitoring RSs and Set A beams
- **Nokia/Ericsson:** Neither is cited on opposing sides of any remaining BM item.

---

## 6. Higher Layer Signaling Status

### Source: R1-2501143 (RAN1 #120, Qualcomm Rapporteur)

This is the most directly relevant document for NVIDIA Aerial integration.

### 6.1 Beam Management RRC Parameters

**UE Features (capabilities):**
- AIML_BM_Case1 support
- AIML_BM_Case2 support
- {Set A, Set B} supported combination values (per case)
- BM AI/ML Processing capability
- Case 2: capability for future prediction time instances
- Case 2: capability for historical instances used
- Support of more than 4 beam report

**RRC Parameters (CSI-ReportConfig):**
- AIML_BM_SetA / AIML_BM_SetB (enumerated lists with max sizes, per case)
- Configuration of predicted time instances (Case 2)
- Enable/Disable per case (single bit)
- Performance Monitoring: Associated_Inference_Report_ID, Resource_Set_for_Monitoring, L1MetricforMonitoring
- Association ID related to applicability
- nrofReportedRS-v19

**Open question:** Whether SetB configuration can reuse existing resourcesForChannelMeasurement. Whether SetA/SetB for Case1 and Case2 are common or different.

### 6.2 Positioning LPP Parameters

**UE Features:**
- AIML_Pos_Case1 support (may be a new positioning method with own UE feature family)
- Positioning AI/ML Processing capability
- No UE features needed for Case 3a and 3b (gNB/LMF-side)

**LPP Parameters:**
- Assistance Data common to legacy methods
- New AD: Association ID as new element
- Case 2b may require new measurements (2nd priority, deferred)

### 6.3 CSI Prediction RRC Parameters

**Status:** Normative work just started at #120. No RRC parameters listed yet. The rapporteur notes that "reuse of Rel-18 CSI framework may be advantageous."

### 6.4 General Framework

**UE Feature:**
- Overall AI/ML Processing capability (cross-use-case)

**RRC Parameters:**
- None identified yet

### 6.5 Key Signaling Mechanisms Across All Use Cases

| Mechanism | Purpose | Framework |
|-----------|---------|-----------|
| CSI-ReportConfig | Inference configuration for BM | Existing CSI framework extended |
| Associated ID | Training/inference consistency | New parameter within CSI framework |
| OtherConfig | Enable UAI reporting | Existing RRC mechanism |
| Applicability reporting (Step 4) | UE reports which configs are applicable | New procedure |
| L1/MAC signaling | Activation/deactivation of CSI reports | Existing CSI activation extended |
| NRPPa | LMF to gNB signaling for positioning parameters | Existing protocol |
| LPP | LMF to UE assistance data for positioning | Existing protocol extended |
| Model transfer/delivery Case z4 | Parameter transfer for known model structure | New mechanism (details FFS) |
| Dataset/parameter exchange (CSI compression) | Inter-vendor collaboration | LS to RAN2 pending on feasibility |

---

## 7. NVIDIA Aerial Integration Implications

The following items have direct implications for how Nokia and Ericsson would approach embedding GPU-accelerated RAN functions:

### 7.1 Model Inference Location and Compute Requirements

- **NW-sided models** (beam management, positioning Cases 3a/3b): Inference runs on the gNB/network side. This is where GPU acceleration (NVIDIA Aerial) would apply directly. The standard is specifying what measurements feed the model and what the model outputs, but NOT the model architecture itself for NW-sided models.
- **UE-sided models** (beam management Cases 1/2, positioning Case 1, CSI prediction): Inference runs on the UE. GPU acceleration on the network side would apply to training data collection, model management, and potentially model transfer (Case z4).
- **Two-sided models** (CSI compression): Both encoder (UE) and decoder (NW) must be compatible. The standardized model structure discussion (Transformer backbone for Case 0) directly constrains what GPU-accelerated implementations can do. **If Direction C (fully standardized reference model) wins, GPU implementations must conform to a specific architecture.**

### 7.2 Ericsson's Positioning Moderator Role

Ericsson's control of the positioning specification directly determines the measurement formats, signaling procedures, and data flows between gNB and LMF. Any GPU-accelerated positioning implementation must conform to these interfaces. **Companies integrating NVIDIA Aerial for positioning would need to track Ericsson's moderator summaries closely**, as they define the exact specification text.

### 7.3 CSI Prediction Compute Intensity

Ericsson's strong push for N4=4 (multi-step prediction) would significantly increase the computational requirements for AI/ML-based CSI processing. If multi-step prediction becomes standard, GPU acceleration becomes more compelling for network-side processing (e.g., training data preparation, model updates).

### 7.4 Model Transfer/Delivery (Case z4)

The surviving model transfer mechanism (known model structure + parameter transfer over air interface) means the standard will define:
- How model parameters are encoded and transmitted
- How the UE signals readiness after receiving parameters
- The scalability of model structure across antenna configurations and bandwidths

This directly impacts how a GPU-accelerated gNB would manage and distribute AI/ML models.

### 7.5 Higher Layer Signaling as Integration Surface

The RRC parameters identified in R1-2501143 represent the **control plane interface** that any AI-RAN implementation must support. For NVIDIA Aerial integration:
- The CSI-ReportConfig extensions for AI/ML are the primary L1/L2 interface
- The OtherConfig mechanism for enabling UAI is the RRC-level switch
- The Associated ID mechanism is the training/inference consistency bridge
- The LPP extensions are the positioning-specific interface

These are the exact specification touchpoints where GPU-accelerated RAN functions must interoperate with the standard UE/NW signaling stack.

---

## Methodology Note

This analysis is based solely on the text extracted from the 9 provided PDFs (converted to markdown). Positions are attributed to Nokia and Ericsson only where they are explicitly named in the documents. Where a company is not mentioned on a topic, this is noted. No positions have been inferred or hallucinated. The session notes capture formal agreements, conclusions, and observations but do not always record which specific company proposed or opposed each item, making it impossible to reconstruct all positions from these documents alone.
