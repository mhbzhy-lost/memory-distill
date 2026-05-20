import hashlib
import re
from dataclasses import dataclass
from pathlib import Path

from bs4 import BeautifulSoup

from recipe_importer.storage import read_json, write_json, write_text


@dataclass(frozen=True)
class ExtractionResult:
    source_id: str
    section_count: int


def normalize_space(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def quote_hash(text: str) -> str:
    return "sha256:" + hashlib.sha256(normalize_space(text).encode("utf-8")).hexdigest()


def extract_snapshot(snapshot_dir: Path) -> ExtractionResult:
    metadata = read_json(snapshot_dir / "response.json")
    source_id = metadata["source_id"]
    html = (snapshot_dir / "raw.html").read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "html5lib")
    main = soup.find("main") or soup.body or soup

    texts: list[str] = []
    for element in main.find_all(["h1", "h2", "h3", "p", "li"]):
        text = normalize_space(element.get_text(" "))
        if text:
            texts.append(text)

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
    readable = "\n\n".join(f"- [{item['span_id']}] {item['text']}" for item in sections)
    write_text(snapshot_dir / "readable.md", readable + "\n")
    return ExtractionResult(source_id=source_id, section_count=len(sections))
