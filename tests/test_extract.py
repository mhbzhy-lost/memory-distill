from pathlib import Path

from recipe_importer.extract import extract_snapshot
from recipe_importer.paths import KbPaths
from recipe_importer.storage import read_json, write_json, write_text


def test_extract_snapshot_writes_sections_and_evidence(kb_root):
    paths = KbPaths(kb_root).ensure()
    snapshot_dir = paths.snapshots_dir / "react-error-418"
    fixture = Path("tests/fixtures/react_error_418.html").read_text(encoding="utf-8")
    write_text(snapshot_dir / "raw.html", fixture)
    write_json(
        snapshot_dir / "response.json",
        {
            "source_id": "react-error-418",
            "url": "https://react.dev/errors/418",
            "final_url": "https://react.dev/errors/418",
            "source_type": "official_error_doc",
            "captured_at": "2026-05-20T00:00:00Z",
            "retrieved_status": 200,
            "content_hash": "sha256:raw",
        },
    )

    result = extract_snapshot(snapshot_dir)

    sections = read_json(snapshot_dir / "sections.json")
    readable = (snapshot_dir / "readable.md").read_text(encoding="utf-8")
    review = (snapshot_dir / "review.md").read_text(encoding="utf-8")

    assert result.source_id == "react-error-418"
    assert result.section_count == 8
    assert sections[0]["span_id"] == "react-error-418-1"
    assert sections[0]["short_excerpt"].startswith("Hydration failed")
    assert "Hydration failed" in readable
    assert "## 预期线索命中" in review
    assert sections[0]["quote_hash"].startswith("sha256:")


def test_extract_snapshot_ignores_invalid_configured_content_selector(kb_root):
    paths = KbPaths(kb_root).ensure()
    snapshot_dir = paths.snapshots_dir / "invalid-selector"
    write_text(
        snapshot_dir / "raw.html",
        """
        <html>
          <body>
            <main>
              <article>
                <h1>Fallback Title</h1>
                <p>Fallback evidence text.</p>
              </article>
            </main>
          </body>
        </html>
        """,
    )
    write_json(
        snapshot_dir / "response.json",
        {
            "source_id": "invalid-selector",
            "url": "https://example.test/invalid-selector",
            "final_url": "https://example.test/invalid-selector",
            "source_type": "official_doc",
            "captured_at": "2026-05-21T00:00:00Z",
            "retrieved_status": 200,
            "content_hash": "sha256:raw",
            "expected_failure_hints": ["Fallback evidence"],
            "extraction_profile": {"content_selectors": ["main["]},
        },
    )

    result = extract_snapshot(snapshot_dir)

    sections = read_json(snapshot_dir / "sections.json")
    qa = read_json(snapshot_dir / "qa.json")

    assert result.section_count == 2
    assert [item["text"] for item in sections] == ["Fallback Title", "Fallback evidence text."]
    assert qa["status"] == "passed"


def test_extract_snapshot_filters_navigation_and_writes_review_summary(kb_root):
    paths = KbPaths(kb_root).ensure()
    snapshot_dir = paths.snapshots_dir / "next-dynamic-server-error"
    write_text(
        snapshot_dir / "raw.html",
        """
        <html>
          <body>
            <aside>
              <ul>
                <li>Guides</li>
                <li>Forms</li>
                <li>Testing</li>
              </ul>
            </aside>
            <main>
              <article>
                <h1>DynamicServerError - Dynamic Server Usage</h1>
                <p>DynamicServerError is thrown when Dynamic Server Usage is detected.</p>
                <p>You attempted to use cookies or headers outside the async call stack.</p>
                <h2>Possible Ways to Fix It</h2>
                <p>Make sure cookies and headers are called in the same async context.</p>
              </article>
            </main>
          </body>
        </html>
        """,
    )
    write_json(
        snapshot_dir / "response.json",
        {
            "source_id": "next-dynamic-server-error",
            "url": "https://nextjs.org/docs/messages/dynamic-server-error",
            "final_url": "https://nextjs.org/docs/messages/dynamic-server-error",
            "source_type": "official_error_doc",
            "captured_at": "2026-05-21T00:00:00Z",
            "retrieved_status": 200,
            "content_hash": "sha256:raw",
            "expected_failure_hints": [
                "DynamicServerError",
                "cookies or headers outside the async call stack",
            ],
        },
    )

    result = extract_snapshot(snapshot_dir)

    sections = read_json(snapshot_dir / "sections.json")
    texts = [item["text"] for item in sections]
    review = (snapshot_dir / "review.md").read_text(encoding="utf-8")

    assert result.section_count == 5
    assert "Forms" not in texts
    assert "DynamicServerError - Dynamic Server Usage" in texts
    assert "## 快照质量检查" in review
    assert "## 预期线索命中" in review
    assert "DynamicServerError" in review
    assert "[next-dynamic-server-error-1]" in review
    assert "## 审阅决策" in review


def test_extract_snapshot_keeps_article_inside_sidebar_layout_wrapper(kb_root):
    paths = KbPaths(kb_root).ensure()
    snapshot_dir = paths.snapshots_dir / "react-error-418"
    write_text(
        snapshot_dir / "raw.html",
        """
        <html>
          <body>
            <main>
              <div class="grid grid-cols-sidebar-content">
                <aside>
                  <li>Installation</li>
                  <li>Debugging and Troubleshooting</li>
                </aside>
                <article>
                  <h1>Hydration failed because the server rendered HTML didn't match the client</h1>
                  <p>This can happen if a SSR-ed Client Component used a server/client branch.</p>
                </article>
              </div>
            </main>
          </body>
        </html>
        """,
    )
    write_json(
        snapshot_dir / "response.json",
        {
            "source_id": "react-error-418",
            "url": "https://react.dev/errors/418",
            "final_url": "https://react.dev/errors/418",
            "source_type": "official_error_doc",
            "captured_at": "2026-05-21T00:00:00Z",
            "retrieved_status": 200,
            "content_hash": "sha256:raw",
            "expected_failure_hints": ["server rendered HTML didn't match the client"],
        },
    )

    result = extract_snapshot(snapshot_dir)

    sections = read_json(snapshot_dir / "sections.json")
    texts = [item["text"] for item in sections]

    assert result.section_count == 2
    assert "Installation" not in texts
    assert "Hydration failed because the server rendered HTML didn't match the client" in texts


def test_extract_snapshot_uses_prose_root_without_deleting_navbar_height_layout(kb_root):
    paths = KbPaths(kb_root).ensure()
    snapshot_dir = paths.snapshots_dir / "tanstack-query-important-defaults"
    write_text(
        snapshot_dir / "raw.html",
        """
        <html>
          <body>
            <div class="min-h-[calc(100dvh-var(--navbar-height))] flex">
              <div class="ts-sidebar-label">
                <li>Getting Started</li>
                <li>Examples</li>
              </div>
              <div class="prose styled-markdown-content">
                <h1>Important Defaults</h1>
                <p>Query instances via useQuery or useInfiniteQuery by default consider cached data as stale.</p>
                <li>Stale queries are refetched automatically in the background when new instances mount.</li>
              </div>
            </div>
          </body>
        </html>
        """,
    )
    write_json(
        snapshot_dir / "response.json",
        {
            "source_id": "tanstack-query-important-defaults",
            "url": "https://tanstack.com/query/latest/docs/framework/react/guides/important-defaults",
            "final_url": "https://tanstack.com/query/latest/docs/framework/react/guides/important-defaults",
            "source_type": "official_doc",
            "captured_at": "2026-05-21T00:00:00Z",
            "retrieved_status": 200,
            "content_hash": "sha256:raw",
            "expected_failure_hints": [
                "query data is stale by default",
                "cached data as stale",
            ],
        },
    )

    result = extract_snapshot(snapshot_dir)

    sections = read_json(snapshot_dir / "sections.json")
    texts = [item["text"] for item in sections]
    review = (snapshot_dir / "review.md").read_text(encoding="utf-8")

    assert result.section_count == 3
    assert "Getting Started" not in texts
    assert "Important Defaults" in texts
    assert any("cached data as stale" in text for text in texts)
    assert "`query data is stale by default`：未找到直接段落命中" not in review
    assert "[tanstack-query-important-defaults-2]" in review


def test_extract_snapshot_reads_next_data_error_message_and_passes_qa(kb_root):
    paths = KbPaths(kb_root).ensure()
    snapshot_dir = paths.snapshots_dir / "react-error-418"
    write_text(
        snapshot_dir / "raw.html",
        """
        <html>
          <body>
            <main>
              <article>
                <h1>Minified React error #418</h1>
                <p>The full text of the error you just encountered is:</p>
                <code>Hydration failed because the server rendered HTML didn't match the client.</code>
              </article>
            </main>
            <script id="__NEXT_DATA__" type="application/json">
              {
                "props": {
                  "pageProps": {
                    "errorMessage": "Hydration failed because the server rendered %s didn't match the client. This can happen if a SSR-ed Client Component used Date.now() or Math.random()."
                  }
                }
              }
            </script>
          </body>
        </html>
        """,
    )
    write_json(
        snapshot_dir / "response.json",
        {
            "source_id": "react-error-418",
            "url": "https://react.dev/errors/418",
            "final_url": "https://react.dev/errors/418",
            "source_type": "official_error_doc",
            "captured_at": "2026-05-21T00:00:00Z",
            "retrieved_status": 200,
            "content_hash": "sha256:raw",
            "expected_failure_hints": [
                "hydration mismatch",
                "server rendered HTML didn't match the client",
            ],
        },
    )

    result = extract_snapshot(snapshot_dir)

    sections = read_json(snapshot_dir / "sections.json")
    qa = read_json(snapshot_dir / "qa.json")
    review = (snapshot_dir / "review.md").read_text(encoding="utf-8")

    assert result.section_count == 4
    assert any("Date.now() or Math.random()" in item["text"] for item in sections)
    assert qa["status"] == "passed"
    assert "## QA 闸门" in review
    assert "状态: 通过" in review
    assert "needs_agentic_fallback" not in review


def test_extract_snapshot_marks_qa_gate_for_agentic_fallback_when_hints_are_missing(kb_root):
    paths = KbPaths(kb_root).ensure()
    snapshot_dir = paths.snapshots_dir / "react-error-418"
    write_text(
        snapshot_dir / "raw.html",
        """
        <html>
          <body>
            <main>
              <article>
                <h1>Minified React error #418</h1>
                <p>The full text of the error you just encountered is:</p>
              </article>
            </main>
          </body>
        </html>
        """,
    )
    write_json(
        snapshot_dir / "response.json",
        {
            "source_id": "react-error-418",
            "url": "https://react.dev/errors/418",
            "final_url": "https://react.dev/errors/418",
            "source_type": "official_error_doc",
            "captured_at": "2026-05-21T00:00:00Z",
            "retrieved_status": 200,
            "content_hash": "sha256:raw",
            "expected_failure_hints": ["hydration mismatch"],
        },
    )

    extract_snapshot(snapshot_dir)

    qa = read_json(snapshot_dir / "qa.json")
    review = (snapshot_dir / "review.md").read_text(encoding="utf-8")

    assert qa["status"] == "needs_agentic_fallback"
    assert any(check["name"] == "expected_hints_matched" and not check["passed"] for check in qa["checks"])
    assert "状态: 需要 agentic fallback" in review
    assert "raw.html" in review


def test_extract_snapshot_handles_plain_markdown(kb_root):
    paths = KbPaths(kb_root).ensure()
    snapshot_dir = paths.snapshots_dir / "swift-doc"
    write_text(
        snapshot_dir / "raw.html",
        "# Error Handling in Swift\n\n"
        "Swift uses a `throws` keyword to mark functions that can propagate errors.\n\n"
        "## Calling Throwing Functions\n\n"
        "Use `try` before a throwing call and wrap it in `do { ... } catch { ... }`.\n"
        "The `try keyword required` rule prevents calling a throwing function from a non-throwing context.\n\n"
        "```swift\n"
        "do {\n"
        "    try fetchData()\n"
        "} catch {\n"
        "    print(error)\n"
        "}\n"
        "```\n",
    )
    write_json(
        snapshot_dir / "response.json",
        {
            "source_id": "swift-doc",
            "url": "https://raw.githubusercontent.com/swiftlang/swift/main/test.md",
            "final_url": "https://raw.githubusercontent.com/swiftlang/swift/main/test.md",
            "source_type": "compiler_doc",
            "captured_at": "2026-05-26T00:00:00Z",
            "retrieved_status": 200,
            "content_hash": "sha256:md",
            "expected_failure_hints": ["try keyword required"],
        },
    )

    result = extract_snapshot(snapshot_dir)

    sections = read_json(snapshot_dir / "sections.json")
    qa = read_json(snapshot_dir / "qa.json")

    assert result.source_id == "swift-doc"
    assert result.section_count >= 2
    assert any("throws" in section["short_excerpt"] for section in sections)
    assert any("try" in section["short_excerpt"] for section in sections)
    assert qa["status"] == "passed"


def test_plain_markdown_detection_preserves_html_content(kb_root):
    from recipe_importer.extract import _looks_like_plain_markdown

    assert _looks_like_plain_markdown("# Heading\n\nSome text\n\n## Sub\n") is True
    assert _looks_like_plain_markdown("<html><body><h1>Title</h1></body></html>") is False
    assert _looks_like_plain_markdown("<!DOCTYPE html><html><body></body></html>") is False
    assert _looks_like_plain_markdown("  \n  # Markdown with leading whitespace\n") is True
