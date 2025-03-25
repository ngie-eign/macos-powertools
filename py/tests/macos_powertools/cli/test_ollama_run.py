"""Tests for `brew-service-pids.py`."""

from unittest.mock import patch

import pytest

from macos_powertools.cli.ollama_run import __main__

# ruff: noqa: ANN001, ANN201, ARG001, D103, INP001


def mock_main(path: str) -> str:
    return f"{__main__.__name__}.{path}"


@pytest.fixture
def mock_ollama():
    with patch(mock_main("OLLAMA")) as patcher:
        yield patcher


@pytest.fixture
def mock_ollama_run():
    with patch(mock_main("ollama_run")) as patcher:
        yield patcher


@pytest.fixture
def mock_subprocess_call():
    with patch(mock_main("subprocess.call")) as patcher:
        yield patcher


def test_main_slow_start(
    mock_ollama,
    mock_ollama_run,
) -> None:
    mock_ollama_run_args = [__main__.__name__, "bogus", "command"]

    mock_ollama.running.side_effect = [False, False, True]

    __main__.main(mock_ollama_run_args)

    mock_ollama.start.assert_called_once()
    mock_ollama_run.assert_called_once_with(*mock_ollama_run_args[1:])
    mock_ollama.stop.assert_not_called()


def test_main_running_already(
    mock_ollama,
    mock_ollama_run,
) -> None:
    mock_ollama_run_args = [__main__.__name__, "bogus", "command"]

    mock_ollama.running.return_value = True

    __main__.main(mock_ollama_run_args)

    mock_ollama.start.assert_not_called()
    mock_ollama_run.assert_called_once_with(*mock_ollama_run_args[1:])
    mock_ollama.stop.assert_not_called()


def test_oneshot_slow_start(
    mock_ollama,
    mock_ollama_run,
) -> None:
    mock_ollama_run_args = [__main__.__name__, "bogus", "command"]

    mock_ollama.running.side_effect = [False, False, True]

    __main__.oneshot_main(mock_ollama_run_args)

    mock_ollama.start.assert_called_once()
    mock_ollama_run.assert_called_once_with(*mock_ollama_run_args[1:])
    mock_ollama.stop.assert_called_once()


def test_oneshot_running_already(
    mock_ollama,
    mock_ollama_run,
) -> None:
    mock_ollama_run_args = [__main__.__name__, "bogus", "command"]

    mock_ollama.running.return_value = True

    __main__.oneshot_main(mock_ollama_run_args)

    mock_ollama.start.assert_not_called()
    mock_ollama_run.assert_called_once_with(*mock_ollama_run_args[1:])
    mock_ollama.stop.assert_called_once()
