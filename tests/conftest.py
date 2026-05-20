from pathlib import Path

import pytest


@pytest.fixture
def kb_root(tmp_path: Path) -> Path:
    root = tmp_path / "repo"
    root.mkdir()
    return root
