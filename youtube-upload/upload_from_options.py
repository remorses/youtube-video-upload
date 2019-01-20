
import json
import os
from .support import dotdict
from .upload_video import upload_video
from .get_credentials import get_credentials
from google.oauth2.credentials import Credentials
from pathlib import Path


def upload_from_options(options):
    """
    config_path: |
        ...

    cresentials_path: |
        credentials

    videos:
        -
            title:  video title
            file:  path
            description: sdf
            category: 22
            privacy: private
            tags:
                - shit
                - holy
    """
    options = dotdict(**options)

    credentials = None
    config = None

    if 'credentials' in options:
        credentials = Credentials.from_authorized_user_info(json.load(options.credentials))

    elif 'credentials_path' in options and Path(options.credentials_path).exists():
        credentials = Credentials.from_authorized_user_file(options.credentials_path)

    elif Path('./credentials.json').exists():
        credentials = Credentials.from_authorized_user_file(options.credentials_path)

    elif 'config' in options:
        config = json.loads(options.config)

    elif 'config_path' in options and Path(options.config_path).exists():
        file = open(options.config_path, 'r')
        config = json.load(file.read())
        file.close()

    if not credentials and config:
        credentials = get_credentials(config)
        save_credentials(credentials, options.credentials_path or "./credentials.json")
    elif not credentials and not config:
        raise Exception('neither config or credentials')

    for video_options in options.videos:
        try:
            upload_video(
                credentials,
                **video_options
            )

        except Exception as e:
            print(e)

    return dump_credentials(credentials)



def save_credentials(creds, credentials_path):

    creds_data = dump_credentials(creds)

    del creds_data['token']

    config_path = os.path.dirname(credentials_path)
    if not os.path.isdir(config_path):
        os.makedirs(config_path)

    with open(credentials_path, 'w') as outfile:
        json.dump(creds_data, outfile)


def dump_credentials(creds):
    creds_data = {
        'token': creds.token,
        'refresh_token': creds.refresh_token,
        'token_uri': creds.token_uri,
        'client_id': creds.client_id,
        'client_secret': creds.client_secret,
        'scopes': creds.scopes
    }
    return creds_data
