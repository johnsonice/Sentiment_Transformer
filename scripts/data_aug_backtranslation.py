#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  9 12:18:59 2019

@author: huang
"""

from googletrans import Translator
#%%

class Back_translator():
    def __init__(self):
        self.translator=Translator()
        self.LANGUAGES = {
                'af': 'afrikaans',
                'sq': 'albanian',
                'am': 'amharic',
                'ar': 'arabic',
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
                'zh-cn': 'chinese (simplified)',
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
                'ko': 'korean',
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
    def back_translate(self,sentence,rep_n=1,langs=[],src='en',unique=True):
        lang_list = list(self.LANGUAGES.keys())
        if len(langs) == 0:
            langs = lang_list[:rep_n]
        
        res = [sentence]
        for lang in langs:
            des_sent = self.translator.translate(sentence,dest=lang,src='en').text
            back_sent = self.translator.translate(des_sent,dest='en',src=lang).text
            res.append(back_sent)
        
        return list(set(res))
        

        

#%%
if __name__ == "__main__":
    BT = Back_translator()
    #%%
    
    test = '''Policy support, strengthening external demand,  \
            and supply-side reforms have helped maintain strong growth which, \
            along with tighter enforcement of capital flow management measures, \
            has also reduced exchange rate pressure. Regulators have recently focused \
            on addressing financial sector risks, resulting in tightening financial conditions. \
            The five-yearly Communist Party Congress is scheduled for the fall.'''
    print(test)
    #%%
    BT.back_translate(test,rep_n = 10)
