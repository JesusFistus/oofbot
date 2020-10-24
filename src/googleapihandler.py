import os.path
import pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import datetime

# TODO: rewrite

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def get_entries(limit=3):
    """ Fetches upcoming calendar entries

    Parameters
    ----------
    limit:  The maximum amount of calendar entries fetched per calendar

    Returns
    -------
    A flattened list of calendar entries
    """
    creds = None

    if os.path.exists('data/google/token.pickle'):
        with open('data/google/token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'data/google/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open('data/google/token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    calendars_result = service.calendarList().list().execute()
    entries = []

    for calendar_info in calendars_result['items']:
        calendar = service.events().list(calendarId=calendar_info['id'], timeMin=now,
                                         maxResults=limit,
                                         singleEvents=True,
                                         orderBy='startTime').execute()

        for entry in calendar['items']:
            if 'backgroundColor' in calendar_info:
                entry['calendarColorId'] = calendar_info['backgroundColor']
            entries.append(entry)

    return entries
