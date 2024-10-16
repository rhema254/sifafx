import smtplib 
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from decouple import config
from config import DevConfig


MAIL_SERVER = config('MAIL_SERVER')
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_USERNAME = config('MAIL_USERNAME')
MAIL_PASSWORD= config('MAIL_PASSWORD')


def send_email(email, subject, body):
    try:
        # Set up the MIME
        message = MIMEMultipart()
        message['From'] = MAIL_USERNAME
        message['To'] = email
        message['Subject'] = subject
        
        
        # Attach the body with the message instance
        message.attach(MIMEText(body, 'plain'))

        # Create the server connection
        server = smtplib.SMTP(host=MAIL_SERVER, port=MAIL_PORT)
        server.starttls()  # Secure the connection
        server.login(MAIL_USERNAME, MAIL_PASSWORD)  # Login using your email and password

        # Send the email
        server.sendmail(MAIL_USERNAME, email, message.as_string())

        # Close the server connection
        server.quit()

        print("Email sent successfully!")

    except Exception as e:
        print(f"Failed to send email. Error: {e}")
