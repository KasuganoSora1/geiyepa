import sqlite3
import pymysql
import configparser
config=configparser.ConfigParser()
config.read("app.conf")
# db_path=".\\d_file\\data.db"
address=config.get("mysql","address")
user_name=config.get("mysql","username")
password=config.get("mysql","password")
def read(sql_str):
    #conn=sqlite3.connect(db_path)
    conn=pymysql.connect(address,user_name,password,"data")
    pointer=conn.cursor()
    pointer.execute(sql_str)
    names=[]
    results=[]
    for name in pointer.description:
        names.append(name[0])
    for row in pointer:
        one_value={

        }
        for col_index in range(0,len(names)):
            one_value[names[col_index]]=row[col_index]
        results.append(one_value)
    pointer.close()
    conn.commit()
    conn.close()
    return results

def execute(sql_str):
    #conn=sqlite3.connect(db_path)
    conn=pymysql.connect(address,user_name,password,"data")
    pointer=conn.cursor()
    pointer.execute(sql_str)
    pointer.close()
    conn.commit()
    conn.close()
    return
def isexist(sql_str):
    #conn=sqlite3.connect(db_path)
    conn=pymysql.connect(address,user_name,password,"data")
    pointer=conn.cursor()
    pointer.execute(sql_str)
    re=True
    if len(list(pointer))==0:
        re=False
    else:
        re=True
    pointer.close()
    conn.commit()
    conn.close()
    return re
