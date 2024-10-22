from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

import datetime
import os

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.events']

def create_event_and_send_invite(summary, start_time, end_time, attendees):
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)

    event = {
        'summary': summary,
        'start': {
            'dateTime': start_time.isoformat(),
            'timeZone': 'Your_Timezone',
        },
        'end': {
            'dateTime': end_time.isoformat(),
            'timeZone': 'Your_Timezone',
        },
        'attendees': [{'email': attendee} for attendee in attendees],
        'conferenceData': {
            'createRequest': {
                'requestId': f"{summary}-{start_time.isoformat()}",
                'conferenceSolutionKey': {'type': 'hangoutsMeet'}
            }
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 30},
            ],
        },
    }

    event = service.events().insert(calendarId='primary', body=event, 
                                    conferenceDataVersion=1, 
                                    sendUpdates='all').execute()
    return event['hangoutLink'], event['id']

# Example usage
summary = "Meeting with Client"
start_time = datetime.datetime(2024, 10, 18, 10, 0, 0)  # Year, month, day, hour, minute, second
end_time = datetime.datetime(2024, 10, 18, 11, 0, 0)
attendees = ['client@example.com', 'team@yourcompany.com']

meet_link, event_id = create_event_and_send_invite(summary, start_time, end_time, attendees)
print(f"Google Meet link: {meet_link}")
print(f"Event ID: {event_id}")