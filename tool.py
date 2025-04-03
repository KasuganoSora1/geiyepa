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

def make_cookie_from_txt(username,webname):
    cookie_file=open(f'./{username}_{webname}_data/cookie.txt')
    cookie_str=cookie_file.readlines()[0]
    cookie_file.flush()
    cookie_file.close()
    cookies={}
    for cookie_item in cookie_str.split(";"):
        cookies[cookie_item.split("=")[0].strip(" ")] = cookie_item.split("=")[1].strip(" ")
    return cookies
def make_header_from_txt(username,webname):
    headers={}
    header_file=open(f'./{username}_{webname}_data/header.txt')
    headers_str=header_file.readlines()
    header_file.flush()
    header_file.close()
    for header_str in headers_str:
        header_name_value=header_str.split(":")
        header_name=header_name_value[0]
        if(header_name=="referer"):
            header_value=header_name_value[1]+":"+header_name_value[2].strip("\n")
            headers[header_name]=header_value
        else:
            header_value=header_name_value[1].strip("\n")
            headers[header_name]=header_value
    return headers
def make_variables_from_txt(username,webname):
    param_file=open(f'./{username}_{webname}_data/variables.json')
    paras_str=param_file.read()
    paras_str=paras_str.replace('\n','')
    paras_str=paras_str.replace('   ','')
    paras_str=paras_str.replace(' ','')
    param_file.flush()
    param_file.close()
    return paras_str
def make_features_from_txt(username,webname):
    feature_file=open(f'./{username}_{webname}_data/features.json')
    featrue_str=feature_file.read()
    featrue_str=featrue_str.replace('\n','')
    featrue_str=featrue_str.replace('   ','')
    feature_file.flush()
    feature_file.close()
    return featrue_str
def  make_url_from_txt(username,webname):
    url_file=open(f'./{username}_{webname}_data/url.txt')
    url_str=url_file.read()
    url_str=url_str.replace('\n','')
    url_file.flush()
    url_file.close()
    return url_str

def make_fieldtoggles_from_txt(username,webname):
    field_file=open(f'./{username}_{webname}_data/fieldToggles.json')
    field_str=field_file.read()
    field_str=field_str.replace('\n','')
    field_file.flush()
    field_file.close()
    return field_str

def debug_html(html_txt):
    f=open("debug.html",mode="w",encoding="utf8")
    f.write(html_txt)
    f.flush()
    f.close()
def debug_zip(html_zip):
    f=open("debug.zip",mode="wb")
    f.write(html_zip)
    f.flush()
    f.close()

def get_dbname(username,webname):
    f=open(f'./{username}_{webname}_data/system_name.txt')
    name=f.readline()
    name=name.strip("\n")
    f.flush()
    f.close()
    return name