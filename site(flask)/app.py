from flask import Flask, render_template, request,flash,session,url_for
from flask import render_template_string,redirect
from random import choice,randint
import pymysql, random, sys, os
from pymysql.err import IntegrityError
import socket,time
from _thread import *
from werkzeug.utils import secure_filename
from datetime import datetime,timedelta

server_ip='1.234.44.132'

def socket_client_add(req,pd_name):
    HOST = server_ip
    PORT = 12345
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    s.connect((HOST,PORT))

    s.send(req.encode('utf-8'))
    time.sleep(1)    

    s.send(pd_name.encode('utf-8'))

    result = s.recv(1024).decode('utf-8')
    print(result)

def socket_client_rental(req,pd_name):

    HOST = server_ip
    PORT = 12345
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    s.connect((HOST,PORT))

    s.send(req.encode('utf-8'))
    time.sleep(1)    

    result = s.recv(1024).decode('utf-8')
    print(result)

def socket_client_return(req,user,pd_name):
    try:
        HOST = server_ip
        PORT = 12345    
        
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        s.connect((HOST,PORT))
        
        s.send(req.encode('utf-8'))
        time.sleep(2)

        s.send(user.encode('utf-8'))
        time.sleep(1)

        s.send(pd_name.encode('utf-8'))

        result = s.recv(1024).decode('utf-8')
        print(result)
    except  Exception   as e:
        print("Error_retrunSocket : ",e)


app = Flask(__name__)
app.secret_key = 'abc'

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/registerAction", methods=['GET', 'POST'])
def registerAction():
    if request.method != 'POST':
        return render_template("register.html")

    user_name = request.form['user_name']
    user = request.form['id']
    password = request.form['password']
    user_email = request.form['user_email']
    phone = request.form['phone']
    point=1000
    print(user_email,phone)


    if len(user)==0:
        flash("아이디를 입력해주세요.")
        return render_template("register.html")
    elif len(password)<8:
        flash("패스워드를 8글자 이상 입력해주세요.")
        return render_template("register.html")
    elif len(password)==0:
        flash("패스워드를 입력해주세요.")
        return render_template("register.html")
    elif len(phone)>15 or len(phone)<7:
        flash("전화번호를 올바르게 입력해주세요.")
        return render_template("register.html")

    try:
        db = pymysql.connect(host='127.0.0.1',
                             port=3306,
                             user='kmj',
                             password='1234',
                             db='capstone',
                             charset='utf8')

        cursor = db.cursor()
        sql = f'INSERT INTO user(user_name,id,password,user_email,phone,point) VALUES(%s,%s,%s,%s,%s,%s)'
        cursor.execute(sql,(user_name,user,password,user_email,phone,point))
        result = cursor.fetchall()

        flash("회원가입 되었습니다.")
        db.commit()
        db.close()
        return render_template("login.html")
    except Exception as e:
        print("[ERROR] registerAction : ",e)
        flash("이미 존재하는 회원입니다.")
        return render_template("register.html")


@app.route("/")
def login():
    return render_template("login.html")

@app.route("/loginAction", methods=["POST"])
def login_action():

    user = request.form['id']
    password = request.form['password']
    
    print("사용자 : ",user,password)
    
    db = pymysql.connect(host='127.0.0.1', # db IP
                        port=3306, # db port
                        user='kmj', # db user 정보
                        password='1234', # db user의 password
                        db='capstone', # db명
                        charset='utf8')
    
    cursor = db.cursor() # 쿼리문에 의해서 반환되는 결과값들을 저장하는 메모리공간
    sql = f'SELECT * FROM user WHERE id=%s and password=%s'
    cursor.execute(sql,(user,password)) # 입력 받은 두 값을 활용해 쿼리 실행
    result = cursor.fetchall() # 커서에서 원하는 결과값을 추출
    db.close()

    print(result)

    if result:
        session['user']=user
        flash("로그인 되었습니다.")
        return redirect(url_for('rental'))
    elif user=="":
        flash("아이디를 입력해주세요")
        return render_template("login.html")
    elif password=="":
        flash("패스워드를 입력해주세요")
        return render_template("login.html")
    else:
        flash("아이디 또는 패스워드가 맞지 않습니다.")
        return render_template("login.html")
        
@app.route("/logout")
def logout():
    session.pop('user',None)
    flash("로그아웃 되었습니다.")
    return redirect(url_for('login'))

@app.route("/rental")
def rental():
    user=session.get('user')
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='kmj', password='1234', db='capstone')
    cursor = conn.cursor()

    sql = 'SELECT * FROM product where pd_name not in (SELECT pd_name from rental)'
    cursor.execute(sql)
    data = cursor.fetchall()
    conn.close()

    return render_template("homepage.html",productList=data)

@app.route("/rentalAction", methods=['GET', 'POST'])
def rentalAction():
    user=session.get('user')
    pd_name=request.form['pd_name']
    

    db = pymysql.connect(host='127.0.0.1', port=3306, user='kmj', password='1234', db='capstone')
    cursor = db.cursor()

    rental_date=datetime.today()
    return_date=rental_date+timedelta(days=1)

    print(user,pd_name,rental_date,return_date)

    sql = 'INSERT INTO rental(id,pd_name,rental_date,return_date) VALUES(%s,%s,%s,%s)'
    cursor.execute(sql,(user,pd_name,rental_date,return_date))
    db.commit()
    db.close()

    db = pymysql.connect(host='127.0.0.1', port=3306, user='kmj', password='1234', db='capstone')
    cursor = db.cursor()

    sql = f"UPDATE user set point=point-(select point from product where pd_name='{pd_name}') where id='{user}'"
    cursor.execute(sql)
    db.commit()
    db.close()


    socket_client_rental("rental",pd_name)
    flash("10초 후 문이 닫힙니다. 대여한 상품을 가져가주세요.")
    return redirect(url_for('rental'))


@app.route('/add')
def add():
    return render_template("add.html")

@app.route('/addAction', methods=['GET', 'POST'])
def addAction():

    try:

        user=session.get('user')
        pd_name=request.form['pd_name']
        pd_img='./static/src/img/'+pd_name
        pd_price=request.form['pd_price']

        print(user,pd_name,pd_img)
        db = pymysql.connect(host='127.0.0.1',
                             port=3306,
                             user='kmj',
                             password='1234',
                             db='capstone',
                             charset='utf8')

        cursor = db.cursor()

        sql = f'INSERT INTO product(id,pd_name,pd_url,cost) VALUES(%s,%s,%s,%s)'
        cursor.execute(sql,(user,pd_name,pd_img,pd_price))
        result = cursor.fetchall()

        socket_client_add("add",pd_name)

        flash("추가되었습니다.")
        db.commit()
        db.close()
        return render_template("add.html")

    except Exception as e:
        print("[ERROR] addAction : ",e)
        flash("입력 값을 올바르게 입력해주세요.")
        return render_template("add.html")


@app.route('/productList')
def productList():
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='kmj', password='1234', db='test')
    cursor = conn.cursor()

    sql = 'SELECT * FROM product'
    cursor.execute(sql)
    data = cursor.fetchall()

    return render_template('test.html', productList=data)


@app.route('/mypage')
def mypage():
    user=session.get('user')
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='kmj', password='1234', db='capstone')
    cursor = conn.cursor()

    sql = f"SELECT * FROM product where pd_name in (SELECT pd_name from rental where id='{user}')"
    cursor.execute(sql)
    data2 = cursor.fetchall()
    conn.close()
    print(data2)

    conn = pymysql.connect(host='127.0.0.1', port=3306, user='kmj', password='1234', db='capstone')
    cursor = conn.cursor()

    sql = f"SELECT point from user where id='{user}'"
    cursor.execute(sql)
    data = cursor.fetchall()
    conn.close()
    print(data[0][0])

    return render_template('mypage.html',rentalList=data2,point=data[0][0])

@app.route("/returnAction", methods=['GET', 'POST'])
def renturnAction():
    user=session.get('user')
    pd_name=request.form['pd_name']
    try:
            user=session.get('user')
            pd_name=request.form['pd_name']

            db = pymysql.connect(host='127.0.0.1', port=3306, user='kmj', password='1234', db='capstone')
            cursor = db.cursor()

            sql = f"Delete from rental where id='{user}' and pd_name='{pd_name}'"
            cursor.execute(sql)
            
            db.commit()
            db.close()

            socket_client_return("return",user,pd_name)
            flash("반납 완료")
            
            return redirect(url_for('mypage'))
    except Exception as e:
        print("ERROR_returnAction : ",e)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
