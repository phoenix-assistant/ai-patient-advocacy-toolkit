# AI Patient Advocacy Toolkit

> **One-line pitch:** Open-source toolkit helping families navigate complex medical situations by extracting, analyzing, and cross-referencing their own health records with AI.

---

## Problem

**Who feels the pain:** Families dealing with serious illness (cancer, rare diseases, chronic conditions) who must coordinate care across multiple providers, interpret complex medical records, catch errors, and advocate for themselves in a system that doesn't prioritize patient understanding.

**How bad:**
- **3.6 million Americans** diagnosed with cancer annually; families become de facto care coordinators overnight
- Medical errors are the **3rd leading cause of death** in the US (~250,000/year per Johns Hopkins)
- Average cancer patient sees **7+ specialists** across multiple health systems
- 80% of serious medical errors involve miscommunication during care transitions
- Patients can legally access their records (21st Century Cures Act) but have no tools to understand them
- The "cancer care case" that went viral showed a family catching a dangerous drug interaction the oncology team missed

**Emotional intensity:** This is life-or-death. Families are desperate, scared, and willing to pay/donate for tools that could save their loved ones.

---

## Solution

A comprehensive open-source toolkit with four core components:

### 1. Record Export Guide
- Step-by-step instructions for exporting from Epic MyChart, Cerner, Meditech, Allscripts
- Video walkthroughs for each major EHR portal
- FHIR API integration for automated pulls where available
- PDF parsing pipeline for legacy records

### 2. Medical Record Analyzer
- Prompt templates optimized for medical record analysis
- Extraction of diagnoses, medications, procedures, lab values
- Timeline reconstruction across multiple providers
- Jargon translation to plain English

### 3. Cross-Reference Checker
- Drug-drug interaction detection (using OpenFDA, DrugBank)
- Diagnosis-treatment alignment verification
- Duplicate test identification
- Missing follow-up detection
- Contradiction finder (conflicting diagnoses/notes between providers)

### 4. Emergency Detection Patterns
- Red flag lab values (critical highs/lows)
- Dangerous medication combinations
- Time-sensitive finding escalation
- "Questions to ask your doctor" generator

---

## Why Now

1. **21st Century Cures Act (2021)** mandated patient access to records via FHIR APIs — infrastructure finally exists
2. **LLMs capable of medical reasoning** — GPT-4, Claude can genuinely parse complex medical text
3. **Viral case study** — cancer care coordination story proved massive latent demand
4. **Post-COVID healthcare skepticism** — patients want to verify, not just trust
5. **Information blocking now illegal** — providers can't refuse electronic access anymore

---

## Market Landscape

### TAM/SAM
- **TAM:** $50B+ US healthcare navigation market
- **SAM:** $2B patient advocacy / care coordination tools
- **SOM:** $50M families actively managing serious illness who would use software tools

### Competitors

| Company | What They Do | Weakness |
|---------|--------------|----------|
| **Picnic Health** | Record aggregation service | $500-1000/year, passive collection not analysis |
| **Particle Health** | B2B record access API | Enterprise only, no consumer tools |
| **Ciitizen** (acquired by Invitae) | Cancer record aggregation | Shutdown after acquisition, was passive |
| **PicnicHealth** | Clinical trial matching via records | Not focused on advocacy/analysis |
| **Medisafe** | Medication management | No record analysis, just pill reminders |
| **CareZone** | Family health organizer | Shut down 2023 |
| **MyChart (Epic)** | Patient portal | No AI analysis, just record viewing |

**Gap:** No one is giving patients **AI-powered analysis tools** to actually understand and cross-reference their records. All existing players either aggregate passively or serve enterprises.

---

## Competitive Advantages

1. **Open source** — Trust matters enormously in healthcare; families can verify what the tool does
2. **Local-first option** — Sensitive records never leave the device (Ollama, llama.cpp)
3. **Community-driven medical prompts** — Oncologists, nurses, patient advocates can contribute domain expertise
4. **No vendor lock-in** — Works with any LLM (OpenAI, Anthropic, local models)
5. **Built by/for families** — Not a VC-backed startup trying to monetize patient data

---

## Technical Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    User Interface                        │
│  (Electron desktop app / Web app with local processing) │
└─────────────────────────────────────────────────────────┘
                            │
┌───────────────────────────┴────────────────────────────┐
│                   Core Processing                       │
├─────────────────┬─────────────────┬───────────────────┤
│  Record Import  │   AI Analysis   │  Cross-Reference  │
│  ─────────────  │   ───────────   │  ───────────────  │
│  • FHIR client  │  • Prompt eng   │  • Drug checker   │
│  • PDF parser   │  • LLM adapter  │  • Lab analyzer   │
│  • HL7 parser   │  • Extraction   │  • Timeline merge │
│  • CCD reader   │  • Summarize    │  • Contradiction  │
└─────────────────┴─────────────────┴───────────────────┘
                            │
┌───────────────────────────┴────────────────────────────┐
│                  LLM Backend (pluggable)                │
│  Local: Ollama, llama.cpp  |  Cloud: OpenAI, Anthropic │
└─────────────────────────────────────────────────────────┘
                            │
┌───────────────────────────┴────────────────────────────┐
│               Medical Knowledge Bases                   │
│  • OpenFDA (drugs)  • RxNorm  • SNOMED CT  • ICD-10   │
└─────────────────────────────────────────────────────────┘
```

### Tech Stack
- **Desktop app:** Electron + React (or Tauri for lighter footprint)
- **PDF parsing:** pdf.js + layoutparser + Azure Document Intelligence fallback
- **FHIR client:** SMART on FHIR JavaScript library
- **LLM integration:** LangChain or custom adapter layer
- **Drug database:** OpenFDA API + local DrugBank cache
- **Local LLM:** Ollama with medical-tuned Llama 3 or Mistral

---

## Build Plan

### Phase 1: Core Toolkit (Months 1-3)
- [ ] Record export documentation for top 5 EHR systems
- [ ] PDF parsing pipeline with OCR fallback
- [ ] Basic prompt templates for medication list extraction
- [ ] Simple drug interaction checker (OpenFDA integration)
- [ ] CLI tool for power users
- **Deliverable:** Usable CLI tool, documentation site

### Phase 2: Desktop App + AI Analysis (Months 4-6)
- [ ] Electron desktop app with local LLM support
- [ ] Full medical record summarization
- [ ] Cross-provider timeline view
- [ ] Contradiction detection between records
- [ ] "Questions for your doctor" generator
- **Deliverable:** Polished desktop app, beta community

### Phase 3: Community + Enterprise (Months 7-12)
- [ ] Community prompt library with voting/rating
- [ ] Patient advocate certification program
- [ ] Enterprise version for patient advocacy organizations
- [ ] White-label for hospital patient experience teams
- [ ] HIPAA compliance documentation
- **Deliverable:** Sustainable revenue, 10K+ active users

---

## Risks & Challenges

| Risk | Severity | Mitigation |
|------|----------|------------|
| **Liability for medical advice** | HIGH | Clear disclaimers, never prescribe/diagnose, "discuss with doctor" framing |
| **LLM hallucination in medical context** | HIGH | Retrieval grounding, confidence scores, human verification UX |
| **HIPAA concerns (cloud processing)** | MEDIUM | Local-first architecture, optional cloud, BAA for enterprise |
| **EHR vendors blocking access** | MEDIUM | Document legal rights, FHIR standardization, community pressure |
| **Emotional weight of errors** | MEDIUM | Extensive testing, clear limitations, support community |
| **Maintenance burden of open source** | MEDIUM | Governance model, enterprise revenue for sustainability |

---

## Monetization (Path to $1M ARR)

### Revenue Streams

1. **Freemium Desktop App**
   - Free: Local processing, basic analysis
   - Pro ($15/month): Cloud LLM access, advanced features, priority support
   - Target: 6,000 Pro subscribers = $1.08M ARR

2. **Enterprise/White-Label**
   - Patient advocacy organizations: $500-2000/month
   - Hospital patient experience teams: $2000-5000/month
   - Target: 50 organizations × $1500/month avg = $900K ARR

3. **Training & Certification**
   - Patient advocate certification: $200-500 one-time
   - Hospital staff training: $5000-10000 per engagement
   - Target: 200 certifications + 20 training engagements = $140K

### Path to $1M ARR
- **Year 1:** Launch, build community, 1000 Pro subscribers ($180K)
- **Year 2:** Enterprise pilots, certification program, 4000 Pro + 30 enterprise ($1M+)

---

## Verdict: 🟢 BUILD

**Why BUILD:**
1. **Genuine pain point** — Families in medical crisis are desperate for tools
2. **Proven demand** — Viral case study shows people want this
3. **Timing perfect** — FHIR mandates + capable LLMs = infrastructure ready
4. **Clear moat** — Open source + local-first creates trust competitors can't match
5. **Multiple revenue paths** — Consumer, enterprise, training all viable
6. **Personal meaning** — This saves lives, not just makes money

**Execution risks are real** (liability, hallucination, emotional weight), but the opportunity to genuinely help families while building a sustainable business is compelling. The viral story proves latent demand; now someone needs to build the tool.

**Recommended approach:** Start with the open-source toolkit (GitHub, community building), then layer on Pro features and enterprise once trust is established. Lead with the mission, monetize around the edges.
