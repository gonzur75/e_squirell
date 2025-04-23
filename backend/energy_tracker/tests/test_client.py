from unittest.mock import MagicMock

import pytest

from energy_tracker.client import PC321MeterClient


@pytest.fixture
def mock_client():
    client = PC321MeterClient(
        device_id="mock_device_id",
        device_ip="192.168.0.100",
        local_key="mock_local_key",
        device_version=3.3
    )
    client.device = MagicMock()  # Mock the Tuya device for testing
    return client


def test_initialize_client(mock_client):
    assert mock_client.device_id == "mock_device_id"
    assert mock_client.device_ip == "192.168.0.100"
    assert mock_client.local_key == "mock_local_key"
    assert mock_client.device_version == 3.3


def test_get_device_status_success(mock_client):
    mock_status = {"dps": {'101': 2439, '102': 802}}
    mock_client.device.status.return_value = mock_status

    result = mock_client.get_device_status()
    assert result == mock_status
    mock_client.device.set_socketTimeout.assert_called_once_with(5)
    mock_client.device.status.assert_called_once()


def test_get_device_status_no_dps(mock_client):
    mock_client.device.status.return_value = {}

    result = mock_client.get_device_status()
    assert result is None
    mock_client.device.set_socketTimeout.assert_called_once_with(5)
    mock_client.device.status.assert_called_once()


def test_get_device_status_exception(mock_client):
    mock_client.device.status.side_effect = Exception("Connection error")

    result = mock_client.get_device_status()
    assert result is None
    mock_client.device.set_socketTimeout.assert_called_once_with(5)
    mock_client.device.status.assert_called_once()
