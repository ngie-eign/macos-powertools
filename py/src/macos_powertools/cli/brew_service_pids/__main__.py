"""Get a homebrew managed service's associated PIDs."""
# SPDX-License-Identifier: BSD-2-Clause

from __future__ import annotations

import argparse

from macos_powertools.homebrew import services

# ruff: noqa: T201


def _get_service(service: str) -> services.Service:
    return services.Service(service)


def _print_pid(pid: int) -> None:
    print(pid)


def main(argv: list[str] | None = None) -> None:
    """Eponymous main."""
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Increase verbosity level.",
    )
    argparser.add_argument("service")

    args = argparser.parse_args(args=argv)

    # ruff: noqa: E501, ERA001
    # log_level = "debug" if args.verbose > 2 else ("info" if args.verbose > 1 else "error")
    # get_logger(__name__, level=log_level)

    service = _get_service(args.service)
    for pid in service.pids():
        _print_pid(pid)
