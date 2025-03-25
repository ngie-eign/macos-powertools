"""Tests for `macos_powertools.lib.logging`"""

import logging
import typing

from macos_powertools.lib import logging as logging_lib


def test_get_logger():
    logger = logging_lib.get_logger(__name__)
    assert typing.cast("logging.Logger", logger) is not None
