#!/usr/bin/env python
# coding: utf-8

# In[1]:


import base64
import requests
from datetime import datetime, timedelta
from urllib.parse import urlencode


# In[2]:


client_id = 'ca305d1bc7e64485b99c494669317577'
client_secret = 'e00556e638e84fd99da29d554ae66778'


# In[3]:


class SpotifyAPI:
    access_token = None
    access_token_expires = datetime.now()
    access_token_expired = True
    client_id = None
    client_secret = None
    token_url = 'https://accounts.spotify.com/api/token'
    
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
    
    def get_client_credentials(self):
        '''
        Returns a base64 encoded string
        '''
        client_id = self.client_id
        client_secret = self.client_secret
        
        if client_id == None or client_secret == None:
            raise Exception('You must set client_id and client_secret.')

        client_creds = f'{client_id}:{client_secret}'
        client_creds_b64 = base64.b64encode(client_creds.encode())
        return client_creds_b64.decode()
    
    def get_token_headers(self):
        return {'Authorization': f'Basic {self.get_client_credentials()}'}
    
    def get_token_data(self):
        return {'grant_type': 'client_credentials'}
    
    def auth(self):
        r = requests.post(self.token_url, data=self.get_token_data(), headers=self.get_token_headers())
        if r.status_code not in range(200, 300):
            return Exception('Could not authenticate client.')
        data = r.json()
        now = datetime.now()
        access_token = data['access_token']
        expires_in = data['expires_in']  # seconds
        expires = now + timedelta(seconds=expires_in)
        self.access_token = access_token
        self.access_token_expires = expires
        self.access_token_expired = expires < now
        return True
    
    def get_access_token(self):
        token = self.access_token
        expires = self.access_token_expires
        now = datetime.now()
        if expires < now:
            self.auth()
            return self.get_access_token()
        elif token == None:
            self.auth()
            return self.get_access_token()
        return token
    
    def get_resource_header(self):
        return {'Authorization': f'Bearer {self.get_access_token()}'}
    
    def get_resource(self, lookup_id, resource_type='albums', version='v1'):
        endpoint = f"https://api.spotify.com/{version}/{resource_type}/{lookup_id}"
        headers = self.get_resource_header()
        r = requests.get(endpoint, headers=headers)
        if r.status_code not in range(200, 300):
            return {}
        return r.json()
    
    def get_album(self, _id):
        return self.get_resource(lookup_id=_id, resource_type='albums')
    
    def get_artist(self, _id):
        return self.get_resource(lookup_id=_id, resource_type='artists')
    
    def base_search(self, query_params):
        headers = self.get_resource_header()
        endpoint = 'https://api.spotify.com/v1/search'

        lookup_url = f"{endpoint}?{query_params}"

        r = requests.get(lookup_url, headers=headers)
        if r.status_code not in range(200, 300):
            return {}
        return r.json()
    
    def search(self, query=None, operator=None, operator_query=None, search_type='artist'):
        if query == None:
            raise Exception('Query is required')
            
        if isinstance(query, dict):
            query = ' '.join([f"{k}:{v}" for k, v in query.items()])
        
        if operator is not None and operator_query is not None:
            if operator.lower() in ['or', 'not']:
                operator = operator.upper()
                if isinstance(operator_query, str):
                    query = f"{query} {operator} {operator_query}"
        
        query_params = urlencode({'q': query, 'type': search_type.lower()})
        return self.base_search(query_params)

