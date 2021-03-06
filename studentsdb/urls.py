"""studentsdb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import patterns, include, url
from django.contrib import admin
from students.views.students import StudentUpdateView, StudentAddView, StudentDeleteView
from students.views.groups import GroupsAddView, GroupsUpdateView, GroupsDeleteView


urlpatterns = patterns('',
# Students urls
url(r'^$', 'students.views.students.students_list', name='home'),
url(r'^students/add/$', StudentAddView.as_view(), name='students_add'),
url(r'^students/(?P<pk>\d+)/edit/$', StudentUpdateView.as_view(), name='students_edit'),
url(r'^students/(?P<pk>\d+)/delete/$', StudentDeleteView.as_view(), name='students_delete'),

# Groups urls
url(r'^groups/$', 'students.views.groups.groups_list', name='groups'),
url(r'^groups/add/$', GroupsAddView.as_view(), name='groups_add'),
url(r'^groups/(?P<pk>\d+)/edit/$', GroupsUpdateView.as_view(), name='groups_edit'),
url(r'^groups/(?P<pk>\d+)/delete/$', GroupsDeleteView.as_view(), name='groups_delete'),
url(r'^admin/', include(admin.site.urls)),

# Journal urls
url(r'^journal/$', 'students.views.journal.students_list', name='journal'),
url(r'^exam', 'students.views.exam.exams_list', name='exam'),
# Isputs urls
url(r'^exam', 'students.views.exam.exams_list', name='exam'),

# Contact urls
url(r'^contact-admin/$', 'students.views.contact_admin.contact_admin', name='contact_admin'),
					   )
from .settings import MEDIA_ROOT, DEBUG

if DEBUG:
	urlpatterns += patterns('', url(r'^media/(?P<path>.*)$', 	'django.views.static.serve', {'document_root': MEDIA_ROOT}))
