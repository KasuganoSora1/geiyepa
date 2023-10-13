import tool
import configparser
import requests
import json
import connect
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
        entry_id=get_entryid(entry)
        user_in_db=tool.get_dbname("spectre","twitter")
        is_exist=connect.isexist(f"select * from twitter_fav where id='{entry_id}' and user='{user_in_db}'")
        if(is_exist==False):
            count=count+1
    return count

def get_entryid(entry):
    tweet_id=entry["entryId"]
    entry_id=tweet_id[6:]
    return entry_id

def sync_entry(entry):
    if(entry["content"].get("itemContent")!=None):
        legacy=entry["content"]["itemContent"]["tweet_results"]["result"]["legacy"]
        full_text=legacy["full_text"]
        print(full_text)
        medias=legacy["entities"]["media"]
        for media in medias:
            if(media["type"]=="video"):
                print(media["type"])
                #print(media["video_info"])
                #bitrate
                bitrate_map={}
                bitrate_max=0
                for variant in media["video_info"]["variants"]:
                    if(variant.get("bitrate")!=None):
                        bitrate_map[variant["bitrate"]]=variant["url"]
                        if(variant["bitrate"]>bitrate_max):
                            bitrate_max=variant["bitrate"]
                print(bitrate_map[bitrate_max])
                print(media["media_url_https"])
            else:
                print(media["type"])
                print(media["media_url_https"])
    else:
        print("不存在 itemContent")
    return None

