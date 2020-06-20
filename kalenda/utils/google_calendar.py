from __future__ import print_function
import requests
import datetime
import pickle
import os.path
from urllib.parse import urlencode
from django.core.exceptions import PermissionDenied
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

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
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if user.google_access_token:
        creds = pickle.load(user.google_access_token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        user.google_access_token = pickle.dumps(creds)
        user.save(update_fields=['google_access_token'])

    service = build('calendar', 'v3', credentials=creds)

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