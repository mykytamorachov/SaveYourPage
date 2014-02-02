from django.conf.urls import patterns, include, url
from app import views as views
from django.contrib import admin
from app.decorators import is_user, is_guest
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', is_user(views.Main.as_view()), name='home'),
    url(r'^login', is_guest(views.Index.as_view()), name='login'),
    url(r'^register', is_guest(views.Register.as_view()), name='register'),
    url(r'^forgot_password', is_guest(views.Forgot.as_view()), name='forgot'),
    url(r'^add_page/', views.addPage, name='add-page'),
    url(r'^add_category/', views.addCategory, name='add-category'),
    url(r'^delete_category/', views.deleteCategory, name='delete-category'),
    url(r'^get_user/', views.getUser, name='get-user'),
    url(r'^reg_user/', views.register, name='register-user'),
    url(r'^log_in/', views.log_in, name='log-in'),
    url(r'^log_out/', views.logout_user, name='log-out'),


    # url(r'^blog/', include('blog.urls')),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
     {'document_root': '/Users/air13/Desktop/SaveYourPage/static'}),

    url(r'^admin/', include(admin.site.urls)),
)
