# Ani-Home 0.0.1
# it suppossed to be a backend for site, but it's not ready yet

import os
import json
import requests
from tempfile import mkdtemp
from subprocess import run, PIPE

agent=""
anime_refr=""
anime_base=""
anime_api=""
anime_mode=""

def search_anime(query, anime_api, anime_refr, anime_agent, anime_mode):
    search_gql = """
    query($search: SearchInput, $limit: Int, $page: Int, $translationType: VaildTranslationTypeEnumType, $countryOrigin: VaildCountryOriginEnumType) {
        shows(search: $search, limit: $limit, page: $page, translationType: $translationType, countryOrigin: $countryOrigin) {
            edges {
                _id
                name
                availableEpisodes
                __typename
            }
        }
    }
    """
    
    variables = {
        "search": {
            "allowAdult": False,
            "allowUnknown": False,
            "query": query
        },
        "limit": 40,
        "page": 1,
        "translationType": anime_mode,
        "countryOrigin": "ALL"
    }
    
    headers = {
        'User-Agent': anime_agent,
        'Content-Type': 'application/json',
        'Referer': anime_refr
    }
    
    params = {
        'query': search_gql,
        'variables': json.dumps(variables)
    }
    
    try:
        response = requests.get(f"{anime_api}/api", headers=headers, params=params)
        response.raise_for_status()
        
        if response.status_code == 200:
            data = response.json()
            shows = data.get('data', {}).get('shows', {}).get('edges', [])

            results = []
            for show in shows:
                show_id = show.get('_id', '')
                name = show.get('name', '')
                available_episodes = show.get('availableEpisodes', 0)
                results.append(f"{show_id}\t{name} ({available_episodes} episodes)")
            
            return "\n".join(results)
        else:
            return f"Error: Received status code {response.status_code}"
    
    except requests.exceptions.HTTPError as http_err:
        return f"HTTP error occurred: {http_err}"
    except Exception as err:
        return f"Other error occurred: {err}"

query = input("Enter anime: ")
result = search_anime(query, anime_api, anime_refr, anime_agent, anime_mode)

title = result.split()[1]
id = result.split()[0]

print(title)
print(id)
