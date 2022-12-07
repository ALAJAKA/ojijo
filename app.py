from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

import pymysql

# 디비 연결하기
db = pymysql.connect(host="localhost",
                     port=3306,
                     user="",
                     db='',
                     password='',
                     charset='utf8')
curs = db.cursor(pymysql.cursors.DictCursor)


# 메인페이지
@app.route("/", methods=["GET"])
def home():
    return render_template('personal.html')


# 개인작성글 목록 페이지
@app.route("/personal", methods=["GET"])
def get_personal_post():
    sql = "select bd_title, bd_content, bd_writeDate\
    from board\
    where user_nk ='람쥐';"
    curs.execute(sql)
    data = curs.fetchall()
    return jsonify({'result': data})
    db.commit()
    db.close()

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

