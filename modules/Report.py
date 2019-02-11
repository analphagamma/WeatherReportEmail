import datetime as dt
import time
import json


class DailyWeather:
    '''
    A collection of weather data for the entire day.
    '''
    def __init__(self, todays_date):
        ''' 
        temps -> dictionary that holds all temperature reports from the day {hour: temp}
        wind_high -> float - it stores the highest wind speed in float
        all_conditions -> dictionary that holds all weather conditions during the day as {hour: condition}
        '''
        self.todays_date = todays_date
        self.temps = {}
        self.wind_high = 0
        self.conditions = {}

    def add_temps(self, hour, temp):
        '''
        Adds a temperature value with time to the record
        hour -> str
        temp -> float
        '''
        self.temps[hour] = temp

    def get_temp_high(self):
        '''
        Returns the highest temperature value
        '''
        warmest_hour = max(self.temps, key=self.temps.get)
        return {'hour': warmest_hour, 'temp': self.temps[warmest_hour]}

    def get_temp_low(self):
        '''
        Returns the lowest temperature value
        '''
        coldest_hour = min(self.temps, key=self.temps.get)
        return {'hour': coldest_hour, 'temp': self.temps[coldest_hour]}

    def set_wind_high(self, wind):
        '''
        Changes the wind_high attribute if wind is higher than the current wind_high
        '''
        if wind > self.wind_high:
            self.wind_high = wind
        else:
            pass

    def get_wind_high(self):
        '''
        Returns the highest wind speed recorded.
        '''
        return self.wind_high

    def add_condition(self, cond, hour):
        '''
        Adds a weather condition value with time to the record
        hour -> str
        cond -> str
        '''
        if not self.conditions.get(cond):
            self.conditions[cond] = [hour]
        else:
            self.conditions.get(cond).append(hour)

    def get_condition_by_hour(self, hour):
        pass

    def get_condition_by_description(self, cond):
        pass

    def add_report(self, report):
        '''
        Adds an hourly report extracted from the api response.
        report_obj is a WeatherPerHour object
        '''

        self.add_condition(report['conditions'], report['hour'])
        self.add_temps(report['hour'], report['temp'])
        self.set_wind_high(report['wind'])


    def get_report(self):
        '''
        Gathers all data in the report, organises it and
        returns it in a dictionary.
        '''
        # if there's going to be rain, snow or thunderstorm the email is sent
        trigger_warning = False
        for key in self.conditions.keys():
            for con in ['rain', 'snow', 'thunderstorm']:
                if con in key:
                    trigger_warning = True

        # build report
        report =  {
                'temp_low': self.get_temp_low(),
                'temp_high': self.get_temp_high(),
                'wind': int(self.get_wind_high()*3.6),
                'conditions': list(set(self.conditions.keys())),
                'most_frequent_condition': '',
                'rain_times': self.conditions.get('rain'),
                'snow_times': self.conditions.get('snow'),
                'thunderstorm_times': self.conditions.get('thunderstorm'),
                'trigger_warning': trigger_warning,
                'date': str(self.todays_date + dt.timedelta(days=1))
                }

        # save report
        with open('./resources/yesterday.json', 'w+') as f:
            json.dump(report, f)

        return report

    
class ResponseParser:

    def __init__(self, response, todays_date=dt.date.today()):
        '''
        response -> a JSON response content from the OpenWeather API
        daily_weather -> an empty DailyWeather object
        '''
        self.response = response
        self.todays_date = todays_date
        self.daily_weather = DailyWeather(self.todays_date)

    def parse(self):
        '''
        Parses the JSON reposponse from the API, disassembles the data and
        fills up the DailyWeather object with the forecast data.
        Returns a dictionary.
        '''
        for report in self.response['list']:
            # extract date and time
            report_date = dt.datetime.strptime(report['dt_txt'], '%Y-%m-%d %H:%M:%S').date()
            report_time = dt.datetime.strptime(report['dt_txt'][-8:], '%H:%M:%S')
            # if British Summer Time we convert UTC to GMT - fuck timezones btw
            if time.localtime()[-1] == 1:
                report_time += dt.timedelta(hours=1)
            report_time = report_time.time()
            # we only care about tomorrow's forecast
            if (self.todays_date + dt.timedelta(days=1)) != report_date:
                next
            else:
                # add weather data to object
                self.daily_weather.add_report({'hour': str(report_time), 
                                               'temp': float(report['main']['temp']),
                                               'conditions': report['weather'][0]['description'],
                                               'wind': float(report['wind']['speed'])
                                            }
                                        )
        return self.daily_weather.get_report()
