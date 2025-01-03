# # from google.oauth2.credentials import Credentials
# # from google_auth_oauthlib.flow import Flow
# # from googleapiclient.discovery import build
# # from google.auth.transport.requests import Request

# # # Handling Google Calendar Authorization

# # def authorize_google():








# # Route to handle Google Calendar authorization
# @app.route('/authorize_google')
# def authorize_google():
#     flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
#         GOOGLE_CLIENT_SECRETS_FILE, scopes=SCOPES)
    
#     flow.redirect_uri = url_for('callback', _external=True)
    
#     authorization_url, state = flow.authorization_url(
#         access_type='offline', include_granted_scopes='true')
    
#     session['state'] = state
    
#     print(authorization_url)
#     return redirect(authorization_url)


# @app.route('/callback')
# def callback():
#     state = session['state']
    
#     flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
#         GOOGLE_CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
#     flow.redirect_uri = url_for('callback', _external=True)

#     authorization_response = request.url
#     flow.fetch_token(authorization_response=authorization_response)

#     credentials = flow.credentials
#     session['credentials'] = credentials_to_dict(credentials)
#     print(credentials)
#     return redirect(url_for('callback'))

# # Route to book a session
# @app.route('/book_session', methods=['POST', 'GET'])
# def book_session():

#     session_name = request.form.get('session_name')
#     session_time = request.form.get('session_time')

#     if session_name and session_time is not None:
#         print(session_time, session_name)


#             # Assuming user is already authenticated
#     credentials = google.oauth2.credentials.Credentials(**session['credentials'])
#     service = googleapiclient.discovery.build('calendar', 'v3', credentials=credentials)

#     print()
#     # Create an event
#     event = {
#         'summary': session_name,
#         'location':'Online',
#         'description':'Testing One TWO WORK!!',
#         'start': {
#             'dateTime': session_time + '+00:00',
#             'timeZone': 'America/Los_Angeles',
#         },
#         'end': {
#             'dateTime': (datetime.strptime(session_time, '%Y-%m-%dT%H:%M') + timedelta(hours=1)).isoformat()+'+00:00',
#             'timeZone': 'America/Los_Angeles',
#         },
#         "attendees": [
#             {"email": "karhem254@gmail.com"}
#         ],
#         'reminders': {
#             'useDefault': False,
#             'overrides': [
#                 {'method': 'email', 'minutes': 2},
#                 {'method': 'popup', 'minutes': 2},
#             ],
#         },
#     }
#     print(event)
#     event = service.events().insert(calendarId='primary', body=event).execute()
#     print ('Event created: %s' % (event.get('htmlLink')))
    
#     return redirect(url_for('success', event_id=event.get('id')))
    


# # Success page after session booking
# @app.route('/success/<event_id>')
# def success(event_id):
#     return f"Session booked! Event ID: {event_id}"

# # Utility function to convert credentials to a dictionary
# def credentials_to_dict(credentials):
#     return {
#         'token': credentials.token,
#         'refresh_token': credentials.refresh_token,
#         'token_uri': credentials.token_uri,
#         'client_id': credentials.client_id,
#         'client_secret': credentials.client_secret,
#         'scopes': credentials.scopes
#     }

# # 