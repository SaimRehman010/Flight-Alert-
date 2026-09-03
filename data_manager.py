import requests

SHEETY_PRICES_ENDPOINT = "https://api.sheety.co/48d0c5e54a26cbeaae3e074bc543c254/flightDealFinder/prices"


class DataManager:

    def __init__(self):
        self.destination_data = []

    def get_destination_data(self):
        response = requests.get(url=SHEETY_PRICES_ENDPOINT)
        data = response.json()
        first_key = list(data.keys())[0]
        self.destination_data = data[first_key]
        return self.destination_data

    def update_destination_codes(self):
        for city in self.destination_data:
            city_id = city.get("id")
            if city_id:
                iata_code = city.get("iataCode", "")
                
                # Payload key MUST be singular "price" for a "/prices" endpoint
                new_data = {
                    "price": {
                        "iataCode": iata_code
                    }
                }
                response = requests.put(
                    url=f"{SHEETY_PRICES_ENDPOINT}/{city_id}",
                    json=new_data
                )
                
                if response.status_code == 200:
                    print(f"✅ Updated {city.get('city')}: Status 200")
                else:
                    print(f"❌ Failed {city.get('city')}: Status {response.status_code}")
                    print(f"   Response details: {response.text}")