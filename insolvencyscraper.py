# -*- coding: utf-8 -*-
"""insolvencyscraper.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1JfsBxk-uMfjVdrvUeyHjrDZcVR6JVX8E
"""

#Install libraries
!pip install scraperwiki
import scraperwiki
import lxml.html
!pip install cssselect
import cssselect
#import pandas
import pandas as pd
#install library to export files
from google.colab import files
#For timer
import time

def scrapedetail(url):
  print("scraping",url)
  #use the scrape function on that url
  html = scraperwiki.scrape(url)
  # turn that variable's contents into an lxml object, making it easier to drill into
  root = lxml.html.fromstring(html) 
  #The basic info is all in <div class="notice-data"> and then <dd>
  noticedata = root.cssselect('div.notice-data dd')
  #The first and second and third items contain data we store
  noticecategory = noticedata[0].text_content()
  noticetype = noticedata[1].text_content()
  pubdate = noticedata[2].text_content()
  #The notice codes provide further detail
  #See https://www.thegazette.co.uk/noticecodes
  #We need to identify which ≤dt> has 'Notice code' to scrape the relevant <dd>
  noticedlabels = root.cssselect('div.notice-data dt')
  #Measure the list so we can loop
  howlong = len(noticedlabels)
  #Loop through numbers
  #Set a default value first
  noticecode = "NO DATA"
  for i in range(0,howlong):
    #Check the text at that index in that list of labels
    if noticedlabels[i].text_content() == 'Notice code:':
      #If it does, grab the corresponding index from the other list of values
      noticecode = noticedata[i].text_content()
  #Create a dictionary
  record = {}
  record['url'] = url
  record['noticecategory'] = noticecategory
  record['noticetype'] = noticetype
  record['noticecode'] = noticecode
  record['pubdate'] = pubdate
  #Other data is in helpful data-gazettes attributes like so:
  companynames = root.cssselect('[data-gazettes="CompanyName"]')
  if len(companynames)>0:
    companyname = companynames[0].text_content()
  else:
    companyname = "NO DATA"
  compnums = root.cssselect('[data-gazettes="CompanyNumber"]')
  if len(compnums)>0:
    compnum = compnums[0].text_content()
  else:
    compnum = "NO DATA"
  record['compnum'] = compnum
  record['companyname'] = companyname
  addresses = root.cssselect('[data-gazettes="CompanyRegisteredOffice"]')
  if len(addresses)>0:
    address = addresses[0].text_content()
  else:
    address = "NO DATA"
  dobs = root.cssselect('[data-gazettes="BirthDetails"]')
  if len(dobs)>0:
    dob = dobs[0].text_content()
  else:
    dob = "NO DATA"
  persdetails = root.cssselect('[data-gazettes="PersonDetails"]')
  if len(persdetails)>0:
    persdetail = persdetails[0].text_content()
  else:
    persdetail = "NO DATA"
  record['compnum'] = compnum
  record['address'] = address
  record['dob'] = dob
  record['persdetail'] = persdetail

  typesofliq = root.cssselect('[data-gazettes="TypeOfLiquidation"]')
  if len(typesofliq)>0:
    typeofliq = typesofliq[0].text_content()
  else:
    typeofliq = "NO DATA"
  record['typeofliq'] = typeofliq
  return(record)

#Set timer
t0= time.clock()
print("Timer started",t0)

#Create a dataframe to store data
df = pd.DataFrame(columns=["notices"])

startnum = 3391187-210000
endnum = startnum-5000
#When going backwards you have to add a negative 'step' argument
for i in range(startnum, endnum, -1):
  #Some URLs are broken so to stop those breaking the scraper we use try/except
  try:
    #We have to convert to string to add to URL
    scraperesult = scrapedetail('https://m.thegazette.co.uk/notice/'+str(i))
    #print(scraperesult)
    df = df.append(scraperesult, ignore_index=True)
  except:
    print("problem")

#Print the dataframe to check
#print(df)
#Export to csv
df.to_csv("notices.csv")
#Download it automatically in case the runtime disconnects before we check and do it manually
files.download('notices.csv') 

#End timer
t1 = time.clock() - t0
print("Time elapsed: ", t1) # CPU seconds elapsed (floating point)