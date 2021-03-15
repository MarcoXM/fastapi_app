import os
import requests

AIRTABLE_BASE_ID = os.environ.get("AIRTABLE_BASE_ID")
AIRTABLE_API_KEY = os.environ.get("AIRTABLE_API_KEY")
AIRTABLE_TABLE_NAME = os.environ.get("AIRTABLE_TABLE_NAME")

def push_to_airtable(email=None):
    if email is None:
        return False
    end_point = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_NAME}"

    header = {
        "Authorization": "Bearer {AIRTABLE_API_KEY}" ,
        "Content-Type": "application/json"
    }

    data = {
    "records": [
        {
        "fields": {}
        },
        {
        "fields": {
            "email_added":email
        }
        }
    ]
    }

    r = requests.post(end_point, json = data, headers= header)
    return r.status_code == 200 or r.status_code == 201
