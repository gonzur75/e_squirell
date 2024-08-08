from rest_framework import status

from storage_heater.views import HeatStorageViewSet


def test_view_list_records(db, api_request_factory, storage_heater_status):
    url = "api/v1/heat_storage"
    view = HeatStorageViewSet.as_view({"get": "list"})

    request = api_request_factory.get(url)
    response = view(request)

    assert response.status_code == status.HTTP_200_OK
    assert storage_heater_status.relay_one == response.data[0]["relay_one"]

