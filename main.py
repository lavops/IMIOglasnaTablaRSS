import requests
import sqlite3

import os
from os.path import isfile, join

import json
from bs4 import BeautifulSoup

from functions import *
from mail import sendMail
   
def main():
    feeds = loadFeeds()

    for feed in feeds:
        feedName = feed["name"]
        feedUrl = feed["url"].rstrip()
        print("Proveravam " + feedName)
        connection = sqlite3.connect(feedName + '.db')
        c = connection.cursor()
        databaseConnection(feedName, c)
        data = checkDiff(feedUrl, feedName, c)
        connection.commit()
        c.close()
        connection.close()

        if(data):
            mails = loadMails()
            for mail in mails:
                html = makeBody(data)
                sendMail(html, mail['mail'], feedName)
        else:
            print('Nema promena')

main()