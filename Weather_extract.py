#! /usr/bin/python3.6
# -*-coding:utf-8 *-

import requests as r
import pandas as pd


page = r.get("https://forecast.weather.gov/MapClick.php?lat=37.7772&lon=-122.4168")

from bs4 import BeautifulSoup as bs

soup = bs(page.content, 'html.parser')

seven_day = soup.find(id="seven-day-forecast")
forecast_items = seven_day.find_all(class_="tombstone-container")

first_forecast = forecast_items[0]
# period = first_forecast.find(class_="period-name").get_text()
# short_desc = first_forecast.find(class_="short-desc").get_text()
# temp_high = first_forecast.find(class_="temp temp-high").get_text()
# img = first_forecast.find("img")
# desc = img['title']

period_tags = seven_day.select(".tombstone-container .period-name")
periods = [pt.get_text() for pt in period_tags]
short_desc = [sd.get_text() for sd in seven_day.select(".tombstone-container .short-desc")]
temp = [t.get_text() for t in seven_day.select(".tombstone-container .temp")]
descs = [d["title"] for d in seven_day.select(".tombstone-container img")]

print(periods)
# print(len(periods))
print(short_desc)
print(temp)
print(descs)

# conversion en Dataframe dans Pandas. On gagne un index et les fonctions d'analyse.
weather = pd.DataFrame({
    "periods": periods,
    "short_desc": short_desc,
    "temp": temp,
    "descs": descs
})

# print(weather)

temp_nums = weather["temp"].str.extract("(?P<temp_num>\d+)", expand=False)
weather["temp_num"] = temp_nums.astype('int')
print(temp_nums)
print(weather["temp_num"].mean())
is_night = weather["temp"].str.contains("Low")
weather["is_night"] = is_night
print(is_night)
