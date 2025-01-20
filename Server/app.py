from flask import Flask, render_template, request, redirect, url_for, session, jsonify, Blueprint
from Server.config import DevConfig
from decouple import config
from flask_restx import Resource, fields, Namespace
from Server.models import *
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from Server.exts import db, api, migrate
from flask_mail import Mail, Message
from Server.send_email import send_mail, reschedule_mail, cancel_mail
# import google.oauth2.credentials
# import google_auth_oauthlib.flow
# import googleapiclient.discovery
from datetime import datetime, timedelta
import os
from Server.admin import admin_blueprint
from Server.serializers import booking_model
from datetime import datetime


app = Flask(__name__)

api.init_app(app, version='1.0', title='SifaFX APIs', doc='/docs', contact='support@sifafx.com')
app.config.from_object(DevConfig)
CORS(app)
db.init_app(app)
migrate.init_app(app, db)
mail = Mail(app)

app.register_blueprint(admin_blueprint, url_prefix='/admin')

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# OAuth 2.0 Client IDs (Google Calendar API)
GOOGLE_CLIENT_SECRETS_FILE = "client_secrets.json"
SCOPES = ['https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/calendar.events']


@app.route('/', methods=['POST', 'GET'])
def index():

    return f'Welcome to Sifa FX '

def convert_to_12_hour(time_24):

    # time_obj = datetime.strptime(time_24, "%H:%M:%S")
    time_12 = time_24.strftime("%I:%M %p").lstrip("0")

    return time_12

def format_date(date_str):
      
    formatted_date = date_str.strftime("%B %d, %Y")

    return formatted_date


@api.route('/submit', methods=['GET', 'POST'])
class bookingsResource(Resource):
    

    @api.expect(booking_model)
    @api.marshal_with(booking_model)
    def post(self):

        """ To create a new booking """
        
        data = request.get_json()
        fullname=data['fullname']
        email=data['email']
        timezone = data['timezone']
        services=data['services']
        phone=data['phone']
        description=data['description']
        time = data['time']
        date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        
        print(time, date)

        new_booking = Booking(
            fullname=fullname,
            email=email,
            phone=phone,
            date=date,
            time=time,
            timezone=timezone,
            services=services,
            description=description,
           
        )
        new_booking.save()
        new_id = new_booking.id
        print(new_id)
        time_12 = convert_to_12_hour(new_booking.time)
        formatted_date = format_date(date)
        send_mail(fullname,email,formatted_date,time_12,new_id)
        print(new_booking)
        return new_booking, 201        
    

@api.route('/Reschedule/<int:id>', methods=['PATCH'])
class bookingResource(Resource):

    @api.expect(booking_model)
    @api.marshal_with(booking_model)
    def patch(self, id):
        """ To update a booking by id partially"""

        updated_booking = Booking.query.get_or_404(id)
        
        if (updated_booking.status != 'Cancelled'):
            data = api.payload
            print(data)
            
            for key, value in data.items():
                if hasattr(updated_booking, key):
                    setattr(updated_booking, key, value)

            updated_booking.update(**data)
            
            email = updated_booking.email
            fullname= updated_booking.fullname
            new_time = convert_to_12_hour(updated_booking.time)
            new_date = format_date(updated_booking.date)
            
            reschedule_mail(fullname, email, new_date, new_time, id)
        else:
            return {"message":"This appointment was cancelled. Please create a new appointment"}, 404


        return updated_booking, 200



@api.route('/Cancel/<int:id>', methods=['PUT'])
class bookingResource(Resource):

    @api.expect(booking_model)
    @api.marshal_with(booking_model)
    def put(self, id):
        """ Update the booking to cancelled """
        data = api.payload
        id = id
        booking_to_update = Booking.query.get_or_404(id)
        
        if not booking_to_update:
            return 404
        
        for key, value in data.items():
            if hasattr(booking_to_update, key):
                setattr(booking_to_update, key, value)
                        
        email = booking_to_update.email
        new_time = convert_to_12_hour(booking_to_update.time)
        new_date = format_date(booking_to_update.date)
        cancel_mail(email, new_date, new_time)


        return booking_to_update, 200
    



if __name__ == '__main__':
    with app.app_context():
        print('Creating database if they are absent')
        db.create_all()
        print('Database created or already exists')
        app.run(debug=True)
        