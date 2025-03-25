"""`ollama run` session helper."""
# SPDX-License-Identifier: BSD-2-Clause

import contextlib
import subprocess
import sys
import time

from macos_powertools.homebrew.services import Service
from macos_powertools.lib import logging as logging_lib

# ruff: noqa: S603, S606, S607


LOGGER = logging_lib.get_logger(__name__)
OLLAMA = Service("ollama")


def ollama_run(*argv: list) -> int:
    """Shorthand proxy for `ollama run [..]`.

    Args:
        argv: arguments to pass to `subprocess.call(..)` as part of `cmd`.

    Returns:
        The exit code from `subprocess.call(..)`.

    """
    return subprocess.call(["ollama", "run", *argv])


def main(argv: list[str] | None = None) -> int:
    """Eponymous main."""
    argv = argv or sys.argv
    if not OLLAMA.running(use_pgrep=True):
        LOGGER.debug("ollama was not started; starting now..")
        OLLAMA.start()
        while not OLLAMA.running():
            LOGGER.debug("Waiting for ollama service to come up..")
            time.sleep(1)
    return ollama_run(*argv[1:])


@contextlib.contextmanager
def autokill_service() -> None:
    """Stop ollama on exit."""
    yield
    OLLAMA.stop()


def oneshot_main(argv: list[str] | None = None) -> int:
    """One-shot main function.

    Unlike `main(..)` this sets up a background process to automatically stop `OLLAMA`
    on exit.

    Returns:
        The exit code from `ollama run`.

    """
    with autokill_service():
        return main(argv=argv)
