from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from datetime import date, timedelta
import datetime
import GBG_settings
import urllib
import urllib2

driver = webdriver.Chrome('/Users/jacob/Downloads/chromedriver')

driver.get("http://gears.guidebook.com")

email = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.NAME,"email")))
email.send_keys(GBG_settings.USERNAME)
pw = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.NAME,"password")))
pw.send_keys(GBG_settings.PASSWORD)
pw.send_keys(Keys.ENTER)
#need login stuff here

#once logged in, pull up pending
pending = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,"//*[contains(text(),'Pending Guides')]")))
pending.click()

#
pending_list = WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,"//div[@id='contentContainer']/div/div/div/table[2]/tbody/tr/td")))
guide_names = []
for x in range(0,len(pending_list)):
	if (x % 4 == 0):
		guide_names.append(str(pending_list[x].text))

#import pdb;pdb.set_trace()
del guide_names[0]
final_names = []
message = ""
counter = 0
for x in guide_names:
	if (x[len(x) - 31:] != "Enterprise Guide, Please Ignore"):
			final_names.append(x)
	else:
		counter += 1
if counter > 0:
	alttext = "excluding the " + str(counter) + " Enterprise guides"
else:
	alttext = "and zero Enterprise guides"

if (len(final_names) > 0):
	if (len(final_names) == 1):
		color = "purple"
		message = "There is " + str(len(final_names)) + " pending guide (" + alttext + ") in the queue."
	else:
		color = "purple"
		message =  "There are " + str(len(final_names)) + " pending guides (" + alttext + ") in the queue."
else:
	color = "green"
	message = "There are currently no pending guides (" + alttext + ") in the queue."
if (len(final_names) >= 5):
	color = "purple"
url = "https://api.hipchat.com/v1/rooms/message?format=json&auth_token=3077b7e43c67a517b24ee9e52b778b"
#values = {'scope': 'send_notification','message':str(message),'color':'green','notify':'1'}
data = {'room_id':994606,'from':'PendingBot','notify':1,'message':message.encode('utf-8'),'color':color,'message_format':'text'}
params = urllib.urlencode(data)
#request = urllib2.Request(url,params)
#response = urllib2.urlopen(request)
f = urllib.urlopen(url,params)
f.close()
#print response.read()
driver.close()

