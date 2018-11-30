from django.contrib import admin

# Register your models here.
from mainsite.models import Student, Course, Score, User

admin.site.register(Student)
admin.site.register(Course)
admin.site.register(Score)
admin.site.register(User)