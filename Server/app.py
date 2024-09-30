from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
from datetime import datetime, timedelta
from Server.config import DevConfig
from decouple import config
from flask_restx import Api, Resource, fields
from Server.models import *
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from Server.exts import db


app = Flask(__name__)

api = Api(app, version='1.0', title='SifaFX APIs', doc='/docs')
app.config.from_object(DevConfig)
CORS(app)
db.init_app(app)


import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# OAuth 2.0 Client IDs (Google Calendar API)
GOOGLE_CLIENT_SECRETS_FILE = "client_secrets.json"
SCOPES = ['https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/calendar.events']


@app.route('/', methods=['POST', 'GET'])
def index():

    return 'Welcome to Sifa FX '


#serializer_model:
booking_model = api.model(
    'Booking',
    {
        "id": fields.Integer(required=True),
        "f_name": fields.String(required=True),
        "l_name": fields.String(required=True),
        "email": fields.String(required=True), 
        "date_time": fields.DateTime(required=True),
        "service": fields.String(required=True),
        "description": fields.String(max_length=200, required=True),
        "created_at": fields.DateTime(required=True)

    }
)

@api.route('/submit', methods=['GET', 'POST'])
class bookingsResource(Resource):
    
    @api.marshal_list_with(booking_model)
    def get(self):
        """ To get all bookings """

        bookings_list = Booking.query.all()
        return bookings_list, 200
    

    @api.expect(booking_model)
    @api.marshal_with(booking_model)
    def post(self):

        """ To create a new booking """
        
        data = request.get_json()
        date_time_obj = datetime.strptime(data['date_time'], '%Y-%m-%dT%H:%M')
        print(date_time_obj)
        new_booking = Booking(
            f_name=data['f_name'],
            l_name=data['l_name'],
            email=data['email'],
            date_time=date_time_obj,
            service=data['service'],
            description=data['description']
            )
        new_booking.save()
        return new_booking, 201
            


@api.route('/submit/<int:id>', methods=['GET', 'UPDATE', 'POST'])    
class bookingResource(Resource):

    @api.marshal_with(booking_model)
    def get(self, id):
        """ To get a booking by id """

        booking = Booking.query.get_or_404(id)
        return booking, 200

    @api.expect(booking_model)
    @api.marshal_with(booking_model)
    def put(self, id):
        """ To update a booking by id """

        updated_booking = Booking.query.get_or_404(id)
        data = api.payload
        updated_booking.update(**data)
        return updated_booking, 200

    def delete(self, id):
        """ To delete a booking by id """

        booking = Booking.query.get_or_404(id)
        booking.delete()
        return booking, 204

        


    



# Route to handle Google Calendar authorization
@app.route('/authorize_google')
def authorize_google():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        GOOGLE_CLIENT_SECRETS_FILE, scopes=SCOPES)
    
    flow.redirect_uri = url_for('callback', _external=True)
    
    authorization_url, state = flow.authorization_url(
        access_type='offline', include_granted_scopes='true')
    
    session['state'] = state
    
    print(authorization_url)
    return redirect(authorization_url)


@app.route('/callback')
def callback():
    state = session['state']
    
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        GOOGLE_CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
    flow.redirect_uri = url_for('callback', _external=True)

    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials
    session['credentials'] = credentials_to_dict(credentials)
    print(credentials)
    return redirect(url_for('callback'))

# Route to book a session
@app.route('/book_session', methods=['POST', 'GET'])
def book_session():

    session_name = request.form.get('session_name')
    session_time = request.form.get('session_time')

    if session_name and session_time is not None:
        print(session_time, session_name)


            # Assuming user is already authenticated
    credentials = google.oauth2.credentials.Credentials(**session['credentials'])
    service = googleapiclient.discovery.build('calendar', 'v3', credentials=credentials)

    print()
    # Create an event
    event = {
        'summary': session_name,
        'location':'Online',
        'description':'Testing One TWO WORK!!',
        'start': {
            'dateTime': session_time + '+00:00',
            'timeZone': 'America/Los_Angeles',
        },
        'end': {
            'dateTime': (datetime.strptime(session_time, '%Y-%m-%dT%H:%M') + timedelta(hours=1)).isoformat()+'+00:00',
            'timeZone': 'America/Los_Angeles',
        },
        "attendees": [
            {"email": "karhem254@gmail.com"}
        ],
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 2},
                {'method': 'popup', 'minutes': 2},
            ],
        },
    }
    print(event)
    event = service.events().insert(calendarId='primary', body=event).execute()
    print ('Event created: %s' % (event.get('htmlLink')))
    
    return redirect(url_for('success', event_id=event.get('id')))
    


# Success page after session booking
@app.route('/success/<event_id>')
def success(event_id):
    return f"Session booked! Event ID: {event_id}"

# Utility function to convert credentials to a dictionary
def credentials_to_dict(credentials):
    return {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }




if __name__ == '__main__':
    with app.app_context():
        print('Creating database if they are absent')
        db.create_all()
        print('Database created or already exists')
        app.run(debug=True)
        