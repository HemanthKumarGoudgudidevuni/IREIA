import requests
import json

# API endpoint
base_url = "https://data.lacity.org/resource/2nrs-mtv8.json"

# Configuration
all_data = []  # List to store all records
limit = 1000   # Number of records per request
offset = 0     # Start from the first record
max_records = 5000  # Set max record limit (Reduced for safety)

while offset < max_records:
    print(f"Fetching records from {offset} to {offset + limit}...")

    params = {
        "$limit": limit,  # Number of records per request
        "$offset": offset  # Offset for pagination
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()

        if not data:  # If no more data, stop fetching
            print("No more data available. Stopping fetch.")
            break

        all_data.extend(data)  # Append data to the list
        offset += limit  # Move to the next batch

    else:
        print(f"Error: {response.status_code}, {response.text}")
        break

# # Save data to a JSON file
# with open("crime_data.json", "w") as f:
#     json.dump(all_data, f, indent=4)

# Print all fetched data (Warning: Can be large)
print(json.dumps(all_data, indent=4))

# print(f"Total records fetched: {len(all_data)}")
