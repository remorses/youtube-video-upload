
import json
import os
import requests
from .support import dotdict
from .upload_video import upload_video
# from .get_credentials import get_credentials
from google.oauth2.credentials import Credentials
from .get_category_number import get_category_number
from colorama import init, Fore
from pathlib import Path
from random import random
from .auth import default

SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

def upload_from_options(options):
    """
    local_server: true

    secrets_path: |
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

    credentials = {}
    secrets = {}
    is_local = True

    if 'local_server' in options:
        is_local = options['local_server']

    if 'credentials' in options:
        credentials = Credentials.from_authorized_user_info(json.loads(options.credentials))

    elif 'credentials_path' in options and Path(options.credentials_path).exists():
        credentials = Credentials.from_authorized_user_file(options.credentials_path)

    elif Path('./credentials.json').exists():
        credentials = Credentials.from_authorized_user_file(options.credentials_path)

    elif 'secrets' in options:
        secrets = json.loads(options.secrets)

    elif 'secrets_path' in options and Path(options.secrets_path).exists():
        file = open(options.secrets_path, 'r')
        secrets = json.loads(file.read())
        file.close()

    if secrets.get('web'):
        print('''Warning: you chose a wrong api auth type,
        when creating a new ID client OAut
        you have to choose `other` and not `web application` in google cloud console:
        https://console.cloud.google.com/apis/credentials''')

    secrets = secrets.get('installed') or secrets.get('web')

    if not credentials and secrets:
        # credentials = get_credentials(secrets)
        credentials, _= default(
            SCOPES,
            client_id=secrets['client_id'],
            client_secret=secrets['client_secret'],
            auth_local_webserver=is_local
        )
        save_credentials(credentials, options.credentials_path or "./credentials.json")

    elif not credentials and not secrets:
        raise Exception('neither secrets or credentials')

    for video_options in options.videos:

        if 'category' in video_options:
            video_options['category'] = get_category_number(video_options['category'])

        if 'http' in video_options['file']:
            url = video_options['file']
            temp_file = './' + str(random())[2:] + '.mp4'
            temp_file = download_video(url, temp_file,)
            video_options['file'] = temp_file

        try:
            link = upload_video(
                credentials,
                **video_options
            )

        except Exception as e:
            init(autoreset=True)
            print()
            print(Fore.RED + str(e))

        finally:
            if 'temp_file' in vars() and temp_file:
                Path(temp_file).unlink()

    return link

def download_video(url, file_path):
        response = requests.get(url, stream=True)
        if response.status_code == 200:
                with open(file_path, 'wb') as f:
                    for chunk in response:
                        f.write(chunk)
        return str(Path(file_path).resolve())

def save_credentials(creds, credentials_path):

    creds_data = dump_credentials(creds)

    del creds_data['token']

    secrets_path = os.path.dirname(credentials_path)
    if not os.path.isdir(secrets_path):
        os.makedirs(secrets_path)

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
