import subprocess
import sys
from pathlib import Path


def test_missing_catalog_exits_without_stdout(tmp_path: Path) -> None:
    project_root = Path(__file__).resolve().parents[1]
    missing_catalog = tmp_path / "missing.json"
    result = subprocess.run(
        [
            sys.executable,
            str(project_root / "main.py"),
            "python",
            "--catalog",
            str(missing_catalog),
        ],
        cwd=project_root,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 1
    assert result.stdout == ""
