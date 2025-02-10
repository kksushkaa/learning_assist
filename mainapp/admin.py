from django.contrib import admin
from mainapp.models import Status, Task, MyUser

# Register your models here.

admin.site.register(Status)
admin.site.register(Task)
admin.site.register(MyUser)
