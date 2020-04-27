import requests
import configparser
import debug
import connect
import twitter
import threading

task=threading.Thread(target=twitter.syn_start)
task1=threading.Thread(target=twitter.down_start)
task.start()
task1.start()