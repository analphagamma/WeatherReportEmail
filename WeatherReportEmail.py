import json
import sys
from modules.APIagent import *
from modules.Report import *
from modules.EmailClient import *

if __name__ == '__main__':
    # getting api key
    with open('./resources/api.json', 'r') as f:
        key = json.load(f)['key']

    # getting a report
    agent = APIagent('oxford,uk', key)
    api_response = agent.get_forecast()
    print("Status code: {}\n{}".format(api_response['status_code'], api_response['status_message']))
    if api_response['status_code'] != 200:
        sys.exit()
    report = ResponseParser(api_response['content'])
    today = report.parse()

    # getting yesterday's report
    try:
        with open('./resources/yesterday.json', 'r') as f:
            yesterday = json.load(f)
    except:
        yesterday = None
    
    # get email details
    with open('./resources/credentials.json', 'r') as f:
        cred = json.load(f)
    
    # connect and send
    email = EmailBuilder(cred['email'], cred['password'])
    email.connect_to_server()
    content = email.create_email(today, yesterday)
    print('Sending email...')
    email.send_email(cred['to'],
                     content['subject_line'],
                     content['body']
                     )
    print('Email sent.')
    # save report as yesterday's report
    with open('./resources/today.json', 'r') as td, open('./resources/yesterday.json', 'w') as yd:
        tday = json.load(td)
        json.dump(tday, yd)
    sys.exit()

