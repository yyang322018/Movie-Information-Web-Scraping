#-------------------------------------------------------------------------------
# Name:        Movie Info Scraping 
# Purpose:
#
# Author:      Yi Yang
#
# Created:     04/21/2021
# Copyright:   (c) Yi Yang 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas 
import csv

def web_url():
    date=input("Please enter the date within this week in YYYY-MM-DD format:")
    base_url="https://www.imdb.com/showtimes/{}?ref_=sh_dt".format(date)
    return base_url

def parse():
    r=requests.get(web_url())
    c=r.content
    soup=BeautifulSoup(c,"html.parser")
    distance_all=soup.find_all("h4",{"class":"li_group"})
    theater_info=soup.find_all("div",{"class":["list_item odd","list_item even"]})
    list=[]
    count=0
    for i in range(0,3):
        try:
            distance=distance_all[i].text.replace("\n","").split("(")[0]
            theater_num=int(distance_all[i].find("span").text[1])
        except:
            print("Showtime is not available in this date ")
            break
        for j in range(count,theater_num+count):
            theater_name=theater_info[j].find("h3",{"itemprop":"name"}).text.replace("\n","").strip() 
            movie_all=theater_info[j].find_all("div",{"class":"list_item"})
            for movie in movie_all:
                dict={}
                dict["Distance"]=distance
                dict["Theater"]=theater_name
                dict["Movie Name"]=movie.find("h4").text.replace("\n","").strip()
                try:
                    dict["Duration"]=movie.find("time",{"itemprop":"duration"}).text.replace("\n","").strip()
                except:
                    dict["Duration"]="None"
                try:
                    rating=movie.find_all("span",{"class":"nobr"})[0].text.replace("\n","").strip().split(" ")
                    dict["User Rating"]=rating[2]
                except:
                    dict["User Rating"]="None"
                try:
                    dict["Metascore"]=movie.find("span",{"class":"metascore favorable"}).text.replace("\n","").strip()
                except:
                    dict["Metascore"]="None"
                try:
                    dict["Rank"]=movie.find_all("span",{"class":"nobr"})[1].text.replace("\n","").replace(" ","").split(":")[1]
                except:
                    dict["Rank"]="None"
                try:
                    showtime=movie.find_all("a",{"class":"tracked-offsite-link"})
                    dict["Showtime"]=""
                    for time in showtime:
                        dict["Showtime"]+=time.text.replace("\n","").replace(" ","")+" "
                except:
                    dict["Showtime"]="None"
                list.append(dict)
        count+=theater_num
    return list

def write_to_csv(list):
    df=pandas.DataFrame(list)
    df.to_csv("imdb.csv",index=False)
    return df

list=parse()
print(write_to_csv(list))
   

