import urllib.request
import random
import json

url = 'http://localhost:8069'
username = 'admin'
password = 'admin'
db = 'real_estate_db_2'

def json_rpc(url, method, params):
    data = {
        'jsonrpc': '2.0',
        'method': method,
        'params': params,
        'id': random.randint(0, 1000000000)
    }
    headers = {
        'Content-Type': 'application/json',
    }
    req = urllib.request.Request(url=url,data=json.dumps(data).encode(),headers=headers)
    
    res = json.loads(urllib.request.urlopen(req).read().decode('UTF-8'))
    
    if res.get('error'):
        raise Exception(res['error'])
    
    return res['result']


def call(url, service, method, *args):
    return json_rpc(f"{url}/jsonrpc", 'call', {'service': service, 'method': method, 'args': args})

user_id = call(url, 'common', 'login', db, username, password)

vals = {
    'name': 'Property from JSON',
    'sales_id': 6
}

create_property = call(url, 'object', 'execute', db, user_id, password, 'estate.property', 'create', vals)
print(create_property)