# Amazon Platform Route

Verify current category rules and limits in Seller Central or authoritative Amazon documentation.

## Fields

- Title.
- Five bullets unless the live template differs.
- Product description.
- A+ brief when available and in scope.
- Backend Search Terms when exposed.
- 8–12 natural-language shopping Q&As or intent answers when requested.

## Decisions

- Resolve ASIN/variation relationships and exclude competitor brands/ASINs.
- Make frontend and backend keyword placement complementary.
- Count Search Terms in UTF-8 bytes and verify the live limit.
- Treat Alexa/Rufus-style questions as conversational coverage, not an official score or guaranteed recommendation.
- For each A+ module specify job, buyer question, message, image concept, proof, mobile safe area, dependency and status.

## JSON aliases

Use `title`, `bullets`, `description`, `a_plus_brief`, `search_terms`, and `qa`, plus shared evidence/routing objects.

See [../assets/listing-output.sample.json](../assets/listing-output.sample.json) for the fictional Amazon-shaped example.
