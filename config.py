import os
from dotenv import load_dotenv

# 初始化.env
load_dotenv()

class Config:
    APP_ENV = os.getenv("APP_ENV", "production") 
    DB_USER = os.getenv("DB_USER")
    DB_PASS = os.getenv("DB_PASS")
    SSH_HOST = os.getenv("SSH_HOST")
    SSH_USER = os.getenv("SSH_USER")
    SSH_PWD = os.getenv("SSH_PWD")