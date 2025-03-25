"""Tests for `macos_powertools.homebrew.services`."""

import json
from unittest import mock

import pytest

from macos_powertools.homebrew import services

# ruff: noqa: ANN001, ANN201, D103, D104, INP001, S101, SLF001

INVALID_INFO_TEST_VECTORS = [
    [
        "foo",
        [
            {
                "name": "foo",
                "pid": 42,
            },
            {
                "name": "bar",
                "pid": 43,
            },
        ],
    ],
    [
        "bar",
        [
            {
                "name": "foo",
                "pid": 42,
            },
        ],
    ],
]


VALID_INFO_TEST_VECTORS = [
    [
        "foo",
        [
            {
                "name": "foo",
                "pid": 42,
            },
            {
                "name": "foo",
                "pid": 43,
            },
        ],
        [42, 43],
    ],
    [
        "foo",
        [
            {
                "name": "foo",
                "pid": None,
            },
        ],
        [],
    ],
    [
        "foo",
        {},
        [],
    ],
]


@pytest.mark.parametrize(
    # ruff: noqa: PT006 - false positive.
    "service_name,mock_info_output",
    INVALID_INFO_TEST_VECTORS,
)
def test_service_pids_invalid_info(service_name, mock_info_output) -> None:
    service = services.Service(service_name)
    service.info = mock.MagicMock(return_value=mock_info_output)
    with pytest.raises(AssertionError):
        _pids = service.pids()


@pytest.mark.parametrize(
    # ruff: noqa: PT006 - false positive.
    "service_name,mock_info_output,service_pids",
    VALID_INFO_TEST_VECTORS,
)
def test_service_pids_valid_info(service_name, mock_info_output, service_pids) -> None:
    service = services.Service(service_name)
    service.info = mock.MagicMock(return_value=mock_info_output)
    assert service.pids() == service_pids


@pytest.fixture
def mock_brew_services():
    with mock.patch(f"{services.__name__}.brew_services") as patcher:
        yield patcher


@pytest.fixture
def mock_subprocess_call():
    with mock.patch(f"{services.__name__}.subprocess.call") as patcher:
        yield patcher


@pytest.fixture
def mock_subprocess_run():
    with mock.patch(f"{services.__name__}.subprocess.run") as patcher:
        yield patcher


def test_service_running(mock_brew_services) -> None:
    service_name = "bogus"
    service = services.Service(service_name)
    mock_brew_services.return_value = json.dumps([{"name": service_name, "pid": 42}])
    assert service.running()


def test_service_running_pgrep(mock_subprocess_call) -> None:
    service_name = "bogus"
    service = services.Service(service_name)
    mock_subprocess_call.return_value = 0
    assert service.running(use_pgrep=True, process_name="bogus")


def test_service_running_pgrep_default_to_service_name(mock_subprocess_call) -> None:
    service_name = "bogus"
    service = services.Service(service_name)
    mock_subprocess_call.return_value = 0
    assert service.running(use_pgrep=True)


def test_service_not_running(mock_brew_services) -> None:
    service_name = "bogus"
    service = services.Service(service_name)
    mock_brew_services.return_value = json.dumps([{"name": service_name, "pid": None}])
    assert not service.running()


def test_service_start_succeeds(mock_brew_services) -> None:
    service_name = "bogus"
    service = services.Service(service_name)
    service.start()
    mock_brew_services.assert_called_with(["start", service_name])


def test_service_stop_succeeds(mock_brew_services) -> None:
    service_name = "bogus"
    service = services.Service(service_name)
    service.stop()
    mock_brew_services.assert_called_with(["stop", service_name])


def test_brew_services_for_coverage(mock_subprocess_run) -> None:
    args = ["list", "a"]
    kwargs = services._DEFAULT_SUBPROCESS_RUN_KW
    services.brew_services(args, **kwargs)
    mock_subprocess_run.assert_called_with(["brew", "services", *args], **kwargs)
