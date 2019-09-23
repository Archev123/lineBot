# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 20:27:32 2019

@author: Deforest
"""

import requests
from linebot.models import TextSendMessage
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

class invoice:

    def __init__(self):
        self.number = 0
        self.url = requests.get("http://invoice.etax.nat.gov.tw/invoice.xml")
        self.tree = ET.fromstring(self.url.text)
        try:
            items = list(self.tree.iter('item'))
            title = items[0][0].text
            awardNum = items[0][2].text
            awardNum = awardNum.replace('<p>','').replace('</p>','\n')
            self.replyMessage = title + "月: \n" + awardNum[:]
        except:
            TextSendMessage("發生一些無法預期錯誤!!!")
        
    def setNumber(self, number):
        self.number = number
    
    def run(self):
        return
        
    def show(self):
        return TextSendMessage(self.replyMessage)
        

if __name__ == "__main__":
    test = invoice()
    test.show()
