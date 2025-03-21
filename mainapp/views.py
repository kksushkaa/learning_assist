import json
import os
import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import HttpResponseRedirect, redirect, render
from openai import OpenAI
from django.contrib import messages

from mainapp.forms import TaskAddForm, TaskEditForm, UserLoginForm, UserRegForm
from mainapp.models import Task
from pytz import timezone


def index(request):
    if request.method == "GET":
        login_form = UserLoginForm()
        context = {"login_form": login_form}
        check_upcoming_tasks(request)
        return render(request, "mainapp/index.html", context)
    else:
        print("Вход")
        login_form = UserLoginForm(data=request.POST)
        # валидация
        if login_form.is_valid():
            # аутентификация проверка, что человек такое есть
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(username=username, password=password)
            if user:
                # авторизация создаем сессию
                login(request, user)
                print("вошел")
                return HttpResponseRedirect("/")
        context = {"login_form": login_form}
        return render(request, "mainapp/index.html", context)


def reg_view(request):
    if request.method == "GET":
        reg_form = UserRegForm()
        context = {"reg_form": reg_form}
        return render(request, "mainapp/reg.html", context)
    else:
        reg_form = UserRegForm(data=request.POST)
        if reg_form.is_valid():
            reg_form.save()
            return HttpResponseRedirect("/")
        print(reg_form.errors)
        context = {"reg_form": reg_form}
        return render(request, "mainapp/reg.html", context)


@login_required
def schedule_view(request):
    context = {"form_add": TaskAddForm(), "form_edit": TaskEditForm()}
    check_upcoming_tasks(request)
    return render(request, "mainapp/schedule.html", context)


@login_required
def todolist(request):
    tasks = Task.objects.filter(user=request.user).order_by("-status_id")
    # tasks = Task.objects.filter(status_id=2)
    context = {"tasks": tasks, "form_add": TaskAddForm(), "form_edit": TaskEditForm()}
    check_upcoming_tasks(request)
    return render(request, "mainapp/todolist.html", context)
    


def check_upcoming_tasks(request):
    if not request.user.is_authenticated:
        return

    now = datetime.datetime.now(tz=timezone('Europe/Moscow'))
    time_30_min = now + datetime.timedelta(minutes=30)
    ff = Task.objects.filter(start_time__gte=now, start_time__lte=time_30_min, user=request.user, status_id=2)
    # print(ff)
    for task in ff:
        # print(now)
        time_diff = task.start_time - now
        min_diff = int(time_diff.total_seconds() // 60)
        messages.info(request, message=f"Напоминаю! До вашей задачи {task.title} осталось {min_diff} минут.")



@login_required
def assist(request):
    check_upcoming_tasks(request)
    return render(request, "mainapp/assist.html")


@login_required
def quiz(request):
    check_upcoming_tasks(request)
    return render(request, "mainapp/quiz.html")


@login_required
def gpt_query_view(request):
    query_text = request.POST.get("gpt_query")
    print(f"Я спрашиваю у gpt {query_text}")
    client = OpenAI(api_key=os.getenv("GPT_TOKEN"))
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Ты помощник по учебе для школьников 1 - 11 класс. Твой ответ должен быть длиной максимум 1000 токенов.",
            },
            {"role": "user", "content": query_text},
        ],
    )

    a = completion.choices[0].message.content

    print(a)
    return JsonResponse({"message": a})


@login_required
def quiz_query_view(request):
    if request.method == "POST":
        query_text = request.POST.get("quiz_query")
        print(f"Викторина {query_text}")
        client = OpenAI(api_key=os.getenv("GPT_TOKEN"))
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": 'Ты помощник по учебе для школьников 1 - 11 класс.Составь тест из 7 вопросов с 4 вариантами ответа, где 1 правильный. Дай ответ в формате json. Ничего перед и после json не пиши. Формат словаря должен быть {"test":[{"question":"Вопрос1","options":["ответ1","ответ2","ответ3","ответ4"], "answer":"правильный ответ"}]}',
                },
                {"role": "user", "content": query_text},
            ],
        )

        a = completion.choices[0].message.content
        print(a)
        if "'" == a[0]:
            test_st = a[7:-3]
        else:
            test_st = a
        test_dic = json.loads(test_st)
        print(test_dic)
        num_lst = list(enumerate(test_dic["test"]))
        context = {"zag": query_text, "test": num_lst}
        request.session["test"] = num_lst
        request.session["zag"] = query_text
        return HttpResponseRedirect("/quiz/quiz_query")
    else:
        print(request.GET)
        context = {"zag": request.session["zag"], "test": request.session["test"]}
        return render(request, "mainapp/quiz_task.html", context)


@login_required
def add_task_view(request):
    print(request.POST)
    add_form = TaskAddForm(request.POST)
    if add_form.is_valid():
        task = add_form.save(commit=False)
        task.user = request.user
        task.status_id = 2
        task.save()
        return redirect(request.META.get("HTTP_REFERER", "/"))


@login_required
def edit_task_view(request):
    edit_form = TaskEditForm(request.POST)
    if edit_form.is_valid():
        task = edit_form.save(commit=False)
        task.id = request.POST.get("task_id")
        task.user = request.user
        task.save()
        return HttpResponseRedirect("/todolist")


@login_required
def get_task_info(request, task_id):
    task = Task.objects.get(id=task_id)
    task_dic = {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "status_id": task.status.id,
        "user_id": task.user.id,
        "start_time": task.start_time.astimezone(timezone("Europe/Moscow")).strftime("%Y-%m-%d %H:%M:%S"),
        "end_time": task.end_time,
        "duration": f"{int(task.duration.total_seconds() // 3600)}:{int(task.duration.total_seconds() % 3600 // 60)}",
    }
    return JsonResponse(task_dic)


@login_required
def delete_task(request, task_id):
    task = Task.objects.get(id=task_id)
    task_title = task.title
    task.delete()

    messages.warning(request, f"Задача {task_title} удалена!")
    return HttpResponseRedirect("/todolist")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")


@login_required
def get_all_users_tasks(request):
    user_tasks = Task.objects.filter(user=request.user)
    all_tasks = []
    for tasks in user_tasks:
        if not tasks.start_time or not tasks.duration:
            continue
        end = tasks.start_time + tasks.duration
        all_tasks.append(
            {
                "title": tasks.title,
                "start": tasks.start_time.isoformat(),
                "end": end.isoformat() if end else None,
            }
        )
        print(all_tasks)
        print(tasks.duration.seconds)
    return JsonResponse(all_tasks, safe=False)


@login_required
def check_answers(request):
    c = 0

    for i in range(7):
        user_ans = request.POST.get(f"q{i}")
        corr_ans = request.session["test"][i][1]["answer"]
        request.session["test"][i].append(user_ans)
        if user_ans == corr_ans:
            c += 1
    context = {"c": c, "test": request.session["test"]}
    return render(request, "mainapp/results.html", context)
