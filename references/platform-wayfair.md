# Wayfair Platform Route

Verify the live supplier-portal category template, required attributes, enumerated values, variation rules and field limits. Public competitor pages show presentation conventions, not the exact editable schema.

## Category and positioning

- Choose one primary category from the product's dominant job and construction.
- Preserve adjacent category language as secondary intent only when accurate.
- Do not let a secondary keyword redefine the product type.

## Fields

Produce fields supported by the live template, typically:

- Product Name/title.
- About This Product.
- Features; do not assume Amazon's five-bullet rule unless requested or required.
- What's Included.
- Product Dimensions and category-specific measurements.
- Structured Details: material, configuration, finish, assembly, care, weight/capacity, safety, certification, warranty and origin when applicable.
- Variation/option mapping and variant-specific assets.
- Image/rich-content brief.
- Buyer-question/Shop with AI intent coverage routed across copy, attributes and images. Publish Q&A only if the supplier experience exposes it.

Wayfair does not publicly expose an Amazon-style backend Search Terms field as a universal component. Create `discovery_terms` internally and use it only in an applicable supplier field.

## Product Name

- Sequence primary product term, supported differentiator, important configuration/quantity, secondary function and room/use case.
- Use multiple useful generic phrases when readable and allowed.
- Avoid noun-chain stuffing, competitor brands, unsupported attributes and synonyms that add no meaning.
- Report character count and priority terms. Treat a user-supplied limit as user-provided until verified live.

## Communication jobs

- About This Product: concise role, differentiation, fit and major configuration.
- Features: distinct jobs; do not repeat the same component inventory across consecutive features.
- Structured attributes: exact facts/enumerated values, not promotional paraphrases.
- Images/rich content: visually answer fit, configuration, operation and comparison questions without unsupported badges.

## Furniture, variations and assets

- Keep assembled, component and carton measurements separate; distinguish net weight, gross carton weight and weight capacity.
- Use inches/pounds for US customer fields while preserving verified source units.
- When an unusual, modular or changeable shape makes standard dimension labels ambiguous, confirm live category mapping instead of inventing width/depth semantics. This is conditional, not a universal priority.
- Confirm parent/child logic, supplier SKU/part number/GTIN and which facts vary.
- Require a real finish name, identifier and matching assets for every selectable option.
- Keep shared parent copy option-neutral and isolate option-specific facts.
- Check swatches, diagrams, lifestyle images, documents and variant linkage against the live template.

## Shop with AI coverage

Use shopping-assistant answers and VOC to order information by relevant practical concerns such as fit, configuration, access/usability, material/durability, safety, assembly/care and room/aesthetic fit.

- Answer verified questions across Product Name, About, Features, attributes and images.
- Hold unanswered questions with evidence tasks.
- Do not invent a score, guarantee inclusion or assume seller-authored Q&A exists.

## JSON aliases

Use `product_name`, `about_this_product`, `features`, `whats_included`, `dimensions`, `structured_details`, `variations`, `media_brief`, `discovery_terms`, and `conversational_coverage`, plus shared evidence/routing objects.

Use `published_qa` only when a real customer-facing Q&A field exists. See [../assets/listing-output.wayfair.sample.json](../assets/listing-output.wayfair.sample.json) for the schema-only fictional example.
