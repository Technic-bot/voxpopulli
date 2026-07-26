import httpx
from flask import (
    Flask, redirect, request, session,
    Blueprint, current_app 
)
import pprint
import os

bp = Blueprint('oauth', __name__, url_prefix='/api')

@bp.route('/oauth')
def oauth():
    voxpop_uri = current_app.config.get('VOXPOPULLI_URI')
    params = {'response_type': 'code', 
        'client_id' : current_app.config['CLIENT_ID'],
        'redirect_uri': f'{voxpop_uri}/api/oauth/redirect',
        'scope': 'identity identity[email] identity.memberships' # campaigns campaigns.members campaigns.members[email] campaigns.members.address'
    }
    authorize_url = 'https://www.patreon.com/oauth2/authorize?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}'
    patreon_url = authorize_url.format(**params)
    return redirect(patreon_url)

@bp.route('/oauth/redirect')
def tokenize():
    code = request.args.get('code')
    token_url = "https://www.patreon.com/api/oauth2/token"
    voxpop_uri = current_app.config.get('VOXPOPULLI_URI')
    token_params = {
        'code': code,
        'grant_type': 'authorization_code',
        'client_id' : current_app.config['CLIENT_ID'],
        'client_secret' : current_app.config['CLIENT_SECRET'],
        'redirect_uri' : f'{voxpop_uri}/api/oauth/redirect',
        'scope' : 'identity,identity[email],identity.memberships'
    }
    headers = { 'Content-Type': 'application/x-www-form-urlencoded' }
    r = httpx.post(token_url, data=token_params, headers=headers)
    resp_dict = r.json()
    # pprint.pprint(resp_dict)

    access_token = resp_dict['access_token']
    refresh_token = resp_dict['refresh_token']
    expiry = resp_dict['expires_in']
    scope = resp_dict['scope']

    id_data = get_identity(access_token)
    # parse_id(id_data)

    return id_data

def get_identity(token):
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
    #pprint.pprint(response)
    return response

def parse_id(resp):
    first_name = response['data']['attributes']['first_name']
    email = response['data']['attributes']['email']
    includes = response['included']
    for include in includes:
        if include['type'] == 'member':
            id_number = include['relationships']['campaign']['data']['id']
            attrs = include['attributes']
            pledge_cents = attrs['currently_entitled_amount_cents']
            #print(f"Member of {id_number} with {pledge_cents}")

    # session['email'] = email
    # session['username'] = first_name

    return first_name

