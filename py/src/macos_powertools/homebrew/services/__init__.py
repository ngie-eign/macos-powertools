"""Get PIDS reported for a homebrew managed service."""
# SPDX-License-Identifier: BSD-2-Clause

from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass
from typing import (
    Any,
    AnyStr,
    TypeAlias,
)

from macos_powertools.lib import logging as logging_lib

# ruff: noqa: FBT001, FBT002, PLW1510, S101, S603, S607


LOGGER = logging_lib.get_logger(__name__)


# Type alias for output returned by `brew services info <service> --json`.
ServiceInfoType: TypeAlias = "dict[str, Any]"


_DEFAULT_SUBPROCESS_RUN_KW = {
    "capture_output": True,
    "check": True,
    "text": True,
}


def brew_services(
    subcommand: list[str],
    *subproc_args: list,
    **subproc_kwargs: dict,
) -> AnyStr:
    """Shorthand for `brew services`.

    Args:
        subcommand: subcommand.
        subproc_args: arguments to pass to `subprocess.run(..)`.
        subproc_kwargs: keyword arguments to pass to `subprocess.run(..)`.

    Returns:
        Output from `subprocess.run(..)`.

    Raises:
        All exceptions subprocess.run(..)` will raise with the provided arguments.

    """
    subproc_kwargs = dict(_DEFAULT_SUBPROCESS_RUN_KW, **subproc_kwargs)
    return subprocess.run(
        ["brew", "services", *subcommand],
        *subproc_args,
        **subproc_kwargs,
    ).stdout


@dataclass
class Service:
    """A Homebrew service.

    Properties:
        name:   service name.
    """

    name: str

    def start(self, *args: list, **kwargs: dict) -> None:
        """Proxy for `brew services start`.

        See `brew_services(..)` for more details.
        """
        LOGGER.debug("Starting service: %s", self.name)
        brew_services(["start", self.name], *args, **kwargs)

    def stop(self, *args: list, **kwargs: dict) -> None:
        """Proxy for `brew services stop`.

        See `brew_services(..)` for more details.
        """
        LOGGER.debug("Stopping service: %s", self.name)
        brew_services(["stop", self.name], *args, **kwargs)

    def info(self) -> list[ServiceInfoType]:
        """Proxy for `brew services info --json`.

        See `brew_services(..)` for more details.

        Returns:
            An empty list (if no output was provided), or the raw JSON document output
            by `brew_services(..)`.

        """
        return json.loads(brew_services(["info", "--json", self.name]))

    def running(self, use_pgrep: bool = False, process_name: str | None = None) -> bool:
        """Query whether or not the service is running.

        Args:
            process_name: the running process to check for with `pgrep`.
            use_pgrep: check whether or not the service is alive with `pgrep` instead
                       of `.info(..)` (the latter is more costly).

        Returns:
            True if running; False otherwise.

        """
        if use_pgrep:
            return subprocess.call(["pgrep", "-q", process_name or self.name]) == 0
        return bool(self.pids())

    def pids(self) -> list[int]:
        """Get service PIDs.

        Returns:
            An empty list (if no processes are running), or a list of PIDs corresponding
            to all running processes.

        """
        complete_service_info = self.info()

        pids = []
        for service_info in complete_service_info:
            assert service_info["name"] == self.name
            if service_info["pid"] is not None:
                pids.append(service_info["pid"])
        return pids
