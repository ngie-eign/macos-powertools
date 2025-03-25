"""Tests for `brew-service-pids.py`."""

from unittest import mock
from unittest.mock import patch

import pytest

from macos_powertools.cli.brew_service_pids import __main__
from macos_powertools.homebrew import services

# ruff: noqa: ANN001, ANN002, ANN003, D102, D103, INP001, PT011, S101


def mock_main(path: str) -> str:
    return f"{__main__.__name__}.{path}"


@pytest.mark.parametrize(
    "mock_pids",
    [
        pytest.param([42], id="single PID"),
        pytest.param([42, 43], id="2 PIDs"),
        pytest.param([], id="No PIDs"),
    ],
)
def test_service_provided(mock_pids) -> None:
    service_name = "bogus"

    mock_service = services.Service(service_name)
    mock_service.pids = mock.MagicMock(return_value=mock_pids)
    with (
        patch(mock_main("_get_service"), return_value=mock_service) as mock_get_service,
        patch(mock_main("_print_pid")) as mock_print_pid,
    ):
        __main__.main([service_name])

        mock_get_service.assert_called_once_with(service_name)
        mock_print_pid.assert_has_calls([mock.call(pid) for pid in mock_pids])


def test_no_args_fails() -> None:
    with pytest.raises(SystemExit):
        __main__.main([])
