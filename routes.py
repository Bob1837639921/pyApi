from flask import Blueprint, request
from bson.objectid import ObjectId
from db import collection # 👈 记得在这一层引入数据库！

# 加密工具
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required


# 创建一个蓝图对象 (名字叫 'api'，随意起)
api_bp = Blueprint('api', __name__)

# ... 之前的代码 ...

# === 🆕 注册接口 (创建管理员) ===
@api_bp.route('/register', methods=['POST'])
def register():
    data = request.form.to_dict()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return {"msg": "账号密码不能为空"}, 400

    # 1. 检查账号是否已存在
    if collection.find_one({"username": username}):
        return {"msg": "这个账号已经被人注册啦！"}, 400

    # 2. 🔐 关键步骤：把密码变成乱码 (Hash)
    # 比如输入 "123456"，存进去的是 "pbkdf2:sha256:..."
    hashed_password = generate_password_hash(password)

    # 3. 存入数据库 (注意存的是 hash 过的密码)
    user_data = {"username": username, "password": hashed_password, "is_admin": True}
    collection.insert_one(user_data)

    return {"msg": "注册成功！请去登录"}

# === 🆕 登录接口 (获取 Token 手环) ===
@api_bp.route('/login', methods=['POST'])
def login():
    data = request.form.to_dict()
    username = data.get('username')
    password = data.get('password')

    # 1. 去数据库找这个人
    user = collection.find_one({"username": username})

    # 2. 验证：人存在 且 密码匹配 (用 check_password_hash 也就是把钥匙插进锁里试)
    if user and check_password_hash(user['password'], password):
        # ✅ 3. 登录成功，发个手环 (Token)
        # identity 记录你是谁，可以是 ID 或 用户名
        access_token = create_access_token(identity=username)
        return {"msg": "登录成功", "token": access_token}
    
    return {"msg": "账号或密码错误！"}, 401

# ... 后面是你之前的 add_user, find_user ...
    

@api_bp.route('/add_user', methods = ["POST"])
def add_user_api():
    data = request.form.to_dict()
    data["age"] = int(data["age"])
    print('我收到了', data)
    collection.insert_one(data)
    return {"message": "添加成功了"}

@api_bp.route('/find_user')
def find_user_api():
    query = {}
    field_map = {
        "name": str,
        "age": int
    }
    for i in field_map:
        item = request.args.get(i)
        if item:
            query[i] = field_map[i](item)
    print(query)
    result = collection.find(query)
    user_list = list(result)
    new_list = []
    for i in user_list:
        new_data = {"id": str(i["_id"]), **i}
        del new_data["_id"]
        new_list.append(new_data)
    return {"data": new_list, "msg": '请求成功'}

@api_bp.route('/delete_user', methods = ["DELETE"])
@jwt_required()
def delete_user_api():
    del_id = request.form.get("id")
    if not del_id:
        return {"message": "请输入正确的用户ID"}
    collection.delete_one({"_id": ObjectId(del_id)})
    return {"message": "删除成功了"}


@api_bp.route('/update_user', methods=["PUT"])
def update_user_api():
    data_filter = request.form.to_dict()
    query = {}
    update_data = {}
    if data_filter.get("name"):
        query["name"] = data_filter["name"] 
    else:
        return {"message": "请输入姓名"}
    if data_filter.get("age"):
        update_data["age"] = int(data_filter["age"])
    result = collection.update_many(query, {"$set": update_data})
    return {"message": f"找到了{result.matched_count}条数据，更新成功了 {result.modified_count} 条数据"}
