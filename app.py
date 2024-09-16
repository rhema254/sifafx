from flask import Flask, url_for, redirect, request, render_template, session, flash
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build


app = Flask(__name__)

@app.route('/')
def index():
    return "And we have Touchdown!!"





if __name__ == "__main__":
    app.run(
        debug=True
        )



