import requests

# API Endpoint
url = "https://data.police.uk/api/crimes-street/all-crime"
params = {
    "lat": 52.629729,  # Latitude
    "lng": -1.131592,  # Longitude
    "date": "2022-02"  # Year-Month format
}

# Send GET request
response = requests.get(url, params=params)

# Check if request was successful
if response.status_code == 200:
    crime_data = response.json()  # Convert JSON response to Python dictionary
    print("Crime Data Retrieved Successfully!")

    # Print first 5 records
    for i, crime in enumerate(crime_data[:5]):
        print(f"{i+1}. {crime['category'].title()} - {crime['location']['street']['name']}")
else:
    print(f"Error: {response.status_code}, {response.text}")
