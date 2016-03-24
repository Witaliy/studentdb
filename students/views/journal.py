# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse

#Views for Students

def students_list(request):
	m = range(0,31)
	students = (
		{'id':1,
		 'name': u'Віталій Статкевич',
		 'month': m },
		{'id':2,
		 'name': u'Акакій Бипка',
		 'month': m },
		{'id':3,
		 'name': u'Васілєвс Корчман',
		 'month': m },
		)
	return render(request, 'students/journal.html', {'students': students})
