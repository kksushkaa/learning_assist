"""
URL configuration for learning_assist project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from mainapp.views import (
    index,
    schedule_view,
    todolist,
    assist,
    quiz,
    gpt_query_view,
    add_task_view,
    get_task_info,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", index),
    path("schedule", schedule_view),
    path("todolist", todolist),
    path("assist/gpt_query", gpt_query_view),
    path("assist", assist),
    path("quiz", quiz),
    path("todolist/add_task_view", add_task_view),
    path("get_task_info/<int:task_id>", get_task_info),  # get_task_info/1
]
