import requests

# Define API key
API_KEY = "5d2b8571d494a60fe31e59c7e0937d505f8787f2"

# Request county-level data instead of state-level
API_URL = f"https://api.census.gov/data/2022/cbp?get=GEO_ID,NAME,EMP&for=county:*&key={API_KEY}"

# Make the request
response = requests.get(API_URL)

# Debugging: Print request details
print(f"Requesting URL: {response.url}")
print(f"Response Status Code: {response.status_code}")

# Check response
if response.status_code == 200:
    try:
        data = response.json()
        print("\n✅ API Response:")

        # Print the first 1000 records
        for row in data[:1000]:  
            print(row)

    except requests.exceptions.JSONDecodeError:
        print("Error: Unable to decode JSON. Response text:", response.text)
else:
    print(f" Error {response.status_code}: {response.text}")  
