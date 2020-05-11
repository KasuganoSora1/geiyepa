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

task=threading.Thread(target=twitter.syn_start)
task1=threading.Thread(target=twitter.down_start)
task.start()
task1.start()
task2=threading.Thread(target=pixiv.syn_start)
task3=threading.Thread(target=pixiv.down_start)
task2.start()
task3.start()


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
