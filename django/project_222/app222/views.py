from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
import datetime


def hello(request):
    return HttpResponse("Hello, World!")


def home(request):
    template = loader.get_template('home.html')
    return HttpResponse(template.render())


def transfer(request):
    template = loader.get_template('transfer.html')

    now = datetime.datetime.now()

    context = {
        'x': 10,
        'str': 'The string',
        'now': now
    }

    return HttpResponse(template.render(context, request))

def static_page(request):
    template = loader.get_template('static.html')
    return HttpResponse(template.render({}, request))

'''
Д.З. Створити сторінку з інструкцією встановлення і налаштування 
статичних файлів. Помістити на сторінку кілька ресурсів різного 
типу: зображення, PDF-посилання, аудіо та/чи відеофайл
'''