import requests
import sqlite3

import os
from os.path import isfile, join

import json
from bs4 import BeautifulSoup

from functions import *
from mail import sendMail


def makeBody(items):
    html = """
        <!DOCTYPE html>
        <html>
        <head>
        </head>
        <body>\n
        """
    
    for item in items:
        html += "<h1>" + item['title'] + "</h1>"
        html += "<link>" + item['link'] + "</link>"
        html += item['description']
        html += "<h5>" + item['author'] + "</h5>"

    html+= """
        </body>
        </html>
        """

    return html


def checkDiff(feedUrl,feedName, c):
    response = requests.get(feedUrl)
    soup = BeautifulSoup(response.content, features="xml")
    items = soup.findAll('item')
    data = []
    for item in items:
        news_item = {}
        news_item['title'] = item.title.text
        news_item['description'] = item.description.text
        if("<a href=\"pub" in news_item['description']):
            news_item['description'] = news_item['description'].replace("<a href=\"pub", "<a href=\"https://imi.pmf.kg.ac.rs/pub")
        news_item['author'] = item.author.text
        news_item['link'] = item.link.text
        news_item['guid'] = item.guid.text
        news_item['guid'] = news_item['guid'].replace("https://imi.pmf.kg.ac.rs/index.php?id=","")
        news_item['date'] = item.pubDate.text
        
        c.execute("SELECT * FROM newTable")
        news = c.fetchall()
        if(news):
            postoji = 1 #ne postoji
            for new in news:
                if(new[0] == int(news_item['guid'])):
                    postoji = 2 #postoji
                    if(new[1] != news_item['title']):
                        print("Obavestenje je promenjeno! -> " + news_item['title'])
                        data.append(news_item)
                        c.execute("UPDATE newTable SET title=(?),description=(?),date=(?) WHERE id=(?)",(news_item['title'], news_item['description'], news_item['date'], news_item['guid']))
                    elif(new[2] != news_item['description']):
                        print("Obavestenje je promenjeno! -> " + news_item['title'])
                        data.append(news_item)
                        c.execute("UPDATE newTable SET title=(?),description=(?),date=(?) WHERE id=(?)",(news_item['title'], news_item['description'], news_item['date'], news_item['guid']))
                    elif(new[5] != news_item['date']):
                        print("Obavestenje je promenjeno! -> " + news_item['title'])
                        data.append(news_item)
                        c.execute("UPDATE newTable SET title=(?),description=(?),date=(?) WHERE id=(?)",(news_item['title'], news_item['description'], news_item['date'], news_item['guid']))
                    
            if (postoji == 1):
                print("Izaslo je novo obavestenje! -> " + news_item['title'])
                data.append(news_item)
                c.execute("INSERT INTO newTable VALUES(?, ?, ?, ?, ?, ?)",(news_item['guid'], news_item['title'], news_item['description'], news_item['author'], news_item['link'], news_item['date']))         
        else:
            print("Izaslo je novo obavestenje! -> " + news_item['title'])
            data.append(news_item)
            c.execute("INSERT INTO newTable VALUES(?, ?, ?, ?, ?, ?)",(news_item['guid'], news_item['title'], news_item['description'], news_item['author'], news_item['link'], news_item['date']))
    return data


def databaseConnection(feedName, c):
    c.execute("CREATE TABLE IF NOT EXISTS newTable(id INT, title TEXT, description TEXT, author TEXT, link TEXT, date TEXT)")


def loadMails():
    MAILS_URL = os.path.dirname(os.path.abspath(__file__)) + "/mails.json"

    with open(MAILS_URL, encoding = "utf-8") as data_file:
        data = json.load(data_file)
    
    return list(data["mails"])


def loadFeeds():
    FEEDS_URL = os.path.dirname(os.path.abspath(__file__)) + "/feeds.json"

    with open(FEEDS_URL, encoding = "utf-8") as data_file:
        data = json.load(data_file)
    
    return list(data["feeds"])