# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime
from  django.views.generic import UpdateView, CreateView, DeleteView
from django.forms import ModelForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
from crispy_forms.bootstrap import FormActions

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


class StudentAddForm(ModelForm):
    class Meta():
        model = Student
        fields = ['first_name', 'last_name', 'middle_name', 'birthday', 'ticket', 'student_group', 'photo', 'notes']

    def __init__(self, *args, **kwargs):
        super(StudentAddForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()

        self.helper.form_action = reverse('students_add')
        self.helper.form_method ='POST'
        self.helper.form_class = 'form-horizontal'

        self.helper.help_text_inline = True
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-5'

        self.helper.layout = Layout(
            Fieldset('', 'first_name', 'last_name', 'middle_name', 'birthday', 'ticket', 'student_group', 'photo', 'notes'),
            ButtonHolder(
                Submit('save_button', u'Зберегти', css_class='btn btn-primary'),
                Submit('cancel_button', u'Скасувати', css_class='btn btn-link')))




class StudentAddView(CreateView):

   model = Student
   template_name = 'students/students_edit_add.html'
   form_class = StudentAddForm

   def get_context_data(self, **kwargs):
        context = super(StudentAddView, self).get_context_data(**kwargs)
        context['title'] = u'Додавання студента'
        return context

   def get_success_url(self):
        return u'%s?status_message=Студента успішно збережено!' % reverse('home')

   def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            return HttpResponseRedirect(u'%s?status_message=Додавання студента відмінено!' % reverse('home'))
        else:
            return super(StudentAddView, self).post(request, *args, **kwargs)


class StudentUpdateForm(ModelForm):
    class Meta():
        model = Student
        fields = ['first_name', 'last_name', 'middle_name', 'birthday', 'ticket', 'student_group', 'photo', 'notes']

    def __init__(self, *args, **kwargs):
        super(StudentUpdateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()

        self.helper.form_action = reverse('students_edit',kwargs={'pk': kwargs['instance'].id})
        self.helper.form_method ='POST'
        self.helper.form_class = 'form-horizontal'

        self.helper.help_text_inline = True
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-10'

        self.helper.layout = Layout(
            Fieldset('', 'first_name', 'last_name', 'middle_name', 'birthday', 'ticket', 'student_group', 'photo', 'notes'),
            ButtonHolder(
                Submit('save_button', u'Зберегти', css_class='btn btn-primary'),
                Submit('cancel_button', u'Скасувати', css_class='btn btn-link')))



class StudentUpdateView(UpdateView):
    model = Student
    template_name = 'students/students_edit_add.html'
    form_class = StudentUpdateForm

    def get_context_data(self, **kwargs):
        context = super(StudentUpdateView, self).get_context_data(**kwargs)
        context['title'] = u'Редагування студента'
        return context

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

class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'students/students_confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = super(StudentDeleteView, self).get_context_data(**kwargs)
        context['title'] = u"Видалити студента"
        return context

    def get_success_url(self):
        return u'%s?status_message=Студента успішно видалено!' % reverse('home')

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            return HttpResponseRedirect(  u'%s?status_message=Видаленя студента відмінено!' %
                reverse('home'))
        else:
            return super(StudentDeleteView, self).post(request, *args, **kwargs)


