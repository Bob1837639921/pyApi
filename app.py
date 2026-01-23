from flask import Flask
from routes import api_bp # 👈 引入你刚写的蓝图
from flask_jwt_extended import JWTManager
import os
from dotenv import load_dotenv # 引入加载器

load_dotenv() # 1. 加载 .env 文件里的内容
app = Flask(__name__)
app.json.sort_keys = False
app.json.ensure_ascii = False

# 2. 使用 os.getenv 读取
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET")

jwt = JWTManager(app)
# 注册蓝图 (把分店挂载到总店下)
app.register_blueprint(api_bp)

if __name__ == '__main__':
    app.run(debug=True, port=5000)