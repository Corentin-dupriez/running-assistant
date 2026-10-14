import requests

url = "https://www.strava.com/api/v3/athlete/activities"

resp = requests.get(url)

print(resp.content)
