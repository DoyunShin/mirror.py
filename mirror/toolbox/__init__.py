import re

def iso_duration_parser(iso8601: str) -> int: # ISO 8601 Parser
    """
    ISO8601 Durations Parser.
    Only supports days, hours, minutes, and seconds.
    """
    match = re.match(
        r'P((?P<years>\d+)Y)?((?P<months>\d+)M)?((?P<weeks>\d+)W)?((?P<days>\d+)D)?(T((?P<hours>\d+)H)?((?P<minutes>\d+)M)?((?P<seconds>\d+)S)?)?',
        iso8601
    ).groupdict()
    return int(match['days'] or 0)*24*3600 + \
        int(match['hours'] or 0)*3600 + \
        int(match['minutes'] or 0)*60 + \
        int(match['seconds'] or 0)

def iso_duration_maker(duration: int) -> str:
    """
    ISO8601 Durations Maker.
    Only supports days, hours, minutes, and seconds. (MAX: 31 days)
    """
    if duration < 0:
        raise ValueError("Duration must be a positive integer.")
    if duration > 2678399:
        raise ValueError("Duration must be less than 31 days.")
    
    dates = [24*3600, 3600, 60, 1]
    names = ["D", "H", "M", "S"]
    iso8601 = "P"
    for i in range(len(dates)):
        if names[i] == "D": iso8601 += "T"
        if unixtime >= dates[i]:
            iso8601 += f"{unixtime // dates[i]}{names[i]}"
            unixtime %= dates[i]
    return iso8601