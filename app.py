from flask import Flask, Response, send_file
import sqlite3

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

"""
Web View 部分
"""
# 首頁網站
@app.route("/")
def home():
    return send_file("templates/home.html")


if __name__ == "__main__":
    app.debug = True
    app.run("127.0.0.1", "80")