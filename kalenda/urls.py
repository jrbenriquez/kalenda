from rest_framework.routers import DefaultRouter
from django.urls import path, include, re_path
from kalenda.views.calendars import calendars, manage_calendar, set_appointment

urlpatterns = [
    path('', calendars, name='calendars'),
    path('manage/<str:calendar_id>', manage_calendar, name='manage'),
    path('appointment/<str:calendar_id>', set_appointment, name='set_appointment')
]

app_name = 'kalenda'
