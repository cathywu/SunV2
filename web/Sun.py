import gflags
import httplib2

from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run

import urllib
from datetime import datetime, time, timedelta
import pytz
import pickle
import os

# Sun v2 is a better sun. It is an alarm clock application that emulates the
# rising of the sun at your convenience. It integrates with Google Calendar
# to figure out the best time to wake you each morning.
#
# This is the Google Calendar integration code, which authenticates with gCal,
# pulls relevant calendar events, and sets a "sunrise" time
# 
# @author cathywu
# @date 2012-10-03

PWD = os.path.realpath(__file__).rsplit("/",1)[0]
STORAGE = "%s/.gcalarm" % PWD

class Sun:
    def __init__(self):
        self.service = self.authenticate()
        self.tz = self.get_tz()
        self.wake_time = self.load_alarm_time(\
                default=datetime.combine(datetime.today(), time(16,0)))

        # update time, in case of failure, will use stored time
        try:
            self.update_alarm_time()
        except Exception as detail:
            print "Error details: %s" % detail
            print "Current alarm time: %s" % self.wake_time

    def authenticate(self):
        FLAGS = gflags.FLAGS
        
        # Set up a Flow object to be used if we need to authenticate. This
        # sample uses OAuth 2.0, and we set up the OAuth2WebServerFlow with
        # the information it needs to authenticate. Note that it is called
        # the Web Server Flow, but it can also handle the flow for native
        # applications
        # The client_id and client_secret are copied from the API Access tab on
        # the Google APIs Console
        FLOW = OAuth2WebServerFlow(
            client_id='515737487015-gjgvprnb0kcsujshcot32utrr5g1elj3.apps.googleusercontent.com',
            client_secret='p5Cg3hJpjlu50_AzpOPPAkLR',
            scope='https://www.googleapis.com/auth/calendar',
            user_agent='Sun/2')
        
        # To disable the local server feature, uncomment the following line:
        # FLAGS.auth_local_webserver = False
        
        # If the Credentials don't exist or are invalid, run through the native
        # client flow. The Storage object will ensure that if successful the
        # good Credentials will get written back to a file.
        storage = Storage('%s/calendar.dat' % PWD)
        credentials = storage.get()
        if credentials is None or credentials.invalid == True:
          credentials = run(FLOW, storage)
        
        # Create an httplib2.Http object to handle our HTTP requests and
        # authorize it with our good Credentials.
        http = httplib2.Http()
        http = credentials.authorize(http)
        
        # Build a service object for interacting with the API. Visit
        # the Google APIs Console
        # to get a developerKey for your own application.
        service = build(serviceName='calendar', version='v3', http=http,
               developerKey='AIzaSyCUNF_vKM-4QoexKi7DMx2RyGTtkJVcS8Q')
        return service

    def get_tz(self):
        # get timezone, turn into UTC offset
        tz = [setting['value'] for setting in \
                self.service.settings().list().execute()['items'] if \
                setting['id']=='timezone'][0]
        tz = datetime.now(pytz.timezone(tz)).strftime('%z')
        return tz

    def load_alarm_time(self, default=None):
        import os
        if not os.path.isfile(STORAGE):
            return default
        # check for unupdated alarm time (perhaps from loss of internet conn)
        if abs(datetime.fromtimestamp(os.path.getmtime(STORAGE))-datetime.now()) \
                > timedelta(hours=18):
            return default
        alarm_time = pickle.load(open(STORAGE))
        # check for stale alarm time (from yesterday, etc.)
        if alarm_time < datetime.combine(datetime.today(), time(0,0)):
            return default
        return alarm_time

    def save_alarm_time(self):
        out = open(STORAGE, 'w')
        pickle.dump(self.wake_time,out)

    def update_alarm_time(self):
        # if datetime.now() > self.wake_time: # done for today
        #     return None
        
        start_time = datetime.combine(datetime.today(), time(0,0))
        gtime_format = "%Y-%m-%dT%H:%M:%S"
        start_time_gg = "%s%s" % (start_time.strftime(gtime_format),self.tz)
        wake_time_gg = "%s%s" % (self.wake_time.strftime(gtime_format),self.tz)
        
        all_calendars = self.service.calendarList().list().execute()['items']
        my_calendars = [cal for cal in all_calendars if \
                cal['accessRole']=='owner']
        
        # print "Calendars: %s" % [cal['summary'] for cal in my_calendars]
        for cal in my_calendars:
            events = self.service.events().list(calendarId=cal['id'],
                    timeMin=start_time_gg,timeMax=wake_time_gg).execute()
            if 'items' in events:
                events = events['items']
            else:
                continue
            # print "%s: %s events" % (cal['summary'], len(events))
            for event in events:
                # skip cancelled events, full day events
                if 'summary' not in event or 'dateTime' not in event['start']:
                    continue
                # omit timezone
                start = datetime.strptime(event['start']['dateTime'][:-6],
                        "%Y-%m-%dT%H:%M:%S")
        
                # check if we have found the rise and shine event for today
                if event['summary'] == 'rise and shine' and start.date() == \
                        datetime.today().date():
                    self.wake_time = start - timedelta(minutes=30)
                    print "RISE AND SHINE: %s" % self.wake_time
                    return self.wake_time
                # for events that are today, check if it's earlier than what we
                # have recorded for wake_time
                if start.date() == datetime.today().date():
                    if start < self.wake_time:
                        self.wake_time = start - timedelta(minutes=30)
                        print "NEW SUNRISE TIME: %s" % self.wake_time
        self.save_alarm_time()
        return self.wake_time

if __name__ == "__main__":
    s = Sun()
    print s.wake_time
