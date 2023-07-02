from flask import Flask, redirect, render_template, url_for, session, request
from authlib.integrations.flask_client import OAuth
import json

app = Flask(__name__)

CLIENTID_SECRET_PATH = 'secret_key_And_ID_Path'

with open(CLIENTID_SECRET_PATH) as f:
    file = json.load(f)

app_config = {

    "OUTH2_CLIENT_ID" : file['web']['client_id'],
    "OUTH2_CLIENT_SECRET" : file['web']['client_secret'],
    "OUTH2_META_URL" : "https://accounts.google.com/.well-known/openid-configuration",
    "FLASK_SECRET" : 'Unique_Flask_Secret_Key',
    "FLASK_PORT" : 8000
}

app.secret_key = app_config['FLASK_SECRET']

oauth = OAuth(app)

oauth.register("myApp"
               , client_id = app_config['OUTH2_CLIENT_ID']
               , client_secret = app_config['OUTH2_CLIENT_SECRET']
               , server_metadata_url = app_config['OUTH2_META_URL']
               ,client_kwargs  = {"scope" : "openid profile email"}
               )

@app.route('/')
def home():
    return render_template('home.html', session = session.get('user'), pretty = json.dumps(session.get('user'), indent=4))

@app.route('/google-login')
def googleLogin():
    return oauth.myApp.authorize_redirect(redirect_uri = url_for("googleCallback", _external = True))

@app.route('/signin-google')
def googleCallback():
    token = oauth.myApp.authorize_access_token()
    session['user'] = token
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = app_config['FLASK_PORT'], debug = True)