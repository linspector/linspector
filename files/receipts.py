# some python receipts for different stuff

# get system timezone name
# https://stackoverflow.com/questions/1111056/get-time-zone-information-of-the-system-in-python
import datetime
tz_string = datetime.datetime.now(datetime.timezone.utc).astimezone().tzname()
