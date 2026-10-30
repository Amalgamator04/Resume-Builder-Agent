import requests


username = "Amalgamator04"
url = f"https://api.github.com/users/{username}/repos"


response = requests.get(url)
repos = response.json()


for repo in repos:
    print("\n")

    print(f"Name: {repo['name']}")

    print(f"Description: {repo['description']}")

    print(f"URL: {repo['html_url']}")

    print("\n")
