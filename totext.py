#!/usr/bin/env python

import argparse
import base64
import json
import time

from googleapiclient import discovery
import httplib2
from oauth2client.client import GoogleCredentials

# Application default credentials provided by env variable
# GOOGLE_APPLICATION_CREDENTIALS
def get_speech_service():
    credentials = GoogleCredentials.get_application_default().create_scoped(
        ['https://www.googleapis.com/auth/cloud-platform'])
    http = httplib2.Http()
    credentials.authorize(http)

    return discovery.build('speech', 'v1beta1', http=http)


def main(speech_file, framerate=44100):
    with speech_file as speech:
        # Base64 encode the binary audio file for inclusion in the request.
        speech_content = base64.b64encode(speech.read())

    service = get_speech_service()
    service_request = service.speech().asyncrecognize(
        body={
            'config': {
                # There are a bunch of config options you can specify. See
                # https://goo.gl/EPjAup for the full list.
                'encoding': 'LINEAR16',  # raw 16-bit signed LE samples
                'sampleRate': framerate,  # 16 khz
                # See https://goo.gl/DPeVFW for a list of supported languages.
                'languageCode': 'en-US',  # a BCP-47 language tag
            },
            'audio': {
                'content': speech_content.decode('UTF-8')
            }
        })
    response = service_request.execute()
    print(json.dumps(response))

    name = response['name']
    # Construct a GetOperation request.
    service_request = service.operations().get(name=name)

    while True:
        # Give the server a few seconds to process.
        print('Waiting for server processing...')
        time.sleep(1)
        # Get the long running operation with response.
        response = service_request.execute()

        if 'done' in response and response['done']:
            break

    print(response)
    if 'results' in response['response']:
        print(json.dumps(response['response']['results']))
        return response['response']['results'][0]['alternatives'][0]['transcript']


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'speech_file', help='Full path of audio file to be recognized')
    args = parser.parse_args()
    main(open(args.speech_file, 'rb'))
