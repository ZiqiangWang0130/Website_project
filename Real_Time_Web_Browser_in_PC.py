#before running the scripts, make sure downloading the right driver to corporate with the platform and web-browser you used 
#from here: https://selenium-python.readthedocs.io/installation.html

#import mudules needed for the script
import os
from selenium import webdriver
#from selenium.webdriver.chrome.options import Options
import csv
import random
import time
import datetime
from datetime import timedelta

#get the cuurent date and time so that we can set the range of the period we want to display
currentDT = datetime.datetime.now().strftime('%Y-%m-%d')
thirty_day_before = (datetime.datetime.now() - timedelta(days = 30)).strftime('%Y-%m-%d')

All_station = []
image_station = []
station_went_through = []
counter = 0

#get the path of the csv file which contains station name and ID 
path = os.getcwd() + "\\" + 'Active_hydrology_Stations_2019-05-30.csv'

#go throgh the csv file and create two list.
#one called All_station which contains all the active station, another called image_station contains all the station which has real time image
with open(path) as csvDataFile:																			
	csvReader = csv.reader(csvDataFile)													
	for row in csvReader:
		All_station.append(row[0])
		image_station.append(row[12])

#create web driver and maximized the window
firefox_options = Options()
#chrome_options.add_argument("--kiosk")
firefox_options.add_argument("--start-maximized")
driver = webdriver.Firefox()

#Change the size of the content
#driver.get('chrome://settings/')
#driver.execute_script('chrome.settingsPrivate.setDefaultZoom(0.70);')

#log into the real time website
driver.get("https://wateroffice.ec.gc.ca/login_e.html")
driver.find_element_by_id("username").send_keys("realtime")
driver.find_element_by_id("password").send_keys("hydrometric")
driver.find_elements_by_xpath("//input[@value='Login']")[0].click()


while True:
	driver.get("https://wateroffice.ec.gc.ca/google_map/google_map_e.html?map_type=real_time&search_type=province&province=all")  
	driver.execute_script("window.scrollTo(0,900);")
	time.sleep(3)
    #pick an random station 
	i = random.randint(0, len(All_station))
	station = All_station[i]
	station_went_through.append(station)
	driver.get(f"https://wateroffice.ec.gc.ca/report/real_time_e.html?stn={station}&mode=Graph&startDate={thirty_day_before}&endDate={currentDT}&prm1=46&y1Max=&y1Min=&max1=1&min1=1&mean1=1&prm2=-1&y2Max=&y2Min")
	if counter == 0:                                                        # need to click on I Agree for the first time to continue
		I_Agree = driver.find_elements_by_xpath("//input[@name='disclaimer_action' and @value='I Agree']")[0]
		I_Agree.click()
		counter = +1
		print (counter)
	driver.execute_script("window.scrollTo(0,700);")
	time.sleep(3)

	driver.get(f"https://wateroffice.ec.gc.ca/report/real_time_e.html?stn={station}&mode=Graph&startDate={thirty_day_before}&endDate={currentDT}&prm1=46&y1Max=&y1Min=&prm2=47&y2Max=&y2Min=")
	driver.execute_script("window.scrollTo(0,650);")
	time.sleep(3)
	if station in image_station:                                            #if the station has a real time image, then show the image
		driver.get(f"https://wateroffice.ec.gc.ca/report/station_images_e.html?mode=Table&stn={station}")
		driver.execute_script("window.scrollTo(0,500);")
		time.sleep(3)
	print (station_went_through)

