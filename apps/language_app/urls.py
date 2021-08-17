from django.conf.urls import url, include
from django.urls.conf import path, re_path
from . import views

urlpatterns=[
    re_path('^$', views.home),
    re_path('^register$', views.register),
    re_path('^login$', views.login),
    re_path('^logout$', views.logout),
    re_path('^all_translations$', views.translations),
    re_path('^add_translation$', views.addTranslation),
    re_path('^submit_translation$', views.submitTranslation),
    re_path('^delete_translation$', views.deleteTranslation),
]