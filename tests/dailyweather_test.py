import unittest
import datetime as dt
import json
from modules.Report import DailyWeather, ResponseParser

class DailyWeatherTest(unittest.TestCase):

    TODAY = dt.datetime.strptime('2019-01-19', '%Y-%m-%d').date()
    w = DailyWeather(TODAY)

    def test01_addtemps(self):
        '''
        Adds two values to the instance variable by using its method and tests if
        values are present.
        '''
        self.w.add_temps('03:00', 10)
        self.assertEqual(self.w.temps, {'03:00': 10})
        self.w.add_temps('06:00', 15)
        self.assertEqual(self.w.temps, {'03:00': 10, '06:00': 15})

    def test02_gettemphigh(self):
        '''
        Gets the highest temperature value and the hour.
        '''
        self.assertEqual(self.w.get_temp_high()['hour'], '06:00')
        self.assertEqual(self.w.get_temp_high()['temp'], 15)

    def test03_gettemplow(self):
        '''
        Gets the lowest temperature value and the hour.
        '''
        self.assertEqual(self.w.get_temp_low()['hour'], '03:00')
        self.assertEqual(self.w.get_temp_low()['temp'], 10)

    def test04_setgetwindhigh(self):
        self.w.set_wind_high(10) # input is in m/s
        self.w.set_wind_high(5)
        self.assertEqual(self.w.get_wind_high(), 10)
        self.w.set_wind_high(20)
        self.assertEqual(self.w.get_wind_high(), 20)

    def test05_addcondition(self):
        self.w.add_condition('rain', '03:00')
        self.assertEqual(self.w.conditions, {'rain': ['03:00']})

    def test06_getconditionbyhour(self):
        pass

    def test07_getconditionbydesc(self):
        pass

    def test08_addreport(self):
        self.w.add_report({'hour': '12:00',
                           'temp': 20,
                           'conditions': 'snow',
                           'wind': 100})

        self.assertEqual(self.w.temps['12:00'], 20)
        self.assertEqual(self.w.wind_high, 100)
        self.assertEqual(self.w.conditions['snow'], ['12:00'])


    def test09_getreport(self):
        report = self.w.get_report()

        self.assertEqual(report['temp_low'], {'hour': '03:00', 'temp': 10})
        self.assertEqual(report['temp_high'], {'hour': '12:00', 'temp': 20})
        self.assertEqual(report['wind'], 360) # output is in km/h
        self.assertEqual(report['trigger_warning'], True)

    def test10_produce_report_output(self):
        '''
        This test produces a JSON file with a full report
        for use in the email_test.py test.
        '''
    
        with open('resources/sample.json', 'r') as f:
            weather_data = json.load(f)
        
        rp = ResponseParser(weather_data, todays_date=self.TODAY)
        report_output = rp.parse()
        with open('test_output.json', 'w+') as f:
            json.dump(report_output, f)

if __name__ == '__main__':
    unittest.main(verbosity=3)