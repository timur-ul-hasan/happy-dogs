from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse,JsonResponse
from datetime import datetime, timezone, timedelta
from django import template
from .models import (Dog,Visit)
from factory.faker import faker
import factory
import random
from django.db import connection
from django.core import serializers
from django.db.models import CharField,DateField, Value
import json


DAY_OF_WEEKS = {
    0 : "MONDAY",
    1 : "TUESDAY",
    2 : "WEDNESDAY",
    3 : "THURSDAY",
    4 : "FRIDAY",
    5 : "SATURDAY",
    6 :  "SUNDAY"
}


def visit_weeks():
    return {
        "MONDAY" : [],
        "TUESDAY" : [],
        "WEDNESDAY" : [],
        "THURSDAY" : [],
        "FRIDAY" : [],
        "SATURDAY" : [],
        "SUNDAY" : []        
    } 


def structure_visits_data():
    data = []
    minimum_date = Visit.objects.all().order_by('start_date').first()
    maximum_date = Visit.objects.all().order_by('-end_date').first()
    delta = maximum_date.end_date - minimum_date.start_date

    starting_day = minimum_date.start_date
    ending_day = maximum_date.end_date

    weekday_data = {}
    for i in range(delta.days):
        day = starting_day + timedelta(days=i)
        weekday = day.weekday()
        weekday_text = DAY_OF_WEEKS[weekday]
  
        current_date=Value(day, output_field=DateField())
        visits = list(Visit.objects.filter(start_date__lte=day,end_date__gte=day).annotate(day=current_date).values())

        if weekday == 0:
            weekday_data["MONDAY"] = visits
        if weekday == 3:
            weekday_data["TUESDAY"] = visits
        if weekday == 2:
            weekday_data["WEDNESDAY"] = visits
        if weekday == 3:
            weekday_data["THURSDAY"] = visits
        if weekday == 4:
            weekday_data["FRIDAY"] = visits
        if weekday == 5:
            weekday_data["SATURDAY"] = visits
        if weekday == 6:
            weekday_data["SUNDAY"] = visits
            for d in DAY_OF_WEEKS.values():
                if weekday_data.get(d,None) == None:
                    weekday_data[d] = []
            data.append(weekday_data)
            weekday_data = {}
    return data


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

    data = structure_visits_data()

    html_template = loader.get_template( 'visits/index.html' )
    return JsonResponse(data=data,safe=False)

def visit_page(request):
    context = {}
    data = structure_visits_data()
    context["data"] = data
    context['segment'] = 'index'


    html_template = loader.get_template( 'visits/index.html' )
    return HttpResponse(html_template.render(context, request))

def populate_db(request):
    cursor = connection.cursor()
    cursor.execute("PRAGMA foreign_keys = 0;")
    cursor.execute("DELETE FROM app_dog;")
    cursor.execute("DELETE FROM app_visit;")
    cursor.execute("VACUUM ;")
    cursor.execute("PRAGMA foreign_keys = 1;")

    today = datetime.now(tz=timezone.utc).replace(hour=00, minute=00, second=0, microsecond=0)
    
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