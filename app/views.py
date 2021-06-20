from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from datetime import datetime, timezone, timedelta
from django import template
from .models import (Dog,Visit)
from factory.faker import faker
import factory
import random

FAKER = faker.Faker()
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
    Dog.objects.all().delete()
    Visit.objects.all().delete()
    for i in range(365):
        try:
            Dog.objects.create(
                first_name=FAKER.first_name(),
                last_name=FAKER.last_name(),
            )
        except:
            print("Unique Constraint Failed")
    for i in range(365):
        start_date = today + timedelta(days=random.randint(1, 365))
        end_date = start_date + timedelta(days=random.randint(2, 365))
        try:
            Visit.objects.create(
                dog=Dog.objects.order_by('?')[0],
                start_date = start_date,
                end_date = end_date,
            )
        except:
            pass
    context = {}
    context['segment'] = 'index'

    html_template = loader.get_template( 'visits/populate-db.html' )
    return HttpResponse(html_template.render(context, request))