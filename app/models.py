#coding: utf-8
from django.db import models
from django.contrib.auth.models import User
from SaveYourPage.settings import STATIC_ROOT
import os

class Page(models.Model):

    title = models.CharField(max_length=100)
    url = models.CharField(max_length=1000)
    image_file = models.CharField(max_length=1000)
    user = models.ForeignKey(User, related_name='page')
    category = models.ForeignKey('Category', related_name='pages')


class Category(models.Model):

    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, related_name='category')

# category = Category(name='Art')
# category.save()
# user = User.objects.get(id=1)
# category = Category.objects.get()
# page = Page(title='google',url='http://google.com/',image_file='/Users/air13/Desktop/SaveYourPage/foo-thumb.png',
#             user=user,
#             category=category)
# page.save()
# page = Page.objects.get(id=3)
# print user.id

# name = ''.join(e for e in title if e.isalnum())
# os.system(STATIC_ROOT+"/webkit2png.py -D "+STATIC_ROOT+"'/images/USER_ID'  -T -o "+name+" "+url)
