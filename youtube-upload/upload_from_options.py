
import json

from .support import dotdict
from .upload_video import upload_video
from .get_credentials import get_credentials


def upload_from_options(options):
    """
    config_file: |
        ...

    cresentials: |
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



    if 'credentials' in options:
        credentials = options.credentials

    elif 'credentials_path' in options:
        file = open(options.credentials_path, 'r')
        credentials = ''#TODO

    elif 'config' in options:
        config = json.loads(options.config)
        credentials = get_credentials(config)

    elif 'config_path' in options:
        file = open(options.config_path, 'r')
        credentials = ''#TODO

    else:
        raise Exception('neither config or credentials')

    for video_options in options.videos:

        try:
            upload_video(
                credentials,
                **video_options
            )

        except Exception as e:
            print(e)

    return dotdict(**options, credentials=credentials)
