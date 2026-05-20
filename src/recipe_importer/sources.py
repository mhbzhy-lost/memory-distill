from pathlib import Path

from recipe_importer.models import SourceList
from recipe_importer.storage import read_yaml


def load_source_list(path: Path) -> SourceList:
    return SourceList.model_validate(read_yaml(path))
