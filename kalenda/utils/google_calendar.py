from __future__ import print_function
import requests
import datetime
import pickle
import os.path
from django.conf import settings
from urllib.parse import urlencode
from django.core.exceptions import PermissionDenied
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from .google_token import create_google_service

SCOPES = settings.SOCIALACCOUNT_PROVIDERS['google']['SCOPE']

URL_BASE = 'https://www.googleapis.com/calendar/v3'


def get_google_calendar_events(calendar_id, access_token, query_params):
    ENDPOINT = '/calendars/{}/events/'.format(calendar_id)

    url = URL_BASE + ENDPOINT

    if query_params:
        url = url + '?' + urlencode(query_params)

    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }

    r = requests.get(url, headers=headers)
    data = r.json()
    if r.status_code != 200:
        raise PermissionDenied

    return data


def get_google_calendars(access_token):
    ENDPOINT = '/users/me/calendarList'

    url = URL_BASE + ENDPOINT

    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }

    r = requests.get(url, headers=headers)
    data = r.json()

    if r.status_code != 200:
        raise PermissionDenied

    return data


def get_gcal_events(user):
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    service = create_google_service(user)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])


def create_event(user, event_data):
    service = create_google_service(user)

    event = {
        'summary': 'Google I/O 2015',
        'location': '800 Howard St., San Francisco, CA 94103',
        'description': 'A chance to hear more about Google\'s developer products.',
        'start': {
            'dateTime': '2020-07-02T09:00:00-07:00',
            'timeZone': 'America/Los_Angeles',
        },
        'end': {
            'dateTime': '2020-07-02T17:00:00-07:00',
            'timeZone': 'America/Los_Angeles',
        },
        'recurrence': [
            'RRULE:FREQ=DAILY;COUNT=2'
        ],
        'attendees': [
            {'email': 'lpage@example.com'},
            {'email': 'sbrin@example.com'},
        ],
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
            ],
        },
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    print('Event created: %s' % (event.get('htmlLink')))



