import xmlrpc.client

url = 'http://localhost:8069'
username = 'admin'
password = 'admin'
db = 'real_estate_db_2'

common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
user_uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')

property_ids = models.execute_kw(db, user_uid, password, 'estate.property', 'search', [[]])

property_read = models.execute_kw(db, user_uid, password, 'estate.property', 'read', [property_ids], {'fields': ['name']})

print(property_read)