# ATREA RA5 Temp stats

Python script to tead temp values from ATREA RA5 recuperation unit and upload to MySQL DB </br> </br>

## Prerequisites
To use atrea temp stats, you need first a `secrets.py` file with following content:
```
ATREA_PASS="<pass>"   # password to atrea unit interface
DB_USER="<user>"
DB_PASS="<pass>"
DB_NAME="<name>"
DB_HOST="<host>"
```
</br>
- make sure, python 3.x is installed </br>
- also change variables in file `read_temp.py`</br>
</br>

## Docker Version

**to build the image, run:**
```
docker build -t atrea-temp-stats:1.0.1 .
```

**to read the values, start a container with the corect script:**
```
docker run -it -w /usr/workspace -v $(pwd)/scripts:/usr/workspace atrea-temp-stats:1.0.1 python read_temp.py
```

</br>

## To use as standalone python version
prerequisites:
`python3.8`,`unzip`,`pip3`,`selenium`,`chromedriver`


1. install mysql connector:
(install it as standard user, not root)
```
pip install mysql-connector-python-rf
```

2. install chrome/chromium and chromedriver, and change permissions:
```
pip install chromedriver-py
pip install chromedriver-binary
sudo chown <user>:<user> /usr/local/bin/chromedriver
```

3. run script:
```
python3 read_temp.py
```


### DB STUFF TO DO:
- https://tableplus.com/blog/2018/08/mysql-how-to-turn-off-only-full-group-by.html
