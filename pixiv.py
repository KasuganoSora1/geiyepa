
import requests
import debug
import connect
import tool
import configparser
from urllib.parse import urlencode
import json
import time
import math
import re
import os
import zipfile
import io
import imageio

#https://www.pixiv.net/users/8790637/bookmarks/artworks
#https://www.pixiv.net/users/8790637/bookmarks/artworks?rest=hide

url="https://www.pixiv.net/ajax/user/8790637/illusts/bookmarks"
config=configparser.ConfigParser()
config.read("./app.conf")
mode=config.get("mode","type")
user=config.get("sys","username")
proxy={
        "http":config.get("proxy","http"),
        "https":config.get("proxy","https")
}
header=tool.make_header("pixiv",user)
cookie=tool.make_cookie("pixiv",user)


def syn_start():
    while True:
        try:
            start("show")
            start("hide")
            time.sleep(60*60)
        except Exception as e:
            tool.t_print("pixiv 错误%s"%e)
def down_start():
    while True:
        try:
            down()
            time.sleep(100)
        except Exception as e:
            tool.t_print("pixiv 错误%s"%e)




def start(type):#type hide or show
    para={
            "tag":"",
            "offset":0,
            "limit":48,
            "rest":type,
            "lang":"zh"
            }
    response=requests.get(url+"?"+urlencode(para),cookies=cookie,headers=header,proxies=proxy)
    jo=json.loads(response.text)
    response.close()


    total_num=int(jo["body"]["total"])
    page_num=math.ceil(total_num/48)
    for page in range(0,page_num):
        #循环获取所有
        para["offset"]=page*48
        response=requests.get(url+"?"+urlencode(para),cookies=cookie,headers=header,proxies=proxy)
        tool.t_print("pixiv open page "+str(page))
        jo=json.loads(response.text)
        response.close()
        for item in jo["body"]["works"]:
            #this get description
            #why add it because shuang
            #if work not exist insert it
            #only when file is exist, get description
            if not connect.isexist("select * from pixiv_fav where id='"+item["illustId"]+"'"):
                response=requests.get("https://www.pixiv.net/artworks/"+item["illustId"],cookies=cookie,headers=header,proxies=proxy)
                pat_des=re.compile(r"\"description\":\"[\s\S]*?\"")
                result_des=pat_des.findall(response.text)
                result_desstr=result_des[0][15:len(result_des[0])-1]

                tool.t_print("insert sql, pixiv id "+item["illustId"])
                connect.execute("insert into pixiv_fav(id,user,txt,time,des) values('"+item["illustId"]+"','"+user+"','"+item["illustTitle"].replace("'","").replace("\\","")+"','"+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"','"+result_desstr.replace("'","").replace("\\","")+"')")
                #gif?
                if item["illustType"]==2:
                    response.close()
                    #https://www.pixiv.net/ajax/illust/81072672/ugoira_meta
                    response=requests.get("https://www.pixiv.net/ajax/illust/"+item["illustId"]+"/ugoira_meta",headers=header,cookies=cookie,proxies=proxy)
                    jo=json.loads(response.text)
                    response.close()
                    frame=json.dumps(jo["body"]["frames"])
                    connect.execute("insert into pixiv_gif(pixiv_id,url,delay) values('"+item["illustId"]+"','"+jo["body"]["originalSrc"]+"','"+frame+"')")
                    #GIF
                else:
                    #not GIF
                    #https://i.pximg.net/img-original/img/2017/01/22/21/15/53/61062485_p0.png
                    #this response is page of works ,on the top we get des from it
                    pat_ori=re.compile(r"https://i\.pximg\.net/img-original/img/[/\d]+_p\d+\.[pngjp]+")
                    result=pat_ori.findall(response.text)
                    response.close()
                    pic_count=item["pageCount"]
                    #insert pic in sql
                    for i in range(pic_count):
                        #https://i.pximg.net/img-original/img/2020/03/20/01/50/36/80230872_p0.jpg
                        connect.execute("insert into pixiv_media(pixiv_id,url) values('"+item["illustId"]+"','"+result[0].replace("p0","p"+str(i))+"')")
            else:
                #response.close()
                tool.t_print("pixiv sql,"+item["illustId"]+" has exist ")


def down():
    while True:
        pic_list=connect.read("select * from pixiv_media")
        gif_list=connect.read("select * from pixiv_gif")
        for pic in pic_list:
            pic_name=pic["url"].split('/')[len(pic["url"].split('/'))-1]
            if(os.access("./d_file/pic_file_pixiv/"+pic_name,os.F_OK)):
                tool.t_print("pixiv file,"+pic_name+" has exist")
                continue
            response=requests.get(pic["url"],proxies=proxy,headers=header)
            bf=response.content
            with open("./d_file/pic_file_pixiv/"+pic_name,'wb') as fi:
                fi.write(bf) 
                fi.close()
                tool.t_print("pixiv file"+pic_name+" has download")
            response.close()
        for gif in gif_list:
            if(os.access("./d_file/pic_file_pixiv/"+gif["pixiv_id"]+".gif",os.F_OK)):
                tool.t_print("pixiv file,"+gif["pixiv_id"]+" has exist")
                continue
            gif_down(gif)
            tool.t_print("pixiv gif "+gif["pixiv_id"]+".gif"+" has download")

    
def gif_down(gif):
    response=requests.get(gif["url"],proxies=proxy,headers=header)
    bf=response.content
    by=io.BytesIO(bf)
    zip_file=zipfile.ZipFile(by,"r")
    response.close()
    image_pic=[]
    image_delay=[]
    for name in zip_file.namelist():
        pic=zip_file.read(name)
        image_pic.append(imageio.imread(pic))
    delays=json.loads(gif["delay"])
    for delay in delays:
        image_delay.append(delay["delay"]/1000)
    imageio.mimsave("./d_file/pic_file_pixiv/"+gif["pixiv_id"]+".gif",image_pic,"GIF",duration=image_delay)
    tool.t_print("pixiv file"+gif["pixiv_id"]+" has download")
