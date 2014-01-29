#coding: utf-8
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.views.generic import TemplateView, FormView
from django.shortcuts import redirect
from rest_framework import status
from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout, user_logged_in
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.template import Context
from django.core.exceptions import ValidationError
from SaveYourPage.settings import STATIC_ROOT
from app.models import Page,Category
from BeautifulSoup import BeautifulSoup
import os
import unicodedata
import urllib2
import slugify
from django.views.decorators.csrf import csrf_exempt
from app.forms import RegisterForm, LoginForm, ForgotPassForm, CategoryForm


class Index(FormView):
    template_name = 'login.html'
    form_class = LoginForm

    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        if form.auth():
            self.request.session['user_id'] = form.resp
        else:
            messages.error(self.request, 'Wrong login or password.')
            return self.form_invalid(form)
        return super(Index, self).form_valid(form)


class Main(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(Main, self).get_context_data(**kwargs)
        cats = Category.objects.all()
        categories = {}
        pages = {}
        cc = []
        pp=[]
        form = CategoryForm()
        page = Page.objects.all()
        for p in page:
            pages.update({p.id:{
                'url':p.url,
                'title':p.title,
                'image':p.image_file,
                'category':p.category.name,
                'page_id':p.pk
            }})
        for row in pages:
            pp.append(pages[row])
        for cat in cats:
            categories.update({cat.id:{
                'id': cat.id,
                'name': cat.name}})
        for row in categories:
            cc.append(categories[row])
        print
        context.update({'categories': cc,'pages':pp, 'user_id':self.request.user.id})
        return context





class Register(FormView):
    template_name = 'register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('register')

    def get_context_data(self, **kwargs):
        context = super(Register, self).get_context_data(**kwargs)

        return context

    def form_valid(self, form):
        if form.save():
            messages.success(
                self.request,
                'Registration completed. You will receive an email as soon as the manager to confirm your account.')
        else:
            for error in form.error_messages:
                print error
                messages.error(self.request, error['err_msg'])
            return self.form_invalid(form)
        return super(Register, self).form_valid(form)


class Forgot(FormView):
    template_name = 'forgot_password.html'
    form_class = ForgotPassForm

    def get_context_data(self, **kwargs):
        context = super(Forgot, self).get_context_data(**kwargs)
        return context

@api_view(['GET', 'POST'])
def addCategory(request):
    f = CategoryForm(request)
    f.save()
    return True

@api_view(['GET', 'POST'])
def getUser(request):
    user = User.objects.get(pk=request.GET.get('id'))
    return Response(user.username)


@api_view(['GET', 'POST'])
def register(request):
    resp = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User(username=username, email=email, password=password)
        try:
            user.save()
        except Exception:
            resp.update({'error': Exception.message})
            return Response(resp, status=500)
        return Response(status=200)
    else:
        return Response(status=404)

@api_view(['GET', 'POST'])
def log_in(request):
    if request.user.id:
        return Response({'message':'User already logged'},status=200)
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                print user
                login(request, user)
                return redirect('home')
            else:
                return Response("The username and password were incorrect.", status=500)
        else:
            return Response(status=200)

@api_view(['GET', 'POST'])
def logout_user(request):
    resp = {}
    try:
        logout(request)
    except Exception:
        resp.update({'error': Exception.message})
        return Response(resp, status=500)
    return Response(status=200)

@csrf_exempt
@api_view(['GET', 'POST'])
def addCategory(request):
    if request.method == 'GET':
        category_name = request.GET.get('name')
        user = User.objects.get(pk=request.user.id)
        category = Category(name=category_name, user=user)
        category.save()
        return redirect('home')
    else:
        return Response(status=403)

@api_view(['GET', 'POST'])
def deleteCategory(request):
    if request.method == 'POST':
        category_id = request.POST.get('id')
        category = Category.objects.get(pk=category_id)
        category.delete()
        return redirect('home')
    else:
        return Response(status=403)

@api_view(['GET', 'POST'])
def addPage(request):
    if request.method == 'GET':
        page_url = request.GET.get('url')
        category_id = request.GET.get('category')

        webpage = urllib2.urlopen(page_url).read()
        soup = BeautifulSoup(''.join(webpage))
        user = User.objects.get(pk=request.user.id)
        category = Category.objects.get(id=category_id)

        page_title = soup('title')[0].string
        page_title = slugify.slugify_ru(page_title)
        file_name = u''.join(e for e in page_title if e.isalnum())
        file_name = slugify.slugify_ru(file_name)
        os.system(STATIC_ROOT+"/webkit2png.py -D "+STATIC_ROOT+"'/images/'"+str(request.user.id)+"  -T -o "+file_name+" "+page_url)
        page = Page(title=page_title, url=page_url, image_file=file_name+'.png',category=category, user=user)
        page.save()
        return redirect('home')
    else:
        return Response(status=403)

@api_view(['GET', 'POST'])
def deletePage(request):
    if request.method == 'GET':
        page_id = request.GET.get('id')
        page = Page.objects.get(pk=page_id)
        page.delete()
