# # from calendar_api.calendar_api import google_calendar_api
# # m=google_calendar_api()
# # m.create_event(calendar_id='csg-506@stalwart-coast-252914.iam.gserviceaccount.com',
# # start='2019-09-28T09:00:00-07:00',
# # end='2019-09-28T09:00:00-07:00',
# # desc='foo'
# # )
# import googleapiclient
# calendar = service.calendars().get(calendarId='csg-506@stalwart-coast-252914.iam.gserviceaccount.com').execute()

# print(calendar['summary'])

from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='iuscompsec@gmail.com', timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])
    event = {
    'summary': 'CSG Email Testing',
    'location': 'CSG LAB 111/115',
    'description': 'Testing Emails and Automated Reminders',
    'start': {
        'dateTime': '2019-09-28T11:50:00-04:00',
        'timeZone': 'America/Kentucky/Louisville',
    },
    'end': {
        'dateTime': '2019-09-28T11:55x:00-04:00',
        'timeZone': 'America/Kentucky/Louisville',
    },
    'recurrence': [
        'RRULE:FREQ=DAILY;COUNT=1'
    ],
    'attendees': [
        {'email': 'zbouvier@iu.edu'},
    ],
    'reminders': {
        'useDefault': False,
        'overrides': [
        {'method': 'email', 'minutes': 40320 },
        {'method': 'email', 'minutes': 20160 },
        {'method': 'email', 'minutes': 1440 },
        {'method': 'email', 'minutes': 1 },
        {'method': 'popup', 'minutes': 10},
        ],
    },
    }

    event = service.events().insert(calendarId='iuscompsec@gmail.com', body=event).execute()
    print('Event created: %s' % (event.get('htmlLink')))
if __name__ == '__main__':
    main()