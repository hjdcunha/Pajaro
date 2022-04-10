import json

def get_secrets(filename):
    data = open(filename)
    secrets = json.load(data)
    secret = []
    secret.append({
        'api_key': secrets['api_key'],
        'api_key_secret': secrets['api_key_secret'],
        'access_token': secrets['access_token'],
        'access_token_secret': secrets['access_token_secret'],
        'bearer_token': secrets['bearer_token']
    })
    return secret

    


    