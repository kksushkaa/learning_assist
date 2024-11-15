from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from mainapp.models import Task
from mainapp.forms import TaskAddForm, TaskEditForm


def index(request):
    return render(request, "mainapp/index.html")


def schedule_view(request):
    return render(request, "mainapp/schedule.html")


def todolist(request):
    tasks = Task.objects.all()
    # tasks = Task.objects.filter(status_id=2)
    context = {"tasks": tasks, 'form_add': TaskAddForm(), 'form_edit': TaskEditForm()}
    return render(request, "mainapp/todolist.html", context)


def assist(request):
    answer_text = request.GET.get("gpt_answer")
    if answer_text:
        context = {"answer_text": answer_text}
    else:
        context = {"answer_text": ""}
    return render(request, "mainapp/assist.html", context)


def quiz(request):
    return render(request, "mainapp/quiz.html")


def gpt_query_view(request):
    query_text = request.GET.get("gpt_query")
    print(f"Я спрашиваю у gpt {query_text}")
    return HttpResponseRedirect("/assist?gpt_answer=я ответил.")

def quiz_query_view(request):
    query_text = request.GET.get("quiz_query")
    print(f"Викторина {query_text}")
    return HttpResponseRedirect("/quiz?quiz_answer=я сделал викторину.")

def add_task_view(request):
    print(request.POST)
    add_form = TaskAddForm(request.POST)
    if add_form.is_valid():
        add_form.save()
        return HttpResponseRedirect('/todolist')
    return HttpResponse("/assist?gpt_answer=я добавил задачу.")

def edit_task_view(request):
    return HttpResponse("/assist?gpt_answer=я добавил задачу.")

def get_task_info(request, task_id):
    task = Task.objects.get(id = task_id)
    task_dic = {
        "title": task.title,
        "description": task.description,
        "status_id": task.status.id,
        "user_id": task.user.id
    }
    return JsonResponse(task_dic)
    