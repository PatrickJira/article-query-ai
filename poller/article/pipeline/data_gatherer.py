from urllib.parse import quote_plus
import requests
import datetime

nuks_token = '57a66138938d7be50285f274c57d44266805285b0f4e25e2678c35e52df1a0c5628e9b7ab0440ce0de8d6a5ea2b5da5d21a64e077ec950439192eece3fee9b44482a2eb6ae4ebaefa3b1297aca2a54d79ab16c207a837a8415db0bb3d1bc1778ef5156568b442399a679b9ae03ac1fe245264d8e93425e637528abbfcbf3e9b5'

def get_articles(query: str):
    url = f'https://editors.spacebar.th/api/articles?{query}'
    response = requests.get(url, headers={'Authorization': f'Bearer {nuks_token}'})
    return response.json()

def obj_to_querystring(obj, parent_key=''):
    parts = []
    for key, value in obj.items():
        if isinstance(value, dict):
            if parent_key:
                next_key = f"{parent_key}[{key}]"
            else:
                next_key = key
            parts.append(obj_to_querystring(value, next_key))
        elif isinstance(value, bool):
            parts.append(f"{parent_key}[{key}]=" +
                         ("true" if value else "false"))
        elif value == '*':
            parts.append(f"{parent_key}[{key}]=*")
        elif value is not None:
            parts.append(f"{parent_key}[{key}]={quote_plus(str(value))}")
    return '&'.join(parts)

from datetime import datetime, timedelta

def generate_get_by_date_query_string(date, page=1, pageSize=50):
    # Parse the input date string
    date_obj = datetime.strptime(date, "%Y-%m-%d")
    
    start_time = date_obj + timedelta(hours=-7)
    
    end_time = date_obj + timedelta(hours=17)
    
    filters = {
        "$and": [
            {
                "publishedAt": {
                    "$gte": start_time.isoformat(),
                },
            },
            {
                "publishedAt": {
                    "$lt": end_time.isoformat(),
                },
            },
        ]
    }
    return generate_query_string(page, pageSize, filters)

def generate_query_string(page=1, pageSize=50, filters={}):

    # Your JavaScript object converted to a Python dictionary
    js_object = {
        "filters": filters,
        "populate": {
            # "hero": {"populate": "*"},
            "categories": True,
            "tags": True,
            "highlights": True,
            "contents": {
                "populate": "*",
                "on": {
                    # "article.content-image": True,
                    "article.richtext": True,
                    "article.quote": True,
                    "article.html": True,
                    # "article.single-image": {"populate": "*"},
                    # "article.multiple-images": {"populate": "*"},
                    # "article.youtube-video": True,
                    # "article.facebook-embed": True,
                    # "article.instagram-embed": True,
                    # "article.spotify-album": True,
                    # "article.spotify-playlist": True,
                    # "article.spotify-track": True,
                    # "article.tiktok-embed": True,
                    # "article.twitter-embed": True,
                },
            },
            "credits": {
                "populate": {
                    "credit": {
                        "populate": {
                            "collaborator": True,
                            "title": True,
                        },
                    },
                },
            },
            "share": {"populate": "*"},
            "references": True,
        },
        "sort": {"publishedAt": "desc"},
        "pagination": {
            "page": page,
            "pageSize": pageSize,
        },
    }

    # Convert the object to a query string
    return obj_to_querystring(js_object)