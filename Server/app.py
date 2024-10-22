from flask import Flask, render_template, request, redirect, url_for, session, jsonify, Blueprint
from Server.config import DevConfig
from decouple import config
from flask_restx import Api, Resource, fields
from Server.models import *
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from Server.exts import db  
from flask_mail import Mail, Message
from Server.send_email import send_email
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
from datetime import datetime, timedelta
import os
from Server.admin import admin_blueprint

app = Flask(__name__)

api = Api(app, version='1.0', title='SifaFX APIs', doc='/docs')
app.config.from_object(DevConfig)
CORS(app)
db.init_app(app)
mail = Mail(app)

app.register_blueprint(admin_blueprint, url_prefix='/api/admin')

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
            "id": fields.Integer(required=True, description="Id"),
            "f_name": fields.String(required=True, description="First Name"),
            "l_name": fields.String(required=True, description="Last Name"),
            "email": fields.String(required=True, description="Booker's Email"), 
            "date": fields.Date(required=True, description="Session Date"),
            "time": fields.String(required=True, description="Session Time in Format: HH:MM"),
            "service": fields.String(required=True, description="Service Required"),
            "description": fields.String(max_length=200, required=True, description="Description of the problem"),
            "created_at": fields.DateTime(required=True, description="Booking Creation Date")

        }
)

@api.route('/submit', methods=['GET', 'POST'])
class bookingsResource(Resource):
    

    @api.expect(booking_model)
    @api.marshal_with(booking_model)
    def post(self):

        """ To create a new booking """
        
        data = request.get_json()
        f_name=data['f_name']
        l_name=data['l_name']
        email=data['email']
        timezone = data['timezone'],
        service=data['service'],
        description=data['description']
        time = data['time']
        date = data['date']
        meet = 'This is just a test'
        print(time, date)
        new_booking = Booking(
            f_name=f_name,
            l_name=data['l_name'],
            email=data['email'],
            date=date,
            time=time,
            timezone = data['timezone'],
            service=data['service'],
            description=data['description']
        )
        new_booking.save()
        subject = "Booking Confirmation"
        body = f"Hello {f_name} {l_name},<br/>Thank you for choosing our consulting services/n./n In your Booking Form, you indicated you'd like to have a session with us on {date} at {time}{timezone}. Please note that the timezone is the timezone that your browser detected! If you were using a vpn, kindly send a follow-up email to confirm this./n/n You can add this meeting to your calendar. Google meet Link:{meet}"
        send_email(email, subject, body)
        
        return new_booking, 201 
            

        
    


if __name__ == '__main__':
    with app.app_context():
        print('Creating database if they are absent')
        db.create_all()
        print('Database created or already exists')
        app.run(debug=True)
        