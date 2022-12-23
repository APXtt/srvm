from flask import Flask, render_template, request, flash, session, url_for
from flask import render_template_string, redirect
from random import choice, randint
import pymysql
import random
import sys
import os
from pymysql.err import IntegrityError
import socket
import time
from _thread import *
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta

server_ip = '220.67.3.185'  # 현재 IP


def socket_client_add(req, pd_name):  # 상품 추가 요청 시 실행되는 함수
    HOST = server_ip
    PORT = 12345

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.connect((HOST, PORT))

    s.send(req.encode('utf-8'))
    time.sleep(1)

    s.send(pd_name.encode('utf-8'))

    result = s.recv(1024).decode('utf-8')
    print(result)


def socket_client_rental(req, pd_name):  # 상품 대여 요청 시 실행되는 함수

    HOST = server_ip
    PORT = 12345

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.connect((HOST, PORT))

    s.send(req.encode('utf-8'))
    time.sleep(1)

    result = s.recv(1024).decode('utf-8')
    print(result)


def socket_client_return(req, user, pd_name):  # 상품 반납 요청 받을 시 실행되는 함수
    try:
        HOST = server_ip
        PORT = 12345

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        s.connect((HOST, PORT))

        s.send(req.encode('utf-8'))
        time.sleep(2)

        s.send(user.encode('utf-8'))
        time.sleep(1)

        s.send(pd_name.encode('utf-8'))

        result = s.recv(1024).decode('utf-8')
        print(result)
    except Exception as e:
        print("Error_retrunSocket : ", e)

################################################################ flask 시작#######################################################


def create_app():
    app = Flask(__name__)
    app.secret_key = 'abc'

    @app.route("/")  # 기본 페이지
    def login():
        return render_template("login.html")  # login.html 출력

    @app.route("/loginAction", methods=["POST"])  # login 요청 시 실행되는 action
    def login_action():

        user = request.form['id']  # from에서 받아온 id 값
        password = request.form['password']  # form에서 받아온 password 값

        print("사용자 : ", user, password)

        db = pymysql.connect(host='127.0.0.1',  # db IP
                             port=3306,  # db port
                             user='kmj',  # db user 정보
                             password='1234',  # db user의 password
                             db='capstone',  # db명
                             charset='utf8')

        cursor = db.cursor()  # 쿼리문에 의해서 반환되는 결과값들을 저장하는 메모리공간
        # 사용할 쿼리 : user 테이블에서 현재 사용자의 id와 password를 조회
        sql = f'SELECT * FROM user WHERE id=%s and password=%s'
        # 입력 받은 두 값을 활용해 쿼리 실행 %s 에 들어 갈 값들 지정
        cursor.execute(sql, (user, password))
        result = cursor.fetchall()  # 쿼리에 맞는 결과 값을 cursor에서 골라 출력 (존재하지 않으면 아무것도 리턴하지 않음)
        db.close()

        print(result)

        if result:  # 로그인한 사용자가 db에 존재하면
            session['user'] = user  # user session 생성
            flash("로그인 되었습니다.")  # alert 창 띄우기
            return redirect(url_for('rental'))  # rental 함수 return
        elif user == "":
            flash("아이디를 입력해주세요")
            return render_template("login.html")
        elif password == "":
            flash("패스워드를 입력해주세요")
            return render_template("login.html")
        else:
            flash("아이디 또는 패스워드가 맞지 않습니다.")
            return render_template("login.html")

    @app.route("/register")  # 회원가입 페이지
    def register():
        return render_template("register.html")

    # 회원 가입 요청 시 실행되는 action
    @app.route("/registerAction", methods=['GET', 'POST'])
    def registerAction():
        if request.method != 'POST':  # method가 post일때만 실행되기 위한 조건문
            return render_template("register.html")

        user_name = request.form['user_name']  # from에서 받아온 값들
        user = request.form['id']
        password = request.form['password']
        user_email = request.form['user_email']
        phone = request.form['phone']
        point = 1000
        print(user_email, phone)

        if len(user) == 0:
            flash("아이디를 입력해주세요.")
            return render_template("register.html")
        elif len(password) < 8:
            flash("패스워드를 8글자 이상 입력해주세요.")
            return render_template("register.html")
        elif len(password) == 0:
            flash("패스워드를 입력해주세요.")
            return render_template("register.html")
        elif len(phone) > 15 or len(phone) < 7:
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
            # user table의 user_name~point 칼럼에 값 추가
            sql = f'INSERT INTO user(user_name,id,password,user_email,phone,point) VALUES(%s,%s,%s,%s,%s,%s)'
            # 위 쿼리문에서 데이터로 넣을 값 지정
            cursor.execute(sql, (user_name, user, password,
                           user_email, phone, point))
            result = cursor.fetchall()

            flash("회원가입 되었습니다.")
            db.commit()  # db 수정 시 commit 해야 반영됨
            db.close()

            return render_template("login.html")

        except Exception as e:
            print("[ERROR] registerAction : ", e)
            flash("이미 존재하는 회원입니다.")
            return render_template("register.html")

    @app.route("/logout")  # logout action
    def logout():
        session.pop('user', None)  # user의 세션 값 삭제
        flash("로그아웃 되었습니다.")
        return redirect(url_for('login'))  # login 함수 리턴

    @app.route("/rental")  # 대여 페이지 (홈페이지)
    def rental():
        user = session.get('user')  # user의 세션 값 가져오기
        conn = pymysql.connect(host='127.0.0.1', port=3306,
                               user='kmj', password='1234', db='capstone')
        cursor = conn.cursor()

        # rental 페이지에 없는 (아직 대여하지 않은) 상품을 출력하는 쿼리문
        sql = 'SELECT * FROM product where pd_name not in (SELECT pd_name from rental)'
        cursor.execute(sql)
        data = cursor.fetchall()  # 쿼리문 실행 결과가 담김
        conn.close()

        # homepage.html 리턴 및 productList 변수에 data 값 넣어 html로 전송
        return render_template("homepage.html", productList=data)

    @app.route("/rentalAction", methods=['GET', 'POST'])  # 대여 요청 시 실행되는 action
    def rentalAction():
        user = session.get('user')  # user의 세션 값 가져오기
        pd_name = request.form['pd_name']  # form에서 받은 pd_name 값 가져오기

        db = pymysql.connect(host='127.0.0.1', port=3306,
                             user='kmj', password='1234', db='capstone')
        cursor = db.cursor()

        rental_date = datetime.today()  # 오늘 날짜
        return_date = rental_date+timedelta(days=1)  # 하루 뒤의 날짜

        print(user, pd_name, rental_date, return_date)

        # 대여 시 rental 테이블에 데이터 추가
        sql = 'INSERT INTO rental(id,pd_name,rental_date,return_date) VALUES(%s,%s,%s,%s)'
        cursor.execute(sql, (user, pd_name, rental_date, return_date))
        db.commit()
        db.close()

        db = pymysql.connect(host='127.0.0.1', port=3306,
                             user='kmj', password='1234', db='capstone')
        cursor = db.cursor()

        # 대여 시 point 를 상품에 저장된 가격(cost)만큼 빼서 수정해주는 쿼리문
        sql = f"UPDATE user set point=point-(select cost from product where pd_name='{user}') where id='{user}'"
        cursor.execute(sql)
        db.commit()
        db.close()

        socket_client_rental("rental", pd_name)  # 소켓 rental 요청 시작

        flash("10초 후 문이 닫힙니다. 대여한 상품을 가져가주세요.")
        return redirect(url_for('rental'))  # rental 함수 리턴

    @app.route('/add')  # 상품 추가 페이지
    def add():
        return render_template("add.html")

    @app.route('/addAction', methods=['GET', 'POST'])  # 상품 추가 요청 시 실행되는 action
    def addAction():

        try:

            user = session.get('user')
            pd_name = request.form['pd_name']
            pd_img = './static/src/img/'+pd_name
            pd_price = request.form['pd_price']

            print(user, pd_name, pd_img)
            db = pymysql.connect(host='127.0.0.1',
                                 port=3306,
                                 user='kmj',
                                 password='1234',
                                 db='capstone',
                                 charset='utf8')

            cursor = db.cursor()

            # product에 상품을 추가하는 쿼리문
            sql = f'INSERT INTO product(id,pd_name,pd_url,cost) VALUES(%s,%s,%s,%s)'
            cursor.execute(sql, (user, pd_name, pd_img, pd_price))
            result = cursor.fetchall()

            socket_client_add("add", pd_name)  # 추가 요청 함수 실행

            flash("추가되었습니다.")
            db.commit()
            db.close()
            return render_template("add.html")

        except Exception as e:
            print("[ERROR] addAction : ", e)
            flash("입력 값을 올바르게 입력해주세요.")
            return render_template("add.html")

    @app.route('/mypage')  # mypage
    def mypage():
        user = session.get('user')  # 현재 user 세션 값
        conn = pymysql.connect(host='127.0.0.1', port=3306,
                               user='kmj', password='1234', db='capstone')
        cursor = conn.cursor()

        # 현재 사용자가 rental한 상품들의 정보를 출력
        sql = f"SELECT * FROM product where pd_name in (SELECT pd_name from rental where id='{user}')"
        cursor.execute(sql)
        data2 = cursor.fetchall()  # data2 에 저장됨
        conn.close()
        print(data2)

        conn = pymysql.connect(host='127.0.0.1', port=3306,
                               user='kmj', password='1234', db='capstone')
        cursor = conn.cursor()

        sql = f"SELECT point from user where id='{user}'"  # 현재 사용의 point 조회
        cursor.execute(sql)
        data = cursor.fetchall()  # data에 point 저장됨
        conn.close()
        print(data[0][0])

        # mypage 리턴 하면서 data2와 data[0][0](point) 를 넘김
        return render_template('mypage.html', rentalList=data2, point=data[0][0])

    # mypage에서 반납 시 실행되는 action
    @app.route("/returnAction", methods=['GET', 'POST'])
    def renturnAction():
        try:
            user = session.get('user')  # 현재 세션 값
            pd_name = request.form['pd_name']  # 폼에서 받아온 상품 이름

            db = pymysql.connect(host='127.0.0.1', port=3306,
                                 user='kmj', password='1234', db='capstone')
            cursor = db.cursor()

            # rental 테이블에서 반납한 상품 삭제
            sql = f"Delete from rental where id='{user}' and pd_name='{pd_name}'"
            cursor.execute(sql)

            db.commit()
            db.close()

            socket_client_return("return", user, pd_name)  # 함수 실행
            flash("반납 완료")

            return redirect(url_for('mypage'))
        except Exception as e:
            print("ERROR_returnAction : ", e)
