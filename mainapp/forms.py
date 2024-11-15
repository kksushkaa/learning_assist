from django.forms import ModelForm
from mainapp.models import Task


class TaskAddForm(ModelForm):
    # настройка формы
    class Meta:
        model = Task
        fields = ['title','description','status','start_time', 'end_time', 'duration', 'user']

class TaskEditForm(ModelForm):
    # настройка формы
    class Meta:
        model = Task
        fields = ['title','description','status','start_time', 'end_time', 'duration', 'user']