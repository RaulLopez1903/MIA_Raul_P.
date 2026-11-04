from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    model_name: str
    batch_size: int
    device: str


def load_settings(config_path: Path | None = None) -> Settings:
    path = config_path or Path(__file__).resolve().parent.parent / "config.json"
    with path.open(encoding="utf-8") as config_file:
        raw_config = json.load(config_file)
    if not isinstance(raw_config, dict):
        raise ValueError("config.json must contain a JSON object")

    model_name = raw_config.get("model_name")
    batch_size = raw_config.get("batch_size")
    device = raw_config.get("device")
    if not isinstance(model_name, str) or not model_name.strip():
        raise ValueError("'model_name' must be a non-empty string")
    if isinstance(batch_size, bool) or not isinstance(batch_size, int) or batch_size <= 0:
        raise ValueError("'batch_size' must be a positive integer")
    if not isinstance(device, str) or not device.strip():
        raise ValueError("'device' must be a non-empty string")
    return Settings(model_name=model_name.strip(), batch_size=batch_size, device=device.strip())
