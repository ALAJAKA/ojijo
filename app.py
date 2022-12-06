from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

import pymysql
# 디비 연결하기
db = pymysql.connect(host="localhost",
                     port=3306,
                     user="각자 알아서",
                     db='ojijo',
                     password='각자 알아서',
                     charset='utf8')
curs = db.cursor()

#메인페이지
@app.route("/", methods=["GET"])
def home():
  return render_template('index.html')


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

