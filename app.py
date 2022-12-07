from flask import Flask, render_template, request, jsonify, session, redirect, url_for
app = Flask(__name__)

#[id:a,pw:b] 라인 딕셔너리 형식으로 받아오기 참고A
#[a,b]
import pymysql.cursors

#패스워드를 저장시 암호화 해쉬로!  참고B
import bcrypt

# 디비 연결하기
db = pymysql.connect(host="localhost",
                     port=3306,
                     user="",
                     db='ojijo',
                     password='',
                     charset='utf8')
curs = db.cursor()

#해쉬화를 위해 필요
app.secret_key = "#@!RFW12adnuiasfWE@!$2"
#메인페이지
@app.route("/", methods=["GET","POST"])#app.route("/" <- 경로 설정
def home():#함수명은 중복이 불가
  return render_template('main.html')

#로그인 페이지
@app.route("/login", methods=["GET","POST"])
def login():
  # 로그인이 되어있는지 확인
  a = bool(session)
  # bool은 true or false 자료형 데이터가 있으면 true 없으면 false로 치환됨
  #if문은 true일때 실행됨
  if a :
    #return 을 하면 함수를 나갑니다. 경로 변경 함수로 보내기
    return redirect(url_for("home"))
  #method가 get일때 실행됨
  if request.method == 'GET': #ajax 타입설정에 따라 변경 login.html 34번라인과 42번라인 참고
    #로그인창 열기
    return render_template('login.html')
  #method가 post일때 실행됨
  if request.method == 'POST':
    #로그인 입력을 하고 버튼을 눌렀을때 실행되는 것
    #id 입력값 받아와서 user_id에 넣기
    user_id = request.form['user_id']
    # password 입력값 받아와서 user_pw에 utf-8로 인코딩해서 넣기
    user_pw = request.form['password'].encode('utf-8')
    #데이터를 받아 올 때 딕셔너리 형식으로 받아 오기 위해 커서를 변경
    curs = db.cursor(pymysql.cursors.DictCursor) #참고A
    #sql users에서 입력받은 user_id를 검색한다.
    sql = "SELECT * FROM users WHERE user_id = %s"
    #sql 실행 하는데 %s에 user_id를 대채해준다.
    curs.execute(sql,(user_id))
    #실행 결과값을 가져오기
    #curs.fetchall()  -> 결과값을 전부 가져온다.
    user = curs.fetchone() #-> 결과값을 1개만 가져온다.
    curs.close() #-> 커서를 닫아준다
    print(user) #-> user에 데이터가 잘 들어갔는지 확인하기 위한 출력

    # curs.fetchone()나 curs.fetchall()실행시 결과값이 없을때 None로 결과가 나옴.
    # 데이터베이스에서 해당 아이디를 찾을 수 없을 때 실행되는 코드
    if user == None:
      return "아이디가 틀렸습니다"
    #데이터베이스에 해당 아이디가 있을 때
    if len(user) > 0:
      #password를 해쉬값으로 인코딩 및 비교 후 일치할시 결과 실행
      if bcrypt.hashpw(user_pw,user['user_pw'].encode('utf-8')) == user['user_pw'].encode('utf-8'):
        # 세션에 닉네임을 넣어주기
        session['user_nk'] = user['user_nk']
        # 세션에 id을 넣어주기
        session['user_id'] = user['user_id']
        return redirect(url_for("home")) #24 라인으로 보내버리기
      else:
        return "에러발생"

#로그아웃하기
@app.route('/logout', methods=['GET'])
def logout():
  #세션을 비워버리기
  session.clear()

  return redirect(url_for("home"))


#회원가입 페이지
@app.route("/join", methods=["GET","POST"])
def join():
  #위의 로그인 페이지랑 같은 기능 로그인 되어있으면 회원가입페이지로 못가게 막는 기능
  a = bool(session)
  if a :
    return redirect(url_for("home"))
  #get일때 실행
  if request.method == 'GET':
    return render_template('join.html')
  #get이 아닐때 실행 메소드가 2개 이상이면 사용하지 말 것
  else:
    user_id = request.form['user_id'] #user아이디 받아오기
    user_email = request.form['email'] #입력값 받아오기
    user_password = request.form['password'].encode('utf-8') #입력값 받아와서 인코딩 utf-8은 궁금하시면 검색
    hash_password = bcrypt.hashpw(user_password, bcrypt.gensalt()) #참고B
    user_name = request.form['name']
    user_nk = request.form['nk']

    curs = db.cursor()
    sql = "insert into users (user_id,user_pw,user_name,user_email,user_nk) values (%s,%s,%s,%s,%s)" #애는 순서가 중요함 순서대로 1:1매칭
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

