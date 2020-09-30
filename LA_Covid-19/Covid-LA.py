import requests
import numpy as np
import pandas as pd 
import os
import sys
from lxml import html
from requests_html import HTMLSession
from datetime import date


#setting url links from LA county Covid Site
url = 'http://publichealth.lacounty.gov/media/coronavirus/locations.htm'
#this is the xpath for the individual Community data
p = "/html/body/div[2]/div[1]/div[3]/div/div/div/table[1]/tbody//tr"
#some os stuff for file handling
dataDir = os.getcwd()
dataDir = dataDir + '/Daily Data'

session = HTMLSession()
r = session.get(url)
r.html.render(timeout=10, sleep=10)
d = r.html.xpath('//*[@id="dte"]')
day = d[0].text
day = day.replace('/', '-')
print(day)
#here we print what data we recieved
#transform html data into text reading html element
source = html.fromstring(r.html.raw_html)
tree = source.xpath(p)
table = np.empty((0,5))

os.chdir(dataDir)

col_names = ['City/Community', 'Cases', 'Case Rate', 'Deaths', 'Death Rate']
dt = {'City/Community':'str', 'Cases':'int', 'Case Rate':'int', 'Deaths':'int', 'Death Rate':'int'}

if os.path.exists('2020-' + day + ' Covid-Data.csv'):
	print("Update hasn't happened. Try again later")
else:
	print("Now updating. creating file for: ", day)
	for rows in tree:
		city = rows[0].text_content()
		cases = rows[1].text_content()
		case_rate = rows[2].text_content()  
		deaths = rows[3].text_content()
		death_rate = rows[4].text_content()
		table = np.append(table, np.array([[city, cases, case_rate, deaths, death_rate]]), axis=0)

	df = pd.DataFrame(table, columns=col_names)
	df = df.replace('', 0)
	df = df.astype(dtype=dt)

	df.to_csv(os.path.join(dataDir ,'2020-' + day+' Covid-Data.csv'), index=False, header=True, sep=' ')

