
from unittest.mock import patch

import pytest
from config import settings
from storage_heater import MqttService


@pytest.fixture
def mock_client():
    with patch('paho.mqtt.client.Client') as mock_client:
        yield mock_client


@pytest.fixture
def service(mock_client):
    return MqttService(mock_client)


def test_connect_success(mock_client, service, caplog):
    mock_client.connect.return_value = True
    mock_client.on_connect.return_value = True
    service.connect()

    mock_client.connect.assert_called_once_with(
        host=settings.MQTT_SERVER, port=settings.MQTT_PORT, keepalive=settings.MQTT_KEEPALIVE
    )
    mock_client.username_pw_set.assert_called_once_with(settings.MQTT_USER, settings.MQTT_PASSWORD)
    assert hasattr(mock_client, 'on_connect')
    assert f'Connected to Mqtt broker at {settings.MQTT_SERVER}' in caplog.text


def test_connect_failure(mock_client, caplog, service):
    mock_client.connect.side_effect = Exception("Connection error")
    service.connect()

    mock_client.connect.assert_called_once_with(
        host=settings.MQTT_SERVER, port=settings.MQTT_PORT, keepalive=settings.MQTT_KEEPALIVE
    )
    assert f"Unable to connect to Mqtt broker {settings.MQTT_SERVER}:" in caplog.text


def test_on_connect(mock_client, caplog, service):
    mock_client.return_value = service.client
    service.on_connect(mock_client, None, None, 0)

    assert f"Subscribed to Mqtt topic: {settings.MQTT_TOPIC}" in caplog.text
    mock_client.subscribe.assert_called_once_with(settings.MQTT_TOPIC)


def test_on_connect_failure(mock_client, caplog, service):
    mock_client.subscribe.side_effect = Exception("Test Error")
    service.on_connect(mock_client, None, None, 0)

    mock_client.subscribe.assert_called_once_with(settings.MQTT_TOPIC)
    assert f"Failed to subscribe to Mqtt topic: {settings.MQTT_TOPIC}" in caplog.text
