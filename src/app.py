from dotenv import load_dotenv
from functools import lru_cache
import pathlib
from fastapi import FastAPI,Request,Form 
from fastapi.templating import Jinja2Templates
from .airtable import Airtable
import os

BASE_DIR = pathlib.Path(__file__).parent ## this is the src/ 


app = FastAPI()
templates = Jinja2Templates(directory = BASE_DIR/"templates")

@lru_cache()
def cached_dotenv():
    load_dotenv()


cached_dotenv()



AIRTABLE_BASE_ID = os.environ.get("AIRTABLE_BASE_ID")
AIRTABLE_API_KEY = os.environ.get("AIRTABLE_API_KEY")
AIRTABLE_TABLE_NAME = os.environ.get("AIRTABLE_TABLE_NAME")





@app.get("/")
def home_view(request: Request):
    return  templates.TemplateResponse("home.html", {"request": request})

@app.post("/")
def home_signup_view(request: Request, email:str = Form(...)):


    airtable_client = Airtable(
        base_id = AIRTABLE_BASE_ID,
        api_key = AIRTABLE_API_KEY,
        table_name = AIRTABLE_TABLE_NAME,
    )
            
    did_send = airtable_client.create_records({"email_added":email})

    return templates.TemplateResponse("home.html", {
        "request": request,
        "submitted_email":email,
        "did_send" : did_send })