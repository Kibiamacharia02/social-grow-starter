import os
import requests
from dotenv import load_dotenv
load_dotenv()

GRAPH_API_BASE = "https://graph.facebook.com/v17.0"

def create_media_container(ig_user_id: str, image_url: str, caption: str, access_token: str):
    url = f"{GRAPH_API_BASE}/{ig_user_id}/media"
    params = {"image_url": image_url, "caption": caption, "access_token": access_token}
    r = requests.post(url, params=params)
    r.raise_for_status()
    return r.json().get("id")

def publish_media(ig_user_id: str, creation_id: str, access_token: str):
    url = f"{GRAPH_API_BASE}/{ig_user_id}/media_publish"
    params = {"creation_id": creation_id, "access_token": access_token}
    r = requests.post(url, params=params)
    r.raise_for_status()
    return r.json()
