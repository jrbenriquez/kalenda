from datetime import datetime

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from kalenda.utils.google_calendar import get_google_calendar_events, get_google_calendars
from kalenda.views.decorators import attach_google_token
# Create your views here.


@login_required
@attach_google_token
def calendars(request):
    print(request.google_token)
    data = get_google_calendars(request.google_token)
    print(data)
    calendars_data = data['items']

    context = {}
    calendar_list = []
    for calendar in calendars_data:
        if 'summaryOverride' in calendar:
            display_text = calendar['summaryOverride']
        else:
            display_text = calendar['summary']
        calendar_list.append({
            "id": calendar['id'],
            "color": calendar['backgroundColor'],
            "displayText": display_text
            })
    context['calendars'] = calendar_list
    return render(request, 'kalenda/calendars.html', context=context)


@login_required
@attach_google_token
def manage_calendar(request, calendar_id):
    # Get only events for current month
    time_min = datetime.utcnow().replace(day=1,hour=0, minute=0,  second=0, microsecond=0).isoformat() +'Z'
    query_params = {'maxResults': 5, 'timeMin': time_min}
    data = get_google_calendar_events(calendar_id, request.google_token, query_params)
    print(data)
    context = {"events": data['items']}
    context['calendar_id'] = calendar_id
    print(len(data['items']))
    return render(request, 'kalenda/events.html', context=context)


@login_required
@attach_google_token
def set_appointment(request, calendar_id):
    # Get only events for current month
    context = {'calendar_id': calendar_id}
    return render(request, 'kalenda/appointment_calendar.html', context=context)


@login_required
@attach_google_token
def set_time(request, calendar_id, datestring):
    # Get only events for current month
    context = {'calendar_id': calendar_id}
    return render(request, 'kalenda/available_time.html', context=context)