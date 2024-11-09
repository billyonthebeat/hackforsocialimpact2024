import requests
import json

def test_almanac_connection():
    """Test connection to Fetch.ai Almanac"""
    try:
        response = requests.get("https://agentverse.ai/health")
        print(f"Connection test result: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Connection error: {str(e)}")

if __name__ == "__main__":
    test_almanac_connection()