# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime
from  django.views.generic import UpdateView

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

         data = {'middle_name': request.POST.get('middle_name'),
                 'notes': request.POST.get('notes')}

         # validate user input
         first_name = request.POST.get('first_name', '').strip()
         if not first_name:
            errors['first_name'] = u"Ім'я є обов'язковим"
         else:
            data['first_name'] = first_name

         last_name = request.POST.get('last_name', '').strip()
         if not last_name:
            errors['last_name'] = u"Прізвище є обов'язковим"
         else:
            data['last_name'] = last_name

         birthday =request.POST.get('birthday', '').strip()
         if not birthday:
            errors['birthday'] = u"Дата народження є обов'язковою"
         else:
            try:
               datetime.strptime(birthday, '%Y-%m-%d')
            except Exception:
               errors['birthday'] = u"Введіть коректний формат дати (напр. 1984-12-30)"
            else:
               data['birthday'] = birthday

         ticket = request.POST.get('ticket', '').strip()
         if not ticket:
            errors['ticket'] = u"Номер білета є обов'язковим"
         else:
            data['ticket'] = ticket

         student_group = request.POST.get('student_group', '').strip()
         if not student_group:
            errors['student_group'] = u"Оберіть групу для студента"
         else:
            groups = Group.objects.filter(pk=student_group)
            if len(groups) != 1:
               errors['student_group'] = u"Оберіть коректну групу"
            else:
               data['student_group'] = groups[0]

         photo = request.FILES.get('photo')
         if photo:
            data['photo'] = photo

         if not errors:
            student = Student(**data)
            student.save()
            return HttpResponseRedirect( u'%s?status_message=Студента успішно додано!' % reverse('home'))

         else:
            return render(request, 'students/students_add.html', {'groups': Group.objects.all().order_by('title'),'errors': errors})

      elif request.POST.get('cancel_button') is not None:
         return HttpResponseRedirect( u'%s?status_message=Додавання студента  скасовано!' % reverse('home'))

   else:
      return render(request, 'students/students_add.html', {'groups': Group.objects.all().order_by('title')})

class StudentUpdateView(UpdateView):
    model = Student
    template_name = 'students/students_edit.html'
    fields = ['first_name', 'last_name', 'middle_name', 'birthday', 'ticket', 'student_group', 'photo', 'notes']

    def get_success_url(self):
        return u'%s?status_message=Студента успішно збережено!' \
            % reverse('home')

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            return HttpResponseRedirect(
                u'%s?status_message=Редагування студента відмінено!' %
                reverse('home'))
        else:
            return super(StudentUpdateView, self).post(request, *args, **kwargs)

def students_delete(request, sid):
   return HttpResponse('<h1>Student Delete %s</h1>' %sid)



