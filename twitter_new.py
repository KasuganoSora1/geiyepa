import tool
import configparser
import requests
import json
import connect
import time
import os
def get_json_from_cursor(username,cursor=None):

    txt_url=tool.make_url_from_txt(username=username,webname="twitter")
    variable_str=tool.make_variables_from_txt(username,"twitter")
    feature_str=tool.make_features_from_txt(username,"twitter")
    header_dict=tool.make_header_from_txt(username,"twitter")
    cookie_dict=tool.make_cookie_from_txt(username,"twitter")

    config=configparser.ConfigParser()
    config.read("./app.conf")
    proxy={
        "http":config.get("proxy","http"),
        "https":config.get("proxy","https")
    }

    if(cursor==None):
        para={
            "variables" :variable_str,
            "features":feature_str
        }
        web_http=requests.get(url=txt_url,params=para,headers=header_dict,cookies=cookie_dict)
        web_txt=web_http.text
        web_http.close()
        pass
    else:
        variable_obj=json.loads(variable_str)
        variable_obj["cursor"]=cursor
        variable_str=json.dumps(variable_obj)
        para={
            "variables" :variable_str,
            "features":feature_str
        }
        web_http=requests.get(url=txt_url,params=para,headers=header_dict,cookies=cookie_dict)
        web_txt=web_http.text
        web_http.close()
    re_jo=json.loads(web_txt)
    return re_jo
#"cursor":"HBakifP00o3PrjEAAA==",
def get_entyties(obj):
    return obj["data"]["user"]["result"]["timeline_v2"]["timeline"]["instructions"][0]["entries"]

def get_bottom_cursor(obj):
    entyties=get_entyties(obj)
    for entry in entyties:
        if(entry["content"].get("itemContent")!=None):
            if(entry["content"]["itemContent"].get("itemType")!=None):
                #print(entry["content"]["itemContent"]["itemType"])
                pass
            else:
                print("不存在 itemType")
        elif(entry["content"].get("entryType")!=None):
            if(entry["content"]["cursorType"]=="Bottom"):
                return entry["content"]["value"]
        else:
            print("不存在itemcontent 和 entryType")
    return None

def get_not_exist_count(entyties,username):
    count=0
    for entry in entyties:
        if(entry["content"].get("itemContent")==None):
            continue
        entry_id=get_entryid(entry)
        user_in_db=tool.get_dbname("spectre","twitter")
        is_exist=connect.isexist(f"select * from twitter_fav where id='{entry_id}'")
        if(is_exist==False):
            count=count+1
    return count
def is_exist(tweet_id,username):
    tf=connect.isexist(f"select * from twitter_fav where id='{tweet_id}'")
    return tf

def get_entryid(entry):
    tweet_id=entry["entryId"]
    entry_id=tweet_id[6:]
    return entry_id
def sync_entry(entry,username):
    if(entry["content"].get("itemContent")!=None):
        if(entry["content"]["itemContent"]["tweet_results"]["result"].get("legacy")==None):
            legacy=entry["content"]["itemContent"]["tweet_results"]["result"]["tweet"]["legacy"]
        else:
            legacy=entry["content"]["itemContent"]["tweet_results"]["result"]["legacy"]
        full_text=legacy["full_text"]
        twitter_id=get_entryid(entry)
        user=tool.get_dbname(username,"twitter")
        time_str=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        connect.execute(f"insert into twitter_fav(id,user,txt,time) values('{twitter_id}','{user}','{full_text}','{time_str}')")
        #print(f"insert into twitter_fav(id,user,txt,time) values('{twitter_id}','{user}','{full_text}','{time_str}')")
        if(legacy["entities"].get("media")==None):
            print(f"{twitter_id} 没有图片")
            return
        else:
            medias=legacy["entities"]["media"]
        for media in medias:
            if(media["type"]=="video"):
                bitrate_map={}
                bitrate_max=0
                for variant in media["video_info"]["variants"]:
                    if(variant.get("bitrate")!=None):
                        bitrate_map[variant["bitrate"]]=variant["url"]
                        if(variant["bitrate"]>bitrate_max):
                            bitrate_max=variant["bitrate"]
                pic_url=media["media_url_https"]
                video_url=bitrate_map[bitrate_max]
                connect.execute(f"insert into twitter_media(twitter_id,url) values('{twitter_id}','{pic_url}')")
                connect.execute(f"insert into twitter_video(twitter_id,url) values('{twitter_id}','{video_url}')")
                #print(f"insert into twitter_media(twitter_id,url) values('{twitter_id}','{pic_url}')")
                #print(f"insert into twitter_video(twitter_id,url) values('{twitter_id}','{video_url}')")
                
            else:
                pic_url=media["media_url_https"]
                connect.execute(f"insert into twitter_media(twitter_id,url) values('{twitter_id}','{pic_url}')")
                #print(f"insert into twitter_media(twitter_id,url) values('{twitter_id}','{pic_url}')")
    else:
        #print(entry["content"]["cursorType"])
        #print("不存在 itemContent")
        pass

def down_start():
    try:
        c_list = connect.read("select * from twitter_media order by id desc")
        for i in c_list:
            pic_name=i["url"].split('/')[len(i["url"].split('/'))-1]

            if(os.access("./d_file/pic_file/"+pic_name,os.F_OK)):
                #tool.t_print(str(i["id"])+": twitter file "+pic_name+" has exists")
                continue

            response = requests.get(i["url"])
            bf=response.content
            if(response.status_code == 200):
                with open("./d_file/pic_file/"+pic_name,"wb") as f:
                    f.write(bf)
                    f.close()
                response.close()
                tool.t_print("twitter file"+pic_name+" has download")
            elif(response.status_code==403):
                tool.t_print("twitter file"+pic_name+" 403")
            else:
                #tool.t_print("twitter file"+pic_name+" not exist")
                response.close()

            
        v_list=connect.read("select * from twitter_video")
        for i in v_list:
            v_name=i["url"].split('/')[len(i["url"].split('/'))-1]
            if(v_name.find("?")!=-1):
                v_name=v_name[0:v_name.find("?")]
            if(v_name.find(".m3u8")!=-1):
                continue
            if(os.access("./d_file/twitter_video/"+v_name,os.F_OK)):
                continue

            response = requests.get(i["url"])
            bf=response.content
            if(response.status_code!=404):
                with open("./d_file/twitter_video/"+v_name,"wb") as f:
                    f.write(bf)
                    f.close()
                    tool.t_print("twitter file"+v_name+" has download")
                    response.close()
            else:
                #tool.t_print("twitter file"+v_name+" not exist")
                response.close()

            print("twitter down end")
    except Exception as e:
        tool.t_print("twitter错误%s"%e)

def start_sync(username):
    cursor=""
    while(True):
        if(cursor==""):
            obj=get_json_from_cursor(username)
        else:
            obj=get_json_from_cursor(username,cursor)
        entyties=get_entyties(obj)
        count=get_not_exist_count(entyties,"spectre")
        #xx_count=len(entyties)
        if(count==0):
            break
        else:
            print("需要sync:"+str(count)+"个")
            #print("总数"+str(xx_count))
            cursor=get_bottom_cursor(obj)
            for entry in entyties:
                tweet_id=get_entryid(entry)
                if(is_exist(tweet_id,"spectre")):
                    pass
                else:
                    sync_entry(entry,"spectre")
    print(f"{username}结束sync")
