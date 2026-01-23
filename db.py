from pymongo import MongoClient
from sshtunnel import SSHTunnelForwarder
import os
from dotenv import load_dotenv
load_dotenv()
# === 1. 设置登录信息 ===
# 服务器的 IP 地址
ssh_ip = os.getenv("SSH_HOST")
# SSH 登录账号（通常是 root）
ssh_user = os.getenv("SSH_USER")
# SSH 登录密码（也就是你远程连接 Linux 服务器的密码）
ssh_pass = os.getenv("SSH_PWD")  # <--- 【注意】这里填你用来登录黑框框的密码！

# 数据库账号密码
db_user = 'user1'
db_pass = 'xym123' # 你的数据库密码

print("⏳ 正在建立 SSH 安全隧道...")

try:
    # 创建隧道
    server = SSHTunnelForwarder(
        (ssh_ip, 22),
        ssh_username=ssh_user,
        ssh_password=ssh_pass,
        remote_bind_address=('127.0.0.1', 27017) # 告诉服务器：帮我连你自己内部的数据库
    )
    
    server.start() # 启动隧道
    print(f"✅ SSH 隧道建立成功！本地入口端口: {server.local_bind_port}")

    # === 2. 连接数据库 (连接隧道的本地入口) ===
    client = MongoClient(
        host='127.0.0.1',             # 注意：这里写本地 IP
        port=server.local_bind_port,  # 这里用隧道分配的端口
        username=db_user,
        password=db_pass,
        authSource='mydb',
    )
    
    # 测试连接
    print("⏳ 正在尝试连接数据库...")
    client.mydb.command('ping')
    print("✅ 数据库连接成功！(通过 SSH 安全隧道)")
        # 赋值给全局变量，方便后面使用
    db = client['mydb'] 
    collection = db['users'] # 或者你之前的 collection 名字
except Exception as e:
    print("❌ 连接出错啦:", e)
    # 如果是 SSH 验证失败，记得检查 ssh_pass 填对了没