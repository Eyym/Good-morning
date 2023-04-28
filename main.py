from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]


# def get_weather():
#   url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
#   res = requests.get(url).json()
#   week_list = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
#   week_list[datetime.date(today).weekday()]
#   weather = res['data']['list'][0]
#   low =  int(weather['low'])
#   high =  int(weather['high'])
#   return weather['weather'], math.floor(weather['temp']),week_list[datetime.date(today).weekday()],city,high,low

def get_weather():
    url = 'https://www.yiketianqi.com/free/day?appid=63984366&appsecret=useiPJq2&unescape=1&city=南昌'
    res = requests.get(url).json()
    city = res['city']
    weather = res['wea']
    low = res['tem_night']
    high =  res['tem_day']
    week = res['week']
    tem = res['tem']
    print("地区:"+city)
    print("今日天气:"+weather)
    print("最高气温:"+high)
    print("最低气温:"+low)
    print("当前温度:"+tem)
    print("week:"+week)
    return weather,tem,week,city,high,low

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature,weekday,city,max_temperature,min_temperature = get_weather()
data = {"weather":{"value":wea},"temperature":{"value":temperature},"weekday":{"value":weekday},"city":{"value":city},"max_temperature":{"value":max_temperature},"min_temperature":{"value":min_temperature},"love_days":{"value":get_count()},"birthday_left":{"value":get_birthday()},"words":{"value":get_words(), "color":get_random_color()}}
res = wm.send_template(user_id, template_id, data)
print(res)
