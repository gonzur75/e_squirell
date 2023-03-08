import requests
import time

# Using random UK octopus energy tariff, until suitable Polish alternative is available
OCTOPUS_ENERGY_API_URL = "https://api.octopus.energy/v1/products/AGILE-FLEX-22-11-25/electricity-tariffs/E-1R-AGILE" \
                         "-FLEX-22-11-25-C/standard-unit-rates/"

ENERGY_PRICES_API = 'http://127.0.0.1:8000/energy_price_api/v1/energy_prices/'

MAX_CALLS = 15


def api_call(url, method, data=None):
    if data is None:
        data = {}
    print('Calling an API')
    call_count = 0

    while call_count <= MAX_CALLS:
        success = False
        if call_count == MAX_CALLS:
            raise SystemExit('API max calls exceeded')

        try:

            if method == 'GET':
                response = requests.get(url, timeout=5)
                response.raise_for_status()
                print(response.status_code)
                if response.status_code == 200:
                    success = True
                    print(response.json())
                    return response.json()
            if method == 'POST':
                response = requests.post(url, data=data)
                response.raise_for_status()
                print(response.status_code)
                if response.status_code == 201:
                    success = True

        except requests.exceptions.HTTPError as erra:
            print(erra)
            time.sleep(2 ** call_count)
            call_count += 1

        except requests.exceptions.ConnectionError as errb:
            print(errb)
            time.sleep(2 ** call_count)
            call_count += 1

        except requests.exceptions.Timeout as errc:
            print(errc)
            time.sleep(2 ** call_count)
            call_count += 1

        except requests.exceptions.RequestException as error:
            raise SystemExit('API Request error: ' + str(error)) from error

        if success:
            print('API request successful, status ' + str(response.status_code) + '.')
            break


data = api_call(OCTOPUS_ENERGY_API_URL, 'GET')

for result in data['results']:
    result.pop('value_exc_vat')
    print(result)
    api_call(ENERGY_PRICES_API, 'POST', result)
