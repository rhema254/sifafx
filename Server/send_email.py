import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from decouple import config
# from config import DevConfig

def send_email(email, subject, body):
    try:
        # Load configuration
        sender = config('Sender_email')
        password = config('Server_pass')
        host = config('MAIL_SERVER')
        port = config('MAIL_PORT', default=587)  # Add this line

        print(f"Connecting to {host}:{port}")
        print(f"Sending from: {sender}")
        print(f"Sending to: {email}")

        # Set up the MIME
        message = MIMEMultipart()
        message['From'] = sender
        message['To'] = email
        message['Subject'] = subject

        # Attach the body with t    he message instance
        message.attach(MIMEText(body, 'plain'))

        # Create the server connection
        with smtplib.SMTP(host=host, port=port) as server:
            print("Connection established. Starting TLS...")
            server.starttls()  # Secure the connection
            print("TLS started. Attempting login...")
            server.login(sender, password)  # Login using your email and password
            print("Login successful. Sending email...")
            
            # Send the email
            server.send_message(message)

        print("Email sent successfully!")

    except Exception as e:
        print(f"Failed to send email. Error: {e}")
        if isinstance(e, smtplib.SMTPAuthenticationError):
            print("This appears to be an authentication error. Please check your email and password.")
        elif isinstance(e, smtplib.SMTPConnectError):
            print("This appears to be a connection error. Please check your SMTP server and port settings.")

# Test block to run the function when script is executed directly
# if __name__ == "__main__":
#     # Test with sample data
#     test_email = "rhematesh@gmail.com"
#     test_subject = "Test Email"
#     test_body = "This is a test email."

#     send_email(test_email, test_subject, test_body)