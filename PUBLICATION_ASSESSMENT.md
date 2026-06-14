# Publication-Positioning Assessment — World Road Geometric-Design Standards Corpus + Skill + Serbia Gap-Analysis

*Prepared 2026-06-14. Skeptical, calibrated read of academic-publication value as the work stands today, and what would raise its level. Every venue/prior-art claim below is grounded in a cited source.*

---

## VERDICT (top line — read this first)

**As it stands today, none of the three built components is, by itself, an international-journal paper.** The work is an impressive *engineering/infrastructure deliverable* and a strong *dissertation enabler*, but its current form is descriptive (a curated corpus + a retrieval skill + a completeness audit), and the one genuinely publishable analysis — the Serbia gap-analysis — is **planned, not done**, and sits in a space where substantial gray-literature prior art already exists (the official DRI/PE "Roads of Serbia" harmonisation project produced 3,200+ bilingual pages comparing Serbian rules to EU/foreign regulations — see §B/§D).

Component-by-component calibration:

| Component | Honest level | Why |
|---|---|---|
| 1. Multilingual corpus / database of ~20 countries' standards | **Not independently publishable** as a research paper. Marginal as a "data paper" (licensing kills it). | Republishing copyrighted national standards is not a novel dataset; the curation is valuable infrastructure, not a finding. |
| 2. Comparative multi-country parameter analysis | **Conference / regional journal** as pure tabulation; **international** only if fused with a safety/operating-speed lens or a defensible framework. | Cross-country comparisons exist but are fragmented; "yet another table" is incremental. |
| 3. AI / multilingual-RAG-over-standards method | **International (computing-in-civil-eng) IF** evaluated rigorously with a benchmark + baselines. Currently a v0 skill with no eval → not yet. | The field is hot and crowded (2024–2026 ASCE JCCE, Automation in Construction, arXiv). Bar is now "beat a baseline on a benchmark," not "we built a RAG." |
| 4. Serbia gap-analysis + improvement proposals (planned) | **National/regional** as descriptive comparison; **international** only with quantitative safety linkage + generalizable method. | Strong, defensible national contribution and a clear dissertation chapter — but overlaps existing official harmonisation work. |

**Bottom line:** This is a **solid PhD-dissertation backbone and 1–2 national/regional papers right now.** Reaching an indexed international journal requires adding *a method or a measured outcome* (a validated retrieval benchmark, OR a safety/operating-speed-grounded comparative framework), not more standards.

---

## A. Is the COMPILATION / database publishable on its own?

**No.** Three reasons, in order of severity:

1. **Copyright / licensing.** A "data paper" requires a *citable, openly reusable* dataset (FAIR, redistributable). The corpus contains paid, licensed PDFs (AASHTO Green Book, FGSV RAA/RAL/RASt) that are *gitignored precisely because they cannot be redistributed*, plus many national standards that are Crown/government copyright. You cannot publish an open dataset whose core content you are not allowed to share. Data journals (Elsevier *Data in Brief*, Nature *Scientific Data*) explicitly require the data be deposited and reusable; a metadata-only "index of where to buy standards" is not a dataset. ([Data in Brief / Scientific Data scope](https://www.nature.com/articles/s41597-025-04402-4); [what data papers require](https://onlinelibrary.wiley.com/doi/full/10.1002/leap.2001))
2. **No novelty in compilation.** Curating known official documents is librarianship, not a research contribution. The provenance/SHA verification is good practice and worth reporting *as a methods subsection of a larger paper*, but is not a standalone finding.
3. **It is derivative re-publication.** The value is the *normalized, comparable knowledge layer* you extract — and that layer (Phases 1–3) is not built yet.

**What it CAN be:** the Methods/Materials section of the comparative paper, and the supplementary "open replication" artifact (release the *glossary, concept taxonomy, extraction code, and a normalized fact-sheet table of values with citations* — those you authored, so they ARE redistributable, even if the source PDFs aren't). That open artifact materially strengthens a methods paper but is not a paper itself.

---

## B. The COMPARATIVE multi-country analysis — prior art & novelty

**Prior art exists and is broader than a quick look suggests — so a plain comparison is incremental.** Key findings:

- **Cross-country comparative studies are an established (if fragmented) genre.** Examples surfaced: design-consistency state-of-the-art reviews ([ASCE *J. Transportation Engineering* 125(4), 1999, "State of the Art of Highway Geometric Design Consistency"](https://ascelibrary.org/doi/10.1061/%28ASCE%290733-947X%281999%29125%3A4%28305%29)); the "Comparative Geometrics" body of work cataloguing multi-country highway design standards ([multi-country highway design standards](https://comparativegeometrics.wordpress.com/2013/08/07/multi-country-highway-design-standards/)); UNECE Trans-European Motorway (TEM) recommended geometric figures as a cross-national reference; and recurring two-country comparisons (e.g. Canada–Germany passing-lane/cross-section practice). A 2026 *Transportation in Developing Economies* systematic review of design-consistency tools shows the comparative/review niche is actively published ([Springer 2026](https://link.springer.com/article/10.1007/s40890-026-00256-6)).
- **The Serbia-specific comparison is already partly done officially.** The Slovenian DRI led "Harmonisation of road technical guidelines in the Republic of Serbia," reviewing Serbian acts/rules/standards against EU and foreign regulations, producing **3,200+ pages in Serbian and English** ([DRI project page](https://www.dri.si/en/fields-of-work/railways/harmonisation-of-road-technical-guidelines-in-the-republic-of-serbia)); the Serbian Road Design Manual (SRDM) is itself the harmonised-practice output. There is even a published note "Technical Essentials of Road Geometric Design in Serbia" comparing Serbian and Chinese codes ([CSUST journal](https://zwgl1980.csust.edu.cn/journal/vol44/iss1/31/)).

**Verdict on B:** A 20-country tabulation of R_min / e_max / sight distance / weaving thresholds is **useful but incremental → conference or regional journal**, *unless* it does something the prior art does not: e.g., (i) the *breadth* (20 standards in 11 languages including CJK/Cyrillic is genuinely larger than typical 2–4 country comparisons) framed as a *structured, reproducible comparison method*; or (ii) couples parameter differences to **operating-speed / design-consistency / crash outcomes** (the lens that gets work into *Accident Analysis & Prevention* and TRR — see [operating-speed consistency models](https://www.sciencedirect.com/science/article/abs/pii/S0001457512003570)). Breadth alone is a quantity argument, not a novelty argument; reviewers at international journals will ask "so what follows from the differences?"

---

## C. The AI / multilingual-RAG-over-standards METHOD

**This is the most likely route to an international (and high-impact) paper — but it is NOT publishable in its current v0 state, and the field is now competitive.**

The field is active and 2024–2026 hot:
- [*J. Computing in Civil Engineering* 39(4): "Using LLMs to Answer Questions about Building Codes and Standards"](https://ascelibrary.org/doi/abs/10.1061/JCCEE5.CPENG-6037) — the flagship ASCE venue, directly on-topic.
- [Fine-tuning LLMs + evaluating retrieval methods for QA on building codes (arXiv 2505.04666, 2025)](https://arxiv.org/pdf/2505.04666)
- [LLM-driven code-compliance checking in BIM (MDPI Electronics, 2025)](https://www.mdpi.com/2079-9292/14/11/2146)
- [NLP-based regulatory compliance with GPT-4 (arXiv 2412.20602)](https://arxiv.org/pdf/2412.20602); [LLMs for interpreting building regulations (arXiv 2407.21060)](https://arxiv.org/pdf/2407.21060)

**Implications:**
- A bare "we built a RAG over standards" is no longer novel. The bar is now: a **benchmark question bank with ground-truth citations**, **measured retrieval/answer accuracy**, **comparison to baselines** (keyword search, generic RAG, an off-the-shelf LLM), and an **ablation** isolating what actually helps.
- **Your genuine differentiator** = *cross-lingual* retrieval over engineering standards in 11+ languages including non-Latin scripts (Cyrillic/CJK), with a domain concept-taxonomy + multilingual term glossary mediating "concept → correct clause in any language." Almost all existing work is monolingual English on building codes. *Multilingual, cross-standard road-geometry QA with citation-grounded answers and a measured benchmark* is a defensible, fresh contribution.
- **Gap to close:** Phase 5 (eval) is not done. Right now there is no benchmark, no accuracy number, no baseline. Until those exist, this is a tool, not a result. The eval is the paper.

**Best venues for C:** ASCE *J. Computing in Civil Engineering*; Elsevier *Automation in Construction* (high impact, very competitive); *Advanced Engineering Informatics*; for an NLP-leaning framing, an *NLLP* (Natural Legal Language Processing) workshop or a domain track.

---

## D. The SERBIA gap-analysis + improvement proposals

**Publishable level: national/regional as descriptive; international only if elevated with measurement + method.**

- A "compare our national standard to international best practice and recommend updates" paper is a **well-established national/regional genre**. It is a strong, legitimate contribution at that tier and a natural dissertation chapter.
- **But the Serbia case is partly occupied** by the official harmonisation work (DRI 3,200 pages; SRDM as the harmonised manual — §B). To be a *research* contribution rather than a consultancy restatement, the gap-analysis must add something those did not: a *systematic, reproducible, multi-standard* benchmarking (your 20-standard corpus is the asset here), explicit identification of where Pravilnik 50/11 is *silent* (the audit already flags "where the standard is mute" as a deliverable — that is the genuinely novel angle), and ideally a **safety/operating-speed rationale** for each recommended change rather than "other countries use a higher value."
- The most defensible framing: *"Where is the Serbian geometric-design regulation silent or divergent versus international practice, and what is the safety/consistency justification for each proposed revision?"* — that reframes a comparison into an evidence-based standards-improvement argument.

**Best venues for D:** national/regional first — Serbian Road Congress; *Put i saobraćaj* / *Tehnika*; *Građevinar* (Croatia, Scopus/SCIE) or *Promet–Traffic & Transportation* (Croatia, Scopus) for a regional ex-YU international reach; then a Scopus/SCIE road journal (Baltic JRBE, *Transport* Vilnius Tech) if the safety/method angle is added.

---

## E. Overall verdict & venue ladder (real, currently-active venues; verified scope/indexing)

### International journals

| Venue | Indexing | Fit for THIS work | Honest acceptance read |
|---|---|---|---|
| **Transportation Research Record (TRR)** | Scopus/SCIE; SAGE/TRB | Good for comparative + safety/operating-speed framing | Realistic *if* there's a measured finding (consistency/safety), not just tables. Volume venue, fair odds with real analysis. |
| **ASCE *J. Transportation Engineering, Part A: Systems*** | Scopus/SCIE | Comparative geometric-design + consistency | Needs modelling/quantitative core, not description. Moderate–hard. |
| **ASCE *J. Computing in Civil Engineering*** | Scopus/SCIE | **Best home for the AI/RAG method** | Strong fit IF rigorous benchmark + baselines. Competitive but on-topic. ([on-topic precedent](https://ascelibrary.org/doi/abs/10.1061/JCCEE5.CPENG-6037)) |
| **Elsevier *Automation in Construction*** | Scopus/SCIE, high IF | AI-over-standards method | Very competitive; needs strong novelty + eval. Aspirational. |
| ***Accident Analysis & Prevention* / *Safety Science*** | Scopus/SCIE | Only if comparison is tied to crash/safety outcomes | Hard; needs genuine safety data/modelling. |
| **European Transport Research Review (ETRR)** | Scopus/SCIE, OA ([scope](https://etrr.springeropen.com/about)) | Policy/system implications of standards divergence | NOTE: *explicitly does not publish pure infrastructure-technology papers* — must frame around transport-system/policy impact. Watch fit. |
| **IATSS Research** | Scopus/SCIE, OA | Safety-policy framing of standards | Plausible if safety/policy angle. |
| ***Transport* (Vilnius Tech)** | Scopus/SCIE | Comparative/method road engineering | Reasonable Q-tier fit for a method or broad comparison. |
| **Baltic J. of Road and Bridge Engineering** | Scopus, SCIE, Q3 ([SJR](https://www.scimagojr.com/journalsearch.php?q=12300154909&tip=sid)) | Road geometric design comparison | Realistic Q3 home for the comparative paper. Good fallback international. |
| ***Građevinar* (HR)** | Scopus/SCIE | Regional, broad civil-eng | Realistic regional-international home for the Serbia/comparison paper. |
| ***Promet – Traffic&Transportation* (HR)** | Scopus | Traffic/road, regional | Realistic regional-international. |

### International conferences

| Venue | Note |
|---|---|
| **TRB Annual Meeting** (Washington) | Premier; TRR-linked. Strong for the comparative/safety angle. |
| **PIARC World Road Congress** | Practitioner-heavy, high prestige, good for standards/harmonisation. |
| **CETRA (Road and Rail Infrastructure, Croatia)** | Regional-international, well-matched, realistic. |
| **TRA (Transport Research Arena, Europe)** | EU policy/research; fits harmonisation framing. |
| **Road-safety confs (ICTCT, RS5C/TRA safety tracks)** | If the safety linkage is developed. |

### National / regional

| Venue | Note |
|---|---|
| **Srpski kongres o putevima (Serbian Road Congress)** — next ed. **4–5 Jun 2026, Belgrade**, co-organized by the Belgrade Faculty of Civil Engineering ([6th congress notice](https://www.via-vita.rs/skupovi/6-srpski-kongres-o-putevima-4-5-jun-2026-prvo-saopstenje/)) | **Ideal first outlet** for the Serbia gap-analysis. Direct audience (regulator, PE Roads of Serbia). |
| ***Put i saobraćaj*** (DRC/Via-Vita journal) | National journal of record for Serbian roads. |
| ***Tehnika*** (SITS, Serbia) | National engineering journal. |
| **Regional ex-YU** (*Građevinar*, *Promet*, *Izgradnja*) | Step-up reach with Scopus indexing. |

---

## F. What concrete additions would lift it from national → international

A prioritized, specific checklist. Items marked **[high leverage]** move the needle most.

- [ ] **[high leverage] Build the retrieval benchmark + measure it (Phase 5).** A ≥50-question bank across concepts/standards/languages, each with ground-truth answer + citation. Report retrieval precision/recall and answer accuracy. **Add baselines**: keyword search, generic (non-taxonomy) RAG, and an off-the-shelf LLM with no retrieval. **Ablate** the multilingual glossary and concept-taxonomy to show they cause the gain. *This single item converts the skill from "tool" to "publishable method" and is your clearest international path (ASCE JCCE / Automation in Construction).*
- [ ] **[high leverage] Tie at least one parameter comparison to a SAFETY / operating-speed outcome.** Don't stop at "country X allows e_max=8%, country Y=7%." Show, via an operating-speed or design-consistency model (the established surrogate-safety method — [Camacho-Torregrosa et al., AAP 2013](https://www.sciencedirect.com/science/article/abs/pii/S0001457512003570)), what a given Serbian threshold implies for consistency/crash risk versus alternatives. This is the dividing line between a national table and a TRR/AAP paper.
- [ ] **[high leverage] Make the method generalizable beyond Serbia.** Frame the gap-analysis as a *reusable framework* ("a citation-grounded, multilingual benchmarking method for auditing any national geometric-design regulation against international practice"), with Serbia as the worked case study. A framework + case study travels internationally; "Serbia vs the world" does not.
- [ ] **Normalize and release the values layer (Phases 1–3) as an open, citable artifact** — the parts you authored (concept taxonomy, multilingual glossary, normalized SI fact-sheets *with citations*, extraction/retrieval code), DOI'd on Zenodo. This gives reproducibility credit without infringing source copyright.
- [ ] **Validate extracted values** against the primary source (the skill itself warns v0 values are unverified). Reviewers will spot-check; you need an accuracy/QA statement and an inter-checker or source-page audit.
- [ ] **Differentiate explicitly from the DRI harmonisation project and SRDM** in the related-work section — state what your systematic 20-standard, silence-aware, reproducible method adds over the existing 3,200-page consultancy comparison. (If you can't articulate this, the international novelty isn't there yet.)
- [ ] **Complete the corpus gaps that affect claims** (CJK OCR for CHN/BRA, the missing junction/cross-section volumes the audit flags). Don't claim "20 countries' weaving rules" if 6 standards are PARTIAL on junctions.
- [ ] **Position the multilingual/cross-script angle as the novelty** in the AI paper — almost all prior code-QA work is monolingual English; cross-lingual citation-grounded QA over engineering standards is genuinely under-explored.

---

## G. Doctoral-dissertation fit

**Strong — this is a credible dissertation backbone, arguably stronger as a thesis than as standalone papers.**

- The natural shape is a **cumulative / paper-based dissertation** with three linked contributions: (1) a *method/system* paper (multilingual citation-grounded retrieval over geometric-design standards — the AI angle, internationally aimed), (2) a *comparative-analysis* paper (the international parameter comparison, ideally with the safety lens), and (3) the *applied national* contribution (Serbia gap-analysis + improvement proposals, national/regional + congress). Together these tell one coherent story: *build the knowledge instrument → use it to compare the world → use the comparison to improve the Serbian standard.*
- For a Belgrade Faculty of Civil Engineering road-design PhD, the Serbia gap-analysis is the *applied core the faculty and the Serbian road community will value*, while the AI method supplies the *international novelty* a modern dissertation is expected to show. That pairing is well-calibrated.
- **Caveats for the dissertation:** (i) the AI/skill component must be evaluated, not just demonstrated, or examiners will read it as engineering plumbing rather than research; (ii) the comparison must rise above tabulation to a defensible analytical framework; (iii) the work must clearly delineate the *new scientific contribution* beyond the existing official harmonisation work — Serbian doctoral evaluation (naučna zasnovanost / scientific foundation) hinges on demonstrable novelty.

**Net:** Excellent dissertation material and a clear 3-paper plan. The corpus/skill as they stand are the *foundation and instrument*, not yet the *findings*; the findings come from the eval (C) and the analysis (D) once executed with a method and a measured outcome.

---

### One-paragraph summary
The built artifacts (multilingual 20-country corpus, retrieval skill, completeness audit) are a high-quality research *instrument*, not yet research *results*. The corpus can't be a data paper (licensing + no novelty). A plain multi-country comparison is conference/regional-tier because comparative prior art and an official Serbian harmonisation project already exist. The clearest international path is the **AI/multilingual-RAG method with a measured benchmark and baselines** (ASCE J. Computing in Civil Eng / Automation in Construction), and/or a **comparison fused with an operating-speed/safety-consistency lens** (TRR / AAP). The Serbia gap-analysis is a strong national/regional + Serbian-Road-Congress contribution and the applied heart of the dissertation. To go international: *measure the retrieval, link parameters to safety, and make the method a generalizable framework.*
