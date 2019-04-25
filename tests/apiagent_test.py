import unittest
import json
from modules.APIagent import APIagent

class APIAgentTest(unittest.TestCase):


    def test1_get_forecast_status200(self):
        with open('resources/api.json', 'r') as f:
            API_KEY = json.load(f)['key']
    
        agent = APIagent('oxford,uk', API_KEY)
        self.assertEqual(agent.get_forecast()['status_code'], 200)

    def test2_get_forecast_status404(self):
        with open('resources/api.json', 'r') as f:
            API_KEY = json.load(f)['key']
    
        agent = APIagent('Winterfell', API_KEY)
        self.assertEqual(agent.get_forecast()['status_code'], 404)

    def test3_get_forecast_status401(self):
        with open('resources/api.json', 'r') as f:
            API_KEY = json.load(f)['key']
    
        agent = APIagent('oxford,uk', API_KEY+'blablamessupapikey')
        self.assertEqual(agent.get_forecast()['status_code'], 401)
        
if __name__ == '__main__':
    unittest.main()