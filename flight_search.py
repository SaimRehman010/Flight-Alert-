from datetime import timedelta
from serpapi import GoogleSearch
from flight_data import FlightData

SERPAPI_KEY = "Your Api"

# Primary airport codes that Google Flights accepts reliably
IATA_CODES = {
    "Paris": "CDG",
    "Tokyo": "HND",
    "New York": "JFK"
}


class FlightSearch:

    def get_destination_code(self, city_name):
        return IATA_CODES.get(city_name, "")

    def check_flights(self, origin_city_code, destination_city_code, from_time, to_time):
        origin_code = "LHR" if origin_city_code == "LON" else origin_city_code
        
        outbound = from_time.strftime("%Y-%m-%d")
        return_date = (from_time + timedelta(days=7)).strftime("%Y-%m-%d")

        params = {
            "engine": "google_flights",
            "departure_id": origin_code,
            "arrival_id": destination_city_code,
            "outbound_date": outbound,
            "return_date": return_date,
            "currency": "GBP",
            "hl": "en",
            "type": "1",
            "api_key": SERPAPI_KEY
        }

        try:
            search = GoogleSearch(params)
            results = search.get_dict()

            if "error" in results:
                print(f"  ➜ SerpApi Error for {destination_city_code}: {results['error']}")
                return None

            flight_list = results.get("best_flights") or results.get("other_flights")
            
            if not flight_list:
                print(f"  ➜ No flight results key found for {destination_city_code}.")
                return None

            best_flight = flight_list[0]
            price = best_flight.get("price", 0)
            
            flights_data = best_flight.get("flights", [])
            origin_ap = flights_data[0]["departure_airport"]["id"] if flights_data else origin_code
            dest_ap = flights_data[-1]["arrival_airport"]["id"] if flights_data else destination_city_code

            return FlightData(
                price=float(price),
                origin_city=origin_code,
                origin_airport=origin_ap,
                destination_city=destination_city_code,
                destination_airport=dest_ap,
                out_date=outbound,
                return_date=return_date
            )

        except Exception as e:
            print(f"  ➜ Exception during search for {destination_city_code}: {e}")
            return None
