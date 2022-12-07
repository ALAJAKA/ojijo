from flask import Flask, render_template, request, jsonify, session, redirect, url_for
app = Flask(__name__)

import pymysql.cursors
import bcrypt

# 디비 연결하기
db = pymysql.connect(host="localhost",
                     port=3306,
                     user="",
                     db='ojijo',
                     password='',
                     charset='utf8')

app.secret_key = "#@!RFW12adnuiasfWE@!$2"
#메인페이지
@app.route("/", methods=["GET","POST"])
def home():
  return render_template('main.html')

@app.route("/login", methods=["GET","POST"])
def login():
  a = bool(session)
  if a :
    return redirect(url_for("home"))
  if request.method == 'GET':
    return render_template('login.html')
  elif request.method == 'POST':
    user_id = request.form['user_id']
    user_pw = request.form['password'].encode('utf-8')
    curs = db.cursor(pymysql.cursors.DictCursor)
    sql = "SELECT * FROM users WHERE user_id = %s"
    curs.execute(sql,(user_id))
    user = curs.fetchone()
    curs.close()
    print(user)
    if user == None:
      return "아이디가 틀렸습니다"

    if len(user) > 0:
      if bcrypt.hashpw(user_pw,user['user_pw'].encode('utf-8')) == user['user_pw'].encode('utf-8'):
        session['user_nk'] = user['user_nk']
        session['user_id'] = user['user_id']
        print(session['user_nk'])
        print(session['user_id'])
        return redirect(url_for("home"))
      else:
        return "에러발생"
@app.route('/logout', methods=['GET'])
def logout():
  session.clear()
  return redirect(url_for("home"))


@app.route("/join", methods=["GET","POST"])
def join():
  a = bool(session)
  if a :
    return redirect(url_for("home"))
  if request.method == 'GET':
    return render_template('join.html')
  else:
    user_id = request.form['user_id']
    user_email = request.form['email']
    user_password = request.form['password'].encode('utf-8')
    hash_password = bcrypt.hashpw(user_password, bcrypt.gensalt())
    user_name = request.form['name']
    user_nk = request.form['nk']

    curs = db.cursor()
    sql = "insert into users (user_id,user_pw,user_name,user_email,user_nk) values (%s,%s,%s,%s,%s)"
    print(sql)
    curs.execute(sql,(user_id,hash_password,user_name,user_email,user_nk))
    db.commit()
    curs.close()
    return jsonify({'msg':'가입완료'})

@app.route("/board", methods=["GET","POST"])
def board():
  return render_template('board.html')

@app.route("/mypage", methods=["GET","POST"])
def mypage():
  return render_template('mypage.html')

@app.route("/personal", methods=["GET","POST"])
def personal():
  return render_template('personal.html')

@app.route("/write", methods=["GET","POST"])
def write():
  return render_template('post_write.html')

if __name__ == '__main__':
    app.run(debug=True)

