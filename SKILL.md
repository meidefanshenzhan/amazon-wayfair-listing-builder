---
name: amazon-wayfair-listing-builder
description: Use when building, rewriting, localizing, or auditing Amazon or Wayfair product listings from verified product facts, keywords, competitor findings, reviews, VOC, or shopping-assistant questions.
---

# Amazon and Wayfair Listing Builder

Build platform-native product content from evidence, not adjectives. Share the evidence model across marketplaces; never force one marketplace's fields or rules onto another.

## Choose the platform first

Identify `platform`, marketplace, language, category, product type and variation structure before drafting.

- For Amazon, read [references/platform-amazon.md](references/platform-amazon.md).
- For Wayfair, read [references/platform-wayfair.md](references/platform-wayfair.md).
- If the target platform is unclear, establish it before producing customer-facing fields.

Read only the selected platform reference. Always use [references/workflow.md](references/workflow.md) for shared schemas and [references/compliance-and-quality.md](references/compliance-and-quality.md) before final delivery.

## Keep the boundary narrow

- Consume upstream keyword, traffic, review, VOC, competitor and product-evidence outputs when available.
- Do not turn a Listing build into deep traffic, advertising, market-sizing or review-frequency analysis.
- When upstream analysis is absent, normalize only what is needed to draft truthfully.
- Mark unknown facts `DATA_MISSING`; mark plausible but unverified judgments `ASSUMPTION`.
- Preserve commercially useful unsupported terms as `evidence_pending`; do not convert them into customer-facing claims.
- Competitor listings and reviews may identify buyer questions and category conventions, but cannot prove the focal product's material, dimensions, performance, safety, assembly experience or certification.

Read [references/data-and-tools.md](references/data-and-tools.md) when raw product IDs, marketplace pages, exports or research tools must fill minimum inputs.

## Choose the mode

- **Full build:** all shared deliverables plus the selected platform's customer-facing fields.
- **Module build:** one field/module plus the minimum placement and evidence decisions supporting it.
- **Audit and rewrite:** compare current and proposed content with exact field actions.
- **Audit only:** identify issues and actions without silently rewriting.
- **Localization:** rebuild for the target marketplace and language; do not translate mechanically.

## Establish the input contract

Collect or infer platform, marketplace, language, category, brand, product type, variations, verified facts, included components, dimensions, materials, use boundaries, care, assembly, warranty, certifications, target buyer, primary job, use cases, differentiation, current fields, keyword priorities, buyer questions and requested outputs.

Use [assets/listing-brief.sample.json](assets/listing-brief.sample.json) when structured input helps. Never invent specifications, tests, certifications, market metrics, platform limits or buyer evidence.

## Produce the shared deliverables

1. Input summary.
2. Keyword placement table.
3. Buyer-question library.
4. Claim-and-expression table.
5. Platform-native Listing package.
6. Field-level execution changes.
7. Structured JSON.
8. Audit report.

The Listing package follows the selected platform reference. Amazon Search Terms/A+ are not Wayfair defaults; Wayfair structured attributes and supplier fields are not Amazon defaults.

## Apply evidence without discarding opportunity

- Use verified claims and carefully bounded observed claims.
- Connect each `evidence_pending` opportunity to a proof task and affected field.
- Treat missing proof as unknown, not as evidence of failure.
- Keep internal statuses and hold instructions out of customer-facing copy.
- Isolate competitor brands and marketplace-specific identifiers while retaining relevant generic language.
- Use `P0` only when unsupported/high-risk copy remains, a required fact conflicts, a trademark/field-rule issue blocks publication, or the chosen category requires missing evidence.
- Use `P1` when proof would unlock stronger content but a safe version can publish without it.

## Validate and deliver

Save normalized JSON with a top-level `platform` value of `amazon` or `wayfair`, then run:

```bash
python scripts/audit_listing.py path/to/listing.json --report path/to/audit_report.md
```

The script is a deterministic preflight, not marketplace approval or legal advice. Verify current platform/category rules in the seller or supplier portal when they affect the output. Require human review for factual accuracy, safety/compliance, trademarks, variations, required attributes and live field limits.

For a full build, deliver eight files: `input_summary.md`, `keyword_placement.md`, `question_library.md`, `claim_expression.md`, `listing_package.md`, `execution_changes.md`, `listing_output.json`, and `audit_report.md`.

End with executable-now actions, evidence/product decisions, true `P0` blockers and required human/platform verification. Do not claim readiness while a true `P0` remains.

