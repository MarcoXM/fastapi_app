import os
import requests
from dataclasses import dataclass



@dataclass()
class Airtable:
    base_id:str 
    api_key:str
    table_name:str

    def create_records(self, data = {}):
        if len(data) == 0:
            return False
        end_point = f"https://api.airtable.com/v0/{self.base_id}/{self.table_name}"

        header = {
            "Authorization": f"Bearer {self.api_key}" ,
            "Content-Type": "application/json"
        }

        json_data = {
        "records": [
            {
            "fields": data
            }
        ]
        }

        r = requests.post(end_point, json = json_data, headers= header)
        print(end_point, r.json())

        return r.status_code == 200 or r.status_code == 201
