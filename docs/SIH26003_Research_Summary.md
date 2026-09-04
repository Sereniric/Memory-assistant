# Research Summary: SIH 26003 — Landscape & Gap Analysis

**Project:** AI-Based Cognitive Gaming and Memory Assistance Platform for Elderly Dementia Patients in North Eastern Region (NER)
**Organization:** Ministry of Development of North Eastern Region (MDoNER)
**Prepared for:** Sequence Recall MVP (Flask / Jinja2 / SQLite architecture)
**Date:** September 2026

---

## 1. What the Problem Statement Actually Asks For

The official SIH 26003 brief is broader than a single memory game. The background notes that the North Eastern Region is seeing rising dementia and memory-loss cases among the elderly, with limited access to affordable, culturally inclusive digital therapeutic solutions due to remote geography and thin healthcare infrastructure.

The expected solution has **five distinct components**:

1. **Interactive cognitive games** — including pattern/object recognition tied to emotional and mental engagement.
2. **AI/ML-driven difficulty adaptation** — based on patient performance *and* cognitive condition (not just score).
3. **Multilingual, voice-assisted interaction** — suitable for elderly users in NER specifically.
4. **Cultural localization** — regional themes, visuals, sounds, and regional-language support for engagement.
5. **Reminders and caregiver tooling** — medical appointment reminders, plus dashboards for caregivers/health workers to track patient progress.

Only component 1 (and part of 2) is what the current MVP scope covers.

---

## 2. Existing Solutions — Global Market

| Solution | Strength | Relevant Limitation |
|---|---|---|
| **BrainHQ** (Posit Science) | Rated highest in a peer-reviewed JMIR mHealth systematic review of cognitive training apps; strong adaptive-difficulty engine | English-only, subscription (~$96–170/yr), not clinically staged to dementia condition |
| **CogniFit** | Has dedicated 55+ programs, personalizes training to user ability, used in some clinical trial contexts | Subscription-based, no regional-language/voice layer, no caregiver medical-reminder system |
| **Lumosity / Peak / Elevate** | Large user bases, polished gamified UX, good daily engagement | Generic "brain fitness" — not designed around a diagnosed cognitive condition; no caregiver dashboard |
| **MindMate** | Closest existing "full platform": brain games + reminders/to-do + reminiscence tools + caregiver engagement features | Built for UK/Western users and languages; no NER cultural content, no clinical difficulty-condition mapping |
| **Medisafe** | Best-in-class medication/appointment reminders with caregiver alerts on missed doses | Reminder-only; no cognitive games or difficulty adaptation at all |

**Independent finding worth noting:** a systematic review of mobile cognitive-training apps for older adults (published in JMIR mHealth) concluded that even the best current apps show "moderate quality with considerable variability," and called for more personalization and closer alignment with healthcare-professional guidance — i.e., the category-wide problem isn't a lack of games, it's a lack of *clinically grounded, personalized* platforms.

---

## 3. Existing Solutions — India-Specific

The most relevant Indian effort is **not a patient-facing app** — it's the ICMR's **MUDRA Toolbox** (Multilingual Dementia Research and Assessment Toolbox), built by NIMHANS, AIIMS, and other institutions.

- It is a **diagnostic/assessment instrument** for clinicians and researchers — cognitive tests and questionnaires across attention, memory, language, and visuospatial domains.
- It is validated in **five Indian languages**: Hindi, Bengali, Telugu, Kannada, and Malayalam.
- **No North-Eastern language is covered** (Assamese, Khasi, Garo, Mizo, Manipuri/Meitei, Naga languages, etc.) — the exact population MDoNER's problem statement targets.
- It is a screening tool, not a gaming/engagement/caregiver platform — it doesn't overlap with what SIH 26003 is asking teams to build, but it confirms that even India's own dementia infrastructure hasn't reached NER languages yet.

Separately, research on rural southern Indian elderly populations has found a correlation between multilingualism and better cognitive outcomes, reinforcing why language-authentic (not just translated) content matters for engagement and outcomes in this demographic — not just accessibility.

---

## 4. Gap Analysis

| Requirement (from PS 26003) | Covered by existing solutions? | Gap |
|---|---|---|
| Regional NER language + cultural content | No | Every major app is English/global-language; even ICMR's own multilingual tool stops at 5 mainstream Indian languages |
| Affordable / low-cost access | Partially | Leading apps (BrainHQ, CogniFit) are paid subscriptions — a barrier for a government-scheme rural population |
| Difficulty tied to *cognitive condition*, not just score | Partially | Consumer apps adapt to performance trends; none adapt to a diagnosed dementia stage |
| Voice-first interaction for low-literacy elderly | No | All major apps are touch/text-first; voice is secondary or absent |
| Games + reminders + caregiver dashboard in one product | Partially | MindMate combines games + reminders + caregiver tools, but with no regional/cultural NER layer or clinical difficulty logic |
| Low-bandwidth / rural-infrastructure friendly | Not addressed anywhere found | No solution reviewed explicitly designs for low-connectivity rural delivery |

**Bottom line:** the *components* (games, reminders, caregiver dashboards, adaptive difficulty) all exist individually and are well-executed elsewhere. What doesn't exist is all five combined **and** localized to NER languages/culture **and** affordable/lightweight enough for rural delivery. That combination — not any single game mechanic — is the actual whitespace in this problem statement.

---

## 5. Implications for the Current MVP

The existing architecture (Flask + Jinja2 + Flask session, no JavaScript) is well suited to:

- **Component 1 (games)** — Sequence Recall is a reasonable first slice; server-rendered simplicity is also an accessibility asset for elderly, low-literacy users (no client-side complexity to fail on old devices/low bandwidth).
- **Component 2 (adaptive difficulty)** — can be built server-side using session/SQLite-tracked performance history; the harder, differentiating version (tied to *cognitive condition*, not just score) would need a simple clinical-staging input rather than pure game-score logic.

Not yet addressed by current scope, but flagged by this research as the actual differentiators:

- Regional language/voice layer (component 3–4)
- Reminders (component 5a)
- Caregiver dashboard (component 5b)

Recommendation: keep SQLite/SQLAlchemy schema design (planned for later) oriented so that game performance data can feed both the difficulty engine *and* a future caregiver-facing progress view — this is the connective tissue none of the reviewed existing products handle well together.

---

## 6. Sources

- SIH 2026 Problem Statements (Software), PS 26003 — https://sih-2026-problem-statements.shaikrohit187.workers.dev/public/pdfs/SIH_2026_All_PS.pdf
- SIH26003 breakdown — https://sih-buddy.vercel.app/ps/SIH26003
- SIH26003 official listing — https://sih2026.vuce.in/ps/SIH26003
- BrainHQ / JMIR mHealth systematic review coverage — https://www.brainhq.com/?p=27149
- Brain training app comparison (2026) — https://caringvillage.com/blog/caregiver-tech/best-brain-training-apps/
- Brain training apps for seniors comparison — https://www.finder.com.au/brain-training-for-seniors
- ICMR MUDRA Toolbox announcement — https://www.deccanherald.com/india/icmr-releases-dementia-research-and-assessment-tool-1038003.html
- ICMR MUDRA Toolbox detail — https://biovoicenews.com/?p=37183
- MindMate app overview — https://dta.com.au/mindmate/
- Dementia caregiver apps overview — https://www.relish-life.com/blog/apps-dementia-caregivers
- Apps for dementia patients overview — https://wis.it.com/apps-for-dementia-patients
- Multilingualism and cognitive performance in rural India — https://pmc.ncbi.nlm.nih.gov/articles/PMC10927057
