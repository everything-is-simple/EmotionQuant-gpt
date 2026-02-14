from __future__ import annotations

import shutil
from uuid import uuid4
from pathlib import Path

from scripts.quality.local_quality_check import (
    PROJECT_ROOT,
    SELF_FILE,
    find_hardcoded_paths,
    iter_scan_files,
)


def test_shebang_is_ignored() -> None:
    tmp_dir = PROJECT_ROOT / ".reports" / ".tmp-test-artifacts" / f"lqc-shebang-{uuid4().hex}"
    tmp_dir.mkdir(parents=True, exist_ok=False)
    try:
        target = tmp_dir / "sample.py"
        target.write_text("#!/usr/bin/env python3\nprint('ok')\n", encoding="utf-8")
        assert find_hardcoded_paths(target) == []
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


def test_windows_path_literal_is_detected() -> None:
    tmp_dir = PROJECT_ROOT / ".reports" / ".tmp-test-artifacts" / f"lqc-winpath-{uuid4().hex}"
    tmp_dir.mkdir(parents=True, exist_ok=False)
    try:
        target = tmp_dir / "sample.py"
        target.write_text('p = "C:\\\\data\\\\cache"\n', encoding="utf-8")
        hits = find_hardcoded_paths(target)
        assert len(hits) == 1
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


def test_scan_files_excludes_env_and_self() -> None:
    files = list(iter_scan_files())
    assert SELF_FILE not in files
    assert not any(p.name == ".env" for p in files)
    assert not any("tests" in p.parts for p in files)
    assert any(p.name == ".env.example" for p in files)
