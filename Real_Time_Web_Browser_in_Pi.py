import os
from selenium import webdriver
import csv
import random
import time
import datetime
from datetime import timedelta

currentDT = datetime.datetime.now().strftime('%Y-%m-%d')
thirty_day_before = (datetime.datetime.now() - timedelta(days = 30)).strftime('%Y-%m-%d')

All_station = []
image_station = []
station_went_through = []
counter = 0
path = os.getcwd() + "/" + 'Active_hydrology_Stations_2019-05-30.csv'

with open(path) as csvDataFile:                                                                         #go through the list 
    csvReader = csv.reader(csvDataFile)                                                 
    for row in csvReader:
        All_station.append(row[0])
        image_station.append(row[1])
#chrome_options = Options()
#chrome_options.add_argument("--kiosk")
#chrome_options.add_argument("--start-maximized")
driver = webdriver.Firefox('')

#driver.get('chrome://settings/')
#driver.execute_script('chrome.settingsPrivate.setDefaultZoom(0.70);')

driver.get("https://wateroffice.ec.gc.ca/login_e.html")
driver.find_element_by_id("username").send_keys("realtime")
driver.find_element_by_id("password").send_keys("hydrometric")
driver.find_elements_by_xpath("//input[@value='Login']")[0].click()

while True:
    driver.get("https://wateroffice.ec.gc.ca/google_map/google_map_e.html?map_type=real_time&search_type=province&province=all")
    driver.execute_script("window.scrollTo(0,900);")
    time.sleep(30)

    i = random.randint(0,len(All_station))
    station = All_station[i]
    station_went_through.append(station)
    driver.get("https://wateroffice.ec.gc.ca/report/real_time_e.html?stn={}&mode=Graph&startDate={}&endDate={}&prm1=46&y1Max=&y1Min=&max1=1&min1=1&mean1=1&prm2=-1&y2Max=&y2Min".format(station,thirty_day_before,currentDT))
    if counter == 0:
        I_Agree = driver.find_elements_by_xpath("//input[@name='disclaimer_action' and @value='I Agree']")[0]
        I_Agree.click()
        counter = +1
        print (counter)
    driver.execute_script("window.scrollTo(0,700);")
    time.sleep(30)

    driver.get("https://wateroffice.ec.gc.ca/report/real_time_e.html?stn={}&mode=Graph&startDate={}&endDate={}&prm1=46&y1Max=&y1Min=&prm2=47&y2Max=&y2Min=".format(station,thirty_day_before,currentDT))
    driver.execute_script("window.scrollTo(0,650);")
    time.sleep(30)
    if station in image_station:
        driver.get("https://wateroffice.ec.gc.ca/report/station_images_e.html?mode=Table&stn={}".format(station))
        driver.execute_script("window.scrollTo(0,400);")
        time.sleep(30)
    print (station_went_through)
