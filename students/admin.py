from django.contrib import admin
from .models import Student
from .models import Group
from .models import Exam
# Register your models here.

admin.site.register(Student)
admin.site.register(Group)
admin.site.register(Exam)