# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from ..models import Student
#Views for Students
def students_list(request):
   students = Student.objects.all()

   #try to order student_list
   order_by = request.GET.get('order_by', '')
   if order_by in ('first_name', 'last_name', 'ticket', 'id'):
      students = students.order_by(order_by)
      if request.GET.get('reverse', '') == '1':
         students = students.reverse()

   #pagination students
   paginator = Paginator(students, 3)
   page = request.GET.get('page')
   try:
      students = paginator.page(page)
   except PageNotAnInteger:
      # IF page NOT an integer
      students = paginator.page(1)
   except EmptyPage:
      # IF page number of range
      students = paginator.page(paginator.num_pages)


   return render(request, 'students/students_list.html', {'students': students})

def students_add(request):
   return HttpResponse('<h1>Student Add Form </h1>')

def students_edit(request, sid):
   return HttpResponse('<h1>Student Edit %s</h1>' %sid)

def students_delete(request, sid):
   return HttpResponse('<h1>Student Delete %s</h1>' %sid)



