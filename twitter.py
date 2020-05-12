import connect
import debug
import configparser
import requests
import json
import time
import os
from urllib.parse import urlencode
import tool
base_url="https://api.twitter.com/2/timeline/favorites/3224794260.json"

config=configparser.ConfigParser()
config.read("./app.conf")
mode=config.get("mode","type")
user=config.get("sys","username")
proxy={
    "http":config.get("proxy","http"),
    "https":config.get("proxy","https")
}

def syn_start():

    p_str = "++++++++++"
    n_str=""
    #para without cursor
    while True:
        try:
            para_w = {
                "include_profile_interstitial_type": 1,
                "include_blocking": 1,
                "include_blocked_by": 1,
                "include_followed_by": 1,
                "include_want_retweets": 1,
                "include_mute_edge": 1,
                "include_can_dm": 1,
                "include_can_media_tag": 1,
                "skip_status": 1,
                "cards_platform": "Web-12",
                "include_cards": 1,
                "include_composer_source": "true",
                "include_ext_alt_text": "true",
                "include_reply_count": 1,
                "tweet_mode": "extended",
                "include_entities": "true",
                "include_user_entities": "true",
                "include_ext_media_color": "true",
                "include_ext_media_availability": "true",
                "send_error_codes": "true",
                "simple_quoted_tweets": "true",
                "sorted_by_time": "true",
                "count":20,
                "ext": "mediaStats,highlightedLabel,cameraMoment"
            }
            if p_str == "..........":
                #发生错误 再次打开该页面
                tool.t_print("twitter 回滚至上一页")
                #p_str = get_next(base_url+"&cursor="+n_str)
                para_w["cursor"]=n_str
                p_str = get_next(base_url+"?"+urlencode(para_w))
                if(p_str!=".........."):
                    n_str=p_str
                time.sleep(60*10)
            elif p_str=="++++++++++":
                #第一次打开 打开base_url
                tool.t_print("twitter 第一次打开")
                p_str = get_next(base_url+"?"+urlencode(para_w))
                if(p_str!=".........."):
                    n_str=p_str
            elif p_str=="**********":
                tool.t_print("twitter 回滚至第一页")
                p_str = get_next(base_url+"?"+urlencode(para_w))
                if(p_str!=".........."):
                    n_str=p_str
                time.sleep(60*60)
            else:
                #正常进入下一页
                tool.t_print("twitter 下一页")
                para_w["cursor"]=n_str
                p_str = get_next(base_url+"?"+urlencode(para_w))
                if(p_str!=".........."):
                    n_str=p_str
                time.sleep(5)
        except Exception as e:
            tool.t_print("twitter 错误%s"%e)


def down_start():
    try:
        while True:
            c_list = connect.read("select * from twitter_media")
            for i in c_list:
                pic_name=i["url"].split('/')[len(i["url"].split('/'))-1]
                if(os.access("./d_file/pic_file/"+pic_name,os.F_OK)):
                    tool.t_print("twitter file "+pic_name+" has exists")
                    continue
                response = requests.get(i["url"],proxies=proxy)
                bf=response.content
                with open("./d_file/pic_file/"+pic_name,"wb") as f:
                    f.write(bf)
                    f.close()
                response.close()
                tool.t_print("twitter file"+pic_name+" has download")
            time.sleep(100)
    except Exception as e:
        tool.t_print("twitter错误%s"%e)


"""
def make_cookie():
    c_list = connect.read("select * from cookie where web='twitter' and user='"+user+"'")
    cookies = {
    }
    cookie_txt = c_list[0]["cookie"]
    for cookie_item in cookie_txt.split(";"):
        cookies[cookie_item.split("=")[0].strip(
            " ")] = cookie_item.split("=")[1].strip(" ")
    return cookies


def make_header():
    h_list = connect.read("select * from header where web='twitter' and user='"+user+"'")
    headers = {

    }
    for item in h_list:
        headers[item["head"]] = item["value"]
    return headers
"""

def get_next(url):
    try:
        add_count=0

        cookie = tool.make_cookie("twitter",user)
        header = tool.make_header("twitter",user)
        page = requests.get(url, cookies=cookie, headers=header,proxies=proxy)
        all_obj = json.loads(page.text)
        page.close()
        twi = all_obj["globalObjects"]["tweets"]

        for key in twi:

            #获取next的ID
            items = all_obj["timeline"]["instructions"][0]["addEntries"]["entries"]
            item = items[len(items)-1]

            #存在ID则跳转到下一页  在一页中比较难出现录入一般的情况
            #另外一种情况为存在ID 则跳转到开头 订正:顺序并非按照收藏顺序排列
            #第一种为数据录入 第二种为运行后保持数据库更新
            #注意 没有按照收藏时间排序
            if connect.isexist("select * from twitter_fav where id='"+key+"' and user='"+user+"'"):
                tool.t_print("twitter sql"+key+" has exists")
                #print(key+" 已存在 跳过")
                #获取该列有多少为已存在
                continue

            add_count=add_count+1
            
            text = twi[key]["full_text"]
            text = text.replace("'", "")
            tool.t_print("twitter insert twitter"+key)
            connect.execute(
                "insert into twitter_fav(id,user,txt,time) values('"+key+"','"+user+"','"+text+"','"+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"')")
            #time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 

            #不存在media 跳过这条twitter
            if(not ("media" in twi[key]["entities"])):
                continue
            #存在media 写入twitter_media
            for pic in twi[key]["entities"]["media"]:
                pic_url = pic["media_url"].replace("\\", "")
                #print("insert media "+pic_url)
                connect.execute(
                    "insert into twitter_media(twitter_id,url) values('"+key+"','"+pic_url+"')")
        #该url不存在新的收藏
        if(add_count==0):
            if(mode=="first"):
                return item["content"]["operation"]["cursor"]["value"]
            else:
                return "**********"
        #该url存在新的收藏         
        else:
            return item["content"]["operation"]["cursor"]["value"]
        #return item["content"]["operation"]["cursor"]["value"]
    except Exception as e:
        tool.t_print("twitter 错误%s"%e)
        return ".........."
