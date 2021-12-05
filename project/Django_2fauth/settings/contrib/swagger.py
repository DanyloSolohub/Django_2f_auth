import os

SWAGGER_SETTINGS = {
    'PERSIST_AUTH': True,
    'SECURITY_DEFINITIONS': {
        'Basic': {
            'type': 'basic'
        },
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    }
}

SWAGGER_URL = os.getenv('SWAGGER_URL', None)
