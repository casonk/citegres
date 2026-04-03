"""Root conftest — adds repo root to sys.path so flat modules are importable."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

pytest_plugins = ["dyno_lab.fixtures"]
