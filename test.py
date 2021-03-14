import requests

url = "https://kong-tatasky.videoready.tv/auth-service/v1/oauth/token-service/token"

payload="{\n    \"action\":\"stream\",\n    \"epids\":[{\"epid\":\"Subscription\",\"bid\":\"1000000174\"}]\n}"
headers = {
  'Authorization': 'bearer 8ld7nbdC4zyd93sPLf51B4AjAxzxwNhb',
  'x-subscriber-id': '1267784138',
  'x-app-id': 'ott-app',
  'x-app-key': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcHBJZCI6ImR2ci11aSIsImtleSI6IiJ9.XUQUYRo82fD_6yZ9ZEWcJkc0Os1IKbpzynLzSRtQJ-E',
  'x-subscriber-name': 'Mohamed Ali',
  'x-api-key': '9a8087f911b248c7945b926f254c833b',
  'x-device-id': 'YVJNVFZWVlZ7S01UZmRZTWNNQ3lHe0RvS0VYS0NHSwA',
  'x-device-platform': 'MOBILE',
  'x-device-type': 'ANDROID',
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)