from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import os, mysql.connector, time
import secrets
import socket
import urllib.request

#--- Edit variables below --------
INSIDE_DATATYPE = "inside_temp"
OUTSIDE_DATATYPE = "outside_temp"
ATREA_PASS = secrets.ATREA_PASS
ATREA_UNIT_URL = "http://192.168.2.19/main.htm"
TEMPERATURES_FILE = "temperatures.txt"
# --------------------------------

mydb = mysql.connector.connect(
  host=secrets.DB_HOST,
  user=secrets.DB_USER,
  passwd=secrets.DB_PASS,
  database=secrets.DB_NAME,
  auth_plugin="mysql_native_password"
)

mycursor = mydb.cursor()

chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-dev-shm-usage')
d = webdriver.Chrome('/usr/local/bin/chromedriver',options=chrome_options)
d.get(ATREA_UNIT_URL)

# wait up to seconds for the elements to become available
d.implicitly_wait(5)

# send the password
element = d.find_element_by_xpath("//input[1]");
element.send_keys(ATREA_PASS)

# simulate hitting enter
element.send_keys(Keys.ENTER)

# wait up to seconds for the elements to become available
d.implicitly_wait(2)

# get the temperature
OUTSIDE_TEMP = d.find_element_by_xpath('//*[@id="contentBoxI10202"]/div').text
INSIDE_TEMP = d.find_element_by_xpath('//*[@id="contentBoxI10200"]/div').text
d.quit()

# write the temperature values to file
CURRENT_DIR = os.getcwd()
#f=open(os.path.join(sys.path[0], TEMPERATURES_FILE), "a+")
f=open(CURRENT_DIR+"/"+TEMPERATURES_FILE, "a+")
f.write(time.strftime("%Y-%m-%d %H:%M") + ";" + OUTSIDE_DATATYPE + ";" + OUTSIDE_TEMP[:-2] + "\n")
f.write(time.strftime("%Y-%m-%d %H:%M") + ";" + INSIDE_DATATYPE + ";" + INSIDE_TEMP[:-2] + "\n")
f.close()

# insert outside temperature into Database
sql = "INSERT INTO meteo (id, timestamp, type, value) VALUES (%s, %s, %s, %s)"
val = ("0", time.strftime("%Y-%m-%d %H:%M"), OUTSIDE_DATATYPE, OUTSIDE_TEMP[:-2])
mycursor.execute(sql, val)
mydb.commit()
print(mycursor.rowcount, "record inserted.")

# insert intside temperature into Database
sql = "INSERT INTO meteo (id, timestamp, type, value) VALUES (%s, %s, %s, %s)"
val = ("0", time.strftime("%Y-%m-%d %H:%M"), INSIDE_DATATYPE, INSIDE_TEMP[:-2])
mycursor.execute(sql, val)
mydb.commit()
print(mycursor.rowcount, "record inserted.")

# send notification to Healthchecks.io
if secrets.HEALTHCHECK_ENABLED:
    urllib.request.urlopen("https://hc-ping.com/"+secrets.HEALTHCHECK_UID, timeout=10)
