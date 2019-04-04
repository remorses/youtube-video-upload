
import random
import time
from http import client
import httplib2

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload


# Explicitly tell the underlying HTTP transport library not to retry, since
# we are handling retry logic ourselves.
httplib2.RETRIES = 1

# Maximum number of times to retry before giving up.
MAX_RETRIES = 10

# Always retry when these exceptions are raised.
RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error, IOError, client.NotConnected,
    client.IncompleteRead, client.ImproperConnectionState,
    client.CannotSendRequest, client.CannotSendHeader,
    client.ResponseNotReady, client.BadStatusLine)

# Always retry when an apiclient.errors.HttpError with one of these status
# codes is raised.
RETRIABLE_STATUS_CODES = [500, 502, 503, 504]

VALID_PRIVACY_STATUSES = ('public', 'private', 'unlisted')




def upload_video(
        credentials,
        file,
        title='video title',
        description='video sescription',
        category=22,
        privacy='private',
        tags=[]
    ):
    """
    youtube is made with get_authenticated_service()
    category is a number, see https://developers.google.com/youtube/v3/docs/videoCategories/list for more
    raises HttpError if connection error
    """
    youtube_service = build('youtube', 'v3', credentials=credentials)

    body=dict(
        snippet=dict(
            title=title,
            description=description,
            tags=tags,
            categoryId=category
        ),
        status=dict(
            privacyStatus=privacy
        )
    )

    # Call the API's videos.insert method to create and upload the video.
    insert_request = youtube_service.videos().insert(
        part=','.join(body.keys()),
        body=body,
        # The chunksize parameter specifies the size of each chunk of data, in
        # bytes, that will be uploaded at a time. Set a higher value for
        # reliable connections as fewer chunks lead to faster uploads. Set a lower
        # value for better recovery on less reliable connections.
        #
        # Setting 'chunksize' equal to -1 in the code below means that the entire
        # file will be uploaded in a single HTTP request. (If the upload fails,
        # it will still be retried where it left off.) This is usually a best
        # practice, but if you're using Python older than 2.6 or if you're
        # running on App Engine, you should set the chunksize to something like
        # 1024 * 1024 (1 megabyte).
        media_body=MediaFileUpload(file, chunksize=-1, resumable=True)
    )

    return resumable_upload(insert_request)

# This method implements an exponential backoff strategy to resume a
# failed upload.
def resumable_upload(request):
    response = None
    error = None
    retry = 0
    while response is None:
        try:
            print()
            print( 'Uploading file...')
            status, response = request.next_chunk()
            if response is not None:
                # print(response)
                if 'id' in response:
                    print()
                    print( 'Video id "%s" was successfully uploaded.' % response['id'])
                    return f'https://www.youtube.com/watch?v={response["id"]}'
                else:
                    exit('The upload failed with an unexpected response: %s' % response)
        except HttpError as e:
            if e.resp.status in RETRIABLE_STATUS_CODES:
                error = 'A retriable HTTP error %d occurred:\n%s' % (e.resp.status, e.content)
            else:
                raise
        except RETRIABLE_EXCEPTIONS as e:
            error = 'A retriable error occurred: %s' % e

        if error is not None:
            print( error)
            retry += 1
            if retry > MAX_RETRIES:
                exit('No longer attempting to retry.')

            max_sleep = 2 ** retry
            sleep_seconds = random.random() * max_sleep
            print( 'Sleeping %f seconds and then retrying...' % sleep_seconds)
            time.sleep(sleep_seconds)
