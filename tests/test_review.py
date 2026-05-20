import pytest

from recipe_importer.models import ReviewDecision
from recipe_importer.paths import KbPaths
from recipe_importer.review import (
    current_candidate,
    decide_current,
    next_candidate,
    previous_candidate,
    start_review,
)
from recipe_importer.storage import read_json, write_text


def test_review_session_current_next_and_decide(kb_root):
    paths = KbPaths(kb_root).ensure()
    write_text(paths.proposed_dir / "a.md", "---\nid: a\n---\n")
    write_text(paths.proposed_dir / "b.md", "---\nid: b\n---\n")

    session = start_review(paths)
    assert current_candidate(paths, session).name == "a.md"

    session = next_candidate(paths, session)
    assert current_candidate(paths, session).name == "b.md"

    decide_current(paths, session, ReviewDecision.NEEDS_MORE_EVIDENCE, notes="source quote too broad")
    record = read_json(paths.review_dir / "decisions.json")[0]

    assert record["candidate_id"] == "b"
    assert record["decision"] == "needs_more_evidence"


def test_previous_candidate_moves_back(kb_root):
    paths = KbPaths(kb_root).ensure()
    write_text(paths.proposed_dir / "a.md", "---\nid: a\n---\n")
    write_text(paths.proposed_dir / "b.md", "---\nid: b\n---\n")

    session = start_review(paths)
    session = next_candidate(paths, session)
    assert current_candidate(paths, session).name == "b.md"

    session = previous_candidate(paths, session)
    assert current_candidate(paths, session).name == "a.md"


def test_previous_candidate_stops_at_start(kb_root):
    paths = KbPaths(kb_root).ensure()
    write_text(paths.proposed_dir / "a.md", "---\nid: a\n---\n")

    session = start_review(paths)
    session = previous_candidate(paths, session)
    assert current_candidate(paths, session).name == "a.md"


def test_next_candidate_stops_at_end(kb_root):
    paths = KbPaths(kb_root).ensure()
    write_text(paths.proposed_dir / "a.md", "---\nid: a\n---\n")

    session = start_review(paths)
    session = next_candidate(paths, session)
    assert current_candidate(paths, session).name == "a.md"


def test_empty_review_queue_raises_on_current(kb_root):
    paths = KbPaths(kb_root).ensure()
    session = start_review(paths)

    with pytest.raises(ValueError):
        current_candidate(paths, session)


def test_decide_appends_multiple_decisions(kb_root):
    paths = KbPaths(kb_root).ensure()
    write_text(paths.proposed_dir / "a.md", "---\nid: a\n---\n")
    write_text(paths.proposed_dir / "b.md", "---\nid: b\n---\n")

    session = start_review(paths)
    decide_current(paths, session, ReviewDecision.ACCEPT, notes="good")
    session = next_candidate(paths, session)
    decide_current(paths, session, ReviewDecision.REJECT, notes="bad")

    records = read_json(paths.review_dir / "decisions.json")
    assert len(records) == 2
    assert records[0]["candidate_id"] == "a"
    assert records[0]["decision"] == "accept"
    assert records[1]["candidate_id"] == "b"
    assert records[1]["decision"] == "reject"


def test_session_is_persisted_to_json(kb_root):
    paths = KbPaths(kb_root).ensure()
    write_text(paths.proposed_dir / "a.md", "---\nid: a\n---\n")
    write_text(paths.proposed_dir / "b.md", "---\nid: b\n---\n")

    start_review(paths)
    data = read_json(paths.review_dir / "session.json")

    assert data["cursor"] == 0
    assert data["candidates"] == ["a.md", "b.md"]
