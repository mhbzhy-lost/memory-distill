import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from bs4 import BeautifulSoup
from markdown_it import MarkdownIt
from soupsieve.util import SelectorSyntaxError

from recipe_importer.storage import read_json, write_json, write_text

NOISE_TAGS = {
    "aside",
    "footer",
    "header",
    "nav",
    "noscript",
    "script",
    "style",
    "svg",
    "template",
}

NOISE_ROLES = {
    "banner",
    "complementary",
    "contentinfo",
    "navigation",
    "search",
}

NOISE_ATTR_MARKERS = (
    "breadcrumb",
    "docs-nav",
    "menu",
    "mobile-nav",
    "navigation",
    "page-nav",
    "pagination",
    "side-nav",
    "sidebar",
    "table-of-contents",
    "toc",
)

CONTENT_ATTR_MARKERS = (
    "doc-content",
    "docs-content",
    "markdown",
    "mdx",
    "prose",
    "styled-markdown-content",
)

HINT_STOPWORDS = {
    "and",
    "are",
    "for",
    "from",
    "has",
    "into",
    "not",
    "that",
    "the",
    "this",
    "with",
    "you",
}

DEFAULT_STRUCTURED_TEXT_PATHS = (
    "__NEXT_DATA__.props.pageProps.errorMessage",
)

TEXT_TAGS = ("h1", "h2", "h3", "p", "li", "pre", "code")


@dataclass(frozen=True)
class ExtractionResult:
    source_id: str
    section_count: int


def normalize_space(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def quote_hash(text: str) -> str:
    return "sha256:" + hashlib.sha256(normalize_space(text).encode("utf-8")).hexdigest()


def attr_text(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, list):
        return " ".join(str(item) for item in value)
    return str(value)


def contains_content_landmark(element: object) -> bool:
    name = getattr(element, "name", None)
    if name in {"article", "main"}:
        return True

    find = getattr(element, "find", None)
    if not callable(find):
        return False
    return find(["article", "main"]) is not None


def attr_marker_text(element: object) -> str:
    attrs = getattr(element, "attrs", {}) or {}
    return " ".join(
        [
            attr_text(attrs.get("class")),
            attr_text(attrs.get("id")),
            attr_text(attrs.get("data-testid")),
            attr_text(attrs.get("aria-label")),
        ]
    ).lower()


def is_noise_node(element: object) -> bool:
    name = getattr(element, "name", None)
    if name in NOISE_TAGS:
        return True

    attrs = getattr(element, "attrs", {}) or {}
    if attrs.get("hidden") is not None:
        return True
    if attr_text(attrs.get("aria-hidden")).lower() == "true":
        return True

    role = attr_text(attrs.get("role")).lower()
    if role in NOISE_ROLES:
        return True

    marker_text = attr_marker_text(element)
    if not any(marker in marker_text for marker in NOISE_ATTR_MARKERS):
        return False
    return not contains_content_landmark(element)


def remove_noise_nodes(soup: BeautifulSoup) -> None:
    for element in list(soup.find_all(True)):
        if is_noise_node(element):
            element.decompose()


def find_content_container(root: object) -> object | None:
    find_all = getattr(root, "find_all", None)
    if not callable(find_all):
        return None
    for element in find_all(True):
        marker_text = attr_marker_text(element)
        if any(marker in marker_text for marker in CONTENT_ATTR_MARKERS):
            return element
    return None


def content_root(soup: BeautifulSoup) -> object:
    main = soup.find("main") or soup.body or soup
    return main.find("article") or find_content_container(main) or main


def profile(metadata: dict[str, object]) -> dict[str, Any]:
    raw_profile = metadata.get("extraction_profile", {})
    return raw_profile if isinstance(raw_profile, dict) else {}


def configured_content_root(soup: BeautifulSoup, metadata: dict[str, object]) -> object:
    for selector in profile(metadata).get("content_selectors", []):
        if not isinstance(selector, str):
            continue
        try:
            selected = soup.select_one(selector)
        except SelectorSyntaxError:
            continue
        if selected is not None:
            return selected
    return content_root(soup)


def short_text(text: str, limit: int = 220) -> str:
    normalized = normalize_space(text)
    if len(normalized) <= limit:
        return normalized
    return normalized[: limit - 3].rstrip() + "..."


def match_tokens(text: str) -> set[str]:
    spaced = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", text)
    tokens = set(re.findall(r"[a-z0-9]+", spaced.lower()))
    return {token for token in tokens if len(token) >= 3 and token not in HINT_STOPWORDS}


def has_keyword_match(hint: str, section_text: str) -> bool:
    hint_tokens = match_tokens(hint)
    if len(hint_tokens) < 2:
        return False
    section_tokens = match_tokens(section_text)
    matched = hint_tokens & section_tokens
    threshold = max(2, (len(hint_tokens) * 3 + 4) // 5)
    return len(matched) >= threshold


def matched_hint_sections(hint: str, sections: list[dict[str, str]]) -> list[dict[str, str]]:
    needle = hint.lower()
    exact_matches = [section for section in sections if needle in section["text"].lower()]
    if exact_matches:
        return exact_matches
    return [section for section in sections if has_keyword_match(hint, section["text"])]


def qa_gate(metadata: dict[str, object], sections: list[dict[str, str]]) -> dict[str, Any]:
    current_profile = profile(metadata)
    hints = [str(hint).strip() for hint in metadata.get("expected_failure_hints", []) if str(hint).strip()]
    build_hints = [str(hint).strip() for hint in metadata.get("expected_build_hints", []) if str(hint).strip()]
    min_sections = int(current_profile.get("min_sections", 1))
    max_sections = int(current_profile.get("max_sections", 500))
    require_expected_hints = bool(current_profile.get("require_expected_hints", True))
    allow_agentic_fallback = bool(current_profile.get("agentic_fallback", True))

    checks: list[dict[str, Any]] = [
        {
            "name": "sections_non_empty",
            "passed": len(sections) > 0,
            "details": f"抽取段落数: {len(sections)}",
        },
        {
            "name": "section_count_within_bounds",
            "passed": min_sections <= len(sections) <= max_sections,
            "details": f"期望范围: {min_sections}-{max_sections}",
        },
    ]

    if hints and require_expected_hints:
        matched = [hint for hint in hints if matched_hint_sections(hint, sections)]
        checks.append(
            {
                "name": "expected_hints_matched",
                "passed": bool(matched),
                "details": f"命中 {len(matched)}/{len(hints)} 条 expected_failure_hints",
                "matched_hints": matched,
                "missing_hints": [hint for hint in hints if hint not in matched],
            }
        )

    if build_hints and require_expected_hints:
        matched_build = [hint for hint in build_hints if matched_hint_sections(hint, sections)]
        checks.append(
            {
                "name": "expected_build_hints_matched",
                "passed": bool(matched_build),
                "details": f"命中 {len(matched_build)}/{len(build_hints)} 条 expected_build_hints",
                "matched_hints": matched_build,
                "missing_hints": [hint for hint in build_hints if hint not in matched_build],
            }
        )

    passed = all(bool(check["passed"]) for check in checks)
    status = "passed" if passed else "needs_agentic_fallback" if allow_agentic_fallback else "failed"
    return {
        "source_id": metadata["source_id"],
        "status": status,
        "checks": checks,
        "fallback": {
            "mode": "agentic_loop",
            "enabled": allow_agentic_fallback and not passed,
            "inputs": ["raw.html", "response.json", "sections.json", "review.md"],
            "instruction": (
                "读取 raw.html、response.json、sections.json、review.md，"
                "产出最小 extraction_profile 或 extractor patch，并补回归测试。"
            ),
        },
    }


def render_qa_gate(qa: dict[str, Any]) -> list[str]:
    status_label = {
        "passed": "通过",
        "needs_agentic_fallback": "需要 agentic fallback",
        "failed": "失败",
    }.get(str(qa["status"]), str(qa["status"]))

    lines = [
        "## QA 闸门",
        f"- 状态: {status_label}",
    ]
    for check in qa["checks"]:
        result = "通过" if check["passed"] else "失败"
        lines.append(f"- {check['name']}: {result}；{check['details']}")

    fallback = qa.get("fallback", {})
    if fallback.get("enabled"):
        lines.extend(
            [
                "- fallback: 启动 agentic loop",
                f"- fallback 输入: {', '.join(fallback.get('inputs', []))}",
                f"- fallback 要求: {fallback.get('instruction', '')}",
            ]
        )
    return lines


def render_review(metadata: dict[str, object], sections: list[dict[str, str]], qa: dict[str, Any]) -> str:
    source_id = str(metadata["source_id"])
    hints = [str(hint).strip() for hint in metadata.get("expected_failure_hints", []) if str(hint).strip()]
    stacks = [str(stack) for stack in metadata.get("stacks", [])]

    lines = [
        f"# 快照人审：{source_id}",
        "",
        "## 快照质量检查",
        f"- 来源 URL: {metadata.get('url', '')}",
        f"- 最终 URL: {metadata.get('final_url', '')}",
        f"- 来源类型: {metadata.get('source_type', '')}",
        f"- 采集时间: {metadata.get('captured_at', '')}",
        f"- HTTP 状态: {metadata.get('retrieved_status', '')}",
        f"- 内容哈希: {metadata.get('content_hash', '')}",
        f"- 技术栈: {', '.join(stacks) if stacks else '未记录'}",
        f"- 抽取段落数: {len(sections)}",
        "",
    ]
    lines.extend(render_qa_gate(qa))
    lines.extend(["", "## 预期线索命中"])

    if hints:
        for hint in hints:
            matches = matched_hint_sections(hint, sections)
            if not matches:
                lines.append(f"- `{hint}`：未找到直接段落命中")
                continue
            lines.append(f"- `{hint}`")
            for section in matches[:3]:
                lines.append(f"  - [{section['span_id']}] {short_text(section['text'])}")
    else:
        lines.append("- `response.json` 未记录 `expected_failure_hints`。")

    lines.extend(
        [
            "",
            "## 段落样例",
        ]
    )
    if sections:
        for section in sections[:8]:
            lines.append(f"- [{section['span_id']}] {short_text(section['text'])}")
    else:
        lines.append("- 未抽取到段落。")

    lines.extend(
        [
            "",
            "## 审阅决策",
            "- [ ] 批准用于 recipe 生成",
            "- [ ] 需要改进抽取过滤",
            "- [ ] 拒绝该 source",
            "",
            "## 审阅备注",
            "- ",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def should_extract_element(element: object) -> bool:
    name = getattr(element, "name", None)
    if name == "code":
        parent = getattr(element, "parent", None)
        parent_name = getattr(parent, "name", None)
        if parent_name == "pre":
            return False
        if parent_name in {"p", "li", "h1", "h2", "h3"}:
            return False
    return True


def append_unique_text(texts: list[str], seen: set[str], text: str) -> None:
    normalized = normalize_space(text)
    if not normalized:
        return
    key = normalized.lower()
    if key in seen:
        return
    seen.add(key)
    texts.append(normalized)


def script_json_payloads(soup: BeautifulSoup) -> dict[str, Any]:
    payloads: dict[str, Any] = {}
    for script in soup.find_all("script"):
        script_id = attr_text(script.get("id"))
        if not script_id:
            continue
        text = script.string or script.get_text()
        if not text or not text.strip():
            continue
        try:
            payloads[script_id] = json.loads(str(text))
        except json.JSONDecodeError:
            continue
    return payloads


def resolve_json_path(data: Any, parts: list[str]) -> list[str]:
    if not parts:
        return [data] if isinstance(data, str) else []
    if isinstance(data, dict):
        if parts[0] not in data:
            return []
        return resolve_json_path(data[parts[0]], parts[1:])
    if isinstance(data, list):
        values: list[str] = []
        for item in data:
            values.extend(resolve_json_path(item, parts))
        return values
    return []


def structured_texts(soup: BeautifulSoup, metadata: dict[str, object]) -> list[str]:
    payloads = script_json_payloads(soup)
    paths = list(DEFAULT_STRUCTURED_TEXT_PATHS)
    for path in profile(metadata).get("structured_text_paths", []):
        if isinstance(path, str) and path not in paths:
            paths.append(path)

    texts: list[str] = []
    for path in paths:
        parts = [part for part in path.split(".") if part]
        if not parts:
            continue
        if parts[0] in payloads:
            texts.extend(resolve_json_path(payloads[parts[0]], parts[1:]))
            continue
        for payload in payloads.values():
            texts.extend(resolve_json_path(payload, parts))
    return texts


_MD_RE = re.compile(r"^#{1,6}\s", re.MULTILINE)
_HTML_ROOT_RE = re.compile(r"<(?:html|body|article|main|div|p|h[1-6])\b", re.IGNORECASE)


def _looks_like_plain_markdown(text: str) -> bool:
    stripped = text.lstrip()
    if _HTML_ROOT_RE.search(stripped[:500]):
        return False
    return bool(_MD_RE.search(stripped[:2000]))


def _render_markdown_to_html(text: str) -> str:
    return MarkdownIt("commonmark").render(text)


def extract_snapshot(snapshot_dir: Path) -> ExtractionResult:
    metadata = read_json(snapshot_dir / "response.json")
    source_id = metadata["source_id"]
    html = (snapshot_dir / "raw.html").read_text(encoding="utf-8")
    if _looks_like_plain_markdown(html):
        html = _render_markdown_to_html(html)
    soup = BeautifulSoup(html, "html5lib")
    structured = structured_texts(soup, metadata)
    remove_noise_nodes(soup)
    root = configured_content_root(soup, metadata)

    texts: list[str] = []
    seen_texts: set[str] = set()
    for element in root.find_all(TEXT_TAGS):
        if should_extract_element(element):
            append_unique_text(texts, seen_texts, element.get_text(" "))
    for text in structured:
        append_unique_text(texts, seen_texts, text)

    sections = []
    for index, text in enumerate(texts, start=1):
        span_id = f"{source_id}-{index}"
        sections.append(
            {
                "source_id": source_id,
                "url": metadata["url"],
                "final_url": metadata["final_url"],
                "source_type": metadata["source_type"],
                "captured_at": metadata["captured_at"],
                "section_anchor": "root",
                "span_id": span_id,
                "short_excerpt": text[:600],
                "quote_hash": quote_hash(text),
                "text": text,
            }
        )

    write_json(snapshot_dir / "sections.json", sections)
    qa = qa_gate(metadata, sections)
    write_json(snapshot_dir / "qa.json", qa)
    readable = "\n\n".join(f"- [{item['span_id']}] {item['text']}" for item in sections)
    write_text(snapshot_dir / "readable.md", readable.rstrip() + "\n")
    write_text(snapshot_dir / "review.md", render_review(metadata, sections, qa))
    return ExtractionResult(source_id=source_id, section_count=len(sections))
