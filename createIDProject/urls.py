# -*- coding: utf-8 -*-
"""createIDProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import url
from django.contrib import admin
from django.views.generic import TemplateView
from createIdApp import views
from taoBaoMonitorApp import views2
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    url(r'^createPros', views.createPros, name='createPros'),
    url(r'^lsedit_projects', views.lsedit_projects, name='lsedit_projects'),
    url(r'^lsAll_PinLun', views.lsAll_PinLun, name='lsAll_PinLun'),
    url(r'^lsDelete_data$', views.lsDelete_data, name='lsDelete_data'),

    #淘宝数据采集API
    url(r'^getAllDatas', views2.getAllDatas, name='getAllDatas'),
    url(r'^getAllBuildData', views2.getAllBuildData, name='getAllBuildData'),
    url(r'^makeDownloadExcel', views2.makeDownloadExcel, name='makeDownloadExcel'),
    url(r'^inserProject', views2.inserProject, name='inserProject'),
    url(r'^removeDataAPI', views2.removeDataAPI, name='removeDataAPI'),
    url(r'^startUpSpider', views2.startUpSpider, name='startUpSpider'),


]

urlpatterns += staticfiles_urlpatterns()