import json
import os
import urllib.request
import pickle
import re
import datetime


class BlockReader:
    def __init__(self, stream, block_size):
            self.stream = stream
            self.block_size = block_size
    def __iter__(self):
           return self

    def __next__(self):
         block = self.stream.read(self.block_size)
         if 0 == len(block):
             raise StopIteration
         return block



class Weather:
    appid = "&appid=86e2bc0b2caf8a9c933c75044312c5d4"
    id_city = "id=524901"
    cnt = "&cnt=9"
    py_obj=object
    weather_dict = {}

    weather_params = {}
    speed_wind = 0
    weather_description = {}

    def __init__(self):
        self.get_reqst()
        self.create_json()
        self.set_weather()
        self.set_weather_params()


    def get_reqst(self):
        r = urllib.request.urlopen(f'https://api.openweathermap.org/data/2.5/weather?{self.id_city}{self.appid}')
        self.py_obj=json.load(r)

    def create_json(self):
        with open((os.path.join(os.getcwd(), "weather.json")), 'wb') as w:
            if self.py_obj is not None:
                pickle.dump(self.py_obj,w)

    def set_weather(self):
        self.weather_dict=self.py_obj


    def get_time(self):
        data = datetime.datetime.fromtimestamp(self. weather_dict["dt"])
        data = data.strftime("%A, %d %B  %I:%M %p")
        return data

    def set_weather_params(self):
        for k, v in self. weather_dict.items():
            if k == "main":
                self. weather_params.update(v)
            elif k == "wind":
                self. speed_wind = int(v["speed"])
            elif k == "weather":
                temp = v[0]
                self. weather_description.update({"icon": temp["icon"]})

    def get_icon(self):
        icon = self. weather_description['icon']
        img = urllib.request.urlopen(f"http://openweathermap.org/img/w/{icon}.png")
        to_png = BlockReader(img, 4096)
        with open(f'{icon}.png', 'wb') as to_img:
            for b in to_png:
                to_img.write(b)
        icon += ".png"
        return icon

    def get_temp(self):
        return str(float("{0:.1f}".format((self.weather_params['temp']) - 273.15)))

    def refresh_weather(self):
        self.get_reqst()
        self.set_weather()
        self.set_weather_params()

a=Weather()
print(a.py_obj)
