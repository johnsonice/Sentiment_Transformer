#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  9 12:18:59 2019

@author: huang
"""
## set environment variable 
import os
#os.system('export GOOGLE_APPLICATION_CREDENTIALS="/home/chengyu/Dev/keys/API Project-f7e180c70a13.json"')
# Imports the Google Cloud client library
from googletrans import Translator
from google.cloud import translate
import time

#%%

class Back_translator():
    def __init__(self,mode='google'):
        self.mode = mode
        if self.mode == 'google':
            # Instantiates a client
            self.translator=translate.Client()
        else:
            self.translator=Translator()
        self.LANGUAGES = {
                'zh-cn': 'chinese (simplified)',
                'ko': 'korean',
                'ar': 'arabic',
                'af': 'afrikaans',
                'sq': 'albanian',
                'am': 'amharic',
                'hy': 'armenian',
                'az': 'azerbaijani',
                'eu': 'basque',
                'be': 'belarusian',
                'bn': 'bengali',
                'bs': 'bosnian',
                'bg': 'bulgarian',
                'ca': 'catalan',
                'ceb': 'cebuano',
                'ny': 'chichewa',
                'zh-tw': 'chinese (traditional)',
                'co': 'corsican',
                'hr': 'croatian',
                'cs': 'czech',
                'da': 'danish',
                'nl': 'dutch',
                'en': 'english',
                'eo': 'esperanto',
                'et': 'estonian',
                'tl': 'filipino',
                'fi': 'finnish',
                'fr': 'french',
                'fy': 'frisian',
                'gl': 'galician',
                'ka': 'georgian',
                'de': 'german',
                'el': 'greek',
                'gu': 'gujarati',
                'ht': 'haitian creole',
                'ha': 'hausa',
                'haw': 'hawaiian',
                'iw': 'hebrew',
                'hi': 'hindi',
                'hmn': 'hmong',
                'hu': 'hungarian',
                'is': 'icelandic',
                'ig': 'igbo',
                'id': 'indonesian',
                'ga': 'irish',
                'it': 'italian',
                'ja': 'japanese',
                'jw': 'javanese',
                'kn': 'kannada',
                'kk': 'kazakh',
                'km': 'khmer',
                'ku': 'kurdish (kurmanji)',
                'ky': 'kyrgyz',
                'lo': 'lao',
                'la': 'latin',
                'lv': 'latvian',
                'lt': 'lithuanian',
                'lb': 'luxembourgish',
                'mk': 'macedonian',
                'mg': 'malagasy',
                'ms': 'malay',
                'ml': 'malayalam',
                'mt': 'maltese',
                'mi': 'maori',
                'mr': 'marathi',
                'mn': 'mongolian',
                'my': 'myanmar (burmese)',
                'ne': 'nepali',
                'no': 'norwegian',
                'ps': 'pashto',
                'fa': 'persian',
                'pl': 'polish',
                'pt': 'portuguese',
                'pa': 'punjabi',
                'ro': 'romanian',
                'ru': 'russian',
                'sm': 'samoan',
                'gd': 'scots gaelic',
                'sr': 'serbian',
                'st': 'sesotho',
                'sn': 'shona',
                'sd': 'sindhi',
                'si': 'sinhala',
                'sk': 'slovak',
                'sl': 'slovenian',
                'so': 'somali',
                'es': 'spanish',
                'su': 'sundanese',
                'sw': 'swahili',
                'sv': 'swedish',
                'tg': 'tajik',
                'ta': 'tamil',
                'te': 'telugu',
                'th': 'thai',
                'tr': 'turkish',
                'uk': 'ukrainian',
                'ur': 'urdu',
                'uz': 'uzbek',
                'vi': 'vietnamese',
                'cy': 'welsh',
                'xh': 'xhosa',
                'yi': 'yiddish',
                'yo': 'yoruba',
                'zu': 'zulu',
                'fil': 'Filipino',
                'he': 'Hebrew'
            }
    def back_translate(self,sentence,rep_n=1,unique=True,langs=[],src='en'):
        lang_list = list(self.LANGUAGES.keys())
        if len(langs) == 0:
            langs = lang_list[:rep_n]
        
        res = [sentence]
        for lang in langs:
            time.sleep(1)
            if self.mode == 'google':
                try:
                    des_sent = self.translator.translate(sentence,target_language=lang)['translatedText']
                    back_sent = self.translator.translate(des_sent,target_language='en')['translatedText']
                except:
                    print('limit hit, wait for 100 sec')
                    time.sleep(100)
                    des_sent = self.translator.translate(sentence,target_language=lang)['translatedText']
                    back_sent = self.translator.translate(des_sent,target_language='en')['translatedText']
            else:
                try:
                    des_sent = self.translator.translate(sentence,dest=lang,src='en').text
                    back_sent = self.translator.translate(des_sent,dest='en',src=lang).text
                except:
                    print('limit hit, wait for 100 sec')
                    time.sleep(100)
                    des_sent = self.translator.translate(sentence,dest=lang,src='en').text
                    back_sent = self.translator.translate(des_sent,dest='en',src=lang).text
                    
            
            res.append(back_sent)
        
        return list(set(res))
        
#%%
if __name__ == "__main__":
    BT = Back_translator(mode='google')
    
    test = '''Policy support, strengthening external demand,  \
            and supply-side reforms have helped maintain strong growth which, \
            along with tighter enforcement of capital flow management measures, \
            has also reduced exchange rate pressure. Regulators have recently focused \
            on addressing financial sector risks, resulting in tightening financial conditions. \
            The five-yearly Communist Party Congress is scheduled for the fall.'''
    print(test)

    print(BT.back_translate(test,rep_n =5,unique=False))
