# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
#Views for Students
def students_list(request):
   students = (
      {'id': 1,
       'first_name': u'Віталій',
       'last_name': u'Статкевич',
       'ticket': 235,
       'image': 'img/WS.jpeg'},
      {'id': 2,
       'first_name': u'Акакій',
       'last_name': u'Бипка',
       'ticket': 236,
       'image': 'img/AK.jpeg'},
      {'id': 3,
       'first_name': u'Васілєвс',
       'last_name': u'Корчман',
       'ticket': 237,
       'image': 'img/WW.jpeg'},
      )
   return render(request, 'students/students_list.html', {'students': students})

def students_add(request):
   return HttpResponse('<h1>Student Add Form </h1>')

def students_edit(request, sid):
   return HttpResponse('<h1>Student Edit %s</h1>' %sid)

def students_delete(request, sid):
   return HttpResponse('<h1>Student Delete %s</h1>' %sid)

#Views for Groups

def groups_list(request):
   groups = (
     {'id': 1,
      'name': u'ПІ-416',
      'captain': u'ТАня'},
     {'id': 2,
      'name': u'ПІ-415',
      'captain': u'Крас'},
     )
   return render(request, 'students/groups_list.html',{'groups': groups})

def groups_add(request):
   return HttpResponse('<h1>Group Add Form</h1>')

def groups_edit(request, gid):
   return HttpResponse('<h1>Edit Group %s</h1>' % gid)

def groups_delete(request, gid):
   return HttpResponse('<h1>Delete Group %s</h1>' % gid)

