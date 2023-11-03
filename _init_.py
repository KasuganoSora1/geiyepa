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
twitter_new.start_sync("someonessomthi1")
twitter_new.start_sync("spectre")
twitter_new.down_start()
pixiv.syn_start()
count=pixiv.down_start()
print(f"存在{count}个图片已经无法下载")
