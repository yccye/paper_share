import pymysql
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt, csrf_protect

connection = pymysql.connect(host='127.0.0.1', user='root', password='2769633', db='paper_share',
                             charset='utf8', cursorclass=pymysql.cursors.DictCursor)
cursor = connection.cursor()


def index(request):
    return render(request, 'login/index.html')


@csrf_exempt
def login(request):
    if request.method == 'GET':
        return HttpResponse("")
    elif request.method == 'POST':
        username = request.POST.get('user')
        password = request.POST.get('passwd')
        print(username, password)
        sql = "select * from user where username = " + "'" + username + "'"
        cursor.execute(sql)
        result = cursor.fetchall()

        if len(result) == 0:
            print(result)
            return HttpResponse("error")

        if result[0]['password'] == password:
            print("密码正确 登陆成功")
            request.session['username'] = result[0]['username']
            request.session['user_id'] = result[0]['user_id']
            request.session.set_expiry(None)
            return HttpResponse("true")

        return HttpResponse("false")


@csrf_exempt
def signin(request):
    if request.method == 'POST':
        username = request.POST.get('user')
        password = request.POST.get('passwd')

        sql = "select password from user where username = " + "'" + username + "'"
        cursor.execute(sql)

        if len(cursor.fetchall()) == 1:
            return HttpResponse("exist")

        try:
            # 进行数据库插入操作
            sql = "insert into user(username,password) values(" + "'" + username + "'" + "," + "'" + password + "'" + ")"
            print(sql)
            cursor.execute(sql)
            connection.commit()
        except Exception as e:
            print(e)
            return HttpResponse("false")

        return HttpResponse("true")
