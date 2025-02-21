import requests
import os

# Store your API keys securely (Recommended)
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAADbWzQEAAAAA55mk4VRkZRPjXjLbiow5S%2B3lw1Q%3DTH2duhfZix0DBPQEWw08fuTEx7waNwUIAAItzetRs6C0UCUYCq"

# Twitter API Endpoint for Searching Tweets
url = "https://api.twitter.com/2/tweets/search/recent"

# Define search query (Adjust as needed)
params = {
    "query": "(stock market OR investing OR crypto) lang:en",  # Search keywords
    "tweet.fields": "created_at,text,public_metrics",  # Fetch extra data
    "max_results": 10  # Number of tweets
}

# Set up authorization header
headers = {"Authorization": f"Bearer {BEARER_TOKEN}"}

# Make request to Twitter API
response = requests.get(url, headers=headers, params=params)

# Check response
if response.status_code == 200:
    tweets = response.json()
    for tweet in tweets.get("data", []):
        print(f"\n🔹 {tweet['text']} \n🕒 {tweet['created_at']}")
else:
    print(f"Error {response.status_code}: {response.text}")
