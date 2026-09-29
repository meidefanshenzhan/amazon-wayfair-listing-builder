# Amazon Platform Route

Verify current marketplace, category and product-type rules in Seller Central or authoritative Amazon documentation before publication. Treat policy values below as a dated default profile, not a permanent universal constant.

## 2026 default policy profile

For non-media Amazon listings, the general rule effective 2026-07-27 is:

- Title: 75 characters or fewer including spaces.
- Item Highlights: up to 125 characters; use for useful materials, use cases or comparison-helping details. It is searchable and visible with the title where supported.
- Bullets / key product features: keep when the live product type exposes them; do not assume Item Highlights replaces every bullet field or that each bullet has a 125-character rule.
- Product description.
- A+ brief when available and in scope.
- Backend Generic Keywords / Search Terms when exposed: less than 250 UTF-8 bytes under the general Amazon rule; verify marketplace exceptions and the live field.

Record `policy_verified_at`, marketplace, product type and sources in the output when live limits materially affect publication.

## Search and semantic strategy

Amazon discovery is not a reason to mechanically repeat every keyword. Build clear product semantics from verified entities, attributes, relationships, use cases and buyer needs while preserving important search-demand language.

Use three evidence layers with different authority:

1. **Search Demand** — user-supplied keyword research, such as ABA/search volume, relevance, intent, traffic tier, competitor organic ranking, root analysis and product applicability. This is the primary source for keyword prioritization and placement.
2. **Shopping Intent / Buyer Concerns** — Alexa/Rufus-style recommended questions, reviews/VOC or other buyer-question research. Use this to identify what shoppers need answered and which product facts/relationships should be made explicit. Question frequency is not search volume.
3. **Supplemental Semantic Assets** — AI/plugin-generated roots, phrases or suggested terms. Treat as low-authority inspiration only. Never let this layer override the keyword library, buyer-question evidence or product truth.

Product truth gates all three layers. A competitor question such as “Is it child-safe?” establishes a concern, not proof that the focal product is child-safe.

## Keyword routing

Do not use a rigid `tier 1 = title, tier 2/3 = bullets, tier 4 = backend` formula. Use that only as a starting tendency. Route each term using, in order:

1. focal-product relevance and factual applicability;
2. search-demand priority / traffic tier;
3. purchase intent versus browse intent;
4. competitor organic-rank/coverage evidence when supplied;
5. root precision and semantic role;
6. existing coverage in the Listing;
7. natural language and readability in the target locale.

Prefer high relevance over raw traffic, precise purchase intent over broad browsing traffic, and natural local-language phrasing over forced exact repetition.

### Coverage states

Audit important terms using these states:

- `exact`: the important phrase appears naturally as supplied.
- `close_variant`: a natural grammatical/orthographic variant preserves the same shopping intent.
- `semantic_root`: the important entities/roots and meaning are expressed, but the phrase is not treated as exact coverage.
- `backend`: intentionally covered only in Generic Keywords/Search Terms.
- `uncovered`: no meaningful coverage.
- `not_applicable`: unsuitable for the focal product.

For compound-heavy languages such as German, do not claim that separated roots are equivalent to exact compound coverage. If a high-value precise compound matters and reads naturally, use the exact compound or a natural close variant. Never manufacture awkward phrases only to force roots together.

## Alexa/Rufus and conversational coverage

Treat shopping-assistant questions as **answer-coverage evidence**, not as keywords to stuff and not as an official ranking/recommendation score.

For supplied competitor questions:

- normalize near-duplicate questions into buyer concerns while retaining raw frequency;
- separate platform/service questions (price alerts, returns, review summaries) from product-content questions;
- prioritize recurring concerns such as size/fit, assembly, material, structure/capacity, cleaning, mobility, stability or compatibility when the data supports them;
- map each relevant concern to verified product facts and the best available field;
- hold any answer that requires missing evidence;
- use natural declarative copy to answer the concern even when seller-authored Q&A is unavailable;
- never promise that phrase coverage will win Alexa/Rufus recommendation. The goal is clearer, more complete and more answerable product information.

A question-frequency count is a within-dataset concern signal only. Do not compare it directly with ABA/search volume.

## Frontend/backend complementarity

- Frontend copy should communicate the product clearly and answer high-value buyer needs, not read like a keyword list.
- Backend terms should complement rather than blindly duplicate strong frontend coverage.
- Exclude competitor brands, ASINs, irrelevant terms and unsupported attributes from Generic Keywords.
- Count Generic Keywords in UTF-8 bytes. Umlauts and other non-ASCII characters can consume multiple bytes.
- Do not use supplemental AI/plugin roots solely because they exist; first validate relevance against Search Demand and Product Truth.

## A+ and rich content

For each A+ module specify job, buyer question, message, image concept, proof, mobile safe area, dependency and status. Use A+ to deepen scenarios, comparisons, structure and trust rather than repeating the title and bullets.

## JSON aliases

Use `title`, `item_highlights`, `bullets`, `description`, `a_plus_brief`, `search_terms`, and `qa` when the fields exist, plus shared evidence/routing objects such as `keyword_placement`, `keyword_coverage`, `question_library`, `buyer_concern_coverage`, `claims`, and `policy_profile`.

See [../assets/listing-output.sample.json](../assets/listing-output.sample.json) for the fictional Amazon-shaped example.
