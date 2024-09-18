import time
from unittest.mock import patch

from config import settings
from conftest import mock_client, service
from storage_heater.serializers import StorageHeaterSerializer
from storage_heater.tests.helpers import mqtt_message_for_testing


def test_connect_success(mock_client, service, caplog):
    mock_client.connect.return_value = True
    mock_client.on_connect.return_value = True
    service.connect()

    mock_client.connect.assert_called_once_with(
        host=settings.MQTT_SERVER, port=settings.MQTT_PORT, keepalive=settings.MQTT_KEEPALIVE
    )
    mock_client.username_pw_set.assert_called_once_with(settings.MQTT_USER, settings.MQTT_PASSWORD)
    assert hasattr(mock_client, 'on_connect')
    assert hasattr(mock_client, 'on_message')
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


@patch.object(StorageHeaterSerializer, 'is_valid')
@patch.object(StorageHeaterSerializer, 'save')
def test_on_message(mock_is_valid, mock_save, mock_client, caplog, service, db):
    mock_client.return_value = service.client
    data = {'status': True, 'time_stamp': time.time(), 'temp_one': 24.5, 'relay_one': 1}
    msg = mqtt_message_for_testing(data)

    service.on_message(mock_client, None, msg)

    mock_is_valid.assert_called_once()
    mock_save.assert_called_once()
    assert msg.topic + " " + str(msg.payload) + " has been saved to database" in caplog.text


@patch.object(StorageHeaterSerializer, 'save')
def test_on_message_invalid_data(mock_save, mock_client, caplog, service, db):
    mock_client.return_value = service.client
    data = {'status': True, 'time_stamp': time.time(), 'temp_one': 140.5, 'relay_one': 1}
    msg = mqtt_message_for_testing(data)

    service.on_message(mock_client, None, msg)
    mock_save.assert_not_called()
    assert 'Failed validating data' in caplog.text
