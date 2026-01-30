import os
import sys
from pymongo import MongoClient
from dotenv import load_dotenv
from config import Config

# 加载 .env 变量
load_dotenv()

# === 获取配置 ===
# 判断当前环境，默认是 production (线上)
app_env = Config.APP_ENV

db_user = Config.DB_USER
db_pass = Config.DB_PASS
mongo_db_name = 'mydb' # 你的数据库名

# 定义全局变量，防止连接丢失
mongo_client = None
ssh_server = None

def get_db_connection():
    global mongo_client, ssh_server
    
    # 如果已经连接过，直接返回（避免重复连接）
    if mongo_client:
        return mongo_client[mongo_db_name]

    mongo_port = 27017 # 默认端口

    # === 分支 A: 本地开发环境 (开启 SSH 隧道) ===
    if app_env == 'local':
        print(f"🔧 检测到本地环境 (APP_ENV={app_env})，正在启动 SSH 隧道...")
        try:
            from sshtunnel import SSHTunnelForwarder
            
            ssh_host = Config.SSH_HOST
            ssh_user = Config.SSH_USER
            ssh_pass = Config.SSH_PWD
            
            # 创建隧道
            ssh_server = SSHTunnelForwarder(
                (ssh_host, 22),
                ssh_username=ssh_user,
                ssh_password=ssh_pass,
                remote_bind_address=('127.0.0.1', 27017)
            )
            ssh_server.start()
            
            # 【关键点】本地连接时，端口要变成隧道分配的随机端口
            mongo_port = ssh_server.local_bind_port
            print(f"✅ SSH 隧道建立成功！本地映射端口: {mongo_port}")
            
        except ImportError:
            print("❌ 错误: 本地模式需要安装 sshtunnel (pip install sshtunnel)")
            sys.exit(1)
        except Exception as e:
            print(f"❌ SSH 连接失败: {e}")
            sys.exit(1)

    # === 分支 B: 线上/通用连接逻辑 ===
    else:
        print(f"🚀 检测到线上环境 (APP_ENV={app_env})，准备直连数据库...")

    # === 统一连接 MongoDB ===
    try:
        print(f"⏳ 正在连接 MongoDB (Port: {mongo_port})...")
        mongo_client = MongoClient(
            host='127.0.0.1', # 无论是本地(通过隧道)还是线上(本机)，最终都是连 127.0.0.1
            port=mongo_port,
            username=db_user,
            password=db_pass,
            authSource=mongo_db_name
        )
        # 测试连通性
        mongo_client[mongo_db_name].command('ping')
        print("✅ MongoDB 连接成功！")
        
        return mongo_client[mongo_db_name]
        
    except Exception as e:
        print(f"❌ 数据库连接失败: {e}")
        # 如果是线上环境，这里失败可能是密码错或服务没起
        sys.exit(1)

# 初始化数据库对象，供其他文件 import
# 例如: from db import db
db = get_db_connection()
collection = db['users']