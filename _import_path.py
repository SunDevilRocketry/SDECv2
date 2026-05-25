# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2025 Sun Devil Rocketry

"""
Ensure the repository root (parent of SDECv2) is on sys.path so SDECv2.* imports resolve
when running tests or scripts from the SDECv2 directory without an editable install.
"""

import sys
from pathlib import Path

_path_configured = False


def ensure_sdecv2_package_path() -> None:
    global _path_configured
    if _path_configured:
        return
    package_root = Path(__file__).resolve().parent
    repo_root = package_root.parent
    # sdec-cli layout: modules live under a sibling SDECv2/ directory at repo root.
    # Firmware CI layout (sdec/): modules are in the install root; pip install -e . handles imports.
    if (repo_root / "SDECv2").is_dir():
        repo_root_str = str(repo_root)
        if repo_root_str not in sys.path:
            sys.path.insert(0, repo_root_str)
    _path_configured = True


ensure_sdecv2_package_path()
