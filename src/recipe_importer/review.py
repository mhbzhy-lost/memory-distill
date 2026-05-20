from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from recipe_importer.models import ReviewDecision
from recipe_importer.paths import KbPaths
from recipe_importer.storage import read_json, write_json


@dataclass(frozen=True)
class ReviewSession:
    cursor: int
    candidates: list[str]


def _session_path(paths: KbPaths) -> Path:
    return paths.review_dir / "session.json"


def _decisions_path(paths: KbPaths) -> Path:
    return paths.review_dir / "decisions.json"


def _candidate_files(paths: KbPaths) -> list[Path]:
    return sorted(paths.proposed_dir.glob("*.md"))


def load_review_session(paths: KbPaths) -> ReviewSession:
    data = read_json(_session_path(paths))
    return ReviewSession(cursor=data["cursor"], candidates=data["candidates"])


def _save_session(paths: KbPaths, session: ReviewSession) -> ReviewSession:
    write_json(_session_path(paths), {"cursor": session.cursor, "candidates": session.candidates})
    return session


def start_review(paths: KbPaths) -> ReviewSession:
    candidates = [path.name for path in _candidate_files(paths)]
    return _save_session(paths, ReviewSession(cursor=0, candidates=candidates))


def current_candidate(paths: KbPaths, session: ReviewSession | None = None) -> Path:
    session = session or load_review_session(paths)
    if not session.candidates:
        raise ValueError("review queue is empty")
    return paths.proposed_dir / session.candidates[session.cursor]


def next_candidate(paths: KbPaths, session: ReviewSession) -> ReviewSession:
    if not session.candidates:
        return session
    cursor = min(session.cursor + 1, len(session.candidates) - 1)
    return _save_session(paths, ReviewSession(cursor=cursor, candidates=session.candidates))


def previous_candidate(paths: KbPaths, session: ReviewSession) -> ReviewSession:
    cursor = max(session.cursor - 1, 0)
    return _save_session(paths, ReviewSession(cursor=cursor, candidates=session.candidates))


def decide_current(
    paths: KbPaths,
    session: ReviewSession,
    decision: ReviewDecision,
    notes: str = "",
) -> dict[str, Any]:
    current = current_candidate(paths, session)
    record = {
        "candidate_id": current.stem,
        "decision": decision.value,
        "reviewed_at": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
        "reviewer": "human",
        "notes": notes,
    }
    decisions = read_json(_decisions_path(paths)) if _decisions_path(paths).exists() else []
    decisions.append(record)
    write_json(_decisions_path(paths), decisions)
    return record
