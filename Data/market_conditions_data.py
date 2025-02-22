import requests
import json

API_KEY = "58A9EE4A-34FA-4395-8BE9-B35312BE0D34"
BASE_URL = "https://apps.bea.gov/api/data"

params = {
    "UserID": API_KEY,
    "method": "GetData",
    "datasetname": "NIPA",
    "TableName": "T10101",
    "Frequency": "Q",
    "Year": "2023",  # Try "X" if this doesn't work
    "ResultFormat": "json"
}

response = requests.get(BASE_URL, params=params)

if response.status_code == 200:
    data = response.json()
    print("Full API Response:\n", json.dumps(data, indent=4))  # Print full response for debugging
    
    gdp_data = data.get("BEAAPI", {}).get("Results", {}).get("Data", [])

    if gdp_data:
        print("\n--- U.S. GDP Data (Quarterly) ---\n")
        for entry in gdp_data:
            print(f"Period: {entry['TimePeriod']} | GDP: {entry['DataValue']} Billion USD")
    else:
        print("No data found for the specified parameters.")
else:
    print("Error:", response.status_code, response.text)
