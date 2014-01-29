from django.test import TestCase


from BeautifulSoup import BeautifulSoup
import os
import urllib2
from SaveYourPage.settings import STATIC_ROOT

webpage = urllib2.urlopen('http://yandex.ru/').read()
soup = BeautifulSoup(''.join(webpage))
title = soup('title')[0].string
file_name = ''.join(e for e in title if e.isalnum())
os.system(STATIC_ROOT+"/webkit2png.py -D "+STATIC_ROOT+"'/images/USER_ID'  -T -o "+file_name+" "+url)