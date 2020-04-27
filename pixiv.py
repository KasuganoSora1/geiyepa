import requests
import connect
import configparser
import json
config=configparser.ConfigParser()

config.read("./app.conf")
mode="first"
user=config.get("sys","username")

address=config.get("mysql","address")
user_name=config.get("mysql","username")
password=config.get("mysql","password")

proxy={
    "http":config.get("proxy","http"),
    "https":config.get("proxy","https")
}

def syn_start():
   p_str = "++++++++++"
    n_str=""
    #para without cursor
    while True:
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
            print("回滚至上一页")
            #p_str = get_next(base_url+"&cursor="+n_str)
            para_w["cursor"]=n_str
            p_str = get_next(base_url+"?"+urlencode(para_w))
            if(p_str!=".........."):
                n_str=p_str
            time.sleep(5)
        elif p_str=="++++++++++":
            #第一次打开 打开base_url
            print("第一次打开")
            p_str = get_next(base_url+"?"+urlencode(para_w))
            if(p_str!=".........."):
                n_str=p_str
        elif p_str=="**********":
            print("回滚至第一页")
            p_str = get_next(base_url+"?"+urlencode(para_w))
            if(p_str!=".........."):
                n_str=p_str
            time.sleep(60*10)
        else:
            #正常进入下一页
            print("下一页")
            para_w["cursor"]=n_str
            p_str = get_next(base_url+"?"+urlencode(para_w))
            if(p_str!=".........."):
                n_str=p_str
            time.sleep(5)


def make_cookie():
    c_list = connect.read("select * from cookie where web='pixiv' and user='"+user+"'")
    cookies = {
    }
    cookie_txt = c_list[0]["cookie"]
    for cookie_item in cookie_txt.split(";"):
        cookies[cookie_item.split("=")[0].strip(
            " ")] = cookie_item.split("=")[1].strip(" ")
    return cookies


def make_header():
    h_list = connect.read("select * from header where web='pixiv' and user='"+user+"'")
    headers = {

    }
    for item in h_list:
        headers[item["head"]] = item["value"]
    return headers

