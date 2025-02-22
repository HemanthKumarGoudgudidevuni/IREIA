import requests

# Define API key and base URL
API_KEY = "KEtM2ilbCufWDbZ07ZOoMimRORB9KFoVpu0EoqyD"
BASE_URL = "https://api.data.gov/ed/collegescorecard/v1/schools.json"

# List of states to query
states = ["CA", "TX", "NY"]  # Example: California, Texas, New York

# Parameters common for all requests
common_params = {
    "api_key": API_KEY,
    "fields": "id,school.name,school.city,school.state,latest.admissions.sat_scores.average.overall",
    "per_page": 100  # Number of results per state
}

# Collect all results
all_schools = []

for state in states:
    params = common_params.copy()
    params["school.state"] = state  # Fetch data for each state separately

    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        all_schools.extend(data.get("results", []))  # Append results for each state
    else:
        print(f"Error fetching data for {state}: {response.status_code}")

# Display results
for school in all_schools:
    print(f"ID: {school.get('id')}")
    print(f"Name: {school.get('school.name')}")
    print(f"City: {school.get('school.city')}, State: {school.get('school.state')}")
    print(f"Avg SAT Score: {school.get('latest.admissions.sat_scores.average.overall', 'N/A')}")
    print("-" * 40)
