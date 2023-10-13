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
import requests
import configparser
import twitter_new
cursor=""
while(True):
    if(cursor==""):
        obj=twitter_new.get_json_from_cursor("spectre")
    else:
        obj=twitter_new.get_json_from_cursor("spectre",cursor)
    entyties=twitter_new.get_entyties(obj)
    count=twitter_new.get_not_exist_count(entyties,"spectre")
    if(count==0):
        break
    else:
        cursor=twitter_new.get_bottom_cursor(obj)
        for entry in entyties:
            tweet_id=twitter_new.get_entryid(entry)
            if(twitter_new.is_exist(tweet_id,"spectre")):
                pass
            else:
                twitter_new.sync_entry(entry,"spectre")
