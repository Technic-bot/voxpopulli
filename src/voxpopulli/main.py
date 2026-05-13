import httpx
from flask import Flask, redirect, request, session

import pprint
import os

app = Flask(__name__)

class Config:
    CLIENT_ID = os.environ.get("patreon_client_id")
    CLIENT_SECRET = os.environ.get("patreon_client_secret")
    CLIENT_TOKEN = os.environ.get("client_token")

app.config.from_object(Config)

app.secret_key = 'BAD_SECRET_KEY'

@app.route('/oauth')
def oauth():
    params = {'response_type': 'code', 
        'client_id' : app.config['CLIENT_ID'],
        'redirect_uri': 'http://127.0.0.1:5000/oauth/redirect'}
    authorize_url = 'https://www.patreon.com/oauth2/authorize?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}'
    patreon_url = authorize_url.format(**params)
    return redirect(patreon_url)

@app.route('/oauth/redirect')
def tokenize():
    code = request.args.get('code')
    token_url = "https://www.patreon.com/api/oauth2/token"
    token_params = {
        'code': code,
        'grant_type': 'authorization_code',
        'client_id' : app.config['CLIENT_ID'],
        'client_secret' : app.config['CLIENT_SECRET'],
        'redirect_uri' : 'http://127.0.0.1:5000/oauth/redirect',
        'scope' : 'identity,identity[email],identity.memberships'
    }
    headers = { 'Content-Type': 'application/x-www-form-urlencoded' }
    print(f"Got code {code}")
    r = httpx.post(token_url, data=token_params, headers=headers)
    resp_dict = r.json()
    pprint.pprint(resp_dict)
    access_token = resp_dict['access_token']
    refresh_token = resp_dict['refresh_token']
    expiry = resp_dict['expires_in']
    scope = resp_dict['scope']

    return f"Authenticated with {access_token}"

@app.route('/identity') 
def get_identity():
    token = app.config['CLIENT_TOKEN']
    base_url = "https://www.patreon.com/api/oauth2/v2/"
    identity_url = base_url + "identity"
    headers = { 'Authorization': f'Bearer {token}'}
    req = { 
        'fields[user]' : 'email,first_name,full_name,last_name',
        'include': 'memberships,memberships.campaign',
        'fields[member]': 'patron_status,currently_entitled_amount_cents'
    }
    r = httpx.get(identity_url, headers=headers, params=req)
    response = r.json()
    pprint.pprint(response)
    first_name = response['data']['attributes']['first_name']
    email = response['data']['attributes']['email']
    includes = response['included']
    for include in includes:
        if include['type'] == 'member':
            id_number = include['relationships']['campaign']['data']['id']
            attrs = include['attributes']
            pledge_cents = attrs['currently_entitled_amount_cents']
            print(f"Member of {id_number} with {pledge_cents}")

    session['email'] = email
    session['username'] = first_name

    return f"You are {first_name} of email {email}"

