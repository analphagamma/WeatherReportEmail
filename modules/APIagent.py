import requests
import json

class APIagent:

    def __init__(self, location, api_key):
        self.location = location
        self.api_key = api_key

    def get_forecast(self):
        '''
        Connects to the website's API, sends a request
        and returns the content in JSON.
        '''
        r = requests.get('http://api.openweathermap.org/data/2.5/forecast?q={}&APPID={}&units=metric'.format(self.location, self.api_key))
        STATUS_MESSAGE = {200: 'Request OK',
                          404: 'API call not valid. Please check location info and API key.',
                          401: 'Authentication error. Check API key and make sure it has been activated.'}

        return {'status_code': r.status_code,
                'status_message': STATUS_MESSAGE[r.status_code],
                'content': json.loads(r.content.decode('utf-8'))}