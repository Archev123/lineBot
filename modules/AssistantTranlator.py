# -*- coding: utf-8 -*-
"""
Created on Thu Sep 20 21:50:14 2019

@author: Deforest
"""
from translate import Translator
from urllib.parse import quote
from linebot.models import TextSendMessage, AudioSendMessage

class assistantTranslator:
    
    langSet={"@英文": "en", "@韓文": "ko", "@中文": "zh-Hant"}
    
    def __init__(self, toLang='', oriText=''):
        self.toLang = toLang
        self.oriText = oriText
        
    def setLang(self, tolang):
        self.toLang = self.langSet.get(tolang, "None")
    
    def setText(self, oriText):
        self.oriText = oriText
        
    def startTranslate(self):
        if self.toLang == "None":
            return TextSendMessage("Do not support this language now, please try again or type @使用說明 to understand usage")
        else:
            translator = Translator(from_lang='zh-Hant', to_lang=self.toLang)
            translation = translator.translate(self.oriText)
            text = quote(translation)
            speakTime = 0.4*len(translation)
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query=' + text + '&language=' + self.toLang
            replyMessage = [
                    TextSendMessage(translation),
                    AudioSendMessage(stream_url, (int(speakTime) + 1) * 1000)
                    ]
            return replyMessage
        
