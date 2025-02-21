import requests

# API Endpoint
url = "https://api.census.gov/data/2020/acs/acs5"

# Dictionary of Cities with (State FIPS, County FIPS)
cities = {
    "San Francisco, CA": ("06", "075"),
    "Los Angeles, CA": ("06", "037"),
    "New York City, NY": ("36", "061"),  # New York County (Manhattan)
    "Chicago, IL": ("17", "031"),
    "Houston, TX": ("48", "201"),
    "Miami, FL": ("12", "086"),
    "Dallas, TX": ("48", "113"),
    "Atlanta, GA": ("13", "121"),
    "Seattle, WA": ("53", "033"),
    "Boston, MA": ("25", "025"),
    "Philadelphia, PA": ("42", "101"),
    "San Diego, CA": ("06", "073"),
    "Denver, CO": ("08", "031"),
    "Phoenix, AZ": ("04", "013"),
    "Las Vegas, NV": ("32", "003"),
    "Detroit, MI": ("26", "163"),
    "Minneapolis, MN": ("27", "053"),
    "Portland, OR": ("41", "051"),
    "New Orleans, LA": ("22", "071"),
    "Washington, DC": ("11", "001"),
}

# Loop through each city and fetch data
for city, (state, county) in cities.items():
    params = {
        "get": "NAME,B01003_001E",
        "for": "tract:*",
        "in": f"state:{state} county:{county}"
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        print(f"\n🔹 Data for {city}:")
        for row in data[:5]:  # Print first 5 rows for preview
            print(row)
    else:
        print(f"Error fetching data for {city}: {response.status_code}")
