from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse, JsonResponse
from datetime import datetime, timezone, timedelta
from django import template
from .models import (Dog, Visit)
from factory.faker import faker
import factory
import random
from django.db import connection
from django.core import serializers
from django.db.models import CharField, DateField, Value
from dateutil.parser import parse
import json


DAY_OF_WEEKS = {
    0: "MONDAY",
    1: "TUESDAY",
    2: "WEDNESDAY",
    3: "THURSDAY",
    4: "FRIDAY",
    5: "SATURDAY",
    6:  "SUNDAY"
}


def visit_weeks():
    return {
        "MONDAY": [],
        "TUESDAY": [],
        "WEDNESDAY": [],
        "THURSDAY": [],
        "FRIDAY": [],
        "SATURDAY": [],
        "SUNDAY": []
    }


def structure_visits_data(start_date=None,end_date=None):
    data = []
    minimum_date =  Visit.objects.all().order_by('start_date').first()
    maximum_date = Visit.objects.all().order_by('-end_date').first()

    starting_day = minimum_date.start_date
    ending_day = maximum_date.end_date

    if start_date:
        starting_day = start_date
    if end_date:
        ending_day = end_date

    if not minimum_date or not maximum_date:
        return []

    delta = ending_day - starting_day

    weekday_data = {}
    for i in range(delta.days):
        day = starting_day + timedelta(days=i)
        weekday = day.weekday()
        weekday_text = DAY_OF_WEEKS[weekday]

        current_date = Value(day, output_field=DateField())
        visits = list(Visit.objects.filter(start_date__lte=day,
                      end_date__gte=day).annotate(day=current_date).values())
        if weekday == 0:
            weekday_data["MONDAY"] = { "day" : day  , "data" :  visits }
        if weekday == 3:
            weekday_data["TUESDAY"] = { "day" : day  , "data" :  visits }
        if weekday == 2:
            weekday_data["WEDNESDAY"] = { "day" : day  , "data" :  visits }
        if weekday == 3:
            weekday_data["THURSDAY"] = { "day" : day  , "data" :  visits }
        if weekday == 4:
            weekday_data["FRIDAY"] = { "day" : day  , "data" :  visits }
        if weekday == 5:
            weekday_data["SATURDAY"] = { "day" : day  , "data" :  visits }
        if weekday == 6:
            weekday_data["SUNDAY"] = { "day" : day  , "data" :  visits }
            weekdays_list = DAY_OF_WEEKS.values()
            count = 0
            for d in weekdays_list:
                if weekday_data.get(d, None) == None:
                    weekday_data[d] = { "day" : day - timedelta(days = (6 - count)) , "data" :  [] }
                count = count+1
            data.append(weekday_data)
            weekday_data = {}
    return data


FAKER = faker.Faker()


@login_required(login_url="/login/")
def index(request):
    context = {}
    context['segment'] = 'index'

    html_template = loader.get_template('index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]
        context['segment'] = load_template

        html_template = loader.get_template(load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:

        html_template = loader.get_template('page-500.html')
        return HttpResponse(html_template.render(context, request))


def visits(request):
    context = {}
    context['segment'] = 'index'

    data = structure_visits_data()

    html_template = loader.get_template('visits/index.html')
    return JsonResponse(data=data, safe=False)


def visit_page(request):
    context = {}
    start_date = request.GET.get('start_date',None)
    end_date = request.GET.get('end_date',None) 


    # minimum_date = Visit.objects.all().order_by('start_date').first()
    # maximum_date = Visit.objects.all().order_by('-end_date').first()

    start_date = parse(start_date) if start_date else None
    end_date = parse(end_date) if end_date else None

    data = structure_visits_data(start_date=start_date,end_date=end_date )
    context["data"] = data
    context['segment'] = 'index'

    html_template = loader.get_template('visits/index.html')
    return HttpResponse(html_template.render(context, request))


def populate_db(request):
    cursor = connection.cursor()
    cursor.execute("PRAGMA foreign_keys = 0;")
    cursor.execute("DELETE FROM app_dog;")
    cursor.execute("DELETE FROM app_visit;")
    cursor.execute("VACUUM ;")
    cursor.execute("PRAGMA foreign_keys = 1;")

    today = datetime.now(tz=timezone.utc).replace(
        hour=00, minute=00, second=0, microsecond=0)

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
                start_date=start_date,
                end_date=end_date,
            )
        except:
            pass
    context = {}
    context['segment'] = 'index'

    html_template = loader.get_template('visits/populate-db.html')
    return HttpResponse(html_template.render(context, request))
