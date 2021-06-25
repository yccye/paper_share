from django.test import TestCase
import pymysql

# connection = pymysql.connect(host='127.0.0.1', user='root', password='2769633', db='paper_share',
#                              charset='utf8', cursorclass=pymysql.cursors.DictCursor)
# # sql = "select * from message"
# # cursor = connection.cursor()
# # cursor.execute(sql)
# # result = cursor.fetchall()
# # print(result)
connection = pymysql.connect(host='127.0.0.1', user='root', password='2769633', db='paper_share',
                             charset='utf8', cursorclass=pymysql.cursors.DictCursor)
cursor = connection.cursor()

sql = "create table user(" \
      "user_id int(11) primary key AUTO_INCREMENT" \
      "username char(12)" \
      "password char(30)" \
      "pic char(100)" \
      ")"

cursor.execute(sql)
connection.commit()

sql = "create table paper(" \
      "paper_id int(11) primary key AUTO_INCREMENT" \
      "author char(30)" \
      "password char(30)" \
      "link char(100)" \
      ")"

cursor.execute(sql)
connection.commit()

sql = "create table record(" \
      "record_id int(11) primary key AUTO_INCREMENT" \
      "paper_id int(11)" \
      "user_id int(11)" \
      "foreign key(paper_id) references paper" \
      "foreign key(user_id) references user" \
      ")"

cursor.execute(sql)
connection.commit()

connection.close()
