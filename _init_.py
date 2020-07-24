import requests
import configparser
import debug
import connect
import twitter
import threading
import pixiv
import tool
import configparser
import zipfile
import io
import imageio
import json
from urllib.parse import urlencode


task=threading.Thread(target=twitter.syn_start)
task1=threading.Thread(target=twitter.down_start)
task.start()
task1.start()
task2=threading.Thread(target=pixiv.syn_start)
task3=threading.Thread(target=pixiv.down_start)
task2.start()
task3.start()



#para_w={
#    "include_profile_interstitial_type": 1,
#    "include_blocking": 1,
#    "include_blocked_by": 1,
#    "include_followed_by": 1,
#    "include_want_retweets": 1,
#    "include_mute_edge": 1,
#    "include_can_dm": 1,
#    "include_can_media_tag": 1,
#    "skip_status": 1,
#    "cards_platform": "Web-12",
#    "include_cards": 1,
#    "include_ext_alt_text": "true",
#    "include_quote_count": "true",
#    "include_reply_count": 1,
#    "tweet_mode": "extended",
#    "include_entities": "true",
#    "include_user_entities": "true",
#    "include_ext_media_color": "true",
#    "include_ext_media_availability": "true",
#    "send_error_codes": "true",
#    "simple_quoted_tweet": "true",
#    "count": 20,
#    "ext": "mediaStats,highlightedLabel"
#}
## https://api.twitter.com/2/timeline/conversation/1246365911038095361.json
#base_url="https://api.twitter.com/2/timeline/conversation/"
#
#cookie = tool.make_cookie("twitter","admin")
#header = tool.make_header("twitter","admin")
#
#config=configparser.ConfigParser()
#config.read("./app.conf")
#mode=config.get("mode","type")
#user=config.get("sys","username")
#proxy={
#    "http":config.get("proxy","http"),
#    "https":config.get("proxy","https")
#}
#
#item_list=connect.read("select * from twitter_fav left join twitter_media on id=twitter_id")
#for item in item_list:
#    if(item["url"]==None or item["url"]==""):
#        continue
#    if(item["url"].find("video")!=-1):#存在video
#        url=base_url+item["twitter_id"]+".json?"+urlencode(para_w)
#        url=url+urlencode(para_w)
#        page = requests.get(url, cookies=cookie, headers=header,proxies=proxy)
#        all_obj = json.loads(page.text)
#        entetis=all_obj["globalObjects"]["tweets"][item["twitter_id"]]
#        for pic in entetis["extended_entities"]["media"]:
#            for video in pic["video_info"]["variants"]:
#                connect.execute("insert into twitter_video(twitter_id,url) values('"+item["twitter_id"]+"','"+video["url"].replace("\\","")+"')")
#        page.close()



#config=configparser.ConfigParser()
#config.read("./app.conf")
#user=config.get("sys","username")
#header=tool.make_header("pixiv",user)
#proxy={
#        "http":config.get("proxy","http"),
#        "https":config.get("proxy","https")
#}
#cookie=tool.make_cookie("pixiv",user)
#gif=connect.read("select * from pixiv_gif")[0]
#response=requests.get(gif["url"],proxies=proxy,headers=header)
#bf=response.content
#by=io.BytesIO(bf)
#zip_file=zipfile.ZipFile(by,"r")
#
#response.close()
#image_pic=[]
#image_delay=[]
#names=zip_file.namelist()
#for name in zip_file.namelist():
#    pic=zip_file.read(name)
#    image_pic.append(imageio.imread(pic))
#delays=json.loads(gif["delay"])
#for delay in delays: 
#    print(delay["delay"])
#    image_delay.append(delay["delay"]/1000)
#imageio.mimsave("test.gif",image_pic,"GIF",duration=image_delay)
