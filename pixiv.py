import html
import requests
import debug
import connect
import tool
import configparser
from urllib.parse import urlencode
from urllib.parse import unquote
import json
import time
import math
import re
import os
import zipfile
import io
import imageio
import chardet

#https://www.pixiv.net/users/8790637/bookmarks/artworks
#https://www.pixiv.net/users/8790637/bookmarks/artworks?rest=hide
#https://www.pixiv.net/ajax/user/8790637/novels/bookmarks?rest=show
#https://www.pixiv.net/ajax/user/8790637/novels/bookmarks?rest=show
config=configparser.ConfigParser()
config.read("./app.conf")
mode=config.get("mode","type")
user=config.get("sys","username")
pixiv_id=config.get("pixiv","pixiv_id")
proxy={
        "http":config.get("proxy","http"),
        "https":config.get("proxy","https")
}
header=tool.make_header("pixiv",user)
cookie=tool.make_cookie("pixiv",user)


def syn_start():
    while True:
        try:
            start("show","illusts")
            start("hide","illusts")
            start("hide","novels")
            start("show","novels")
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




def start(type,ion):#type hide or show,ion illusts or novels
    para={
            "tag":"",
            "offset":0,
            "limit":48,
            "rest":type,
            "lang":"zh"
            }
    url="https://www.pixiv.net/ajax/user/"+pixiv_id+"/"+ion+"/bookmarks"
    response=requests.get(url+"?"+urlencode(para),cookies=cookie,headers=header)
    jo=json.loads(response.text)
    response.close()


    total_num=int(jo["body"]["total"])
    page_num=math.ceil(total_num/48)
    for page in range(0,page_num):
        #循环获取所有
        para["offset"]=page*48
        response=requests.get(url+"?"+urlencode(para),cookies=cookie,headers=header)
        tool.t_print("pixiv open page "+str(page))
        jo=json.loads(response.text)
        response.close()
        for item in jo["body"]["works"]:
            #this get description
            #why add it because shuang
            #if work not exist insert it
            #only when file is exist, get description
            #add get novels code
            item_id=""
            if(isinstance(item["id"],str)):
                item_id=item["id"]
            else:
                item_id=str(item["id"])

            if(ion=="illusts"):
                getillustitem(item_id,item)
            elif (ion=="novels"):
                getnovelitem(item_id,item)
            else:
                tool.t_print("not exits type")


def down():
    while True:
        pic_list=connect.read("select * from pixiv_media")
        gif_list=connect.read("select * from pixiv_gif")
        cover_list=connect.read("select * from pixiv_novel")
        for pic in pic_list:
            pic_name=pic["url"].split('/')[len(pic["url"].split('/'))-1]
            if(os.access("./d_file/pic_file_pixiv/"+pic_name,os.F_OK)):
                #tool.t_print("pixiv file,"+pic_name+" has exist")
                continue
            response=requests.get(pic["url"],headers=header)
            bf=response.content
            with open("./d_file/pic_file_pixiv/"+pic_name,'wb') as fi:
                fi.write(bf) 
                fi.close()
                tool.t_print("pixiv file"+pic_name+" has download")
            response.close()

        for gif in gif_list:
            if(os.access("./d_file/pic_file_pixiv/"+gif["pixiv_id"]+".gif",os.F_OK)):
                #tool.t_print("pixiv file,"+gif["pixiv_id"]+" has exist")
                continue
            gif_down(gif)
            tool.t_print("pixiv gif "+gif["pixiv_id"]+".gif"+" has download")

        for cover in cover_list:
            cover_name=cover["novel_cover"].split('/')[len(cover["novel_cover"].split('/'))-1]
            if(os.access("./d_file/novel_cover_pixiv/"+cover_name,os.F_OK)):
                continue
            response=requests.get(cover["novel_cover"],headers=header)
            bf=response.content
            with open("./d_file/novel_cover_pixiv/"+cover_name,'wb') as fi:
                fi.write(bf) 
                fi.close()
                tool.t_print("novel cover"+cover_name+" has download")
            response.close()
    
def gif_down(gif):
    response=requests.get(gif["url"],headers=header)
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

def getillustitem(item_id,item):
    if not connect.isexist("select * from pixiv_fav where id='"+item_id+"'"):
        response=requests.get("https://www.pixiv.net/artworks/"+item_id,cookies=cookie,headers=header)
        result_desstr=getanitemfromjosntxt(response.text,"\"illustComment\"",1)
        #pat_des=re.compile(r"\"description\":\"[\s\S]*?\",")
        #result_des=pat_des.findall(response.text)
        #result_desstr=""
        #if(len(result_des)!=0):
            #result_desstr=result_des[0][15:len(result_des[0])-2]
        result_desstr=unquote(result_desstr,"utf-8")
        result_desstr=html.unescape(result_desstr)
        tool.t_print("insert sql, pixiv id "+item_id)
        connect.execute("insert into pixiv_fav(id,user,txt,time,des) values('"+item_id+"','"+user+"','"+item["title"].replace("'","").replace("\\","")+"','"+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"','"+result_desstr.replace("'","").replace("\\","")+"')")
        #gif?
        if item["illustType"]==2:
            response.close()
            #https://www.pixiv.net/ajax/illust/81072672/ugoira_meta
            response=requests.get("https://www.pixiv.net/ajax/illust/"+item_id+"/ugoira_meta",headers=header,cookies=cookie)
            jo=json.loads(response.text)
            response.close()
            frame=json.dumps(jo["body"]["frames"])
            connect.execute("insert into pixiv_gif(pixiv_id,url,delay) values('"+item_id+"','"+jo["body"]["originalSrc"]+"','"+frame+"')")
            #GIF
        else:
            #not GIF
            #https://i.pximg.net/img-original/img/2017/01/22/21/15/53/61062485_p0.png
            #this response is page of works ,on the top we get des from it
            pat_ori=re.compile(r"https://i\.pximg\.net/img-original/img/[/\d]+_p\d+\.[pngjp]+")
            result=pat_ori.findall(response.text)
            response.close()
            pic_count=item["pageCount"]
            if(len(result)==0):
                return
            #insert pic in sql
            for i in range(pic_count):
                #https://i.pximg.net/img-original/img/2020/03/20/01/50/36/80230872_p0.jpg
                connect.execute("insert into pixiv_media(pixiv_id,url) values('"+item_id+"','"+result[0].replace("p0","p"+str(i))+"')")
            else:
                response.close()
                #tool.t_print("pixiv sql,"+item_id+" has exist ")
def getnovelitem(item_id,item):
    if not connect.isexist("select * from pixiv_novel where novel_id='"+item_id+"'"):#not exist
        #novel_id item_id
        #novel_title title
        #novel_count textCount
        #time now
        #novel_cover url
        # https://www.pixiv.net/novel/show.php?id=
        response=requests.get("https://www.pixiv.net/novel/show.php?id="+item_id,headers=header,cookies=cookie)
        html_txt=response.text
        txt=getanitemfromjosntxt(html_txt,"\"content\"",0)
        txt=txt.replace("\\n","</br>")
        txt=txt.replace("\\t","</br>")
        response.close()
        connect.execute("insert into pixiv_novel(novel_id,novel_title,novel_count,time,novel_cover) values('"+item_id+"','"+item["title"]+"',"+str(item["textCount"])+",'"+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"','"+item["url"]+"')")
        i=0
        while(i*1000 <= len(txt)):
            if((i+1)*1000<=len(txt)):
                #print(txt[i*1000:(i+1)*1000].encode("utf8"))
                connect.execute("insert into pixiv_novel_txt(novel_id,txt) values('"+item_id+"','"+txt[i*1000:(i+1)*1000]+"')")
            else:
                connect.execute("insert into pixiv_novel_txt(novel_id,txt) values('"+item_id+"','"+txt[i*1000:len(txt)]+"')")
            i=i+1

    else:#exist
        pass


def getanitemfromjosntxt(ori_str,s_str,index):
    j=0
    k=0
    l=0
    m=0
    for i in range(0,index-1):
        m=ori_str.index(s_str,m)+len(s_str)

    for i in range(ori_str.index(s_str,m)+len(s_str),len(ori_str)):
        if(ori_str[i]=="\"" and ori_str[i-1]!="\\"):
            l=l+1
            if(l==1):
                j=i
            if(l==2):
                k=i
                break
    return ori_str[j+1:k]