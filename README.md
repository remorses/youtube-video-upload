# youtube-video-upload

Upload videos starting from a yaml file.

## Setup

Install dependencies, python-3.x is needed.
```
pip install youtube-video-upload
```

To use this script you need a `client_secrets.json` to put in `secrets_path`.
To get this file:
1. Create an account on the [Google Developers Console](https://console.developers.google.com)
1. Register a new app there
1. Enable the Youtube API (APIs & Auth -> APIs)
1. Create Client ID (APIs & Auth -> Credentials), select 'Other'
1. Download the secrets file clicking on the download icon

Then you will be able to download a file with content similar to this:

```
{
  "installed": {
    "client_id": "xxxxxxxxxxxxxxxxxxx.apps.googleusercontent.com",
    "client_secret": "xxxxxxxxxxxxxxxxxxxxx",
    "redirect_uris": ["http://localhost:8080/oauth2callback"],
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://accounts.google.com/o/oauth2/token"
  }
}
```
Store that file somewhere and update `secrets_path`.

## Usage

To access the youtube api you will need the `secrets` downloaded from the google developers console, then you will be able to create the `credentials` to authorize your requests. For choosing where to store the newly created credentials put a path in `secrets_path` in the yaml file.
To upload the video in `tests/glitch.mp4` simply write a yaml file like this in `tests/example.yaml`:
```yaml
videos:
    -
        title: testing this amazing script!
        file:  tests/video.mp4
        description: sdf
        category: Music
        privacy: private
        tags:
            - shit
            - holy

secrets_path: tests/client_secrets.json      # path for your google secrets
credentials_path:  path/to/credentials.json  # where to store credentials

```
Then execute:
```
pip install youtube-video-upload
python -m youtube_video_upload tests/example.yaml
```
If you run this script for the first time it will ask you to go to a url and copy paste a code to get the credentials.
After that the script will store the credentials in `credentials_path` or default to `./credentials.json`.
Using `credentials_path` the credentials will be created there even if that path doesn't exist.
