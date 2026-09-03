from datetime import datetime, timedelta
from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager

print("🚀 Starting Flight Deal Finder...")

data_manager = DataManager()
sheet_data = data_manager.get_destination_data()
flight_search = FlightSearch()
notification_manager = NotificationManager()

ORIGIN_CITY_IATA = "LON"

print(f"📊 Raw sheet data received: {sheet_data}")

# 1. Resolve primary airport codes
for row in sheet_data:
    city = row.get("city")
    if city:
        code = flight_search.get_destination_code(city)
        if code:
            row["iataCode"] = code
            print(f"🔍 Airport code for {city}: {code}")

data_manager.destination_data = sheet_data
data_manager.update_destination_codes()

# 2. Search flights starting tomorrow for a 7-day duration
tomorrow = datetime.now() + timedelta(days=1)
six_months_later = datetime.now() + timedelta(days=180)

for destination in sheet_data:
    city_name = destination.get("city")
    iata_code = destination.get("iataCode")
    lowest_price = destination.get("lowestPrice", 0)

    if city_name and iata_code:
        print(f"✈️ Checking flights for {city_name} ({iata_code})...")
        flight = flight_search.check_flights(
            ORIGIN_CITY_IATA,
            iata_code,
            from_time=tomorrow,
            to_time=six_months_later
        )
        
        if flight and flight.price < lowest_price:
            print(f"🎉 Deal found for {city_name}! Sending email...")
            email_body = (
                f"Low price alert! Only £{flight.price} to fly from "
                f"{flight.origin_city}-{flight.origin_airport} to "
                f"{flight.destination_city}-{flight.destination_airport}, "
                f"from {flight.out_date} to {flight.return_date}."
            )
            notification_manager.send_email(message=email_body)
        else:
            current_price = f"£{flight.price}" if flight else "£N/A"
            print(f"❌ No deal for {city_name} (Current lowest: {current_price}, Budget: £{lowest_price}).")
    else:
        print(f"⚠️ Skipped entry: Missing city or IATA code.")

print("✅ Run completed!")