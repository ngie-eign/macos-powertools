"""Get PIDS reported for a homebrew managed service."""

# SPDX-License-Identifier: BSD-2-Clause

from __future__ import annotations

import argparse
import json
import logging
import subprocess
import sys
from typing import Any, TypeAlias

# ruff: noqa: S603, S607, T201


logging.basicConfig(format="%(name)s: %(levelname)s: %(message)s")
LOGGER = logging.getLogger(__name__)


def brew_service_info_json(service: str) -> str:
    """`brew services info --json` wrapper.

    Helps mock out the subprocess call when testing.

    Returns:
        The matching service definitions for `service`.

    """
    proc = subprocess.run(
        ["brew", "services", "info", "--json", service],
        capture_output=True,
        check=True,
        text=True,
    )
    return proc.stdout


ServiceInfoType: TypeAlias = "list[dict[str, Any]]"


def service_pids_from_info(
    service: str, complete_service_info: ServiceInfoType,
) -> list[int]:
    """Get a list of PIDs from the complete service info.

    Args:
        service: service to match on in `complete_service_info`.
        complete_service_info: all matching service information decoded from
                               the JSON document output by `brew services info --json`.

    Returns:
        A list (empty or populated) containing all of the PIDs associated with
        `service`.

    """
    return [
        service_info["pid"]
        for service_info in complete_service_info
        if service_info["name"] == service and service_info["pid"] is not None
    ]


def main(argv: list[str] | None = None) -> None:
    """Eponymous main."""
    argparser = argparse.ArgumentParser()
    argparser.add_argument("service")

    args = argparser.parse_args(args=argv)
    try:
        complete_service_info = json.loads(brew_service_info_json(args.service))
    except json.JSONDecodeError:
        LOGGER.exception("Could not decode JSON")
        sys.exit(1)

    try:
        service_pids = service_pids_from_info(args.service, complete_service_info)
    except (IndexError, TypeError, ValueError):
        LOGGER.exception("Invalid JSON output: %r", complete_service_info)
        sys.exit(1)

    for service_pid in service_pids:
        print(service_pid)
