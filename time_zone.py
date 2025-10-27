import pytz

# Get all American timezones
american_timezones = [tz for tz in pytz.all_timezones if tz.startswith('America/')]

# Print the list
for tz in american_timezones:
    print(tz)