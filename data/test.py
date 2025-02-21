import requests

# API endpoint for the dataset
api_url = "https://data.lacity.org/resource/2nrs-mtv8.json"

# Parameters (if any) can be added to filter the data
params = {
    # Example: filter by date range
    # "$where": "date_occ >= '2023-01-01T00:00:00' AND date_occ < '2024-01-01T00:00:00'"
}

# Make the GET request to fetch the data
response = requests.get(api_url, params=params)

if response.status_code == 200:
    data = response.json()
    # Process the data as needed
    print(data[:5])  # Print the first 5 records as a sample
else:
    print(f"Error: {response.status_code}")
