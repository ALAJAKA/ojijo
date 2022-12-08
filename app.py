from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import os
import shutil

app = Flask(__name__)

# [id:a,pw:b] 라인 딕셔너리 형식으로 받아오기 참고A
# [a,b]
import pymysql.cursors

# 패스워드를 저장시 암호화 해쉬로!  참고B
import bcrypt

# timedelta 는 정해진 시간을 표현하기 위해 사용됩니다.
from datetime import timedelta

# 디비 연결하기
db = pymysql.connect(host="localhost",
                     port=3306,
                     user="",
                     db='ojijo',
                     password='',
                     charset='utf8')
cur = db.cursor(pymysql.cursors.DictCursor)

# 해쉬화를 위해 필요
app.secret_key = "#@!RFW12adnuiasfWE@!$2"

# session 의 지속 시간을 정함. 해당 시간이 지나면 세션은 만료됨.
app.permanent_session_lifetime = timedelta(hours=1)


# 메인페이지
@app.route("/", methods=["GET", "POST"])  # app.route("/" <- 경로 설정
def home():  # 함수명은 중복이 불가
  return render_template('main.html')

@app.route("/getMain", methods=["GET"])
def getMain():
  # 1. 보드테이블 모든 게시물 정보를 가져온다
  cur = db.cursor(pymysql.cursors.DictCursor) #장바구니
  sql = "SELECT * FROM board"
  cur.execute(sql)
  # 2. 변수에 담는다
  curs = cur.fetchall()  # -> 결과값을 전부 가져온다.
  for a in curs:
    print(a)     #전부 가져왔는지 확인
  cur.close()  # -> 커서를 닫아준다  #장바구니 반환
  # 3. 다시 메인html으로 보내준다.
  return jsonify(curs)


# 로그인 페이지
@app.route("/login", methods=["GET", "POST"])
def login():
  # 로그인이 되어있는지 확인
  a = bool(session)
  # bool은 true or false 자료형 데이터가 있으면 true 없으면 false로 치환됨
  # if문은 true일때 실행됨
  if a:
    # return 을 하면 함수를 나갑니다. 경로 변경 함수로 보내기
    return redirect(url_for("home"))
  # method가 get일때 실행됨
  if request.method == 'GET':  # ajax 타입설정에 따라 변경 login.html 34번라인과 42번라인 참고
    # 로그인창 열기
    return render_template('login.html')
  # method가 post일때 실행됨
  if request.method == 'POST':
    # 로그인 입력을 하고 버튼을 눌렀을때 실행되는 것
    # id 입력값 받아와서 user_id에 넣기
    user_id = request.form['user_id']
    # password 입력값 받아와서 user_pw에 utf-8로 인코딩해서 넣기
    user_pw = request.form['password'].encode('utf-8')
    # 데이터를 받아 올 때 딕셔너리 형식으로 받아 오기 위해 커서를 변경
    curs = db.cursor(pymysql.cursors.DictCursor)  # 참고A
    # sql users에서 입력받은 user_id를 검색한다.
    sql = "SELECT * FROM users WHERE user_id = %s"
    # sql 실행 하는데 %s에 user_id를 대채해준다.
    curs.execute(sql, (user_id))
    # 실행 결과값을 가져오기
    # curs.fetchall()  -> 결과값을 전부 가져온다.
    user = curs.fetchone()  # -> 결과값을 1개만 가져온다.
    curs.close()  # -> 커서를 닫아준다
    print(user)  # -> user에 데이터가 잘 들어갔는지 확인하기 위한 출력

    # curs.fetchone()나 curs.fetchall()실행시 결과값이 없을때 None로 결과가 나옴.
    # 데이터베이스에서 해당 아이디를 찾을 수 없을 때 실행되는 코드
    if user == None:
      return "아이디가 틀렸습니다"
    # 데이터베이스에 해당 아이디가 있을 때
    if len(user) > 0:
      # password를 해쉬값으로 인코딩 및 비교 후 일치할시 결과 실행
      if bcrypt.hashpw(user_pw, user['user_pw'].encode('utf-8')) == user['user_pw'].encode('utf-8'):
        # 세션에 닉네임을 넣어주기
        session['user_nk'] = user['user_nk']
        # 세션에 id을 넣어주기
        session['user_id'] = user['user_id']
        return redirect(url_for("home"))  # 24 라인으로 보내버리기
      else:
        return "에러발생"


# 로그아웃하기
@app.route('/logout', methods=['GET'])
def logout():
  # 세션을 비워버리기
  session.clear()

  return redirect(url_for("home"))


# 회원가입 페이지
@app.route("/join", methods=["GET", "POST"])
def join():
  # 위의 로그인 페이지랑 같은 기능 로그인 되어있으면 회원가입페이지로 못가게 막는 기능
  a = bool(session)
  if a:
    return redirect(url_for("home"))
  # get일때 실행
  if request.method == 'GET':
    return render_template('join.html')
  # get이 아닐때 실행 메소드가 2개 이상이면 사용하지 말 것
  else:
    user_id = request.form['user_id']  # user아이디 받아오기
    user_email = request.form['email']  # 입력값 받아오기
    user_password = request.form['password'].encode('utf-8')  # 입력값 받아와서 인코딩 utf-8은 궁금하시면 검색
    hash_password = bcrypt.hashpw(user_password, bcrypt.gensalt())  # 참고B
    user_name = request.form['name']
    user_nk = request.form['nk']

    curs = db.cursor()
    sql = "insert into users (user_id,user_pw,user_name,user_email,user_nk) values (%s,%s,%s,%s,%s)"  # 애는 순서가 중요함 순서대로 1:1매칭
    curs.execute(sql, (user_id, hash_password, user_name, user_email, user_nk))
    db.commit()
    curs.close()
    return jsonify({'msg': '가입완료'})


@app.route("/mypage", methods=["GET", "POST"])
def mypage():
  return render_template('mypage.html')


@app.route("/personal", methods=["GET", "POST"])
def personal():
  return render_template('personal.html')


@app.route("/write", methods=["GET", "POST"])
def write():
  return render_template('post_write.html')


# 게시글 저장
@app.route('/post_save', methods=["POST"])
def post_save():
    bd_title = request.form['bd_title_give']
    bd_content = request.form['bd_content_give']
    user_nk = session.get("user_nk")

    sql = """insert into board (bd_title, bd_content, bd_updateDate, user_nk) Values ('%s', '%s', null, '%s');""" %(bd_title, bd_content, user_nk)

    cur.execute(sql)
    cur.fetchall()
    db.commit()
    cur.close()

    return redirect(url_for("home"))


# 게시글 가져오기



# 게시글 업데이트
# @app.route('/post_up', methods=["POST"])
# def post_up():
#     bd_title = request.form['bd_title_give']
#     bd_content = request.form['bd_content_give']
#     user_nk = session.get("user_nk")
#
#     sql = """insert into board (bd_title, bd_content, user_nk) Values ('%s', '%s');""" %(bd_title, bd_content, user_nk)
#
#     cur.execute(sql)
#     cur.fetchall()
#     db.commit()
#     cur.close()
#
#     return redirect(url_for("home"))


# 상세 게시물 페이지
@app.route("/boards/<board_id>", methods=["GET"])
def board(board_id):
  board_id_receive = int(board_id)
  sql = """SELECT b.id, b.bd_title, b.bd_content, b.user_nk, u.user_email
    , u.user_site, u.user_img, u.user_fp FROM board AS b 
    INNER JOIN users AS u ON b.user_nk = u.user_nk WHERE b.id = %s;"""
  post_detail_result = query_mysql(sql, board_id_receive, 1)
  # 해당 포스트에서 사용된 이미지
  sql = "select * from board_img where board_id = %s"
  img_result = query_mysql(sql, board_id_receive, 1)

  doc = {"detail": post_detail_result[0]}
  print(doc["detail"])
  if img_result != ():
    doc["images"] = img_result

  return render_template("board.html", user_nk=session.get("user_nk"), detailDict=doc)


# 상세 게시물 페이지에서 이전, 이후 페이지 값 가져 오기
@app.route("/boards/pages", methods=["POST"])
def other_detail():
  user_nk_receive = request.form["user_nk_give"]
  post_id_receive = int(request.form["post_id_give"])

  # 이전 글의 post_id 가져오기
  sql = """SELECT id, bd_title FROM board b WHERE user_nk = %s AND id = (SELECT max(id) FROM board b2 
    WHERE user_nk = %s AND id < %s);"""
  post_detail_before = query_mysql(sql, (user_nk_receive, user_nk_receive, post_id_receive), 1)

  # 이후 글의 post_id 가져오기
  sql = """SELECT id, bd_title FROM board b WHERE user_nk = %s AND id = (SELECT min(id) FROM board b2 
    WHERE user_nk = %s AND id > %s);"""
  post_detail_next = query_mysql(sql, (user_nk_receive, user_nk_receive, post_id_receive), 1)

  ##### 값이 없을 경우 () 이렇게 튜플로 나와.
  doc = {
    "before": post_detail_before,
    "after": post_detail_next
  }
  return jsonify({'msg': 'detail 이전, 이후 글 get!', "result": doc})


# 상세 게시물 삭제
@app.route("/boards", methods=["DELETE"])
def delete_post():
  board_id_receive = request.form["board_id_give"]
  user_nk = session.get("user_nk")

  sql = "delete from board where id = %s"
  query_mysql(sql, board_id_receive)

  sql = "delete from board_img where board_id = %s"
  query_mysql(sql, board_id_receive)

  folder_path = f'./static/posting_images/{user_nk}/board_{board_id_receive}'

  if os.path.exists(folder_path):
    shutil.rmtree(folder_path)

  return jsonify({'msg': 1})


# db 쿼리문
def query_mysql(sql, value=0, select_use_value=0, check_last_id=0):
  db = pymysql.connect(host="localhost", port=3306, user="root", db='sparta_test', password='1q2w3e4r',
                       charset='utf8')
  cur = db.cursor(pymysql.cursors.DictCursor)

  if value == 0 and check_last_id == 0:  # value 가 초기값 그대로 0이라면, 이는 select 문.
    cur.execute(sql)
    select_result = cur.fetchall()
    db.close()
    return select_result
  else:
    if select_use_value == 1:  # select 인데, 검색어를 value 로 주는 select.
      cur.execute(sql, value)
      select_result = cur.fetchall()
      db.close()
      return select_result
    elif check_last_id == 1:  # insert 를 실행했을 때 생성된 레코드의 id 값을 같이 반환받고 싶다면.
      cur.execute(sql, value)  # value 가 하나라면 ()는 필요없고, 다수라면 밖에서 매개변수를 넣어줄 때 () 로 넣어줘야 해.
      db.commit()
      db.close()
      return cur.lastrowid
    else:  # 그냥 insert, update, delete 를 적용만 시키고 끝내고 싶다.
      cur.execute(sql, value)
      db.commit()
      db.close()


# 세션이 있는지 없는지를 체크하는 함수
def check_session():
  if session.get("user_id") is not None and session.get("user_nk") is not None:
    return True
  else:
    return False


if __name__ == '__main__':
  app.run(debug=True)
