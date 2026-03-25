from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
import datetime
from .forms.demo_form import DemoForm

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

def forms(request):
    template = loader.get_template('forms.html')
    context = {
        'demo_form': DemoForm(request.POST) if request.method == 'POST' else DemoForm()
    }
    return HttpResponse(template.render(context, request))
