from modules.EmailClient import EmailBuilder
import unittest
import json

class EmailTest(unittest.TestCase):

    def test1_connion(self):
        pass

    @unittest.skip('Skip - not sending email')
    def test2_sending(self):
        with open('credentials.json', 'r+') as f: 
            cred = json.load(f)

        client = EmailBuilder(cred['email'], cred['password'])
        client.connect_to_server()
        client.send_email(cred['to'], 'Test Subj Line', 'This is the body of the test message', cred['from'])

    @unittest.skip('Not needed now.')
    def test3_creation(self):
        with open('test_output.json', 'r+') as f:
            report = json.load(f)
        
        client = EmailBuilder(None, None)
        print(client.create_email(report, None))

    #@unittest.skip('Skip - not sending email')
    def test4_email(self):

        # setting up email server
        with open('credentials.json', 'r+') as f: 
            cred = json.load(f)

        client = EmailBuilder(cred['email'], cred['password'])
        client.connect_to_server()

        # getting content
        with open('test_output.json', 'r+') as f:
            report = json.load(f)

        content = client.create_email(report, None)

        # sending email
        client.send_email(cred['to'], content['subj_line'], content['body'])




if __name__ == '__main__':
    unittest.main()