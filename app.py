from flask import Flask, Response, make_response, send_file, request
import sqlite3, hashlib, datetime

app = Flask(__name__, static_url_path="/images", static_folder="images", template_folder="templates")

"""
WebAPI 部分將資料傳送給前端
"""
### 取得所有房間資訊
@app.route('/houseInfo', methods=['GET'])
def getHouseInfo():
    with sqlite3.connect("sqlite.db") as con:
        res = con.execute("SELECT * FROM HouseInfo")
        return {"result":"success", "data": res.fetchall()}
    return {"result": "failed"}

### 取得單一房間資訊
@app.route('/houseInfo/<num>', methods=['GET'])
def getSingleHouseInfo(num):
    with sqlite3.connect("sqlite.db") as con:
        res = con.execute(f"SELECT * FROM HouseInfo WHERE houseid={num}")
        return {"result":"success", "data": res.fetchall()}
    return {"result": "failed"}

### 新增房間資訊
@app.route('/houseInfo', methods=['POST'])
def postHouseInfo():
    return {"result": "success"}

### 登入並取得登入Session
@app.route('/login', methods=['POST'])
def getLoginSession():
    # 取得帳號密碼
    username = request.json.get("username")
    password = request.json.get("password")

    # 對密碼做雜湊
    h = hashlib.new('sha256')
    h.update(password.encode('utf-8'))
    hashPassword = h.hexdigest()

    # 與資料庫密碼做比對
    with sqlite3.connect("sqlite.db") as con:
        res = con.execute(f"SELECT * FROM UserInfo WHERE username='{username}' and password='{hashPassword}'")
        userInfo = res.fetchall()
        if len(userInfo) == 0: return {"result": "failed"}

        
        # 計算 Session
        h = hashlib.new('sha256')
        h.update((username+datetime.datetime.now().__str__()).encode('utf-8'))
        session = h.hexdigest()

        # 保存 Session
        res = con.execute(f"SELECT session, date FROM Session WHERE user='{username}'")
        if len(res.fetchall()) == 0:
            con.execute(f"INSERT INTO Session(session, user, date) VALUES ('{session}','{username}','{datetime.datetime.now().__str__()}')")
            con.commit()
        else:
            con.execute(f"UPDATE Session SET session='{session}', user='{username}', date='{datetime.datetime.now().__str__()}' WHERE user='{username}'")
            con.commit()
        
        resp = make_response({"result": "success", "userName": userInfo[0][1]})
        resp.set_cookie('session', session)
        return resp

def isLogin(request):
    # 檢查 session
    with sqlite3.connect("sqlite.db") as con:
        session = request.cookies.get('session')
        res = con.execute(f"SELECT session, user, date FROM Session WHERE session='{session}'")
        userSession = res.fetchall()
        if(len(userSession) == 0): return False
        else: return True

"""
Web View 部分
"""
# 首頁網站
@app.route("/")
def home():
    return send_file("templates/home.html")

# 登入頁面
@app.route("/login")
def login():
    return send_file("templates/login.html")


if __name__ == "__main__":
    app.debug = True
    app.run("127.0.0.1", "80")