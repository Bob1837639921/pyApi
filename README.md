# Python Flask API Project

这是一个基于 Python Flask 框架开发的 Web API 项目，集成了 MongoDB 数据库操作、JWT 用户认证以及通过 SSH 隧道安全连接远程数据库的功能。

## 🛠 技术栈

- **Web 框架**: Flask
- **数据库**: MongoDB (使用 `pymongo` 驱动)
- **认证**: Flask-JWT-Extended (JWT Token)
- **安全**: SSH Tunnel (通过 SSH 隧道连接数据库), Werkzeug (密码哈希)
- **环境配置**: python-dotenv

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone <repository-url>
cd <project-directory>
```

### 2. 安装依赖

建议使用虚拟环境：

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境 (Windows)
venv\Scripts\activate

# 激活虚拟环境 (macOS/Linux)
source venv/bin/activate
```

安装项目依赖：

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量

在项目根目录下创建一个 `.env` 文件，并填入以下配置信息：

```ini
# SSH 服务器配置 (用于连接远程数据库)
SSH_HOST=你的远程服务器IP
SSH_USER=你的SSH用户名
SSH_PWD=你的SSH密码

# JWT 配置
JWT_SECRET=你的JWT密钥(随便填一串复杂的字符串)

# 数据库配置 (如果在 db.py 中硬编码了，这里可能不需要，建议检查 db.py)
# 这里的代码示例中数据库用户和密码是在 db.py 中设置的，请根据实际情况修改 db.py 或将其移入 .env
```

### 4. 运行项目

```bash
python app.py
```

项目默认运行在 `http://127.0.0.1:5000`。

## 📚 API 接口文档

### 用户认证

#### 1. 注册用户
- **URL**: `/register`
- **Method**: `POST`
- **参数 (Form Data)**:
    - `username`: 用户名
    - `password`: 密码
- **描述**: 创建新用户，密码会进行加密存储。

#### 2. 用户登录
- **URL**: `/login`
- **Method**: `POST`
- **参数 (Form Data)**:
    - `username`: 用户名
    - `password`: 密码
- **描述**: 验证用户身份，成功后返回 `token`。

### 用户管理

#### 3. 添加用户
- **URL**: `/add_user`
- **Method**: `POST`
- **参数 (Form Data)**:
    - `name`: 姓名
    - `age`: 年龄
    - ...其他字段
- **描述**: 向数据库添加一条用户记录。

#### 4. 查询用户
- **URL**: `/find_user`
- **Method**: `GET`
- **参数 (Query Params)**:
    - `name`: (可选) 按姓名筛选
    - `age`: (可选) 按年龄筛选
- **描述**: 获取用户列表。

#### 5. 删除用户 (需要认证)
- **URL**: `/delete_user`
- **Method**: `DELETE`
- **Header**:
    - `Authorization`: `Bearer <你的Token>`
- **参数 (Form Data)**:
    - `id`: 要删除的用户 ID
- **描述**: 删除指定用户。需要先登录获取 Token，并在请求头中携带。

#### 6. 更新用户 (开发中)
- **URL**: `/update_user`
- **Method**: `PUT`
- **描述**: 更新用户信息接口。

## ⚠️ 注意事项

- 本项目使用了 SSH 隧道连接数据库，请确保你的开发环境能够访问配置的 SSH 服务器。
- 首次运行时，SSH 连接可能需要几秒钟建立，请耐心等待控制台输出 "✅ 数据库连接成功"。
