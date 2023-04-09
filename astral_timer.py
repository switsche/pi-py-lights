#! /usr/bin/python

import time
import datetime
import logging
import pytz
import astral


class AstralTimer:
    def __init__(self, city_name):
        ast = astral.Astral()
        ast.solar_depression = 'civil'
        self.city_name = city_name
        self.city = ast[city_name]
        self.city_timezone = pytz.timezone(self.city.timezone)
        self.city_info()

    def city_info(self):
        logging.info('Information for {}/{}'.format(self.city_name, self.city.region))
        logging.info('Timezone: {}'.format(self.city_timezone))
        logging.info('Latitude: {:f}; Longitude: {:f}'.format(self.city.latitude, self.city.longitude))

    def blue_hour(self):
        return self.city.blue_hour(astral.SUN_SETTING)

    def sunset_info(self, sun):
        logging.info('Sunset:  {}'.format(str(sun['sunset'])))
        logging.info('Dusk:    {}'.format(str(sun['dusk'])))

    def sunrise_info(self, sun):
        logging.info('Tomorrow dawn: {}'.format(sun['dawn']))
        logging.info('Tomorrow sunrise: {}'.format(sun['sunrise']))

    def compute_duration(self, event_time):
        now = datetime.datetime.now(tz=self.city_timezone)
        duration = (event_time - now).total_seconds() / 2
        return duration

    def wait_until(self, event, date):
        sun = self.city.sun(date=date, local=True)
        event_time = sun[event]
        logging.info("wait until {} on {} which is {}".format(event, date.date(), event_time))
        duration = self.compute_duration(event_time,)
        while duration > 10:
            logging.info("sleeping for {}".format(duration))
            time.sleep(duration)
            duration = self.compute_duration(event_time)
        logging.info("{} happening now".format(event))
