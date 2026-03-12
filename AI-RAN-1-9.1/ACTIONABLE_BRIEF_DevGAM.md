# Actionable Intelligence Brief: NVIDIA DevGAM Role
## Mapping 3GPP AI/ML Standards Intelligence to Job Responsibilities

---

## How to Use This Document

Each section below maps **one JD responsibility** to:
- **What the brief tells you** (standards intelligence you already have)
- **What the SDK enables** (NVIDIA Aerial capabilities that connect)
- **Actionable talking points** (what you'd say/do in the role, demonstrating you already think like the PIC)

---

## 1. Strategic Technical Account Leadership ("Pilot in Command")

> *JD: Serve as the "Pilot in Command" for partners. Guide their R&D roadmaps to align with NVIDIA's AI-RAN/Aerial capabilities across Open RAN, C-RAN, D-RAN, and Cloud-RAN.*

### What the Brief Tells You

**Nokia and Ericsson need fundamentally different PIC strategies:**

| Dimension | Nokia Account Strategy | Ericsson Account Strategy |
|-----------|----------------------|--------------------------|
| Standards posture | Broad participant, no moderator roles, follows consensus | Positioning agenda driver, CSI prediction evaluation leader |
| Technical bet | Vehicular/in-car deployment (100% in-car UE distribution) | General outdoor + multi-step prediction (N4=4) |
| Two-sided models | Actively focused (paper titles indicate priority) | Not specifically emphasized |
| Generalization gap | -33.6% to -19% speed mismatch degradation | -11.4% to -2.7% -- significantly better |
| What they need from GPU | Flexibility across diverse scenarios | Raw compute density for multi-step inference |

**Nokia's R&D roadmap alignment:**
- Nokia's focus on two-sided models (CSI compression) means they care deeply about the Direction A/B/C down-selection. If Direction C wins (fully standardized Transformer), Nokia needs Aerial's cuPHY to run a *specific* model architecture. If Direction A wins, Nokia keeps proprietary models and needs Aerial to be a flexible inference engine.
- Nokia's vehicular focus (in-car UE distribution) maps to D-RAN/C-RAN edge deployments where the DU is close to the road. The ARC platform's workload consolidation (cuPHY + cuMAC + NIM on one GH200) is the value proposition: one box at the cell site handles RAN + AI for V2X.
- Nokia + T-Mobile field validation trials starting 2026 -- this is a live commercial engagement you'd be guiding.

**Ericsson's R&D roadmap alignment:**
- Ericsson's N4=4 multi-step CSI prediction generates 4x the compute demand vs N4=1. This is where cuPHY's GPU acceleration becomes essential -- CPU-based L1 can't handle the inference throughput.
- Ericsson controls the positioning specification as moderator. Their measurement formats (sample-based with Nt' from Nt consecutive samples, timing granularity T=2^k x Tc) define exactly what data flows into the GPU for NW-sided positioning inference. The PIC needs to ensure Aerial's L1 pipeline can ingest these measurement formats natively.
- Ericsson is an AI-RAN Alliance member -- commercial relationship already exists.

### SDK Connection

| Aerial Component | Nokia Relevance | Ericsson Relevance |
|-----------------|-----------------|-------------------|
| **cuPHY** (L1) | Must support standardized Transformer inference if Direction C wins | Must handle N4=4 multi-step CSI prediction inference load |
| **cuMAC** (L2) | MAC scheduling for vehicular scenarios (high-mobility, frequent handover) | MAC scheduling optimized for multi-step prediction feedback |
| **pyAerial** | Rapid prototyping of Nokia's antenna-port-delay domain models | Rapid prototyping of Ericsson's beam-delay domain models |
| **NIM** | AI-on-RAN services for Nokia's diverse deployment scenarios | Agentic RIC for continuous positioning parameter optimization |
| **ARC** (GH200) | Single-box DU + AI for edge/D-RAN (vehicular) | Compute-dense C-RAN/Cloud-RAN for multi-cell positioning |

### Interview Talking Points

- "I'd differentiate the PIC approach per partner. For Nokia, I'd focus the Aerial value proposition on deployment flexibility -- their 3GPP evaluation assumptions show they're targeting vehicular scenarios with diverse channel conditions. The ARC platform's workload consolidation is their story: one GH200 at the cell site running cuPHY + NIM for V2X AI. For Ericsson, I'd lead with compute density -- their N4=4 multi-step prediction results are the strongest in 3GPP, and that compute intensity is exactly where GPU acceleration becomes non-optional."

- "I'd track the CSI compression Direction A/B/C down-selection as the single highest-stakes standards decision for both accounts. If Direction C wins, we need to ensure cuPHY can run the standardized Transformer backbone efficiently. If Direction A wins, we preserve flexibility. Either way, I'd be briefing both partners quarterly on how Aerial's roadmap aligns with each direction."

---

## 2. Deep Technical Engagement

> *JD: Lead architecture reviews, feature mapping, and performance benchmarking. Work side-by-side with NEP engineers to optimize containerized network functions (DU/CU, UPF, RIC) on NVIDIA GPUs.*

### What the Brief Tells You

**The 3GPP RRC parameter surface is the exact integration specification:**

The RRC parameters from R1-2501143 define the control plane interface that every AI-RAN DU must support. Here's the feature mapping between 3GPP and Aerial:

| 3GPP Parameter/Mechanism | Aerial Component | Integration Surface |
|--------------------------|-----------------|-------------------|
| CSI-ReportConfig extensions (AIML_BM_SetA/SetB) | cuPHY L1 | CSI-RS pipeline must generate Set A/Set B measurements and route them to AI inference |
| Associated ID (training/inference consistency) | cuPHY-CP + L2 stack | Control plane must track model-to-measurement associations across training and inference |
| nrofReportedRS-v19 (>4 beam report) | cuPHY L1 | PUSCH pipeline must decode expanded beam reports from UE |
| L1MetricforMonitoring | cuPHY L1 | Must compute and report the selected performance metric |
| OtherConfig (UAI enable) | CU (RRC on Grace CPU) | RRC stack running on Grace must signal UAI enable/disable |
| LPP extensions (positioning) | CU + positioning NIM | LMF functions can run as NIM on the same ARC platform |
| Model Transfer Case z4 | CU (PDCP/RRC) | Parameter encoding and OTA transfer to UE |
| Applicability Report (Step 4) | L2 stack + cuPHY | UE capability exchange and AI/ML config validation |

**Architecture review framework for NEP engineers:**

For a DU architecture review with Nokia or Ericsson engineers, you'd walk through:

1. **L1 Pipeline Mapping**: How does cuPHY's CSI-RS pipeline map to the 3GPP AI/ML measurement framework?
   - cuPHY already processes CSI-RS. The Rel-19 extensions add Set A/Set B configuration, associated IDs, and monitoring reports.
   - Key question: Where in the cuPHY pipeline does AI inference insert? After channel estimation (for NW-sided beam management) or after CSI report decoding (for UE-sided model management)?

2. **Containerized NF Optimization**:
   - **DU**: cuPHY (GPU) + cuMAC (GPU) + L2+ (Grace CPU) -- all on one GH200
   - **CU**: RRC/PDCP/SDAP on Grace CPU -- handles OtherConfig, model transfer, applicability signaling
   - **UPF**: dUPF on Grace CPU with BlueField-3 acceleration -- edge deployment for low-latency AI-RAN
   - **RIC**: NIM-based agentic AI on the same GPU -- MX-RIC for parameter optimization

3. **Performance Benchmarking Targets**:
   - cuPHY L1 throughput with AI/ML inference overhead (how much GPU headroom remains after L1 processing for AI inference?)
   - Inference latency for BM-Case2 temporal prediction (must complete within CSI processing timeline -- still open in 3GPP)
   - Multi-cell positioning inference throughput (Cases 3a/3b run on gNB/LMF side)

### SDK Connection

**pyAerial is the benchmarking tool:**
- pyAerial provides bit-accurate Python bindings to the exact CUDA kernels used in cuBB production. NEP engineers can prototype AI/ML inference pipelines in Python, validate against cuBB, and benchmark GPU utilization before deploying to production cuPHY.
- Sionna provides the channel simulation for benchmarking AI/ML model performance under different channel conditions -- directly relevant to the evaluation scenarios in the 3GPP session notes (30km/h vs 60km/h, indoor vs outdoor, etc.).

**Aerial Framework (Apache 2.0, open-source):**
- NEP engineers can generate custom GPU-accelerated pipelines from Python, adding AI/ML inference stages to the standard L1 pipeline.
- This is the "developer" in "developer-to-deployment" -- NEPs build custom AI-RAN functions using the framework, validate with pyAerial, then deploy on ARC.

### Interview Talking Points

- "I'd structure architecture reviews around the 3GPP RRC parameter surface. The CSI-ReportConfig extensions for AI/ML beam management define the exact L1/L2 API that cuPHY needs to support. I'd walk NEP engineers through the cuPHY pipeline -- here's where CSI-RS measurements feed into AI inference, here's where the inference results flow back into the MAC scheduler via cuMAC, here's how the Associated ID tracks training-inference consistency through the control plane."

- "For performance benchmarking, I'd use pyAerial to prototype the AI/ML inference pipeline in Python, measure GPU utilization overhead, and then validate against the 3GPP processing timeline requirements. The key open question in 3GPP is the CSI processing timeline for BM-Case1 and BM-Case2 -- whatever they decide becomes our latency budget."

---

## 3. Ecosystem Orchestration

> *JD: Drive the "developer-to-deployment" lifecycle by crafting reference builds, integration guides, and runbooks that allow partners to scale NVIDIA-based solutions globally.*

### What the Brief Tells You

**The 3GPP standards create three distinct reference build scenarios:**

| Scenario | 3GPP Basis | Reference Build Contents |
|----------|-----------|------------------------|
| **NW-sided AI/ML** (Beam Mgmt, Positioning Cases 3a/3b) | Model architecture is implementation-specific; only interfaces standardized | Reference build: cuPHY L1 + custom AI inference pipeline + CSI-ReportConfig handling. Guide shows how to plug any PyTorch/TensorFlow model into the cuPHY pipeline via pyAerial |
| **UE-sided AI/ML** (BM Cases 1/2, Positioning Case 1, CSI Prediction) | UE runs inference; NW manages training data and model delivery | Reference build: CU-side model management + Case z4 parameter transfer + training data collection pipeline. Guide shows how to use NIM for training data preparation and model lifecycle management |
| **Two-sided AI/ML** (CSI Compression) | Encoder on UE, decoder on NW; Transformer backbone standardized (Case 0) | Reference build: cuPHY decoder implementation conforming to standardized Transformer architecture + inter-vendor collaboration support (Direction A/B/C). Highest complexity -- guide must address model compatibility |

**Runbook priorities based on standards maturity:**

1. **Beam Management** (most mature, Rel-19 normative work advanced): Ready for reference build NOW. CSI-ReportConfig extensions, Set A/Set B configuration, monitoring reports -- all agreed. Runbook can be built against agreed parameters.

2. **Positioning** (moderately mature, Ericsson-controlled): Reference build possible but must track Ericsson's moderator summaries for final spec text. Runbook should cover Cases 1, 2a, 3a, 3b with measurement format details.

3. **CSI Prediction** (normative work just started Q1 2025): Too early for production reference build. Provide a pyAerial-based prototype guide using Sionna channel simulation.

4. **CSI Compression** (Direction A/B/C still open): Cannot write a definitive reference build until direction is selected. Provide a "three-path" integration guide covering all three directions.

### SDK Connection

**Developer-to-Deployment Lifecycle:**

```
DEVELOPER PHASE                    DEPLOYMENT PHASE
+-------------------+              +-------------------+
| pyAerial          |              | cuBB (cuPHY +     |
| (Python + CUDA    |  validate    |  cuMAC)           |
|  kernels)         | ----------> | Production L1/L2  |
+-------------------+              +-------------------+
| Sionna            |              | ARC (GH200 +      |
| (Channel sim +    |  benchmark   |  BlueField-3)     |
|  ray tracing)     | ----------> | Hardware platform  |
+-------------------+              +-------------------+
| Aerial Framework  |              | Docker containers  |
| (Pipeline gen     |  package     | (cuBB + L2+ +     |
|  from Python)     | ----------> |  NIM + CU + UPF)  |
+-------------------+              +-------------------+
```

**Integration guide structure:**
1. Use pyAerial to prototype AI/ML inference in Python
2. Validate with Sionna channel simulation (matching 3GPP evaluation assumptions)
3. Use Aerial Framework to generate GPU-accelerated pipeline
4. Package as Docker container on ARC
5. Deploy with O-RAN 7.2 fronthaul to O-RU

### Interview Talking Points

- "I'd organize reference builds by 3GPP maturity. Beam management is ready for a production reference build today -- the RRC parameters are agreed and the CSI framework extensions are well-defined. For CSI compression, I'd provide a three-path integration guide because the Direction A/B/C down-selection hasn't happened yet, and each direction has radically different implications for the GPU implementation. I wouldn't let partners build against an assumption that might be wrong."

- "The developer-to-deployment lifecycle maps directly to the Aerial toolchain: pyAerial for prototyping with bit-accurate CUDA kernels, Sionna for channel simulation matching 3GPP evaluation assumptions, Aerial Framework for generating production pipelines, and ARC for deployment. Each reference build would walk NEP engineers through this exact path."

---

## 4. Influence Product Strategy

> *JD: Discover new RAN workflows and recognize adoption challenges. Convey these observations to NVIDIA product teams to direct the future of the Aerial SDK and NIMs.*

### What the Brief Tells You

**Five product strategy recommendations derived from the standards intelligence:**

### Recommendation 1: cuPHY Needs a Standardized Transformer Inference Path

**Observation:** 3GPP agreed on a Transformer backbone for CSI compression Case 0 at RAN1 #119. If Direction C (fully standardized reference model) wins the down-selection, every GPU implementation must run this exact model. cuPHY currently doesn't have a standardized model inference path -- it's optimized for traditional L1 signal processing.

**Product action:** Add a TensorRT-integrated inference stage to the cuPHY pipeline that can load and execute a standardized Transformer model. This should be a first-class citizen in cuBB, not a sidecar.

**Timing:** Direction C down-selection likely in next 2-3 RAN1 meetings (2025-2026). Must be ready before Rel-19 freeze.

### Recommendation 2: pyAerial Should Support 3GPP AI/ML Evaluation Assumptions

**Observation:** The 3GPP evaluation framework specifies exact channel conditions (30/60 km/h UE speed, CSI-RS periodicity 5/20ms, indoor/outdoor distributions, spatial consistency). NEP engineers need to benchmark their AI/ML models against these exact assumptions to validate 3GPP compliance.

**Product action:** Add pre-configured 3GPP Rel-19 evaluation profiles to pyAerial/Sionna that match the assumptions in TR 38.843. This becomes a competitive advantage -- "validate your AI-RAN model against 3GPP assumptions in one line of Python."

### Recommendation 3: NIM Needs a Positioning-Specific Microservice

**Observation:** AI/ML positioning (Cases 1, 2a, 3a, 3b) runs NW-side inference using DL PRS and UL SRS measurements with sample-based measurement format (Nt' from Nt consecutive samples, timing granularity T=2^k x Tc). This is a well-defined inference problem: measurements in, position estimate out.

**Product action:** Create a Positioning NIM that ingests 3GPP-formatted measurements (DL PRS-RSRPP, UL SRS-RSRPP, timing measurements with NR-TimingQuality) and outputs position estimates. Package the LMF function as a NIM running on the same ARC platform.

### Recommendation 4: Aerial SDK Needs Associated ID Lifecycle Management

**Observation:** The "Associated ID" mechanism is the training/inference consistency bridge across all AI/ML use cases. It links a specific training dataset/configuration to the inference configuration. This is a new concept that doesn't exist in current L1/L2 stacks.

**Product action:** Add Associated ID management to cuPHY-CP and the L2 stack. The PIC for each NEP partner will need to help them integrate this -- it's not a simple parameter, it's a lifecycle that spans training data collection, model training, inference configuration, and performance monitoring.

### Recommendation 5: Adoption Challenge -- NEPs Don't Know What's Standard vs. Implementation-Specific

**Observation:** The single biggest adoption challenge is that the 3GPP standard intentionally leaves model architecture as implementation-specific for NW-sided and UE-sided models, but standardizes the interfaces. NEP engineers often don't know where the "standard boundary" ends and the "Aerial advantage" begins.

**Product action:** Create a clear "what's standardized vs. what's yours" mapping document for each AI/ML use case. This becomes the foundation of every PIC engagement. The Aerial value proposition is clearest in the "implementation-specific" zone -- that's where GPU acceleration is a competitive differentiator, not a compliance requirement.

### Interview Talking Points

- "From tracking 237 decisions across 7 RAN1 sessions, I've identified five specific product strategy inputs for the Aerial SDK team. The most urgent is the Transformer inference path in cuPHY -- if 3GPP's CSI compression Direction C wins, every GPU L1 implementation must run a specific model architecture, and cuPHY needs to be ready. The most impactful NIM opportunity is positioning -- it's a clean inference problem with well-defined inputs and outputs, and Ericsson controls the spec as moderator."

- "The biggest adoption challenge I see is the standard-vs-implementation boundary confusion. NEP engineers don't always know where 3GPP's interface specification ends and Aerial's implementation freedom begins. I'd create a mapping document for each use case and make it the centerpiece of every architecture review."

---

## 5. Coordinated Approach

> *JD: Lead a multi-functional NVIDIA team -- including Solutions Architects, Engineering, Product Management, and Industry Business Development -- to ensure partnership turning points are met.*

### What the Brief Tells You

**Three partnership turning points to orchestrate:**

### Turning Point 1: CSI Compression Direction Down-Selection (Next 2-3 Meetings)

| NVIDIA Function | Role | Deliverable |
|----------------|------|-------------|
| **Solutions Architect** | Model three scenarios (Direction A/B/C) and assess GPU impact of each | Architecture decision document per partner |
| **Engineering** | Prototype Transformer inference in cuPHY for Direction C scenario | Working cuPHY build with TensorRT integration |
| **Product Management** | Track RAN1 sessions for down-selection signals | Standards watch brief after each meeting |
| **Industry BD** | Engage Nokia and Ericsson standards delegates to understand their positions | Partner preference intelligence |

### Turning Point 2: CSI Prediction Normative Specification (Started Feb 2025)

| NVIDIA Function | Role | Deliverable |
|----------------|------|-------------|
| **Solutions Architect** | Map Ericsson's N4=4 compute requirements to ARC sizing | ARC sizing guide for multi-step prediction |
| **Engineering** | Implement CSI prediction inference pipeline in cuPHY | pyAerial prototype + cuBB integration plan |
| **Product Management** | Decide whether CSI prediction is a NIM or a cuPHY-native function | Product positioning decision |
| **Industry BD** | Coordinate with Ericsson on positioning + CSI prediction combined deployment | Joint deployment roadmap |

### Turning Point 3: Rel-19 Feature Freeze and Commercial Deployment (2026)

| NVIDIA Function | Role | Deliverable |
|----------------|------|-------------|
| **Solutions Architect** | Final reference architecture per partner (Nokia C-RAN/D-RAN, Ericsson Cloud-RAN) | Reference architecture documents |
| **Engineering** | Production cuBB release with all Rel-19 AI/ML features | Release candidate |
| **Product Management** | GTM strategy for AI-RAN as differentiated platform | Launch plan |
| **Industry BD** | Commercial terms for SoftBank, T-Mobile, other CSP deployments | Commercial agreements |

### Interview Talking Points

- "I'd organize the cross-functional team around three partnership turning points, each with clear deliverables per function. The most urgent is the CSI compression direction down-selection -- it's the single decision that most constrains our product architecture. I'd have Engineering prototyping the Direction C scenario (Transformer in cuPHY) while Solutions Architects model all three scenarios for each partner."

- "For each turning point, I'd run a 'standards watch' cadence -- Product Management tracks the RAN1 sessions, I synthesize the implications for each partner, and we brief the full team quarterly. The 3GPP calendar is predictable, so we can plan the coordination in advance."

---

## 6. Industry Advocacy

> *JD: Represent joint technical positions in industry groups (e.g., AI-RAN Alliance, 3GPP) to unblock partner execution and promote AI-native telecommunications.*

### What the Brief Tells You

**Specific positions to advocate based on standards intelligence:**

### Position 1: In the AI-RAN Alliance -- "GPU Acceleration Is Where the Standard Points"

The 3GPP standard intentionally separates standardized interfaces from implementation-specific model architecture. For NW-sided models (beam management, positioning), the gNB has complete freedom in model selection, training, and inference. This is exactly where GPU acceleration has maximum impact -- behind a standards-compliant interface.

**Talking point for Alliance meetings:** "3GPP has created the interface standard. What runs behind that interface is the competitive battleground. Aerial provides the compute platform that makes sophisticated AI models practical in real-time L1 processing. The standard doesn't mandate GPUs, but the compute requirements -- especially for multi-step prediction and positioning -- make GPU acceleration the natural implementation choice."

### Position 2: In 3GPP Context -- "Processing Timeline Must Account for AI Inference"

The CSI processing timeline for AI/ML-based beam management and CSI prediction is still open. This is critical for GPU implementations because it determines how much latency budget exists for AI inference within the L1 processing window.

**Talking point for 3GPP-adjacent discussions:** "We need the processing timeline to accommodate AI inference without forcing a choice between model complexity and latency. The GPU's parallel processing capability means we can run more complex models within the same time budget -- but only if the timeline is set appropriately."

### Position 3: Model Transfer (Case z4) Scalability

Case z4 (known model structure + parameter transfer OTA) is the surviving model transfer mechanism. The scalability of model structure across antenna configurations and bandwidths directly impacts how a GPU-accelerated gNB manages and distributes models.

**Talking point:** "Model transfer scalability is critical for commercial deployment at scale. The ARC platform can manage model lifecycle (training, compression, transfer) as a containerized NIM function, but the standard needs to define efficient parameter encoding formats that don't create bottlenecks in the air interface."

### Key Context: NVIDIA's Alliance Relationships

- **AI-RAN Alliance**: 130+ members including Nokia, Ericsson, T-Mobile, SoftBank, Deutsche Telekom
- **AI-WIN Project** (Oct 2025): NVIDIA + Booz Allen + Cisco + T-Mobile + MITRE + ODC -- "all-American AI-RAN stack"
- **Nokia partnership**: Announced to pioneer AI platform for 6G; field validation with T-Mobile in 2026
- **SoftBank**: Commercial AI-RAN deployment planned for 2026

### Interview Talking Points

- "In the AI-RAN Alliance, I'd advocate the position that 3GPP's interface-vs-implementation separation creates a natural GPU opportunity. The standard doesn't mandate GPUs, but the compute requirements for Rel-19 AI/ML -- especially Ericsson's N4=4 multi-step prediction and NW-sided positioning inference -- make GPU acceleration the practical implementation choice. I'd bring the specific 3GPP evaluation results to make this concrete, not abstract."

- "I'd coordinate with Nokia and Ericsson's 3GPP delegates on the processing timeline discussion. Both companies have a stake in this -- Nokia because their models show higher generalization degradation (meaning they may need more complex models to compensate), and Ericsson because their multi-step prediction demands more inference time. NVIDIA's position should be: set the timeline to accommodate AI, because that's where the industry is heading."

---

## Quick Reference: The Five Things You Know That Other Candidates Won't

1. **Ericsson moderated positioning across all 7 RAN1 meetings** -- they wrote every summary document and shaped every agreement. Any partner engagement on positioning must account for this.

2. **Nokia and Ericsson use fundamentally different CSI evaluation approaches** (antenna-port-delay vs beam-delay domain, in-car vs outdoor) -- they need different things from the same GPU platform.

3. **The CSI compression Direction A/B/C down-selection is the highest-stakes standards decision** for NVIDIA's product architecture -- Direction C constrains every GPU implementation to a specific Transformer model.

4. **237 formal decisions across 7 sessions with beam management leading** -- this is the most mature use case and the most ready for a production reference build on Aerial.

5. **The RRC parameter surface (R1-2501143) is the exact integration specification** -- CSI-ReportConfig, Associated ID, OtherConfig, and LPP extensions define where Aerial touches the standard.

---

## Appendix: SDK Component Quick Reference

| Component | What It Does | 3GPP Relevance |
|-----------|-------------|----------------|
| **cuPHY** | GPU-accelerated L1 PHY (PDSCH, PUSCH, SSB, CSI-RS pipelines) | Processes all measurements that feed AI/ML inference |
| **cuMAC** | GPU-accelerated L2 MAC scheduler | Scheduling decisions informed by AI/ML predictions |
| **cuPHY-CP** | L1 control plane orchestration | Handles CSI-ReportConfig, Associated ID routing |
| **pyAerial** | Python + CUDA kernel bindings (bit-accurate to cuBB) | Prototyping AI/ML pipelines against 3GPP eval assumptions |
| **Sionna** | GPU-accelerated channel simulation + ray tracing | Benchmarking against 3GPP TR 38.843 scenarios |
| **Aerial Framework** | Python-to-pipeline generation (Apache 2.0) | NEP engineers build custom AI-RAN functions |
| **NIM** | Containerized AI inference microservices | AI-on-RAN (positioning NIM, RIC NIM, network config) |
| **ARC** | GH200 + BlueField-3 hardware platform | DU + CU + UPF + RIC + NIM consolidated |
| **AODT** | Omniverse Digital Twin for RAN simulation | Pre-deployment validation of AI-RAN functions |
