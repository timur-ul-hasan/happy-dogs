from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from datetime import datetime, timezone, timedelta
from django import template
from .models import (Dog,Visit)


@login_required(login_url="/login/")
def index(request):
    
    context = {}
    context['segment'] = 'index'

    html_template = loader.get_template( 'index.html' )
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:
        
        load_template      = request.path.split('/')[-1]
        context['segment'] = load_template
        
        html_template = loader.get_template( load_template )
        return HttpResponse(html_template.render(context, request))
        
    except template.TemplateDoesNotExist:

        html_template = loader.get_template( 'page-404.html' )
        return HttpResponse(html_template.render(context, request))

    except:
    
        html_template = loader.get_template( 'page-500.html' )
        return HttpResponse(html_template.render(context, request))

def visits(request):
    context = {}
    context['segment'] = 'index'

    html_template = loader.get_template( 'visits/index.html' )
    return HttpResponse(html_template.render(context, request))


def populate_db(request):
    today = datetime.now(tz=timezone.utc).replace(hour=00, minute=00, second=0, microsecond=0)
    for i in range(365):
        Dog.create()



    for i in range(365):


        print(i)

    context = {}
    context['segment'] = 'index'

    html_template = loader.get_template( 'visits/index.html' )
    return HttpResponse(html_template.render(context, request))