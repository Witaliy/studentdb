# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from ..models import Student,Group
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

   if request.method == 'POST':
      if request.POST.get('add_button') is not None:
         errors = {}

         if not errors:
            student = Student(
               first_name = request.POST['first_name'],
               last_name = request.POST['last_name'],
               middle_name = request.POST['middle_name'],
               birthday = request.POST['birthday'],
               ticket = request.POST['ticket'],
               student_group = Group.objects.get(pk=request.POST['student_group']),
               photo = request.FILES['photo']
            )

            student.save()

            return HttpResponseRedirect(reverse('home'))

         else:
            return render(request, 'students/students_add.html', {'groups': Group.objects.all().order_by('title'),'errors': errors})

      elif request.POST.get('cancel_button') is not None:
         return HttpResponseRedirect(reverse('home'))

   else:
      return render(request, 'students/students_add.html', {'groups': Group.objects.all().order_by('title')})

def students_edit(request, sid):
   return HttpResponse('<h1>Student Edit %s</h1>' %sid)

def students_delete(request, sid):
   return HttpResponse('<h1>Student Delete %s</h1>' %sid)



