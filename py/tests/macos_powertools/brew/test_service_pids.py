"""Tests for `brew-service-pids.py`."""

import shutil
from unittest import mock

import pytest

from macos_powertools.brew.service_pids import __main__

# ruff: noqa: ANN001, ANN002, ANN003, D102, D103, INP001, PT011, S101


def mock_main(subpath: str, *args, **kwargs) -> mock._patch:
    return mock.patch(f"{__main__.__name__}.{subpath}", *args, **kwargs)


BREW = shutil.which("brew")
SERVICE_PIDS_FROM_INFO_TEST_VECTORS = [
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
        [42],
    ],
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
        "bar",
        [
            {
                "name": "foo",
                "pid": 42,
            },
        ],
        [],
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
    "service,service_info,service_pids", SERVICE_PIDS_FROM_INFO_TEST_VECTORS,
)
def test_service_pids_from_info(service, service_info, service_pids) -> None:
    assert __main__.service_pids_from_info(service, service_info) == service_pids


class TestMain:
    """main function test suite."""

    @staticmethod
    def test_service_provided() -> None:
        mock_service = "bogus"
        with mock_main("brew_service_info_json") as mock_brew_service_info_json:
            mock_brew_service_info_json.return_value = '[{"name": "bogus", "pid": 42}]'
            __main__.main([mock_service])


    @staticmethod
    def test_brew_services_returns_nonjson() -> None:
        mock_service = "bogus"
        with mock_main("brew_service_info_json") as mock_brew_service_info_json:
            mock_brew_service_info_json.return_value = "<!-- NOT JSON -->"
            with pytest.raises(SystemExit):
                __main__.main([mock_service])


    @staticmethod
    def test_brew_services_returns_invalid_json() -> None:
        mock_service = "bogus"
        with mock_main("brew_service_info_json") as mock_brew_service_info_json:
            mock_brew_service_info_json.return_value = '"boo"'
            with pytest.raises(SystemExit):
                __main__.main([mock_service])


    @staticmethod
    def test_no_args_fails() -> None:
        with pytest.raises(SystemExit):
            __main__.main([])
