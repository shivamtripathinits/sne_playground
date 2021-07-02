from fastapi import FastAPI,Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.cors import ALL_METHODS
from starlette.responses import Response
from schemas.fns import serializeDict,serializeList
from fastapi.templating import Jinja2Templates
from config.db import conn 
import json
import scraper_date
from fastapi_utils.tasks import repeat_every
import scraper


origins = [
    "http://localhost:3000",
]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
template=Jinja2Templates(directory="htmldirectory")

@app.get("/")
async def index(request: Request):    
    kk=serializeList(conn.scraps.scrap_items.find())
    kkk= json.dumps(kk, indent = 4)  
    return kk

@app.on_event("startup")
@repeat_every(seconds=60 * 60)  # 1 hour
def printit():
  scraper_date.main_scraper()