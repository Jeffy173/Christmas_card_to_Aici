from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional,List,Dict
import sqlite3
import hashlib
from fastapi.middleware.cors import CORSMiddleware 
from fastapi.staticfiles import StaticFiles
import os
from fastapi.responses import Response
import io
# from PIL import Image
import base64
import uuid
import time
import threading

global_lock=threading.Lock()

#create api
app=FastAPI()

# 定義可訪問的來源(CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        # 线上环境：你的Railway域名
        # "https://endearing-alignment.up.railway.app",
        # 本地开发：常见的前端开发服务器端口
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8080",
        "http://127.0.0.1:8080",
        "http://localhost:5500", # 一些Live Server的默认端口
        "http://127.0.0.1:5500",
        # "*"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# password hashing
def new_hash(s:str)->str:
    return hashlib.sha256(s.encode()).hexdigest()

# accounts and passwords -> name : hashed_key
accounts={
    "Aici":new_hash("mp042958H"),
}
import base64

def Aici_response():
    with open("backend/Aici/favicon.svg","rb") as f:
        favicon_b64 = base64.b64encode(f.read()).decode()
    with open("backend/Aici/Christmas_card_picture.jpg", "rb") as f:
        picture_b64 = base64.b64encode(f.read()).decode()
    with open("backend/Aici/gift.svg", "rb") as f:
        gift_b64 = base64.b64encode(f.read()).decode()
    with open("backend/Aici/style.css", "rb") as f:
        css_b64 = base64.b64encode(f.read()).decode()
    with open("backend/Aici/script.js", "r",encoding="utf-8") as f:
        script = f.read()
    with open("backend/Aici/index.html", "r", encoding="utf-8") as f:
        template = f.read()
    html=template.format(
        favicon=favicon_b64,
        css=css_b64,
        picture=picture_b64,
        gift=gift_b64,
        script=script
    )
    return Response(content=html, media_type="text/html")

responses={
    "Aici":Aici_response(),
}

class Talking:
    def __init__(self,id,response):
        self.id=id
        self.time=time.time()
        self.response=response

# uuids -> id : talking
talkings:Dict[str,"Talking"]={}

class Checker:
    def __init__(self):
        self.running=True
        self.T=60
    
    def check(self):
        with global_lock:
            now=time.time()
            vals=list(talkings.values())
            for talking in vals:
                if talking.time+60*5<now:
                    del talkings[talking.id]

    def execute(self):
        while self.running:
            self.check()
            time.sleep(self.T)
    
    def start(self):
        thread=threading.Thread(target=self.execute,daemon=True)
        thread.start()
    
    def stop(self):
        self.running=False

checker=Checker()
checker.start()

@app.get("/api/")
def home():
    return {"message":"the home"}

@app.get("/api/get_photo/")
def get_photo():
    with open("backend/Christmas_card_picture.jpg", "rb") as f:
        image_bytes = f.read()
    
    return Response(
        content=image_bytes,
        media_type="image/png"
    )

class Get_card_input(BaseModel):
    id:str
@app.post("/api/get_card/")
def get_card(get_card_input:Get_card_input):
    with global_lock:
        if get_card_input.id not in talkings.keys(): raise HTTPException(status_code=404,detail="account not found!")
        talking=talkings[get_card_input.id]
        return {
            "message":"get card successful!",
            "data":talking.response
            }

class Get_talking_input(BaseModel):
    name:str
    password:str
@app.post("/api/get_talking/")
def get_talking(get_talking_input:Get_talking_input):
    with global_lock:
        if get_talking_input.name not in accounts: raise HTTPException(status_code=404,detail="account not found!")
        if new_hash(get_talking_input.password)!=accounts[get_talking_input.name]: raise HTTPException(status_code=401,detail="wrong password!")
        talking=Talking(str(uuid.uuid4()).replace('-', ''),responses[get_talking_input.name])
        talkings[talking.id]=talking
        return {
            "message":"get talking successful!",
            "id":talking.id,
            }

# 靜態文件服務
app.mount("/", StaticFiles(directory="./frontend", html=True), name="frontend")

