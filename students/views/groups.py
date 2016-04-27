# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse,  HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from  django.views.generic import UpdateView, CreateView, DeleteView
from django.forms import ModelForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
from ..models import Group

#Views for Groups

def groups_list(request):
   groups = Group.objects.all()

   order_by = request.GET.get('order_by', '')
   if order_by in ('title', 'leader'):
       groups = groups.order_by(order_by)
       if request.GET.get('reverse', '') == '1':
           groups = groups.reverse()

    #pagination students
   paginator = Paginator(groups, 3)
   page = request.GET.get('page')
   try:
      groups = paginator.page(page)
   except PageNotAnInteger:
      # IF page NOT an integer
      groups = paginator.page(1)
   except EmptyPage:
      # IF page number of range
      groups = paginator.page(paginator.num_pages)

   return render(request, 'students/groups_list.html',{'groups': groups})

class GroupsAddForm(ModelForm):
   class Meta:
      model = Group
      fields = ['title', 'leader', 'notes']

   def __init__(self, *args, **kwargs):
      super(GroupsAddForm, self).__init__(*args, **kwargs)

      self.helper = FormHelper()

      self.helper.form_action = reverse('groups_add')
      self.helper._form_method = 'POST'
      self.helper._form_class = 'form-horizontal'

      self.helper.help_text_inline = True
      self.helper.label_class = 'col-sm-2 control-label'
      self.helper.field_class = 'col-sm-5'

      self.helper.layout = Layout(
         Fieldset('', 'title', 'leader', 'notes'),
         ButtonHolder(
             Submit('save_button', u'Зберегти', css_class='btn btn-primary'),
                Submit('cancel_button', u'Скасувати', css_class='btn btn-link')))


class GroupsAddView(CreateView):

   model = Group
   template_name = 'students/students_edit_add.html'
   form_class = GroupsAddForm

   def get_context_data(self, **kwargs):

      context = super(GroupsAddView, self).get_context_data(**kwargs)
      context['title'] = u'Додати групу'
      return context

   def get_success_url(self):
      return u'%s?status_message=Групу успішно збережено!' % reverse('groups')

   def post(self, request, *args, **kwargs):
      if request.POST.get('cancel_button'):
         return HttpResponseRedirect(u'%s?status_message=Додавання групи відмінено!' % reverse('groups'))
      else:
         return super(GroupsAddView, self).post(request, *args, **kwargs)


class GroupsUpdateForm(ModelForm):
   class Meta:
      model = Group
      fields = ['title', 'leader', 'notes']

   def __init__(self, *args, **kwargs):
      super(GroupsUpdateForm, self).__init__(*args, **kwargs)

      self.helper = FormHelper()

      self.helper.form_action = reverse('groups_edit',kwargs={'pk': kwargs['instance'].id})
      self.helper._form_method = 'POST'
      self.helper._form_class = 'form-horizontal'

      self.helper.help_text_inline = True
      self.helper.label_class = 'col-sm-2 control-label'
      self.helper.field_class = 'col-sm-5'

      self.helper.layout = Layout(
         Fieldset('', 'title', 'leader', 'notes'),
         ButtonHolder(
             Submit('save_button', u'Зберегти', css_class='btn btn-primary'),
                Submit('cancel_button', u'Скасувати', css_class='btn btn-link')))



class GroupsUpdateView(UpdateView):

   model = Group
   template_name = 'students/students_edit_add.html'
   form_class = GroupsUpdateForm


   def get_context_data(self, **kwargs):

      context = super(GroupsUpdateView, self).get_context_data(**kwargs)
      context['title'] = u'Редагувати групу'
      return context

   def get_success_url(self):
      return u'%s?status_message=Зміни успішно збережені!' % reverse('groups')

   def post(self, request, *args, **kwargs):
      if request.POST.get('cancel_button'):
         return HttpResponseRedirect(u'%s?status_message=Редагування групи відмінено!' % reverse('groups'))
      else:
         return super(GroupsUpdateView, self).post(request, *args, **kwargs)


class GroupsDeleteView(DeleteView):
   model = Group
   template_name = 'students/groups_confirm_delete.html'

   def get_context_data(self, **kwargs):
      context = super(GroupsDeleteView, self).get_context_data(**kwargs)
      context['title'] = u'Видалити групу'
      return context

   def get_success_url(self):
      return u'%s?status_message=Групу успішно видалено!' % reverse('groups')

   def post(self, request, *args, **kwargs):
      if request.POST.get('cancel_button'):
         return HttpResponseRedirect(u'%s?status_message=Видаленя групи відмінено!' % reverse('groups'))
      else:
         return super(GroupsDeleteView, self).post(request, *args, **kwargs)




