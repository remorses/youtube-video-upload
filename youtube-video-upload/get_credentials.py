
from google_auth_oauthlib.flow import Flow
from colorama import init, Fore

SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

VALID_PRIVACY_STATUSES = ('public', 'private', 'unlisted')





def get_credentials(secrets):
    flow = Flow.from_client_config(
        secrets,
        scopes=SCOPES,
        redirect_uri='urn:ietf:wg:oauth:2.0:oob')

    # Tell the user to go to the authorization URL.
    auth_url, _ = flow.authorization_url(prompt='consent')

    init(autoreset=True)
    print()
    print(Fore.GREEN + 'Please go to this URL: ' + Fore.CYAN + str(auth_url))

    # The user will get an authorization code. This code is used to get the
    # access token.
    print()
    code = input(Fore.GREEN + 'Enter the authorization code: ')
    flow.fetch_token(code=code)
    print()

    return flow.credentials

    # using flow.authorized_session.
    # session = flow.authorized_session()
    # print(session.get('https://www.googleapis.com/userinfo/v2/me').json())
