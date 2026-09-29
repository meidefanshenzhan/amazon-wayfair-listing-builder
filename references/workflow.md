# Shared Workflow and Output Schemas

## 1. Input summary and source hierarchy

Summarize target platform/marketplace/language/category, verified facts and boundaries, variation structure, supplied keyword priorities, buyer questions, current fields, `DATA_MISSING`, `ASSUMPTION` and conflicts. Carry forward upstream conclusions rather than reproducing full research.

When Amazon research files are supplied, classify them before drafting:

| Layer | Typical inputs | Authority | Purpose |
|---|---|---|---|
| Product Truth | specs, manuals, drawings, packaging, verified product facts | highest for claims | determines what may be said |
| Search Demand | ABA/search volume, relevance, intent, traffic tiers, competitor ranks, root analysis | primary for keyword decisions | determines how shoppers search |
| Shopping Intent | Alexa/Rufus questions, VOC, reviews, buyer questions | primary for concern coverage | determines what shoppers need answered |
| Supplemental Semantic Assets | plugin/AI roots and suggested phrases | low / reference only | inspiration and gap discovery |

Never allow a lower-authority layer to override a higher-authority layer. Formatting/color may assist a human but must not be the only carrier of meaning when explicit fields exist.

## 2. Build a focal-product keyword pool

Do not draft directly from a category-wide keyword library. First filter to terms applicable to the focal SKU/variation.

Use this expanded schema when the source data supports it:

| Keyword | Relevance | Traffic tier / volume | Intent | Root precision | Semantic role | Competitor organic evidence | Product applicability | Evidence state | Status | Target field | Coverage state | Rationale |
|---|---|---|---|---|---|---|---|---|---|---|---|---|

Recommended values:

- Relevance: `high`, `medium`, `low`, `irrelevant`.
- Intent: preserve upstream labels such as `purchase`, `browse`; do not invent if absent.
- Root precision: preserve supplied labels such as absolute/relative/general/not-relevant; do not silently re-score upstream research.
- Status: `use`, `qualified_use`, `evidence_pending`, `brand_isolate`, `irrelevant`.
- Coverage: `exact`, `close_variant`, `semantic_root`, `backend`, `uncovered`, `not_applicable`.

Search Demand is the primary keyword authority. Supplemental Semantic Assets may suggest a phrase to inspect but cannot promote it above the researched keyword library without evidence.

## 3. Build the buyer-question / concern library

Keep raw question evidence and a normalized concern layer. Question frequency is not search volume.

| Priority | Raw question / normalized concern | Frequency | Source | Purchase stage | Answer status | Current verified answer | Best platform field | Evidence needed | Publish status |
|---|---|---:|---|---|---|---|---|---|---|

Answer statuses are `answerable`, `evidence_pending`, and `irrelevant`; publish statuses are `publish` and `hold`.

- Merge obvious near-duplicate questions for prioritization, but retain the original wording/frequency in source data.
- Separate platform/service questions from product-content questions.
- Competitors, reviews and Alexa/Rufus questions establish concerns, not focal-product answers.
- Every `evidence_pending` concern is held and names needed proof.
- Route relevant concerns into title/item highlights/bullets/description/A+/attributes/images or an internal intent library according to platform availability.
- Do not assume a marketplace exposes seller-authored Q&A.
- Aim for high-value concern coverage, not literal question repetition.

## 4. Map Product Truth to Search Demand and Shopping Intent

For every important keyword or concern, ask:

1. Is it applicable to this SKU?
2. What verified product fact supports it?
3. Is the buyer asking about a fact, benefit, use case, comparison or risk?
4. Which field can answer it most naturally?
5. Does the expression require qualification or evidence?

A concern can be important and still remain `evidence_pending`. Importance never creates proof.

## 5. Claim and expression

| Opportunity/claim | Current evidence | Current status | Allowed wording now | Boundary | Evidence needed | Wording unlocked after proof | Priority |
|---|---|---|---|---|---|---|---|

Statuses are `verified`, `observed`, `evidence_pending`, and `prohibited`. Choose a verified expression, a qualified expression, an evidence task/hold, or prohibition.

## 6. Draft the platform-native Listing

Read the selected platform reference. Across platforms:

- Build around `Who / Where / What need / Why buy` when supported, but do not force all four into every field.
- Titles/product names prioritize product clarity, primary generic intent and supported differentiation.
- Longer allowed limits are room for useful information, not a target to fill mechanically.
- Each feature/bullet has one communication job. Avoid an overview followed by repeated component detail.
- Descriptions deepen role, differentiation, scenarios, specifications and boundaries without repeating every feature.
- Rich-content/image briefs state job, buyer question, message, image concept, proof, mobile crop, dependency and status.
- Conversational coverage uses natural buyer needs; it is not an official readiness score.
- Localize meaning and shopping language; do not mechanically translate keyword phrases from another marketplace.

## 7. Audit keyword and concern coverage

### Keyword coverage

For each important focal-product term, record `exact`, `close_variant`, `semantic_root`, `backend`, `uncovered`, or `not_applicable`. Do not falsely label semantic/root coverage as exact phrase coverage.

### Buyer-concern coverage

For each high-priority relevant concern, record:

| Concern | Frequency signal | Answerable? | Covered? | Field(s) | Evidence | Gap/action |
|---|---:|---|---|---|---|---|

Coverage means the Listing provides enough verified information to answer the underlying concern. It does not require copying the question verbatim.

## 8. Execution changes

| Priority | Platform field | Current issue | Exact action | Replacement/hold instruction | Dependency | Executable now | Acceptance check |
|---|---|---|---|---|---|---|---|

- `P0`: unsupported/high-risk copy, contradictory required fact, trademark/field-rule failure, or category-required missing evidence.
- `P1`: material relevance, conversion, clarity, keyword/concern gap or evidence opportunity that does not block a safe version.
- `P2`: optional wording, layout or experiment.

Separate executable actions, evidence/product decisions and true blockers. Every action names an actual or explicitly conditional platform field.

## 9. Audit dimensions

Audit factual support, claim/trademark risk, focal-product keyword selection, keyword coverage state, buyer-concern answer coverage, readability/duplication, live limits, cross-field/variation consistency, attribute/asset completeness and action executability. Never claim marketplace approval, ranking lift, conversion lift or shopping-assistant preference from a heuristic.
