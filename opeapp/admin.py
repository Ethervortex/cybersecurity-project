from django.contrib import admin
from .models import Student, Course

#admin.register(User)
admin.site.register(Student)
admin.site.register(Course)
