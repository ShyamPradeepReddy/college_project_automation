from django.contrib import admin
from .models import User,BookRequest,Book,Attendance
admin.site.register(User)
admin.site.register(Book)
admin.site.register(BookRequest)
admin.site.register(Attendance)

