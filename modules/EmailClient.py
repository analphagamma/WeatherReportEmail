import smtplib
from email.message import EmailMessage
import sys


class EmailBuilder:
    '''
    Establishes the SMTP server connection and sends the email.
    It should be instantiated with a valid email-password pair

    You can add an SMTP server but the default is gmail
    '''

    def __init__(self, email, password, smtp_server='smtp.gmail.com'):
        self.smtp_server = smtp_server
        self.email = email
        self.password = password

    def create_email(self, report, last_report):
        '''
        Assembles the email body and subject line from today's and yesterday's report
        report and last_report are both dictionaries that are the output of the Report module
        Returns a dictionary where values are strings
        '''
        header     = 'Weather forecast for {}\n'.format(report['date'])
        conditions = 'Tomorrow expect {}.\n'.format(', '.join(report['conditions']))
        low_temp   = 'The lowest temperature will be {}\u2103 at {}\n'.format(report['temp_low']['temp'], report['temp_low']['hour'][:-3])
        high_temp  = 'The highest temperature will be {}\u2103 at {}\n'.format(report['temp_high']['temp'], report['temp_high']['hour'][:-3])
        wind       = 'Winds will be up to {}km/h\n'.format(report['wind'])

        warning = '======================\n'
        if report['trigger_warning']:
            warning += 'There will be'
            if report['snow_times']:
                warning += ' snow at {}'.format(', '.join(report['snow_times']))
            if report['rain_times']:
                warning += ' rain at {}'.format(', '.join(report['rain_times']))
            if report['thunderstorm_times']:
                warning += ' a thunderstorm at {}'.format(', '.join(report['thunderstorm_times']))

            warning += '.\nHave a nice day!'

        # build subject line
        subject = 'Tomorrow: '
        if last_report:
            # if there's no last report record, we skip this part
            if report['temp_high']['temp'] > last_report['temp_high']['temp'] + 5:
                subject += ' warmer temperatures '
            elif (report['temp_low']['temp'] < last_report['temp_low']['temp'] - 5) or report['temp_high']['temp'] > last_report['temp_high']['temp'] - 5:
                subject += ' colder temperatures '

        subject += ', '.join(report['conditions'])

        return {'subject_line': subject,
                'body': header+conditions+low_temp+high_temp+wind+warning}


    def connect_to_server(self):
        '''
        Connects to the SMTP server and makes sure the authentication is correct
        If the connection it will exit.
        '''
        # establishing server connection
        self.server = smtplib.SMTP(self.smtp_server, 587)
        self.server.starttls()
        # logging in
        self.server.login(self.email, self.password) # add exception handling and logging

    def send_email(self, sent_to, subject_line, body, sent_from='Weather Bot'):
        '''
        Sends an email that was built by the create_email method
        all arguments are strings but the sent_to must be a valid email address
        '''

        self.subject_line = subject_line
        self.body = body
        self.sent_from = sent_from
        self.sent_to = sent_to
        msg = EmailMessage()
        msg.set_content(self.body)
        for k, v in zip(['Subject', 'To', 'From'], [self.subject_line, self.sent_to, self.sent_from+"<{}>".format(self.email)]):
            msg[k] = v
        try:
            self.server.send_message(msg)
        except Exception as e:
            print('Could not send email\n', e)
            self.server.quit()
            sys.exit()
        else:
            self.server.quit()


