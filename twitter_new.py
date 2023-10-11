import tool
import configparser
import requests
import json
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

def down_entry(entry):
    return None

