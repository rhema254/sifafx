from flask_restx import fields
from Server.exts import api

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
