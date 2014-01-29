# -*- coding: utf-8 -*-
from django.shortcuts import redirect
from django.contrib import messages
from django.conf import settings
from django.core.cache import get_cache
from functools import wraps

def is_user(view_func):

    def _view(request, *args, **kwargs):
        if not request.user.id:
            messages.error(request, 'Access denied. Sign in to continue.')
            return redirect('login')
        return view_func(request, *args, **kwargs)

    return _view


def is_guest(view_func):

    def _view(request, *args, **kwargs):
        if request.user.id:
            return redirect('home')
        return view_func(request, *args, **kwargs)

    return _view


def is_admin(view_func):

    def _view(request, *args, **kwargs):
        u = request.user
        if not u.is_authenticated() and not u.is_staff:
            messages.error(request, 'You are not admin. Sign in as admin to continue')
            return redirect('login')
        return view_func(request, *args, **kwargs)

    return _view


def cached_api_request(func):
        u'''Проверка содержимого результата ф-ции в кеше'''
        
        @wraps(func)
        def calledFunc(self, *args, **kwargs):
            cache = get_cache('mongo')
            cache_timeout = settings.DEFAULT_MONGO_CACHE_TIME
            func_name = func.__name__
            if self.__class__:
                if self.__class__.__name__!='ModelBase':
                    func_name = self.__class__.__name__+'.'+func.__name__
                else:
                    func_name = self.__name__+'.'+func.__name__
            key = '%s:%s:%s' % (func_name, args, kwargs)
            if getattr(settings, 'NOCACHE', False):
                result = None
            else:
                result = cache.get(key)
            if not result or kwargs.get('without_cache', False):
                result = func(self, args, kwargs)
                
            if func_name in settings.CACHE_TIME:
                cache_timeout = settings.CACHE_TIME[func_name]                
            cache.set(key, result, cache_timeout)
            return result
        return calledFunc


def get_or_none(model, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        return None