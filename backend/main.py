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

# 靜態文件服務
app.mount("/", StaticFiles(directory="./Aici", html=True), name="frontend")

