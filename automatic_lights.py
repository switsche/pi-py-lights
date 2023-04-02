import logging
import datetime
import astral_timer

logging.basicConfig(format='%(levelname)s %(asctime)s: %(message)s', level=logging.INFO)

at = astral_timer.AstralTimer('Salem')

day = datetime.datetime.today()

while True:
    at.wait_until('sunset', day)

    at.wait_until('dusk', day)

    day += datetime.timedelta(days=1)