from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import mysql.connector
import time
import secrets

INSIDE_DATATYPE = "inside_temp"
OUTSIDE_DATATYPE = "outside_temp"
ATREA_PASS = secrets.ATREA_PASS

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
d.get('http://192.168.2.19/main.htm')

# wait up to seconds for the elements to become available
d.implicitly_wait(1)

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
f=open("/data/TempStats/temperatures.txt", "a+")
f.write(time.strftime("%Y-%m-%d %H:%M") + ";" + OUTSIDE_DATATYPE + ";" + OUTSIDE_TEMP[:-2] + "\n")
f.write(time.strftime("%Y-%m-%d %H:%M") + ";" + INSIDE_DATATYPE + ";" + INSIDE_TEMP[:-2] + "\n")
f.close()

# insert outside temperature into Database
sql = "INSERT INTO meteo (id, date, type, value) VALUES (%s, %s, %s, %s)"
val = ("0", time.strftime("%Y-%m-%d %H:%M"), OUTSIDE_DATATYPE, OUTSIDE_TEMP[:-2])
mycursor.execute(sql, val)
mydb.commit()
print(mycursor.rowcount, "record inserted.")

# insert intside temperature into Database
sql = "INSERT INTO meteo (id, date, type, value) VALUES (%s, %s, %s, %s)"
val = ("0", time.strftime("%Y-%m-%d %H:%M"), INSIDE_DATATYPE, INSIDE_TEMP[:-2])
mycursor.execute(sql, val)
mydb.commit()
print(mycursor.rowcount, "record inserted.")

