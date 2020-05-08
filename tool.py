import connect
import configparser
import time

config=configparser.ConfigParser()
config.read("./app.conf")
user=config.get("sys","username")

def make_cookie(web_name,user_name):
    c_list = connect.read("select * from cookie where web='"+web_name+"' and user='"+user_name+"'")
    cookies = {
    }
    cookie_txt = c_list[0]["cookie"]
    for cookie_item in cookie_txt.split(";"):
        cookies[cookie_item.split("=")[0].strip(
            " ")] = cookie_item.split("=")[1].strip(" ")
    return cookies

def make_header(web_name,user_name):
    h_list = connect.read("select * from header where web='"+web_name+"' and user='"+user_name+"'")
    headers = {

    }
    for item in h_list:
        headers[item["head"]] = item["value"]
    return headers

def t_print(str):
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+":"+str)
