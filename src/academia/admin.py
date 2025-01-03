from django.contrib import admin
from .models import University, Faculty, Department, AcademicYear, Course, Division, Chapter, Topic, SubTopic, Element

# Register your models here.

admin.site.register(University)
admin.site.register(Faculty)
admin.site.register(Department)
admin.site.register(AcademicYear)
admin.site.register(Course)
admin.site.register(Division)
admin.site.register(Chapter)
admin.site.register(Topic)
admin.site.register(SubTopic)
admin.site.register(Element)