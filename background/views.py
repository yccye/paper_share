from datetime import datetime

import pymysql
import time

from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views.decorators.csrf import csrf_exempt


def getPage(request, filename):
    return render(request, "background/" + filename)


def group(request):
    connection = pymysql.connect(host='127.0.0.1', user='root', password='2769633', db='paper_share',
                                 charset='utf8', cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    user_id = request.session.get('user_id')
    print(user_id)
    sql = ""
    if user_id == 0:
        sql = "select * from `group`"
    else:
        sql = "select * from `group` natural join group_list where user_id = " + str(user_id)
    cursor.execute(sql)
    result = cursor.fetchall()

    sql = "select * from logs natural join user"
    # else:
    #     sql = "select group_id from `group` natural join group_list where user_id = %s)"
    cursor.execute(sql)
    logs = cursor.fetchall()
    print(logs)
    content = {'group': result, 'logs': logs}
    print(content)
    connection.close()
    return render(request, 'background/group_list.html', content)


def paper(request):
    connection = pymysql.connect(host='127.0.0.1', user='root', password='2769633', db='paper_share',
                                 charset='utf8', cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    login_user_id = request.session.get('user_id')
    if login_user_id == 0:
        sql = "select * from paper"
    else:
        sql = "select * from (select * from paper natural join record_list natural join `user` natural join `group`) as n where n.group_id in (select group_id from group_list where user_id = " + str(
            login_user_id) + ")"
    cursor.execute(sql)
    result = cursor.fetchall()
    content = {'paper': result}
    for item in content['paper']:
        print(item)
        sql2 = "select group_name from record_list natural join `group` where paper_id = " + str(item['paper_id'])
        cursor.execute(sql2)
        result = cursor.fetchone()
        print(result)
        if result is not None:
            item['group_name'] = result['group_name']
        else:
            item['group_name'] = "None"

    connection.close()

    return render(request, 'background/paper_list.html', content)


def note(request):
    connection = pymysql.connect(host='127.0.0.1', user='root', password='2769633', db='paper_share',
                                 charset='utf8', cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()

    login_user_id = request.session.get('user_id')
    if login_user_id == 0:
        sql = "select * from note_list natural join `user` natural join `group` natural join paper "
    else:
        sql = "select * from (select * from note_list natural join `user` natural join `group` natural join paper) as n where n.group_id in (select group_id from group_list where user_id = " + str(
            login_user_id) + ")"

    cursor.execute(sql)
    result = cursor.fetchall()
    content = {'note': result}
    print(content)
    connection.close()

    return render(request, 'background/note_list.html', content)


def paper_insert(request):
    connection = pymysql.connect(host='127.0.0.1', user='root', password='2769633', db='paper_share',
                                 charset='utf8', cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()

    group_id = request.POST.get('group_id')
    name = request.POST.get('name')
    author = request.POST.get('author')
    link = request.POST.get('link')
    source = request.POST.get('source')
    user_id = request.POST.get("user_id")
    sql = "insert into paper(`name`,author,link,source) VALUES" + "(" + "'" + name + "'" + "," + "'" + author + "'" + "," + "'" + link + "'" + "," + "'" + source + "'" + ")"
    cursor.execute(sql)
    sql2 = "insert into record_list(paper_id,user_id,group_id) values (" + "'" + str(
        connection.insert_id()) + "'" + "," + "'" + str(user_id) + "'" + "," + "'" + str(group_id) + "'" + ")"
    cursor.execute(sql2)
    connection.commit()
    connection.close()

    return redirect("/background/paper_list.html")


@csrf_exempt
def group_create(request):
    print("create group2")

    connection = pymysql.connect(host='127.0.0.1', user='root', password='2769633', db='paper_share',
                                 charset='utf8', cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    name = request.POST.get('name')
    select = request.POST.get('select')
    email = request.POST.get('email')
    description = request.POST.get('description')
    print(name, select, email, description)
    now = datetime.now()
    now = now.strftime("%Y-%m-%d %H:%M:%S")
    sql = "insert into `group`(group_name,private,description,time,email) values(" + "'" + name + "'" + "," + "'" + select + "'" + "," + "'" + description + "'" + "," + "'" + now + "'" + "," + "'" + email + "'" + ")"
    print(sql)
    cursor.execute(sql)

    # 将创建的用户加入group中
    user_sql = "insert into group_list(user_id, group_id) values (" + str(request.session.get('user_id')) + "," + str(
        connection.insert_id()) + ")"
    cursor.execute(user_sql)
    connection.commit()
    connection.close()

    return redirect("/background/group")


def note_form(request, paper_id):
    print("note form")
    print(paper_id)
    connection = pymysql.connect(host='127.0.0.1', user='root', password='2769633', db='paper_share',
                                 charset='utf8', cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()

    # 查询相应Paper_id号的论文的信息
    sql = "select * from paper natural join record_list where paper_id = " + str(paper_id)
    cursor.execute(sql)
    result = cursor.fetchall()
    print(result)
    connection.close()
    result[0]['user_id'] = request.session.get("user_id")
    return render(request, "background/note_create.html", result[0])


def note_create(request):
    connection = pymysql.connect(host='127.0.0.1', user='root', password='2769633', db='paper_share',
                                 charset='utf8', cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    name = request.POST.get('name')
    group_id = request.POST.get('group_id')
    user_id = request.POST.get('user_id')
    if user_id == "管理员上传":
        user_id = 0
    paper_id = request.POST.get('paper_id')
    context = request.POST.get('context')
    print(context)
    sql = "insert into note_list(note_id,group_id,user_id,paper_id,content) values (%s, %s, %s, %s, %s)"
    cursor.execute(sql, (connection.insert_id(), group_id, user_id, paper_id, context))
    connection.commit()
    connection.close()

    return redirect("/background/note_list.html")


@csrf_exempt
def add_number(request, group_id, user_id):
    connection = pymysql.connect(host='127.0.0.1', user='root', password='2769633', db='paper_share',
                                 charset='utf8', cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    sql = "select * from `user` where user_id = " + str(user_id)
    cursor.execute(sql)
    if cursor.fetchone() is None:
        return HttpResponse("error")
    sql = "select * from `group` where group_id = " + str(group_id)
    cursor.execute(sql)
    if cursor.fetchone() is None:
        return HttpResponse("error")

    sql2 = "insert into group_list values (" + str(user_id) + ',' + str(group_id) + ")"
    cursor.execute(sql2)
    connection.commit()
    connection.close()
    return HttpResponse("success")


def paper_detail(request, paper_id):
    connection = pymysql.connect(host='127.0.0.1', user='root', password='2769633', db='paper_share',
                                 charset='utf8', cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()

    paper_sql = "select * from paper where paper_id = " + str(paper_id)
    cursor.execute(paper_sql)
    info = cursor.fetchall()
    print(info)
    content_sql = "select * from note_list natural join `user` natural join `group` where paper_id = " + str(
        paper_id)
    cursor.execute(content_sql)
    content = cursor.fetchall()
    print(content)
    result = {'paper': info[0], 'content': content}
    print(result)
    connection.close()

    return render(request, 'background/paper_detail.html', result)


def group_detail(request, group_id):
    connection = pymysql.connect(host='127.0.0.1', user='root', password='2769633', db='paper_share',
                                 charset='utf8', cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()

    group_sql = "select * from `group` where group_id = " + str(group_id)
    cursor.execute(group_sql)
    group_res = cursor.fetchall()

    paper_sql = "select * from paper natural join record_list where group_id = " + str(group_id)
    cursor.execute(paper_sql)
    paper_res = cursor.fetchall()

    user_sql = "select * from  `user` natural join group_list where group_id = " + str(group_id)
    cursor.execute(user_sql)
    user_res = cursor.fetchall()

    content = {
        'group': group_res[0],
        'paper': paper_res,
        'user': user_res
    }
    connection.close()
    return render(request, 'background/group_detail.html', content)


def note_detail(request, note_id):
    connection = pymysql.connect(host='127.0.0.1', user='root', password='2769633', db='paper_share',
                                 charset='utf8', cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()

    sql = "select * from  note_list natural join `user` natural join paper where note_id = " + str(
        note_id)
    cursor.execute(sql)
    result = cursor.fetchall()
    connection.close()
    return render(request, 'background/note_detail.html', result[0])


@csrf_exempt
def info_delete(request, kind, group_id):
    connection = pymysql.connect(host='127.0.0.1', user='root', password='2769633', db='paper_share',
                                 charset='utf8', cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()

    if kind == "exit_group":
        try:
            sql = "delete from group_list where user_id =" + str(request.session.get(
                "user_id")) + " and " + "group_id = " + str(group_id)
            cursor.execute(sql)
            connection.commit()
            return HttpResponse("success")
        except Exception as e:
            print(e)
            return HttpResponse("error")

    elif kind == "delete_group":
        try:
            sql = "delete from `group` where group_id = " + str(group_id)
            cursor.execute(sql)
            connection.commit()
            return HttpResponse("success")
        except Exception as e:
            print(e)
            return HttpResponse("error")

    connection.close()
    return HttpResponse("error")


def main_page(request):
    connection = pymysql.connect(host='127.0.0.1', user='root', password='2769633', db='paper_share',
                                 charset='utf8', cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    content = {}

    sql = "select count(*) as total from user"
    cursor.execute(sql)
    result = cursor.fetchall()
    content['person'] = result[0]['total']

    sql = "select count(*) as total from `group`"
    cursor.execute(sql)
    result = cursor.fetchall()
    content['group'] = result[0]['total']

    sql = "select count(*) as total from paper"
    cursor.execute(sql)
    result = cursor.fetchall()
    content['paper'] = result[0]['total']

    sql = "select count(*) as total from note_list"
    cursor.execute(sql)
    result = cursor.fetchall()
    content['note'] = result[0]['total']

    sql = "select *  from task where user_id = %s"
    cursor.execute(sql, request.session.get("user_id"))
    result = cursor.fetchall()
    content['task'] = result
    print(sql)
    print(result)

    sql = "select group_id,group_name,count(paper_id) as paper_num,count(note_id) as note_num,count(user_id) as user_num from `group` natural join group_list natural left join record_list natural left join `user` natural left join paper natural left join note_list group by group_id, group_name"
    cursor.execute(sql)
    result = cursor.fetchall()
    content['group_rank'] = result
    print(result)
    connection.close()
    return render(request, "background/main_page.html", content)


@csrf_exempt
def task_add(request, content):
    connection = pymysql.connect(host='xxxx.xxxx.xxxx.xxxx', user='xxxx', password='xxxxx', db='paper_share',
                                 charset='utf8', cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    user_id = request.session.get('user_id')
    print(user_id)
    sql = "insert into task(user_id,content,time,status) values (%s,%s,%s,%s)"
    cursor.execute(sql, (user_id, content, datetime.now(), 0))
    connection.commit()
    connection.close()
    return HttpResponse("true")


def task_delete(request, task_id):
    connection = pymysql.connect(host='127.0.0.1', user='root', password='2769633', db='paper_share',
                                 charset='utf8', cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    sql = "delete from task where task_id = %s"
    cursor.execute(sql, task_id)
    connection.commit()
    connection.close()
    return HttpResponse("success")


def task_toggle(request, task_id):
    connection = pymysql.connect(host='127.0.0.1', user='root', password='2769633', db='paper_share',
                                 charset='utf8', cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    sql = "update task set status = !status where task_id = %s"
    cursor.execute(sql, task_id)
    connection.commit()
    connection.close()
    return HttpResponse("success")
