"""Get PIDS reported for a homebrew managed service."""
# SPDX-License-Identifier: BSD-2-Clause

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import traceback

# ruff: noqa: S603, S607, T201


def main(argv: list[str] | None = None) -> None:
    """Eponymous main."""
    argparser = argparse.ArgumentParser()
    argparser.add_argument("service")

    args = argparser.parse_args(args=argv)

    proc = subprocess.run(
        ["brew", "services", "info", "--json", args.service],
        capture_output=True,
        check=True,
        text=True,
    )
    for service_info in json.loads(proc.stdout):
        if service_info["name"] == args.service and service_info["pid"] is not None:
            print(service_info["pid"])


if __name__ == "__main__":
    try:
        main()
    # ruff: noqa: BLE001
    except Exception:
        traceback.print_exc()
        sys.exit(1)
