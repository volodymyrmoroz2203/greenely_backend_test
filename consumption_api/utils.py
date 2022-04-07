import re
from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta
from django.db.models import Min, Max

date_regex = r'\d{4}-\d{2}-\d{2}'


def get_date_from_datetime(datetime_str):
    """For timestamp fields convert datetime to date for API responses."""
    return re.match(date_regex, datetime_str).group(0)


def is_date_valid(date_str):
    """Check if date in request is valid."""
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def is_count_valid(count_text):
    """Check if count in request is valid."""
    try:
        count = int(count_text)
        if count > 0:
            return True
    except ValueError:
        return False


def get_end_date(start_date_str, count, resolution):
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    time_difference = timedelta(days=count) if resolution.lower() == 'd' else relativedelta(months=+count)
    return start_date + time_difference


def get_min_max(stats, aggregation):
    """Returns minimum and maximum values of aggregation field."""
    minimum = stats.aggregate(Min(aggregation))[f'{aggregation}__min']
    maximum = stats.aggregate(Max(aggregation))[f'{aggregation}__max']
    return {'minimum': get_date_from_datetime(minimum) if aggregation == 'timestamp' else minimum,
            'maximum': get_date_from_datetime(maximum) if aggregation == 'timestamp' else maximum}


def get_limits_dict(stats):
    """Return dict with limits of needed fields."""
    return {'timestamp': get_min_max(stats, 'timestamp'),
            'consumption': get_min_max(stats, 'consumption'),
            'temperature': get_min_max(stats, 'temperature')}
