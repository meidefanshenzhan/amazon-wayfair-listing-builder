#!/usr/bin/env python3
"""Deterministic preflight for normalized Amazon or Wayfair Listing JSON."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


RISK_PATTERNS = {
    "absolute_or_guarantee": r"\b(100%|always|never|guaranteed|lifetime|forever)\b",
    "superiority_or_rank": r"(?:\b(best|ultimate|top[- ]rated)\b|#\s*1)",
    "medical": r"\b(cure[sd]?|treat[sd]?|prevent[sd]?|heal[sd]?|diagnos(?:e|es|ed))\b",
    "safety": r"\b(non[- ]?toxic|child[- ]?safe|fireproof|waterproof|completely safe)\b",
    "environmental": r"\b(eco[- ]?friendly|biodegradable|sustainable|green product)\b",
    "certification": r"\b(FDA approved|certified organic|clinically proven)\b",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Audit Listing structure, counts, keyword coverage, and review-trigger phrases."
    )
    parser.add_argument("input", type=Path, help="Normalized Listing JSON")
    parser.add_argument("--report", type=Path, help="Write a Markdown report")
    parser.add_argument(
        "--title-limit",
        type=int,
        default=None,
        help="Optional verified marketplace/category title character limit",
    )
    parser.add_argument(
        "--item-highlights-limit",
        type=int,
        default=None,
        help="Optional verified Amazon Item Highlights character limit",
    )
    parser.add_argument(
        "--search-terms-byte-limit",
        type=int,
        default=None,
        help="Optional verified backend Search Terms UTF-8 byte limit",
    )
    return parser.parse_args()


def require_type(value: Any, expected: type, label: str) -> Any:
    if not isinstance(value, expected):
        raise ValueError(f"{label} must be {expected.__name__}")
    return value


def text_fields(data: dict[str, Any]) -> dict[str, str]:
    platform = str(data.get("platform", "amazon")).casefold()
    bullets = require_type(data.get("bullets", data.get("features", [])), list, "bullets/features")
    qa = require_type(
        data.get("qa", []) if platform == "amazon" else data.get("published_qa", []),
        list,
        "qa/published_qa",
    )
    qa_text = " ".join(
        f"{item.get('question', '')} {item.get('answer', '')}"
        for item in qa
        if isinstance(item, dict)
    )
    return {
        "title": str(data.get("title", data.get("product_name", ""))),
        "item_highlights": str(data.get("item_highlights", "")),
        "bullets": " ".join(str(item) for item in bullets),
        "description": str(data.get("description", data.get("about_this_product", ""))),
        "search_terms": str(data.get("search_terms", data.get("discovery_terms", ""))),
        "qa": qa_text,
    }


def normalize_phrase(value: str) -> str:
    return re.sub(r"\s+", " ", value.casefold()).strip()


def claim_is_present(claim: dict[str, Any], normalized_copy: str) -> bool:
    """Best-effort check; human review must catch paraphrases."""
    if claim.get("used_in_customer_copy") is True:
        return True
    terms = claim.get("copy_terms")
    if not isinstance(terms, list):
        terms = [claim.get("text", "")]
    return any(
        normalized_term and normalized_term in normalized_copy
        for term in terms
        if (normalized_term := normalize_phrase(str(term)))
    )


def audit(data: dict[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    platform = str(data.get("platform", "amazon")).casefold()
    if platform not in {"amazon", "wayfair"}:
        raise ValueError("platform must be `amazon` or `wayfair`")
    fields = text_fields(data)
    all_frontend = " ".join(
        fields[name] for name in ("title", "item_highlights", "bullets", "description", "qa")
    )
    all_copy = f"{all_frontend} {fields['search_terms']}"
    required_keywords = require_type(
        data.get("required_keywords", []), list, "required_keywords"
    )
    claims = require_type(data.get("claims", []), list, "claims")
    keyword_placement = require_type(
        data.get("keyword_placement", []), list, "keyword_placement"
    )
    execution_changes = require_type(
        data.get("execution_changes", []), list, "execution_changes"
    )
    question_library = require_type(
        data.get("question_library", []), list, "question_library"
    )

    coverage = []
    normalized_copy = normalize_phrase(all_copy)
    for keyword in required_keywords:
        keyword_text = str(keyword).strip()
        if not keyword_text:
            continue
        locations = [
            name
            for name, content in fields.items()
            if normalize_phrase(keyword_text) in normalize_phrase(content)
        ]
        coverage.append(
            {
                "keyword": keyword_text,
                "covered": bool(locations),
                "locations": locations,
            }
        )

    risks = []
    for label, pattern in RISK_PATTERNS.items():
        for match in re.finditer(pattern, all_copy, flags=re.IGNORECASE):
            risks.append(
                {
                    "type": label,
                    "term": match.group(0),
                    "status": "human_review_required",
                }
            )

    missing_evidence = []
    evidence_opportunities = []
    unsupported_claims_in_copy = []
    for index, claim in enumerate(claims, start=1):
        if not isinstance(claim, dict):
            missing_evidence.append(f"claim[{index}] is not an object")
            continue
        evidence = str(claim.get("evidence", "")).strip()
        status = str(claim.get("status", "")).casefold()
        claim_text = str(claim.get("text", f"claim[{index}]"))
        needs_evidence = (
            not evidence
            or evidence == "DATA_MISSING"
            or status in {"blocked", "assumption", "evidence_pending"}
        )
        present_in_copy = claim_is_present(claim, normalized_copy)
        if needs_evidence:
            missing_evidence.append(claim_text)
            if present_in_copy:
                unsupported_claims_in_copy.append(claim_text)
            else:
                evidence_opportunities.append(claim_text)
        elif status == "prohibited" and present_in_copy:
            unsupported_claims_in_copy.append(claim_text)

    issues = []
    bullets = require_type(data.get("bullets", data.get("features", [])), list, "bullets/features")
    qa = require_type(
        data.get("qa", []) if platform == "amazon" else data.get("published_qa", []),
        list,
        "qa/published_qa",
    )
    if platform == "amazon":
        if len(bullets) != 5:
            issues.append(f"Expected 5 Amazon bullets; found {len(bullets)}.")
        if qa and not 8 <= len(qa) <= 12:
            issues.append(f"Expected 8–12 Amazon Q&A items when supplied; found {len(qa)}.")
    else:
        if not fields["title"].strip():
            issues.append("Wayfair Product Name is missing.")
        if not fields["description"].strip():
            issues.append("Wayfair About This Product is missing.")
        if not bullets:
            issues.append("Wayfair Features are missing or empty.")
    if "DATA_MISSING" in all_copy:
        issues.append("Customer-facing copy contains DATA_MISSING.")
    if "ASSUMPTION" in all_copy:
        issues.append("Customer-facing copy contains ASSUMPTION.")

    allowed_placement_statuses = {
        "use",
        "qualified_use",
        "evidence_pending",
        "brand_isolate",
        "irrelevant",
    }
    for index, item in enumerate(keyword_placement, start=1):
        if not isinstance(item, dict):
            issues.append(f"keyword_placement[{index}] is not an object.")
            continue
        status = str(item.get("status", ""))
        if status not in allowed_placement_statuses:
            issues.append(
                f"keyword_placement[{index}] has invalid status `{status or 'missing'}`."
            )
        coverage_state = str(item.get("coverage_state", ""))
        allowed_coverage_states = {"exact", "close_variant", "semantic_root", "backend", "uncovered", "not_applicable", ""}
        if coverage_state not in allowed_coverage_states:
            issues.append(
                f"keyword_placement[{index}] has invalid coverage_state `{coverage_state}`."
            )

    allowed_priorities = {"P0", "P1", "P2"}
    allowed_answer_statuses = {"answerable", "evidence_pending", "irrelevant"}
    allowed_publish_statuses = {"publish", "hold"}
    qa_questions = {
        normalize_phrase(str(item.get("question", "")))
        for item in qa
        if isinstance(item, dict) and str(item.get("question", "")).strip()
    }
    question_routing = {
        "total": len(question_library),
        "answerable": 0,
        "evidence_pending": 0,
        "irrelevant": 0,
        "publish": 0,
        "hold": 0,
    }
    if not question_library:
        issues.append("Buyer question library is missing or empty.")
    for index, item in enumerate(question_library, start=1):
        if not isinstance(item, dict):
            issues.append(f"question_library[{index}] is not an object.")
            continue
        priority = str(item.get("priority", ""))
        answer_status = str(item.get("answer_status", ""))
        publish_status = str(item.get("publish_status", ""))
        question = str(item.get("question", "")).strip()
        current_answer = str(item.get("current_answer", "")).strip()
        evidence_needed = str(item.get("evidence_needed", "")).strip()
        best_placement = item.get("best_placement", [])
        if priority not in allowed_priorities:
            issues.append(
                f"question_library[{index}] has invalid priority `{priority or 'missing'}`."
            )
        if answer_status not in allowed_answer_statuses:
            issues.append(
                "question_library["
                f"{index}] has invalid answer_status `{answer_status or 'missing'}`."
            )
        else:
            question_routing[answer_status] += 1
        if publish_status not in allowed_publish_statuses:
            issues.append(
                "question_library["
                f"{index}] has invalid publish_status `{publish_status or 'missing'}`."
            )
        else:
            question_routing[publish_status] += 1
        if not question:
            issues.append(f"question_library[{index}] is missing a buyer question.")
        if not isinstance(best_placement, list) or not best_placement:
            issues.append(f"question_library[{index}] is missing best_placement.")
        if answer_status == "evidence_pending":
            if publish_status != "hold":
                issues.append(
                    f"question_library[{index}] is evidence_pending but not held."
                )
            if not evidence_needed:
                issues.append(
                    f"question_library[{index}] is evidence_pending but lacks evidence_needed."
                )
        if publish_status == "publish":
            if answer_status != "answerable":
                issues.append(
                    f"question_library[{index}] is publishable but not answerable."
                )
            if not current_answer:
                issues.append(
                    f"question_library[{index}] is publishable but lacks current_answer."
                )
        if answer_status == "irrelevant" and publish_status != "hold":
            issues.append(f"question_library[{index}] is irrelevant but not held.")
        if publish_status == "hold" and normalize_phrase(question) in qa_questions:
            issues.append(
                "Held buyer question appears in customer-facing Q&A: "
                f"{question}"
            )

    for index, action in enumerate(execution_changes, start=1):
        if not isinstance(action, dict):
            issues.append(f"execution_changes[{index}] is not an object.")
            continue
        priority = str(action.get("priority", ""))
        if priority not in allowed_priorities:
            issues.append(
                f"execution_changes[{index}] has invalid priority `{priority or 'missing'}`."
            )
        if not str(action.get("field", "")).strip():
            issues.append(f"execution_changes[{index}] is missing a Listing field.")
        if not str(action.get("exact_action", "")).strip():
            issues.append(f"execution_changes[{index}] is missing an exact action.")

    title_chars = len(fields["title"])
    item_highlights_chars = len(fields["item_highlights"])
    search_terms_bytes = len(fields["search_terms"].encode("utf-8"))
    if args.title_limit is not None and title_chars > args.title_limit:
        issues.append(
            f"Title has {title_chars} characters, above supplied limit {args.title_limit}."
        )
    if (
        platform == "amazon"
        and args.item_highlights_limit is not None
        and item_highlights_chars > args.item_highlights_limit
    ):
        issues.append(
            f"Item Highlights has {item_highlights_chars} characters, above supplied limit {args.item_highlights_limit}."
        )
    if (
        platform == "amazon"
        and args.search_terms_byte_limit is not None
        and search_terms_bytes > args.search_terms_byte_limit
    ):
        issues.append(
            "Search Terms use "
            f"{search_terms_bytes} UTF-8 bytes, above supplied limit "
            f"{args.search_terms_byte_limit}."
        )

    covered_count = sum(1 for item in coverage if item["covered"])
    verified_claim_terms = []
    for claim in claims:
        if not isinstance(claim, dict) or str(claim.get("status", "")).casefold() != "verified":
            continue
        terms = claim.get("copy_terms")
        if not isinstance(terms, list):
            terms = [claim.get("text", "")]
        verified_claim_terms.extend(normalize_phrase(str(term)) for term in terms)

    unverified_risk_hits = []
    for risk in risks:
        risk_term = normalize_phrase(risk["term"])
        if not any(risk_term in term for term in verified_claim_terms if term):
            unverified_risk_hits.append(risk["term"])

    publish_blockers = list(issues)
    publish_blockers.extend(
        f"Unsupported declared claim appears in customer-facing copy: {item}"
        for item in unsupported_claims_in_copy
    )
    publish_blockers.extend(
        f"High-risk phrase lacks a matching verified claim declaration: {item}"
        for item in unverified_risk_hits
    )
    publish_blockers = list(dict.fromkeys(publish_blockers))
    return {
        "platform": platform,
        "counts": {
            "title_characters": title_chars,
            "item_highlights_characters": item_highlights_chars,
            "bullet_count": len(bullets),
            "description_characters": len(fields["description"]),
            "search_terms_utf8_bytes": search_terms_bytes,
            "qa_count": len(qa),
            "conversational_coverage_count": len(
                data.get("conversational_coverage", [])
                if isinstance(data.get("conversational_coverage", []), list)
                else []
            ),
        },
        "keyword_coverage": {
            "covered": covered_count,
            "required": len(coverage),
            "items": coverage,
        },
        "risk_phrase_hits": risks,
        "claims_missing_evidence": missing_evidence,
        "publish_blockers": publish_blockers,
        "evidence_opportunities": evidence_opportunities,
        "buyer_question_routing": question_routing,
        "execution_change_count": len(execution_changes),
        "structural_issues": issues,
        "disclaimer": (
            f"Deterministic preflight only. Verify current {platform.title()} "
            "marketplace/category rules and obtain human compliance review."
        ),
    }


def markdown_report(result: dict[str, Any], source: Path) -> str:
    counts = result["counts"]
    coverage = result["keyword_coverage"]
    if result["platform"] == "wayfair":
        field_lines = [
            f"- Product Name characters: {counts['title_characters']}",
            f"- Features: {counts['bullet_count']}",
            f"- About This Product characters: {counts['description_characters']}",
            f"- Discovery terms UTF-8 bytes: {counts['search_terms_utf8_bytes']}",
            f"- Published Q&A items: {counts['qa_count']}",
            f"- Internal conversational coverage items: {counts['conversational_coverage_count']}",
        ]
    else:
        field_lines = [
            f"- Title characters: {counts['title_characters']}",
            f"- Item Highlights characters: {counts['item_highlights_characters']}",
            f"- Bullets: {counts['bullet_count']}",
            f"- Description characters: {counts['description_characters']}",
            f"- Search Terms UTF-8 bytes: {counts['search_terms_utf8_bytes']}",
            f"- Q&A items: {counts['qa_count']}",
        ]
    lines = [
        f"# {result['platform'].title()} Listing Preflight",
        "",
        f"- Source: `{source}`",
    ]
    lines.extend(field_lines)
    lines.extend(
        [
            f"- Required keyword coverage: {coverage['covered']}/{coverage['required']}",
            "",
            "## P0 publish blockers",
            "",
        ]
    )
    issues = result["publish_blockers"]
    lines.extend(f"- {item}" for item in issues) if issues else lines.append("- None detected.")
    lines.extend(["", "## Keyword coverage", ""])
    for item in coverage["items"]:
        status = "covered" if item["covered"] else "missing"
        locations = ", ".join(item["locations"]) or "—"
        lines.append(f"- `{item['keyword']}`: {status}; locations: {locations}")
    lines.extend(["", "## Risk phrases requiring human review", ""])
    risks = result["risk_phrase_hits"]
    if risks:
        lines.extend(f"- {item['type']}: `{item['term']}`" for item in risks)
    else:
        lines.append("- None detected by the built-in patterns.")
    routing = result["buyer_question_routing"]
    lines.extend(
        [
            "",
            "## Buyer question routing",
            "",
            f"- Total questions: {routing['total']}",
            f"- Answerable: {routing['answerable']}",
            f"- Evidence pending: {routing['evidence_pending']}",
            f"- Irrelevant: {routing['irrelevant']}",
            f"- Publish: {routing['publish']}",
            f"- Hold: {routing['hold']}",
        ]
    )
    lines.extend(["", "## Evidence opportunities not used in copy", ""])
    opportunities = result["evidence_opportunities"]
    if opportunities:
        lines.extend(f"- {item}" for item in opportunities)
    else:
        lines.append("- None declared.")
    lines.extend(["", "## All claims missing evidence", ""])
    missing = result["claims_missing_evidence"]
    lines.extend(f"- {item}" for item in missing) if missing else lines.append("- None declared.")
    lines.extend(
        [
            "",
            "## Execution changes",
            "",
            f"- Declared field-level actions: {result['execution_change_count']}",
        ]
    )
    lines.extend(["", "## Limitation", "", result["disclaimer"], ""])
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    try:
        data = json.loads(args.input.read_text(encoding="utf-8"))
        require_type(data, dict, "root")
        result = audit(data, args)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(markdown_report(result, args.input), encoding="utf-8")
        print(args.report)
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
