import requests

response = requests.get(
    "https://api.pullpush.io/reddit/search/comment/",
    params={"subreddit":"askreddit", "size": "10"},
)

print(response.json().get('data'))
