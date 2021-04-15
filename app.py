from flask import Flask, render_template, request

from chatterbot import ChatBot

from chatterbot.trainers import ChatterBotCorpusTrainer

import webbrowser as wb

import requests

import os

import ctypes

import urllib.request as urllib2

import datetime

import time

import json

from time import strftime

from youtube_search import YoutubeSearch

app = Flask(__name__)

english_bot = ChatBot("Chatterbot",storage_adapter="chatterbot.storage.SQLStorageAdapter")

trainer = ChatterBotCorpusTrainer(english_bot)

trainer.train("chatterbot.corpus.english")

@app.route("/")

def home():
    return render_template("index.html")

@app.route("/get")

def get_bot_response():

    userText = request.args.get('msg')

    yeucau = request.args.get('yeucau')

    if(english_bot.get_response(userText) == "đã đổi hình nền"):

        print(english_bot.get_response(userText))

        api_key = "NDBhkMQZQuOO6QA7F6ng8_o0abw0sZk9JMgABl-Ux9Y"
        
        url = 'https://api.unsplash.com/photos/random?client_id=' + \
            api_key  
        
        f = urllib2.urlopen(url)

        json_string = f.read()

        f.close()

        parsed_json = json.loads(json_string)

        photo = parsed_json['urls']['full']

        urllib2.urlretrieve(photo,"C:\\Users\\USER\\Downloads\\a.png")

        image = os.path.join("C:\\Users\\USER\Downloads\\a.png")

        ctypes.windll.user32.SystemParametersInfoW(20, 0, image, 3)

    if(yeucau == "1"):

        while True:

            result = YoutubeSearch(userText, max_results=10).to_dict()

            if result:
            
                break   

        url = f"https://www.youtube.com" + result[0]['url_suffix']

        wb.open_new_tab(url)

    elif(yeucau == "2"): 
       
        ow_url = "http://api.openweathermap.org/data/2.5/weather?"

        city = userText
        
        api_key = "956b3f6d6e673c965ca122222e12d505"
        
        call_url = ow_url + "appid=" + api_key + "&q=" + city + "&units=metric"
       
        response = requests.get(call_url)
       
        data = response.json()
       
        if data["cod"] != "404":
           
            city_res = data["main"]
           
            current_temperature = city_res["temp"]
            
            current_pressure = city_res["pressure"]
            
            current_humidity = city_res["humidity"]
            
            suntime = data["sys"]
            
            sunrise = datetime.datetime.fromtimestamp(suntime["sunrise"])
            
            sunset = datetime.datetime.fromtimestamp(suntime["sunset"])
            
            wthr = data["weather"]
            
            weather_description = wthr[0]["description"]
            
            now = datetime.datetime.now()
            
            content = f"""
            Hôm nay là ngày {now.day} tháng {now.month} năm {now.year}
            Mặt trời mọc vào {sunrise.hour} giờ {sunrise.minute} phút
            Mặt trời lặn vào {sunset.hour} giờ {sunset.minute} phút
            Nhiệt độ trung bình là {current_temperature} độ C
            Áp suất không khí là {current_pressure} héc tơ Pascal
            Độ ẩm là {current_humidity}%
            """
            return str(content)

        else:
            
            return str("không tìm thấy địa điểm")

    else:
        return str(english_bot.get_response(userText))
    

# def openYoutube():   
#     userText = request.args.get('msg') 
#     print(userText)     
#     return

# def open_google_and_search(text):
#     search_for = text.split("kiếm", 1)[1]
    
#     driver = webdriver.Chrome(path)
#     driver.get("http://www.google.com")
#     que = driver.find_element_by_xpath("//input[@name='q']")
#     que.send_keys(str(search_for))
#     que.send_keys(Keys.RETURN)
#     time.sleep(10)    

if __name__ == "__main__":
    app.run()