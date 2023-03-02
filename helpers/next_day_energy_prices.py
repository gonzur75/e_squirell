import requests
import time

# Using random UK octopus energy tariff, until suitable Polish alternative is available
API_URL = "https://api.octopus.energy/v1/products/AGILE-FLEX-22-11-25/electricity-tariffs/E-1R-AGILE-FLEX-22-11-25-C/standard-unit-rates/"
MAX_CALLS = 15


def api_call_for_energy_prices(url):
    print('Calling an API')
    call_count = 0

    while call_count <= MAX_CALLS:

        if call_count == MAX_CALLS:
            raise SystemExit('API max calls exceeded')

        try:
            success = False
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            if response.status_code == 200:
                success = True
                print(response.json())
                return response.json()

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

api_call_for_energy_prices(API_URL)
